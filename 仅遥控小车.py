from machine import Pin, PWM
import machine
from utime import sleep
from myIRremote import IR

if __name__ == "__main__":
    machine.freq(160000000)
    pwm1 = PWM(Pin(13), freq=500, duty=0)
    pwm2 = PWM(Pin(27), freq=500, duty=0)
    pwm3 = PWM(Pin(12), freq=500, duty=0)
    pwm4 = PWM(Pin(14), freq=500, duty=0)
    state = 0
    speed = 512
    t = IR(34)
    while(True):
        changed, s, repeat, t_ok = t.scan()
        if changed == True:
            if s == '1':
                speed = 512
            elif s == '2':
                speed = 640
            elif s == '3':
                speed = 768
            if repeat >= 2:
                if s == 'up' and state != 1:
                    state = 1
                    pwm1.duty(speed)       
                    pwm2.duty(speed)        
                    pwm3.duty(0)          
                    pwm4.duty(0)          
                    print("state1")
                elif s == 'down' and state != 2:
                    state = 2
                    pwm1.duty(0)          
                    pwm2.duty(0)          
                    pwm3.duty(speed)        
                    pwm4.duty(speed)        
                    print("state2")
                elif s == 'left' and state != 3:
                    state = 3
                    pwm1.duty(0)          
                    pwm2.duty(int(speed/2 + 128))        
                    pwm3.duty(int(speed/2 + 128))        
                    pwm4.duty(0)         
                    print("state3")
                elif s == 'right' and state != 4:
                    state = 4
                    pwm1.duty(int(speed/2 + 128))        
                    pwm2.duty(0)          
                    pwm3.duty(0)          
                    pwm4.duty(int(speed/2 + 128))        
                    print("state4")
        else:
            if state != 0:
                state = 0
                pwm1.duty(0)         
                pwm2.duty(0)         
                pwm3.duty(0)          
                pwm4.duty(0)         
                print("state0")
        sleep(0.2)