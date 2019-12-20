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

topic_pc = "172.16.120.130/lm75b-1/temp"
topic1 = "172.16.120.228/lm75b-1/temp"
#topic2=
#topic3=
topic4 = "172.16.120.159/lm75b-1/temp"
topic_camera = "172.16.120.88/lm75b-1/temp"
host = "172.16.120.148"

#各種関数
#topic関数
class Decode():
    def topic(self):
        #queryをブロードキャスト 
        publish.single(topic1,"111001",hostname=host)
        #Query:111011
        #sleep(1)
        #publish.single(topic4,"111001",hostname=host)
        publish.single(topic_pc,"111001",hostname=host)
        publish.single(topic_camera,"111001",hostname=host)

        from datetime import datetime
        print(datetime.now())
#-------------------------------------------------------------------------------------------
#カメラ関数
#引数1:capture:撮影回数
#引数2:mode:符号器検出用の画像=0,復号用の画像=1
    def main(self, mode, loop):
        # camera class to simplify uEye API access
            file_name = "C:\Users\owner\Desktop\watanabe\decoding_\input\capture"+str(mode)+"_"+str(loop)+".png"
            cam = Camera()
            cam.init()
            cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
            cam.set_aoi(0,0, 2500, 2500)
            cam.alloc()
            #print(ueye.is_GetImageMem(self.h_cam,buff.mem_ptr))
            cam.set_pixelclock()
            cam.set_framerate()
            cam.set_exposure()
            cam.capture_video()
            time.sleep(1)
            cam.image_file(file_name)
            cam.stop_video()
            cam.exit()

            print(datetime.now())
            print("capture")

