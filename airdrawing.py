import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "hand_landmarker.task"

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

current_color = (255, 0, 0)

def start_drawing():

    base_options = BaseOptions(model_asset_path=model_path)

    options = HandLandmarkerOptions(
        base_options=base_options,
        running_mode=VisionRunningMode.IMAGE,
        num_hands=1
    )

    landmarker = HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    canvas = None
    prev_x, prev_y = 0, 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = landmarker.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:

                h, w, _ = frame.shape

                index_tip = hand_landmarks[8]
                middle_tip = hand_landmarks[12]
                ring_tip = hand_landmarks[16]

                index_pip = hand_landmarks[6]
                middle_pip = hand_landmarks[10]
                ring_pip = hand_landmarks[14]

                ix, iy = int(index_tip.x * w), int(index_tip.y * h)

                index_up = index_tip.y < index_pip.y
                middle_up = middle_tip.y < middle_pip.y
                ring_up = ring_tip.y < ring_pip.y

                # CLEAR
                if index_up and middle_up and ring_up:
                    canvas = np.zeros_like(frame)
                    prev_x, prev_y = 0, 0

                # ERASER
                elif index_up and middle_up:
                    cv2.circle(canvas, (ix, iy), 20, (0, 0, 0), -1)
                    prev_x, prev_y = 0, 0

                # DRAW
                elif index_up and not middle_up:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = ix, iy

                    cv2.line(canvas, (prev_x, prev_y), (ix, iy), current_color, 5)
                    prev_x, prev_y = ix, iy

                else:
                    prev_x, prev_y = 0, 0

        combined = cv2.add(frame, canvas)
        cv2.imshow("Jarvis Air Canvas", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 👇 YE LOOP KE BAHAR HONA CHAHIYE
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_drawing()