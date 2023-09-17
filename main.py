import Car

def main():
    car = Car.Car()

    try:
        while(True):
            message = car.receive()
            car.control(0.2, 0.2)
            if message.Valid:
                print(f"Distance: {message.Distance}, ForeBlock: {message.ForeBlock}, OnGround: {message.OnGround}")
    except KeyboardInterrupt:
        print("exit")
        car.close()

if __name__ == "__main__":
    main()