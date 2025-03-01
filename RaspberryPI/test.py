import requests
import json

with open("/home/max/DoorLock/RaspberryPi/RaspberryPI/config.json") as f:
    config = json.load(f)
    host = config["host"]
    port = config["port"]

print(requests.post(f'http://{host}:{port}/status').json().get("locked", ""))