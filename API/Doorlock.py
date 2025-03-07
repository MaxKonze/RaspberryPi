import json 

class DoorLock:
    def __init__(self):
        self.locked = False
        self.code = ""
        self.opentime = 10
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.unlock_code = config['unlock_code']

    def reset_code(self):
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
        
        if len(self.code) > 4:
            self.reset_code()
    
    def checkPin(self):
        if self.code == self.unlock_code:
            self.unlock()
            return True
        else:
            return False
        
    def get_length(self):
        return len(self.code)
    
    def get_opentime(self):
        return self.opentime
