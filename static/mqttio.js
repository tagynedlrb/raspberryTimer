var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음

function startConnect() { // 접속을 시도하는 함수
	// 랜덤한 사용자 ID 생성
	clientID = "clientID-" + parseInt(Math.random() * 100);

	// 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
	broker = document.getElementById("broker").value; // 브로커의 IP 주소

	// id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
	// MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
	client = new Paho.MQTT.Client(broker, Number(port), clientID);

	// client 객체에 콜백 함수 등록
	client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
	client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록

	// 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}로서, 객체의 프로퍼틴느 onSuccess이고 그 값이 onConnect.
	// 접속에 성공하면 onConnect 함수를 실행하라는 지시
	client.connect({
		onSuccess: onConnect,
	});
	subscribe('CookTimer/#');
		
}

var isConnected = false;

function onConnect() { // 브로커로의 접속이 성공할 때 호출되는 함수
	isConnected = true;

	//document.getElementById("messages").innerHTML += '<span>Connected</span><br/>';
}

var topicSave;
function subscribe(topic) {
	if(client == null) return;
	if(isConnected != true) {
		topicSave = topic;
		window.setTimeout("subscribe(topicSave)", 500);
		return
	}
	// 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
	client.subscribe(topic); // 브로커에 subscribe
}
function publish(topic, msg) {
	if(client == null) return; // 연결되지 않았음
	client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
	if(client == null || isConnected != true) return;

	// 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
	document.getElementById("messages").innerHTML += '<span>Unsubscribing to: ' + topic + '</span><br/>';

	client.unsubscribe(topic, null); // 브로커에 subscribe
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
	document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
	if (responseObject.errorCode !== 0) {
		document.getElementById("messages").innerHTML += '<span>오류 : ' + responseObject.errorMessage + '</span><br/>';
	}
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
	console.log("onMessageArrived: " + msg.destinationName +" | "+ msg.payloadString);

    // 토픽 image가 도착하면 payload에 담긴 파일 이름의 이미지 그리기
    if(msg.destinationName == "CookTimer/image") {
            drawImage(msg.payloadString); // 메시지에 담긴 파일 이름으로 drawImage() 호출. drawImage()는 웹 페이지에 있음
    }
	else if(msg.destinationName == "CookTimer/time"){
		var clock = document.getElementById("clock");
		var time = parseInt(msg.payloadString);
		var currentHours = addZeros(parseInt(time/3600), 2); 
		time %= 3600;
		var currentMinute = addZeros(parseInt(time/60), 2);
		time %= 60;
		var currentSeconds = addZeros(parseInt(time), 2);

		if(currentSeconds >= 50){// 50초 이상일 때 색을 변환해 준다.
			currentSeconds = '<span style="color:#de1951;">'+currentSeconds+'</span>';
		}
		clock.innerHTML = currentHours+":"+currentMinute+":"+currentSeconds; //시간 출력
		 
		if(msg.payloadString == '0')
			play();
	}

	else if(msg.destinationName == "CookTimer/alarm"){
		pause();
	}
	// 도착한 메시지 출력. mqttio5.js에서 수정함
	else if(msg.destinationName == "CookTimer/temperature")
		addChartData(parseFloat(msg.payloadString));
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
	client.disconnect(); // 브로커에 접속 해제
//	document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}

function addZeros(num, digit) { // 자릿수 맞춰주기
	  var zero = '';
	  num = num.toString();
	  if (num.length < digit) {
	    for (i = 0; i < digit - num.length; i++) {
	      zero += '0';
	    }
	  }
	  return zero + num;
}
