#!/usr/bin/env python
#coding:utf-8

import cv2
import numpy as np

from pyueye_example_camera import Camera
from pyueye import ueye
import paho.mqtt.publish as publish
from time import sleep
import time
from datetime import datetime
from capture_camera_def_test import Decode

#capture_camera_def_test内のEncodeクラスを呼び出す
decode = Decode()

#符号器を検出するために一度topicを送信する
decode.topic()

#ここのsleep時間は符合器の全点灯+全消灯の時間に準ずる
sleep(10)

#連続撮影＋復号を行う------------------------------------------------------------
#topicを符号器に送信
loop = 10
for i in range(loop):
    decode.topic()
    print("publish Query")
    sleep(5)