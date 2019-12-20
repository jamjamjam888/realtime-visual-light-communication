#!/usr/bin/env python
#coding:utf-8


import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import sys
import pprint

pprint.pprint(sys.path)

print("sys.path:",sys.path)

topic_pc = "172.16.120.130/lm75b-1/temp"
#topic1 = "172.16.120.228/lm75b-1/temp"
#topic2=
#topic3=
#topic4 = "172.16.120.159/lm75b-1/temp"
topic_camera = "172.16.120.88/lm75b-1/temp"
host = "172.16.120.148"


print("staring publishing query")
#publish.single(topic1,"111001",hostname=host)
publish.single(topic_pc,"111001",hostname=host)
print("finished publishing query")

print("wait sensor_info")
sensor_info = subscribe.simple(topic_pc, hostname=host, retained=False, msg_count=1)
print("get sensor_info")
#sensor情報をansに格納
ans = (sensor_info.payload)
print(ans)