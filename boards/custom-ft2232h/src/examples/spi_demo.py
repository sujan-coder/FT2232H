#!/usr/bin/env python3
"""
This code is just for understanding the protocol implementation
SPI Communication Example
Reads from an SPI sensor (e.g., MCP3008 ADC)
Requires: FT2232H Mini Module
"""

from pyftdi.spi import SpiController
import time

# ============================================================
# 1. INITIALIZE SPI CONTROLLER
# ============================================================
# Create SPI controller on Channel A
spi = SpiController(cs_count=1)

# Configure the FTDI device
spi.configure('ftdi://ftdi:2232h/1')

# ============================================================
# 2. GET A PORT (CS = Chip Select)
# ============================================================
# Port 0 corresponds to CS pin (ADBUS3)
slave = spi.get_port(cs=0, freq=1e6, mode=0)

print("=" * 50)
print("SPI DEMONSTRATION")
print("=" * 50)

# ============================================================
# 3. SIMPLE WRITE
# ============================================================
print("\n1. Simple Write Test")
data_to_send = b'\x55\xAA'  # Test pattern
print(f"   Sending: {data_to_send.hex()}")
slave.write(data_to_send)
print("   ✓ Write complete")

# ============================================================
# 4. SIMPLE READ
# ============================================================
print("\n2. Simple Read Test")
bytes_to_read = 4
received = slave.read(bytes_to_read)
print(f"   Read {bytes_to_read} bytes: {received.hex()}")
print("   ✓ Read complete")

# ============================================================
# 5. FULL DUPLEX (Write and Read Simultaneously)
# ============================================================
print("\n3. Full Duplex Exchange")
# Send 3 bytes, simultaneously receive 3 bytes
tx_data = b'\x01\x02\x03'
rx_data = slave.exchange(tx_data, duplex=True)
print(f"   Sent: {tx_data.hex()}")
print(f"   Received: {rx_data.hex()}")
print("   ✓ Exchange complete")

# ============================================================
# 6. READ FROM MCP3008 ADC (Example)
# ============================================================
def read_mcp3008(channel):
    """Read from MCP3008 ADC channel (0-7)"""
    if channel < 0 or channel > 7:
        return None
    
    # MCP3008 command: start bit (1) + single-ended (1) + channel (3 bits)
    command = 0b00011000 | (channel << 4)  # 0x18 = start+single
    command = ((command << 8) & 0xFF00) | 0x00
    
    # Send 3 bytes, receive 3 bytes back
    result = slave.exchange([command >> 8, command & 0xFF, 0x00])
    
    # Extract 10-bit ADC value
    value = ((result[1] & 0x03) << 8) | result[2]
    return value

print("\n4. Reading from MCP3008 ADC (if connected)")
print("   Connect MCP3008 to SPI bus")
print("   Channel 0: ", end="", flush=True)
# Uncomment when device is connected:
# adc_value = read_mcp3008(0)
# print(f"{adc_value}")

# ============================================================
# 7. CLOSE CONNECTION
# ============================================================
spi.close()
print("\nSPI Demo Complete!")
