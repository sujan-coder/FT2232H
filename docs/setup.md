# Environment Setup

## Prerequisites
- Linux (Ubuntu/Debian)
- Python 3.10+
- FT2232H hardware connected via USB

## Installation

### 1. Install Required Packages
```bash
pip install pyftdi pyusb pyserial

```
### 2. Configure USB Permissions
Create udev rule:
```bash
sudo bash -c 'cat > /etc/udev/rules.d/99-ftdi.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", MODE="0666", GROUP="plugdev"
EOF'

sudo udevadm control --reload-rules
sudo udevadm trigger

```

### 3. Verify Installation
Run detection
```bash
python3 -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
```
### Temporary Fix (If udev not working)
Find your device:
```bash
lsusb | grep 0403
```
Apply permissions (replace BUS and DEV with actual values)
```bash
sudo chmod 666 /dev/bus/usb/001/007
```
### Hardware Reference
Channel A: Interface 1
Channel B: Interface 2
```bash
user@user-System-Product-Name:~/Documents$ python3 -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
Available interfaces:
  ftdi://ftdi:2232:1:7/1  (Dual RS232-HS)
  ftdi://ftdi:2232:1:7/2  (Dual RS232-HS)
```