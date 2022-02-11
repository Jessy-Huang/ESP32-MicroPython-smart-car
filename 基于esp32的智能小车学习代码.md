## 第一课 ##

## 点亮led ##

```python
#外设LED闪烁
from machine import Pin
import time
led = Pin(22,Pin.OUT)
while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep_ms(500)
    led.value(1)
    time.sleep_us(1000000)
    led.value(0)
    time.sleep(0.5)


```

## 流水灯 ##

```python
from machine import Pin
import time

led0 = Pin(21,Pin.OUT)
led1 = Pin(22,Pin.OUT)
led2 = Pin(23,Pin.OUT)

while True:
        led0.value(1) #点亮led
        time.sleep(1)
        led0.value(0) #熄灭led
        time.sleep(1)
        
        led1.value(1)
        time.sleep(1)
        led1.value(0)
        time.sleep(1)
        
        led2.value(1)
        time.sleep(1)
        led2.value(0)
        time.sleep(1)
        
```

## 从1数到3 ##

```python
from machine import Pin
import time

led0 = Pin(32,Pin.OUT)
led1 = Pin(33,Pin.OUT)
led2 = Pin(25,Pin.OUT)

while True:
    led0.on()
    time.sleep(0.5)
    led1.on()
    time.sleep(0.5)
    led1.on()
    time.sleep(0.5)
    led0.off()
    led1.off()
    led2.off()
   
```

## 按键控制led ##

```Python
import machine

led = machine.Pin(32,machine.Pin.OUT)
button = machine.Pin(0,machine.Pin.IN)

while True:
    if(button.value()==0):
        led.value(0)
    else:
        led.value(1)
```



# 第二课 #

## ## pwm ## ##

```Python
>>> from machine import PWM,Pin
>>> p22 = Pin(22,Pin.OUT)
>>> pwm = PWM(p22)
>>> pwm
PWM(22, freq=100, duty=736)
>>> pwm.freq(500)
>>> pwm.duty(512)
>>> pwm
PWM(22, freq=500, duty=512)

```

## 呼吸灯 ##

```Python
from machine import Pin,PWM
import time

p22 = Pin(22,Pin.OUT)
#构建PWM对象pwm_LED
pwm_led = PWM(p22,)
#设置pwm_led频率
pwm_led.freq(100) #1/T表示时间
#占空比
duty=0 #占空比为0是电压为0.灯泡不亮
while True:
    while duty<1008:
        duty=duty+16
        time.sleep_ms(10)   #延时10ms
        pwm_led.duty(duty)
    while duty>0:
        duty=duty-16
        time.sleep_ms(10)
        pwm_led.duty(duty)


```

## 练习题 ##

```Python
import machine

led = machine.Pin(32,machine.Pin.OUT)
button = machine.Pin(0,machine.Pin.IN)

while True:
    if(button.value()==0):
        led.value(0)
    else:
        led.value(1)

```

## 边沿出发中断 ##

```python
### boot 按键按下led状态与前一次按键相反

from machine import Pin
import time

led = Pin(2,Pin.OUT)
button = Pin(21,Pin.IN,Pin.PULL_UP)

mode = 0
def handler_interrupt(pin):
    global mode
    led.value(not led.value())
    if(mode<4):
        mode = mode + 1
    else:
        mode = 0
    print(mode)

def get_mode():
    button.irq(trigger=Pin.IRQ_FALLING,handler=handler_interrupt)
    return mode

while 1:
    if get_mode():
        break

while 1:
    mode = get_mode()
    if mode==1:
        #tracing()
        print("tracing mode")
    elif mode==2:
        #avoid_obstacle()
        print("avoid obstacle mode")
    else:
        #stop()
        print("stop mode")

```



## 第三课 ##

## motor ##

```Python
from machine import Pin,PWM
import time

def gpio_init():
    global motor1
    global motor2
    motor1 = Pin(15,Pin.OUT)
    motor2 = Pin(2,Pin.OUT)
    #led = Pin(22,Pin.OUT)

def simple_motor():
    gpio_init()
    motor1.value(0)
    motor2.value(1)
    #led.on()
    
def spin_clockwise():
    motor1.value(0)
    motor2.value(1)

def spin_anticlockwise():
    motor1.value(1)
    motor2.value(0)
    
def stop():
    motor1.value(0)
    motor2.value(0)
    
def smart_motor():
    gpio_init()
    spin_clockwise()
    time.sleep(10)
    spin_anticlockwise()
    time.sleep(10)
    stop()
```

