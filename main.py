#!/usr/bin/env python
#coding:utf-8

import cv2
import numpy as np

from pyueye_example_camera import Camera
from pyueye import ueye
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from time import sleep
import time
from datetime import datetime

from capture_camera_def_test import Decode



#----------------------------------------------------------
#capture_camera_def_test内のEncodeクラスを呼び出す
decode = Decode()
#-----------------------------------------------------------------
#topicを符号器に送信
decode.topic()

#-----------------------------------------------------------------
#符号器を撮影------------------------------------------------------
for capture in range(2):
    decode.main(1, capture)
    #引数1:撮影回数,引数2:mode.今は1

#画像読み出し+符号器の座標------------------------------------------------------
#areas:座標.これを以下の関数で返り値として利用する
#len(areas):符号器の数
areas = decode.imread()
print(areas)

#連続で撮影＋復号処理を行う
#loop:撮影回数かつ「復号処理回数
loops = 10
for loop in range(loops):
	print("loop"+str(loop))
	#同期のためにtopicを送信
	decode.topic()
	sleep(0.5)
	#点灯した符号パターンを撮影＋復号処理する
	#撮影
	decode.main(2, loop)
	#復号
	decode.imread_src(areas, loop)
    
    #--------------------------------------------------------------------------------
	"""
    #書き込みモードで開く
    #ユーザーのディレクトリに入っている
    f = open("output.txt", mode='a')
    f.write(str(i)+"\n") # 引数の文字列をファイルに書き込む
    f.close()
    """