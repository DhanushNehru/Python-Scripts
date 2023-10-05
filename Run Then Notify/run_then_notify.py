import subprocess
import sys
import time


def run_then_notify(command):
    try:
        start_time = time.time()
        completed_process = subprocess.run(
            command, text=True, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT, stdin=sys.stdin)

        end_time = time.time()
        execution_time = end_time - start_time

        print('-' * 50)

        print(f"Command '{command}' completed with exit code {completed_process.returncode}.")
        print(f"Execution time: {execution_time:.2f} seconds")
        print("Standard Output:")
        print(completed_process.stdout.strip().split('\n'))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_then_notify.py 'your_command_here'")
        sys.exit(1)

    command = sys.argv[1]
    run_then_notify(command)
