# Pomodoro Timer with GUI

This project is a graphical user interface (GUI) application for a Pomodoro Timer, implemented in Python using the Tkinter library. The Pomodoro Timer helps users manage their work and break periods effectively based on the Pomodoro Technique. The application also includes visual features such as a progress bar and an image carousel.

## Features

- **Timer Functionality**:
  - Work sessions (25 minutes by default).
  - Short breaks (5 minutes after every cycle).
  - Long breaks (15 minutes after every 8 cycles).
  
- **Progress Bar**:
  - Displays the current progress of the work session.

- **Buttons**:
  - **Start**: Starts the timer.
  - **Pause**: Pauses the timer.
  - **Reset**: Resets the timer to the initial state.

- **Notifications**:
  - Alerts the user when transitioning between work and break periods.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `tkinter` (built into Python standard library)
  - `Pillow` (for image processing)

Install `Pillow` using pip if not already installed:
```bash
pip install pillow
```

## File Structure

- **`pomodoroTimerWithGUI.py`**: Main Python script containing the implementation.
- **Images**: A set of PNG images used in the image carousel. Place these images in the specified directory (`./Pomodoro Timer with GUI/images`).
  - `0.png`
  - `1.png`
  - `2.png`
  - ...
  - `9.png`

## How to Run

1. Ensure you have Python and the required libraries installed.
2. Place the required images in the directory `./Pomodoro Timer with GUI/images`.
3. Run the script:
   ```bash
   python pomodoroTimerWithGUI.py
   ```

## How to Use

1. **Start**: Click the "Start" button to begin the timer. The timer will start with a 25-minute work session by default.
2. **Pause**: Click the "Pause" button to pause the timer. The image carousel will also pause.
3. **Reset**: Click the "Reset" button to reset the timer to its initial state (work session of 25 minutes).
4. **Progress Bar**: Observe the progress bar at the top of the window to monitor session progress.
5. **Notifications**: Receive alerts when it’s time to switch between work and break periods.

## Customization

- **Timer Durations**: Modify the `work_time`, `short_break`, and `long_break` variables in the `PomodoroTimer` class to adjust the durations.
- **Images**: Replace the images in the `./Pomodoro Timer with GUI/images` directory with your own images. Ensure they are named `0.png`, `1.png`, ..., `10.png` and have the appropriate dimensions.
- **UI Appearance**: Customize fonts, colors, or layout by modifying the Tkinter widgets in the script.





