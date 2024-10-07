# Pomodoro Timer for macOS/Linux
import time
import os

def pomodoro_timer_unix(work_duration=25, break_duration=5, cycles=4):
    for cycle in range(cycles):
        print(f"Cycle {cycle + 1}/{cycles}: Start working for {work_duration} minutes.")
        time.sleep(work_duration * 60)
        os.system('echo -e "\a"')  # Make a beep sound on macOS/Linux
        print("Time's up! Take a break.")

        print(f"Break time! Relax for {break_duration} minutes.")
        time.sleep(break_duration * 60)
        os.system('echo -e "\a"')  # Make a beep sound on macOS/Linux
        print("Break is over! Back to work.")
    
    print("All cycles completed! Great job!")

if __name__ == "__main__":
    work_duration = int(input("Enter work duration in minutes (default is 25): ") or 25)
    break_duration = int(input("Enter break duration in minutes (default is 5): ") or 5)
    cycles = int(input("Enter number of cycles (default is 4): ") or 4)
    
    pomodoro_timer_unix(work_duration, break_duration, cycles)
