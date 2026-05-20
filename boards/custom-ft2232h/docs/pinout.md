# FTDI_ADAPTOR_BOARD_CUSTOM - Pinout Reference

## Connector G1 (Channel A - Primary JTAG/GPIO)

| Header Pin | Signal Name | FT2232H Pin | Function | Direction |
|------------|-------------|-------------|----------|-----------|
| 1 | G1-TDI | ADBUS1 | TDI / SPI_MOSI | Output |
| 2 | G1-TCK | ADBUS0 | TCK / SPI_CLK | Output |
| 3 | G1-TDO | ADBUS2 | TDO / SPI_MISO | Input |
| 4 | G1-TMS | ADBUS3 | TMS / SPI_CS | Output |
| 5 | G1-L00 | ADBUS4 | GPIO / Lower bit 0 | I/O |
| 6 | G1-L01 | ADBUS5 | GPIO / Lower bit 1 | I/O |
| 7 | G1-L02 | ADBUS6 | GPIO / Lower bit 2 | I/O |
| 8 | G1-L03 | ADBUS7 | GPIO / Lower bit 3 | I/O |
| 9 | G1-H00 | ACBUS0 | Control / High bit 0 | I/O |
| 10 | G1-H01 | ACBUS1 | Control / High bit 1 | I/O |
| 11 | G1-H02 | ACBUS2 | Control / High bit 2 | I/O |
| 12 | G1-H03 | ACBUS3 | Control / High bit 3 | I/O |
| 13 | G1-H04 | ACBUS4 | Control / High bit 4 | I/O |
| 14 | G1-H05 | ACBUS5 | Control / High bit 5 | I/O |
| 15 | G1-H06 | ACBUS6 | Control / High bit 6 | I/O |
| 16 | G1-H07 | ACBUS7 | Control / High bit 7 | I/O |

## Connector G2 (Channel B - Secondary JTAG/GPIO)

| Header Pin | Signal Name | FT2232H Pin | Function | Direction |
|------------|-------------|-------------|----------|-----------|
| 1 | G2-TDI | BDBUS1 | TDI / SPI_MOSI | Output |
| 2 | G2-TCK | BDBUS0 | TCK / SPI_CLK | Output |
| 3 | G2-TDO | BDBUS2 | TDO / SPI_MISO | Input |
| 4 | G2-TMS | BDBUS3 | TMS / SPI_CS | Output |
| 5 | G2-L00 | BDBUS4 | GPIO / Lower bit 0 | I/O |
| 6 | G2-L01 | BDBUS5 | GPIO / Lower bit 1 | I/O |
| 7 | G2-L02 | BDBUS6 | GPIO / Lower bit 2 | I/O |
| 8 | G2-L03 | BDBUS7 | GPIO / Lower bit 3 | I/O |
| 9 | G2-H00 | BCBUS0 | Control / High bit 0 | I/O |
| 10 | G2-H01 | BCBUS1 | Control / High bit 1 | I/O |
| 11 | G2-H02 | BCBUS2 | Control / High bit 2 | I/O |
| 12 | G2-H03 | BCBUS3 | Control / High bit 3 | I/O |
| 13 | G2-H04 | BCBUS4 | Control / High bit 4 | I/O |
| 14 | G2-H05 | BCBUS5 | Control / High bit 5 | I/O |
| 15 | G2-H06 | BCBUS6 | Control / High bit 6 | I/O |
| 16 | G2-H07 | BCBUS7 | Control / High bit 7 | I/O |

## Power/Control Header (J1)

| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | GND | Ground |
| 2 | PWR+ | External power input (5V typical) |
| 3 | PWR- | Power ground |
| 4 | RST+ | Reset input (active low) |
| 5 | RST- | Reset output to target |
| 6 | 3V3 | 3.3V output (from FT2232H VCCIO) |

## DIP Switch Configuration

| Switch | Function | ON | OFF |
|--------|----------|-----|-----|
| SW1 | Channel A Mode | MPSSE | UART |
| SW2 | Channel B Mode | MPSSE | UART |
| SW3 | Pull-ups Enable | Enabled | Disabled |
| SW4 | Reserved | - | - |

*(Verify actual switch labels on your board)*

## Quick Reference

### For JTAG Programming (Channel A)
- Connect G1 pins 1-4 to target: TDI, TCK, TDO, TMS
- Use G1-H00-H07 for additional debug signals

### For UART (Channel A)
- TX: G1-TDI (ADBUS1)
- RX: G1-TDO (ADBUS2) 
- RTS: G1-L00 (ADBUS4)
- CTS: G1-L01 (ADBUS5)

### For SPI (Channel A)
- CLK: G1-TCK (ADBUS0)
- MOSI: G1-TDI (ADBUS1)
- MISO: G1-TDO (ADBUS2)
- CS: G1-TMS (ADBUS3)
EOF