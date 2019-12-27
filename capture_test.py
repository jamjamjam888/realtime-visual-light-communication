#!/usr/bin/env python
#coding:utf-8

#ラズパイカメラをマウントしてusbカメラにするコマンド
#sudo modprobe bcm2835-v4l2

#usbカメラで動かすことに成功

import time
import math
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    #VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()

    #加工なし画像を表示する
    cv2.imshow('Raw Frame', frame)

    #キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
"""
# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
"""