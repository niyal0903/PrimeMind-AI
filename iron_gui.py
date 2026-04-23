# import tkinter as tk
# import math
# import random

# class iron_gui:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("J.A.R.V.I.S. NEURAL INTERFACE")
        
#         # Window size set ki
#         self.win_width = 800
#         self.win_height = 800
#         self.root.geometry(f"{self.win_width}x{self.win_height}")
#         self.root.resizable(False, False)
#         self.root.configure(bg="#000000")

#         self.canvas = tk.Canvas(root, bg="black", highlightthickness=0, width=self.win_width, height=self.win_height)
#         self.canvas.pack(fill="both", expand=True)

#         # IMPORTANT: Ab center window ke hisaab se hoga, screen ke hisaab se nahi
#         self.cx, self.cy = self.win_width // 2, self.win_height // 2
        
#         self.angle = 0
#         # Particles ki radius thodi kam ki taaki 800x800 mein fit aayein
#         self.particles = [[random.uniform(0, 2*math.pi), random.randint(150, 280), random.uniform(0.01, 0.03)] for _ in range(60)]
        
#         self.root.bind("<Escape>", lambda e: self.root.destroy())
#         self.update_ui()

#     def draw_tech_border(self):
#         """Corner UI frames ko window size ke hisaab se set kiya"""
#         color = "#004455"
#         # Top Left
#         self.canvas.create_line(20, 50, 200, 50, fill=color)
#         self.canvas.create_line(20, 50, 20, 150, fill=color)
#         self.canvas.create_text(30, 40, text="SYSTEM_DIAGNOSTICS: v10.4", fill="#00FFFF", font=("Courier", 10), anchor="w")
        
#         # Bottom Right (Window width/height ka use kiya)
#         self.canvas.create_text(self.win_width-20, self.win_height-40, text="ENCRYPTION: ACTIVE", fill="#00FFFF", font=("Courier", 10), anchor="e")
#         self.canvas.create_line(self.win_width-200, self.win_height-30, self.win_width-20, self.win_height-30, fill=color)

#     def update_ui(self):
#         self.canvas.delete("all")
#         self.angle += 0.05
        
#         # Background Grid (Window ke andar limited)
#         for i in range(0, self.win_width, 100):
#             self.canvas.create_line(i, 0, i, self.win_height, fill="#001111")
#         for i in range(0, self.win_height, 100):
#             self.canvas.create_line(0, i, self.win_width, i, fill="#001111")

#         self.draw_tech_border()

#         # Main Volumetric Rings
#         layers = [
#             {"r": 120, "color": "#00FFFF", "dash": (5, 15), "speed": 1.5, "width": 1},
#             {"r": 150, "color": "#0088AA", "dash": (20, 10), "speed": -0.8, "width": 2},
#             {"r": 180, "color": "#003344", "dash": None, "speed": 0.5, "width": 1},
#             {"r": 210, "color": "#00FFFF", "dash": (2, 40), "speed": 2.0, "width": 3}
#         ]

#         for layer in layers:
#             rot = self.angle * layer["speed"]
#             for start_a in [0, 120, 240]:
#                 self.canvas.create_arc(
#                     self.cx - layer["r"], self.cy - layer["r"],
#                     self.cx + layer["r"], self.cy + layer["r"],
#                     start=start_a + math.degrees(rot), extent=80,
#                     outline=layer["color"], style="arc", width=layer["width"], dash=layer["dash"]
#                 )

#         # Central Neural Sphere
#         points = []
#         for i in range(0, 361, 5):
#             theta = math.radians(i)
#             wave = math.sin(theta * 6 + self.angle * 2) * 8
#             wave += math.cos(theta * 3 - self.angle) * 4
#             r = 100 + wave # Radius thoda kam kiya window ke liye
#             x = self.cx + r * math.cos(theta)
#             y = self.cy + r * math.sin(theta)
#             points.append((x, y))
        
