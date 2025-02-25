import json 

class DoorLock:
    def __init__(self):
        self.locked = False
        self.code = ""
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.unlock_code = config['unlock_code']

    def reset_code(self):
        self.code = self.code[-1]
    
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
            return True
        else:
            return False
