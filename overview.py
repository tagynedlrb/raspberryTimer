import time
import RPi.GPIO as GPIO
import enum

	#GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

#TIME SELECT
def buttonPressedTIME(pin):
	global tNum
	tNum += 1
	tNum %= 10
#GPIO.cleanup()

# Select MODE
GPIO.add_event_detect(buttonM, GPIO.RISING, buttonPressedMODE, 200)
GPIO.wait_for_edge(buttonS, GPIO.RISING)	#Waiting for MODE Confirm)
GPIO.remove_event_detect(buttonM)

# Confirm tUnit depending on mode
def confirmMODE(mode):
	global tUnit
	if(mode == Mode.MIN):
		tUnit = 60
	elif(mode == Mode.MIN_10):
		tUnit = 600
	elif(mode == Mode.HOUR):
		tUnit = 3600
confirmMODE(mode)

print("mode ", mode, " selected") 
print("tUnit ", tUnit)

# Select TIME
GPIO.add_event_detect(buttonM, GPIO.RISING, buttonPressedTIME, 200)
GPIO.wait_for_edge(buttonS, GPIO.RISING)	#Waiting for TIME Confirm)
GPIO.remove_event_detect(buttonM)

print("time ", (tNum+1), " selected") 

#start Timer
while(True):

	print(tUnit, tNum)
	if(tNum >= 5):	#if over 5 hour/min/sec
		GPIO.output(ledG, 1)
#	else:
#		GPIO.output(ledG, 0)
	
	tYellow = tNum%5
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
		if(tUnit != 60 and tUnit != 1):
			time.sleep((tUnit-60)) #last LED
	#	alarm	#1분전 알람
		GPIO.cleanup()	#This CODE is for TEST
		print("ALARM")
		time.sleep(60)
#		GPIO.cleanup()	#REAL CODE
		break	#break while
	
	time.sleep(1*tUnit)
	tNum -= 1

'''
while(버튼을 누를때까지):
	alarm()	// finish alarm

	if( 21 button pressed ):
		stop alarm()
		break
	
'''
