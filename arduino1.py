import serial
import cv2
import mediapipe as mp
import numpy as np
from medipipe.tasks import python
from mediapipe.tasks.python import vision
import time
import math

cap = cv2.VideoCapture(0)

base_options = python.BaseOptions(model_asset_path = 'hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 1,
    running_mode = vision.RunningMode.VIDEO
)
detector = vision.HandLandmarker.create_from_options(options)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

in_min = 0.04346
in_max = 0.13800

def map_value(x, in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max - out_min) / (in_max - in_min) + out_min

arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Wait for Arduino reset

# cap  =
# while :
#     arduino.write(b'1')
#     print("LED ON")
#     time.sleep(0.5)

#     arduino.write(b'0')
#     print("LED OFF")
#     time.sleep(0.5)