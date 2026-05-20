#!/usr/bin/env python3
"""
FT2232H Detection Utility

Verifies device connectivity and displays available interfaces.
"""

from pyftdi.ftdi import Ftdi

def main():
    print("=" * 50)
    print("FT2232H Detection")
    print("=" * 50)
    
    print("\nScanning for FTDI devices...\n")
    Ftdi.show_devices()
    
    print("\n" + "=" * 50)
    print("To access channels:")
    print("  Channel A: ftdi://ftdi:2232:1:7/1")
    print("  Channel B: ftdi://ftdi:2232:1:7/2")
    print("=" * 50)

if __name__ == "__main__":
    main()
