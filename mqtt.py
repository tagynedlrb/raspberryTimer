# publisher

import time
import paho.mqtt.client as mqtt
import temperature # 온습도 센서 입력 모듈 임포트
import myCamera # 카메라 사진 보내기

flag = False # True이면 "action" 메시지를 수신하였음을 나타냄

def on_connect(client, userdata, flag, rc):
	client.subscribe("CookTimer/#", qos = 0)

def on_message(client, userdata, msg) :
	global flag
	command = msg.payload.decode("utf-8")

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

while(True):
	temp = temperature.getTemperature()
	client.publish("CookTimer/temperature", temp, qos=0)

	imageFileName = myCamera.takePicture() # 카메라 사진 촬영
	client.publish("CookTimer/image", imageFileName, qos=0)
	time.sleep(1)
client.loop_stop()
client.disconnect()
