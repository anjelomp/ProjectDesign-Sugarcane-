import time
import serial
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Conveyor and actuator control pins
CONVEYOR_PIN = 18
ACTUATOR_PIN = 23

# Ultrasonic sensor pins
ULTRASONIC_TRIGGER = 4
ULTRASONIC_ECHO = 17

# Set up GPIO
GPIO.setup(CONVEYOR_PIN, GPIO.OUT)
GPIO.setup(ACTUATOR_PIN, GPIO.OUT)
ultrasonic = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIGGER)

# Start conveyor
GPIO.output(CONVEYOR_PIN, GPIO.HIGH)

# Initialize serial communication with Arduino
arduino = serial.Serial("/dev/ttyS0", 9600, timeout=1)
time.sleep(2)

# Generate 20 randomized variety signals (5 of each type)
varieties = [1, 2, 3, 4, 5] * 4
random.shuffle(varieties)

variety_index = 0

def detect_and_send():
    global variety_index

    while variety_index < len(varieties):
        distance = ultrasonic.distance  # Read ultrasonic sensor

        if distance < 0.1:  # Object detected
            detected_variety = varieties[variety_index]
            variety_index += 1

            message = f"{detected_variety}\n"
            arduino.write(message.encode())  # Send variety number to Arduino
            print(f"Sent to Arduino: {message.strip()}")

            GPIO.output(ACTUATOR_PIN, GPIO.HIGH)  # Activate actuator for 5 sec
            time.sleep(5)
            GPIO.output(ACTUATOR_PIN, GPIO.LOW)

            time.sleep(5)  # Wait before next detection
        else:
            arduino.write(b"0\n")  # Send idle signal
            print("No object detected")

try:
    detect_and_send()
except KeyboardInterrupt:
    GPIO.output(CONVEYOR_PIN, GPIO.LOW)  # Stop conveyor on exit
    GPIO.cleanup()
