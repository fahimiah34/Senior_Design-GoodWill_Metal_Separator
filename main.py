import time
from servo import ServoControl # use the ServoControl class from servo.py
from proximity_sensor import ProximitySensor # use the ProximitySensor class from proximity_sensor.py
from ir_sensor import IRSensor, MLX90614, MLX90615 # use the IRSensor class from ir_sensor.py
from smbus2 import SMBus

# # changes state of metal detection
# def change_state(state):
#     return not state 

# # sees if the current state and new state are the same
# def is_different_state(currentState, newState):
#     if currentState != newState:
#         newState = currentState
#     return newState


if __name__ == '__main__':
    # set up servo 
    servoControl = ServoControl(23) # initialize servo to work on GPIO 23

    # set up proximity sensor
    sensorControl = ProximitySensor(24) # initialize proximity sensor to work on GPIO 24

    # set up IR sensor
    bus = SMBus(1) # use I2C bus 1 (pins 3 (SDA), 5 (SCL) on Raspberry Pi)
    sensor = MLX90614(bus, address=0x5A)  # Initialize the MLX90614 sensor, Default I2C address of MLX90614 is 0x5A

    state = False

    try:
        while True: 
            # checks if the proximity sensor detects metal, then moves servo to specific direction
            # True for metal and False otherwise 
            if sensorControl.is_object_detected():
                print("Object Detected")
                time.sleep(1.5)
                servoControl.servo_left()
                time.sleep(3)
            else: 
                print("No object detected")
                servoControl.servo_right()
                #time.sleep(10)
        
            # read ambient and object temperature from the IR sensor
            # ambient_temp = sensor.ambient_temp 
            # object_temp = sensor.object_temp     

            # # print the temperatures
            # print(f"Ambient Temperature: {ambient_temp:.2f}°C")
            # print(f"Object Temperature: {object_temp:.2f}°C")

            time.sleep(0.1) # waits 0.5 seconds before loop restarts
    except KeyboardInterrupt: 
        print("Code stopped")
    finally: 
        sensorControl.cleanup()
