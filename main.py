import Car

def main():
    car = Car.Car()

    try:
        while(True):
            message = car.receive()
            car.control(0.2, 0.2)
            if message.isValid:
                print(f"Distance: {message.distance}, ForeBlock: {message.frontBlock}, OnGround: {message.onBlack}")
    except KeyboardInterrupt:
        print("exit")
        car.close()

if __name__ == "__main__":
    main()