## car ##

```python
from machine import Pin
import time

# 设置管脚PIN
motro_left1  = Pin(15,Pin.OUT)   
motro_left2  = Pin(2,Pin.OUT) 
motro_right1  = Pin(16,Pin.OUT) 
motro_right2  = Pin(4,Pin.OUT) 

#方向函数
def turn_left():
    motro_left1.value(0) # 输出高电平
    motro_left2.value(0)
    motro_right1.value(1) # 输出高电平
    motro_right2.value(0)
def turn_right():
    motro_left1.value(1) # 输出高电平
    motro_left2.value(0)
    motro_right1.value(0) # 输出高电平
    motro_right2.value(0)
def forward():
    motro_left1.value(1) # 输出高电平
    motro_left2.value(0)
    motro_right1.value(1) # 输出高电平
    motro_right2.value(0)
def backward():
    motro_left1.value(0) # 输出高电平
    motro_left2.value(1)
    motro_right1.value(0) # 输出高电平
    motro_right2.value(1)
def stop():
    motro_left1.value(0) # 输出高电平
    motro_left2.value(0)
    motro_right1.value(0) # 输出高电平
    motro_right2.value(0)
    
def smart_car():
    forward()
    time.sleep(5)
    stop()
    turn_left()
    time.sleep(1)
    stop()
    turn_right()
    time.sleep(1)
    stop()
    backward()
    time.sleep(5)
    stop()
```

## 红外使用 ##

```python
from machine import Pin
from time import sleep

infared = Pin(5,Pin.IN)
led = Pin(22,Pin.OUT)
while True:
    if infared.value()==0:   # 检测到障碍物
        print('检测到障碍物')
        led.on()
    else:
        print('没有检测到障碍物')
        led.on()
    sleep(1)

```



# 第四课 #

## pwm_motor ##

```python
from machine import Pin,PWM
import time

def setup():
    global motor1
    global motor2
    motor1 = PWM(Pin(15,Pin.OUT),freq=20000, duty=0)
    motor2 = PWM(Pin(2,Pin.OUT),freq=20000, duty=0)
def fast():
    motor1.duty(1023)
    motor2.duty(0)  
def slow():
    motor1.duty(768)
    motor2.duty(0)    
def acw():
    motor1.duty(0)
    motor2.duty(768)
def stop():
    motor1.duty(0)
    motor2.duty(0)

def smart_motor():
    setup()
    slow()
    time.sleep(10)
    fast()
    time.sleep(10)
    acw()
    time.sleep(10)
    stop()
```

## pwm_car ##

```python
from machine import Pin, PWM
from utime import sleep

# 设置管脚PIN
left1_pin  = 15   
left2_pin   = 2
right1_pin  = 16
right2_pin  = 4

def motor_setup():
    global motro_left1
    global motro_left2
    global motro_right1     
    global motro_right2
        
    motro_left1 = PWM(Pin(left1_pin), freq=20000, duty=0)  # 创建motor pwm对象，设置为输出模式 
    motro_left2 = PWM(Pin(left2_pin),freq=20000, duty=0)
    motro_right1 = PWM(Pin(right1_pin),freq=20000, duty=0)   
    motro_right2 = PWM(Pin(right2_pin),freq=20000, duty=0)
    
 #方向函数
def turn_left():
    motro_left1.duty(400) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(780) # 输出高电平
    motro_right2.duty(0)
def turn_right():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(400) # 输出高电平
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
    
def smart_car():
    slow_forward()
    sleep(5)
    #stop()
    fast_forward()
    sleep(5)
    #stop()
    turn_left()
    sleep(1)
    #stop()
    turn_right()
    sleep(1)
    #stop()
    backward()
    sleep(5)
    stop()

```

# class 5 #

## 避障小车 ##

