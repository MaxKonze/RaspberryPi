import json 

class DoorLock:
    def __init__(self):
        self.locked = False
        self.code = ""
        self.opentime = 20
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.unlock_code = config['unlock_code']
            self.opentime = config['opentime']
            self.rfid = config['rfid_uid']

    def reset_code(self):
        if len(self.code) >= 4:
            self.code = ""
        
    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
        self.reset_code()

    def is_locked(self):
        return self.locked
    
    def update_code(self, code):
        self.code += code
    
    def checkPin(self):
        if self.code == self.unlock_code:
            return True
        else:
            return False
        
    def get_length(self):
        return len(self.code)
    
    def get_opentime(self):
        return self.opentime
    
    def check_rfid(self, rfid):
        print(rfid)
        
        if rfid == self.rfid:
            return True
        else:
            return False
