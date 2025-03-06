# DoorLock Project

This project is designed to control a door lock using a Raspberry Pi. It includes a Python script to manage the lock mechanism.

## Prerequisites

- Raspberry Pi
- Python 3.x
- Required Python libraries (see `requirements.txt`)

## Setup

1. Clone the repository to your PC (API Host):
    ```sh
    git clone https://github.com/MaxKonze/DoorLock.git
    ```
2. Navigate to the project directory:
    ```sh
    cd DoorLock
    ```
3. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the main script to start the door lock control API:
```sh
python main.py
```
Run the doorLock script to start the door lock control on the Raspberry Pi:
```sh
cd ../RaspberryPi
```

```sh
python doorLock.py
```
