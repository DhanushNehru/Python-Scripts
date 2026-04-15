import time
import platform
import signal
import sys
import os
from datetime import datetime


class WebsiteBlocker:
    def __init__(
        self, websites: list[str], start_hour: int = 8, end_hour: int = 16
    ) -> None:
        self.websites = set(websites)
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.redirect = "127.0.0.1"
        self.hosts_path = self.get_hosts_path()
        self.is_blocked = False

    # ----------------------------
    # OS handling
    # ----------------------------
    def get_hosts_path(self) -> str:
        if platform.system() == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        return "/etc/hosts"

    # ----------------------------
    # Admin check (IMPORTANT)
    # ----------------------------
    def check_admin(self) -> None:
        try:
            if platform.system() == "Windows":
                import ctypes
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    raise PermissionError
            else:
                if os.geteuid() != 0:
                    raise PermissionError
        except Exception:
            print("\033[91m❌ Please run the script as administrator/root\033[0m")
            sys.exit(1)

    # ----------------------------
    # Time logic
    # ----------------------------
    def is_working_hours(self) -> bool:
        now = datetime.now()
        return self.start_hour <= now.hour < self.end_hour

    # ----------------------------
    # Blocking logic
    # ----------------------------
    def block_websites(self) -> None:
        try:
            with open(self.hosts_path, "r+") as file:
                content = file.read()

                for site in self.websites:
                    entry = f"{self.redirect} {site}"
                    if entry not in content:
                        file.write(entry + "\n")

        except PermissionError:
            self.admin_error()

    # ----------------------------
    # Unblocking logic
    # ----------------------------
    def unblock_websites(self) -> None:
        try:
            with open(self.hosts_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)

                for line in lines:
                    if not any(site in line for site in self.websites):
                        file.write(line)

                file.truncate()

        except PermissionError:
            self.admin_error()

    # ----------------------------
    # Error helpers
    # ----------------------------
    def admin_error(self):
        print("\033[91m❌ Permission denied. Run as admin/root.\033[0m")
        sys.exit(1)

    # ----------------------------
    # Cleanup on exit (Ctrl + C)
    # ----------------------------
    def cleanup(self, signum=None, frame=None) -> None:
        print("\n\033[96m🧹 Cleaning up hosts file before exit...\033[0m")
        try:
            self.unblock_websites()
        except Exception:
            pass
        print("\033[92m✅ Cleanup done. Exiting safely.\033[0m")
        sys.exit(0)

    # ----------------------------
    # Main loop
    # ----------------------------
    def run(self) -> None:
        print("\033[92m🚀 Website Blocker running...\033[0m")

        # ✔ Ensure admin FIRST
        self.check_admin()

        # ✔ Handle Ctrl + C
        signal.signal(signal.SIGINT, self.cleanup)

        # ✔ Initial state (print ONCE)
        if self.is_working_hours():
            print("\033[91m🔒 Blocking websites...\033[0m")
            self.block_websites()
            self.is_blocked = True
        else:
            print("\033[92m🔓 Unblocking websites...\033[0m")
            print("\033[93m⏰ Outside of working hours.\033[0m")
            self.unblock_websites()
            self.is_blocked = False

        # ✔ Loop (ONLY reacts to change)
        while True:
            try:
                should_block = self.is_working_hours()

                if should_block and not self.is_blocked:
                    print("\033[91m🔒 Blocking websites...\033[0m")
                    self.block_websites()
                    self.is_blocked = True

                elif not should_block and self.is_blocked:
                    print("\033[92m🔓 Unblocking websites...\033[0m")
                    print("\033[93m⏰ Outside of working hours.\033[0m")
                    self.unblock_websites()
                    self.is_blocked = False

                time.sleep(60)

            except KeyboardInterrupt:
                self.cleanup()

            except Exception as e:
                print(f"\033[91m⚠️ Unexpected error: {e}\033[0m")
                time.sleep(5)


# ----------------------------
# User input
# ----------------------------
def get_user_websites() -> list[str]:
    options = {
        "1": "facebook.com",
        "2": "youtube.com",
        "3": "instagram.com",
        "4": "twitter.com",
        "5": "gmail.com",
        "6": "\033[33mCustom: Enter your own domains\033[0m",
    }

    print("- Select websites to block (comma separated):")
    for key, value in options.items():
        print(f"{key}) {value}")

    print()
    selected: list[str] = []
    choices = input("Your choice: ").split(",")

    for choice in choices:
        choice = choice.strip()

        if choice in options and choice != "6":
            site = options[choice]
            selected.append(site)
            selected.append("www." + site)

        elif choice == "6":
            custom_sites = input("Enter custom domains (comma separated): ")
            for site in custom_sites.split(","):
                site = site.strip()
                if site:
                    selected.append(site)
                    selected.append("www." + site)

        else:
            print(f"\033[91mInvalid option: {choice}\033[0m")
            return []

    return selected


# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":

    print("\n\033[33m⚠️ Run this script as administrator/root.\033[0m\n")

    websites: list[str] = []
    while not websites:
        websites = get_user_websites()

    try:
        start = int(input("Enter start hour (0-23) [default 8]: ") or 8)
        end = int(input("Enter end hour (0-23) [default 16]: ") or 16)

        if not (0 <= start <= 23 and 0 <= end <= 23):
            raise ValueError

    except ValueError:
        print("\033[91mInvalid input. Using default (8-16).\033[0m")
        start, end = 8, 16

    blocker = WebsiteBlocker(websites, start, end)
    blocker.run()
