class DoorLock:
    def __init__(self):
        self.locked = False
        self.code = None

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def is_locked(self):
        return self.locked
