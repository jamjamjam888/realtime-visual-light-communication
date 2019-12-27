#!/usr/bin/env python
#coding:utf-8

import cv2
import picamera
from time import sleep
from datetime import datetime
import numpy as np

#参照
#https://qiita.com/otakoma/items/04216c60fa31eae60947

#class呼び出し
cam = picamera.PiCamera()
now = datetime.now()
print(now)

#################################################
print("start capture")
#画像の大きさ
picture_width = 1080
picture_height = 1080
#撮影間隔
interval = 5

cam.resolution = (picture_width,picture_height)
cam.start_preview()
#camera warm-up
sleep(1)
now = datetime.now()
print(now)
#capture photo
print("撮影開始")

#カレントディレクトリ上に保存
cam.capture("initial.jpg")
print("撮影終了")
now = datetime.now()
print(now)

flame_ini = cv2.imread("/home/pi/initial.jpg",1)
print("読み出し終了")

print(type(flame_ini))
#表示
cv2.imshow("color1",flame_ini)

cv2.destroyAllWindows()
############################################################

#ペットボトルキャップ撮影
print("キャップ撮影開始")
cam.capture("val.jpg")
print("キャップ撮影終了")
frame_val = cv2.imread("val.jpg",1)

#差分検出
color_diff = cv2.absdiff(frame_val, flame_ini)
cv2.imwrite("/home/pi/color_diff.jpg",color_diff)


#画像を二値化+しきい値処理
gray_diff = cv2.cvtColor(color_diff, cv2.COLOR_BGR2GRAY)  # グレースケール変換
retval, black_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
cv2.imwrite("/home/pi/black_diff.jpg",black_diff)

#膨張処理関数を定義
def dilation(dilationSize, kernelSize, img):  #膨張した画像にして返す
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_RECT, (2 * dilationSize + 1, 2 * dilationSize + 1), (dilationSize, dilationSize))
    dilation_img = cv2.dilate(img, kernel, element)
    return dilation_img

dilation_img = dilation(3,3,black_diff)
cv2.imwrite("/home/pi/dilation_img.jpg",dilation_img)

#物体の重心座標(x,y)を計算し、円で囲う
#image, contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #境界線検出
contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
ball_pos = []

for i in range(len(contours)):  #重心位置を計算
        count = len(contours[i])
        area = cv2.contourArea(contours[i])  #面積計算
        x, y = 0.0, 0.0
        for j in range(count):
            x += contours[i][j][0][0]
            y += contours[i][j][0][1]

        x /= count
        y /= count
        x = int(x)
        y = int(y)
        ball_pos.append([x, y])
        
print(ball_pos)

###################
areas = []#符号器の輪郭だけを入れるための空のリスト
for cnt in contours:#cnt:輪郭#輪郭の数だけループする
    area = cv2.contourArea(cnt)#cv2.contourArea(cnt):領域が占める面積を計算
    if area > 900:#輪郭の面積が5000以上の場合、リストに追加する
        epsilon = 0.1*cv2.arcLength(cnt,True)
        #領域を囲む周囲長を計算する
        #第二引数は対象とする領域が閉じている(True)か単なる曲線かを表すフラグ
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        #approx:輪郭の近似を行う
        #第二引数は実際の輪郭と近似輪郭の最大距離を表し近似の精度を表すパラメータ
        areas.append(approx)

frame_val = cv2.imread("val.jpg",1)       
cv2.drawContours(frame_val,areas,-1,(0,0,255),1)
cv2.imwrite("/home/pi/drawContours_img.jpg",frame_val)