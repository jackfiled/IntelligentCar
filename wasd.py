import Car

from pynput import keyboard
import threading
import time



# 创建Car对象
car = Car.Car()

# 控制标志位
forward_pressed = False
backward_pressed = False
left_pressed = False
right_pressed = False

# 监听键盘输入
def on_key_release(key):
    global forward_pressed, backward_pressed, left_pressed, right_pressed
    try:
        if key.char == 'w':
            forward_pressed = False
        elif key.char == 's':
            backward_pressed = False
        elif key.char == 'a':
            left_pressed = False
        elif key.char == 'd':
            right_pressed = False
    except AttributeError:
        pass

def on_key_press(key):
    global forward_pressed, backward_pressed, left_pressed, right_pressed
    try:
        if key.char == 'w':
            forward_pressed = True
        elif key.char == 's':
            backward_pressed = True
        elif key.char == 'a':
            left_pressed = True
        elif key.char == 'd':
            right_pressed = True
    except AttributeError:
        pass


# 设置键盘状态
def set_key_state(key, state):
    global forward_pressed, backward_pressed, left_pressed, right_pressed
    if key == 'forward':
        forward_pressed = state
    elif key == 'backward':
        backward_pressed = state
    elif key == 'left':
        left_pressed = state
    elif key == 'right':
        right_pressed = state

# 定义控制线程的函数
def control_thread():
    while True:
        # 根据按键状态控制小车
        if forward_pressed:
            car.set(car.normalSpeeed, car.normalSpeeed)  # 前进
        elif backward_pressed:
            car.set(-car.normalSpeeed, -car.normalSpeeed)  # 后退
        elif left_pressed:
            car.set(0, car.normalSpeeed)  # 左转
        elif right_pressed:
            car.set(car.normalSpeeed, 0)  # 右转
        else:
            car.set(0, 0)  # 停止
        # time.sleep(0.1)  # 控制频率


def main(control_thread=None):
    try:
        control_thread = threading.Thread(target=control_thread)
        control_thread.start()
        with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("exit")
        car.close()

if __name__ == "__main__":
    main(control_thread)
