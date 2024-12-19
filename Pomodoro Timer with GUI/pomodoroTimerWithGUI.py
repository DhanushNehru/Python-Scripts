import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import time


class PomodoroTimer:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Pomodoro Timer")

        # Initialize time settings (in seconds)
        self.work_time = 25 * 60  # Work time 25 minutes
        self.short_break = 5 * 60  # Short break time 5 minutes
        self.long_break = 15 * 60  # Long break time 15 minutes
        self.current_time = self.work_time  # Default to work time

        self.is_running = False  # Track if the timer is running
        self.cycle_count = 0  # Track the count of work and rest cycles
        self.work = True  # Track if the timer is work-timer

        # Create UI elements
        self.label = tk.Label(
            root, text="Pomodoro Timer", font=("Helvetica", 20)
        )  # Title label
        self.label.pack(pady=10)

        self.timer_label = tk.Label(
            root, text=self.format_time(self.current_time), font=("Helvetica", 48)
        )  # Countdown label
        self.timer_label.pack(pady=10)

        # Use Frame container to manage button layout
        progress_frame = tk.Frame(root)
        progress_frame.pack(
            side=tk.TOP, pady=10
        )  # Place the button container at the bottom of the window

        # Create progress bar
        self.progress = ttk.Progressbar(
            progress_frame, orient="horizontal", length=300, mode="determinate"
        )
        self.progress.pack(side=tk.LEFT, pady=5, padx=20)
        self.progress["maximum"] = (
            100  # Set the maximum value of the progress bar to 100
        )

        # adjust the location of progress
        empty_image = ImageTk.PhotoImage(
            Image.open("C:/Users/Ming/Desktop/empty.png").resize((300, 9))
        )
        empty_image_label = tk.Label(progress_frame, image=empty_image)
        empty_image_label.pack(pady=0, padx=10)

        # Use Frame container to manage button layout
        button_frame = tk.Frame(root)
        button_frame.pack(
            side=tk.BOTTOM, pady=10
        )  # Place the button container at the bottom of the window
        button_width = 20

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            font=("Helvetica", 14),
            width=button_width,
            command=self.start_timer,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=("Helvetica", 14),
            width=button_width,
            command=self.pause_timer,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("Helvetica", 14),
            width=button_width,
            command=self.reset_timer,
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Use Frame's pack attribute to center the button container
        button_frame.pack(anchor="center")

        self.update_timer()  # Start updating the timer

        self.current_image_index = 0  # set current image index
        # input image
        self.images = [
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/0.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/1.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/2.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/3.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/4.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/5.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/6.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/7.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/8.png").resize((864, 286))
            ),
            ImageTk.PhotoImage(
                Image.open("./Pomodoro Timer with GUI/images/9.png").resize((864, 286))
            ),
            # ImageTk.PhotoImage(
            #     Image.open("C:/Users/Ming/Desktop/10.png").resize((864, 286))
            # ),
        ]

        self.image_label = tk.Label(root, image=self.images[self.current_image_index])
        self.image_label.pack(pady=0, anchor="center")

    def change_image(self):  # Image switch function
        if self.is_running:
            # Update the current image index
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            # Update the image in the Label control
            self.image_label.config(image=self.images[self.current_image_index])
            # Switch to the next image after 100 milliseconds
            self.root.after(100, self.change_image)

    def format_time(self, seconds):
        # Format the number of seconds into MM:SS format
        mins = seconds // 60  # Number of minutes
        secs = seconds % 60  # Number of seconds
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        # Timer update logic
        if self.is_running and self.current_time > 0:
            self.current_time -= 1  # Decrease by 1 second every second
            self.timer_label.config(
                text=self.format_time(self.current_time)
            )  # Update the countdown display
            if self.work:
                self.update_progress()  # Update the progress bar
            self.root.after(1000, self.update_timer)  # Call itself once a second
        elif self.current_time == 0:
            # Handling logic after the timer ends
            self.is_running = False
            self.cycle_count += 1  # Increase cycle count
            self.notify_user()  # Notify the user of the next step

    def update_progress(self):
        # Update the progress bar
        progress_value = (self.current_time / self.work_time) * 100
        self.progress["value"] = progress_value

    def notify_user(self):
        # Notify the user to enter different states based on cycle count
        if self.work:  # i
            self.work = False
            if self.cycle_count % 8 == 0:  # Enter long rest every 8 cycles
                self.current_time = self.long_break
                messagebox.showinfo(
                    "Pomodoro Timer", "You did it. Time for a long break!"
                )
            else:  # Otherwise, enter short rest
                self.current_time = self.short_break
                messagebox.showinfo("Pomodoro Timer", "You did it. Take a break!")
        else:
            self.work = True
            self.current_time = self.work_time
            messagebox.showinfo("Pomodoro Timer", "Time to fight!!!")

        self.timer_label.config(
            text=self.format_time(self.current_time)
        )  # Update display to new timing time

    def start_timer(self):
        # Start the timer
        if not self.is_running:  # If the timer is not running
            self.is_running = True
            self.update_timer()  # Start the countdown
            if self.work:
                self.change_image()

    def pause_timer(self):
        # Pause the timer
        self.is_running = False
        self.current_image_index = 0
        self.image_label.config(image=self.images[self.current_image_index])
        messagebox.showinfo(
            "Pomodoro Timer",
            "PAUSE!!!\n But Charmeleon is still waiting your command!!!",
        )

    def reset_timer(self):
        # Reset the timer to its initial state
        self.is_running = False
        self.current_time = self.work_time  # Reset to work time
        self.current_image_index = 0
        self.image_label.config(image=self.images[self.current_image_index])
        self.cycle_count = 0  # Reset cycle count
        self.timer_label.config(
            text=self.format_time(self.current_time)
        )  # Update display
        self.progress["value"] = 0  # Reset progress bar
        self.work = True


if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = PomodoroTimer(root)  # Initialize the Pomodoro Timer app
    root.mainloop()  # Start the main loop
