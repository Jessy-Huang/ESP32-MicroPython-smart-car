# ESP32-MicroPython-smart-car
使用ESP32开发板、红外寻迹、红外避障、rgb小灯、红外遥控等实现的具有寻迹、避障、遥控三种模式的智能小车
 
 ## 开发平台
 Thonny  MicroPython开发
 开发工具见上传的安装包和串口工具
 
 ## 引脚接口(根据实际接线可以自定义)
'''Python
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
'''
