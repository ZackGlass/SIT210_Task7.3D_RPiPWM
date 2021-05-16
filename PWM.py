import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
TRIG = 16
ECHO = 18
LED = 12

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, 3000)
last = 0
pwm.start(last)

counter = 0;

def Distance():
    
    count = 0;
    newRead = False
    
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    
    while GPIO.input(ECHO) == 0:
        pass
        count += 1
        if count == 5000:
            newRead = True
            break
        
    if newRead:
        return False
    
    start = time.time()
    stop = 0
    
    while GPIO.input(ECHO) == 1:
        stop = time.time()
        pass
        
        
    if stop == start or stop == 0:
        distance = 0
    else:
        duration = stop - start
        distance = (duration * 34300) / 2
    
    print(distance)
    return int(distance)

def dutyCycle(dist):
    if dist > 2 and dist <= 400:
        x = 100 - (dist / 4)
    elif dist > 400:
        x = 0 
    elif dist <= 2:
        x = 100
    #x = 100 - x
    return int(x)
    

try:
    while True:
        counter += 1
        
        dist = Distance()
        dcycle = dutyCycle(dist)
        print("counter: ", counter, " | distance: ", dist, " | duty cycle: ", dcycle)
        #pwm.ChangeDutyCycle(dcycle)
        if (last < dcycle):
            for x in range(last, dcycle, 1):
                pwm.ChangeDutyCycle(x)
                time.sleep(0.0001)
        elif (last > dcycle):
            for x in range(last, dcycle, -1):
                pwm.ChangeDutyCycle(x)
                time.sleep(0.0001)
        else:
            continue
                                                    
        last = dcycle          
        time.sleep(0.05)
             
            
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
        
     