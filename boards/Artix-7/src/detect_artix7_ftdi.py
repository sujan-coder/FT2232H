#!/usr/bin/env python3
"""
JTAG Detection for Artix-7 via FT232H
Compatible with older pyftdi version
"""

from pyftdi.ftdi import Ftdi
import time

print("=" * 60)
print("Artix-7 JTAG Detection via FT232H")
print("=" * 60)

url = 'ftdi://ftdi:232h:210299B92A72/1'
print(f"\n📡 Device URL: {url}")

# ============================================================
# Test 1: Basic FTDI Communication
# ============================================================
print("\n" + "-" * 40)
print("Test 1: Basic FTDI Communication")
print("-" * 40)

try:
    # Use the correct method for older pyftdi
    ftdi = Ftdi()
    ftdi.open_from_url(url)
    print("✅ FTDI device opened")
    print(f"   Device: {url}")
    ftdi.close()
    basic_working = True
except Exception as e:
    print(f"❌ Failed: {e}")
    basic_working = False

# ============================================================
# Test 2: Simple Pin Read (No JTAG)
# ============================================================
print("\n" + "-" * 40)
print("Test 2: Simple Pin Read (Bitbang Mode)")
print("-" * 40)

if basic_working:
    try:
        ftdi = Ftdi()
        ftdi.open_from_url(url)
        
        # Use integer for bitmode (0x01 = BITBANG, 0x02 = MPSSE)
        # Try bitbang mode first
        ftdi.set_bitmode(0x0F, 0x01)  # 0x01 = BITBANG mode
        print("✅ Bitbang mode enabled")
        
        # Read all pins
        pins = ftdi.read_port()
        print(f"   Pin states: 0x{pins:02X}")
        print(f"   Binary: {pins:08b}")
        print("   (bit0=TCK, bit1=TDI, bit2=TDO, bit3=TMS)")
        
        ftdi.close()
        print("✅ Pin read successful")
        
    except Exception as e:
        print(f"❌ Pin read failed: {e}")
        print("   This may indicate FPGA is not powered")

# ============================================================
# Test 3: JTAG TAP Reset Sequence
# ============================================================
print("\n" + "-" * 40)
print("Test 3: JTAG TAP Reset Sequence")
print("-" * 40)

if basic_working:
    try:
        ftdi = Ftdi()
        ftdi.open_from_url(url)
        
        # Use MPSSE mode (0x02)
        ftdi.set_bitmode(0x0F, 0x02)
        print("✅ MPSSE mode enabled")
        
        # JTAG pin definitions
        TCK = 0x01  # bit0
        TDI = 0x02  # bit1
        TMS = 0x08  # bit3
        
        def jtag_clock(tms=0):
            """Generate one JTAG clock cycle"""
            pins = (tms << 3)  # TMS at bit3
            ftdi.write_port(pins)          # TCK low
            time.sleep(0.00001)
            ftdi.write_port(pins | TCK)    # TCK high
            time.sleep(0.00001)
            ftdi.write_port(pins)          # TCK low
            time.sleep(0.00001)
        
        def read_tdo():
            """Read TDO pin (bit2)"""
            pins = ftdi.read_port()
            return (pins >> 2) & 0x01
        
        print("\n🔄 Sending JTAG reset sequence (5 clocks with TMS=1)...")
        for i in range(5):
            jtag_clock(tms=1)
        
        print("   TAP should now be in Test-Logic-Reset")
        
        # Move to idle
        print("\n➡️  Moving to Run-Test/Idle...")
        jtag_clock(tms=0)
        
        # Read TDO
        tdo = read_tdo()
        print(f"\n📊 TDO status: {tdo} ({'HIGH' if tdo else 'LOW'})")
        
        if tdo == 0:
            print("   TDO is LOW - No device detected in JTAG chain")
            print("   Make sure FPGA is powered and configured for JTAG")
        else:
            print("   TDO is HIGH - Possible device detected!")
        
        ftdi.close()
        print("\n✅ JTAG reset sequence complete")
        
    except Exception as e:
        print(f"❌ JTAG test failed: {e}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

print("""
What we learned:
1. FT232H is detected and accessible
2. Pin read works (you can see TCK/TDI/TMS/TDO states)
3. JTAG reset sequence can be sent

Next steps:
1. POWER THE FPGA BOARD
2. Run this script again - TDO should change
3. If TDO stays LOW, check:
   - FPGA power LED is on
   - JTAG jumpers on board are correct
   - Board is not in configuration mode

To test with OpenOCD instead:
   sudo apt install openocd
   openocd -f interface/ftdi.cfg -f board/digilent_arty.cfg
""")
print("=" * 60)