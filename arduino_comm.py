import serial
import time

arduino = None

def connect_arduino(port='COM7'):
    global arduino
    arduino = serial.Serial(port, 9600)
    time.sleep(2)
    print("Arduino Connected")

def send_signal(signal):
    if arduino:
        print("Sending:", signal)
        arduino.write(signal.encode())
        time.sleep(0.1)