#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# －－－－极光编程－－－－
#  文件名：motor.py
#  版本：V2.0
#  author: Jessy
#  说明：智能小车实验
#####################################################
from machine import Pin, PWM
from utime import sleep

# 设置管脚PIN
left1_pin  = 15   
left2_pin   = 2
right1_pin  = 16   #5
right2_pin  = 4
avoid_left_pin = 5       #寻迹  22
avoid_right_pin = 17      #23
follow_left_pin = 19     #避障
follow_right_pin = 18
mode_pin = 21
redLED_pin = 22
blueLED_pin = 23

#motor初始化
def motor_setup():
    global motro_left1
    global motro_left2
    global motro_right1     
    global motro_right2
        
    motro_left1 = PWM(Pin(left1_pin), freq=20000, duty=0)  # 创建motor pwm对象，设置为输出模式 
    motro_left2 = PWM(Pin(left2_pin),freq=20000, duty=0)
    motro_right1 = PWM(Pin(right1_pin),freq=20000, duty=0)   
    motro_right2 = PWM(Pin(right2_pin),freq=20000, duty=0)

# 初始化寻迹避障模块GPIO口
def gpio_setup():
    global avoid_left
    global avoid_right
    global follow_left
    global follow_right
    global mode_button
    global led_red
    global led_blue
    
    avoid_left = Pin(avoid_left_pin,Pin.IN)
    avoid_right = Pin(avoid_right_pin,Pin.IN)
    follow_left = Pin(follow_left_pin,Pin.IN,Pin.PULL_UP)
    follow_right = Pin(follow_right_pin,Pin.IN,Pin.PULL_UP)
    mode_button = Pin(mode_pin,Pin.IN,Pin.PULL_UP)
    led_red = Pin(redLED_pin,Pin.OUT)
    led_blue = Pin(blueLED_pin,Pin.OUT)
    
#方向函数
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
def fast_forward():
    motro_left1.duty(1000) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(1000) # 输出高电平
    motro_right2.duty(0)
def slow_forward():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(780) # 输出高电平
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
    
def tracing():
    slow_forward()
    if follow_left.value()==1 and follow_right.value()==0:
        turn_left()
        print('Black line is detected on the left,turn left')
    elif follow_left.value()==0 and follow_right.value()==1:
        turn_right()
        print('Black line is detected on the ritht,turn right')
    else:
        slow_forward()
        print('forward')

def avoid_obstacle():
    if avoid_left.value()==0 and avoid_right.value()==1 :       #前方任何一个红外遇到黑色（障碍物）
        backward()
        print('backward')
        sleep(1)
        turn_right()
        print('turn right')
        sleep(0.5)
        slow_forward()
        print('forward')
    elif avoid_left.value()==1 and avoid_right.value()==0 :       #前方任何一个红外遇到黑色（障碍物）
        backward()
        print('backward')
        sleep(1)
        turn_left()
        print('turn left')
        sleep(0.5)
        slow_forward()
        print('forward')
    elif avoid_left.value()==0 and avoid_right.value()==0 :       #前方任何一个红外遇到黑色（障碍物）
        backward()
        print('backward')
        sleep(1)
        slow_forward()
        print('forward')
    else:
        slow_forward()
        print('forward')
def led_show():
    if mode==1: #寻迹模式
        led_red.on()
        led_blue.off()
    elif mode==2: #避障模式
        led_red.off()
        led_blue.on()
    else:
        led_red.off()
        led_blue.off()
        
        
    
#通过红外模块获取方向
#红外传感器，二极管不断发射红外线，遇到白色反射回来，红外接收管饱和，输出低电平，否则输出高电平
#    (black line:1,white line:0)

def handler_interrupt(pin):
    global mode
    if(mode<2):
        mode = mode + 1
    else:
        mode = 0
    print("mode:",mode,end='\t')
def get_mode():
    mode_button.irq(trigger=Pin.IRQ_FALLING,handler=handler_interrupt)
    return mode
    


#主程序
mode = 0
motor_setup()
gpio_setup()
# 按键监听
while True:
    if get_mode():
        break
    
while True:
    mode = get_mode()
    if mode==1:
        tracing()
        led_show()
        print("tracing mode",end="\t")
    elif mode==2:
        avoid_obstacle()
        led_show()
        print("avoid obstacle mode",end="\t")
    else:
        stop()
        led_show()
        break
        print("break",end="\t")
    





















