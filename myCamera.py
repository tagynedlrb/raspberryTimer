import os
import io
import time
import picamera
import cv2
import numpy as np

# 전역 변수 선언 및 초기화
fileName = ""

camera =  picamera.PiCamera()
camera.resolution = (320, 240)
time.sleep(1) # 카메라 워밍업

def takePicture() :
	global fileName
	global camera

	# 이전에 만들어둔 사진 파일이 있으면 삭제
	if len(fileName) != 0:
		os.unlink(fileName)

        
	camera.start_preview() # 연결된 모니터에 보이도록 하기 위함
	time.sleep(0) # 사용자가 카메라  앞에서 얼굴 들이미는 동안 시간 주기
	camera.stop_preview()

	takeTime = time.time()
	fileName = "./static/%d.jpg" % (takeTime * 10)
	camera.capture(fileName, format='jpeg', use_video_port=True)
	return fileName

if __name__ == '__main__' :
	takePicture()

if __name__ == 'myCamera' :
	pass

