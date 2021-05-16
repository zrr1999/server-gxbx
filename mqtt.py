# -*- coding: utf-8 -*-
"""
Created on Sat May 15 09:14:28 2021

@author: jiawei zhang
"""
import datetime
import paho.mqtt.client as mqtt

client = mqtt.Client()


def connect():
    i = client.connect("test.ranye-iot.net", 1883, 60)
    if i == 0:
        print("connected")
    else:
        print("unconnected")
    client.subscribe("back")


connect()


# 连接服务器

def subscribe():
    def on_message(client, userdata, msg):
        print(msg.payload)
        with open("test.txt", "a") as f:
            f.write(str(datetime.datetime.now()) + str(msg.payload) + '\n')
        # 将锁的状态写入文件，锁开为open,关为close

    client.on_message = on_message
    client.loop_start()


subscribe()


# 订阅主题
# subscribe只需调用一次，便会一直执行，当收到信息后，打印并保存入文件

def publish(a, t):
    client.publish('send' + str(a), payload=str(t), qos=0, retain=False)
# 发送主题
# 参数a为冰箱地址，取1,2,3,4..目前只有一个取a=1
# 参数t为指令，t=1/2/3/4时，1/2/3/4号锁打开，并返回是否打开，将其打印,并写入文件
# t='a'/'b'/'c'/'d'时，查询1/2/3/4号锁状态，将其打印，并写入文件
