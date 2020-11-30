import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sda = 2 # GPIO 핀 번호, sda라고 이름이 보이는 핀
scl = 3 # GPIO 핀 번호, scl이라고 이름이 보이는 핀
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c) # HTU21D 장치를 제어하는 객체 리턴

def getTemperature():
	return sensor.temperature # HTU21D 장치로부터 온도 값 읽기

