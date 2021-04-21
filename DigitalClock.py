import tkinter
from time import strftime

top = tkinter.Tk()
top.title('Digital Clock')
# 0,0 makes the window non-resizable
top.resizable(0,0)

def time():
    # %p defines AM or PM
    string = strftime('%H: %M: %S %p')
    clockTime.config(text=string)
    clockTime.after(1000, time)

clockTime = tkinter.Label(top, font=('courier new', 40),
 background='red',foreground='black')
clockTime.pack(anchor='center')
time()
top.mainloop()