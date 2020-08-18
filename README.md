# B4-research
卒業研究の実験に用いたコード. 

## 実装

```
OpenCV4.1.1
python3.7.5
Raspberry Pi 3
Raspberry Pi 3 model B(Broker)
SenseHat(LED+環境センサ)
USBcamera
```

## 環境

### 共通ツール
```
MQTT通信(IoTゲートウェイ→IoT)
DOC(卒業研究内容)(IoT→IoTゲートウェイ)
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
ラズパイごとにtopicの調整や輝度値の調整などはする必要がある.

備考)
復号マスクは偶数番目にかけているが、複数の符号化開口マスクにして、組み合わせをさらに多重化することを検討してもいい

## コード
符号器側コード:continuous_encoder.py
復号器側コード:capture_camera_def_test.py(ライブラリ)  + main.py(実行ファイル)

## 注意

IPアドレスを指定しているtopic* の状態に注意.

IPアドレスと実際のラズペリーパイのIPアドレスは, IPアドレスの固定がうまくいっていないとエラーになる.

その場合, IPアドレスを固定した上でtopic(IPアドレス)の状態を変更する.
topic_pcがtopicを送信するエッジサーバーとなる.
topic_hostは中継サーバ(Broker)のIPアドレス.
