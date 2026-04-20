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
import tkinter as tk
from airdrawing import start_drawing
import threading
import pythoncom
import win32com.client
import pywhatkit

# ---------------- Contacts ----------------
contacts = {
    "xyz": "**********",
    "abc": "**********",
    "def": "**********",
    
}

# ---------------- Voice Loop ----------------
def jarvis_loop():
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    def speak(text):
        print("Jarvis:", text)
        speaker.Speak(text)

    recognizer = sr.Recognizer()
    speak("Jarvis is online tell me sir...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print("You said:", command)

            # ---------------- Wake word ----------------
            if any(word in command for word in ["jarvis","jar wis", "service", "travis", "jervis"]):
                print("Wake word detected")
                speak("Yes sir")
                continue

            if "send message" in command:
                speak("Whom should I send message to?")
                with sr.Microphone() as source2:
                    audio2 = recognizer.listen(source2, timeout=5, phrase_time_limit=5)

                contact_name = recognizer.recognize_google(audio2, language="en-IN").lower().strip()

                if contact_name in contacts:
                    contact_number = contacts[contact_name]
                    speak(f"What should I say to {contact_name}?")

                    with sr.Microphone() as source3:
                        audio3 = recognizer.listen(source3, timeout=5, phrase_time_limit=10)

                    message = recognizer.recognize_google(audio3, language="en-IN")
                    speak(f"Sending message to {contact_name}: {message}")
                    pywhatkit.sendwhatmsg_instantly(contact_number, message)

                else:
                    speak("Contact not found in your list.")

                for name in contacts:
                    if name in command:
                        found = True
                        contact_number = contacts[name]

                        speak(f"What should I say to {name}?")

                        with sr.Microphone() as source2:
                            audio2 = recognizer.listen(source2, timeout=5, phrase_time_limit=10)

                        message = recognizer.recognize_google(audio2, language="en-IN")

                        speak(f"Sending message to {name}: {message}")

                        pywhatkit.sendwhatmsg_instantly(contact_number, message)
                        break

                    if not found:
                        speak("Contact not found in your list.")

                continue

            # ---------------- Commands ----------------
            elif "open google" in command:
                speak("Opening Google, sir")
                webbrowser.open("https://google.com")

            elif "open youtube" in command:
                speak("Opening YouTube, sir")
                webbrowser.open("https://youtube.com")

            elif "open" in command and "channel" in command:
                speak("Opening the channel, sir")
                channel_name = command.replace("open", "").replace("channel", "").strip()
                url = f"https://www.youtube.com/results?search_query={channel_name}"
                webbrowser.open(url)

            elif "open chrome" in command:
                speak("Opening Chrome, sir")
                webbrowser.open("https://google.com")

            elif "linkedin" in command:
                speak("Opening LinkedIn, sir")
                webbrowser.open("https://linkedin.com")

            elif "open chat gpt" in command or "open chatgpt" in command:
                speak("Opening Chat GPT, sir")
                webbrowser.open("https://chat.openai.com")

            elif "open file explorer" in command or "open explorer" in command:
                speak("Opening File Explorer, sir")
                os.system("explorer")

            elif "open settings" in command or "open setting" in command:
                speak("Opening Settings, sir")
                os.system("start ms-settings:")

            elif "open spotify" in command:
                speak("Opening Spotify, sir")
                os.system("start spotify:")

            elif "play" in command and "spotify" in command:
                speak("Playing on Spotify, sir")
                song_name = command.replace("play", "").replace("on spotify", "").strip()
                url = f"https://open.spotify.com/search/{song_name}"
                webbrowser.open(url)

            elif "open word" in command or "open ms word" in command:
                speak("Opening Microsoft Word, sir")
                os.system("start winword")

            elif "open powerpoint" in command or "open power point" in command:
                speak("Opening PowerPoint, sir")
                os.system("start powerpnt")

            elif "open excel" in command:
                speak("Opening Microsoft Excel, sir")
                os.system("start excel")

            elif "date and time" in command:
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")
                current_date = now.strftime("%d %B %Y")
                speak(f"Sir, today is {current_date} and the time is {current_time}")

            elif any(word in command for word in ["time", "clock"]):
                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")
                speak(f"Sir, the current time is {current_time}")

            elif "start air drawing" in command or "ai drawing" in command:
                speak("Starting air drawing mode, sir")
                start_drawing()
                speak("Air drawing mode closed, sir")

            elif any(word in command for word in ["date", "today"]):
                today = datetime.datetime.now()
                current_date = today.strftime("%d %B %Y")
                speak(f"Sir, today's date is {current_date}")

            elif any(word in command for word in ["exit", "exist", "stop", "quit", "bye", "goodbye"]):
                print("Exit command detected")
                speak("Goodbye sir")
                os._exit(0)

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print("i can't recognizer:", e)

# ---------------- Start voice thread ----------------
voice_thread = threading.Thread(target=jarvis_loop)
voice_thread.daemon = True
voice_thread.start()

# Keep program running
while True:
    pass