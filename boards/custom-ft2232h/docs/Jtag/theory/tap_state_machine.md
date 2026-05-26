# JTAG TAP State Machine - Complete Reference

## The 16 States

### Data Register (DR) Path
1. **Test-Logic-Reset** - Power-on state, TAP disabled
2. **Run-Test/Idle** - Normal operational state
3. **Select-DR-Scan** - Decision point for DR operations
4. **Capture-DR** - Load data into shift register
5. **Shift-DR** - Shift data through register
6. **Exit1-DR** - Partial exit from Shift-DR
7. **Pause-DR** - Temporarily halt shifting
8. **Exit2-DR** - Resume or exit shifting
9. **Update-DR** - Latch shifted data

### Instruction Register (IR) Path
10. **Select-IR-Scan** - Decision point for IR operations
11. **Capture-IR** - Load instruction register
12. **Shift-IR** - Shift instruction
13. **Exit1-IR** - Partial exit from Shift-IR
14. **Pause-IR** - Temporarily halt shifting
15. **Exit2-IR** - Resume or exit shifting
16. **Update-IR** - Latch new instruction

## Key Transition Patterns

| Operation | TMS Sequence |
|-----------|--------------|
| Reset to Idle | 0 |
| Idle to Shift-DR | 1,0,0 |
| Idle to Shift-IR | 1,1,0,0 |
| Shift-DR back to Idle | 1,1,0 |

## Common Instructions

| Instruction | Code | Description |
|-------------|------|-------------|
| BYPASS | 0x1F (5-bit) | 1-bit path through device |
| IDCODE | 0x01 (8-bit) | Read device identification |
| SAMPLE/PRELOAD | 0x02 (8-bit) | Capture boundary scan |
| EXTEST | 0x03 (8-bit) | Test external connections |