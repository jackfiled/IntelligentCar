import socket
import json
import threading
import time


class Message:
    def __init__(self, input) -> None:
        try:
            input = json.loads(input)

            input = input["sensors"]

            for item in input:
                if item["name"] == "distance":
                    self.distance = item["value"]
                elif item["name"] == "light" and item["id"] == 2:
                    if item["value"] == 0:
                        self.frontBlock = True
                    elif item["value"] == 1:
                        self.frontBlock = False
                elif item["name"] == "light" and item["id"] == 1:
                    if item["value"] == 1:
                        self.onBlack = True
                    elif item["value"] == 0:
                        self.onBlack = False

            self.isValid = True
        except json.decoder.JSONDecodeError:
            print("JSON Decode error:")
            print(input)

            self.isValid = False


class Car:
    def __init__(self) -> None:
        self.left = 0.0
        self.right = 0.0
        self.message=None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("192.168.0.1", 9999))
        except :
            print("连接小车失败")

        self.normalSpeeed=0.2

        # 持续发送控制信号
        def work():
            while True:
                threading.Thread(target=self.doSend).start()
                threading.Thread(target=self.receive).start()
                time.sleep(0.05)

        thread = threading.Thread(target=work)
        thread.start()

    # 接受传感器
    def receive(self) -> Message:
        try:
            receiveData = self.socket.recv(1024)
            m = Message(receiveData.decode())

            if m.isValid:
                self.message=m
                if m.frontBlock or m.distance<10 or m.distance> 1000:
                    self.set(0, 0)
        except :
            #print("接受传感器信息失败")
            pass
        return self.message

    # 设定舵机属性
    def set(self, left, right) -> None:
        self.left = left
        self.right = right

    # def set(self,speed)->None:
    #     self.set(speed,speed)

    # 立即控制
    def control(self, left, right) -> None:
        self.set(left, right)
        self.doSend()

    # 实际发送
    def doSend(self):
        controlObj = {}
        controlObj["servos"] = [
            {
                "isTurn": True if self.left > 0 else False,
                "servoId": 6,
                "servoSpeed": abs(self.left)
            },
            {
                "isTurn": True if self.right > 0 else False,
                "servoId": 3,
                "servoSpeed": abs(self.right)
            }
        ]
        controlStr = json.dumps(controlObj) + "\r\n"
        # print(controlStr)
        code=0
        try:
            code=self.socket.send(controlStr.encode())
        except Exception as e:
            #print(f"发送失败{e}")
            pass
        return code

    def close(self) -> None:
        self.socket.close()
