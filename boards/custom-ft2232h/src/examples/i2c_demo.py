#!/usr/bin/env python3
"""
This code is just for understanding the protocol implementation
I2C Communication Example
Reads from common I2C sensors (e.g., BMP280, MPU6050)
Requires: FT2232H Mini Module with pull-up resistors
"""

from pyftdi.i2c import I2cController
import time

# ============================================================
# 1. INITIALIZE I2C CONTROLLER
# ============================================================
# Create I2C controller on Channel A
i2c = I2cController()

# Configure FTDI device with 100kHz clock speed
i2c.configure('ftdi://ftdi:2232h/1', frequency=100000)

print("=" * 50)
print("I2C DEMONSTRATION")
print("=" * 50)

# ============================================================
# 2. SCAN FOR DEVICES
# ============================================================
print("\n1. Scanning for I2C devices...")
devices = []
for address in range(8, 120):  # 0x08 to 0x77
    try:
        port = i2c.get_port(address)
        port.write(b'')  # Test connection
        devices.append(address)
        print(f"   Found device at address: 0x{address:02X}")
    except:
        pass

if not devices:
    print("   No I2C devices found!")
    print("   Check connections and pull-up resistors")
else:
    print(f"   Found {len(devices)} device(s)")

# ============================================================
# 3. READ FROM A KNOWN DEVICE (e.g., BMP280)
# ============================================================
def read_bmp280():
    """Read temperature and pressure from BMP280 sensor"""
    BMP280_ADDRESS = 0x76
    BMP280_ID_REG = 0xD0
    
    try:
        port = i2c.get_port(BMP280_ADDRESS)
        
        # Read chip ID
        chip_id = port.read(1, address=BMP280_ADDRESS, start=True)
        print(f"   BMP280 Chip ID: 0x{chip_id[0]:02X}")
        
        # Read temperature (simplified - would need more registers)
        # temp_data = port.read(2, address=BMP280_ADDRESS)
        # temperature = temp_data[0] << 8 | temp_data[1]
        # print(f"   Temperature: {temperature / 100:.2f}°C")
        
        return True
    except Exception as e:
        print(f"   Error reading BMP280: {e}")
        return False

# ============================================================
# 4. WRITE TO A DEVICE
# ============================================================
def write_example():
    """Write to a device (e.g., configure sensor)"""
    DEVICE_ADDRESS = 0x68  # Example: MPU6050
    
    try:
        port = i2c.get_port(DEVICE_ADDRESS)
        
        # Write configuration byte to register
        register = 0x6B  # Power management register
        value = 0x00     # Wake up device
        
        port.write(bytes([register, value]))
        print(f"   Written 0x{value:02X} to register 0x{register:02X}")
        return True
    except Exception as e:
        print(f"   Error writing: {e}")
        return False

# ============================================================
# 5. READ FROM SPECIFIC REGISTER
# ============================================================
def read_register(address, register, length=1):
    """Read from a specific I2C device register"""
    try:
        port = i2c.get_port(address)
        port.write(bytes([register]))
        data = port.read(length, start=True)
        return data
    except Exception as e:
        print(f"   Read error: {e}")
        return None

# ============================================================
# 6. EXAMPLE: READ MPU6050 WHO_AM_I REGISTER
# ============================================================
print("\n2. Reading MPU6050 (if connected)")
MPU6050_ADDRESS = 0x68
WHO_AM_I_REG = 0x75

result = read_register(MPU6050_ADDRESS, WHO_AM_I_REG)
if result:
    print(f"   MPU6050 WHO_AM_I: 0x{result[0]:02X}")
    if result[0] == 0x68:
        print("   ✅ MPU6050 detected!")

# ============================================================
# 7. CONTINUOUS READING EXAMPLE
# ============================================================
def read_temperature_humidity():
    """Read from common temperature/humidity sensor (e.g., Si7021)"""
    SI7021_ADDRESS = 0x40
    
    try:
        port = i2c.get_port(SI7021_ADDRESS)
        # Trigger measurement
        port.write(bytes([0xF3]))  # Measure temperature command
        time.sleep(0.1)
        data = port.read(2)
        temp = (data[0] << 8 | data[1]) * 175.72 / 65536.0 - 46.85
        print(f"   Temperature: {temp:.2f}°C")
        return temp
    except:
        return None

print("\n3. Continuous reading (press Ctrl+C to stop)")
print("   Connect a temperature/humidity sensor")
print("   Reading every 2 seconds...\n")

try:
    count = 0
    while count < 5:
        count += 1
        # Uncomment when you have a sensor
        # temp = read_temperature_humidity()
        # if temp:
        #     print(f"   [{count}] {temp:.2f}°C")
        # else:
        #     print(f"   [{count}] No sensor detected")
        print(f"   [{count}] Placeholder - Connect sensor for real data")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n   Stopped")

# ============================================================
# 8. CLOSE CONNECTION
# ============================================================
i2c.close()
print("\nI2C Demo Complete!")
