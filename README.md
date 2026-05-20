# FTDI Board Learning - Custom FT2232H PCB

## Current Focus Board
**Custom FT2232H PCB** (FTDI_ADAPTOR_BOARD_REVB)

### Board Specifications
- **Chip:** FT2232H
- **VID:PID:** 0403:6010
- **Exposed Pins:** ADBUS0-7 only (8 pins on J2 header)
- **Labels:** 1L0 through 1L7

### Connector J2 Pinout

| J2 Pin | Label | FT2232H | Function |
|--------|-------|---------|----------|
| 1 | 1L0 | ADBUS0 | TCK / SPI_CLK |
| 2 | 1L1 | ADBUS1 | TDI / SPI_MOSI / TX |
| 3 | 1L2 | ADBUS2 | TDO / SPI_MISO / RX |
| 4 | 1L3 | ADBUS3 | TMS / SPI_CS |
| 5 | 1L4 | ADBUS4 | GPIO |
| 6 | 1L5 | ADBUS5 | GPIO |
| 7 | 1L6 | ADBUS6 | GPIO |
| 8 | 1L7 | ADBUS7 | GPIO |
| 9 | - | GND | Ground |
| 10 | - | VCC | Power (3.3V/5V) |

### Quick Start

```bash
# Detection
python3 boards/custom-ft2232h/src/detection/detect_ftdi.py

# LED test
python3 boards/custom-ft2232h/src/bitbang/led_test.py

# UART loopback (connect J2 pin2 → J2 pin3)
python3 boards/custom-ft2232h/src/uart/loopback.py