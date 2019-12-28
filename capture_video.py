#!/usr/bin/env python
#coding:utf-8

#ラズパイカメラをマウントしてusbカメラにするコマンド
#sudo modprobe bcm2835-v4l2

#usbカメラで動かすことに成功

from time import sleep
import math
import cv2
import numpy as np
from datetime import datetime

cap = cv2.VideoCapture(0)

#backgroundを任意のタイミングで撮影する
while True:
    ret, frame = cap.read()
    gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("background_capture", gray_background)

    k = cv2.waitKey(1)&0xff # キー入力を待つ
    if k == ord('p'):
        # 「p」キーで画像を保存
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = "/home/pi/" + "background" + date + ".png"
        cv2.imwrite(path, frame) # ファイル保存

        cv2.imshow(path, frame) # キャプチャした画像を表示
        break
    #elif k == ord('q'):
        # 「q」キーが押されたら終了する
        break
# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()

###########################################################################################

#backgroundを読み込む
background = cv2.imread("/home/pi/background" +date+ ".ping",1)
#gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

#フレーム間差分を計算
cap = cv2.VideoCapture(0)
while (True):
    #VideoCaptureから1フレーム読み込む
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    #加工なし画像を表示する
    #cv2.imshow('Raw Frame', frame1)
    #加工ありの画像を表示    
    cv2.imshow('Gray Frame',gray1)
    
    #差分検出
    color_diff_ini = cv2.absdiff(gray1, gray_background)

    retval, black_diff = cv2.threshold(color_diff_ini, 130, 255, cv2.THRESH_BINARY)
    
    #加工ありの画像を表示    
    cv2.imshow('black_diff',black_diff)
    
    #キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
print("終了")
################################################
