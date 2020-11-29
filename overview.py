import time
import RPi.GPIO as GPIO

# LED 점등을 위한 전역 변수 선언 및 초기화
led = 6 # 핀 번호 GPIO6 의미

tUnit = 1	#Unit differs on MODE

'''
def measureDistance():
	global trig, echo

	while(GPIO.input(echo) == 0):
		pass
	pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
	while(GPIO.input(echo) == 1):
		pass
	
	pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림
	pulse_duration = pulse_end - pulse_start
	return 340*100/2*pulse_duration

GPIO.setup(led, GPIO.OUT) # GPIO 6번 핀을 출력 선으로 지정.

def controlLED(onOff): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
	GPIO.output(led, onOff)
'''

#MODE SELECT

while(True){	# Setup Mode

20번 눌림
	mode++ % 3
MODE1
	tUnit = 60
MODE2
	tUnit = 60*10
MODE3
	tUnit = 60*60

21번 눌림 => break;

}


#start Timer
while(True){

if(time >= 5)	//	if over 5 hour/min/sec
	GREEN UP

tYellow = time%5 If ( tYellow >= 4 )
	YELLOW 5 UP
If ( tYellow >= 3 )
	YELLOW 4 UP
If ( tYellow >= 2 )
	YELLOW 3 UP
If ( tYellow >= 1 )
	YELLOW 2 UP

if(time == 0){
	YELLOW 1 UP
	sleep(tUnit-60) //	last LED
	alarm	//1분전 알람
	sleep(60)
	break	//break while
}
else{
	sleep(1*tUnit)
	time—
}

}

while(버튼을 누를때까지){
	alarm()	// finish alarm

	if( 21 button pressed ){
		stop alarm()
		break
	}
}
