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

html_content = """
<!DOCTYPE html>
<html>
<head>
<style>
body { background: radial-gradient(circle,#001219 0%,#000000 100%);
color:#00f2ff;font-family:Segoe UI;
display:flex;justify-content:center;align-items:center;
height:100vh;margin:0;overflow:hidden;}

.main-container{position:relative;width:500px;height:500px;
display:flex;justify-content:center;align-items:center;}

.ring{position:absolute;border-radius:50%;
border:2px solid transparent;
animation:rotate linear infinite;}

.outer{width:400px;height:400px;
border-top:3px solid #00f2ff;
border-bottom:3px solid #00f2ff;
animation-duration:4s;
box-shadow:0 0 20px #00f2ff;}

.middle{width:300px;height:300px;
border-left:3px solid #ff4d4d;
border-right:3px solid #ff4d4d;
animation-duration:3s;
animation-direction:reverse;
box-shadow:0 0 15px #ff4d4d;}

.inner{width:200px;height:200px;
border-top:3px solid #ffeb3b;
animation-duration:2s;
box-shadow:0 0 10px #ffeb3b;}

.content{text-align:center;z-index:10;}

h1{font-size:2.5rem;letter-spacing:5px;
margin:0;text-shadow:0 0 15px #00f2ff;}

.stats{font-size:1rem;margin-top:10px;
color:#ffffff;line-height:1.6;font-weight:bold;}

@keyframes rotate{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}
</style>
</head>

<body>

<div class="main-container">
<div class="ring outer"></div>
<div class="ring middle"></div>
<div class="ring inner"></div>

<div class="content">
<h1>J.A.R.V.I.S</h1>
<div id="stats-display" class="stats">
SYSTEM INITIALIZING...
</div>
</div>

</div>

<script>
function updateStats(cpu,ram,disk,battery){
document.getElementById("stats-display").innerHTML=
`CPU: ${cpu}% | RAM: ${ram}%<br>DISK: ${disk}% | BAT: ${battery}%`
}
</script>

</body>
</html>
"""


def update_logic(window):

    while True:

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:\\").percent

        bat = psutil.sensors_battery()
        battery = bat.percent if bat else "N/A"

        try:
            window.evaluate_js(
                f"updateStats({cpu},{ram},{disk},'{battery}')"
            )
        except:
            pass

        time.sleep(1)


def iron_gui(root):

    window = webview.create_window(
        "JARVIS SYSTEM",
        html=html_content,
        width=600,
        height=600,
        resizable=False
    )

    threading.Thread(
        target=update_logic,
        args=(window,),
        daemon=True
    ).start()

    webview.start(gui="edgechromium")