# Disk Usage Visualizer (CLI)

A simple Python script that scans directories and displays the largest folders or files by disk usage — right from your terminal.
Lightweight, fast, and cross-platform (works on Linux, macOS, and Windows).

## Features

- Recursively analyzes disk usage in a directory

- Displays top N largest folders (default: 10)

- Handles long file paths and permission errors gracefully

- Works seamlessly on Windows, Linux, and macOS

## Usage

```bash
# Analyze current directory
python disk_visualizer.py

# Analyze a specific path
python disk_visualizer.py D:\Projects        # Windows
python disk_visualizer.py /home/user/docs    # Linux/macOS

# Show top 20 largest folders
python disk_visualizer.py . -n 20
```
