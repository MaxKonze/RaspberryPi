from gpiozero import AngularServo
from time import sleep
import Keypad
import requests
import json
from datetime import datetime, timedelta
import motor

with open("/home/max/DoorLock/RaspberryPi/RaspberryPI/config.json") as f:
    config = json.load(f)
    host = config["host"]
    port = config["port"]

delay_seconds = 3

ang_open = 1
ang_close = -1

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


def moveMotor(destination):
    motor.moveSteps(destination, delay_seconds, 100)

def loop():
    global pin, closing_time
    while True:
        if closing_time != None:
            if closing_time <= datetime.now():
                moveMotor(ang_close)
                closing_time = None
                requests.post(f'http://{host}:{port}/lock')

        key = keypad.getKey()
        

        if key != keypad.NULL:

            state = requests.post(f'http://{host}:{port}/status').json().get("locked", "")

            if state == True:
                continue

            response = requests.post(f'http://{host}:{port}/key', json={'key': key})
            response_data = response.json()

            pin = response_data.get("pin", "")
            status = response_data.get("status","")

            print(f"Input: {pin}")
            
            if status == True:
                closing_time = datetime.now() + timedelta(seconds=time_opened)
                moveMotor(ang_open)
    

            
if __name__ == '__main__':
    print("Starting")
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopping")
        exit()