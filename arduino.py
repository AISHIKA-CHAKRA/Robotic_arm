import serial
import time

arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for Arduino reset

while True:
    arduino.write(b'1')
    print("LED ON")
    time.sleep(0.5)

    arduino.write(b'0')
    print("LED OFF")
    time.sleep(0.5)
