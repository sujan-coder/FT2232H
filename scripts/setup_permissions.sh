#!/bin/bash
# Apply permissions to currently connected FT2232H

set -e

# Find the device
BUS=$(lsusb | grep 0403:6010 | awk '{print $2}')
DEV=$(lsusb | grep 0403:6010 | awk '{print $4}' | tr -d ':')

if [ -z "$BUS" ] || [ -z "$DEV" ]; then
    echo "ERROR: FT2232H not found"
    echo "Run 'lsusb | grep 0403' to verify connection"
    exit 1
fi

DEVICE_PATH="/dev/bus/usb/$BUS/$DEV"

if [ -e "$DEVICE_PATH" ]; then
    sudo chmod 666 "$DEVICE_PATH"
    echo "✓ Permissions applied to $DEVICE_PATH"
    echo "✓ Run: python3 -c 'from pyftdi.ftdi import Ftdi; Ftdi.show_devices()'"
else
    echo "ERROR: Device path $DEVICE_PATH not found"
    exit 1
fi
