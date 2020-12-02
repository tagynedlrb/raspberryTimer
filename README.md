전체 구성


LED(9개) - GPIO5, GPIO6, GPIO23, GPIO24,
GPIO12, GPIO13, GPIO16, GPIO19, GPIO26

5,6,23 => RED	[MODE]
24 => GREEN	[5]
12, 13, 16, 19, 26 => YELLOW	[1]

스위치(2개) - GPIO20, GPIO21 

20 => [MODE]
21 => [SELECT]

온습도 센서 – SDA(GPIO2), SCL(GPIO3)
블루투스 스피커 => 1분전 알람, 종료 알람(닭소리)

mqtt Topic : CookTimer/#
CookTimer/temperature
CookTimer/time
CookTimer/image
등

[사용 방법]
mosquitto -c /etc/mosquitto/mosquitto.conf
python3 mqtt.py &
python3 app.py &
python3 cookTimer.py
