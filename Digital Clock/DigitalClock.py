import tkinter as tk
from time import strftime

# Create main window
top = tk.Tk()
top.title('🕒 Digital Clock')
top.geometry('500x150')
top.resizable(0, 0)
top.configure(bg='#1e1e2f')  # Dark background

# Function to update time
def time():
    string = strftime('%I:%M:%S %p')  # 12-hour format with AM/PM
    clock_label.config(text=string)
    clock_label.after(1000, time)

# Digital clock label styling
clock_label = tk.Label(top, font=('Segoe UI', 48, 'bold'),
                       background='#1e1e2f',
                       foreground='#00FFCC',
                       padx=20, pady=20)
clock_label.pack(anchor='center', expand=True)

# Start clock
time()

# Start the main loop
top.mainloop()
