import time
import struct
from smbus2 import SMBus

class IRSensor:
    def read16(self, register):
        data = self.i2c.read_i2c_block_data(self.address, register, 2)
        return struct.unpack('<H', bytearray(data))[0]

    def read_temp(self, register):
        temp = self.read16(register)
        # Apply measurement resolution (0.02 degrees per LSB)
        temp *= 0.02
        # Kelvin to Celsius
        temp -= 273.15
        return temp

    def read_ambient_temp(self):
        return self.read_temp(self._REGISTER_TA)

    def read_object_temp(self):
        return self.read_temp(self._REGISTER_TOBJ1)

    def read_object2_temp(self):
        if self.dual_zone:
            return self.read_temp(self._REGISTER_TOBJ2)
        else:
            raise RuntimeError("Device only has one thermopile")

    @property
    def ambient_temp(self):
        return self.read_ambient_temp()

    @property
    def object_temp(self):
        return self.read_object_temp()

    @property
    def object2_temp(self):
        return self.read_object2_temp()


class MLX90614(IRSensor):
    _REGISTER_TA = 0x06
    _REGISTER_TOBJ1 = 0x07
    _REGISTER_TOBJ2 = 0x08

    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address
        _config1 = self.i2c.read_i2c_block_data(address, 0x25, 2)
        _dz = struct.unpack('<H', bytearray(_config1))[0] & (1 << 6)
        self.dual_zone = bool(_dz)


class MLX90615(IRSensor):
    _REGISTER_TA = 0x26
    _REGISTER_TOBJ1 = 0x27

    def __init__(self, i2c, address=0x5B):
        self.i2c = i2c
        self.address = address
        self.dual_zone = False


# Main execution logic
if __name__ == "__main__":
    # Use I2C bus 1 (pins 3 (SDA), 5 (SCL) on Raspberry Pi)
    bus = SMBus(1)

    # Initialize the MLX90614 sensor
    sensor = MLX90614(bus, address=0x5A)  # Default I2C address of MLX90614 is 0x5A

    try:
        while True:
            # Read ambient and object temperature
            ambient_temp = sensor.ambient_temp  # Use property
            object_temp = sensor.object_temp      # Use property

            # Print the temperatures
            print(f"Ambient Temperature: {ambient_temp:.2f}°C")
            print(f"Object Temperature: {object_temp:.2f}°C")

            # Wait for 1 second before taking the next reading
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        # Close the I2C bus when done
        bus.close()
