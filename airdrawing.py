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
J.A.R.V.I.S AIR CANVAS — STARK INDUSTRIES ULTRA PRO MAX v5.0
JARVIS Voice Assistant Compatible
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

# ═══════════════════════════════════════════
#  MODEL PATH
# ═══════════════════════════════════════════
# hand_landmarker.task same folder mein hona chahiye
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

# ═══════════════════════════════════════════
#  COLOR PALETTE (BGR)
# ═══════════════════════════════════════════
PALETTE = [
    ("ARC BLUE",  (255, 210,  60)),
    ("REPULSOR",  (255, 255,   0)),
    ("VIBRANIUM", (255, 120,  60)),
    ("HULK",      (  0, 220,  60)),
    ("PLASMA",    (  0,  60, 255)),
    ("NOVA",      (180,   0, 255)),
    ("SOLAR",     (  0, 200, 255)),
    ("GHOST",     (220, 220, 220)),
    ("OBSIDIAN",  ( 80,  80, 100)),
]
COLOR_NAMES  = [p[0] for p in PALETTE]
COLOR_VALUES = [p[1] for p in PALETTE]

BRUSH_SIZES = [2, 5, 9, 15, 22, 32]
ERASER_R    = 40
TOOLBAR_H   = 100
HUD_ACCENT  = (0, 210, 255)


# ═══════════════════════════════════════════
#  PARTICLE SYSTEM
# ═══════════════════════════════════════════
class Particle:
    __slots__ = ['x','y','vx','vy','life','color','size']
    def __init__(self, x, y, color):
        angle     = random.uniform(0, 2*math.pi)
        speed     = random.uniform(0.5, 3.0)
        self.x    = float(x)
        self.y    = float(y)
        self.vx   = math.cos(angle)*speed
        self.vy   = math.sin(angle)*speed
        self.life = random.uniform(0.4, 1.0)
        self.color= color
        self.size = random.randint(1, 3)

    def update(self, dt):
        self.x   += self.vx
        self.y   += self.vy
        self.vy  += 0.04
        self.life -= dt * 1.6

    def draw(self, img):
        if self.life <= 0:
            return
        a     = min(1.0, self.life)
        faded = (int(self.color[0]*a), int(self.color[1]*a), int(self.color[2]*a))
        ix, iy = int(self.x), int(self.y)
        if 0 <= ix < img.shape[1] and 0 <= iy < img.shape[0]:
            cv2.circle(img, (ix, iy), self.size, faded, -1)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, color, n=4):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def update_draw(self, img, dt):
        alive = []
        for p in self.particles:
            p.update(dt)
            if p.life > 0:
                p.draw(img)
                alive.append(p)
        self.particles = alive


