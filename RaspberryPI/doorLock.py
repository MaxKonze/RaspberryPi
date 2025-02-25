from gpiozero import AngularServo
from time import sleep
import Keypad
import json
import requests


delay_seconds = 0.01

ang = 0

ang_open = 180
ang_close = 0

myCorrection = 0
maxPW = (2.5 + myCorrection) / 1000
minPW = (0.5 + myCorrection) / 1000

servo = AngularServo(16, initial_angle=ang, min_angle=0, max_angle=180, min_pulse_width=minPW, max_pulse_width=maxPW)

pin = ""

ROWS = 4
COLS = 4
keys = ['1','2','3','A',
        '4','5','6','B',
        '7','8','9','C',
        '*','0','#','D']

row_Pins = [18, 23, 24, 25]
col_Pins = [22, 27, 17, 4]

keypad = Keypad.Keypad(keys, row_Pins, col_Pins, ROWS, COLS)
keypad.setDebounceTime(50)

def moveServo(destination):
    global ang
    if destination > ang:
        for angle in range(ang, destination):
            servo.angle = angle
            sleep(delay_seconds)
    else:
        for angle in range(ang, destination, -1):
            servo.angle = angle
            sleep(delay_seconds)
    ang = destination

def loop():
    global pin
    while True:
        key = keypad.getKey()
        if key != keypad.NULL:
            response = requests.post('http://localhost:8000/key', json={'key': key})
            print(response.pin)
            pin = response.pin
            
            print(f"Input: {pin}")
            
            if response.pin_status == True:
                moveServo(ang_open)

if __name__ == '__main__':
    print("Starting")
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopping")
        servo.close()
        keypad.cleanup()
        exit()