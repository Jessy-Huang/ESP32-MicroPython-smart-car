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



   
    


