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
        response = subprocess.call("ping -n 1 " + hostname)
        if response == 1:
            print("Your Connection is not working")
            disable()
            time.sleep(1)
            enable()

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