#         self.canvas.create_polygon(points, outline="#00D4FF", fill="", smooth=True, width=2)
        
#         # Internal core
#         core_r = 15 + abs(math.sin(self.angle) * 5)
#         self.canvas.create_oval(self.cx-core_r, self.cy-core_r, self.cx+core_r, self.cy+core_r, outline="#FFFFFF", width=2)

#         # Floating Orbital Data
#         for p in self.particles:
#             p[0] += p[2]
#             x = self.cx + p[1] * math.cos(p[0])
#             y = self.cy + p[1] * math.sin(p[0])
            
#             if random.random() > 0.95:
#                 self.canvas.create_line(self.cx, self.cy, x, y, fill="#003344", width=1)
            
#             self.canvas.create_rectangle(x-2, y-2, x+2, y+2, fill="#00FFFF", outline="")

#         # Animated Status Bars
#         for i in range(10):
#             h = abs(math.sin(self.angle + i)) * 40
#             self.canvas.create_rectangle(50 + i*15, 200, 60 + i*15, 200-h, fill="#0088AA", outline="")

#         self.root.after(20, self.update_ui)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = iron_gui(root)
#     root.mainloop()


import webview
import psutil
import threading
import time

# Global window reference
_window = None

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --cyan: #00f2ff;
    --red: #ff2a2a;
    --gold: #ffd700;
    --blue: #0066ff;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: radial-gradient(ellipse at center, #001830 0%, #000510 60%, #000 100%);
    color: var(--cyan);
    font-family: 'Rajdhani', sans-serif;
    width:100vw; height:100vh;
    overflow:hidden;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
  }
  body::before {
    content:'';
    position:fixed; inset:0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,242,255,0.015) 2px, rgba(0,242,255,0.015) 4px);
    pointer-events:none; z-index:999;
  }
  .corner { position:fixed; width:40px; height:40px; }
  .corner::before,.corner::after { content:''; position:absolute; background:var(--cyan); }
  .corner::before { width:100%; height:2px; top:0; }
  .corner::after  { width:2px; height:100%; top:0; }
  .corner.tl { top:16px; left:16px; }
  .corner.tr { top:16px; right:16px; transform:scaleX(-1); }
  .corner.bl { bottom:16px; left:16px; transform:scaleY(-1); }
  .corner.br { bottom:16px; right:16px; transform:scale(-1); }

  .topbar {
    position:fixed; top:0; left:0; right:0; height:36px;
    background:linear-gradient(90deg,transparent,rgba(0,242,255,0.08),transparent);
    border-bottom:1px solid rgba(0,242,255,0.2);
    display:flex; align-items:center; justify-content:space-between;
    padding:0 60px;
    font-family:'Orbitron',monospace; font-size:0.55rem; letter-spacing:3px;
    color:rgba(0,242,255,0.5);
  }
  .topbar-center { color:var(--cyan); font-size:0.6rem; letter-spacing:5px; }

  .bottombar {
    position:fixed; bottom:0; left:0; right:0; height:32px;
    border-top:1px solid rgba(0,242,255,0.15);
    display:flex; align-items:center; justify-content:center; gap:40px;
    font-family:'Orbitron',monospace; font-size:0.5rem; letter-spacing:3px;
    color:rgba(0,242,255,0.35);
  }

  .stage {
    position:relative; width:520px; height:520px;
    display:flex; align-items:center; justify-content:center;
    animation: stageIn 1.2s ease forwards;
  }
  @keyframes stageIn { from{opacity:0;transform:scale(0.85)} to{opacity:1;transform:scale(1)} }

  .ring { position:absolute; border-radius:50%; animation:spin linear infinite; }
  .r1 { width:500px;height:500px; border:1px dashed rgba(0,242,255,0.12); animation-duration:60s; }
  .r2 { width:460px;height:460px; border-top:2px solid rgba(0,242,255,0.7); border-bottom:2px solid rgba(0,242,255,0.7); border-left:2px solid transparent; border-right:2px solid transparent; animation-duration:8s; filter:drop-shadow(0 0 6px var(--cyan)); }
  .r3 { width:400px;height:400px; border:1px solid rgba(0,242,255,0.1); border-top:1px solid rgba(0,242,255,0.4); animation-duration:12s; animation-direction:reverse; }
  .r4 { width:350px;height:350px; border-left:2px solid rgba(255,42,42,0.7); border-right:2px solid rgba(255,42,42,0.7); border-top:2px solid transparent; border-bottom:2px solid transparent; animation-duration:5s; filter:drop-shadow(0 0 8px var(--red)); }
  .r5 { width:300px;height:300px; border:1px dashed rgba(0,242,255,0.2); animation-duration:20s; }
  .r6 { width:250px;height:250px; border-top:2px solid rgba(255,215,0,0.8); border-right:2px solid rgba(255,215,0,0.4); border-bottom:2px solid transparent; border-left:2px solid transparent; animation-duration:3s; animation-direction:reverse; filter:drop-shadow(0 0 6px var(--gold)); }
  .r7 { width:200px;height:200px; border:1px solid rgba(0,102,255,0.3); border-right:1px solid rgba(0,102,255,0.8); animation-duration:2s; filter:drop-shadow(0 0 4px var(--blue)); }
  @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

  .side-panel { position:absolute; top:50%; transform:translateY(-50%); width:130px; display:flex; flex-direction:column; gap:8px; }
  .side-panel.left  { right:calc(100% + 20px); align-items:flex-end; }
  .side-panel.right { left:calc(100% + 20px);  align-items:flex-start; }

  .stat-block { background:rgba(0,30,60,0.6); border:1px solid rgba(0,242,255,0.2); padding:8px 12px; position:relative; overflow:hidden; }
  .stat-block::before { content:''; position:absolute; left:0; top:0; bottom:0; width:2px; background:var(--cyan); box-shadow:0 0 6px var(--cyan); }
  .stat-block.r::before { background:var(--red);  box-shadow:0 0 6px var(--red); }
  .stat-block.g::before { background:var(--gold); box-shadow:0 0 6px var(--gold); }
  .stat-block.b::before { background:var(--blue); box-shadow:0 0 6px var(--blue); }

  .stat-label { font-family:'Orbitron',monospace; font-size:0.42rem; letter-spacing:3px; color:rgba(0,242,255,0.45); margin-bottom:4px; }
  .stat-val   { font-family:'Orbitron',monospace; font-size:1.05rem; font-weight:700; color:var(--cyan); text-shadow:0 0 8px var(--cyan); }
  .stat-val.r { color:var(--red);  text-shadow:0 0 8px var(--red); }
  .stat-val.g { color:var(--gold); text-shadow:0 0 8px var(--gold); }
  .stat-val.b { color:var(--blue); text-shadow:0 0 8px var(--blue); }

  .bar { width:100%; height:3px; background:rgba(0,242,255,0.1); margin-top:5px; }
  .bar-fill { height:100%; background:var(--cyan); box-shadow:0 0 4px var(--cyan); transition:width 0.8s ease; }
  .bar-fill.r { background:var(--red);  box-shadow:0 0 4px var(--red); }
  .bar-fill.g { background:var(--gold); box-shadow:0 0 4px var(--gold); }
  .bar-fill.b { background:var(--blue); box-shadow:0 0 4px var(--blue); }

  .core { position:relative; width:160px; height:160px; display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:10; }
  .core-glow { position:absolute; inset:0; border-radius:50%; background:radial-gradient(circle,rgba(0,102,255,0.3) 0%,rgba(0,242,255,0.1) 40%,transparent 70%); animation:breath 3s ease-in-out infinite; }
  @keyframes breath { 0%,100%{opacity:0.6;transform:scale(1)} 50%{opacity:1;transform:scale(1.1)} }

  .title { font-family:'Orbitron',monospace; font-size:1.4rem; font-weight:900; letter-spacing:8px; color:var(--cyan); text-shadow:0 0 20px var(--cyan); position:relative; z-index:1; }
  .subtitle { font-size:0.5rem; letter-spacing:3px; color:rgba(0,242,255,0.45); margin-top:4px; z-index:1; }

  #status-line { font-family:'Orbitron',monospace; font-size:0.55rem; letter-spacing:2px; color:var(--gold); text-shadow:0 0 8px var(--gold); margin-top:8px; z-index:1; text-align:center; min-height:16px; }

  #listen-pulse { display:none; position:fixed; top:50px; right:60px; align-items:center; gap:8px; font-family:'Orbitron',monospace; font-size:0.5rem; letter-spacing:3px; color:var(--red); }
  .pdot { width:8px; height:8px; border-radius:50%; background:var(--red); box-shadow:0 0 8px var(--red); animation:blink 0.8s ease-in-out infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

  .cmd-log { position:fixed; bottom:40px; left:60px; width:220px; }
  .log-title { font-family:'Orbitron',monospace; font-size:0.42rem; letter-spacing:3px; color:rgba(0,242,255,0.35); margin-bottom:6px; border-bottom:1px solid rgba(0,242,255,0.12); padding-bottom:4px; }
  .log-entry { font-size:0.68rem; color:rgba(0,242,255,0.4); padding:2px 0; }
  .log-entry.active { color:var(--cyan); }

  .time-display { position:fixed; bottom:40px; right:60px; text-align:right; }
  #clock { font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700; color:var(--cyan); text-shadow:0 0 12px var(--cyan); letter-spacing:3px; }
  #datestr { font-size:0.6rem; letter-spacing:3px; color:rgba(0,242,255,0.4); margin-top:2px; }
</style>
</head>
<body>

<div class="corner tl"></div>
<div class="corner tr"></div>
<div class="corner bl"></div>
<div class="corner br"></div>

<div class="topbar">
  <span>STARK INDUSTRIES</span>
  <span class="topbar-center">◈ JARVIS INTERFACE v1.0 ◈</span>
  <span id="sys-status">SYSTEM NOMINAL</span>
</div>
<div class="bottombar">
  <span>ENCRYPTION: AES-256</span>
  <span id="uptime">UPTIME: 00:00:00</span>
  <span>NETWORK: SECURE</span>
</div>

<div id="listen-pulse"><div class="pdot"></div><span>LISTENING</span></div>

<div class="time-display">
  <div id="clock">--:--:--</div>
  <div id="datestr">--</div>
</div>

<div class="stage">
  <div class="ring r1"></div>
  <div class="ring r2"></div>
  <div class="ring r3"></div>
  <div class="ring r4"></div>
  <div class="ring r5"></div>
  <div class="ring r6"></div>
  <div class="ring r7"></div>

  <div class="side-panel left">
    <div class="stat-block">
      <div class="stat-label">// CPU</div>
      <div class="stat-val" id="cpu-v">--%</div>
      <div class="bar"><div class="bar-fill" id="cpu-b" style="width:0%"></div></div>
    </div>
    <div class="stat-block r">
      <div class="stat-label">// RAM</div>
      <div class="stat-val r" id="ram-v">--%</div>
      <div class="bar"><div class="bar-fill r" id="ram-b" style="width:0%"></div></div>
    </div>
  </div>

  <div class="side-panel right">
    <div class="stat-block g">
      <div class="stat-label">// DISK</div>
      <div class="stat-val g" id="disk-v">--%</div>
      <div class="bar"><div class="bar-fill g" id="disk-b" style="width:0%"></div></div>
    </div>
    <div class="stat-block b">
      <div class="stat-label">// BATTERY</div>
      <div class="stat-val b" id="bat-v">--%</div>
      <div class="bar"><div class="bar-fill b" id="bat-b" style="width:0%"></div></div>
    </div>
  </div>

  <div class="core">
    <div class="core-glow"></div>
    <div class="title">JARVIS</div>
    <div class="subtitle">JUST A RATHER VERY INTELLIGENT SYSTEM</div>
    <div id="status-line">INITIALIZING...</div>
  </div>
</div>

<div class="cmd-log">
  <div class="log-title">// COMMAND LOG</div>
  <div id="log-list"></div>
</div>

<script>
  var logEntries = [];
  var startTime = Date.now();

  function updateStats(cpu, ram, disk, bat) {
    document.getElementById('cpu-v').textContent  = cpu  + '%';
    document.getElementById('ram-v').textContent  = ram  + '%';
    document.getElementById('disk-v').textContent = disk + '%';
    document.getElementById('bat-v').textContent  = bat  + '%';
    document.getElementById('cpu-b').style.width  = cpu  + '%';
    document.getElementById('ram-b').style.width  = ram  + '%';
    document.getElementById('disk-b').style.width = disk + '%';
    document.getElementById('bat-b').style.width  = (isNaN(bat) ? 0 : bat) + '%';
  }

  function setStatus(text) {
    document.getElementById('status-line').textContent = text;
  }

  function setListening(active) {
    document.getElementById('listen-pulse').style.display = active ? 'flex' : 'none';
  }

  function addLog(entry) {
    logEntries.push(entry);
    if (logEntries.length > 5) logEntries.shift();
    var html = '';
    for (var i = 0; i < logEntries.length; i++) {
      var cls = (i === logEntries.length - 1) ? 'active' : '';
      html += '<div class="log-entry ' + cls + '">> ' + logEntries[i] + '</div>';
    }
    document.getElementById('log-list').innerHTML = html;
  }

  function tick() {
    var now = new Date();
    document.getElementById('clock').textContent = now.toTimeString().slice(0,8);
    document.getElementById('datestr').textContent = now.toDateString().toUpperCase();
    var e = Math.floor((Date.now()-startTime)/1000);
    var h=String(Math.floor(e/3600)).padStart(2,'0');
    var m=String(Math.floor((e%3600)/60)).padStart(2,'0');
    var s=String(e%60).padStart(2,'0');
    document.getElementById('uptime').textContent = 'UPTIME: '+h+':'+m+':'+s;
  }
  setInterval(tick, 1000); tick();

  var bootMsgs = ['LOADING MODULES...','VOICE ENGINE ONLINE','SCANNING HARDWARE...','ALL SYSTEMS GO','SAY: JARVIS'];
  var bi = 0;
  function boot() {
    if (bi < bootMsgs.length) {
      setStatus(bootMsgs[bi]); addLog(bootMsgs[bi]); bi++;
      setTimeout(boot, 700);
    }
  }
  setTimeout(boot, 500);
</script>
</body>
</html>
"""

def _stats_loop(win):
    while True:
        try:
            cpu  = psutil.cpu_percent(interval=None)
            ram  = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:\\").percent
            bat  = psutil.sensors_battery()
            b    = int(bat.percent) if bat else 0
            win.evaluate_js(f"updateStats({cpu},{ram},{disk},{b})")
        except:
            pass
        time.sleep(1)


def set_status(win, text):
    try:
        safe = text.replace("'","").replace('"','')[:50]
        win.evaluate_js(f"setStatus('{safe}')")
    except:
        pass


def set_listening(win, active):
    try:
        win.evaluate_js(f"setListening({'true' if active else 'false'})")
    except:
        pass


def add_log(win, text):
    try:
        safe = text.replace("'","").replace('"','')[:40]
        win.evaluate_js(f"addLog('{safe}')")
    except:
        pass


def iron_gui():
    """Call this ONCE from main thread — it blocks until window is closed."""
    global _window
    _window = webview.create_window(
        "JARVIS — Stark Industries",
        html=HTML,
        width=900,
        height=700,
        resizable=True,
    )
    threading.Thread(target=_stats_loop, args=(_window,), daemon=True).start()
    webview.start(gui="edgechromium")   # blocks here — returns only when window closed