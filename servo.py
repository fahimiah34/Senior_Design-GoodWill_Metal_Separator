from gpiozero import Servo
from time import sleep

class ServoControl: 
    # initialize servo 
    def __init__(self, gpio_pin):
        self.servo = Servo(gpio_pin) # controls the servo, which is connected on a GPIO pin

    # turn servo to the right which in this case in the min position
    def servo_right(self):
        self.servo.min()
    
    # turn servo to the left which in this case in the max position
    def servo_left(self):
        self.servo.max()


