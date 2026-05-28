#!/usr/bin/env python3
"""
JTAG Detection for Artix-7 via FT2232H (0403:6010)
"""

from pyftdi.jtag import JtagController
import sys

print("=" * 60)
print("Artix-7 JTAG Detection via FT2232H")
print("=" * 60)

# Your FT2232H is at 0403:6010
# Try both channels
urls = [
    ('ftdi://0403:6010/1', 'Channel A'),
    ('ftdi://0403:6010/2', 'Channel B'),
    ('ftdi://ftdi:2232h/1', 'FT2232H Channel A (alt)'),
    ('ftdi://ftdi:2232h/2', 'FT2232H Channel B (alt)'),
]

for url, desc in urls:
    print(f"\n📡 Trying {desc}: {url}")
    
    try:
        jtag = JtagController()
        jtag.configure(url, frequency=6000000)
        jtag.reset()
        
        # Try to read IDCODE
        idcode = jtag.read_idcode()
        
        if idcode and idcode != 0xFFFFFFFF:
            print(f"   ✅ SUCCESS! JTAG working on {desc}")
            print(f"   IDCODE: 0x{idcode:08X}")
            
            # Decode Artix-7 IDCODE
            version = (idcode >> 28) & 0xF
            part = (idcode >> 13) & 0x7FFF
            manufacturer = (idcode >> 1) & 0xFFF
            
            print(f"\n   📊 Decoded:")
            print(f"      Version:      {version}")
            print(f"      Part Number:  0x{part:04X}")
            print(f"      Manufacturer: 0x{manufacturer:03X}")
            
            # Artix-7 part numbers
            artix_parts = {
                0x362D: "XC7A35T / XC7A50T",
                0x402D: "XC7A75T",
                0x482D: "XC7A100T",
                0x502D: "XC7A200T",
            }
            
            if part in artix_parts:
                print(f"      Device:       {artix_parts[part]}")
            
            jtag.close()
            print("\n✅ Ready for JTAG deep dive!")
            sys.exit(0)
        else:
            print(f"   ⚠️  No response (FPGA not detected)")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:60]}")
    
    try:
        jtag.close()
    except:
        pass

print("\n" + "=" * 60)
print("❌ No JTAG response from Artix-7")
print("\nPossible reasons:")
print("  1. FPGA not powered")
print("  2. JTAG cable on wrong channel (try channel B)")
print("  3. Board needs specific initialization")
print("  4. Check board jumpers for JTAG selection")
print("=" * 60)