#符号器検出---------------------------------------------------------------------------------------------------
    def imread(self):
    	img_src0 = cv2.imread("C:\Users\owner\Desktop\watanabe\decoding_\input\\capture1_0.png", 1) 
        img_src1 = cv2.imread("C:\Users\owner\Desktop\watanabe\decoding_\input\\capture1_1.png", 1) 
        #全点灯グレイスケール化
        gray0 = cv2.cvtColor(img_src0,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_gray0.png",gray0)
        print(gray0.shape)
        
        #全消灯グレイスケール化
        gray1 = cv2.cvtColor(img_src1,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_gray1.png",gray1)
        print(gray1.shape)

        #src0とsrc1の差分をとる
        img_diff = cv2.absdiff(gray1, gray0)
        cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_abs_gray.png",img_diff)
        #二値化
        ret,img = cv2.threshold(img_diff,#入力画像
                                200,#閾値
                                255,#画素値の最大値
                                cv2.THRESH_BINARY)#2値化のType

        #処理画像を出力↓
        cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_capture_binary.png",img)

        #cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_capture_bitwise.png",img)
        #operator
        operator = np.ones((3, 3), np.uint8)
        #膨張処理
        img = cv2.dilate(img, operator,iterations=4)
        #収縮処理
        img = cv2.erode(img,operator, iterations=3)

        #矩形検知
        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #img:出力画像
        #contours:検出した全輪郭をpythonのリストとして出力する。len(contours)が矩形の数と対応する
        #hierarchy:輪郭の数と階層情報を出力

        # cv2.RETR_EXTERNAL:一番外の輪郭を抽出する
        # cv2.RETR_TREE:入れ子
        # cv2.RETR_LIST:同じ階層の輪郭が取得
        # cv2.RETR_CCOMP:内部輪郭と外部輪郭両方を抽出
        # cv2.CHAIN_APPROX_NONE:輪郭上のすべての点の情報を保持する
        # cv2.CHAIN_APPROX_SIMPLE:輪郭の端点を保持する。メモリの使用量が減るのでこちらのほうが好ましい

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
        return areas
#---------------------------------------------------------------------------------------------------------------------------------------------
#符号点灯を撮影＋二値化
    def imread_src(self, areas, loop):#coordinate:座標。上記の返り値areasと同じ.loopで決定する
        #符号パターンも二値化
        src = cv2.imread("C:\Users\owner\Desktop\watanabe\decoding_\input\\capture2_"+str(loop)+".png", 1) 
        ret,thre_src = cv2.threshold(src,#入力画像
                                    100,#閾値
                                    255,#画素値の最大値
                                    cv2.THRESH_BINARY)#2値化のType

        #BGRの順で並ぶことに注意
        cv2.drawContours(thre_src,areas,-1,(0,0,255),1)
        cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_capture_contours_src.png",thre_src)

        #k = 矩形の数(符号器の数)
        k = len(areas)          
        M = np.zeros((k,3,3))
        #3×3ですべての値が0の行列をk(符号器の数)だけ作る
        for i in range(k):#矩形の数だけ繰り返す繰り返す
            if len(areas[i]) == 4: #これはたぶん矩形かどうかの判定
                ar = areas[i]
                #print("ar:{}".format(ar))#4点の抽出
                ar = ar.reshape(4,2)
                #print("ar.reshape:{}".format(ar))#4点の抽出
                #列順に並べる
                ar = ar[ar[:,0].argsort(),:]
                #print("ar.argsort:{}".format(ar))#
                #射影変換前の図形
                pts1 = np.float32(ar)
                #射影変換後の図形
                pts2 = np.float32([[0,0],[0,64],[64,0],[64,64]])
                #変換行列を計算
                M[i] = cv2.getPerspectiveTransform(pts1,pts2)
                dst=[]
                #画像を変形
                dst = cv2.warpPerspective(thre_src,M[i],(64,64))
                cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\dst_1_"+str(2+i)+".png",dst)
                #grayにする
                gray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
                cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\dst_gray_1_"+str(2+i)+".png",gray)
                #dstを二値化する
                ret,dst_thre = cv2.threshold(gray,#入力画像
                                            150,#閾値
                                            255,#画素値の最大値
                                            cv2.THRESH_BINARY)#2値化のType
                cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\dst_thre_1_"+str(2+i)+".png",dst)
        
        for kk in range(k):
            dst = cv2.imread("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\dst_thre_1_"+str(2+kk)+".png",1)
            w=int(dst.shape[0]/8)#img.shape[0]:画像の縦列
            h=int(dst.shape[1]/8)#img.shape[1]:画像の横列

            dst1 = dst[w:8*w,h:8*h]#右下切り取り　1LED左上　
            dst2 = dst[w:8*w,0:7*h]#左下切り取り　1LED左
            dst3 = dst[0:7*w,h:8*h]#右上切り取り　1LED上
            dst4 = dst[0:7*w,0:7*h]#左上切り取り　これを基本とする
            #XORはdst2とdst3を選択
            imgc1 = dst2#[左下7*7画像]
            imgc2 = dst3#[右上7*7画像]
            img_weighted = cv2.addWeighted(imgc1, 0.5, imgc2, 0.5, 0)
            img = np.array(img_weighted)
            for i in range(int(3)):#横縞#3回
                cv2.rectangle(img, (0, h*(2*i+1)), (8*h, h*(2*i+2)), (0, 0, 0), thickness=-1)
            for j in range(int(3)):#縦縞
                cv2.rectangle(img, (w*(2*j+1), 0), (w*(2*j+2), 8*w), (0, 0, 0), thickness=-1)
            cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\hugouka_mask_"+str(2+kk)+".png", img)
################################################################################################################################

        for hukugou in range(k):#符号器の数繰り返す
        #画像の読み出し
            img = cv2.imread("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\hugouka_mask_"+str(2+hukugou)+".png",1)
            for delete in range(3):#なんかよくわからんけど3ならうまくいく
                #8画素ずつマスクをしたところを切り出していく
                img = np.delete(img,np.s_[8*(delete+1):8*(delete+1)+8], axis=0) #列(要素)の消去
                #img = np.delete(img,np.s_[0*w:8*w:3*w], axis=0)
                img = np.delete(img,np.s_[8*(delete+1):8*(delete+1)+8], axis=1) #行の消去

            ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            #閾値を100にしている。ノイズが多い場合は変更する必要あり。
            cv2.imwrite('C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\hukugou_pxl_1_0_'+str(2+hukugou)+'.png', img)
            decode=[]
            #for i in range(1):
            for i in range(4):#4行あるうち、出力する行の数#長いので今は2行まで
                for j in range(4):#4列
                    mean=np.mean(img[8*i:8*(i+1)-1,8*j : 8*(j+1)-1])
                    if mean<50:
                    	mean = 0
                        decode.append(mean)
                    else:
                    	mean = 1
                    	decode.append(mean)
            #output:2bit→符号器番号,2bit→パラメータの指定番号,12bit→センサ情報
            prefix = decode[0:2:1]#[0,0][0,1][1,0][1,1]の4通り
            params = decode[2:4:1]#te=[0,1],pr=[1,0],hu=[1,1]
            sensor = decode[4:16:1]
            
            output=[]
            #符号器番号
            if prefix == [0,0]:
                output.append(0)
            elif prefix == [0,1]:
                output.append(1)
            elif prefix == [1,0]:
                output.append(2)
            elif prefix == [1,1]:
                output.append(3)
            else:
                output.append("error")


            #パラメータ指定番号
            if params == [0,1]:
                output.append("te")
            elif params == [1,0]:
                output.append("pr")
            elif params == [1,1]:
                output.append("hu")
            else:
                output.append("error")

            #sensor:2進数→10進数
            sensor_2 = str()
            for x in range(len(sensor)):
                sensor_2 += str(sensor[x])
            sensor_10 = int(sensor_2,2)
            output.append(sensor_10)

            print(output)

            f = open("output.txt", mode='a')
            f.write(str(hukugou)+str(output)+"\n") # 引数の文字列をファイルに書き込む
            f.close()
            print("finish decode loading")

        """
        #mqtt通信がうまくいかないので、いったんあきらめる
        #sensor情報を取得

        print("wait sensor_info")
        sensor_info = subscribe.simple(topic_pc, hostname=host, retained=False, msg_count=1)
        #sensor情報をansに格納
        ans = (sensor_info.payload)
        print("get sensor_info")
        print(ans)
        #print(str(hukugou),output
        #符号器の番号とoutputを書き込む
        """
