Wi-Fi Password Retrieval 🔑📡
A Python script to retrieve saved Wi-Fi passwords on Windows systems. Useful for network troubleshooting or recovering forgotten passwords.

Features ✨
Retrieves all saved Wi-Fi profiles on your machine.

Displays SSID (network name) and password in clear text.

Lightweight and no external dependencies (uses built-in subprocess).

Prerequisites ⚙️
Operating System: Windows 10/11.

Python: 3.6+ (tested on 3.10).

Installation & Usage 🚀
-----------------------
1. Clone the repository (or download the script):
-->bash<--
git clone https://github.com/DhanushNehru/Python-Scripts.git
cd Python-Scripts/Networking/WiFi_Password_Retriever
-----------------------
2. Run the script:
-->bash<--
python wifi_password_retriever.py
-----------------------
3. Output Example:
Saved Wi-Fi Passwords:
Profile: Home_WiFi       Password: FluffyBunny123
Profile: Office_Network  Password: Secure@2024
Profile: Starbucks       Password: LatteWithExtraShots
How It Works 🔍
The script uses Windows' native netsh command to:

List all saved Wi-Fi profiles.

Extract passwords (requires admin privileges for decryption).

Notes ⚠️
Admin Rights Required: Run the script as Administrator to access passwords.

Security: Passwords are stored in plaintext in the terminal output. Use responsibly!

Linux/Mac: Not supported (uses Windows-specific netsh).

License 📜
MIT License - Use freely, but credit the original author.

Contribution 🤝
Found a bug? Want to improve it?

Fork the repo.

Create a PR with your changes.

Follow the contribution guidelines.

Disclaimer: Use only on networks you own or have permission to access.
