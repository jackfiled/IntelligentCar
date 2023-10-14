import Car
import time    

def main():
    car = Car.Car()
    left = 0.3
    right = 0.3
    try:
        while(True):
            car.set(left, right)
            if car.message != None and car.message.isValid:
                print(f"Distance: {car.message.distance}, ForeBlock: {car.message.frontBlock}, OnGround: {car.message.onBlack}")
                if car.message.frontBlock == True or float(car.message.distance) < 15.0:
                    left = 0
                    right = 0
                    continue
                else:
                    left = 0.3
                    right = 0.3
                
                if car.message.onBlack == False:
                    left = 0.3
                    right = 0.3
                else:
                    find_time = 10
                
                    while True:
                        flag = False
                        for i in range(find_time):
                            time.sleep(0.05)
                            car.set(-0.3, 0.3)
                            if car.message != None and car.message.isValid:
                                if car.message.onBlack == False:
                                    flag = True
                                    break
                    
                        if flag:
                            break
                        
                        for i in range(find_time * 2):
                            time.sleep(0.05)
                            car.set(0.3, -0.3)
                            if car.message != None and car.message.isValid:
                                if car.message.onBlack == False:
                                    flag = True
                                    break
                        
                        if flag:
                            break
                        find_time += 10
                time.sleep(0.05)
    except KeyboardInterrupt:
        print("exit")
        car.close()

if __name__ == "__main__":
    main()