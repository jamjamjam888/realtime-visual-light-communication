# B4-research
卒業研究の実験に用いたコード. OpenCVとpython2.

## 環境

### 共通ツール
```
MQTT通信
DOC(卒業研究内容)
```

### 復号器側(Publisher, IoTゲートウェイ)

```
PC:Windows8
Editor:Sublime Text
ソフトウェア:OpenCV3.4.3
言語:python2
カメラ:USBcamera
```

### 符号器側(Subscriber, エッジ(IoT)デバイス)
```
符号器:Raspberry Pi 3
OS:Raspbian(=Raspberry Pi OS)(based on Debian)
センサ:SenseHat(Raspberry Pi拡張モジュール)
Editor:Thonny
言語:python2
```

### 仲介サーバ(Broker)
```
Raspberry Pi 3 model B
```

## 注意事項

画像の書き込み・読み出しは絶対パスで指定しているので注意.

## memo 
moment_detect.pyとRGB_reverse_coding.pyが基本的には完成コード.
ラズパイごとにtopicの調整や輝度値の調整などはする必要がある.

備考)
復号マスクは偶数番目にかけているが、複数の符号化開口マスクにして、組み合わせをさらに多重化することを検討してもいい
