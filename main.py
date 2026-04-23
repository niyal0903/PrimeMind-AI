# import speech_recognition as sr
# import webbrowser
# import pyttsx3
# import os
# import datetime
# from iron_gui import IronManHUD
# import tkinter as tk
# from airdrawing import start_drawing

# root = tk.Tk()
# hud = IronManHUD(root)

# recognizer = sr.Recognizer()
# # engine = pyttsx3.init()
# engine = pyttsx3.init()      # Windows ke liye best

# voices = engine.getProperty('voices')

# engine.setProperty('voice', voices[0].id)   # Agar sound na aaye to voices[1] try karo
# engine.setProperty('rate', 170)
# engine.setProperty('volume', 1.0)


# def speak(text):
#     print("jarvis",text)
#     engine.stop()
#     engine.say(text)
#     engine.runAndWait()

# if __name__ == "__main__":
#     speak("Jarvis is online tell me sir...")

#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source, duration=0.5)

#         while True:
            
#             try:
#                 print("Listening...")
#                 audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

#                 print("Recognizing...")
#                 command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
#                 print(command)

#                 if any(word in command for word in ["jarvis","jar wis", "service", "travis", "jervis"]):
#                     print("wake word dtected")
#                     speak("Yes sir")
#                     continue

#                 elif "open google" in command:
#                     speak("Opening Google, sir")
#                     webbrowser.open("https://google.com")

#                 elif "open youtube" in command:
#                     speak("Opening YouTube, sir")
#                     webbrowser.open("https://youtube.com")

#                 elif "open" in command and "channel" in command:
#                     speak("Opening the channel, sir")
#                     channel_name = command.replace("open", "").replace("channel", "").strip()
#                     url = f"https://www.youtube.com/results?search_query={channel_name}"
#                     webbrowser.open(url)

#                 elif "open chrome" in command:
#                     speak("Opening Chrome, sir")
#                     webbrowser.open("https://google.com")

#                 elif "linkedin" in command:
#                     speak("Opening LinkedIn, sir")
#                     webbrowser.open("https://linkedin.com")

#                 elif "open chat gpt" in command or "open chatgpt" in command:
#                     speak("Opening Chat GPT, sir")
#                     webbrowser.open("https://chat.openai.com")

#                 elif "open file explorer" in command or "open explorer" in command:
#                     speak("Opening File Explorer, sir")
#                     os.system("explorer")

#                 elif "open settings" in command or "open setting" in command:
#                     speak("Opening Settings, sir")
#                     os.system("start ms-settings:")

#                 elif "open spotify" in command:
#                     speak("Opening Spotify, sir")
#                     os.system("start spotify:")

#                 elif "play" in command and "spotify" in command:
#                     speak("Playing on Spotify, sir")
#                     song_name = command.replace("play", "").replace("on spotify", "").strip()
#                     url = f"https://open.spotify.com/search/{song_name}"
#                     webbrowser.open(url)

#                 elif "open word" in command or "open ms word" in command:
#                     speak("Opening Microsoft Word, sir")
#                     os.system("start winword")

#                 elif "open powerpoint" in command or "open power point" in command:
#                     speak("Opening PowerPoint, sir")
#                     os.system("start powerpnt")

#                 elif "open excel" in command:
#                     speak("Opening Microsoft Excel, sir")
#                     os.system("start excel")

#                 elif "date and time" in command:
#                     now = datetime.datetime.now()
#                     current_time = now.strftime("%I:%M %p")
#                     current_date = now.strftime("%d %B %Y")
#                     speak(f"Sir, today is {current_date} and the time is {current_time}")

#                 elif any(word in command for word in ["time", "clock"]):
#                     now = datetime.datetime.now()
#                     current_time = now.strftime("%I:%M %p")
#                     speak(f"Sir, the current time is {current_time}")
#                 elif ("start air drawing" in command or "ai drawing" in command):
#                     speak("Starting air drawing mode, sir")
#                     start_drawing()
#                     speak("Air drawing mode closed, sir")
                    

#                 elif any(word in command for word in ["date", "today"]):
#                     today = datetime.datetime.now()
#                     current_date = today.strftime("%d %B %Y")
#                     speak(f"Sir, today's date is {current_date}")

