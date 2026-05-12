# FT2232H - Dual USB to Serial/FIFO Bridge

## Overview
FT2232H development and testing utilities. Documentation for setup, pinout, and troubleshooting.

## Quick Start

```bash
# Clone
git clone https://github.com/sujan-coder/FT2232H.git
cd FT2232H

# Install dependencies
pip install pyftdi pyusb pyserial

# Setup permissions
./scripts/setup_permissions.sh

# Verify detection
python3 src/detection/detect_ftdi.py