#!/usr/bin/env python3
"""
Deep Dive: JTAG TAP State Machine
Complete implementation with state tracking and visualization
"""

from pyftdi.ftdi import Ftdi
import time

class TAPStateMachine:
    """
    JTAG TAP (Test Access Port) State Machine
    Implements all 16 states of IEEE 1149.1
    """
    
    # TAP States (numbered for easy reference)
    STATES = {
        0:  "Test-Logic-Reset",
        1:  "Run-Test/Idle",
        2:  "Select-DR-Scan",
        3:  "Capture-DR",
        4:  "Shift-DR",
        5:  "Exit1-DR",
        6:  "Pause-DR",
        7:  "Exit2-DR",
        8:  "Update-DR",
        9:  "Select-IR-Scan",
        10: "Capture-IR",
        11: "Shift-IR",
        12: "Exit1-IR",
        13: "Pause-IR",
        14: "Exit2-IR",
        15: "Update-IR",
    }
    
    def __init__(self, ftdi):
        self.ftdi = ftdi
        self.current_state = 0  # Start in Test-Logic-Reset
        self.state_history = []
        
        # Pin definitions (Channel A)
        self.TCK = 0x01  # ADBUS0
        self.TDI = 0x02  # ADBUS1
        self.TDO = 0x04  # ADBUS2 (input)
        self.TMS = 0x08  # ADBUS3
        
        # Configure pins
        self.ftdi.set_bitmode(0x0B, Ftdi.BITMODE_BITBANG)  # TCK, TDI, TMS as outputs
        self.record_state("Initialized")
    
    def record_state(self, action=""):
        """Record state change for analysis"""
        state_name = self.STATES.get(self.current_state, "Unknown")
        self.state_history.append({
            'state': self.current_state,
            'name': state_name,
            'action': action,
            'time': time.time()
        })
    
    def clock(self, tms_value):
        """
        Generate a TCK clock cycle with given TMS value
        This is the fundamental JTAG operation
        """
        # Set TMS to desired value
        pins = tms_value << 3  # TMS is bit 3 (value 0 or 8)
        
        # Clock low to high
        self.ftdi.write_port(pins)           # TCK low (0)
        time.sleep(0.000001)                 # 1us hold
        self.ftdi.write_port(pins | self.TCK) # TCK high
        time.sleep(0.000001)
        self.ftdi.write_port(pins)           # TCK low
        
        # Update state based on TMS
        self.update_state(tms_value)
    
    def update_state(self, tms):
        """
        Update TAP state machine based on current state and TMS value
        Implements the complete 16-state transition diagram
        """
        old_state = self.current_state
        
        # State transition logic (from IEEE 1149.1 standard)
        transitions = {
            # (current_state, tms) -> new_state
            (0, 0): 1,   # Test-Logic-Reset + TMS=0 -> Run-Test/Idle
            (0, 1): 0,   # Test-Logic-Reset + TMS=1 -> Test-Logic-Reset
            
            (1, 0): 1,   # Run-Test/Idle + TMS=0 -> Run-Test/Idle
            (1, 1): 2,   # Run-Test/Idle + TMS=1 -> Select-DR-Scan
            
            (2, 0): 3,   # Select-DR-Scan + TMS=0 -> Capture-DR
            (2, 1): 9,   # Select-DR-Scan + TMS=1 -> Select-IR-Scan
            
            (3, 0): 4,   # Capture-DR + TMS=0 -> Shift-DR
            (3, 1): 5,   # Capture-DR + TMS=1 -> Exit1-DR
            
            (4, 0): 4,   # Shift-DR + TMS=0 -> Shift-DR
            (4, 1): 5,   # Shift-DR + TMS=1 -> Exit1-DR
            
            (5, 0): 6,   # Exit1-DR + TMS=0 -> Pause-DR
            (5, 1): 8,   # Exit1-DR + TMS=1 -> Update-DR
            
            (6, 0): 6,   # Pause-DR + TMS=0 -> Pause-DR
            (6, 1): 7,   # Pause-DR + TMS=1 -> Exit2-DR
            
            (7, 0): 4,   # Exit2-DR + TMS=0 -> Shift-DR
            (7, 1): 8,   # Exit2-DR + TMS=1 -> Update-DR
            
            (8, 0): 1,   # Update-DR + TMS=0 -> Run-Test/Idle
            (8, 1): 2,   # Update-DR + TMS=1 -> Select-DR-Scan
            
            (9, 0): 10,  # Select-IR-Scan + TMS=0 -> Capture-IR
            (9, 1): 0,   # Select-IR-Scan + TMS=1 -> Test-Logic-Reset
            
            (10, 0): 11, # Capture-IR + TMS=0 -> Shift-IR
            (10, 1): 12, # Capture-IR + TMS=1 -> Exit1-IR
            
            (11, 0): 11, # Shift-IR + TMS=0 -> Shift-IR
            (11, 1): 12, # Shift-IR + TMS=1 -> Exit1-IR
            
            (12, 0): 13, # Exit1-IR + TMS=0 -> Pause-IR
            (12, 1): 15, # Exit1-IR + TMS=1 -> Update-IR
            
            (13, 0): 13, # Pause-IR + TMS=0 -> Pause-IR
            (13, 1): 14, # Pause-IR + TMS=1 -> Exit2-IR
            
            (14, 0): 11, # Exit2-IR + TMS=0 -> Shift-IR
            (14, 1): 15, # Exit2-IR + TMS=1 -> Update-IR
            
            (15, 0): 1,  # Update-IR + TMS=0 -> Run-Test/Idle
            (15, 1): 2,  # Update-IR + TMS=1 -> Select-DR-Scan
        }
        
        self.current_state = transitions.get((old_state, tms), 0)
        self.record_state(f"TMS={tms}")
    
    def reset(self):
        """Force TAP into Test-Logic-Reset state (TMS=1 for 5 clocks)"""
        print("\n🔄 Resetting TAP to Test-Logic-Reset...")
        for i in range(5):
            self.clock(1)
        self.record_state("Reset")
        print(f"   Current state: {self.STATES[self.current_state]}")
    
    def go_to_idle(self):
        """Go from reset to Run-Test/Idle"""
        print("\n➡️  Moving to Run-Test/Idle...")
        self.clock(0)  # TMS=0 from reset goes to idle
        self.record_state("Moved to idle")
        print(f"   Current state: {self.STATES[self.current_state]}")
    
    def show_path_to_shift_dr(self):
        """Demonstrate the path to Shift-DR state"""
        print("\n📊 Path to Shift-DR (for data register access):")
        print("   Test-Logic-Reset → Run-Test/Idle → Select-DR-Scan → Capture-DR → Shift-DR")
        print("   TMS sequence: 0 → 1 → 0 → 0")
    
    def go_to_shift_dr(self):
        """Navigate to Shift-DR state for data register operations"""
        # From idle
        self.clock(1)  # Select-DR-Scan
        self.clock(0)  # Capture-DR
        self.clock(0)  # Shift-DR
        print(f"   In Shift-DR: {self.STATES[self.current_state]}")
    
    def read_idcode(self):
        """
        Read IDCODE register (most common JTAG operation)
        Demonstrates complete instruction + data register flow
        """
        print("\n🔍 Reading IDCODE Register")
        print("-" * 40)
        
        # Step 1: Reset TAP
        self.reset()
        self.go_to_idle()
        
        # Step 2: Go to Shift-IR to send IDCODE instruction
        print("\n📝 Shifting IDCODE instruction...")
        self.clock(1)  # Select-DR-Scan
        self.clock(1)  # Select-IR-Scan
        self.clock(0)  # Capture-IR
        self.clock(0)  # Shift-IR
        
        # IDCODE instruction is typically 0x01 (8 bits)
        idcode_inst = 0x01
        print(f"   Instruction: 0x{idcode_inst:02X}")
        
        for bit in range(8):
            tdi_bit = (idcode_inst >> bit) & 0x01
            # Set TDI accordingly
            pins = (tdi_bit << 1)  # TDI is bit 1
            self.ftdi.write_port(pins)
            self.clock(1 if bit == 7 else 0)
        
        # Step 3: Go to Shift-DR to read IDCODE value
        print("\n📖 Reading 32-bit IDCODE value...")
        self.clock(1)  # Exit1-IR
        self.clock(1)  # Update-IR
        self.clock(1)  # Select-DR-Scan
        self.clock(0)  # Capture-DR
        self.clock(0)  # Shift-DR
        
        # Read 32 bits
        idcode = 0
        for bit in range(32):
            # Read TDO
            pins = self.ftdi.read_port()
            tdo_bit = (pins >> 2) & 0x01  # TDO is bit 2
            
            idcode = (idcode >> 1) | (tdo_bit << 31)
            
            # Clock next bit (TMS=1 on last bit)
            self.clock(1 if bit == 31 else 0)
        
        # Return to idle
        self.clock(1)  # Exit1-DR
        self.clock(0)  # Update-DR
        self.clock(0)  # Run-Test/Idle
        
        return idcode
    
    def print_state_history(self):
        """Print the complete state transition history"""
        print("\n📜 State Transition History:")
        print("-" * 60)
        for entry in self.state_history:
            print(f"  {entry['name']:20} - {entry['action']}")
    
    def close(self):
        self.ftdi.close()