#                 elif any(word in command for word in ["exit", "exist", "stop", "quit", "bye", "goodbye"]):
#                     print("Exit command detected")
#                     speak("Goodbye sir")
#                     break

#             except sr.WaitTimeoutError:
#                 continue   # no speech detected

#             except sr.UnknownValueError:
#                 continue   # speech not understood (NO spam print)

#             except Exception as e:
#                 print("i can't recognize:", e)
import speech_recognition as sr
import webbrowser
import os
import datetime
import threading
import pythoncom
import win32com.client
import pywhatkit
import time
import psutil

# GUI import
try:
    import iron_gui as GUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("[JARVIS] iron_gui.py not found — terminal mode")

# Contacts
contacts = {
    "xyz": "+91XXXXXXXXXX",
    "abc": "+91XXXXXXXXXX",
    "def": "+91XXXXXXXXXX",
}

# GUI helpers
def gui_status(text):
    try:
        if GUI_AVAILABLE and GUI._window:
            GUI.set_status(GUI._window, text)
    except:
        pass

def gui_log(text):
    try:
        if GUI_AVAILABLE and GUI._window:
            GUI.add_log(GUI._window, text)
    except:
        pass

def gui_listening(active):
    try:
        if GUI_AVAILABLE and GUI._window:
            GUI.set_listening(GUI._window, active)
    except:
        pass


