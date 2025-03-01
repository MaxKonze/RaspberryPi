from gpiozero import AngularServo
from time import sleep
import Keypad
import requests
import json
from datetime import datetime, timedelta

with open("/home/max/DoorLock/RaspberryPi/RaspberryPI/config.json") as f:
    config = json.load(f)
    host = config["host"]
    port = config["port"]

delay_seconds = 0.001

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

time_opened = 5
closing_time = None


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
    global pin, closing_time
    while True:
        if closing_time != None:
            if closing_time <= datetime.now():
                moveServo(ang_close)
                closing_time = None
                requests.post(f'http://{host}:{port}/lock')

        key = keypad.getKey()
        state = requests.post(f'http://{host}:{port}/status').json().get("locked", "")

        if key != keypad.NULL and state == True:

            response = requests.post(f'http://{host}:{port}/key', json={'key': key})
            response_data = response.json()

            pin = response_data.get("pin", "")
            status = response_data.get("status","")

            print(f"Input: {pin}")
            
            if status == True:
                closing_time = datetime.now() + timedelta(seconds=time_opened)
                moveServo(ang_open)
                
        sleep(1)

            
if __name__ == '__main__':
    print("Starting")
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopping")
        servo.close()
        keypad.close()
        exit()