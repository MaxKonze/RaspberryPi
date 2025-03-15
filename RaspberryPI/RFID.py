from RFID import MFRC522
import time

# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

def read_uid():
    print("Place the RFID card near the reader...")
    
    while True:
        # Scan for cards
        (status, TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
        
        # If a card is found
        if status == mfrc.MI_OK:
            print("Card detected")
            
            # Get the UID of the card
            (status, uid) = mfrc.MFRC522_Anticoll()
            
            # If we have the UID, print it
            if status == mfrc.MI_OK:
                print(f"Card UID: {' '.join(map(str, uid))}")
                break  # Exit after reading the card UID

        time.sleep(1)

if __name__ == "__main__":
    read_uid()
