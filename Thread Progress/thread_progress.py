import threading
import time

# Shared variable
progress = 0
lock = threading.Lock()

def increase_by_10():
    global progress
    for _ in range(10):
        time.sleep(0.01)  # Simulate work
        with lock:  # Only one thread can change `progress` at a time
            progress += 10
            print(f"{threading.current_thread().name}: progress = {progress}%")

# Create two threads
thread1 = threading.Thread(target=increase_by_10, name="Thread-1")
thread2 = threading.Thread(target=increase_by_10, name="Thread-2")

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print(f"Final progress: {progress}%")
