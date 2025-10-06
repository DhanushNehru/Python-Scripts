import pyperclip
import tkinter as tk
from tkinter import scrolledtext
import time
import threading
import os
import queue

history_file = os.path.join(os.path.expanduser("~"), "clipboard_history.txt")

if not os.path.exists(history_file):
    with open(history_file, "w", encoding="utf-8") as f:
        f.write("Clipboard History:\n\n")

last_text = ""

gui_queue = queue.Queue()

MAX_HISTORY_LINES = 1000


def monitor_clipboard():
    global last_text
    while True:
        try:
            text = pyperclip.paste()
        except Exception:
            time.sleep(1)
            continue 
        if text != last_text and text.strip() != "":
            last_text = text
            timestamped_text = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {text}\n"
            try:
                with open(history_file, "a", encoding="utf-8") as f:
                    f.write(timestamped_text)
            except Exception:
                pass  
            gui_queue.put(timestamped_text)
        time.sleep(1)

def limit_file_size():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        header = lines[:2]
        history = lines[2:]
        if MAX_HISTORY_LINES is not None and len(history) > MAX_HISTORY_LINES:
            history = history[-MAX_HISTORY_LINES:]
            with open(history_file, "w", encoding="utf-8") as f:
                f.writelines(header + history)
    except Exception:
        pass


def process_queue():
    while not gui_queue.empty():
        text = gui_queue.get()
        text_area.configure(state='normal')
        text_area.insert(tk.END, text)
        text_area.configure(state='disabled')
        text_area.yview(tk.END)
    root.after(100, process_queue)

#
def clear_history():
    text_area.configure(state='normal')
    text_area.delete(1.0, tk.END)
    text_area.configure(state='disabled')
    try:
        with open(history_file, "w", encoding="utf-8") as f:
            f.write("Clipboard History:\n\n")
    except Exception:
        pass

root = tk.Tk()
root.title("Clipboard Manager")
root.geometry("600x400")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
text_area.pack(expand=True, fill='both', padx=10, pady=10)

clear_button = tk.Button(root, text="Clear History", command=clear_history)
clear_button.pack(pady=5)


limit_file_size()
try:
    with open(history_file, "r", encoding="utf-8") as f:
        text_area.configure(state='normal')
        text_area.insert(tk.END, f.read())
        text_area.configure(state='disabled')
except Exception:
    pass


thread = threading.Thread(target=monitor_clipboard, daemon=True)
thread.start()


root.after(100, process_queue)

root.mainloop()
