import Car

def main():
    car = Car.Car()
    left = 0.8
    right = 0.8

    try:
        while(True):
            message = car.receive()
            car.set(left, right)
            if message.isValid:
                print(f"Distance: {message.distance}, ForeBlock: {message.frontBlock}, OnGround: {message.onBlack}")
                if float(message.distance) < 10.0:
                    print(f"Blocked")
                    left = 0
                    right = 0
                else:
                    left = 0.8
                    right = 0.8
    except KeyboardInterrupt:
        print("exit")
        car.close()

if __name__ == "__main__":
    main()