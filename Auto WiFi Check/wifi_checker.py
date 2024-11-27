import ctypes
import subprocess
import sys
import time
import logging
import schedule as sc

# Create the log file if it doesn't already exist
LOG_FILE = "wifi_status_log.txt"
PING_HOST = "www.google.com"

try:
    with open(LOG_FILE, 'x') as file:
        file.write("Logs:\n")
    print(f"File '{LOG_FILE}' created successfully.")
except FileExistsError:
    print(f"File '{LOG_FILE}' already exists.")

# Set up logging to log to a file with timestamps
logging.basicConfig(filename=LOG_FILE, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s', 
                    filemode='a')  # Append mode

def enable():
    try:
        subprocess.call("netsh interface set interface Wi-Fi enabled", shell=True)
        print("Turning On the laptop WiFi")
        logging.info("WiFi enabled")
    except Exception as e:
        print(f"Failed to enable WiFi: {e}")
        logging.error(f"Failed to enable WiFi: {e}")

def disable():
    try:
        subprocess.call("netsh interface set interface Wi-Fi disabled", shell=True)
        print("Turning Off the laptop WiFi")
        logging.info("WiFi disabled")
    except Exception as e:
        print(f"Failed to disable WiFi: {e}")
        logging.error(f"Failed to disable WiFi: {e}")

def job():
    try:
        subprocess.call("netsh interface set interface Wi-Fi enabled", shell=True)
        print("WiFi is enabled and connected to internet")
        logging.info("WiFi is enabled and connected to the internet.")
        
        response = subprocess.call(f"ping -n 1 {PING_HOST}", shell=True)
        
        if response == 1:
            print("Your Connection is not working")
            logging.warning("WiFi connection not working, ping failed.")

            attempt_counter = 0
            max_attempts = 3

            while attempt_counter < max_attempts:
                print(f"Attempt {attempt_counter + 1} to reconnect...")
                logging.info(f"Attempt {attempt_counter + 1} to reconnect...")
                
                disable()
                time.sleep(1)
                enable()

                time.sleep(5)

                response = subprocess.call(f"ping -n 1 {PING_HOST}", shell=True)
                if response == 0:
                    print("Reconnection successful!")
                    logging.info("Reconnection successful!")
                    break
                else:
                    print(f"Reconnection attempt {attempt_counter + 1} failed.")
                    logging.warning(f"Reconnection attempt {attempt_counter + 1} failed.")
                
                attempt_counter += 1

            if attempt_counter == max_attempts and response != 0:
                print(f"Failed to reconnect after {max_attempts} attempts.")
                logging.error(f"Failed to reconnect after {max_attempts} attempts.")
    except Exception as e:
        print(f"Error during WiFi check: {e}")
        logging.error(f"Error during WiFi check: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(f"Admin check failed: {e}")
        return False

if is_admin():
    sc.every(50).seconds.do(job)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

while True:
    sc.run_pending()
    time.sleep(1)
