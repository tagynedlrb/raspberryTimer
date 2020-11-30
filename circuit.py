import time
import RPi.GPIO as GPIO

# 전역 변수 선언 및 초기화
trig = 20
echo = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

def measureDistance():
        global trig, echo
        GPIO.output(trig, True) # 신호 1 발생
        time.sleep(0.00001) # 짧은시간후 0으로 떨어뜨려 falling edge를 만들기 위함             
        GPIO.output(trig, False) # 신호 0 발생(falling 에지)

        while(GPIO.input(echo) == 0):
                pass
        pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
        while(GPIO.input(echo) == 1):
                pass
        pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

        pulse_duration = pulse_end - pulse_start
        return 340*100/2*pulse_duration

# LED 점등을 위한 전역 변수 선언 및 초기화
led = 6 # 핀 번호 GPIO06 의미
GPIO.setup(led, GPIO.OUT) # GPIO 6번 핀을 출력 선으로 지정.

def controlLED(onOff): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
        GPIO.output(led, onOff)
