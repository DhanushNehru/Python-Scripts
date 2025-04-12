# Hardware Resource Monitor in Python

## Description

This project is a Python-based hardware resource monitoring tool that provides real-time information about the system's hardware specifications and resource usage. It uses the `psutil` and `pynvml` libraries to gather data about the CPU, RAM, disk space, and GPU.

## Features

- Detects and displays GPU specifications, including:
  - GPU name
  - Total memory (in GB)
  - Used memory (in GB)
- Detects and displays system specifications, including:
  - Total and used RAM (in GB)
  - Available disk space (in GB)
  - Number of CPU cores
  - CPU usage percentage
- Continuously monitors hardware resources with a customizable update interval.
- Displays data in a clean and user-friendly format in the console.

## Requirements

The following Python libraries are required to run the project:

- `psutil`
- `pynvml`
- `typing` (built-in for Python 3.5+)

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository or download the project files.
2. Install the required dependencies using the `requirements.txt` file.
3. Run the `hardware_detector.py` script to start monitoring hardware resources:

```bash
python hardware_detector.py
```

4. Press `Ctrl+C` to stop the monitoring process.

## Notes

- Ensure that your system has a CUDA-enabled GPU with the correct drivers installed to retrieve GPU information.
- The script clears the console output on each update for a clean display. This behavior may vary depending on the operating system.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
