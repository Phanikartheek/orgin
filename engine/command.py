import pyttsx3
import speech_recognition as sr
import time
import eel
import webbrowser
import pywhatkit  # optional for YouTube play

# ------------------- Initialize Eel -------------------
eel.init('web')  # Replace 'web' with your HTML folder

# ------------------- Text-to-Speech -------------------
def speak(text):
    """
    Convert text to speech using pyttsx3 and optionally display it in Eel.
    """
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 174)
        try:
            eel.DisplayMessage(text)
        except:
            print(f"[EEL] {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS ERROR] {e}")

# ------------------- Speech Recognition -------------------
def takecommand(timeout=10, phrase_time_limit=6):
    """
    Listen to microphone input and return recognized text.
    Returns empty string if recognition fails.
    """
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("[INFO] Listening...")
            try:
                eel.DisplayMessage('Listening...')
            except:
                pass

            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("[INFO] Recognizing...")
        try:
            eel.DisplayMessage('Recognizing...')
        except:
            pass

        query = r.recognize_google(audio, language='en-in')
        print(f"[USER] {query}")
        try:
            eel.DisplayMessage(query)
        except:
            pass
        return query.lower()

    except sr.WaitTimeoutError:
        print("[WARN] Listening timed out")
    except sr.RequestError:
        print("[ERROR] Could not request results from Google Speech Recognition")
    except sr.UnknownValueError:
        print("[WARN] Could not understand audio")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    return ""  # return empty string if anything fails

# ------------------- Feature Functions -------------------
def openCommand(query):
    """Open websites or apps based on user query"""
    try:
        if "youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
        elif "google" in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")
        else:
            speak("I can't open that")
    except Exception as e:
        print(f"[ERROR] {e}")

def PlayYoutube(query):
    """Play YouTube videos using pywhatkit"""
    try:
        song = query.replace("on youtube", "").replace("play", "").strip()
        pywhatkit.playonyt(song)
        speak(f"Playing {song} on YouTube")
    except Exception as e:
        print(f"[ERROR] {e}")

# ------------------- Commands Handler -------------------
@eel.expose
def allCommands():
    """
    Eel-exposed function that listens to command and executes it.
    """
    query = takecommand()
    if not query:
        print("[INFO] No command detected")
        return

    try:
        if "open" in query:
            openCommand(query)
        elif "on youtube" in query or "play" in query:
            PlayYoutube(query)
        else:
            speak("Command not recognized")
            print("[INFO] Command not recognized")
    except Exception as e:
        print(f"[ERROR] Command execution failed: {e}")

    # Show Hood in UI if available
    try:
        eel.ShowHood()
    except:
        pass

# ------------------- Start Eel -------------------
if __name__ == "__main__":                                                                                                                                                                                                                                                                                                     
    eel.start('index.html', size=(800, 600), block=True)