def jarvis_loop():
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 1

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    def speak(text):
        print(f"Jarvis : {text}")
        gui_status(text.upper()[:45])
        gui_log(text[:40])
        speaker.Speak(text)

    def listen():
        """Always listening — shows clean output"""
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("Listening...")
            gui_listening(True)
            gui_status("LISTENING...")
            try:
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=7)
            except sr.WaitTimeoutError:
                gui_listening(False)
                gui_status("LISTENING...")
                return ""
            gui_listening(False)

        try:
            print("Recognizing...")
            gui_status("RECOGNIZING...")
            cmd = recognizer.recognize_google(audio, language="en-IN")
            print(f"You said : {cmd}")
            gui_log(cmd[:35])
            return cmd.lower().strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Internet connection error sir.")
            return ""

    # Wait for GUI to load
    time.sleep(3)
    speak("Jarvis is online tell me sir.")

    # ══════════════════════════════════════
    #  MAIN LOOP — always listening
    # ══════════════════════════════════════
    while True:

        cmd = listen()

        if not cmd:
            continue

        # ── COMMANDS ──────────────────────

        if any(word in cmd for word in ["jarvis","jar wis", "service", "travis", "jervis"]):
            print("wake word dtected")
            speak("Yes sir")
            continue
        if "send message" in cmd:
            speak("Who should I message sir?")
            name = listen()
            if name and name in contacts:
                speak(f"What should I say to {name}?")
                msg = listen()
                if msg:
                    speak(f"Sending message to {name}.")
                    pywhatkit.sendwhatmsg_instantly(contacts[name], msg, wait_time=10)
                else:
                    speak("Couldn't hear the message sir.")
            else:
                speak("Contact not found sir.")

        elif "system" in cmd and any(w in cmd for w in ["status", "report", "info"]):
            cpu  = psutil.cpu_percent(interval=1)
            ram  = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:\\").percent
            bat  = psutil.sensors_battery()
            b    = f"{int(bat.percent)} percent" if bat else "unavailable"
            speak(f"CPU {cpu}%. RAM {ram}%. Disk {disk}%. Battery {b}.")

        elif "date and time" in cmd:
            n = datetime.datetime.now()
            speak(f"Sir today is {n.strftime('%d %B %Y')} and time is {n.strftime('%I:%M %p')}.")

        elif any(w in cmd for w in ["what time", "current time", "time"]):
            speak(f"Sir the time is {datetime.datetime.now().strftime('%I:%M %p')}.")

        elif any(w in cmd for w in ["what date", "todays date", "date", "today"]):
            speak(f"Sir today is {datetime.datetime.now().strftime('%d %B %Y')}.")

        elif "air drawing" in cmd or "start drawing" in cmd:
            speak("Starting air drawing sir.")
            gui_status("AIR DRAWING ACTIVE")
            try:
                from airdrawing import start_drawing
                start_drawing()
            except Exception as e:
                speak("Air drawing module not found sir.")
            gui_status("LISTENING...")

        elif "open google" in cmd:
            speak("Opening Google sir.")
            webbrowser.open("https://google.com")

        elif "open youtube" in cmd:
            speak("Opening YouTube sir.")
            webbrowser.open("https://youtube.com")

        elif "open" in cmd and "channel" in cmd:
            ch = cmd.replace("open", "").replace("channel", "").strip()
            speak(f"Searching {ch} on YouTube sir.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={ch}")

        elif "open chrome" in cmd:
            speak("Opening Chrome sir.")
            webbrowser.open("https://google.com")

        elif "linkedin" in cmd:
            speak("Opening LinkedIn sir.")
            webbrowser.open("https://linkedin.com")

        elif "open chatgpt" in cmd or "open chat gpt" in cmd:
            speak("Opening ChatGPT sir.")
            webbrowser.open("https://chat.openai.com")

        elif "open github" in cmd:
            speak("Opening GitHub sir.")
            webbrowser.open("https://github.com")

        elif "search" in cmd:
            q = cmd.replace("search", "").replace("on google", "").strip()
            speak(f"Searching {q} sir.")
            webbrowser.open(f"https://www.google.com/search?q={q}")

        elif "open file explorer" in cmd or "open explorer" in cmd:
            speak("Opening File Explorer sir.")
            os.system("explorer")

        elif "open settings" in cmd:
            speak("Opening Settings sir.")
            os.system("start ms-settings:")

        elif "open notepad" in cmd:
            speak("Opening Notepad sir.")
            os.system("notepad")

        elif "open calculator" in cmd:
            speak("Opening Calculator sir.")
            os.system("calc")

        elif "open task manager" in cmd:
            speak("Opening Task Manager sir.")
            os.system("taskmgr")

        elif "open cmd" in cmd or "command prompt" in cmd:
            speak("Opening Command Prompt sir.")
            os.system("start cmd")

        elif "open paint" in cmd:
            speak("Opening Paint sir.")
            os.system("mspaint")

        elif "open word" in cmd:
            speak("Opening Word sir.")
            os.system("start winword")

        elif "open powerpoint" in cmd or "open power point" in cmd:
            speak("Opening PowerPoint sir.")
            os.system("start powerpnt")

        elif "open excel" in cmd:
            speak("Opening Excel sir.")
            os.system("start excel")

        elif "open spotify" in cmd:
            speak("Opening Spotify sir.")
            os.system("start spotify:")

        elif "play" in cmd and "spotify" in cmd:
            song = cmd.replace("play", "").replace("on spotify", "").strip()
            speak(f"Playing {song} sir.")
            webbrowser.open(f"https://open.spotify.com/search/{song}")

        elif "screenshot" in cmd:
            try:
                import pyautogui
                f = f"ss_{datetime.datetime.now().strftime('%H%M%S')}.png"
                pyautogui.screenshot(f)
                speak("Screenshot saved sir.")
            except:
                speak("Please install pyautogui sir.")

        elif "shutdown" in cmd:
            speak("Shutting down in 10 seconds. Say cancel to abort.")
            c = listen()
            if "cancel" in c:
                os.system("shutdown /a")
                speak("Cancelled sir.")
            else:
                os.system("shutdown /s /t 10")

        elif "restart" in cmd:
            speak("Restarting sir.")
            os.system("shutdown /r /t 5")

        elif "sleep" in cmd:
            speak("Going to sleep sir.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif any(w in cmd for w in ["exit", "stop", "quit", "bye", "goodbye"]):
            speak("Goodbye sir.")
            gui_status("OFFLINE")
            time.sleep(1)
            os._exit(0)

        else:
            speak("Sorry sir I did not understand.")


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    t = threading.Thread(target=jarvis_loop, daemon=True)
    t.start()

    if GUI_AVAILABLE:
        GUI.iron_gui()
    else:
        print("[JARVIS] No GUI. Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[JARVIS] Offline.")
            #updtae