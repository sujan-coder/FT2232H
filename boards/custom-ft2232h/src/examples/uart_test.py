from pyftdi.serialext import serial_for_url
import time

ser = serial_for_url('ftdi://ftdi:2232h/1', baudrate=115200)

print("UART Loopback Test")
print("Connect Jumper: TX (ADBUS1) → RX (ADBUS2)\n")

test_data = b"Loopback Test Message 123!\r\n"
print(f"Sending: {test_data}")
ser.write(test_data)

time.sleep(0.1)
response = ser.read(len(test_data))

if response == test_data:
    print(f"Received: {response}")
    print("✅ SUCCESS! UART is working correctly")
else:
    print(f"❌ FAILED! Received: {response}")
