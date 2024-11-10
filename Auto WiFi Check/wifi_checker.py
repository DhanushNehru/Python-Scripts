import ctypes
import subprocess
import sys
import time
import logging
from datetime import datetime
import schedule as sc

# Set up logging to log to a file with timestamps
logging.basicConfig(filename='wifi_status_log.txt', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def enable():
    subprocess.call("netsh interface set interface Wi-Fi enabled")
    print("Turning On the laptop WiFi")
    logging.info("WiFi enabled")

def disable():
    subprocess.call("netsh interface set interface Wi-Fi disabled")
    print("Turning Off the laptop WiFi")
    logging.info("WiFi disabled")

def job():
    if subprocess.call("netsh interface set interface Wi-Fi enabled") == 0:
        print("WiFi is enabled and connected to internet")
        logging.info("WiFi is enabled and connected to the internet.")
        
        hostname = "www.google.com"
        response = subprocess.call(f"ping -n 1 {hostname}") # Using f-string for cleaner string formatting
        
        if response == 1:
            print("Your Connection is not working")
            logging.warning("WiFi connection not working, ping failed.")

            attempt_counter = 0
            max_attempts = 3
            
            while attempt_counter < max_attempts:
                print(f"Attempt {attempt_counter} to reconnect...")
                logging.info(f"Attempt {attempt_counter} to reconnect...")
                
                disable()
                time.sleep(1)
                enable()

                time.sleep(5)

                response = subprocess.call(f"ping -n 1 {hostname}")
                if response == 0:
                    print("Reconnection successful!")
                    logging.info("Reconnection successful!")
                    break
                elif response == 1:
                    print(f"Reconnection attempt {attempt_counter} failed.")
                    logging.warning(f"Reconnection attempt {attempt_counter} failed.")
                
                attempt_counter += 1

                if attempt_counter == max_attempts and response != 0:
                    print(f"Failed to reconnect after {attempt_counter} attempts.")
                    logging.error(f"Failed to reconnect after {attempt_counter} attempts.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    sc.every(50).seconds.do(job)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

while True:
    sc.run_pending()
    time.sleep(1)
