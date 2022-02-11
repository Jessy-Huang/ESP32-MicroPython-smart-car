from machine import Pin, PWM
from time import sleep
import machine
from myIRremote import IR

# 设置管脚PIN
left1_pin  = 13   
left2_pin   = 12
right1_pin  = 14   #5
right2_pin  = 27
IRremote_pin = 34

def motor_setup():
    global motro_left1
    global motro_left2
    global motro_right1     
    global motro_right2
        
    motro_left1 = PWM(Pin(left1_pin), freq=20000, duty=0)  # 创建motor pwm对象，设置为输出模式 
    motro_left2 = PWM(Pin(left2_pin),freq=20000, duty=0)
    motro_right1 = PWM(Pin(right1_pin),freq=20000, duty=0)   
    motro_right2 = PWM(Pin(right2_pin),freq=20000, duty=0)
# 方向控制
def slow_forward():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(780) # 输出高电平
    motro_right2.duty(0)
def turn_left():
    motro_left1.duty(380) # 输出高电平 400
    motro_left2.duty(0)
    motro_right1.duty(680) # 输出高电平
    motro_right2.duty(0)
def turn_right():
    motro_left1.duty(680) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(380) # 输出高电平
    motro_right2.duty(0)
def backward():
    motro_left1.duty(0) # 输出高电平
    motro_left2.duty(780)
    motro_right1.duty(0) # 输出高电平
    motro_right2.duty(780)
def stop():
    motro_left1.duty(0) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(0) # 输出高电平
    motro_right2.duty(0)
# 程序入口
if __name__ == '__main__':
    motor_setup()
    ir = IR(IRremote_pin)
    state = 0
    
    while True:
        changed, s, repeat, ir_ok = ir.scan()
        if changed == True:  
            if s == 'up' and state != 1:
                state = 1
                slow_forward()
                print("forward")
            elif s == 'down' and state != 2:
                state = 2
                backward()
                print("backward")
            elif s == 'left' and state != 3:
                state = 3
                turn_left()
                print("turn left")
            elif s == 'right' and state != 4:
                state = 4
                turn_right()
                print("turn right")
        else:
            if state != 0:
                state = 0
                stop()
                print("stop")
        sleep(0.2)
                
        
