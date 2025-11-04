import os
import webbrowser

apps = {
    "notepad": "notepad.exe",
    "onenote": r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
}

def open_app(app_name):
    app_name = app_name.lower()
    if app_name in apps:
        path = apps[app_name]
        if path.startswith("http"):   # 🌐 If it’s a website
            webbrowser.open(path)
            print(f"Opening website: {path}")
        else:                         # 🖥️ If it’s a local app
            os.startfile(path)
            print(f"Opening app: {app_name}")
    else:
        print(f"App '{app_name}' not found.")