# ============================================================
# MAIN DEMONSTRATION
# ============================================================

def main():
    print("=" * 70)
    print("JTAG TAP State Machine Deep Dive")
    print("=" * 70)
    
    print("""
    This script demonstrates the complete JTAG TAP state machine
    including all 16 states and transitions.
    
    The TAP (Test Access Port) is the heart of JTAG - understanding
    these states is essential for any JTAG operation.
    """)
    
    input("Press Enter to start TAP demonstration...")
    
    # Initialize FTDI
    ftdi = Ftdi()
    ftdi.open('ftdi://ftdi:2232h/1')
    
    # Create TAP state machine
    tap = TAPStateMachine(ftdi)
    
    try:
        # Demonstrate state machine
        print("\n" + "=" * 70)
        print("DEMONSTRATION 1: TAP State Transitions")
        print("=" * 70)
        
        tap.show_path_to_shift_dr()
        tap.go_to_shift_dr()
        
        print("\n" + "=" * 70)
        print("DEMONSTRATION 2: IDCODE Reading")
        print("=" * 70)
        print("""
        IDCODE is a standard JTAG instruction that returns
        a 32-bit value identifying the device:
        - Bits 31-28: Version
        - Bits 27-12: Part Number  
        - Bits 11-1:  Manufacturer ID
        - Bit 0:      1 (always)
        """)
        
        idcode = tap.read_idcode()
        
        if idcode and idcode != 0xFFFFFFFF:
            print(f"\n✅ IDCODE: 0x{idcode:08X}")
            
            # Decode
            version = (idcode >> 28) & 0xF
            part = (idcode >> 12) & 0xFFFF
            manufacturer = (idcode >> 1) & 0x7FF
            
            print(f"\n📊 Decoded:")
            print(f"   Version:      {version}")
            print(f"   Part Number:  0x{part:04X}")
            print(f"   Manufacturer: 0x{manufacturer:03X}")
        else:
            print("\n⚠️  No IDCODE read - check target connection")
        
        tap.print_state_history()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted")
    finally:
        tap.close()
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("  1. Connect a JTAG target device")
    print("  2. Study the state transition diagram")
    print("  3. Experiment with different TMS sequences")
    print("=" * 70)

if __name__ == "__main__":
    main()