# ═══════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════
def dist2d(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def fingers_up(lm):
    tips = [4, 8, 12, 16, 20]
    pip  = [3, 6, 10, 14, 18]
    up   = [lm[4].x < lm[3].x]
    for i in range(1, 5):
        up.append(lm[tips[i]].y < lm[pip[i]].y)
    return up


def neon_line(canvas, p1, p2, color, thick):
    if p1 == (0,0) or p2 == (0,0):
        return
    glow_lay = np.zeros_like(canvas)
    cv2.line(glow_lay, p1, p2, color, thick+18, cv2.LINE_AA)
    glow = cv2.GaussianBlur(glow_lay, (25,25), 0)
    cv2.addWeighted(canvas, 1.0, glow, 0.5, 0, canvas)
    cv2.line(canvas, p1, p2, color, thick+6, cv2.LINE_AA)
    bright = tuple(min(255, int(c*1.8)) for c in color)
    cv2.line(canvas, p1, p2, bright, max(1, thick-1), cv2.LINE_AA)
    cv2.line(canvas, p1, p2, (255,255,255), max(1, thick-3), cv2.LINE_AA)


def apply_scanlines(img, skip=4, alpha=0.06):
    scan = img.copy()
    for y in range(0, img.shape[0], skip):
        scan[y] = (scan[y] * 0.3).astype(np.uint8)
    cv2.addWeighted(img, 1-alpha, scan, alpha, 0, img)


def glass_rect(img, x1, y1, x2, y2, bg=(8,12,22), alpha=0.80, border=None):
    ov = img.copy()
    cv2.rectangle(ov, (x1,y1), (x2,y2), bg, -1)
    cv2.addWeighted(ov, alpha, img, 1-alpha, 0, img)
    if border:
        cv2.rectangle(img, (x1,y1), (x2,y2), border, 1)


def corner_brackets(img, x1, y1, x2, y2, color, length=18, thick=2):
    for corner in [
        ((x1,y1),(x1+length,y1),(x1,y1+length)),
        ((x2,y1),(x2-length,y1),(x2,y1+length)),
        ((x1,y2),(x1+length,y2),(x1,y2-length)),
        ((x2,y2),(x2-length,y2),(x2,y2-length)),
    ]:
        cv2.line(img, corner[0], corner[1], color, thick, cv2.LINE_AA)
        cv2.line(img, corner[0], corner[2], color, thick, cv2.LINE_AA)


def text_c(img, txt, cx, cy, scale, color, thick=1):
    (tw,th),_ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, scale, thick)
    cv2.putText(img, txt, (cx-tw//2, cy+th//2),
                cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)


def glow_circle(img, cx, cy, r, color, thick=2):
    lay  = np.zeros_like(img)
    cv2.circle(lay, (cx,cy), r, color, thick)
    blur = cv2.GaussianBlur(lay, (15,15), 0)
    cv2.addWeighted(img, 1.0, blur, 0.8, 0, img)
    cv2.circle(img, (cx,cy), r, color, thick, cv2.LINE_AA)


def pulse_ring(img, cx, cy, t, color, base_r=30):
    r       = base_r + int(8*math.sin(t*3.0))
    alpha_f = 0.5 + 0.5*math.sin(t*3.0)
    lay     = np.zeros_like(img)
    cv2.circle(lay, (cx,cy), r, color, 2)
    blur    = cv2.GaussianBlur(lay, (11,11), 0)
    cv2.addWeighted(img, 1.0, blur, alpha_f*0.6, 0, img)
    cv2.circle(img, (cx,cy), r, color, 1, cv2.LINE_AA)


# ═══════════════════════════════════════════
#  VOICE LOG
# ═══════════════════════════════════════════
class VoiceLog:
    def __init__(self, maxlines=7):
        self.lines = collections.deque(maxlen=maxlines)
        self.ts    = collections.deque(maxlen=maxlines)

    def log(self, msg):
        self.lines.append(msg)
        self.ts.append(time.time())

    def draw(self, img, x, y, w):
        now = time.time()
        glass_rect(img, x, y, x+w, y+len(self.lines)*20+18, (5,8,15), 0.80, HUD_ACCENT)
        cv2.putText(img, "JARVIS LOG", (x+8, y+13),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, HUD_ACCENT, 1, cv2.LINE_AA)
        for i, (ln, ts) in enumerate(zip(self.lines, self.ts)):
            age  = now - ts
            a    = max(0.0, 1.0 - age/8.0)
            clr  = (int(0*a), int(200*a), int(255*a))
            cv2.putText(img, f"> {ln}", (x+8, y+28+i*18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.30, clr, 1, cv2.LINE_AA)


# ═══════════════════════════════════════════
#  RADAR
# ═══════════════════════════════════════════
def draw_radar(img, cx, cy, r, t, hx, hy, W, H):
    lay = np.zeros_like(img)
    cv2.circle(lay, (cx,cy), r, (0,60,20), -1)
    cv2.addWeighted(img, 1.0, lay, 0.55, 0, img)
    for ri in [r//4, r//2, 3*r//4, r]:
        cv2.circle(img, (cx,cy), ri, (0,100,40), 1, cv2.LINE_AA)
    cv2.line(img, (cx-r,cy), (cx+r,cy), (0,100,40), 1)
    cv2.line(img, (cx,cy-r), (cx,cy+r), (0,100,40), 1)
    sweep = (t*120) % 360
    ex = cx + int(r*math.cos(math.radians(sweep)))
    ey = cy + int(r*math.sin(math.radians(sweep)))
    lay2 = np.zeros_like(img)
    cv2.line(lay2, (cx,cy), (ex,ey), (0,255,80), 2)
    cv2.addWeighted(img, 1.0, cv2.GaussianBlur(lay2,(9,9),0), 0.6, 0, img)
    cv2.line(img, (cx,cy), (ex,ey), (0,255,80), 1, cv2.LINE_AA)
    if hx > 0 and hy > 0:
        bx = max(cx-r, min(cx+r, cx+int((hx/W-0.5)*r*2)))
        by = max(cy-r, min(cy+r, cy+int((hy/H-0.5)*r*2)))
        glow_circle(img, bx, by, 5, (0,255,100), 2)
    cv2.circle(img, (cx,cy), r, HUD_ACCENT, 2, cv2.LINE_AA)
    text_c(img, "TRACK", cx, cy+r+10, 0.28, HUD_ACCENT)


def draw_power_bar(img, x, y, w, h, val, label, color):
    glass_rect(img, x, y, x+w, y+h, (5,5,15), 0.8, HUD_ACCENT)
    if int(w*val) > 0:
        lay = np.zeros_like(img)
        cv2.rectangle(lay, (x,y), (x+int(w*val), y+h), color, -1)
        cv2.addWeighted(img, 1.0, lay, 0.7, 0, img)
    cv2.putText(img, f"{label}: {int(val*100)}%", (x+4, y+h-4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.28, (200,220,255), 1, cv2.LINE_AA)


# ═══════════════════════════════════════════
#  HUD
# ═══════════════════════════════════════════
def draw_hud(frame, col_idx, thick_idx, mode, undo_count,
             show_help, fps, t, hand_x, hand_y, W, H,
             voice_log, stroke_count, session_secs):

    SW, SH, SPAD, sw_x0 = 54, 72, 5, 290

    # Toolbar bg
    glass_rect(frame, 0, 0, W, TOOLBAR_H, (5,8,18), 0.88, HUD_ACCENT)
    ba = 0.5 + 0.5*math.sin(t*2.0)
    lay = np.zeros_like(frame)
    cv2.line(lay, (0,TOOLBAR_H), (W,TOOLBAR_H), HUD_ACCENT, 2)
    cv2.addWeighted(frame, 1.0, cv2.GaussianBlur(lay,(7,7),0), ba, 0, frame)
    cv2.line(frame, (0,TOOLBAR_H), (W,TOOLBAR_H), HUD_ACCENT, 1, cv2.LINE_AA)

    # Title
    cv2.putText(frame, "STARK INDUSTRIES", (10,22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, HUD_ACCENT, 1, cv2.LINE_AA)
    cv2.putText(frame, "J.A.R.V.I.S  AIR CANVAS  ULTRA v5.0",
                (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "MARK VII  |  AUTHORIZED USER",
                (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0,140,160), 1, cv2.LINE_AA)

    # Arc reactor
    pulse_ring(frame, 262, 50, t, (0,200,255), 22)
    cv2.circle(frame, (262,50), 12, (0,180,255), -1)
    cv2.circle(frame, (262,50), 6,  (200,240,255), -1)

    # Color swatches
    for i,(name,val) in enumerate(PALETTE):
        x1 = sw_x0 + i*(SW+SPAD)
        x2, y1, y2 = x1+SW, 6, 6+SH
        cv2.rectangle(frame, (x1,y1), (x2,y2), val, -1)
        ref = np.zeros_like(frame)
        cv2.rectangle(ref, (x1,y1), (x2,y1+18), (255,255,255), -1)
        cv2.addWeighted(frame, 1.0, ref, 0.08, 0, frame)
        if i == col_idx:
            for bw,ba2 in [(8,0.3),(4,0.6),(1,1.0)]:
                bl = np.zeros_like(frame)
                cv2.rectangle(bl,(x1-bw,y1-bw),(x2+bw,y2+bw),(0,255,255),2)
                cv2.addWeighted(frame,1.0,cv2.GaussianBlur(bl,(11,11),0),ba2*0.5,0,frame)
            cv2.rectangle(frame,(x1-2,y1-2),(x2+2,y2+2),(0,255,255),2)
            pts = np.array([[x1+SW//2-5,y2+2],[x1+SW//2+5,y2+2],[x1+SW//2,y2+9]])
            cv2.fillPoly(frame,[pts],(0,255,255))
        else:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(40,50,65),1)
        text_c(frame, name[:4], (x1+x2)//2, (y1+y2)//2, 0.26, (0,0,0), 1)

    # Brush sizes
    tx0 = sw_x0 + len(PALETTE)*(SW+SPAD) + 20
    for i,sz in enumerate(BRUSH_SIZES):
        cx2 = tx0 + i*52 + 26
        cy2 = TOOLBAR_H//2
        r   = sz//2 + 5
        if i == thick_idx:
            pulse_ring(frame, cx2, cy2, t, (0,255,255), r+6)
            cv2.circle(frame,(cx2,cy2),r,COLOR_VALUES[col_idx],-1)
            cv2.circle(frame,(cx2,cy2),r,(0,255,255),1,cv2.LINE_AA)
        else:
            cv2.circle(frame,(cx2,cy2),r,(40,45,60),-1)
            cv2.circle(frame,(cx2,cy2),r,(80,90,110),1,cv2.LINE_AA)

    # Right panel
    rpx, rpy = W-200, 6
    glass_rect(frame, rpx-5, rpy, W-2, TOOLBAR_H-4, (8,10,20), 0.85, HUD_ACCENT)
    corner_brackets(frame, rpx-5, rpy, W-2, TOOLBAR_H-4, HUD_ACCENT, 10)
    mc = {"DRAW":(0,255,120),"ERASE":(0,60,255),"IDLE":(80,100,120)}.get(mode,(200,200,200))
    cv2.putText(frame, f"MODE: {mode}",           (rpx,rpy+18), cv2.FONT_HERSHEY_SIMPLEX, 0.48, mc, 2, cv2.LINE_AA)
    cv2.putText(frame, f"FPS  {fps:05.1f}",       (rpx,rpy+38), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,180,200), 1, cv2.LINE_AA)
    cv2.putText(frame, f"UNDO {undo_count:03d}",  (rpx,rpy+54), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,180,200), 1, cv2.LINE_AA)
    cv2.putText(frame, f"STRK {stroke_count:04d}",(rpx,rpy+70), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,180,200), 1, cv2.LINE_AA)
    cv2.putText(frame, f"TIME {int(session_secs)//60:02d}:{int(session_secs)%60:02d}",
                (rpx,rpy+86), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,180,200), 1, cv2.LINE_AA)

    # Radar + power bars
    rcx, rcy, rr = 75, H-95, 60
    draw_radar(frame, rcx, rcy, rr, t, hand_x, hand_y, W, H)
    pbx, pby = rcx+rr+18, H-145
    draw_power_bar(frame, pbx, pby,    120, 16, 0.72+0.05*math.sin(t*1.3), "ARC  ", (0,210,255))
    draw_power_bar(frame, pbx, pby+22, 120, 16, 0.88,                       "SUIT ", (0,180,200))
    draw_power_bar(frame, pbx, pby+44, 120, 16, min(1.0,fps/60),            "PROC ", (0,255,120))
    voice_log.draw(frame, pbx+130, pby-10, 240)

    # Bottom bar
    glass_rect(frame, 0, H-26, W, H, (5,8,18), 0.82, (0,70,100))
    cv2.putText(frame,
        f"  COLOR:{COLOR_NAMES[col_idx]}  SIZE:{BRUSH_SIZES[thick_idx]}px  "
        f"[1-9]Color  [+/-]Size  [E]Erase  [Z]Undo  [C]Clear  [S]Save  [H]Help  [Q]Quit",
        (8,H-8), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0,160,190), 1, cv2.LINE_AA)

    # Help overlay
    if show_help:
        lines = [
            ("STARK HUD  --  GESTURE CONTROL", (0,255,255)),
            ("--------------------------------",(0,100,120)),
            ("1 Finger   ->  DRAW",   (0,220,180)),
            ("2 Fingers  ->  ERASE",  (0,220,180)),
            ("3 Fingers  ->  CLEAR",  (0,220,180)),
            ("Fist       ->  PAUSE",  (0,220,180)),
            ("Pinch      ->  COLOR",  (0,220,180)),
            ("Thumb UP   ->  BIGGER", (0,220,180)),
            ("Pinky UP   ->  SMALLER",(0,220,180)),
            ("--------------------------------",(0,100,120)),
            ("KEYBOARD",              (0,255,255)),
            ("1-9 Color  +/- Size",   (0,200,220)),
            ("Z Undo     E Erase",    (0,200,220)),
            ("C Clear    S Save",     (0,200,220)),
            ("H Help     Q Quit",     (0,200,220)),
        ]
        hx, hy0 = W-275, TOOLBAR_H+15
        bh = len(lines)*20+18
        glass_rect(frame, hx-10, hy0-10, hx+270, hy0+bh, (5,8,18), 0.88, HUD_ACCENT)
        corner_brackets(frame, hx-10, hy0-10, hx+270, hy0+bh, HUD_ACCENT, 14)
        for j,(ln,clr) in enumerate(lines):
            cv2.putText(frame, ln, (hx, hy0+j*20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.34, clr, 1, cv2.LINE_AA)


# ═══════════════════════════════════════════════════════════
#  START_DRAWING  ← JARVIS IS FUNCTION KO CALL KARTA HAI
# ═══════════════════════════════════════════════════════════
def start_drawing():
    """JARVIS voice assistant se call hoti hai yeh function."""

    print("[JARVIS] Air Canvas loading...")

    # Model check
    if not os.path.exists(MODEL_PATH):
        print(f"[JARVIS] ERROR: hand_landmarker.task nahi mili!")
        print(f"[JARVIS] Yahan download karo:")
        print("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        print(f"[JARVIS] Aur is folder mein rakho: {os.path.dirname(MODEL_PATH)}")
        return

    # MediaPipe
    base_opt = python.BaseOptions(model_asset_path=MODEL_PATH)
    options  = vision.HandLandmarkerOptions(
        base_options=base_opt,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.5,
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    ret, f0 = cap.read()
    if not ret:
        print("[JARVIS] Camera nahi mili!")
        cap.release()
        detector.close()
        return

    H, W = f0.shape[:2]

    # State variables
    canvas       = np.zeros((H, W, 3), dtype=np.uint8)
    undo_stack   = collections.deque(maxlen=30)
    col_idx      = 0
    thick_idx    = 1
    mode         = "IDLE"
    show_help    = True
    sx, sy       = 0, 0
    px, py       = 0, 0
    ALPHA        = 0.55
    gesture_ts   = 0.0
    G_COOL       = 0.5
    fps_ts       = time.time()
    fps_val      = 30.0
    frame_cnt    = 0
    session_start= time.time()
    stroke_count = 0
    last_t       = time.time()

    particles  = ParticleSystem()
    voice_log  = VoiceLog(7)
    voice_log.log("JARVIS ONLINE. Good day, sir.")
    voice_log.log("Hand tracking: READY")
    voice_log.log("Arc Reactor: NOMINAL")
    voice_log.log("Air Canvas: ACTIVE")

    SW, SH, SPAD, sw_x0 = 54, 72, 5, 290

    def push_undo():
        undo_stack.append(canvas.copy())

    cv2.namedWindow("JARVIS AIR CANVAS", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("JARVIS AIR CANVAS", W, H)

    print("[JARVIS] All systems go. Starting...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        H, W  = frame.shape[:2]

        now    = time.time()
        dt     = max(0.001, now - last_t)
        last_t = now
        t      = now - session_start

        frame_cnt += 1
        if now - fps_ts >= 1.0:
            fps_val   = frame_cnt / (now - fps_ts)
            frame_cnt = 0
            fps_ts    = now

        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_img)

        hand_x, hand_y = 0, 0

        if result.hand_landmarks:
            lm = result.hand_landmarks[0]
            rx = int(lm[8].x * W)
            ry = int(lm[8].y * H)
            hand_x, hand_y = rx, ry

            sx = int(ALPHA*rx + (1-ALPHA)*sx) if sx else rx
            sy = int(ALPHA*ry + (1-ALPHA)*sy) if sy else ry

            fu = fingers_up(lm)
            thumb, index, middle, ring, pinky = fu
            tx_px = int(lm[4].x*W)
            ty_px = int(lm[4].y*H)
            ix_px = int(lm[8].x*W)
            iy_px = int(lm[8].y*H)

            # FIST → IDLE
            if not index and not middle and not ring and not pinky:
                if mode != "IDLE":
                    voice_log.log("Pause mode.")
                mode   = "IDLE"
                px, py = 0, 0

            # 3 FINGERS → CLEAR
            elif index and middle and ring and (now - gesture_ts > G_COOL):
                push_undo(); canvas[:] = 0
                mode = "DRAW"; px, py = 0, 0
                gesture_ts = now
                voice_log.log("Canvas cleared.")

            # 2 FINGERS → ERASE
            elif index and middle and not ring:
                if mode != "ERASE":
                    voice_log.log("Eraser engaged.")
                mode = "ERASE"
                if sy > TOOLBAR_H:
                    if (px,py) == (0,0):
                        push_undo()
                    cv2.circle(canvas,(sx,sy),ERASER_R,(0,0,0),-1)
                    particles.spawn(sx, sy, (80,80,100), 3)
                px, py = 0, 0

            # THUMB PINCH → NEXT COLOR
            elif thumb and not middle and not ring and not pinky:
                d = dist2d((tx_px,ty_px),(ix_px,iy_px))
                if d < 45 and (now - gesture_ts > G_COOL):
                    col_idx = (col_idx+1) % len(PALETTE)
                    gesture_ts = now
                    voice_log.log(f"Color: {COLOR_NAMES[col_idx]}")
                mode = "DRAW"; px, py = 0, 0

            # THUMB ONLY → BIGGER
            elif thumb and not index and not middle and not ring:
                if now - gesture_ts > G_COOL:
                    thick_idx = min(thick_idx+1, len(BRUSH_SIZES)-1)
                    gesture_ts = now
                    voice_log.log(f"Brush: {BRUSH_SIZES[thick_idx]}px")
                mode = "DRAW"; px, py = 0, 0

            # PINKY → SMALLER
            elif pinky and not index and not middle and not ring:
                if now - gesture_ts > G_COOL:
                    thick_idx = max(thick_idx-1, 0)
                    gesture_ts = now
                    voice_log.log(f"Brush: {BRUSH_SIZES[thick_idx]}px")
                mode = "DRAW"; px, py = 0, 0

            # INDEX → DRAW / TOOLBAR
            elif index and not middle:
                if sy < TOOLBAR_H:
                    mode = "DRAW"
                    for i in range(len(PALETTE)):
                        x1c = sw_x0 + i*(SW+SPAD)
                        if x1c < sx < x1c+SW and (now-gesture_ts > G_COOL):
                            col_idx = i; gesture_ts = now
                            voice_log.log(f"Color: {COLOR_NAMES[i]}")
                            break
                    tx0c = sw_x0 + len(PALETTE)*(SW+SPAD) + 20
                    for i in range(len(BRUSH_SIZES)):
                        cxc = tx0c + i*52 + 26
                        if abs(sx-cxc) < 26 and (now-gesture_ts > G_COOL):
                            thick_idx = i; gesture_ts = now
                            voice_log.log(f"Brush: {BRUSH_SIZES[i]}px")
                            break
                    px, py = 0, 0
                else:
                    if mode != "DRAW":
                        voice_log.log("Draw mode active.")
                    mode = "DRAW"
                    if px == 0 and py == 0:
                        px, py = sx, sy
                        push_undo()
                        stroke_count += 1
                    else:
                        neon_line(canvas,(px,py),(sx,sy),
                                  COLOR_VALUES[col_idx], BRUSH_SIZES[thick_idx])
                        if dist2d((sx,sy),(px,py)) > 8:
                            particles.spawn(sx, sy, COLOR_VALUES[col_idx], 2)
                        px, py = sx, sy
            else:
                px, py = 0, 0

            # Cursor
            if mode == "ERASE":
                glow_circle(frame,(sx,sy),ERASER_R,(0,60,255),2)
                cv2.circle(frame,(sx,sy),5,(0,60,255),-1)
                for ang in range(0,360,20):
                    ex2=sx+int(ERASER_R*math.cos(math.radians(ang)))
                    ey2=sy+int(ERASER_R*math.sin(math.radians(ang)))
                    cv2.circle(frame,(ex2,ey2),1,(0,100,200),-1)
            elif mode == "DRAW":
                rc = BRUSH_SIZES[thick_idx]//2+6
                glow_circle(frame,(sx,sy),rc,COLOR_VALUES[col_idx],2)
                cv2.circle(frame,(sx,sy),3,COLOR_VALUES[col_idx],-1)
                cv2.line(frame,(sx-rc-4,sy),(sx-rc+2,sy),HUD_ACCENT,1)
                cv2.line(frame,(sx+rc-2,sy),(sx+rc+4,sy),HUD_ACCENT,1)
                cv2.line(frame,(sx,sy-rc-4),(sx,sy-rc+2),HUD_ACCENT,1)
                cv2.line(frame,(sx,sy+rc-2),(sx,sy+rc+4),HUD_ACCENT,1)
                corner_brackets(frame,sx-rc-4,sy-rc-4,sx+rc+4,sy+rc+4,HUD_ACCENT,6,1)
            else:
                cv2.circle(frame,(sx,sy),10,(60,70,80),1,cv2.LINE_AA)
                cv2.circle(frame,(sx,sy),3,(80,90,100),-1)

            # Hand skeleton
            for a,b in [(0,1),(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),
                        (9,10),(10,11),(11,12),(13,14),(14,15),(15,16),
                        (17,18),(18,19),(19,20),(0,5),(5,9),(9,13),(13,17),(0,17)]:
                cv2.line(frame,
                         (int(lm[a].x*W),int(lm[a].y*H)),
                         (int(lm[b].x*W),int(lm[b].y*H)),
                         (0,110,150),1,cv2.LINE_AA)
            for i in range(21):
                lx,ly=int(lm[i].x*W),int(lm[i].y*H)
                cv2.circle(frame,(lx,ly),3,(0,210,250),-1)
                cv2.circle(frame,(lx,ly),3,(0,100,130),1)
        else:
            sx,sy,px,py = 0,0,0,0
            if mode != "IDLE":
                mode = "IDLE"

        # Composite
        gray     = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _,mask   = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        bg       = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        b1       = cv2.GaussianBlur(canvas,(9,9),0)
        b2       = cv2.GaussianBlur(canvas,(21,21),0)
        cg       = cv2.addWeighted(cv2.addWeighted(canvas,0.8,b1,0.3,0),1.0,b2,0.15,0)
        display  = cv2.add(bg, cg)

        particles.update_draw(display, dt)
        apply_scanlines(display)

        # Vignette
        vig = np.zeros((H,W), dtype=np.uint8)
        cv2.ellipse(vig,(W//2,H//2),(W//2,H//2),0,0,360,255,-1)
        vig = cv2.GaussianBlur(vig,(201,201),0)
        display = np.clip(
            cv2.addWeighted(display,1.0,cv2.cvtColor(vig,cv2.COLOR_GRAY2BGR),-0.25,0),
            0,255).astype(np.uint8)

        draw_hud(display,col_idx,thick_idx,mode,len(undo_stack),
                 show_help,fps_val,t,hand_x,hand_y,W,H,voice_log,stroke_count,t)

        cv2.imshow("JARVIS AIR CANVAS", display)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 27):
            break
        elif key == ord('c'):
            push_undo(); canvas[:]=0; voice_log.log("Cleared.")
        elif key == ord('z'):
            if undo_stack:
                canvas = undo_stack.pop(); voice_log.log("Undo.")
        elif key == ord('s'):
            fname = f"stark_art_{int(time.time())}.png"
            cv2.imwrite(fname, display)
            print(f"[SAVED] {fname}"); voice_log.log(f"Saved!")
        elif key == ord('h'):
            show_help = not show_help
        elif key == ord('e'):
            mode = "ERASE" if mode!="ERASE" else "DRAW"
            voice_log.log(f"Mode: {mode}"); px,py=0,0
        elif ord('1') <= key <= ord('9'):
            idx = key-ord('1')
            if idx < len(PALETTE):
                col_idx = idx; voice_log.log(f"Color: {COLOR_NAMES[col_idx]}")
        elif key in (ord('+'),ord('=')):
            thick_idx=min(thick_idx+1,len(BRUSH_SIZES)-1)
            voice_log.log(f"Brush: {BRUSH_SIZES[thick_idx]}px")
        elif key == ord('-'):
            thick_idx=max(thick_idx-1,0)
            voice_log.log(f"Brush: {BRUSH_SIZES[thick_idx]}px")
        elif key == ord(']'):
            col_idx=(col_idx+1)%len(PALETTE)
        elif key == ord('['):
            col_idx=(col_idx-1)%len(PALETTE)

    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    print("[JARVIS] Air Canvas closed.")


# Directly chalane ke liye
if __name__ == "__main__":
    start_drawing()