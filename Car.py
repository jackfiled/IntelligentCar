import socket
import json

class Message:
    def __init__(self, input) -> None:
        try:
            input = json.loads(input)

            input = input["sensors"]

            for item in input:
                if item["name"] == "distance":
                    self.Distance = item["value"]
                elif item["name"] == "light" and item["id"] == 2:
                    if item["value"] == 0:
                        self.ForeBlock = True;
                    elif item["value"] == 1:
                        self.ForeBlock = False;
                elif item["name"] == "light" and item["id"] == 1:
                    if item["value"] == 1:
                        self.OnGround = True
                    elif item["value"] == 0:
                        self.OnGround = False
            
            self.Valid = True
        except json.decoder.JSONDecodeError:
            print("JSON Decode error:")
            print(input)

            self.Valid = False
        

class Car:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

        self.socket.connect(("192.168.0.1", 9999))

    def receive(self) -> Message:
        receiveData = self.socket.recv(1024)

        return Message(receiveData.decode())
    
    def control(self, left, right) -> None:
        controlObj  = {}
        controlObj["servos"] = [
            {
                "isTurn": True if left > 0 else False,
                "servoId": 6,
                "servoSpeed": abs(left)
            },
            {
                "isTurn": True if right > 0 else False,
                "servoId": 3,
                "servoSpeed": abs(right)
            }
        ]

        controlStr = json.dumps(controlObj) + "\r\n"

        print(controlStr)
        self.socket.send(controlStr.encode())
    
    def close(self) -> None:
        self.socket.close()

        

    