import time
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def countdown(minutes, name):
    print(name)
    seconds = minutes * 60
    bar_format = Fore.GREEN + '{l_bar}{bar}| {remaining} seconds' + Style.RESET_ALL
    with tqdm(total=seconds, desc='Time remaining', bar_format=bar_format, ncols=100) as pbar:
        while seconds:
            mins, secs = divmod(seconds, 60)
            timer = f'{mins:02d}:{secs:02d}'
            print(Fore.YELLOW + timer, end='\r' + Style.RESET_ALL)
            time.sleep(1)
            seconds -= 1
            pbar.update(1)
    print(Fore.RED + '\nTime is up!' + Style.RESET_ALL)

# Example usage:
countdown(1,"Work Session")  # for a 1-minute work session
countdown(1,"Break")  # for a 1-minute break

# Example use, running for infinity:

while True: 
    countdown(25,"Work Session")
    countdown(5, "Break")
