# Wi-Fi Password Extractor and QR Code Generator

This Python script helps you extract saved Wi-Fi profiles and passwords from your Windows computer and generates QR codes for each network. You can scan the QR code with your phone or other devices to connect quickly.

## Features

* Lists all saved Wi-Fi networks (SSIDs)
* Retrieves saved Wi-Fi passwords (if available)
* Creates QR codes with the Wi-Fi credentials
* Saves each QR code as a PNG image

## Requirements

* Operating System: Windows only
* Python: Version 3.8 or above

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/.git
   cd Wifi_QR_Generator
   ```

2. Install the required Python libraries:

   ```bash
   pip install qrcode[pil]
   ```

## How to Use

Run the script using Python:

```bash
python WiFi_QR_Generator.py
```

After running the script:

* A message will appear showing the progress
* QR code PNG files will be saved in the same directory
* Each file will be named after the Wi-Fi network (e.g., `MyHomeWiFi.png`)

## Output Format

Each QR code contains Wi-Fi configuration details using the standard format:

```
WIFI:T:WPA;S:SSID;P:PASSWORD;;
```

You can scan this QR code using your phone to connect to the Wi-Fi automatically.

## Notes

* This script uses the `netsh` command, which only works on Windows.
* Administrator permissions may be needed to retrieve some saved Wi-Fi passwords.
* Make sure Python and pip are correctly installed and added to your system PATH.

## Example

If your computer has a saved Wi-Fi network called `OfficeWiFi`, running the script will generate:

```
OfficeWiFi.png
```

You can then open and scan this QR code on your phone to connect without typing the password.

## License

This project is licensed under the MIT License.