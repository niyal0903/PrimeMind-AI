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

_window = None

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }

body {
  background: #000;
  font-family: 'Orbitron', monospace;
  width: 100vw; height: 100vh;
  overflow: hidden;
  color: #00f2ff;
}

/* ── SCANLINES ── */
body::after {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(0,0,0,0.15) 3px, rgba(0,0,0,0.15) 4px
  );
  pointer-events: none; z-index: 9999;
}

/* ── BACKGROUND GRID ── */
.bg-grid {
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,242,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,242,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
}
@keyframes gridMove {
  from { background-position: 0 0; }
  to   { background-position: 40px 40px; }
}

/* ── VIGNETTE ── */
.vignette {
  position: fixed; inset: 0;
  background: radial-gradient(ellipse at center,
    transparent 40%, rgba(0,0,0,0.85) 100%);
  pointer-events: none; z-index: 1;
}

/* ── MAIN LAYOUT ── */
.layout {
  position: relative;
  width: 100vw; height: 100vh;
  display: flex; align-items: center; justify-content: center;
  z-index: 10;
}

/* ════════════════════════════════
   CENTER — ARC REACTOR
════════════════════════════════ */
.arc-wrap {
  position: relative;
  width: 440px; height: 440px;
  display: flex; align-items: center; justify-content: center;
}

/* Hex grid background behind arc */
.arc-wrap::before {
  content: '';
  position: absolute;
  width: 300px; height: 300px;
  background:
    radial-gradient(circle, rgba(0,102,255,0.12) 0%, transparent 70%);
  border-radius: 50%;
  animation: corePulse 3s ease-in-out infinite;
}
@keyframes corePulse {
  0%,100% { transform: scale(1); opacity: 0.6; }
  50%      { transform: scale(1.15); opacity: 1; }
}

/* Rings */
.ring {
  position: absolute;
  border-radius: 50%;
  animation: spin linear infinite;
}

.ring-1 {
  width: 420px; height: 420px;
  border: 1px solid rgba(0,242,255,0.08);
  animation-duration: 80s;
}
.ring-2 {
  width: 390px; height: 390px;
  border-top: 1px solid rgba(0,242,255,0.25);
  border-bottom: 1px solid rgba(0,242,255,0.25);
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  animation-duration: 30s;
  animation-direction: reverse;
}
.ring-3 {
  width: 360px; height: 360px;
  border: 1px dashed rgba(0,242,255,0.1);
  animation-duration: 25s;
}
.ring-4 {
  width: 320px; height: 320px;
  border-top: 2px solid #00f2ff;
  border-right: 2px solid transparent;
  border-bottom: 2px solid transparent;
  border-left: 2px solid #00f2ff;
  animation-duration: 10s;
  filter: drop-shadow(0 0 6px #00f2ff);
}
.ring-5 {
  width: 280px; height: 280px;
  border: 1px solid rgba(255,42,42,0.15);
  border-right: 1px solid rgba(255,42,42,0.5);
  animation-duration: 7s;
  animation-direction: reverse;
  filter: drop-shadow(0 0 4px rgba(255,42,42,0.3));
}
.ring-6 {
  width: 240px; height: 240px;
  border-top: 2px solid rgba(255,215,0,0.7);
  border-bottom: 2px solid rgba(255,215,0,0.3);
  border-left: 2px solid transparent;
  border-right: 2px solid transparent;
  animation-duration: 5s;
  filter: drop-shadow(0 0 5px rgba(255,215,0,0.4));
}
.ring-7 {
  width: 200px; height: 200px;
  border: 1px solid rgba(0,242,255,0.2);
  border-bottom: 2px solid #00f2ff;
  animation-duration: 3s;
  animation-direction: reverse;
}
.ring-8 {
  width: 170px; height: 170px;
  border-top: 1px solid rgba(0,102,255,0.6);
  border-bottom: 1px solid transparent;
  border-left: 1px solid rgba(0,102,255,0.6);
  border-right: 1px solid transparent;
  animation-duration: 2s;
  filter: drop-shadow(0 0 6px rgba(0,102,255,0.5));
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* Tick marks on ring-4 */
.ticks {
  position: absolute;
  width: 320px; height: 320px;
  border-radius: 50%;
  animation: spin 10s linear infinite;
}
.tick {
  position: absolute;
  width: 2px; background: rgba(0,242,255,0.6);
  left: 50%; top: 0;
  transform-origin: 50% 160px;
}

/* Dot nodes */
.dot-node {
  position: absolute;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #00f2ff;
  box-shadow: 0 0 8px #00f2ff;
}

/* ── LISTEN RING ── */
#listen-ring {
  position: absolute;
  width: 155px; height: 155px;
  border-radius: 50%;
  border: 2px solid #00ff88;
  box-shadow: 0 0 20px #00ff88, inset 0 0 20px rgba(0,255,136,0.1);
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 5;
}
#listen-ring.active {
  opacity: 1;
  animation: listenPulse 1s ease-in-out infinite;
}
@keyframes listenPulse {
  0%,100% { transform: scale(1);    opacity: 1; }
  50%      { transform: scale(1.12); opacity: 0.4; }
}

