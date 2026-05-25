from pyftdi.i2c import I2cController

i2c = I2cController()
i2c.configure('ftdi://ftdi:2232h/1', frequency=100000)

print("Scanning for I2C devices...")
for addr in range(8, 120):
    try:
        port = i2c.get_port(addr)
        port.write(b'')
        print(f"Found device at 0x{addr:02X}")
    except:
        pass