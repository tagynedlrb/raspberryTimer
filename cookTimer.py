import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import enum
import alarm
import sys

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.connect(broker_ip, 1883)
client.loop_start()

# LED 점등을 위한 전역 변수 선언 및 초기화
ledR1 = 5 # 핀 번호 GPIO5 의미
ledR2 = 6 # 핀 번호 GPIO6 의미
ledR3 = 23 # 핀 번호 GPIO23 의미

ledG = 24 # 핀 번호 GPIO24 의미

ledY1 = 12 # 핀 번호 GPIO12 의미
ledY2 = 13 # 핀 번호 GPIO13 의미
ledY3 = 16 # 핀 번호 GPIO16 의미
ledY4 = 19 # 핀 번호 GPIO19 의미
ledY5 = 26 # 핀 번호 GPIO26 의미

buttonM = 20 #MODE button
buttonS = 21 #SELECT button

#GPIO settings
def gpio_init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(ledR1, GPIO.OUT)
	GPIO.setup(ledR2, GPIO.OUT)
	GPIO.setup(ledR3, GPIO.OUT)
	GPIO.setup(ledG, GPIO.OUT)
	GPIO.setup(ledY1, GPIO.OUT)
	GPIO.setup(ledY2, GPIO.OUT)
	GPIO.setup(ledY3, GPIO.OUT)
	GPIO.setup(ledY4, GPIO.OUT)
	GPIO.setup(ledY5, GPIO.OUT)
	GPIO.setup(buttonM, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(buttonS, GPIO.IN, GPIO.PUD_DOWN)

tUnit = 1	#Unit differs on MODE
mode = 0
tNum = 0
alarmFlag = 1
timeLeft = 0

from enum import Enum
class Mode(Enum):
	MIN = 0
	MIN_10 = 1
	HOUR = 2

#MODE SELECT
def buttonPressedMODE(pin):
	global mode
	mode += 1
	mode %= 3
	if(mode == 0):
		GPIO.output(ledR1, 1)
		GPIO.output(ledR3, 0)
	elif(mode == 1):
		GPIO.output(ledR2, 1)
		GPIO.output(ledR1, 0)
	elif(mode == 2):
		GPIO.output(ledR3, 1)
		GPIO.output(ledR2, 0)

#TIME SELECT
def buttonPressedTIME(pin):
	global tNum
	tNum += 1
	tNum %= 10
	ledByTime(tNum)


# Confirm tUnit depending on mode
def confirmMODE(mode):
	global tUnit
	if(mode == Mode.MIN.value):
		tUnit = 60
	elif(mode == Mode.MIN_10.value):
		tUnit = 600
	elif(mode == Mode.HOUR.value):
		tUnit = 3600

# False Alarm flag when pressed
def buttonPressedALARM(pin):
	global alarmFlag
	alarmFlag = False

def publishTime(unit):
	global timeLeft
	cnt = 0
	while(cnt != unit):
		client.publish("CookTimer/time", timeLeft, qos=0)
		timeLeft -= 1
		cnt += 1
		time.sleep(1)
def ledAllUp():
		GPIO.output(ledG, 1)
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 1)
		GPIO.output(ledY3, 1)
		GPIO.output(ledY4, 1)
		GPIO.output(ledY5, 1)
def ledAllDown():
		GPIO.output(ledG, 0)
		GPIO.output(ledY1, 0)
		GPIO.output(ledY2, 0)
		GPIO.output(ledY3, 0)
		GPIO.output(ledY4, 0)
		GPIO.output(ledY5, 0)

# ledG, Y by time
def ledByTime(setTime):
	ledAllDown()
	if(setTime >= 5):       #if over 5 hour/min/sec
		GPIO.output(ledG, 1)
	else:
		GPIO.output(ledG, 0)

	tYellow = setTime%5
	if(tYellow >= 4):
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 1)
		GPIO.output(ledY3, 1)
		GPIO.output(ledY4, 1)
		GPIO.output(ledY5, 1)
	elif(tYellow >= 3):
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 1)
		GPIO.output(ledY3, 1)
		GPIO.output(ledY4, 1)
		GPIO.output(ledY5, 0)
	elif(tYellow >= 2):
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 1)
		GPIO.output(ledY3, 1)
		GPIO.output(ledY4, 0)
	elif(tYellow >= 1):
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 1)
		GPIO.output(ledY3, 0)
	elif(tYellow == 0):
		GPIO.output(ledY1, 1)
		GPIO.output(ledY2, 0)

try:
	gpio_init()
	ledAllDown()

	# Select MODE
	GPIO.output(ledR1, 1) # Start with Mode.MIN
	GPIO.add_event_detect(buttonM, GPIO.RISING, buttonPressedMODE, 200)
	GPIO.wait_for_edge(buttonS, GPIO.RISING)	#Waiting for MODE Confirm)
	GPIO.remove_event_detect(buttonM)
	confirmMODE(mode)

	print("mode ", mode, " selected") 
	time.sleep(1)

	# Select TIME
	GPIO.output(ledY1, 1) # Start with TIME 1
	GPIO.add_event_detect(buttonM, GPIO.RISING, buttonPressedTIME, 200)
	GPIO.wait_for_edge(buttonS, GPIO.RISING)	#Waiting for TIME Confirm)
	GPIO.remove_event_detect(buttonM)

	print("time ", (tNum+1), " selected") 

	# FOR TEST
	GPIO.output(ledG, 0)
	GPIO.output(ledY1, 0)
	GPIO.output(ledY2, 0)
	GPIO.output(ledY3, 0)
	GPIO.output(ledY4, 0)
	GPIO.output(ledY5, 0)

	timeLeft = tUnit * (tNum+1)
	print(timeLeft)
	#start Timer
	while(True):
		print(tUnit, tNum+1)
		ledByTime(tNum)
		if(tNum == 0):
			if(tUnit != 60):
				publishTime((tUnit-60))	
			alarm.alart_1min_left()	#1분전 알람
			print("ALARM")
			publishTime(60)	
			break	#break while
		publishTime(tUnit)
		tNum -= 1

	GPIO.cleanup()
	gpio_init()
	GPIO.add_event_detect(buttonS, GPIO.RISING, buttonPressedALARM, 200)

	#Alarm until button pressed
	while(alarmFlag):
		alarm.rooster()
		ledAllUp()
		time.sleep(1)
		ledAllDown()
		time.sleep(1)

	GPIO.remove_event_detect(buttonS)
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()

GPIO.cleanup()
client.loop_stop()
client.disconnect()
