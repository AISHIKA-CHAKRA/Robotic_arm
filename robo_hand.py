import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import time
import serial

# SERIAL
arduino = serial.Serial('COM7', 9600)
time.sleep(2)

# MEDIAPIPE
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.HandLandmarker.create_from_options(options)

# DUTO distance FUNCTION
in_min = 0.04346 # Ekdom Change noi
in_max = 0.13771 # Ekdom Change noi

def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def map_value(x, in_min, in_max, out_min, out_max):
    return max(0, min(180,
        (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    ))

def map_middle(x):
    return (x + 0.027) * 180 / 0.054

def map_rotate(x):
    return (x - 0.35) * (-270 / -0.51) + 270

# Video Camera
cap = cv2.VideoCapture(0)
claw_angle = 90
middle_angle = 90
base_angle = 0
v_angle = 90
m_angle = 90
b_angle = 90
last_angle = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    timestamp_ms = int(time.time() * 1000)
    result = detector.detect_for_video(mp_image, timestamp_ms)

    if result.hand_world_landmarks:
        landmark = result.hand_world_landmarks[0]
        base = landmark[0]
        index = landmark[5]
        thumb = landmark[4]
        radius = landmark[1]
        little = landmark[17]

        lit_base = (little.x - base.x)
        angle_middle = map_middle(lit_base)
        if angle_middle <= 35:
            m_angle = 5
        elif angle_middle < 75:
            m_angle = 90
        else:
            m_angle = 175

        abs_dis = distance(thumb.x, thumb.y, thumb.z, little.x, little.y, little.z)
        angle_claw = map_value(abs_dis, in_min, in_max, 0, 180)
        if result.handedness:
            hand = result.handedness[0][0].display_name
            Right = 1 if hand == 'Right' else -1
            dx = radius.x - base.x
            d = map_rotate(dx)
            # d = map_rotate(dx)
            b = (Right*d)
            if b<=90:
                b_angle = 60
            elif b>90 and b<100:
                b_angle = 134
            else:
                b_angle = 270

        # Ekhane 3 teh angle a filter korchi jeta phone ae bollam
        # Nahole oto different value porte porte unstable hoye jabe
        if angle_claw <= 35:
            v_angle = 70
        elif angle_claw < 100:
            v_angle = 90
        else:
            v_angle = 175

        # Send only if angle changed
        # if v_angle != last_angle:
        if b_angle == last_angle:
            arduino.write(f"{int(v_angle)} {int(m_angle)} {int(90)}\n".encode())
        else:
            arduino.write(f"{int(v_angle)} {int(m_angle)} {int(b_angle)}\n".encode())

        # arduino.write(f"{int(v_angle)} {int(m_angle)} {int(b_angle)}\n".encode())
    else:
        arduino.write(f"{int(v_angle)} {int(m_angle)} {int(90)}\n".encode())

    print(v_angle, m_angle, b_angle)
    cv2.imshow("RoboHandControl", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()

