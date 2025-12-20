# Wi-Fi Password Extractor + QR Code Generator

A small Windows-only Python utility that extracts saved Wi-Fi profiles (SSIDs) and their passwords from the current machine and optionally generates QR codes for each network so other devices can scan and join easily.

> ⚠️ **Important — Use ethically**  
> Only run this script on machines you own or have permission to inspect. Do NOT use it to access networks that you are not authorized to access.

---

## Features

- Lists saved Wi-Fi SSIDs on the current Windows machine.
- Prints stored passwords (if present).
- Generates QR code PNG files for networks with passwords.
- Saves QR images to a local folder named `wifi_qr_codes`.

---

## Requirements

- Python 3.8+ (recommended)
- Windows (uses `netsh wlan` commands)
- See `requirements.txt` for Python package dependencies.

Install dependencies:

```bash
# Using pip
python -m pip install -r requirements.txt

# or directly
python -m pip install qrcode[pil]
```
