from mfrc522 import MFRC522
import time

reader = MFRC522()

def scanRFIDCARD():
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    if status == reader.MI_OK:
        print("RFID-Karte erkannt!")


        (status, uid) = reader.MFRC522_Anticoll()
        print(uid)
        
        if status == reader.MI_OK:
            uid_str = "-".join([str(i) for i in uid])
            print(f"RFID UID: {uid_str}")
            
try:
    while True:
        scanRFIDCARD()
        time.sleep(1) 

except KeyboardInterrupt:
    print("Beendet")
