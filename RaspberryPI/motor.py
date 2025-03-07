from gpiozero import OutputDevice
import time

motorPins = (6, 13, 19, 26) 

motors = list(map(lambda pin: OutputDevice(pin), motorPins))
CCWStep = (0x01,0x02,0x04,0x08)
CWStep = (0x08,0x04,0x02,0x01) 

def moveOnePeriod(direction,ms):
    for j in range(0,4,1): 
        for i in range(0,4,1): 
            if (direction == 1):
                motors[i].on() if (CCWStep[j] == 1<<i) else motors[i].off()
            else:
                motors[i].on() if CWStep[j] == 1<<i else motors[i].off()
            if(ms<3): 
                ms = 3
            time.sleep(0.0005)
            
def moveSteps(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod(direction, ms)
    
def motorStop():
    for i in range(0,4,1):
        motors.off()

