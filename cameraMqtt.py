# publisher/subscriber

import time
import paho.mqtt.client as mqtt
import myCamera # 카메라 사진 보내기

flag = False # True이면 "action" 메시지를 수신하였음을 나타냄

def on_connect(client, userdata, flag, rc):
	client.subscribe("facerecognition", qos = 0)

def on_message(client, userdata, msg) :
	global flag
	command = msg.payload.decode("utf-8")
	if command == "action" :
		print("action msg received..")
		flag = True

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

while True :
	if flag==True : # "action" 메시지 수신. 사진 촬영
		imageFileName = myCamera.takePicture() # 카메라 사진 촬영
		print(imageFileName)
		client.publish("image", imageFileName, qos=0)
		flag = False
	time.sleep(1)
	print("time...", end=" ")
	print(flag)

client.loop_end()
client.disconnect()

