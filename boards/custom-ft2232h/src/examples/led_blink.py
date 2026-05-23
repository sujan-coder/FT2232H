import time
from pyftdi.gpio import GpioMpsseController

# =====================================================================
# STEP 1: Initialize the Controllers for Both Channels
# =====================================================================
controller_A = GpioMpsseController()
controller_B = GpioMpsseController()

# Connect using your system's exact detected USB hardware addresses
controller_A.configure('ftdi://ftdi:2232:1:f/1', frequency=1e6)
controller_B.configure('ftdi://ftdi:2232:1:f/2', frequency=1e6)

# =====================================================================
# STEP 2: Configure the Pin Directions (Input vs. Output)
# =====================================================================
# Before we can turn pins ON, we must tell the chip they are "Outputs".
# We use the exact same hex values we just calculated to open up the paths.

pins_A = 0x0110    # Targets ADBUS 0,4
pins_B = 0x0110    # Targets BCBUS 0,4

# 1 means Output mode, 0 means Input mode
controller_A.set_direction(pins_A, pins_A)
controller_B.set_direction(pins_B, pins_B)

print("Pins initialized successfully!")
print("Toggling your custom pin groups... Press Ctrl+C to stop.")

# =====================================================================
# STEP 3: The Main Loop (Turning Pins On and Off)
# =====================================================================
try:
    while True:
        print("-> Setting pins HIGH (Electricity flowing)")
        print("-> D10 on")
        controller_A.write(0x0010)
        time.sleep(0.1) 

        print("-> D11 on")
        controller_A.write(0x0100)
        time.sleep(0.1)
        controller_A.write(0x0110)

        print("-> D12 on")
        controller_B.write(0x0010)
        time.sleep(0.1) 

        print("-> D13 on")
        controller_B.write(0x0100)
        time.sleep(0.1) 
        controller_B.write(0x0110)

except KeyboardInterrupt:
    controller_A.write(0x0110)
    controller_B.write(0x0110)
    print("\nProgram stopped safely. All pins reset to 0V.")