```Python
from machine import Pin, PWM
from utime import sleep

# 设置管脚PIN
left1_pin  = 15   
left2_pin   = 2
right1_pin  = 16
right2_pin  = 4
avoid_left_pin = 26       #寻迹  22
avoid_right_pin = 25       #23

def motor_setup():
    global motro_left1
    global motro_left2
    global motro_right1     
    global motro_right2
        
    motro_left1 = PWM(Pin(left1_pin), freq=20000, duty=0)  # 创建motor pwm对象，设置为输出模式 
    motro_left2 = PWM(Pin(left2_pin),freq=20000, duty=0)
    motro_right1 = PWM(Pin(right1_pin),freq=20000, duty=0)   
    motro_right2 = PWM(Pin(right2_pin),freq=20000, duty=0)
#寻迹避障等gpio初始化
def gpio_setup():
    global avoid_left
    global avoid_right
    
    avoid_left = Pin(avoid_left_pin,Pin.IN)
    avoid_right = Pin(avoid_right_pin,Pin.IN)
 #方向函数
def turn_left():
    motro_left1.duty(400) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(780) # 输出高电平
    motro_right2.duty(0)
def turn_right():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(400) # 输出高电平
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

        
    
if __name__=='__main__':
    motor_setup()
    gpio_setup()
    while True:
        avoid_obstacle()


```

# 按键控制寻迹避障小车 #

```Python
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
    
```

# 红外遥控小车 #

**1、将一下代码下载至esp32开发板并命名为：myIRremote.py**

```python
# from machine import Pin
# import configs
import os
import machine
import utime
import micropython
import ujson
from machine import Pin, PWM
micropython.alloc_emergency_exception_buf(100)

'''
无重复：
[9047, 4488, 554, 573, 558, 626, 556, 599, 558, 598, 558, 599, 557, 600, 532,
625, 532, 624, 558, 1672, 582, 1624, 554, 1698, 534, 1693, 533, 1697, 558, 1648,
555, 1696, 559, 1670, 557, 1671, 558, 598, 559, 1670, 558, 599, 582, 550, 582,
598, 559, 1671, 532, 623, 557, 600, 586, 1614, 562, 624, 557, 1645, 584, 1672,
558, 1671, 559, 573, 557, 1696, 557]
有重复
[9072, 4492, 535, 601, 535, 600, 581, 571, 588, 596, 559, 572, 586, 596, 535,
622, 534, 597, 586, 1669, 581, 1669, 535, 1696, 585, 1644, 534, 1696, 559, 1670,
534, 1696, 558, 1673, 559, 1645, 610, 572, 560, 1670, 534, 629, 554, 570, 587,
573, 558, 1696, 559, 598, 533, 624, 558, 1671, 533, 623, 560, 1643, 588, 1642,
561, 1696, 533, 623, 560, 1671, 559, 39230, 9049, 2246, 583, 95490, 9027, 2265,
534, 95509, 9023, 2268, 559, 95482, 9014, 2269, 533, 95514, 9019, 2268, 585, 95443,
9041, 2268, 559, 95467, 9043, 2271, 531, 95495, 9043, 2247, 581, 95490, 9020,
2243, 559, 95517, 9043, 2246, 558, 95492, 9042, 2244, 559, 95492, 9017, 2268, 534, 
95490, 9046, 2269, 537, 95516, 9041, 2243, 535, 95517, 9089, 2152, 579, 95489,
9044, 2244, 585, 95492, 9025, 2269, 585]
'''

class IR(object):
    CODE = {162: "1", 98: "2", 226: "3", 34: "4", 2: "5", 194: "6", 224: "7", 168: "8", 144: "9",
            152: "0", 104: "*", 176: "#", 24: "up", 74: "down", 16: "left", 90: "right", 56: "ok"}

    def __init__(self, gpioNum):
        self.irRecv = machine.Pin(gpioNum, machine.Pin.IN, machine.Pin.PULL_UP)
        self.irRecv.irq(
             trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
             handler=self.__logHandler)

        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0        
        self.changed = False

    def __logHandler(self, source):
        thisComeInTime = utime.ticks_us()

        # 更新时间
        curtime = utime.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime
        

        if curtime >= 8500 and curtime <= 9500:
            self.ir_step = 1
            return

        if self.ir_step == 1:
            if curtime >= 4000 and curtime <= 5000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif curtime >= 2000 and curtime <= 3000:  # 长按重复接收
                self.ir_step = 3
                self.repeat += 1

        elif self.ir_step == 2:  # 接收4个字节
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start #记录最后ok的时间
                self.ir_step = 0

        elif self.ir_step == 3:  # 重复
            if curtime >= 500 and curtime <= 650:
                self.repeat += 1

        # elif self.ir_step == 4:  # 结束码，若果没有结束码有可能收到重复码再从step=1开始
        #     if curtime >= 500 and curtime <= 650:
        #         self.ir_step = 0

    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x+1]
            byte4 <<= 1
            if t >= 1800 and t <= 2800:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code

    def scan(self):        
        # 接收到数据
        if self.recived_ok:
            self.__check_cmd()
            self.recived_ok = False
            
        #数据有变化
        if self.cmd != self.cmd_last or self.repeat != self.repeat_last or self.t_ok != self.t_ok_last:
            self.changed = True
        else:
            self.changed = False

        #更新
        self.cmd_last = self.cmd
        self.repeat_last = self.repeat
        self.t_ok_last = self.t_ok
        #对应按钮字符
        s = self.CODE.get(self.cmd)
        return self.changed, s, self.repeat, self.t_ok

```

