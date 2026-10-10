# Pomodoro Timer for Linux/macOS/Windows

import time
import platform

def alert():
    """Play an alert sound based on the operating system."""
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 1000)
    else:
        print("\a", end="", flush=True)


def pomodoro_timer(work_duration=25, break_duration=5, cycles=4):
    for cycle in range(cycles):
        print(f"\nCycle {cycle + 1}/{cycles}: Start working for {work_duration} minutes.")
        time.sleep(work_duration * 60)

        alert()
        print("\nTime's up! Take a break.")

        print(f"Break time! Relax for {break_duration} minutes.")
        time.sleep(break_duration * 60)

        alert()
        print("\nBreak is over! Back to work.")

    print("\nAll cycles completed! Great job!")


if __name__ == "__main__":
    work_duration = int(input("Enter work duration in minutes (default is 25): ") or 25)
    break_duration = int(input("Enter break duration in minutes (default is 5): ") or 5)
    cycles = int(input("Enter number of cycles (default is 4): ") or 4)

    pomodoro_timer(work_duration, break_duration, cycles)