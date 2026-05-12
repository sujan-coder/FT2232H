# FT2232H Pinout Reference

## Channel A (Interface 1)

| Pin | Name | Function | Notes |
|-----|------|----------|-------|
| ADBUS0 | TXD / TCK / SK | UART TX / JTAG TCK / SPI CLK | Default: UART TX |
| ADBUS1 | RXD / TDI / DO | UART RX / JTAG TDI / SPI MOSI | Default: UART RX |
| ADBUS2 | RTS# / TDO / DI | UART RTS / JTAG TDO / SPI MISO | |
| ADBUS3 | CTS# / TMS / CS# | UART CTS / JTAG TMS / SPI CS | |
| ADBUS4 | DTR# / GPIO | UART DTR | Bit-bang capable |
| ADBUS5 | DSR# / GPIO | UART DSR | Bit-bang capable |
| ADBUS6 | DCD# / GPIO | UART DCD | Bit-bang capable |
| ADBUS7 | RI# / GPIO | UART RI | Bit-bang capable |

## Channel B (Interface 2)

| Pin | Name | Function | Notes |
|-----|------|----------|-------|
| BDBUS0 | TXD / TCK / SK | UART TX / JTAG TCK / SPI CLK | Same as Channel A |
| BDBUS1 | RXD / TDI / DO | UART RX / JTAG TDI / SPI MOSI | |
| BDBUS2 | RTS# / TDO / DI | UART RTS / JTAG TDO / SPI MISO | |
| BDBUS3 | CTS# / TMS / CS# | UART CTS / JTAG TMS / SPI CS | |
| BDBUS4 | DTR# / GPIO | UART DTR | |
| BDBUS5 | DSR# / GPIO | UART DSR | |
| BDBUS6 | DCD# / GPIO | UART DCD | |
| BDBUS7 | RI# / GPIO | UART RI | |

## Configuration Modes

| Mode | Description | Typical Use |
|------|-------------|-------------|
| UART | Async serial | 2 independent serial ports |
| MPSSE | Multi-Protocol Sync Serial Engine | JTAG, SPI, I2C |
| FIFO | Parallel interface | High-speed data transfer |
| Bit-bang | GPIO control | Custom protocols |

## Current Configuration

ftdi://ftdi:2232:1:7/1  (Dual RS232-HS)
ftdi://ftdi:2232:1:7/2  (Dual RS232-HS)