2、以下为main函数

```Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# －－－－极光编程－－－－
#  文件名：motor.py
#  版本：V2.0
#  author: Jessy
#  说明：智能小车实验
#####################################################
from machine import Pin, PWM
import machine
from utime import sleep
from myIRremote import IR

# 设置管脚PIN
left1_pin  = 13   
left2_pin   = 12
right1_pin  = 14   #5
right2_pin  = 27
avoid_left_pin = 26       #寻迹  22
avoid_right_pin = 25      #23
follow_left_pin = 33     #避障
follow_right_pin = 32
mode_pin = 35
IRremote_pin = 34
redLED_pin = 15
blueLED_pin = 2
yellowLED_pin = 4
#buzzer_pin = 33


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
    global led_yellow
    
    avoid_left = Pin(avoid_left_pin,Pin.IN)
    avoid_right = Pin(avoid_right_pin,Pin.IN)
    follow_left = Pin(follow_left_pin,Pin.IN,Pin.PULL_UP)
    follow_right = Pin(follow_right_pin,Pin.IN,Pin.PULL_UP)
    mode_button = Pin(mode_pin,Pin.IN,Pin.PULL_UP)
    led_red = Pin(redLED_pin,Pin.OUT)
    led_blue = Pin(blueLED_pin,Pin.OUT)
    led_yellow = Pin(yellowLED_pin,Pin.OUT)
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
def middle_forward():
    motro_left1.duty(840) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(840) # 输出高电平
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
        
def ir_control():
    stop()
    machine.freq(160000000)
    state = 0
    ir = IR(IRremote_pin)
    changed, s, repeat, ir_ok = ir.scan()
    if changed == True:
        if repeat >= 2:
            if s == 'up' and state != 1:
                state = 1
                slow_forward()          
                print("state1"," up")
            elif s == 'down' and state != 2:
                state = 2
                backward()        
                print("state2"," down")
            elif s == 'left' and state != 3:
                state = 3
                turn_left()         
                print("state3"," left")
            elif s == 'right' and state != 4:
                state = 4
                turn_right()       
                print("state4"," right")
    else:
        if state != 0:
            state = 0
            stop()         
            print("state0")
    sleep(0.2)
    
def led_show():
    if mode==1: #寻迹模式
        led_red.on()
        led_blue.off()
        led_yellow.off()
    elif mode==2: #避障模式
        led_red.off()
        led_blue.on()
        led_yellow.off()
    elif mode==3:
        led_red.off()
        led_blue.off()
        led_yellow.on()
    else:
        led_red.off()
        led_blue.off()
        led_yellow.off()
        
    
#通过红外模块获取方向
#红外传感器，二极管不断发射红外线，遇到白色反射回来，红外接收管饱和，输出低电平，否则输出高电平
#    (black line:1,white line:0)

def handler_interrupt(pin):
    global mode
    if(mode<3):
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
    elif mode==3:
        ir_control()
        led_show()
        print("IRremote control mode",end="\t")
    else:
        stop()
        led_show()
        break
        print("break",end="\t")
    
```