/* ── CORE CENTER ── */
.core {
  position: relative;
  width: 140px; height: 140px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  z-index: 20;
  text-align: center;
}

/* Arc reactor inner glow */
.core::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle,
    rgba(0,150,255,0.4) 0%,
    rgba(0,242,255,0.15) 40%,
    transparent 70%
  );
  animation: corePulse 3s ease-in-out infinite;
}

/* Hexagonal pattern on core */
.core::after {
  content: '';
  position: absolute; inset: 10px;
  border-radius: 50%;
  border: 1px solid rgba(0,242,255,0.2);
  background:
    repeating-conic-gradient(
      rgba(0,242,255,0.05) 0deg 60deg,
      transparent 60deg 120deg
    );
}

.core-title {
  font-size: 1.1rem;
  font-weight: 900;
  letter-spacing: 6px;
  color: #00f2ff;
  text-shadow: 0 0 20px #00f2ff, 0 0 40px rgba(0,242,255,0.3);
  position: relative; z-index: 2;
  animation: titleFlicker 5s ease-in-out infinite;
}
@keyframes titleFlicker {
  0%,94%,100% { opacity: 1; }
  95% { opacity: 0.5; }
  96% { opacity: 1; }
  97% { opacity: 0.7; }
}

#status-line {
  font-size: 0.38rem;
  letter-spacing: 2px;
  margin-top: 6px;
  color: #ffd700;
  text-shadow: 0 0 8px #ffd700;
  position: relative; z-index: 2;
  min-height: 14px;
  transition: color 0.3s, text-shadow 0.3s;
}
#status-line.listening   { color: #00ff88; text-shadow: 0 0 8px #00ff88; }
#status-line.recognizing { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; }
#status-line.speaking    { color: #ff8800; text-shadow: 0 0 8px #ff8800; }


/* ════════════════════════════════
   LEFT PANEL
════════════════════════════════ */
.left-panel {
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 200px;
  display: flex; flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 0 20px;
}

/* ════════════════════════════════
   RIGHT PANEL
════════════════════════════════ */
.right-panel {
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 200px;
  display: flex; flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 0 20px;
}

