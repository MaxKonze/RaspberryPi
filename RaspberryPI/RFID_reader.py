import sys
import os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), 'RFID'))

from RFID.MFRC522 import MFRC522

mfrc = MFRC522()

def read_uid():
    print("Place the RFID card near the reader...")
    
    (status, TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
        
    if status == mfrc.MI_OK:
        print("Card detected")
            
        (status, uid) = mfrc.MFRC522_Anticoll()
            
        if status == mfrc.MI_OK:
            print(f"Card UID: {' '.join(map(str, uid))}")  
            
            return ' '.join(map(str, uid))

    return None

if __name__ == "__main__":
    while True:
        status = read_uid()
        if status:
            break
        sleep(1)
