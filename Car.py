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
        self.receiveFlag = True
        self.sendFlag = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("192.168.0.1", 9999))
        except :
            print("连接小车失败")

        self.receiveThread = threading.Thread(target=self.doReceive)
        self.sendThread = threading.Thread(target=self.doSend)
        
        self.receiveThread.start()
        self.sendThread.start()


    
    def doReceive(self) -> None:
        while self.receiveFlag:
            try:
                receiveDaa = self.socket.recv(1024)
                m = Message(receiveDaa.decode())

                if m.isValid:
                    self.message = m;
            except Exception as e:
                print(f"接受传感器消息失败: {e}")

    # 实际发送
    def doSend(self):
        while self.sendFlag:
            controlObj = {}
            controlObj["servos"] = [
                {
                    "isTurn": True if self.left > 0 else False,
                    "servoId": 6,
                    "servoSpeed": self.left
                },
                {
                    "isTurn": True if self.right > 0 else False,
                    "servoId": 3,
                    "servoSpeed": self.right
                }
            ]
            controlStr = json.dumps(controlObj) + "\r\n"
            try:
                self.socket.send(controlStr.encode())
            except Exception as e:
                print(f"发送控制消息失败: {e}")

        # 设定舵机属性
    def set(self, left, right) -> None:
        self.left = left
        self.right = right

    def close(self) -> None:
        self.socket.close()
        
