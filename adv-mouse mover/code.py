import win32api
import win32con
import time
import random
import threading
import logging

# Set up logging
logging.basicConfig(filename='click_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    logging.info(f'Clicked at: ({x}, {y})')

def clicker(click_count, x_min, x_max, y_min, y_max, interval):
    for _ in range(click_count):
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        click(x, y)
        time.sleep(interval)

def main():
    # User-defined settings
    click_count = 10  # Number of clicks
    x_min, x_max = 0, 1920  # Screen width range (example for 1920x1080)
    y_min, y_max = 0, 1080  # Screen height range (example for 1920x1080)
    interval = 2  # Time in seconds between clicks

    print("Clicking will start...")
    click_thread = threading.Thread(target=clicker, args=(click_count, x_min, x_max, y_min, y_max, interval))
    click_thread.start()

    try:
        while click_thread.is_alive():
            time.sleep(1)  # Keep the main thread alive while clicks are happening
    except KeyboardInterrupt:
        print("Clicking stopped by user.")
        # Optionally, you could set a flag here to stop the clicker thread gracefully.

if __name__ == "__main__":
    main()
