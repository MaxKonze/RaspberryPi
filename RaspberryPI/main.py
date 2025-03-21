import RFID_reader
import asyncio
import websockets
import json
import requests
import Keypad
import motor

with open("/home/max/DoorLock/RaspberryPi/RaspberryPI/config.json") as f:
    config = json.load(f)
    host = config["host"]
    port = config["port"]

delay_seconds = 3
ang_open = 1
ang_close = -1

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


def moveMotor(destination):
    motor.moveSteps(destination, delay_seconds, 200)

async def websocket_listener():
    uri = f"ws://{host}:{port}/ws" 

    async with websockets.connect(uri) as websocket:
        print("WebSocket verbunden!")

        while True:
            message = await websocket.recv()
            print(f"WebSocket-Befehl erhalten: {message}")

            if message == "exit":
               raise KeyboardInterrupt 
           
            if message == "lock":
                moveMotor(ang_close)
                
            elif message == "unlock":
                moveMotor(ang_open)
                

def keypad_loop():
    while True:
        
        key = keypad.getKey()
        
        rfid = RFID_reader.read_uid()

        if key != keypad.NULL:
            state = requests.post(f'http://{host}:{port}/status').json().get("locked", "")

            if state == False:
                continue

            response = requests.post(f'http://{host}:{port}/key', json={'key': key})
            response_data = response.json()

            pin = response_data.get("pin", "")

            print(f" Eingabe: {pin}")
            
        elif rfid != None:
            
            state = requests.post(f'http://{host}:{port}/status').json().get("locked", "")

            if state == False:
                continue
            
            response = requests.post(f'http://{host}:{port}/rfid', json={'rfid': rfid})

            print(f" RFID: {rfid}")

async def main():
    requests.post(f'http://{host}:{port}/reset_pin') 
    
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, keypad_loop) 
    await websocket_listener()
    


if __name__ == '__main__':
    print("Starting")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Ending...")
        exit()
