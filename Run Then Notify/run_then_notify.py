import subprocess
import sys
import time
import socket


def run_then_notify(command):
    try:
        start_time = time.time()
        completed_process = subprocess.run(
            command,
            text=True,
            shell=True,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
            stdin=sys.stdin
        )

        end_time = time.time()
        execution_time = end_time - start_time

        notif_subject = '[Run completed] Your command finished execution'
        notif_message = f"Command '{command}' completed\n\
            \twith exit code {completed_process.returncode}\n\
            \tin {execution_time:.2f} seconds\n\
            \n\
            This is an automated message sent from your device {socket.gethostname()}"

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_then_notify.py 'your_command_here'")
        sys.exit(1)

    command = sys.argv[1]
    run_then_notify(command)
