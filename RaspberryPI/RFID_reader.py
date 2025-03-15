import sys
import os
import time

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
            
            return True

        time.sleep(1)

if __name__ == "__main__":
    while True:
        st = read_uid()
        if st:
            break
