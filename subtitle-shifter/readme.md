# MUST READ BEFORE EXECUTION (ONE TIME ONLY)

This script allows you to **shift subtitles in .srt file forward or backward** using the **pysubs2** Python library. Please read these instructions carefully before running the script.  

---

## 1️ Prerequisites

1. **Install Python (3.8 or higher)**  
   Download and install from [https://www.python.org/downloads/](https://www.python.org/downloads/).  
   Make sure to **add Python to your system PATH** during installation.
   OR you can simply run this command in terminal to install python: "winget install Python.Python.3"
   for MAC: brew install python

2. **Install pysubs2** (required for subtitle work)  
   pip install pysubs2
---

## 2️ Subtitle File Requirements

- Place the subtitle file you want to shift **in the same folder** as the script.  
- Make sure to use the **correct file extension** i.e .srt 
- The output .srt file will also be saved in the same folder with the filename: subtitleFileName_shifted.srt


---

## 3 Running the Script

1. Open a terminal or command prompt in the folder containing the script.  
2. Run the script: type "python shifter.py"
3. Follow Along the input instructions prompted on screen

## Developer
- GitHub: https://github.com/Syed-56
- LinkedIn: https://www.linkedin.com/in/syedsultan10

## Dependencies & Licenses
- pysrt: GNU GPL v3.0 (https://github.com/byroot/pysrt)