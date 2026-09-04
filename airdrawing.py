# import cv2
# import mediapipe as mp
# import numpy as np
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# model_path = "hand_landmarker.task"

# BaseOptions = python.BaseOptions
# HandLandmarker = vision.HandLandmarker
# HandLandmarkerOptions = vision.HandLandmarkerOptions
# VisionRunningMode = vision.RunningMode

# current_color = (255, 0, 0)

# def start_drawing():

#     base_options = BaseOptions(model_asset_path=model_path)

#     options = HandLandmarkerOptions(
#         base_options=base_options,
#         running_mode=VisionRunningMode.IMAGE,
#         num_hands=1
#     )

#     landmarker = HandLandmarker.create_from_options(options)

#     cap = cv2.VideoCapture(0)
#     canvas = None
#     prev_x, prev_y = 0, 0

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         frame = cv2.flip(frame, 1)

#         if canvas is None:
#             canvas = np.zeros_like(frame)

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         mp_image = mp.Image(
#             image_format=mp.ImageFormat.SRGB,
#             data=rgb_frame
#         )

#         result = landmarker.detect(mp_image)

#         if result.hand_landmarks:
#             for hand_landmarks in result.hand_landmarks:

#                 h, w, _ = frame.shape

#                 index_tip = hand_landmarks[8]
#                 middle_tip = hand_landmarks[12]
#                 ring_tip = hand_landmarks[16]

#                 index_pip = hand_landmarks[6]
#                 middle_pip = hand_landmarks[10]
#                 ring_pip = hand_landmarks[14]

#                 ix, iy = int(index_tip.x * w), int(index_tip.y * h)

#                 index_up = index_tip.y < index_pip.y
#                 middle_up = middle_tip.y < middle_pip.y
#                 ring_up = ring_tip.y < ring_pip.y

#                 # CLEAR
#                 if index_up and middle_up and ring_up:
#                     canvas = np.zeros_like(frame)
#                     prev_x, prev_y = 0, 0

#                 # ERASER
#                 elif index_up and middle_up:
#                     cv2.circle(canvas, (ix, iy), 20, (0, 0, 0), -1)
#                     prev_x, prev_y = 0, 0

#                 # DRAW
#                 elif index_up and not middle_up:
#                     if prev_x == 0 and prev_y == 0:
#                         prev_x, prev_y = ix, iy

#                     cv2.line(canvas, (prev_x, prev_y), (ix, iy), current_color, 5)
#                     prev_x, prev_y = ix, iy

#                 else:
#                     prev_x, prev_y = 0, 0

#         combined = cv2.add(frame, canvas)
#         cv2.imshow("Jarvis Air Canvas", combined)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # 👇 YE LOOP KE BAHAR HONA CHAHIYE
#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     start_drawing()
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   J.A.R.V.I.S  x  DOCTOR STRANGE  —  NEXUS AIR CANVAS  ULTIMATE v9.0       ║
║   STARK INDUSTRIES  x  MASTERS OF THE MYSTIC ARTS                           ║
║   ⚡ Iron Man HUD  🔮 Strange Mandalas  💎 Vibranium  ⚡ Asgard Lightning   ║
╚══════════════════════════════════════════════════════════════════════════════╝

JARVIS VOICE ASSISTANT COMPATIBLE — from airdrawing import start_drawing
"""

import cv2
import mediapipe as mp
import numpy as np
import collections
import time
import math
import random
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

# ══════════════════════════════════════════════════════
#  4 HERO MODES
# ══════════════════════════════════════════════════════
HERO_MODES = ["STARK", "STRANGE", "WAKANDA", "ASGARD"]

HERO_PALETTES = {
    "STARK": [
        ("ARC BLUE",  (255, 210,  60)),
        ("GOLD",      ( 30, 180, 255)),
        ("REPULSOR",  (255, 255,   0)),
        ("PLASMA",    (  0,  60, 255)),
        ("WHITE HOT", (255, 255, 255)),
        ("HULK",      (  0, 220,  60)),
        ("NOVA",      (180,   0, 255)),
        ("SOLAR",     (  0, 200, 255)),
    ],
    "STRANGE": [
        ("SLING GOLD",(  0, 180, 255)),
        ("PORTAL",    ( 30, 100, 255)),
        ("MYSTIC",    (200,  50, 255)),
        ("RUNE",      (255, 200,  80)),
        ("ASTRAL",    (255, 255, 200)),
        ("DARK DIM",  ( 80,  20, 140)),
        ("MIRROR",    (180, 220, 255)),
        ("EYE",       (  0, 230, 200)),
    ],
    "WAKANDA": [
        ("VIBRANIUM", (255,  60, 180)),
        ("PURPLE",    (200,   0, 255)),
        ("PANTHER",   ( 60,  20, 100)),
        ("GOLD",      ( 20, 180, 255)),
        ("TECH",      (  0, 255, 200)),
        ("HEART HRB", (  0,  30, 180)),
        ("WHITE",     (240, 240, 240)),
        ("CLAW",      (  0, 200, 255)),
    ],
    "ASGARD": [
        ("LIGHTNING", (255, 255, 100)),
        ("BIFROST",   (255, 100, 200)),
        ("MJOLNIR",   (180, 180, 200)),
        ("FROST",     (200, 230, 255)),
        ("LOKI",      ( 80, 200,  80)),
        ("STORM",     (255, 200,  60)),
        ("GOLD",      ( 30, 180, 255)),
        ("VOID",      ( 20,  20,  40)),
    ],
}

HERO_ACCENTS = {
    "STARK":   (0, 210, 255),
    "STRANGE": (0, 160, 255),
    "WAKANDA": (200, 0, 255),
    "ASGARD":  (200, 200, 60),
}

BRUSH_SIZES = [2, 5, 9, 15, 22, 32]
ERASER_R    = 40
TOOLBAR_H   = 105


# ══════════════════════════════════════════════════════
#  PARTICLE SYSTEM
# ══════════════════════════════════════════════════════
class Particle:
    __slots__ = ['x','y','vx','vy','life','color','size','ptype','angle','spin']
    def __init__(self, x, y, color, ptype="spark"):
        angle      = random.uniform(0, 2*math.pi)
        speed      = random.uniform(0.3, 3.5)
        self.x     = float(x)
        self.y     = float(y)
        self.vx    = math.cos(angle)*speed
        self.vy    = math.sin(angle)*speed
        self.life  = random.uniform(0.5, 1.2)
        self.color = color
        self.size  = random.randint(1, 4)
        self.ptype = ptype
        self.angle = angle
        self.spin  = random.uniform(-0.15, 0.15)

    def update(self, dt):
        self.x    += self.vx
        self.y    += self.vy
        if self.ptype == "spark":      self.vy += 0.06
        elif self.ptype == "rune":     self.vy -= 0.02; self.vx *= 0.97
        elif self.ptype == "lightning":
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-0.5, 0.5)
        self.angle += self.spin
        self.life  -= dt * 1.4

    def draw(self, img):
        if self.life <= 0: return
        a     = min(1.0, self.life)
        faded = (int(self.color[0]*a), int(self.color[1]*a), int(self.color[2]*a))
        ix,iy = int(self.x), int(self.y)
        if not (0 <= ix < img.shape[1] and 0 <= iy < img.shape[0]): return
        if self.ptype == "rune":
            s  = self.size + 2
            ca = math.cos(self.angle); sa = math.sin(self.angle)
            pts= np.array([[ix+int(s*ca),iy+int(s*sa)],[ix+int(s*(-sa)),iy+int(s*ca)],
                           [ix+int(s*(-ca)),iy+int(s*(-sa))],[ix+int(s*sa),iy+int(s*(-ca))]],np.int32)
            cv2.polylines(img,[pts],True,faded,1,cv2.LINE_AA)
        elif self.ptype == "mandala":
            cv2.circle(img,(ix,iy),self.size+1,faded,1,cv2.LINE_AA)
            cv2.circle(img,(ix,iy),1,faded,-1)
        else:
            cv2.circle(img,(ix,iy),self.size,faded,-1)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, color, n=4, ptype="spark"):
        for _ in range(n):
            self.particles.append(Particle(x, y, color, ptype))

    def update_draw(self, img, dt):
        alive = []
        for p in self.particles:
            p.update(dt)
            if p.life > 0:
                p.draw(img)
                alive.append(p)
        self.particles = alive[:500]


# ══════════════════════════════════════════════════════
#  DR STRANGE EFFECTS
# ══════════════════════════════════════════════════════
def draw_strange_mandala(img, cx, cy, r, t, color, alpha=0.6):
    lay    = np.zeros_like(img)
    spokes = 12
    for ri in range(1, 5):
        cv2.circle(lay,(cx,cy),int(r*ri/4),color,1,cv2.LINE_AA)
    for s in range(spokes):
        angle = t*1.5 + s*(2*math.pi/spokes)
        cv2.line(lay,(cx,cy),(cx+int(r*math.cos(angle)),cy+int(r*math.sin(angle))),color,1,cv2.LINE_AA)
    for s in range(6):
        angle = -t*2.2 + s*(math.pi/3)
        ir = r//2
        cv2.circle(lay,(cx+int(ir*math.cos(angle)),cy+int(ir*math.sin(angle))),3,color,-1)
    blur = cv2.GaussianBlur(lay,(15,15),0)
    cv2.addWeighted(img,1.0,blur,alpha*0.8,0,img)
    cv2.addWeighted(img,1.0,lay,alpha*0.4,0,img)


def draw_sling_ring(img, cx, cy, r, t, color):
    lay = np.zeros_like(img)
    for i in range(0,360,6):
        a1=math.radians(i+t*120); a2=math.radians(i+t*120+4)
        cv2.line(lay,(cx+int(r*math.cos(a1)),cy+int(r*math.sin(a1))),
                      (cx+int(r*math.cos(a2)),cy+int(r*math.sin(a2))),color,2,cv2.LINE_AA)
    r2=int(r*0.65)
    for i in range(0,360,10):
        a1=math.radians(i-t*180)
        cv2.circle(lay,(cx+int(r2*math.cos(a1)),cy+int(r2*math.sin(a1))),2,color,-1)
    cv2.addWeighted(img,1.0,cv2.GaussianBlur(lay,(19,19),0),0.9,0,img)
    cv2.addWeighted(img,1.0,lay,0.6,0,img)


# ══════════════════════════════════════════════════════
#  DRAW MODES
# ══════════════════════════════════════════════════════
def lightning_line(canvas, p1, p2, color, thick):
    if p1==(0,0) or p2==(0,0): return
    dx=p2[0]-p1[0]; dy=p2[1]-p1[1]
    dist=max(1,int(math.hypot(dx,dy))); steps=max(2,dist//8)
    pts=[p1]
    for i in range(1,steps):
        tt=i/steps
        pts.append((int(p1[0]+dx*tt+random.uniform(-6,6)*(1-abs(tt-0.5)*2)),
                    int(p1[1]+dy*tt+random.uniform(-6,6)*(1-abs(tt-0.5)*2))))
    pts.append(p2)
    for i in range(len(pts)-1):
        lay=np.zeros_like(canvas)
        cv2.line(lay,pts[i],pts[i+1],color,thick+10,cv2.LINE_AA)
        cv2.addWeighted(canvas,1.0,cv2.GaussianBlur(lay,(15,15),0),0.4,0,canvas)
        cv2.line(canvas,pts[i],pts[i+1],color,thick+3,cv2.LINE_AA)
        cv2.line(canvas,pts[i],pts[i+1],(255,255,255),max(1,thick-1),cv2.LINE_AA)


def vibranium_line(canvas, p1, p2, color, thick):
    if p1==(0,0) or p2==(0,0): return
    dx=p2[0]-p1[0]; dy=p2[1]-p1[1]; dist=max(1,int(math.hypot(dx,dy)))
    lay=np.zeros_like(canvas)
    cv2.line(lay,p1,p2,color,thick+14,cv2.LINE_AA)
    cv2.addWeighted(canvas,1.0,cv2.GaussianBlur(lay,(21,21),0),0.6,0,canvas)
    cv2.line(canvas,p1,p2,color,thick+4,cv2.LINE_AA)
    perp_x=-dy/max(1,dist); perp_y=dx/max(1,dist)
    for off in [-8,8]:
        cv2.line(canvas,(int(p1[0]+perp_x*off),int(p1[1]+perp_y*off)),
                        (int(p2[0]+perp_x*off),int(p2[1]+perp_y*off)),
                        tuple(int(c*0.4) for c in color),max(1,thick-2),cv2.LINE_AA)
    cv2.line(canvas,p1,p2,(255,255,255),max(1,thick-3),cv2.LINE_AA)


def neon_line(canvas, p1, p2, color, thick):
    if p1==(0,0) or p2==(0,0): return
    lay=np.zeros_like(canvas)
    cv2.line(lay,p1,p2,color,thick+18,cv2.LINE_AA)
    cv2.addWeighted(canvas,1.0,cv2.GaussianBlur(lay,(25,25),0),0.5,0,canvas)
    cv2.line(canvas,p1,p2,color,thick+6,cv2.LINE_AA)
    cv2.line(canvas,p1,p2,tuple(min(255,int(c*1.8)) for c in color),max(1,thick-1),cv2.LINE_AA)
    cv2.line(canvas,p1,p2,(255,255,255),max(1,thick-3),cv2.LINE_AA)


def draw_stroke(canvas, p1, p2, color, thick, hero):
    if   hero=="ASGARD":  lightning_line(canvas,p1,p2,color,thick)
    elif hero=="WAKANDA": vibranium_line(canvas,p1,p2,color,thick)
    else:                 neon_line(canvas,p1,p2,color,thick)


# ══════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════
def dist2d(a,b): return math.hypot(a[0]-b[0],a[1]-b[1])

def fingers_up(lm):
    up=[lm[4].x<lm[3].x]
    for tip,pip in [(8,6),(12,10),(16,14),(20,18)]:
        up.append(lm[tip].y<lm[pip].y)
    return up

def apply_scanlines(img,skip=4,alpha=0.05):
    scan=img.copy()
    for y in range(0,img.shape[0],skip): scan[y]=(scan[y]*0.25).astype(np.uint8)
    cv2.addWeighted(img,1-alpha,scan,alpha,0,img)

def glass_rect(img,x1,y1,x2,y2,bg=(8,12,22),alpha=0.80,border=None):
    ov=img.copy(); cv2.rectangle(ov,(x1,y1),(x2,y2),bg,-1)
    cv2.addWeighted(ov,alpha,img,1-alpha,0,img)
    if border: cv2.rectangle(img,(x1,y1),(x2,y2),border,1)

def corner_brackets(img,x1,y1,x2,y2,color,length=18,thick=2):
    for c in [((x1,y1),(x1+length,y1),(x1,y1+length)),((x2,y1),(x2-length,y1),(x2,y1+length)),
              ((x1,y2),(x1+length,y2),(x1,y2-length)),((x2,y2),(x2-length,y2),(x2,y2-length))]:
        cv2.line(img,c[0],c[1],color,thick,cv2.LINE_AA)
        cv2.line(img,c[0],c[2],color,thick,cv2.LINE_AA)

def text_c(img,txt,cx,cy,scale,color,thick=1):
    (tw,th),_=cv2.getTextSize(txt,cv2.FONT_HERSHEY_SIMPLEX,scale,thick)
    cv2.putText(img,txt,(cx-tw//2,cy+th//2),cv2.FONT_HERSHEY_SIMPLEX,scale,color,thick,cv2.LINE_AA)

def glow_circle(img,cx,cy,r,color,thick=2):
    cx,cy,r=int(cx),int(cy),max(1,int(r))
    lay=np.zeros_like(img); cv2.circle(lay,(cx,cy),r,color,thick)
    cv2.addWeighted(img,1.0,cv2.GaussianBlur(lay,(15,15),0),0.8,0,img)
    cv2.circle(img,(cx,cy),r,color,thick,cv2.LINE_AA)

def pulse_ring(img,cx,cy,t,color,base_r=30):
    cx,cy=int(cx),int(cy)
    r=max(1,base_r+int(8*math.sin(t*3.0))); af=0.5+0.5*math.sin(t*3.0)
    lay=np.zeros_like(img); cv2.circle(lay,(cx,cy),r,color,2)
    cv2.addWeighted(img,1.0,cv2.GaussianBlur(lay,(11,11),0),af*0.6,0,img)
    cv2.circle(img,(cx,cy),r,color,1,cv2.LINE_AA)


# ══════════════════════════════════════════════════════
#  VOICE LOG
# ══════════════════════════════════════════════════════
class VoiceLog:
    def __init__(self,maxlines=8):
        self.lines=collections.deque(maxlen=maxlines)
        self.ts=collections.deque(maxlen=maxlines)

    def log(self,msg): self.lines.append(msg); self.ts.append(time.time())

    def draw(self,img,x,y,w,accent):
        now=time.time()
        glass_rect(img,x,y,x+w,y+len(self.lines)*18+22,(5,8,15),0.82,accent)
        cv2.putText(img,"NEXUS LOG",(x+8,y+13),cv2.FONT_HERSHEY_SIMPLEX,0.30,accent,1,cv2.LINE_AA)
        for i,(ln,ts) in enumerate(zip(self.lines,self.ts)):
            a=max(0.0,1.0-(now-ts)/9.0)
            clr=(int(accent[0]*a),int(accent[1]*a),int(accent[2]*a))
            cv2.putText(img,f"> {ln}",(x+8,y+26+i*17),cv2.FONT_HERSHEY_SIMPLEX,0.28,clr,1,cv2.LINE_AA)


# ══════════════════════════════════════════════════════
#  RADAR
# ══════════════════════════════════════════════════════
def draw_radar(img,cx,cy,r,t,hx,hy,W,H,accent):
    lay=np.zeros_like(img); cv2.circle(lay,(cx,cy),r,(0,40,15),-1)
    cv2.addWeighted(img,1.0,lay,0.55,0,img)
    for ri in [r//4,r//2,3*r//4,r]: cv2.circle(img,(cx,cy),ri,(0,80,30),1,cv2.LINE_AA)
    cv2.line(img,(cx-r,cy),(cx+r,cy),(0,80,30),1); cv2.line(img,(cx,cy-r),(cx,cy+r),(0,80,30),1)
    sweep=(t*100)%360
    ex=cx+int(r*math.cos(math.radians(sweep))); ey=cy+int(r*math.sin(math.radians(sweep)))
    lay2=np.zeros_like(img); cv2.line(lay2,(cx,cy),(ex,ey),(0,255,80),2)
    cv2.addWeighted(img,1.0,cv2.GaussianBlur(lay2,(9,9),0),0.7,0,img)
    cv2.line(img,(cx,cy),(ex,ey),(0,255,80),1,cv2.LINE_AA)
    if hx>0 and hy>0:
        bx=max(cx-r,min(cx+r,cx+int((hx/W-0.5)*r*2)))
        by=max(cy-r,min(cy+r,cy+int((hy/H-0.5)*r*2)))
        glow_circle(img,bx,by,6,accent,2)
    cv2.circle(img,(cx,cy),r,accent,2,cv2.LINE_AA)
    text_c(img,"TRACK",cx,cy+r+10,0.26,accent)


def draw_power_bar(img,x,y,w,h,val,label,color,accent):
    glass_rect(img,x,y,x+w,y+h,(5,5,15),0.8,accent)
    if int(w*val)>0:
        lay=np.zeros_like(img); cv2.rectangle(lay,(x,y),(x+int(w*val),y+h),color,-1)
        cv2.addWeighted(img,1.0,lay,0.7,0,img)
    cv2.putText(img,f"{label}:{int(val*100)}%",(x+4,y+h-3),cv2.FONT_HERSHEY_SIMPLEX,0.26,(200,220,255),1,cv2.LINE_AA)


# ══════════════════════════════════════════════════════
#  HERO BACKGROUND
# ══════════════════════════════════════════════════════
def apply_hero_bg(frame,hero,t,H,W):
    if hero=="STRANGE":
        for cx2,cy2 in [(80,H-80),(W-80,H-80)]:
            draw_strange_mandala(frame,cx2,cy2,55,t,(0,120,200),0.2)
    elif hero=="WAKANDA":
        p=0.07+0.03*math.sin(t*1.5)
        lay=np.zeros_like(frame); cv2.rectangle(lay,(0,TOOLBAR_H),(W,H),(60,0,80),-1)
        cv2.addWeighted(frame,1.0,lay,p,0,frame)
    elif hero=="ASGARD":
        for x in range(0,W,50):
            al=0.03+0.02*math.sin(t*3+x*0.05)
            lay=np.zeros_like(frame)
            c=(int(80+80*math.sin(t+x*0.1)),int(80+80*math.sin(t*1.3+x*0.08)),
               int(160+55*math.sin(t*0.7+x*0.12)))
            cv2.line(lay,(x,TOOLBAR_H),(x,H),c,1)
            cv2.addWeighted(frame,1.0,lay,al,0,frame)


# ══════════════════════════════════════════════════════
#  FULL HUD
# ══════════════════════════════════════════════════════
def draw_hud(frame,col_idx,thick_idx,mode,undo_count,show_help,fps,t,
             hand_x,hand_y,W,H,voice_log,stroke_count,session_secs,
             hero,hero_idx,palette,accent):

    SW,SH,SPAD,sw_start=52,70,4,360

    # Toolbar
    glass_rect(frame,0,0,W,TOOLBAR_H,(4,6,14),0.90,accent)
    ba=0.4+0.4*math.sin(t*2.0); lay=np.zeros_like(frame)
    cv2.line(lay,(0,TOOLBAR_H),(W,TOOLBAR_H),accent,3)
    cv2.addWeighted(frame,1.0,cv2.GaussianBlur(lay,(9,9),0),ba,0,frame)
    cv2.line(frame,(0,TOOLBAR_H),(W,TOOLBAR_H),accent,1,cv2.LINE_AA)

    # Title
    titles={"STARK":("STARK INDUSTRIES","J.A.R.V.I.S  NEXUS AIR CANVAS  v9.0"),
            "STRANGE":("MASTERS OF MYSTIC ARTS","DR.STRANGE  SLING-RING  CANVAS  v9.0"),
            "WAKANDA":("WAKANDA FOREVER","SHURI  VIBRANIUM  CANVAS  v9.0"),
            "ASGARD":("ASGARD  BIFROST","THOR  LIGHTNING  CANVAS  v9.0")}
    sub,title=titles[hero]
    cv2.putText(frame,sub,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.38,accent,1,cv2.LINE_AA)
    cv2.putText(frame,title,(10,44),cv2.FONT_HERSHEY_SIMPLEX,0.48,(0,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,f"HERO: {hero}  |  NEXUS ONLINE",(10,68),cv2.FONT_HERSHEY_SIMPLEX,0.28,(0,130,150),1,cv2.LINE_AA)

    # Hero emblem
    arc_cx,arc_cy=330,52
    if hero=="STARK":
        pulse_ring(frame,arc_cx,arc_cy,t,accent,20)
        cv2.circle(frame,(arc_cx,arc_cy),11,(0,180,255),-1)
        cv2.circle(frame,(arc_cx,arc_cy),5,(200,240,255),-1)
    elif hero=="STRANGE":
        draw_sling_ring(frame,arc_cx,arc_cy,18+int(4*math.sin(t*2)),t,accent)
        cv2.circle(frame,(arc_cx,arc_cy),5,accent,-1)
    elif hero=="WAKANDA":
        for i in range(3):
            ang=math.pi*0.3+i*0.25
            cv2.line(frame,(arc_cx+int(8*math.cos(ang)),arc_cy-10),
                           (arc_cx+int(10*math.cos(ang+0.1)),arc_cy+10),accent,2,cv2.LINE_AA)
        cv2.circle(frame,(arc_cx,arc_cy),14,accent,2,cv2.LINE_AA)
    elif hero=="ASGARD":
        pts=np.array([[arc_cx-6,arc_cy-14],[arc_cx+4,arc_cy-2],
                      [arc_cx-2,arc_cy+2],[arc_cx+8,arc_cy+14]],np.int32)
        cv2.polylines(frame,[pts],False,accent,3,cv2.LINE_AA)
        pulse_ring(frame,arc_cx,arc_cy,t,accent,16)

    # Color swatches
    for i,(name,val) in enumerate(palette):
        x1=sw_start+i*(SW+SPAD); x2=x1+SW; y1,y2=6,6+SH
        cv2.rectangle(frame,(x1,y1),(x2,y2),val,-1)
        ref=np.zeros_like(frame); cv2.rectangle(ref,(x1,y1),(x2,y1+16),(255,255,255),-1)
        cv2.addWeighted(frame,1.0,ref,0.07,0,frame)
        if i==col_idx:
            for bw,ba2 in [(8,0.3),(4,0.6),(1,1.0)]:
                bl=np.zeros_like(frame); cv2.rectangle(bl,(x1-bw,y1-bw),(x2+bw,y2+bw),(0,255,255),2)
                cv2.addWeighted(frame,1.0,cv2.GaussianBlur(bl,(11,11),0),ba2*0.45,0,frame)
            cv2.rectangle(frame,(x1-2,y1-2),(x2+2,y2+2),(0,255,255),2)
            cv2.fillPoly(frame,[np.array([[x1+SW//2-5,y2+2],[x1+SW//2+5,y2+2],[x1+SW//2,y2+9]])],(0,255,255))
        else:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(40,50,65),1)
        text_c(frame,name[:4],(x1+x2)//2,(y1+y2)//2,0.24,(0,0,0),1)

    # Brush sizes
    tx0=sw_start+len(palette)*(SW+SPAD)+16
    for i,sz in enumerate(BRUSH_SIZES):
        cx2=tx0+i*48+24; cy2=TOOLBAR_H//2; r=sz//2+5
        if i==thick_idx:
            pulse_ring(frame,cx2,cy2,t,(0,255,255),r+5)
            cv2.circle(frame,(cx2,cy2),r,palette[col_idx][1],-1)
            cv2.circle(frame,(cx2,cy2),r,(0,255,255),1,cv2.LINE_AA)
        else:
            cv2.circle(frame,(cx2,cy2),r,(35,40,55),-1)
            cv2.circle(frame,(cx2,cy2),r,(70,80,100),1,cv2.LINE_AA)

    # Hero switcher buttons
    hm_x=tx0+len(BRUSH_SIZES)*48+20
    cv2.putText(frame,"HERO",(hm_x,28),cv2.FONT_HERSHEY_SIMPLEX,0.28,accent,1,cv2.LINE_AA)
    for i,hm in enumerate(HERO_MODES):
        hx2=hm_x+i*56; hy2=36
        bg_c=(int(accent[0]*0.25),int(accent[1]*0.25),int(accent[2]*0.25)) if hm==hero else (28,30,48)
        cv2.rectangle(frame,(hx2,hy2),(hx2+52,hy2+24),bg_c,-1)
        cv2.rectangle(frame,(hx2,hy2),(hx2+52,hy2+24),accent if hm==hero else (50,60,80),1)
        text_c(frame,hm[:4],(hx2+26),(hy2+12),0.24,(0,255,255) if hm==hero else (110,130,150),1)

    # Right panel
    rpx,rpy=W-195,5
    glass_rect(frame,rpx-5,rpy,W-2,TOOLBAR_H-4,(8,10,20),0.86,accent)
    corner_brackets(frame,rpx-5,rpy,W-2,TOOLBAR_H-4,accent,10)
    mc={"DRAW":(0,255,120),"ERASE":(0,60,255),"IDLE":(80,100,120)}.get(mode,(200,200,200))
    cv2.putText(frame,f"MODE: {mode}",(rpx,rpy+18),cv2.FONT_HERSHEY_SIMPLEX,0.46,mc,2,cv2.LINE_AA)
    cv2.putText(frame,f"FPS  {fps:05.1f}",(rpx,rpy+36),cv2.FONT_HERSHEY_SIMPLEX,0.33,(0,180,200),1,cv2.LINE_AA)
    cv2.putText(frame,f"UNDO {undo_count:03d}",(rpx,rpy+52),cv2.FONT_HERSHEY_SIMPLEX,0.33,(0,180,200),1,cv2.LINE_AA)
    cv2.putText(frame,f"STRK {stroke_count:04d}",(rpx,rpy+68),cv2.FONT_HERSHEY_SIMPLEX,0.33,(0,180,200),1,cv2.LINE_AA)
    cv2.putText(frame,f"TIME {int(session_secs)//60:02d}:{int(session_secs)%60:02d}",
                (rpx,rpy+84),cv2.FONT_HERSHEY_SIMPLEX,0.33,(0,180,200),1,cv2.LINE_AA)

    # Radar + power bars
    rcx,rcy,rr=75,H-90,55
    draw_radar(frame,rcx,rcy,rr,t,hand_x,hand_y,W,H,accent)
    pbx,pby=rcx+rr+16,H-138
    draw_power_bar(frame,pbx,pby,   110,15,0.72+0.05*math.sin(t*1.3),"PWR",(0,210,255),accent)
    draw_power_bar(frame,pbx,pby+20,110,15,0.88,"SUIT",(0,180,200),accent)
    draw_power_bar(frame,pbx,pby+40,110,15,min(1.0,fps/60),"PROC",(0,255,120),accent)
    if hero=="STRANGE":
        draw_power_bar(frame,pbx,pby+60,110,15,0.65+0.1*math.sin(t*0.8),"MYSTIC",(0,160,255),accent)
    voice_log.draw(frame,pbx+124,pby-8,230,accent)

    # Bottom bar
    glass_rect(frame,0,H-24,W,H,(4,6,14),0.84,(0,60,90))
    cv2.putText(frame,
        f"  {hero}  |  COLOR:{palette[col_idx][0]}  SIZE:{BRUSH_SIZES[thick_idx]}px  |  "
        f"[1-8]Color [+/-]Size [E]Erase [Z]Undo [C]Clear [S]Save [M]Hero [H]Help [Q]Quit",
        (8,H-7),cv2.FONT_HERSHEY_SIMPLEX,0.27,(0,150,180),1,cv2.LINE_AA)

    # Help
    if show_help:
        lines=[
            (f"=== {hero} MODE CONTROLS ===",(0,255,255)),
            ("---------------------------",(0,80,100)),
            ("GESTURES:",(0,200,180)),
            ("1 Finger   ->  DRAW",(0,210,160)),
            ("2 Fingers  ->  ERASE",(0,210,160)),
            ("3 Fingers  ->  CLEAR",(0,210,160)),
            ("4 Fingers  ->  NEXT HERO !",(0,255,200)),
            ("Fist       ->  PAUSE",(0,210,160)),
            ("Pinch      ->  COLOR",(0,210,160)),
            ("Thumb UP   ->  BIGGER",(0,210,160)),
            ("Pinky UP   ->  SMALLER",(0,210,160)),
            ("---------------------------",(0,80,100)),
            ("KEYBOARD:",(0,200,180)),
            ("1-8 Color  +/- Brush",(0,190,210)),
            ("Z Undo     E Erase",(0,190,210)),
            ("C Clear    S Save",(0,190,210)),
            ("M Hero     H Help  Q Quit",(0,190,210)),
        ]
        hx2=W-270; hy0=TOOLBAR_H+12; bh=len(lines)*19+16
        glass_rect(frame,hx2-10,hy0-8,hx2+265,hy0+bh,(4,6,14),0.90,accent)
        corner_brackets(frame,hx2-10,hy0-8,hx2+265,hy0+bh,accent,14)
        for j,(ln,clr) in enumerate(lines):
            cv2.putText(frame,ln,(hx2,hy0+j*19),cv2.FONT_HERSHEY_SIMPLEX,0.32,clr,1,cv2.LINE_AA)


# ══════════════════════════════════════════════════════
#  MAIN — JARVIS CALLS THIS
# ══════════════════════════════════════════════════════
def start_drawing():
    """JARVIS voice assistant se call hoti hai: from airdrawing import start_drawing"""

    print("""
╔══════════════════════════════════════════════════════════╗
║  NEXUS AIR CANVAS  ULTIMATE v9.0                        ║
║  J.A.R.V.I.S  x  DR.STRANGE  x  WAKANDA  x  ASGARD     ║
║  Loading all systems...                                 ║
╚══════════════════════════════════════════════════════════╝
    """)

    if not os.path.exists(MODEL_PATH):
        print("[ERROR] hand_landmarker.task nahi mili!")
        print("Download: https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        return

    base_opt=python.BaseOptions(model_asset_path=MODEL_PATH)
    options=vision.HandLandmarkerOptions(base_options=base_opt,
        running_mode=vision.RunningMode.IMAGE,num_hands=1,
        min_hand_detection_confidence=0.6,min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.5)
    detector=vision.HandLandmarker.create_from_options(options)

    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280); cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720); cap.set(cv2.CAP_PROP_FPS,30)
    ret,f0=cap.read()
    if not ret: print("[ERROR] Camera nahi mili!"); cap.release(); detector.close(); return
    H,W=f0.shape[:2]

    canvas=np.zeros((H,W,3),dtype=np.uint8)
    undo_stack=collections.deque(maxlen=30)
    hero_idx=0; col_idx=0; thick_idx=1; mode="IDLE"; show_help=True
    sx,sy=0,0; px,py=0,0; ALPHA=0.55
    gesture_ts=0.0; G_COOL=0.55
    fps_ts=time.time(); fps_val=30.0; frame_cnt=0
    session_start=time.time(); stroke_count=0; last_t=time.time()

    particles=ParticleSystem()
    voice_log=VoiceLog(8)
    voice_log.log("NEXUS ONLINE. Avengers assemble!")
    voice_log.log("STARK mode active.")
    voice_log.log("4 fingers = switch hero!")

    def hero():    return HERO_MODES[hero_idx]
    def palette(): return HERO_PALETTES[hero()]
    def accent():  return HERO_ACCENTS[hero()]
    def ptype():   return {"STARK":"spark","STRANGE":"rune","WAKANDA":"mandala","ASGARD":"lightning"}.get(hero(),"spark")
    def push_undo(): undo_stack.append(canvas.copy())

    SW,SH,SPAD,sw_start=52,70,4,360

    cv2.namedWindow("NEXUS AIR CANVAS",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("NEXUS AIR CANVAS",W,H)
    print("[NEXUS] All systems go!")

    while True:
        ret,frame=cap.read()
        if not ret: break
        frame=cv2.flip(frame,1); H,W=frame.shape[:2]
        now=time.time(); dt=max(0.001,now-last_t); last_t=now; t=now-session_start
        frame_cnt+=1
        if now-fps_ts>=1.0: fps_val=frame_cnt/(now-fps_ts); frame_cnt=0; fps_ts=now

        pal=palette(); acc=accent()
        apply_hero_bg(frame,hero(),t,H,W)

        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        mp_img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
        result=detector.detect(mp_img)
        hand_x,hand_y=0,0

        if result.hand_landmarks:
            lm=result.hand_landmarks[0]
            rx=int(lm[8].x*W); ry=int(lm[8].y*H); hand_x,hand_y=rx,ry
            sx=int(ALPHA*rx+(1-ALPHA)*sx) if sx else rx
            sy=int(ALPHA*ry+(1-ALPHA)*sy) if sy else ry
            fu=fingers_up(lm); thumb,index,middle,ring,pinky=fu
            tx_px=int(lm[4].x*W); ty_px=int(lm[4].y*H)
            ix_px=int(lm[8].x*W); iy_px=int(lm[8].y*H)

            # FIST
            if not index and not middle and not ring and not pinky:
                if mode!="IDLE": voice_log.log("Pause.")
                mode="IDLE"; px,py=0,0

            # 4 FINGERS → NEXT HERO
            elif index and middle and ring and pinky and (now-gesture_ts>G_COOL):
                hero_idx=(hero_idx+1)%len(HERO_MODES); col_idx=0; gesture_ts=now; px,py=0,0
                voice_log.log(f"HERO: {hero()} !")
                particles.spawn(sx,sy,acc,25,ptype())

            # 3 FINGERS → CLEAR
            elif index and middle and ring and not pinky and (now-gesture_ts>G_COOL):
                push_undo(); canvas[:]=0; mode="DRAW"; px,py=0,0; gesture_ts=now
                voice_log.log("Canvas cleared.")

            # 2 FINGERS → ERASE
            elif index and middle and not ring:
                if mode!="ERASE": voice_log.log("Eraser on.")
                mode="ERASE"
                if sy>TOOLBAR_H:
                    if (px,py)==(0,0): push_undo()
                    cv2.circle(canvas,(sx,sy),ERASER_R,(0,0,0),-1)
                    particles.spawn(sx,sy,(80,80,100),3,"spark")
                px,py=0,0

            # THUMB PINCH → COLOR
            elif thumb and not middle and not ring and not pinky:
                d=dist2d((tx_px,ty_px),(ix_px,iy_px))
                if d<45 and (now-gesture_ts>G_COOL):
                    col_idx=(col_idx+1)%len(pal); gesture_ts=now
                    voice_log.log(f"Color: {pal[col_idx][0]}")
                mode="DRAW"; px,py=0,0

            # THUMB ONLY → BIGGER
            elif thumb and not index and not middle and not ring:
                if now-gesture_ts>G_COOL:
                    thick_idx=min(thick_idx+1,len(BRUSH_SIZES)-1); gesture_ts=now
                    voice_log.log(f"Size: {BRUSH_SIZES[thick_idx]}px")
                mode="DRAW"; px,py=0,0

            # PINKY → SMALLER
            elif pinky and not index and not middle and not ring:
                if now-gesture_ts>G_COOL:
                    thick_idx=max(thick_idx-1,0); gesture_ts=now
                    voice_log.log(f"Size: {BRUSH_SIZES[thick_idx]}px")
                mode="DRAW"; px,py=0,0

            # INDEX → DRAW / TOOLBAR
            elif index and not middle:
                if sy<TOOLBAR_H:
                    mode="DRAW"
                    for i in range(len(pal)):
                        x1c=sw_start+i*(SW+SPAD)
                        if x1c<sx<x1c+SW and (now-gesture_ts>G_COOL):
                            col_idx=i; gesture_ts=now; voice_log.log(f"Color:{pal[i][0]}"); break
                    tx0c=sw_start+len(pal)*(SW+SPAD)+16
                    for i in range(len(BRUSH_SIZES)):
                        cxc=tx0c+i*48+24
                        if abs(sx-cxc)<24 and (now-gesture_ts>G_COOL):
                            thick_idx=i; gesture_ts=now; voice_log.log(f"Size:{BRUSH_SIZES[i]}px"); break
                    hm_x=tx0c+len(BRUSH_SIZES)*48+20
                    for i,hm in enumerate(HERO_MODES):
                        hx2=hm_x+i*56
                        if hx2<sx<hx2+52 and 36<sy<60 and (now-gesture_ts>G_COOL):
                            hero_idx=i; col_idx=0; gesture_ts=now
                            voice_log.log(f"HERO:{hero()}!"); break
                    px,py=0,0
                else:
                    if mode!="DRAW": voice_log.log("Drawing!")
                    mode="DRAW"
                    if px==0 and py==0:
                        px,py=sx,sy; push_undo(); stroke_count+=1
                    else:
                        draw_stroke(canvas,(px,py),(sx,sy),pal[col_idx][1],BRUSH_SIZES[thick_idx],hero())
                        if dist2d((sx,sy),(px,py))>6:
                            particles.spawn(sx,sy,pal[col_idx][1],3,ptype())
                        px,py=sx,sy
            else:
                px,py=0,0

            # Cursor — int force karo
            isx,isy = int(sx), int(sy)
            if mode=="ERASE":
                glow_circle(frame,isx,isy,ERASER_R,(0,60,255),2)
                cv2.circle(frame,(isx,isy),5,(0,60,255),-1)
                for ang in range(0,360,18):
                    cv2.circle(frame,(isx+int(ERASER_R*math.cos(math.radians(ang))),
                                      isy+int(ERASER_R*math.sin(math.radians(ang)))),1,(0,100,200),-1)
            elif mode=="DRAW":
                rc=int(BRUSH_SIZES[thick_idx]//2+6)
                if hero()=="STRANGE":
                    draw_sling_ring(frame,isx,isy,rc+10,t,acc)
                    cv2.circle(frame,(isx,isy),4,acc,-1)
                elif hero()=="ASGARD":
                    glow_circle(frame,isx,isy,rc,(200,200,60),2)
                    cv2.circle(frame,(isx,isy),3,(255,255,150),-1)
                else:
                    glow_circle(frame,isx,isy,rc,pal[col_idx][1],2)
                    cv2.circle(frame,(isx,isy),3,pal[col_idx][1],-1)
                cv2.line(frame,(isx-rc-4,isy),(isx-rc+2,isy),acc,1)
                cv2.line(frame,(isx+rc-2,isy),(isx+rc+4,isy),acc,1)
                cv2.line(frame,(isx,isy-rc-4),(isx,isy-rc+2),acc,1)
                cv2.line(frame,(isx,isy+rc-2),(isx,isy+rc+4),acc,1)
                corner_brackets(frame,isx-rc-4,isy-rc-4,isx+rc+4,isy+rc+4,acc,6,1)
            else:
                cv2.circle(frame,(isx,isy),10,(60,70,80),1,cv2.LINE_AA)
                cv2.circle(frame,(isx,isy),3,(80,90,100),-1)

            # Skeleton
            for a,b in [(0,1),(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),
                        (13,14),(14,15),(15,16),(17,18),(18,19),(19,20),(0,5),(5,9),(9,13),(13,17),(0,17)]:
                cv2.line(frame,(int(lm[a].x*W),int(lm[a].y*H)),(int(lm[b].x*W),int(lm[b].y*H)),(0,100,140),1,cv2.LINE_AA)
            for i in range(21):
                cv2.circle(frame,(int(lm[i].x*W),int(lm[i].y*H)),3,(0,200,240),-1)
        else:
            sx,sy,px,py=0,0,0,0
            if mode!="IDLE": mode="IDLE"

        # Composite
        gray=cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
        _,mask=cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
        bg=cv2.bitwise_and(frame,frame,mask=cv2.bitwise_not(mask))
        b1=cv2.GaussianBlur(canvas,(9,9),0); b2=cv2.GaussianBlur(canvas,(21,21),0)
        cg=cv2.addWeighted(cv2.addWeighted(canvas,0.8,b1,0.3,0),1.0,b2,0.15,0)
        if hero()=="STRANGE":
            tint=np.zeros_like(cg); tint[:,:,1]=12; tint[:,:,2]=18; cg=cv2.add(cg,tint)
        display=cv2.add(bg,cg)
        particles.update_draw(display,dt)
        apply_scanlines(display)
        vig=np.zeros((H,W),dtype=np.uint8)
        cv2.ellipse(vig,(W//2,H//2),(W//2,H//2),0,0,360,255,-1)
        vig=cv2.GaussianBlur(vig,(201,201),0)
        display=np.clip(cv2.addWeighted(display,1.0,cv2.cvtColor(vig,cv2.COLOR_GRAY2BGR),-0.28,0),0,255).astype(np.uint8)

        draw_hud(display,col_idx,thick_idx,mode,len(undo_stack),show_help,fps_val,t,
                 hand_x,hand_y,W,H,voice_log,stroke_count,t,hero(),hero_idx,pal,acc)

        cv2.imshow("NEXUS AIR CANVAS",display)
        key=cv2.waitKey(1)&0xFF
        if key in (ord('q'),27): break
        elif key==ord('c'): push_undo(); canvas[:]=0; voice_log.log("Cleared.")
        elif key==ord('z'):
            if undo_stack: canvas=undo_stack.pop(); voice_log.log("Undo.")
        elif key==ord('s'):
            fname=f"nexus_{int(time.time())}.png"; cv2.imwrite(fname,display)
            voice_log.log("Saved!"); print(f"[SAVED] {fname}")
        elif key==ord('h'): show_help=not show_help
        elif key==ord('e'): mode="ERASE" if mode!="ERASE" else "DRAW"; voice_log.log(f"Mode:{mode}"); px,py=0,0
        elif key==ord('m'): hero_idx=(hero_idx+1)%len(HERO_MODES); col_idx=0; voice_log.log(f"HERO:{hero()}!")
        elif ord('1')<=key<=ord('8'):
            idx=key-ord('1')
            if idx<len(pal): col_idx=idx; voice_log.log(f"Color:{pal[col_idx][0]}")
        elif key in (ord('+'),ord('=')): thick_idx=min(thick_idx+1,len(BRUSH_SIZES)-1); voice_log.log(f"Size:{BRUSH_SIZES[thick_idx]}px")
        elif key==ord('-'): thick_idx=max(thick_idx-1,0); voice_log.log(f"Size:{BRUSH_SIZES[thick_idx]}px")

    cap.release(); cv2.destroyAllWindows(); detector.close()
    print("[NEXUS] Systems offline.")


if __name__ == "__main__":
    start_drawing()
