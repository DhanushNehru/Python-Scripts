## Thread Progress

This script demonstrates the use of **Python threads** to simulate parallel progress updates using a shared variable and a `Lock` to avoid race conditions.

### 🧠 Concepts Covered

- Python `threading.Thread`
- Synchronization with `threading.Lock`
- Global variables and shared state
- Simulated concurrent work using `time.sleep`

### 📝 Description

Two threads increment a shared `progress` variable by `10` in a loop. A `Lock` ensures only one thread can modify the shared variable at a time, preventing race conditions.

### 👉 Run
```
python3 thread_progress.py
```
