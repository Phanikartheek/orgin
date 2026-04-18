"""
Jarvis AI Brain — Gemini Agent with Function Calling
This is the core intelligence of Jarvis. Instead of keyword matching,
Gemini decides which tool to call based on natural language understanding.
"""

import asyncio
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, ASSISTANT_NAME
from app.agent.memory import ConversationMemory

# Import all tool functions
from app.agent.tools.app_launcher import open_application, open_website
from app.agent.tools.youtube import play_youtube
from app.agent.tools.communication import (
    send_whatsapp_message,
    make_whatsapp_call,
    make_whatsapp_video_call,
    make_phone_call,
    send_sms,
)
from app.agent.tools.contacts import find_contact, add_contact, list_contacts
from app.agent.tools.system import (
    get_current_time,
    get_current_date,
    set_system_volume,
    take_screenshot,
)

# System prompt that defines Jarvis's personality and behavior
SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, an advanced AI-powered personal assistant.

## Your Personality:
- You are intelligent, witty, and helpful — inspired by J.A.R.V.I.S. from Iron Man
- You address the user as "Sir" occasionally
- Keep responses concise and natural for voice output (2-3 sentences max)
- Be proactive — suggest related actions when appropriate

## Your Capabilities:
You have access to tools that let you control the computer and communicate on behalf of the user.
Always use the appropriate tool when the user asks you to perform an action.
If the user is just chatting or asking a question, respond conversationally without using tools.

## Important Rules:
1. When opening apps/websites, use the appropriate tool — don't just describe how to do it
2. For music/video requests, always use the play_youtube tool
3. For messages/calls, execute the requested tool immediately. DO NOT ask for confirmation unless the user's request is ambiguous.
4. Keep spoken responses SHORT — they will be read aloud via text-to-speech
5. If you don't know something, say so honestly
6. ALWAYS use tools for actions — never just describe steps
7. If the user asks to "open whatsapp and call...", just use the whatsapp call tool directly. It opens whatsapp automatically.
"""

# Collect all tools into a list
ALL_TOOLS = [
    open_application,
    open_website,
    play_youtube,
    send_whatsapp_message,
    make_whatsapp_call,
    make_whatsapp_video_call,
    make_phone_call,
    send_sms,
    find_contact,
    add_contact,
    list_contacts,
    get_current_time,
    get_current_date,
    set_system_volume,
    take_screenshot,
]

# Map function names to actual functions for manual calling
TOOL_MAP = {func.__name__: func for func in ALL_TOOLS}


class JarvisBrain:
    """The AI brain that processes user queries and decides actions."""

    def __init__(self):
        self.init_error = None
        try:
            # If we have a key from our config, use it. 
            # Otherwise, call Client() without args to let it auto-detect GOOGLE_API_KEY from Render.
            if GEMINI_API_KEY:
                self.client = genai.Client(api_key=GEMINI_API_KEY)
            else:
                self.client = genai.Client() 
        except Exception as e:
            self.init_error = str(e)
            print(f"[Brain Error] Failed to initialize Gemini client: {e}")
            self.client = None
        self.memory = ConversationMemory()
        self.model = "gemini-2.0-flash"

    async def think(self, user_input: str) -> str:
        """
        Process user input through Gemini with function calling.
        Returns the assistant's text response.
        """
        # Safety Check: If client failed to initialize (usually due to missing API Key)
        if not self.client:
            return f"Sir, I am unable to connect to my AI brain. Error: {self.init_error or 'Unknown initialization failure'}. Please check your GEMINI_API_KEY in Render."

        # Add user message to memory
        self.memory.add_message("user", user_input)

        try:
            # Build conversation for Gemini
            contents = self.memory.get_gemini_contents()

            # Call Gemini with tools (disable auto-calling so we control execution)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        tools=ALL_TOOLS,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                        temperature=0.7,
                        max_output_tokens=500,
                    ),
                )
            )

            # Check if Gemini wants to call a function
            if response.function_calls:
                tool_results = []
                for fc in response.function_calls:
                    func_name = fc.name
                    func_args = fc.args or {}

                    print(f"[Brain] Calling tool: {func_name}({func_args})")

                    # Execute the tool function
                    if func_name in TOOL_MAP:
                        try:
                            result = await loop.run_in_executor(
                                None,
                                lambda f=func_name, a=func_args: TOOL_MAP[f](**a)
                            )
                            print(f"[Brain] Tool result: {result}")
                            tool_results.append(result)
                        except Exception as te:
                            result = f"Tool error: {str(te)}"
                            print(f"[Brain] Tool error: {te}")
                            tool_results.append(result)
                    else:
                        tool_results.append(f"Unknown tool: {func_name}")

                # Build a response from tool results
                combined_result = "; ".join(tool_results)

                # Send the tool results back to Gemini for a natural response
                followup_contents = contents + [
                    {"role": "model", "parts": [{"text": f"I executed the following action: {combined_result}"}]},
                    {"role": "user", "parts": [{"text": f"The action result was: {combined_result}. Give a brief, natural confirmation to the user."}]},
                ]

                followup = await loop.run_in_executor(
                    None,
                    lambda: self.client.models.generate_content(
                        model=self.model,
                        contents=followup_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.7,
                            max_output_tokens=200,
                        ),
                    )
                )

                assistant_response = followup.text if followup.text else combined_result

            else:
                # No function call — just a text response
                assistant_response = response.text if response.text else "I'm not sure how to help with that, Sir."

            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_response)
            return assistant_response

        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            print(f"[Brain Error] {e}")
            return error_msg

    def reset_memory(self):
        """Clear conversation history."""
        self.memory.clear()
