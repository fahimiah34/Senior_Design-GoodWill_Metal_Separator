import RPi.GPIO as GPIO
import time

class ProximitySensor:
    # initializes the sensor 
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin # initializes the sensor to the set GPIO pin
        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
        GPIO.setup(self.sensor_pin, GPIO.IN)  # Set up the sensor pin as an input

    # checks if the voltage of the sensor is high 
    # returns True if an object is detected (high voltage)
    # returns False otherwise
    def is_object_detected(self):
        return GPIO.input(self.sensor_pin) == GPIO.HIGH
    
    # clean up GPIO settings
    def cleanup(self):
        GPIO.cleanup()
