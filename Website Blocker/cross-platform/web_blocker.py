import time
import platform
from datetime import datetime as dt

# Detect OS and set hosts path
if platform.system() == "Windows":
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"

redirect = "127.0.0.1"

website_list = [
    "www.facebook.com", "facebook.com"]

START_HOUR = 8
END_HOUR = 16

while True:
    now = dt.now()
    start = dt(now.year, now.month, now.day, START_HOUR)
    end = dt(now.year, now.month, now.day, END_HOUR)

    if start < now < end:
        print("Working hours...")

        with open(hosts_path, "r+") as file:
            content = file.read()

            for website in website_list:
                if website not in content:
                    file.write(f"{redirect} {website}\n")

    else:
        with open(hosts_path, "r+") as file:
            content = file.readlines()
            file.seek(0)

            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)

            file.truncate()

    time.sleep(3600)  # Check every hour