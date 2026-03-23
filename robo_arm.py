import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
import math


base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.HandLandmarker.create_from_options(options)



in_min = 0.04740
in_max = 0.14474
def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def map_middle(x):
    return (x + 0.027) * 180 / 0.054

def map_rotate(x):
    return (x - 0.35) * (-270 / -0.51) + 270



cap = cv2.VideoCapture(0)
v_angle = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image( image_format=mp.ImageFormat.SRGB, data=rgb_frame )

    timestamp_ms = int(time.time() * 1000)
    result = detector.detect_for_video(mp_image, timestamp_ms)

    if result.hand_world_landmarks != []:
        landmark = result.hand_world_landmarks
        thumb_x, thumb_y, thumb_z = landmark[0][4].x, landmark[0][4].y, landmark[0][4].z
        little_x, little_y, little_z = landmark[0][17].x, landmark[0][17].y, landmark[0][17].z

        
        base = landmark[0][0]
        index = landmark[0][5]
        thumb = landmark[0][4]
        radius = landmark[0][1]
        little = landmark[0][17]

        lit_base = (little.x - base.x)

        angle_middle = map_middle(lit_base)
        if angle_middle <= 35:
            m_angle = 5
        elif angle_middle < 90:
            m_angle = 90
        else:
            m_angle = 175
        # print(m_angle)

        abs_dis = distance(thumb_x, thumb_y, thumb_z, little_x, little_y, little_z)
        angle = map_value(abs_dis, in_min, in_max, 0, 180)
        if angle<=35:
            v_angle = 5
        elif angle>35 and angle<100:
            v_angle = 90
        else:
            v_angle = 175
    # print(v_angle)

    # if(result.handedness.isempty!=True):
    if result.handedness:
        hand = result.handedness[0][0].display_name
        Right = 1 if hand == 'Right' else -1
        dx = radius.x - base.x
        d = map_rotate(dx)
        # d = map_rotate(dx)
        b = (Right*d)
        if b<=90:
            b_angle = 5
        elif b>90 and angle<100:
            b_angle = 134
        else:
            b_angle = 270
        # print(b_angle)
        print(v_angle, m_angle, b_angle)



    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
