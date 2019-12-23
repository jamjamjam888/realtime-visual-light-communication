#coding: utf-8

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from time import sleep

import cv2
import numpy as np
from sense_hat import SenseHat
import time
from datetime import datetime

import picamera()

sense = SenseHat()

cam = picamera.Picamera()
#----------------------------------------------------------------

topic1 = "172.16.120.130/lm75b-1/temp"
#topic2 =
#topic3 =
#topic4 = "172.16.120.130/lm75b-1/temp"

topic_pc = "172.16.120.228/lm75b-1/temp"
host = "172.16.120.148"

print("復号化を行います")

now=datetime.now()
print(now)


#query choice-----------------------------------------------------
"""
msg=subscribe.simple(topic1, hostname=host, retained=False, msg_count=1)
print("msg.topic", msg.topic)
print("Queryを受け取りました")

#------------------------------符号器検出
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
"""
###capture###
now=datetime.now()
print(now)
print("start capture")

camera_width =1000
camera_height =1000
cam.resolution=(camera_width,camera_height)
cam.start_preview()
#camera warm-up

cam.capture("/home/pi/デスクトップ/watanabe/image.jpg")
print("finish capture")

###video###
now=datetime.now()
print(now)
print("start video")

camera_width =1000
camera_height =1000
cam.resolution=(camera_width,camera_height)
cam.start_preview()
#camera warm-up

cam.start_recording("/home/pi/デスクトップ/watanabe/video.h264")
cam.wait_recording(5)

cam.stop_recording()
cam.stop_preview()

cam.capture("/home/pi/デスクトップ/watanabe/image.jpg")
print("finish video")
