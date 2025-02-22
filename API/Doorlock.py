class DoorLock:
    def __init__(self):
        self.locked = False
        self.code = None

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
    
