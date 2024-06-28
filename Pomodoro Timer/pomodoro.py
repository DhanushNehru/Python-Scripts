import time

def countdown(minutes):
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end='\r')
        time.sleep(1)
        seconds -= 1
    print('Time is up!')

# Example usage:
countdown(1)  # for a 25-minute work session
countdown(1)   # for a 5-minute break
