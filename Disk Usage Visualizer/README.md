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
python vis.py

# Analyze a specific path
python vis.py D:\Projects        # Windows
python vis.py /home/user/docs    # Linux/macOS

# Show top 20 largest folders
python vis.py . -n 20
```
