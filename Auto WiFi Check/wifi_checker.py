import ctypes
import subprocess
import sys
import time
from datetime import datetime
import schedule as sc


def enable():
    subprocess.call("netsh interface set interface Wi-Fi enabled")
    print("Turning On the laptop WiFi")

def disable():
    subprocess.call("netsh interface set interface Wi-Fi disabled")
    print("Turning Off the laptop WiFi")


    
def job():
    if subprocess.call("netsh interface set interface Wi-Fi enabled") == 0:
        print("WiFi is enabled and connected to internet")
        hostname = "www.google.com"
        response = subprocess.call(f"ping -n 1 {hostname}") # Using f-string for cleaner string formatting
        if response == 1:
            print("Your Connection is not working")

            attempt_counter = 0
            max_attempts = 3
            
            while attempt_counter < max_attempts:
                print(f"Attempt {attempt_counter} to reconnect...")

                disable()
                time.sleep(1)
                enable()

                time.sleep(5)

                response = subprocess.call(f"ping -n 1 {hostname}")
                if response == 0:
                    print("Reconnection successful!")
                    break
                elif response == 1:
                    print(f"Reconnection attempt {attempt_counter} failed.")
                
                if attempt_counter == max_attempts and response != 0:
                    print(f"Failed to reconnect after {attempt_counter} attemps.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # job()
    sc.every(50).seconds.do(job)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


while True:
    sc.run_pending()
    time.sleep(1)