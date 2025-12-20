import subprocess
import re
import qrcode
import os

def get_wifi_profiles():
    """Get all saved Wi-Fi profile names"""
    try:
        profiles_data = subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data)
        return profiles
    except subprocess.CalledProcessError:
        print("[ERROR] Unable to fetch Wi-Fi profiles. Make sure you are running on Windows.")
        return []

def get_wifi_password(profile_name):
    """Get Wi-Fi password for a given profile"""
    try:
        profile_info = subprocess.check_output(
            ["netsh", "wlan", "show", "profile", profile_name, "key=clear"],
            text=True
        )
        password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info)
        return password_match.group(1) if password_match else None
    except subprocess.CalledProcessError:
        return None

def generate_qr_code(ssid, password):
    """Generate QR code for Wi-Fi credentials"""
    qr_folder = "wifi_qr_codes"
    os.makedirs(qr_folder, exist_ok=True)
    
    qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr_img = qrcode.make(qr_data)
    qr_img.save(os.path.join(qr_folder, f"{ssid}.png"))

def main():
    print("\n=== Wi-Fi Password Extractor ===\n")

    wifi_profiles = get_wifi_profiles()
    if not wifi_profiles:
        print("No Wi-Fi profiles found.")
        return

    for profile in wifi_profiles:
        password = get_wifi_password(profile)
        if password:
            print(f"SSID: {profile}\nPassword: {password}\n")
            generate_qr_code(profile, password)
        else:
            print(f"SSID: {profile}\nPassword: Not Found or Open Network\n")

    print("\nQR codes saved in 'wifi_qr_codes' folder.\n")

if __name__ == "__main__":
    main()
