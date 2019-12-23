#coding: utf-8

#raspi recording_test

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from time import sleep

import cv2
import numpy as np
"""
from sense_hat import SenseHat
"""
import time
import picamera
import datetime
"""
sense = SenseHat()
"""
#class camera
cam = picamera.PiCamera()

now = datetime.datetime.now()
print(now)
#----------------------------------------------------------------

topic_pc = "172.16.120.130/lm75b-1/temp"
topic1 = "172.16.120.130/lm75b-1/temp"
#topic2 =
topic3 ="172.16.120.144/lm75b-1/temp"
#topic4 = 
#topic_camera = "172.16.120.228

host = "172.16.120.148"

#query choice-----------------------------------------------------
"""
msg=subscribe.simple(topic1, hostname=host, retained=False, msg_count=1)
print("msg.topic", msg.topic)
print("get query")
"""


"""
e=[0,0,0]
w=[255,255,255]
z3 = [e]*64
#z4 = [w]*64
z4 = [w,w,w,w,w,w,w,w,
      w,w,w,e,e,w,w,w,
      w,w,e,w,e,w,w,w,
      w,w,w,w,e,w,w,w,
      w,w,w,w,e,w,w,w,
      w,w,e,e,e,e,w,w,
      w,w,w,w,w,w,w,w,
      w,w,w,w,w,w,w,w,
    ]

#1
#点灯
sense.set_pixels(z4)
time.sleep(5)
sense.clear()
"""
now = datetime.datetime.now()
print(now)

print("start capture")
picture_width = 1080
picture_height = 1080
interval = 5

cam.resolution = (picture_width,picture_height)
cam.start_preview()
#camera warm-up

cam.start_recording("/home/pi/desktop/watanabe/video_test.h264")
cam.wait_recording(5)

cam.stop_recording()
cam.stop_preview()

#capture photo
#cam.capture("/home/pi/desktop/watanabe/test1.jpg")

print("finish capture")
now = datetime.datetime.now()
print(now)