from pydantic import BaseModel

class DoorLock(BaseModel):

    locked: bool
    
    def __init__(self):
        self.locked = False
    