🤖 J.A.R.V.I.S — Mark I
AI-Powered Voice-Controlled Desktop Assistant with Air Drawing & Live HUD

J.A.R.V.I.S ek next-generation personal AI assistant hai jo sirf commands nahi leta — balki real-time mein aapke Windows PC ka intelligent companion ban jaata hai. Tony Stark ke JARVIS se inspired, yeh system voice, hand gestures, aur live system monitoring ko ek saath combine karta hai.


🆕 Mark I — What's New?
FeatureDescription🎙️ Voice ControlGoogle Speech Recognition — Indian English optimized🖐️ Air DrawingMediaPipe Hand Landmark AI — hawa mein finger se draw karo💻 Iron Man HUDAnimated neon rings + real-time CPU / RAM / Disk / Battery📱 WhatsApp AutomationVoice se contact ko instantly WhatsApp message bhejo🌐 Smart App Launcher15+ apps aur websites sirf awaaz se open karo🗣️ Text-to-SpeechWindows SAPI5 — Jarvis ki awaaz mein jawab deta hai

🚀 Core Features
🎤 Voice Controlled Interface
Jarvis se seedha baat karo — commands voice se execute hoti hain:
CommandAction"Jarvis"Wake word — system acknowledge karta hai"Open Google"Google browser mein open hota hai"Open YouTube"YouTube open hota hai"Open [name] channel"YouTube pe channel search hota hai"Open ChatGPT"ChatGPT directly open hota hai"Open LinkedIn"LinkedIn open hota hai"Open Spotify"Spotify app launch hota hai"Play [song] on Spotify"Spotify pe song search hota hai"Open File Explorer"Windows Explorer open hota hai"Open Settings"Windows Settings open hoti hai"Open Word"Microsoft Word launch hota hai"Open PowerPoint"PowerPoint launch hota hai"Open Excel"Excel launch hota hai"Date and time"Aaj ki date aur time bolti hai"Time"Current time bolti hai"Date"Aaj ki date bolti hai"Send message"WhatsApp message bhejne ka flow shuru"Start air drawing"Air Drawing Mode activate hota hai"Exit" / "Bye"Jarvis band ho jaata hai

🖐️ Air Drawing Canvas
MediaPipe ke real-time hand detection se hawa mein drawing karo — koi touch nahi, sirf gestures:
GestureAction☝️ Sirf Index finger uparDraw mode — line kheencho✌️ Index + Middle uparEraser mode — brush se mita do🤟 Index + Middle + Ring uparClear all — poora canvas saafQ key pressDrawing mode se bahar aao

💻 Iron Man HUD Dashboard
         ╔══════════════════════════╗
         ║      J.A.R.V.I.S        ║
         ╠══════════════════════════╣
         ║  CPU: 34%  │  RAM: 61%  ║
         ║  DISK: 72% │  BAT: 88%  ║
         ╚══════════════════════════╝

Outer Ring — Cyan neon glow, 4 second rotation
Middle Ring — Red neon glow, 3 second reverse rotation
Inner Ring — Yellow glow, 2 second rotation
Live Stats — CPU, RAM, Disk, Battery — har 1 second update hota hai
Edge Chromium Renderer — Smooth pywebview HTML/CSS/JS GUI


📱 WhatsApp Automation Flow
Voice: "Send message"
         ↓
Jarvis: "Whom should I send message to?"
         ↓
Voice: Contact ka naam bolo
         ↓
Jarvis: "What should I say to [name]?"
         ↓
Voice: Message bolo
         ↓
WhatsApp Web pe instantly message chala jaata hai ✓

🛠️ Tech Stack
CategoryTechnologiesLanguagePython 3.10+Voice InputSpeechRecognition, PyAudio, Google Speech APIVoice Outputwin32com.client — Windows SAPI5Hand AIMediaPipe Hand Landmarker (.task model)Computer VisionOpenCV (cv2)Drawing CanvasNumPy array-based overlayGUI / HUDpywebview, Edge Chromium, HTML / CSS / JSSystem Statspsutil — CPU, RAM, Disk, BatteryWhatsApppywhatkitConcurrencythreading, pythoncom

📂 Project Structure
jarvis-ai-assistant/
│
├── jarvis.py                ← Main Hub — Voice loop & command routing
├── airdrawing.py            ← Air Drawing module (OpenCV + MediaPipe)
├── gui.py                   ← Iron Man HUD Dashboard (pywebview)
│
├── hand_landmarker.task     ← MediaPipe hand detection model (download separately)
├── requirements.txt         ← All dependencies
└── README.md

⚙️ Installation & Setup
1. Clone the Repository
bashgit clone https://github.com/YOUR_USERNAME/jarvis-ai-assistant.git
cd jarvis-ai-assistant
2. Virtual Environment (Recommended)
bashpython -m venv venv
venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt

⚠️ PyAudio install error aaye toh yeh karo:
bashpip install pipwin
pipwin install pyaudio

4. Download MediaPipe Hand Model
MediaPipe Hand Landmarker se hand_landmarker.task file download karo aur root folder mein rakho.
5. Configure Your Contacts
jarvis.py mein contacts dictionary update karo apne numbers se:
pythoncontacts = {
    "name": "+91XXXXXXXXXX",   # Country code ke saath
}
6. Run Jarvis!
bashpython jarvis.py

⚠️ System Requirements
RequirementDetailOSWindows 10 / 11 onlyPython3.10 or higherBrowserMicrosoft Edge (pywebview renderer ke liye)HardwareMicrophone + Webcam zaroori haiWhatsAppBrowser mein WhatsApp Web login hona chahiye

🚧 Known Issues / Limitations

Windows Only — win32com aur SAPI5 sirf Windows pe kaam karta hai
WhatsApp Web Required — pywhatkit browser mein WhatsApp Web open karta hai
hand_landmarker.task — Manually download karna padega, bundle nahi hai
Noisy Environment — adjust_for_ambient_noise duration badhao noisy room mein


🛣️ Roadmap — Aane Wale Features

 🧠 ChatGPT / Gemini API — real AI conversation
 📧 Gmail voice automation — awaaz se email bhejo
 🔔 Reminder aur alarm system
 🌤️ Live weather aur news updates
 🎨 Air drawing mein color picker
 🔐 Face recognition authentication
 📊 Screen activity logger


⚠️ Disclaimer
Yeh tool sirf personal use aur learning ke liye banaya gaya hai. WhatsApp automation ke liye apna khud ka account use karein. Unauthorized use prohibited hai.

🤝 Contributing

Fork the repository
Naya branch banao: git checkout -b feature/your-feature
Commit karo: git commit -m "Add: your feature"
Push karo: git push origin feature/your-feature
Pull Request open karo


👨‍💻 Author
Your Name
AI & Automation Developer
GitHub: @YOUR_USERNAME


"Sometimes you gotta run before you can walk." — Tony Stark