/* ── STAT CARD ── */
.stat-card {
  background: rgba(0,15,35,0.8);
  border: 1px solid rgba(0,242,255,0.15);
  border-left: 2px solid #00f2ff;
  padding: 10px 12px;
  position: relative;
  overflow: hidden;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
}
.stat-card.red   { border-left-color: #ff2a2a; }
.stat-card.gold  { border-left-color: #ffd700; }
.stat-card.blue  { border-left-color: #0066ff; }
.stat-card.green { border-left-color: #00ff88; }

/* Animated scan line inside card */
.stat-card::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 40%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,242,255,0.06), transparent);
  animation: cardScan 3s linear infinite;
}
@keyframes cardScan { to { left: 200%; } }

.card-label {
  font-size: 0.38rem;
  letter-spacing: 3px;
  color: rgba(0,242,255,0.4);
  margin-bottom: 4px;
}
.card-val {
  font-size: 1.3rem;
  font-weight: 700;
  color: #00f2ff;
  text-shadow: 0 0 10px #00f2ff;
  line-height: 1;
}
.card-val.red   { color: #ff4d4d; text-shadow: 0 0 10px #ff2a2a; }
.card-val.gold  { color: #ffd700; text-shadow: 0 0 10px #ffd700; }
.card-val.blue  { color: #4d88ff; text-shadow: 0 0 10px #0066ff; }
.card-val.green { color: #00ff88; text-shadow: 0 0 10px #00ff88; }

.bar-track {
  width: 100%; height: 2px;
  background: rgba(0,242,255,0.08);
  margin-top: 6px;
}
.bar-fill {
  height: 100%;
  background: #00f2ff;
  box-shadow: 0 0 4px #00f2ff;
  transition: width 1s ease;
}
.bar-fill.red   { background: #ff2a2a; box-shadow: 0 0 4px #ff2a2a; }
.bar-fill.gold  { background: #ffd700; box-shadow: 0 0 4px #ffd700; }
.bar-fill.blue  { background: #0066ff; box-shadow: 0 0 4px #0066ff; }
.bar-fill.green { background: #00ff88; box-shadow: 0 0 4px #00ff88; }

/* mini sparkline */
.sparkline {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 20px;
  margin-top: 5px;
}
.spark-bar {
  flex: 1;
  background: rgba(0,242,255,0.4);
  min-height: 2px;
  transition: height 0.4s ease;
  border-radius: 1px;
}
.spark-bar.red  { background: rgba(255,42,42,0.5); }
.spark-bar.gold { background: rgba(255,215,0,0.5); }
.spark-bar.blue { background: rgba(0,102,255,0.5); }


/* ════════════════════════════════
   TOP BAR
════════════════════════════════ */
.topbar {
  position: fixed; top: 0; left: 0; right: 0;
  height: 40px;
  background: linear-gradient(90deg,
    transparent,
    rgba(0,242,255,0.05) 20%,
    rgba(0,242,255,0.05) 80%,
    transparent
  );
  border-bottom: 1px solid rgba(0,242,255,0.12);
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 0.45rem;
  letter-spacing: 3px;
  color: rgba(0,242,255,0.4);
  z-index: 100;
}
.topbar-mid {
  color: #00f2ff;
  font-size: 0.5rem;
  letter-spacing: 5px;
  text-shadow: 0 0 10px rgba(0,242,255,0.4);
}

/* ── CORNER BRACKETS ── */
.corner { position: fixed; width: 20px; height: 20px; z-index: 100; }
.corner::before, .corner::after { content: ''; position: absolute; background: #00f2ff; }
.corner::before { width: 100%; height: 1px; top: 0; }
.corner::after  { width: 1px; height: 100%; top: 0; }
.corner.tl { top: 44px; left: 8px; }
.corner.tr { top: 44px; right: 8px; transform: scaleX(-1); }
.corner.bl { bottom: 36px; left: 8px; transform: scaleY(-1); }
.corner.br { bottom: 36px; right: 8px; transform: scale(-1); }


/* ════════════════════════════════
   BOTTOM BAR
════════════════════════════════ */
.bottombar {
  position: fixed; bottom: 0; left: 0; right: 0;
  height: 32px;
  border-top: 1px solid rgba(0,242,255,0.1);
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 0.4rem;
  letter-spacing: 3px;
  color: rgba(0,242,255,0.3);
  z-index: 100;
}

/* ════════════════════════════════
   COMMAND LOG (bottom left)
════════════════════════════════ */
.cmd-log {
  position: fixed;
  bottom: 40px; left: 210px;
  width: 180px;
  z-index: 50;
}
.log-hdr {
  font-size: 0.38rem; letter-spacing: 3px;
  color: rgba(0,242,255,0.3);
  border-bottom: 1px solid rgba(0,242,255,0.1);
  padding-bottom: 4px; margin-bottom: 5px;
}
.log-entry {
  font-size: 0.55rem;
  color: rgba(0,242,255,0.35);
  padding: 2px 0;
  white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis;
  border-left: 1px solid rgba(0,242,255,0.1);
  padding-left: 6px;
  margin-bottom: 2px;
}
.log-entry.active {
  color: #00f2ff;
  border-left-color: #00f2ff;
  text-shadow: 0 0 6px rgba(0,242,255,0.4);
}

/* ════════════════════════════════
   CLOCK (bottom right)
════════════════════════════════ */
.clock-wrap {
  position: fixed;
  bottom: 40px; right: 210px;
  text-align: right;
  z-index: 50;
}
#clock {
  font-size: 2rem; font-weight: 700;
  color: #00f2ff;
  text-shadow: 0 0 15px #00f2ff;
  letter-spacing: 4px;
}
#datestr {
  font-size: 0.45rem; letter-spacing: 3px;
  color: rgba(0,242,255,0.4);
  margin-top: 2px;
}
#daystr {
  font-size: 0.5rem; letter-spacing: 4px;
  color: rgba(255,215,0,0.5);
  margin-top: 1px;
}

/* ── LISTENING TOP RIGHT ── */
#listen-badge {
  position: fixed; top: 50px; right: 20px;
  display: none; align-items: center; gap: 6px;
  font-size: 0.42rem; letter-spacing: 3px;
  color: #00ff88; z-index: 100;
}
#listen-badge.show { display: flex; }
.badge-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #00ff88; box-shadow: 0 0 8px #00ff88;
  animation: dotBlink 0.7s ease-in-out infinite;
}
@keyframes dotBlink { 0%,100%{opacity:1} 50%{opacity:0.1} }

/* ── ALERT BORDER ── */
#alert-border {
  display: none; position: fixed; inset: 0;
  border: 2px solid #ff2a2a;
  box-shadow: inset 0 0 40px rgba(255,42,42,0.1);
  pointer-events: none; z-index: 998;
  animation: alertBlink 1s ease-in-out infinite;
}
@keyframes alertBlink { 0%,100%{opacity:1} 50%{opacity:0.3} }
</style>
</head>
<body>

<div class="bg-grid"></div>
<div class="vignette"></div>

<!-- Alert border -->
<div id="alert-border"></div>

<!-- Topbar -->
<div class="topbar">
  <span>STARK INDUSTRIES · MARK I</span>
  <span class="topbar-mid">◈ J.A.R.V.I.S ◈</span>
  <span id="sys-label">ALL SYSTEMS NOMINAL</span>
</div>

<!-- Corners -->
<div class="corner tl"></div>
<div class="corner tr"></div>
<div class="corner bl"></div>
<div class="corner br"></div>

<!-- Listen badge -->
<div id="listen-badge"><div class="badge-dot"></div><span>LISTENING</span></div>

<!-- Bottom bar -->
<div class="bottombar">
  <span>ENCRYPTION · AES-256-GCM</span>
  <span id="uptime-label">UPTIME · 00:00:00</span>
  <span>NETWORK · SECURE</span>
</div>

<!-- Clock -->
<div class="clock-wrap">
  <div id="clock">--:--:--</div>
  <div id="datestr">-- --- ----</div>
  <div id="daystr">--------</div>
</div>

<!-- Command log -->
<div class="cmd-log">
  <div class="log-hdr">// COMMAND LOG</div>
  <div id="log-list"></div>
</div>

<!-- MAIN LAYOUT -->
<div class="layout">

  <!-- LEFT PANEL -->
  <div class="left-panel">
    <div class="stat-card">
      <div class="card-label">// CPU USAGE</div>
      <div class="card-val" id="cpu-v">--%</div>
      <div class="bar-track"><div class="bar-fill" id="cpu-b" style="width:0%"></div></div>
      <div class="sparkline" id="cpu-spark">
        <div class="spark-bar" style="height:40%"></div>
        <div class="spark-bar" style="height:60%"></div>
        <div class="spark-bar" style="height:30%"></div>
        <div class="spark-bar" style="height:80%"></div>
        <div class="spark-bar" style="height:50%"></div>
        <div class="spark-bar" style="height:70%"></div>
        <div class="spark-bar" style="height:45%"></div>
        <div class="spark-bar" style="height:90%"></div>
      </div>
    </div>
    <div class="stat-card red">
      <div class="card-label">// RAM USAGE</div>
      <div class="card-val red" id="ram-v">--%</div>
      <div class="bar-track"><div class="bar-fill red" id="ram-b" style="width:0%"></div></div>
      <div class="sparkline" id="ram-spark">
        <div class="spark-bar red" style="height:50%"></div>
        <div class="spark-bar red" style="height:70%"></div>
        <div class="spark-bar red" style="height:65%"></div>
        <div class="spark-bar red" style="height:80%"></div>
        <div class="spark-bar red" style="height:55%"></div>
        <div class="spark-bar red" style="height:75%"></div>
        <div class="spark-bar red" style="height:60%"></div>
        <div class="spark-bar red" style="height:85%"></div>
      </div>
    </div>
    <div class="stat-card green">
      <div class="card-label">// PROCESSES</div>
      <div class="card-val green" id="proc-v">--</div>
      <div class="bar-track"><div class="bar-fill green" id="proc-b" style="width:50%"></div></div>
    </div>
  </div>

  <!-- ARC REACTOR -->
  <div class="arc-wrap">
    <div class="ring ring-1"></div>
    <div class="ring ring-2"></div>
    <div class="ring ring-3"></div>
    <div class="ring ring-4"></div>
    <div class="ring ring-5"></div>
    <div class="ring ring-6"></div>
    <div class="ring ring-7"></div>
    <div class="ring ring-8"></div>

    <!-- Tick marks -->
    <div class="ticks" id="ticks"></div>

    <!-- Listen ring -->
    <div id="listen-ring"></div>

    <!-- CORE -->
    <div class="core">
      <div class="core-title">JARVIS</div>
      <div id="status-line">INITIALIZING</div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="right-panel">
    <div class="stat-card gold">
      <div class="card-label">// DISK C:</div>
      <div class="card-val gold" id="disk-v">--%</div>
      <div class="bar-track"><div class="bar-fill gold" id="disk-b" style="width:0%"></div></div>
      <div class="sparkline" id="disk-spark">
        <div class="spark-bar gold" style="height:70%"></div>
        <div class="spark-bar gold" style="height:70%"></div>
        <div class="spark-bar gold" style="height:72%"></div>
        <div class="spark-bar gold" style="height:71%"></div>
        <div class="spark-bar gold" style="height:73%"></div>
        <div class="spark-bar gold" style="height:70%"></div>
        <div class="spark-bar gold" style="height:72%"></div>
        <div class="spark-bar gold" style="height:74%"></div>
      </div>
    </div>
    <div class="stat-card blue">
      <div class="card-label">// BATTERY</div>
      <div class="card-val blue" id="bat-v">--%</div>
      <div class="bar-track"><div class="bar-fill blue" id="bat-b" style="width:0%"></div></div>
    </div>
    <div class="stat-card">
      <div class="card-label">// NETWORK</div>
      <div class="card-val" id="net-v" style="font-size:0.7rem">SECURE</div>
      <div class="sparkline" id="net-spark">
        <div class="spark-bar" style="height:30%"></div>
        <div class="spark-bar" style="height:70%"></div>
        <div class="spark-bar" style="height:40%"></div>
        <div class="spark-bar" style="height:90%"></div>
        <div class="spark-bar" style="height:20%"></div>
        <div class="spark-bar" style="height:60%"></div>
        <div class="spark-bar" style="height:50%"></div>
        <div class="spark-bar" style="height:80%"></div>
      </div>
    </div>
  </div>

</div><!-- end layout -->

<script>
// ── TICK MARKS ──
var ticksEl = document.getElementById('ticks');
for (var i = 0; i < 48; i++) {
  var t = document.createElement('div');
  t.className = 'tick';
  t.style.transform = 'rotate(' + (i * 7.5) + 'deg)';
  t.style.height = (i % 4 === 0) ? '14px' : '7px';
  t.style.opacity = (i % 4 === 0) ? '0.8' : '0.3';
  ticksEl.appendChild(t);
}

// ── CLOCK ──
var startTime = Date.now();
function updateClock() {
  var now = new Date();
  document.getElementById('clock').textContent = now.toTimeString().slice(0,8);
  document.getElementById('datestr').textContent =
    now.getDate().toString().padStart(2,'0') + ' ' +
    ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][now.getMonth()] +
    ' ' + now.getFullYear();
  document.getElementById('daystr').textContent =
    ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'][now.getDay()];

  var elapsed = Math.floor((Date.now()-startTime)/1000);
  var h = String(Math.floor(elapsed/3600)).padStart(2,'0');
  var m = String(Math.floor((elapsed%3600)/60)).padStart(2,'0');
  var s = String(elapsed%60).padStart(2,'0');
  document.getElementById('uptime-label').textContent = 'UPTIME · ' + h + ':' + m + ':' + s;
}
setInterval(updateClock, 1000);
updateClock();

// ── SPARKLINE UPDATE ──
var cpuHist=[], ramHist=[], netHist=[];
function pushHistory(arr, val) {
  arr.push(val);
  if (arr.length > 8) arr.shift();
}
function updateSparkline(id, arr, cls) {
  var bars = document.querySelectorAll('#' + id + ' .spark-bar');
  var max = Math.max.apply(null, arr) || 1;
  for (var i = 0; i < bars.length; i++) {
    bars[i].style.height = ((arr[i] || 0) / max * 90 + 5) + '%';
  }
}

// ── NET SPARKLINE RANDOM ──
setInterval(function() {
  pushHistory(netHist, Math.random() * 100);
  updateSparkline('net-spark', netHist, '');
}, 800);

// ── STATS (called from Python) ──
function updateStats(cpu, ram, disk, bat, procs) {
  document.getElementById('cpu-v').textContent  = cpu  + '%';
  document.getElementById('ram-v').textContent  = ram  + '%';
  document.getElementById('disk-v').textContent = disk + '%';
  document.getElementById('bat-v').textContent  = bat  + '%';
  document.getElementById('proc-v').textContent = procs;

  document.getElementById('cpu-b').style.width  = cpu  + '%';
  document.getElementById('ram-b').style.width  = ram  + '%';
  document.getElementById('disk-b').style.width = disk + '%';
  document.getElementById('bat-b').style.width  = (isNaN(bat)?0:bat) + '%';
  document.getElementById('proc-b').style.width = Math.min(procs/5,100) + '%';

  pushHistory(cpuHist, cpu);
  pushHistory(ramHist, ram);
  updateSparkline('cpu-spark', cpuHist, '');
  updateSparkline('ram-spark', ramHist, 'red');

  // High CPU alert
  var alert = document.getElementById('alert-border');
  var lbl   = document.getElementById('sys-label');
  if (cpu > 85) {
    alert.style.display = 'block';
    lbl.textContent = '⚠ HIGH CPU DETECTED';
    lbl.style.color = '#ff2a2a';
  } else {
    alert.style.display = 'none';
    lbl.textContent = 'ALL SYSTEMS NOMINAL';
    lbl.style.color = '';
  }
}

// ── STATUS LINE ──
function setStatus(text) {
  var el = document.getElementById('status-line');
  el.textContent = text;
  el.className = '';
  var t = text.toLowerCase();
  if (t.includes('listen'))     el.className = 'listening';
  else if (t.includes('recog')) el.className = 'recognizing';
  else if (t.includes('sir') || t.includes('opening') || t.includes('jarvis is')) el.className = 'speaking';
}

// ── LISTEN INDICATOR ──
function setListening(active) {
  var badge = document.getElementById('listen-badge');
  var ring  = document.getElementById('listen-ring');
  if (active) {
    badge.classList.add('show');
    ring.classList.add('active');
  } else {
    badge.classList.remove('show');
    ring.classList.remove('active');
  }
}

// ── COMMAND LOG ──
var logs = [];
function addLog(entry) {
  logs.push(entry);
  if (logs.length > 5) logs.shift();
  var html = '';
  for (var i = 0; i < logs.length; i++) {
    var cls = (i === logs.length-1) ? 'active' : '';
    html += '<div class="log-entry ' + cls + '">&rsaquo; ' + logs[i] + '</div>';
  }
  document.getElementById('log-list').innerHTML = html;
}

// ── BOOT SEQUENCE ──
var bootMsgs = [
  'LOADING NEURAL CORE...',
  'VOICE ENGINE ONLINE',
  'BIOMETRICS VERIFIED',
  'SCANNING HARDWARE...',
  'ALL SYSTEMS GO',
  'TELL ME SIR'
];
var bi = 0;
function boot() {
  if (bi < bootMsgs.length) {
    setStatus(bootMsgs[bi]);
    addLog(bootMsgs[bi]);
    bi++;
    setTimeout(boot, 600);
  }
}
setTimeout(boot, 400);
</script>
</body>
</html>
"""


def _stats_loop(win):
    while True:
        try:
            cpu   = psutil.cpu_percent(interval=None)
            ram   = psutil.virtual_memory().percent
            disk  = psutil.disk_usage("C:\\").percent
            bat   = psutil.sensors_battery()
            b     = int(bat.percent) if bat else 0
            procs = len(psutil.pids())
            win.evaluate_js(f"updateStats({cpu},{ram},{disk},{b},{procs})")
        except:
            pass
        time.sleep(1)


def set_status(win, text):
    try:
        safe = text.replace("'", "").replace('"', '')[:50]
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
        safe = text.replace("'", "").replace('"', '')[:40]
        win.evaluate_js(f"addLog('{safe}')")
    except:
        pass


def iron_gui():
    global _window
    _window = webview.create_window(
        "J.A.R.V.I.S — Stark Industries",
        html=HTML,
        width=1000,
        height=700,
        resizable=True,
    )
    threading.Thread(target=_stats_loop, args=(_window,), daemon=True).start()
    webview.start(gui="edgechromium")