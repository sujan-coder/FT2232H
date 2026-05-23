#!/usr/bin/env python3
"""
Detection script specifically for Custom FT2232H PCB
Checks for PID 0x6010 (FT2232H)
"""

from pyftdi.ftdi import Ftdi
import usb.core

def main():
    print("=" * 60)
    print("Custom FT2232H PCB Detector")
    print("=" * 60)
    
    # Find FT2232H devices (PID 0x6010)
    devices = usb.core.find(find_all=True, idVendor=0x0403, idProduct=0x6010)
    
    found = False
    for dev in devices:
        found = True
        print(f"\n✅ Custom PCB detected!")
        print(f"   Bus: {dev.bus}, Device: {dev.address}")
        
        # Check for J2 connector (8 pins expected)
        print(f"   Available pins: 1L0 through 1L7 (ADBUS0-7)")
        print(f"   Missing: Channel B, ACBUS pins")
        
    if not found:
        print("\n❌ Custom FT2232H PCB not found!")
        print("   Check:")
        print("   1. USB connection")
        print("   2. Power jumpers (CN3-1 to CN3-3, CN2-1 to CN2-11)")
        print("   3. Run: lsusb | grep 0403")
        return
    
    print("\n" + "=" * 60)
    print("pyFTDI View:")
    Ftdi.show_devices()

if __name__ == "__main__":
    main()
