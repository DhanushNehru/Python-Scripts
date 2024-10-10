import time
import tkinter as tk 
from tkinter import messagebox 

def start():
    work_time = 25*60
    break_time = 5*60 
    long_break = 15*60 

    cycles = 0

    def countDown(t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            timer_label.config(text=timer) 
            root.update()
            time.sleep(1)
            t-=1 
        
    def startCycle():
        nonlocal cycles 
        if cycles < 4:
            countDown(work_time)
            messagebox.showinfo("Time's up!", "Take a 5-minute break!")
            countDown(break_time) 
            cycles +=1 
            startCycle()
        else:
            countDown(work_time)
            messagebox.showinfo("Time's up!", "Take a 15-minute break!")
            countDown(long_break)
            cycles = 0
        
    startCycle()




root = tk.Tk()
root.title("Pomodoro Timer") 

timer_label = tk.Label(root, font = ('Helvetica', 48), text="25:00")
timer_label.pack(pady=20)

start_btn = tk.Button(root, text="Start Pomdoro", command=start) 
start_btn.pack()

root.mainloop()
