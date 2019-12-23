#coding: utf-8

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from time import sleep

import cv2
import numpy as np
from sense_hat import SenseHat
import time
sense = SenseHat()

#----------------------------------------------------------------

topic_pc = "172.16.120.130/lm75b-1/temp"
topic1 = "172.16.120.228/lm75b-1/temp"
host = "172.16.120.148"

print("符号化を行います")
from datetime import datetime
now=datetime.now()
print(now)

#file書き込み
f = open("/home/pi/Desktop/sensor_info.txt",mode ="a")
f.write(str(now) +"\n")
print("書き込み完了")
#query choice-----------------------------------------------------

msg=subscribe.simple(topic1, hostname=host, retained=False, msg_count=1)
print("msg.topic", msg.topic)
print("Queryを受け取りました")

#------------------------------符号器検出
e=[0,0,0]
w=[255,225,225]
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

#消灯
time.sleep(5)
#符号器の番号を割り当てる--------------------------------------------------------
#prefix=01
prefix=[0,1]
print("prefix",prefix)

#sensor------------------------------------------------------------------------
#count数

#複数回topic+センサ情報取得
loops = 10
for loop in range(loops):
   
    print("loop",loop)
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    #取得した情報をint型にする
    te = int(t)
    pr = int(p)
    hu = int(h)
    
    #sensor_infoにセンサ情報を格納。あとでPCに送信する
    sensor_info = [te,pr,hu]
    #情報を出力
    print("temperature",te)
    print("pressure",pr)
    print("humidity",hu)

    #先頭に0bのついたバイナリデータをリストで取得
    te=list(bin(te))
    #print("te_binarydata",te)
    te=np.array(te)
    #print("te_np.array",te)
    #リストを配列のように使うと遅くなるので一般にnp.arrayにするのがよい

    #先頭の0bを除いたバイナリデータ
    b1=te[2:]
    #リストで取得しなおす
    b1 = [int(i) for i in b1]
    #print("b1",b1)
    
    pr=list(bin(pr-1000))
    pr=np.array(pr)
    b2=pr[2:]
    b2 = [int(i) for i in b2]
    #print("b2",b2)

    hu=list(bin(hu))
    hu=np.array(hu)
    b3=hu[2:]
    b3 = [int(i) for i in b3]
    #print("b3",b3)
    
    ##b = np.insert(b1,len(b1),b3) #te & hu

    #prefixに¥センサ情報を結合させる------------------------------------
    #ついでに温度、圧力、湿度のprefixもくっつける
    te_prefix = [0,1]
    pr_prefix = [1,0]
    hu_prefix = [1,1]
    
    prefix1 = prefix + te_prefix + [0]*(12-len(b1))
    prefix2 = prefix + pr_prefix + [0]*(12-len(b2))
    prefix3 = prefix + hu_prefix + [0]*(12-len(b3))

    b1 = prefix1 + b1
    b2 = prefix2 + b2
    b3 = prefix3 + b3

    print("b1",b1)
    print("b2",b2)
    print("b3",b3)
    #query choice-----------------------------------------------------

    #msg=subscribe.simple(topic1, hostname=host, retained=False, msg_count=1)
    s1 = list(msg.payload)
    print("s1(Query)",s1)

    #Queryで渡される値。Publisher側で指定している
    a = [int(i) for i in s1]
    print("a",a)

    #温度のQuery
    a1 = a[0:2]
    #圧力のQuery
    a2 = a[2:4]
    #湿度のQuery
    a3 = a[4:6]

    #aのprefix.bと桁合わせするためのもの
    prefix_a = [0]*14

    a1 = a1 + prefix_a
    a2 = a2 + prefix_a
    a3 = a3 + prefix_a

    #----------------------------------------------------------------

    #a,b cahange into x,y--------------------------------------------
    def input(X,Y):
        #Query aの長さ
        lswt = len(a)
    
    #aと同じ長さの行列を作成する。ここではそれぞれ1×6行列
        a_ = np.zeros(lswt,dtype=np.int)
        b_ = np.zeros(lswt,dtype=np.int)
        x = np.zeros(lswt,dtype=np.int)
        y = np.zeros(lswt,dtype=np.int)
    
    #a_に変換.1と0を反転させる   
        for i in range(lswt):
            if a[i]==0:
                a_[i]=1
            elif a[i]==1:
                a_[i]=0    
            
    #b_に変換
        for i in range(lswt):
            if b[i]==0:
                b_[i]=1
            elif a[i]==1:
                b_[i]=0 
            
    #x生成 (a*b)
    #np.logical_and(a,b):a and b と同じ。and演算。
        c = np.logical_and(a,b)
    
    #and演算の結果が1だったら1を返す
        for i in range(lswt):
            if c[i]==True:
                x[i]=1
            elif c[i]==False:
                x[i]=0
            
    #y生成 (a_*b)
        c = np.logical_and(a_,b)
        for i in range(lswt):
            if c[i]==True:
                y[i]=1
            elif c[i]==False:
                y[i]=0
                
        x = np.reshape(x,(1,lswt))
        y = np.reshape(y,(1,lswt)) 
        #print("x:",x)
        #print("y:",y)
        return x,y,lswt

    #--------------------------------符号化画像を生成
    e=[0,0,0]

    l=np.array([[0,0,0] for i in range(64)])
    #print(l)

    #中西さんのアドバイスにもとづいて実装
    #符号長の長さだけ行う
    #------------------------R-------------------------
    a=a1
    b=b1
    input1 = input(a,b)

    x1=input1[0].tolist()
    y1=input1[1].tolist()

    #print("x1:",x1)
    #print("y1:",y1)
    ls1=input1[2]
    #print("ls1:",ls1)

    x1=x1[0]
    y1=y1[0]

    for i in range(ls1):
    #LED上の配列をここで指定
        index = i//4
    #iを4で割ったときの商。これに8をかければLEDの点灯箇所を指定できる。ここで、iは入力X,Yの符号長ということに注意。
    #また最大値は3(4かも?)になる。これは1bitを表すのに2*2の符号化画像を使うので、4*16=64で、8*8のLEDアレイと一致する    
        r=220
    #左上
        if x1[i]==0 and y1[i]==0:
            l[2*i + index*8][0]=r
        
    #右上
        if x1[i]==0 and y1[i]==1:
            l[2*i + index*8+1][0]=r
     
    #左下
        if x1[i]==1 and y1[i]==0:
            l[2*i + index*8+8][0]=r

    #右下
        if x1[i]==1 and y1[i]==1:
            l[2*i + index*8+9][0]=r
        
    #次の2*2の符号化画像アレイに移る
    #print(l)
    #----------------G------------------------------
    a=a2
    b=b2
    input2 = input(a,b)
    
    x2=input2[0].tolist()
    y2=input2[1].tolist()
    ls2=input2[2]
    
    x2=x2[0]
    y2=y2[0]
    
    #print("ls2:",ls2)

    for i in range(0,ls2):
    #LED上の配列をここで指定
        index = i//4
    #iを4で割ったときの商。これに8をかければLEDの点灯箇所を指定できる。ここで、iは入力X,Yの符号長ということに注意。
    #また最大値は3(4かも?)になる。これは1bitを表すのに2*2の符号化画像を使うので、4*16=64で、8*8のLEDアレイと一致する    
        g=150
    #左上
        if x2[i]==0 and y2[i]==0:
            l[2*i + index*8][1]=g
    
    #右上
        if x2[i]==0 and y2[i]==1:
            l[2*i + index*8+1][1]=g
     
    #左下
        if x2[i]==1 and y2[i]==0:
            l[2*i + index*8+8][1]=g

    #右下
        if x2[i]==1 and y2[i]==1:
            l[2*i + index*8+9][1]=g
    
    
    #------------------B---------------------------------------
    a=a3
    b=b3
    input3 = input(a,b)

    x3=input3[0].tolist()
    y3=input3[1].tolist()
    ls3=input3[2]

    x3=x3[0]
    y3=y3[0]

    for i in range(0,ls3):
    #LED上の配列をここで指定
        index = i//4
    #iを4で割ったときの商。これに8をかければLEDの点灯箇所を指定できる。ここで、iは入力X,Yの符号長ということに注意。
    #また最大値は3(4かも?)になる。これは1bitを表すのに2*2の符号化画像を使うので、4*16=64で、8*8のLEDアレイと一致する    
        b=120
    #左上
        if x3[i]==0 and y3[i]==0:
            l[2*i + index*8][2]=b
        
    #右上
        if x3[i]==0 and y3[i]==1:
            l[2*i + index*8+1][2]=b
     
    #左下
        if x3[i]==1 and y3[i]==0:
            l[2*i + index*8+8][2]=b

    #右下
        if x3[i]==1 and y3[i]==1:
            l[2*i + index*8+9][2]=b
    
    #-----------------------------------------------
    tolist_l=l.tolist()
    #print(tolist_l)

    #reverseする
    sense.set_pixels(tolist_l)

    time.sleep(5)
    sense.clear()
    print("符号パターン消灯")
    
    f = open("/home/pi/Desktop/sensor_info.txt",mode ="a")
    f.write(str(sensor_info)+"\n")
    print("書き込み完了")
    """
    #mqtt通信がうまくいかないのでいったん諦める
    #sensor_infoをPCに送信ホントはwhile文とかにしたほうがいい
    print("sensor_info",sensor_info)
    print("sensor_infoを送信します")
    b=11011
    publish.single(topic_pc,b,hostname=host)
    print("sensor_infoを送信しました")
    
    """