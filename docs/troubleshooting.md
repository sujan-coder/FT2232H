# Troubleshooting Log

## Issue 1: pyFTDI "device has no langid" Error

```bash
user@user-System-Product-Name:~/Documents$ python3 -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/labuser/.local/lib/python3.10/site-packages/pyftdi/ftdi.py", line 377, in show_devices
    devdescs = UsbTools.list_devices(url or 'ftdi:///?',
  File "/home/labuser/.local/lib/python3.10/site-packages/pyftdi/usbtools.py", line 261, in list_devices
    candidates, _ = cls.enumerate_candidates(urlparts, vdict, pdict,
  File "/home/labuser/.local/lib/python3.10/site-packages/pyftdi/usbtools.py", line 405, in enumerate_candidates
    devices = cls.find_all(vps)
  File "/home/labuser/.local/lib/python3.10/site-packages/pyftdi/usbtools.py", line 99, in find_all
    description = UsbTools.get_string(dev, dev.iProduct)
  File "/home/labuser/.local/lib/python3.10/site-packages/pyftdi/usbtools.py", line 544, in get_string
    return usb_get_string(device, stridx)
  File "/home/labuser/.local/lib/python3.10/site-packages/usb/util.py", line 309, in get_string
    raise ValueError("The device has no langid"
ValueError: The device has no langid (permission issue, no string descriptors supported or device error)
```

**Root Cause:** 
Insufficient permissions on USB device node. The kernel driver can see the device but pyFTDI cannot read string descriptors.

**Diagnosis:**
```bash
# Device visible to system
lsusb | grep 0403
Bus 001 Device 007: ID 0403:6010 Future Technology Devices...

# But pyFTDI fails
python3 -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
# Throws langid error

# Solution - Temporary:
# Apply permissions directly (adjust bus/device numbers)
sudo chmod 666 /dev/bus/usb/001/007

# Solution - Permanent:
# Install udev rule
sudo bash -c 'cat > /etc/udev/rules.d/99-ftdi.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", MODE="0666", GROUP="plugdev"
EOF'

sudo udevadm control --reload-rules
sudo udevadm trigger

# Unplug and replug device

# Verification:
python3 -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
# Should now show interfaces
```