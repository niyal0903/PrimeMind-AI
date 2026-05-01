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
╔══════════════════════════════════════════════════════════════╗
║        J.A.R.V.I.S  AIR  CANVAS — AVENGERS EDITION v4.0      ║
║   Arc Reactor HUD · Shield Eraser · Shape Detect · VFX       ║
╚══════════════════════════════════════════════════════════════╝
"""

import cv2
import mediapipe as mp
import numpy as np
import collections
import time
import math
import random
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ═══════════════════════════════════════════
#  COLOR PALETTE  (BGR)
# ═══════════════════════════════════════════
PALETTE = [
    ("CYAN",    (255, 230,   0)),
    ("MAGENTA", (255,   0, 255)),
    ("BLUE",    (255,  80,  30)),
    ("GREEN",   (  0, 255, 120)),
    ("YELLOW",  (  0, 220, 255)),
    ("RED",     (  0,  30, 255)),
    ("WHITE",   (255, 255, 255)),
    ("ORANGE",  (  0, 140, 255)),
]
COLOR_NAMES  = [p[0] for p in PALETTE]
COLOR_VALUES = [p[1] for p in PALETTE]

BRUSH_SIZES  = [3, 6, 10, 16, 24]
ERASER_R     = 35
TOOLBAR_H    = 90

# ═══════════════════════════════════════════
#  AVENGERS VFX STATE & MEMORY
# ═══════════════════════════════════════════
particles = collections.deque(maxlen=60)
explosions = []
current_stroke = []  # For shape detection
brush_styles = ["NEON", "PLASMA", "GALAXY"]
current_brush_style = 0
jarvis_lines = [
    "J.A.R.V.I.S: Mark LXXXV armor deployed.",
    "J.A.R.V.I.S: Scanning visual canvas...",
    "J.A.R.V.I.S: Trajectory calculated.",
    "J.A.R.V.I.S: Sir, I detect a new shape.",
    "J.A.R.V.I.S: Awaiting your command, Sir.",
    "J.A.R.V.I.S: Thermal signatures nominal."
]
active_jarvis_msg = jarvis_lines[0]
msg_timer = time.time()

# ═══════════════════════════════════════════
#  MATH & GESTURE HELPERS
# ═══════════════════════════════════════════
def dist2d(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def fingers_up(lm):
    """[thumb, index, middle, ring, pinky]"""
    tips = [4, 8, 12, 16, 20]
    pip  = [3, 6, 10, 14, 18]
    up   = []
    up.append(lm[4].x < lm[3].x)          # thumb: x-axis
    for i in range(1, 5):
        up.append(lm[tips[i]].y < lm[pip[i]].y)
    return up

# ═══════════════════════════════════════════
#  VFX & DRAWING SYSTEMS
# ═══════════════════════════════════════════
def neon_line(canvas, p1, p2, color, thick, style="NEON"):
    if p1 == (0,0) or p2 == (0,0):
        return
    
    if style == "NEON":
        # Outer glow layer
        blur_lay = np.zeros_like(canvas)
        cv2.line(blur_lay, p1, p2, color, thick + 12, cv2.LINE_AA)
        glow = cv2.GaussianBlur(blur_lay, (21, 21), 0)
        cv2.addWeighted(canvas, 1.0, glow, 0.55, 0, canvas)
        # Mid layer
        cv2.line(canvas, p1, p2, color, thick + 3, cv2.LINE_AA)
        # White hot core
        white = tuple(min(255, int(c*1.6)) for c in color)
        cv2.line(canvas, p1, p2, white, max(1, thick - 2), cv2.LINE_AA)
        
    elif style == "PLASMA":
        cv2.line(canvas, p1, p2, color, thick, cv2.LINE_AA)
        for _ in range(5):
            ox = random.randint(-thick, thick)
            oy = random.randint(-thick, thick)
            white = tuple(min(255, int(c*1.8)) for c in color)
            cv2.circle(canvas, (p2[0]+ox, p2[1]+oy), random.randint(1, thick//2+1), white, -1)

    elif style == "GALAXY":
        cv2.line(canvas, p1, p2, color, thick//2, cv2.LINE_AA)
        for _ in range(8):
            ox = random.randint(-thick*2, thick*2)
            oy = random.randint(-thick*2, thick*2)
            cv2.circle(canvas, (p2[0]+ox, p2[1]+oy), random.randint(1, 3), color, -1)

def draw_shield(img, cx, cy, r):
    # Captain America Shield (Red, White, Red, Blue, Star)
    cv2.circle(img, (cx, cy), r, (0, 0, 200), -1)      # Outer Red
    cv2.circle(img, (cx, cy), int(r*0.8), (220, 220, 220), -1) # White
    cv2.circle(img, (cx, cy), int(r*0.6), (0, 0, 200), -1)     # Inner Red
    cv2.circle(img, (cx, cy), int(r*0.4), (200, 0, 0), -1)     # Center Blue
    # Simple Star
    pts = []
    for i in range(5):
        angle = i * (4 * math.pi / 5) - math.pi/2
        px = cx + int(r*0.35 * math.cos(angle))
        py = cy + int(r*0.35 * math.sin(angle))
        pts.append((px, py))
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], (255, 255, 255))

def add_explosion(x, y, color):
    explosions.append({'x': x, 'y': y, 'radius': 10, 'color': color, 'life': 255})

def draw_explosions(img):
    for exp in explosions[:]:
        cv2.circle(img, (exp['x'], exp['y']), int(exp['radius']), exp['color'], 4)
        exp['radius'] += 8
        exp['life'] -= 15
        if exp['life'] <= 0:
            explosions.remove(exp)

def draw_arc_reactor_hud(img):
    h, w = img.shape[:2]
    cx, cy = w - 80, 150
    t = time.time()
    color = (255, 230, 0) # Cyan-ish
    
    # Rotating outer triangles
    for i in range(3):
        angle = t * 2 + i * (2*math.pi/3)
        px = cx + int(40 * math.cos(angle))
        py = cy + int(40 * math.sin(angle))
        cv2.circle(img, (px, py), 3, color, -1)
        cv2.line(img, (cx, cy), (px, py), color, 1)

    cv2.circle(img, (cx, cy), 35, color, 1, cv2.LINE_AA)
    cv2.circle(img, (cx, cy), 25, color, 2, cv2.LINE_AA)
    cv2.circle(img, (cx, cy), 10, (255, 255, 255), -1, cv2.LINE_AA)

def draw_audio_visualizer(img):
    h, w = img.shape[:2]
    t = time.time() * 5
    for i in range(15):
        height = int(20 + 15 * math.sin(t + i))
        cv2.line(img, (w - 180 + i*10, h - 30), (w - 180 + i*10, h - 30 - height), (0, 220, 255), 2)

def draw_scanlines(img):
    h, w = img.shape[:2]
    scan_y = int((time.time() * 200) % h)
    overlay = img.copy()
    cv2.line(overlay, (0, scan_y), (w, scan_y), (0, 255, 100), 2)
    cv2.line(overlay, (0, scan_y-10), (w, scan_y-10), (0, 255, 100), 1)
    cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

# ═══════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════
def glass_rect(img, x1, y1, x2, y2, bg=(20,20,30), alpha=0.72, border=None):
    ov = img.copy()
    cv2.rectangle(ov, (x1,y1), (x2,y2), bg, -1)
    cv2.addWeighted(ov, alpha, img, 1-alpha, 0, img)
    if border:
        cv2.rectangle(img, (x1,y1), (x2,y2), border, 1)

def text_c(img, txt, cx, cy, scale, color, thick=1):
    (tw,th),_ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, scale, thick)
    cv2.putText(img, txt, (cx-tw//2, cy+th//2),
                cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)

def glow_circle(img, cx, cy, r, color, thick=2):
    lay = np.zeros_like(img)
    cv2.circle(lay, (cx,cy), r, color, thick)
    blur = cv2.GaussianBlur(lay, (15,15), 0)
    cv2.addWeighted(img, 1.0, blur, 0.7, 0, img)
    cv2.circle(img, (cx,cy), r, color, thick, cv2.LINE_AA)

# ═══════════════════════════════════════════
#  TOOLBAR LAYOUT
# ═══════════════════════════════════════════
SW   = 58   # swatch width
SH   = 70   # swatch height
SPAD = 6    # swatch padding
SX0  = 10   # start x

def swatch_rect(i):
    x1 = SX0 + i*(SW+SPAD)
    return x1, 8, x1+SW, 8+SH

def thick_rect(i, tx0):
    x1 = tx0 + i*(44+5)
    return x1, 12, x1+44, 12+60

# ═══════════════════════════════════════════
#  DRAW UI
# ═══════════════════════════════════════════
def draw_ui(frame, col_idx, thick_idx, mode, undo_count, show_help, fps):
    h, w = frame.shape[:2]

    # Toolbar background
    glass_rect(frame, 0, 0, w, TOOLBAR_H, (10,12,20), 0.82, (0,180,220))

    # Title
    cv2.putText(frame, "J.A.R.V.I.S  AIR  CANVAS",
                (SX0, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0,220,255), 2, cv2.LINE_AA)
    cv2.putText(frame, "AVENGERS EDITION v4.0",
                (SX0, 52), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0,140,255), 1, cv2.LINE_AA)
    
    # Display Active Brush Style
    cv2.putText(frame, f"BRUSH: {brush_styles[current_brush_style]}",
                (SX0, 75), cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (0,255,100), 1, cv2.LINE_AA)

    # Color swatches — start after title
    sw_x0 = 290
    for i,(name,val) in enumerate(PALETTE):
        x1,y1,x2,y2 = swatch_rect(i)
        x1 += sw_x0; x2 += sw_x0
        sel = (i == col_idx)
        # Swatch fill
        cv2.rectangle(frame, (x1,y1), (x2,y2), val, -1)
        # Border
        if sel:
            lay = np.zeros_like(frame)
            cv2.rectangle(lay, (x1-3,y1-3),(x2+3,y2+3),(0,255,255),2)
            blur= cv2.GaussianBlur(lay,(11,11),0)
            cv2.addWeighted(frame,1.0,blur,0.8,0,frame)
            cv2.rectangle(frame,(x1-3,y1-3),(x2+3,y2+3),(0,255,255),2)
        else:
            cv2.rectangle(frame,(x1,y1),(x2,y2),(50,50,60),1)
        text_c(frame, name[:3], (x1+x2)//2, (y1+y2)//2, 0.3, (0,0,0), 1)

    # Thickness buttons
    tx0 = sw_x0 + len(PALETTE)*(SW+SPAD) + 18
    for i,sz in enumerate(BRUSH_SIZES):
        x1,y1,x2,y2 = thick_rect(i, tx0)
        cx,cy = (x1+x2)//2, (y1+y2)//2
        r = sz//2 + 4
        sel = (i == thick_idx)
        clr = COLOR_VALUES[col_idx]
        if sel:
            glow_circle(frame,cx,cy,r+4,(0,255,255),1)
            cv2.circle(frame,(cx,cy),r,clr,-1)
        else:
            cv2.circle(frame,(cx,cy),r,(60,60,70),-1)
            cv2.circle(frame,(cx,cy),r,(100,100,110),1)

    # Mode label
    mode_clr = {
        "DRAW":  (0,255,120),
        "ERASE": (0,80,255),
        "IDLE":  (120,120,120),
        "SHAPE": (255,100,255)
    }.get(mode,(200,200,200))
    mx = w - 210
    cv2.putText(frame, f"MODE: {mode}", (mx,32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, mode_clr, 2, cv2.LINE_AA)
    cv2.putText(frame, f"UNDO: {undo_count}  FPS: {fps:.0f}",
                (mx,58), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (100,180,200), 1, cv2.LINE_AA)

    # Brush preview circle
    bp_x, bp_y = w-35, TOOLBAR_H//2
    r2 = BRUSH_SIZES[thick_idx]//2 + 2
    cv2.circle(frame,(bp_x,bp_y),r2+4,(20,20,30),-1)
    cv2.circle(frame,(bp_x,bp_y),r2,COLOR_VALUES[col_idx],-1)
    cv2.circle(frame,(bp_x,bp_y),r2,(180,180,200),1)

    # Bottom status bar
    glass_rect(frame,0,h-28,w,h,(10,12,20),0.75,(0,80,120))
    status = (
        f"  COLOR:{COLOR_NAMES[col_idx]}  "
        f"SIZE:{BRUSH_SIZES[thick_idx]}px  "
        f"[1-8]Color  [+/-]Size  "
        f"[B]Brush Style  [E]Erase  [Z]Undo  [C]Clear  [S]Save  [H]Help  [Q]Quit"
    )
    cv2.putText(frame, status, (8,h-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.34, (0,180,200), 1, cv2.LINE_AA)

    # HUD Elements
    draw_arc_reactor_hud(frame)
    draw_audio_visualizer(frame)
    
    # Jarvis Voice Line
    global active_jarvis_msg, msg_timer
    if time.time() - msg_timer > 5:
        active_jarvis_msg = random.choice(jarvis_lines)
        msg_timer = time.time()
    cv2.putText(frame, active_jarvis_msg, (20, h - 45), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 200), 1, cv2.LINE_AA)

    # Help overlay
    if show_help:
        lines = [
            "AVENGERS GESTURE GUIDE",
            "──────────────────────",
            "1 Finger UP   → Draw",
            "2 Fingers UP  → Erase (Shield)",
            "3 Fingers UP  → Clear All (Explosion)",
            "Fist          → Idle/Pause",
            "Pinch (T+I)   → Next Color",
            "Spider-Man    → Shape Detect! (T+I+P)",
            "Thumb UP      → Bigger brush",
            "Pinky UP      → Smaller brush",
            "──────────────────────",
            "KEYBOARD",
            "B    Change Brush Style",
            "1-8  Select Color",
            "+/-  Brush Size",
            "Z    Undo",
            "C    Clear Canvas",
            "H    Hide Help",
        ]
        hx, hy0 = w-250, TOOLBAR_H+10
        bh = len(lines)*19 + 16
        glass_rect(frame, hx-8, hy0-8, hx+242, hy0+bh, (8,10,18), 0.82, (0,120,160))
        for j,ln in enumerate(lines):
            clr = (0,220,255) if j in (0,11) else (0,160,180)
            cv2.putText(frame, ln, (hx, hy0+j*19),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.36, clr, 1, cv2.LINE_AA)

# ═══════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════
def start_drawing():
    global current_brush_style, current_stroke

    # ── MediaPipe setup (IMAGE mode) ──
    base_opt  = python.BaseOptions(model_asset_path="hand_landmarker.task")
    options   = vision.HandLandmarkerOptions(
        base_options=base_opt,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.5,
    )
    detector  = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    ret, f0 = cap.read()
    if not ret:
        print("[AIR DRAW] Camera not found.")
        return
    H, W = f0.shape[:2]

    # ── State ──
    canvas     = np.zeros((H, W, 3), dtype=np.uint8)
    undo_stack = collections.deque(maxlen=25)

    col_idx    = 0
    thick_idx  = 1
    mode       = "IDLE"
    show_help  = True

    sx, sy     = 0, 0
    px, py     = 0, 0
    ALPHA      = 0.55

    gesture_ts = 0
    G_COOL     = 0.5

    fps_ts     = time.time()
    fps_val    = 0.0
    frame_cnt  = 0
    sw_x0 = 290

    def push_undo():
        undo_stack.append(canvas.copy())

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        H, W  = frame.shape[:2]

        # ── FPS ──
        frame_cnt += 1
        now = time.time()
        if now - fps_ts >= 1.0:
            fps_val   = frame_cnt / (now - fps_ts)
            frame_cnt = 0
            fps_ts   = now

        # ── MediaPipe detect ──
        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_img)

        if result.hand_landmarks:
            lm = result.hand_landmarks[0]
            rx = int(lm[8].x * W)
            ry = int(lm[8].y * H)

            if sx == 0 and sy == 0:
                sx, sy = rx, ry
            else:
                sx = int(ALPHA*rx + (1-ALPHA)*sx)
                sy = int(ALPHA*ry + (1-ALPHA)*sy)

            fu = fingers_up(lm)
            thumb, index, middle, ring, pinky = fu

            tx_px = int(lm[4].x*W); ty_px = int(lm[4].y*H)
            ix_px = int(lm[8].x*W); iy_px = int(lm[8].y*H)

            # ── GESTURES ──

            # FIST → IDLE
            if not index and not middle and not ring and not pinky:
                mode = "IDLE"
                px, py = 0, 0
                current_stroke = []

            # SPIDER-MAN GESTURE (Thumb, Index, Pinky) → SHAPE DETECT
            elif thumb and index and not middle and not ring and pinky:
                mode = "SHAPE"
                if len(current_stroke) > 10 and (now - gesture_ts > G_COOL):
                    push_undo()
                    pts_np = np.array(current_stroke, dtype=np.int32).reshape((-1, 1, 2))
                    peri = cv2.arcLength(pts_np, False)
                    approx = cv2.approxPolyDP(pts_np, 0.04 * peri, True)
                    
                    # Erase the raw stroke
                    for p in current_stroke:
                        cv2.circle(canvas, p, BRUSH_SIZES[thick_idx]*2, (0,0,0), -1)
                    
                    # Draw perfected shape
                    color = COLOR_VALUES[col_idx]
                    thk = BRUSH_SIZES[thick_idx]
                    if len(approx) == 3:
                        cv2.drawContours(canvas, [approx], 0, color, thk)
                    elif len(approx) == 4:
                        x,y,w_s,h_s = cv2.boundingRect(approx)
                        cv2.rectangle(canvas, (x,y), (x+w_s, y+h_s), color, thk)
                    else:
                        (cx, cy), rad = cv2.minEnclosingCircle(pts_np)
                        cv2.circle(canvas, (int(cx), int(cy)), int(rad), color, thk)
                    
                    add_explosion(sx, sy, (255, 0, 255))
                    current_stroke = []
                    gesture_ts = now
                px, py = 0, 0

            # 3 FINGERS → CLEAR W/ EXPLOSION
            elif index and middle and ring and not pinky and (now - gesture_ts > G_COOL):
                push_undo()
                add_explosion(W//2, H//2, (0, 100, 255)) # Massive explosion center
                canvas[:] = 0
                mode = "DRAW"
                px, py = 0, 0
                current_stroke = []
                gesture_ts = now

            # 2 FINGERS → ERASE (SHIELD)
            elif index and middle and not ring and not pinky:
                mode = "ERASE"
                if sy > TOOLBAR_H:
                    push_undo() if (px,py)==(0,0) else None
                    cv2.circle(canvas,(sx,sy),ERASER_R,(0,0,0),-1)
                px, py = 0, 0
                current_stroke = []

            # THUMB PINCH → NEXT COLOR
            elif thumb and not middle and not ring and not pinky:
                d = dist2d((tx_px,ty_px),(ix_px,iy_px))
                if d < 45 and (now - gesture_ts > G_COOL):
                    col_idx = (col_idx+1) % len(PALETTE)
                    gesture_ts = now
                    px, py = 0, 0
                mode = "DRAW"
                current_stroke = []

            # THUMB ONLY → BIGGER BRUSH
            elif thumb and not index and not middle and not ring:
                if now - gesture_ts > G_COOL:
                    thick_idx = min(thick_idx+1, len(BRUSH_SIZES)-1)
                    gesture_ts = now
                mode = "DRAW"
                px, py = 0, 0

            # PINKY ONLY → SMALLER BRUSH
            elif pinky and not index and not middle and not ring:
                if now - gesture_ts > G_COOL:
                    thick_idx = max(thick_idx-1, 0)
                    gesture_ts = now
                mode = "DRAW"
                px, py = 0, 0

            # 1 FINGER → DRAW
            elif index and not middle:
                if sy < TOOLBAR_H:
                    mode = "DRAW"
                    for i in range(len(PALETTE)):
                        x1 = sw_x0 + SX0 + i*(SW+SPAD)
                        if x1 < sx < x1 + SW and (now - gesture_ts > G_COOL):
                            col_idx = i
                            gesture_ts = now
                            break
                    tx0 = sw_x0 + len(PALETTE)*(SW+SPAD) + 18
                    for i in range(len(BRUSH_SIZES)):
                        cx = tx0 + i*(44+5) + 22
                        if abs(sx-cx) < 22 and (now - gesture_ts > G_COOL):
                            thick_idx = i
                            gesture_ts = now
                            break
                    px, py = 0, 0
                    current_stroke = []
                else:
                    mode = "DRAW"
                    # Spawn particles
                    particles.append({'x': sx, 'y': sy, 'color': COLOR_VALUES[col_idx], 'life': 20, 'vx': random.uniform(-2,2), 'vy': random.uniform(-2,2)})
                    
                    if px == 0 and py == 0:
                        px, py = sx, sy
                        current_stroke = [(sx, sy)]
                    else:
                        push_undo() if dist2d((sx,sy),(px,py)) > 40 and len(undo_stack)==0 else None
                        
                        style = brush_styles[current_brush_style]
                        neon_line(canvas, (px,py), (sx,sy), COLOR_VALUES[col_idx], BRUSH_SIZES[thick_idx], style)
                        
                        current_stroke.append((sx, sy))
                        px, py = sx, sy
            else:
                px, py = 0, 0
                current_stroke = []

            # ── CURSOR ──
            if mode == "ERASE":
                draw_shield(frame, sx, sy, ERASER_R)
            elif mode == "SHAPE":
                glow_circle(frame,(sx,sy), 20, (255,0,255), 2)
                cv2.putText(frame, "DETECTING", (sx-30, sy-30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            elif mode == "DRAW":
                glow_circle(frame,(sx,sy), BRUSH_SIZES[thick_idx]//2+4, COLOR_VALUES[col_idx], 2)
                cv2.circle(frame,(sx,sy),3,COLOR_VALUES[col_idx],-1)
            else:
                cv2.circle(frame,(sx,sy),8,(80,80,90),2)

            # ── HAND SKELETON (Holo-theme) ──
            BONES = [(0,1),(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(13,14),(14,15),(15,16),(17,18),(18,19),(19,20),(0,5),(5,9),(9,13),(13,17),(0,17)]
            for a,b in BONES:
                ax,ay = int(lm[a].x*W), int(lm[a].y*H)
                bx2,by2= int(lm[b].x*W), int(lm[b].y*H)
                cv2.line(frame,(ax,ay),(bx2,by2),(0,255,255),1,cv2.LINE_AA)
            for i in range(21):
                lx,ly = int(lm[i].x*W), int(lm[i].y*H)
                cv2.circle(frame,(lx,ly),2,(0,200,240),-1)

        else:
            sx, sy, px, py = 0, 0, 0, 0
            mode = "IDLE"

        # ── DRAW PARTICLES & EXPLOSIONS (VFX) ──
        for p in list(particles):
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] > 0:
                cv2.circle(frame, (int(p['x']), int(p['y'])), max(1, p['life']//4), p['color'], -1)
            else:
                particles.remove(p)
                
        draw_explosions(frame)

        # ── COMPOSITE ──
        gray  = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        bg    = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        bloom = cv2.GaussianBlur(canvas,(9,9),0)
        canvas_glow = cv2.addWeighted(canvas,0.85,bloom,0.4,0)
        display = cv2.add(bg, canvas_glow)

        # ── OVERLAYS ──
        draw_scanlines(display)
        draw_ui(display, col_idx, thick_idx, mode, len(undo_stack), show_help, fps_val)

        cv2.namedWindow("JARVIS AIR CANVAS - AVENGERS", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("JARVIS AIR CANVAS - AVENGERS", W, H)
        cv2.imshow("JARVIS AIR CANVAS - AVENGERS", display)

        # ── KEYS ──
        key = cv2.waitKey(1) & 0xFF
        if   key == ord('q') or key==27:   break
        elif key == ord('c'):
            push_undo(); canvas[:]=0; add_explosion(W//2, H//2, (0, 255, 255))
        elif key == ord('z'):
            if undo_stack: canvas = undo_stack.pop()
        elif key == ord('b'):
            current_brush_style = (current_brush_style + 1) % len(brush_styles)
        elif key == ord('s'):
            fname = f"jarvis_art_{int(time.time())}.png"
            cv2.imwrite(fname, display)
            print(f"[SAVED] {fname}")
        elif key == ord('h'): show_help = not show_help
        elif key == ord('e'): mode = "ERASE" if mode!="ERASE" else "DRAW"; px,py = 0,0
        elif ord('1') <= key <= ord('8'): col_idx = key - ord('1')
        elif key == ord('+') or key == ord('='): thick_idx = min(thick_idx+1, len(BRUSH_SIZES)-1)
        elif key == ord('-'): thick_idx = max(thick_idx-1, 0)
        elif key == ord(']'): col_idx = (col_idx+1) % len(PALETTE)
        elif key == ord('['): col_idx = (col_idx-1) % len(PALETTE)

    cap.release()
    cv2.destroyAllWindows()
    detector.close()

if __name__ == "__main__":
    start_drawing()