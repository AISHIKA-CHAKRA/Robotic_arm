🖐️ Hand Gesture Controlled Angle System

A real-time hand gesture recognition system that converts finger movements into discrete angle outputs using computer vision. This project uses a webcam to track hand landmarks and maps gestures to control values, making it suitable for robotics and gesture-based interfaces.

🚀 Features

Real-time hand tracking using webcam

Detects up to 2 hands simultaneously

Converts gestures into 3 control angles:

Vertical Angle (v_angle)

Middle Angle (m_angle)

Rotation Angle (b_angle)

Works with both left and right hands

Smooth mapping of hand movements to discrete outputs


🧠 How It Works

Captures live video using OpenCV

Uses MediaPipe Hand Landmarker to detect 21 hand landmarks

Tracks key points:

Thumb tip

Little finger tip

Wrist (base)

Index base

Calculates:

Distance between fingers → controls vertical angle

Horizontal movement → controls middle angle

Hand orientation → controls rotation

Maps values into predefined angle ranges (e.g., 5°, 90°, 175°)

📦 Tech Stack
Python

OpenCV

MediaPipe

NumPy

📂 Project Structure

├── main.py                 # Main script

├── hand_landmarker.task   # Pretrained MediaPipe model

├── README.md              # Project documentation
