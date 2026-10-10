# Python Scripts

A collection of Python scripts I've written, developed, and organized to automate tasks, explore programming concepts, and build useful tools.

This repository contains scripts for file management, data conversion, games, graphics, sorting algorithms, and everyday automation. Each category has its own directory to keep things organized.

Feel free to explore the scripts, use them, and suggest improvements. Please respect the repository's license and credit the original author when using or adapting code.

## Table of Contents

- [About](#about)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)
- [List of Scripts](#list-of-scripts)
  - [Converters](#converters)
  - [Design](#design)
  - [Games](#games)
  - [Sorting Algorithms](#sorting-algorithms)
  - [Tools](#tools)
- [License](#license)
- [Support](#support)

## About

I created this repository to collect my Python projects in one place, making them easier to maintain, explore, and improve.

The repository includes beginner-friendly programs, practical utilities, small games, graphical experiments, and scripts that automate repetitive tasks.

Most scripts focus on a specific task and can be explored independently. Some projects require additional Python packages, so check the relevant source code and any accompanying `README.md` or `requirements.txt` before running them.

## Repository Structure

```text
Python-Scripts/
├── Converters/
├── Design/
├── Games/
├── Sorting/
├── Tools/
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

Each directory contains scripts grouped by purpose. Some projects have their own subdirectories for related files, documentation, and dependencies.

## Contributing

Contributions, bug fixes, suggestions, and improvements are welcome.

If you'd like to contribute, please read [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guidelines.

Before submitting a pull request, please:

- Open an issue to discuss significant changes or new scripts.
- Keep your code readable and consistent with the existing project structure.
- Include documentation and dependency information where necessary.
- Update this README when adding a new script.
- Remove unnecessary temporary files and generated artifacts.

I'll review contributions and provide feedback where necessary.

## List of Scripts

### Converters

Scripts for converting files, images, documents, and data between different formats.

| Script | Description |
|---|---|
| [Audio Book](Converters/audio_book.py) | Converts text or supported documents into audio. |
| [Convert Temperature](Converters/Convert%20Temperature.py) | Converts temperatures between Fahrenheit, Celsius, and Kelvin. |
| [CSV to Excel](Converters/csv_excel.py) | Converts CSV files into Excel spreadsheets. |
| [CSV to NDJSON](Converters/csv_to_ndjson.py) | Converts CSV data into newline-delimited JSON. |
| [Emoji to PDF](Converters/emoji_to_pdf.py) | Creates PDF documents containing emojis. |
| [HTML to Images](Converters/html-to-images.py) | Converts HTML documents into images. |
| [Image to ASCII](Converters/image_to_ascii.py) | Converts images into ASCII art. |
| [Image to GIF](Converters/imageTogif.py) | Creates GIF animations from images. |
| [Image to WebP](Converters/image_to_webp.py) | Converts images into WebP format. |
| [Image to WebP GUI](Converters/image_to_webp_gui.py) | Provides a graphical interface for converting images to WebP. |
| [Image Text to PDF](Converters/imagetxt_to_pdf.py) | Combines images and text into PDF documents. |
| [JSON to CSV 1](Converters/jsontocsv1.py) | Converts JSON data into CSV format. |
| [JSON to CSV 2](Converters/jsontocsv2.py) | Provides another implementation of JSON-to-CSV conversion. |
| [JSON to YAML](Converters/json_to_yaml.py) | Converts JSON data into YAML format. |
| [Longitude and Latitude Converter](Converters/lonlat_converter_lambert.py) | Converts geographic coordinates using the Lambert conformal conic projection. |
| [PDF to HTML](Converters/pdf_to_html.py) | Converts PDF documents into HTML. |
| [PDF to Text](Converters/pdf_to_txt.py) | Extracts text from PDF documents. |
| [PNG to JPG](Converters/png_to_jpg.py) | Converts PNG images into JPG format. |
| [Text to Image](Converters/text2image.py) | Converts text into images. |
| [Weight Converter](Converters/weight.py) | Converts between different weight measurement units. |
| [Word to PDF](Converters/wordToPDF.py) | Converts Word documents into PDF files. |

### Design

Scripts for generating graphics, patterns, and visual experiments.

| Script | Description |
|---|---|
| [Font Art](Design/FontArt.py) | Generates text-based font art. |
| [Fractal Tree](Design/fractaltree.py) | Generates a fractal tree using recursive drawing. |
| [Star Pattern](Design/starPattern.py) | Creates star patterns using Python. |
| [Turtle Graphics](Design/TurtleGraphics.py) | Demonstrates graphics and drawing using Python's Turtle module. |

#### Turtle Art

The `Design/Turtle Art/` directory contains additional drawing projects.

| Script | Description |
|---|---|
| [Art 2](Design/Turtle%20Art/art2.py) | A Turtle graphics drawing. |
| [Art 4](Design/Turtle%20Art/art4.py) | A Turtle graphics drawing. |
| [Art 5](Design/Turtle%20Art/art5.py) | A Turtle graphics drawing. |
| [Doraemon](Design/Turtle%20Art/Doraemon.py) | Draws Doraemon using Turtle graphics. |
| [Happy Birthday](Design/Turtle%20Art/happy_birthday.py) | Creates a birthday-themed drawing. |
| [Pikachu](Design/Turtle%20Art/Pikachu.py) | Draws Pikachu using Turtle graphics. |
| [Rainbow Hexagon](Design/Turtle%20Art/rainbow_hexagon.py) | Creates a rainbow-colored hexagonal pattern. |
| [Rainbow Triangle](Design/Turtle%20Art/rainbow_triangle.py) | Creates a rainbow-colored triangular pattern. |
| [Scenery](Design/Turtle%20Art/scenery.py) | Draws a scenery illustration. |
| [Shinchan](Design/Turtle%20Art/Shinchan.py) | Draws Shinchan using Turtle graphics. |
| [Sunflower](Design/Turtle%20Art/sunflowerGood.py) | Creates a sunflower drawing. |
| [X Square](Design/Turtle%20Art/Xsquare.py) | Creates a geometric drawing. |

The `Design/Turtle Art/Prompt_Based/` directory contains interactive drawing scripts.

| Script | Description |
|---|---|
| [Benzene](Design/Turtle%20Art/Prompt_Based/benzene.py) | Draws a benzene ring. |
| [Tkinter Name](Design/Turtle%20Art/Prompt_Based/tkinterName.py) | Displays a name using a Tkinter interface. |
| [Windows Logo](Design/Turtle%20Art/Prompt_Based/windowsLogo.py) | Draws a Windows-style logo. |

### Games

Small games and simulations built with Python.

| Script | Description |
|---|---|
| [Blackjack](Games/BlackjackGame.py) | A playable Blackjack card game. |
| [Chessboard](Games/ChessBoard.py) | Generates a chessboard using Python. |
| [Connect Four](Games/connectfour.py) | Implements the Connect Four game. |
| [Hangman](Games/hangman_game.py) | A word-guessing game in which players guess letters to reveal a hidden word. |
| [Planet Simulation](Games/Planet_simulation.py) | Simulates planets orbiting the Sun. |
| [Rock Paper Scissors](Games/rps.py) | Implements the classic Rock Paper Scissors game. |
| [Snake Water Gun](Games/snake-water-gun.py) | A game based on the Rock Paper Scissors concept. |
| [Tic Tac Toe](Games/tic_tac_toe.py) | Implements the classic Tic Tac Toe game. |
| [Snake Game](Games/Snake%20Game/) | A Snake game with separate modules for the game, food, snake, and scoreboard. |

### Sorting Algorithms

Implementations of common sorting algorithms.

| Script | Description |
|---|---|
| [Bubble Sort](Sorting/bubblesort.py) | Sorts elements using the bubble sort algorithm. |
| [Insertion Sort](Sorting/insertionsort.py) | Sorts elements using the insertion sort algorithm. |
| [Selection Sort](Sorting/selectionsort.py) | Sorts elements using the selection sort algorithm. |

### Tools

Utilities for automation, file management, data processing, networking, and other everyday tasks.

| Script | Description |
|---|---|
| [Automated Emails](Tools/automails_daily.py) | Automates email-related tasks. |
| [Birthday Manager](Tools/Automating%20Emails/) | Manages birthday information and related email automation. |
| [DDoS Demonstration](Tools/ddos.py) | Demonstrates concurrent HTTP request generation. Use only in an authorized test environment. |
| [Disk Usage Visualizer](Tools/disk_visualizer.py) | Displays directories that consume the most disk space. |
| [Distance Calculator](Tools/distance_calculator.py) | Calculates the distance between two points. |
| [Duplicate Finder](Tools/duplicate-finder.py) | Identifies duplicate files using file hashes. |
| [Expense Tracker](Tools/Expense%20Tracker/) | Tracks expenses and stores related data. |
| [Face Reaction](Tools/face_reaction.py) | Attempts to detect facial expressions. |
| [Fake Profile Generator](Tools/FakeProfile.py) | Generates sample profile data. |
| [File Encryption and Decryption](Tools/fileEncryptDecrypt.py) | Encrypts and decrypts files. |
| [File Organizer](Tools/FileOrganizer.py) | Organizes files according to their types. |
| [File Renamer](Tools/File_Renamer.py) | Renames multiple files automatically. |
| [File Search](Tools/file_search.py) | Searches for files in directories and subdirectories. |
| [File Text Search](Tools/FileTextSearch.py) | Searches files for specific text or phrases. |
| [Hand Volume Control](Tools/Hand%20Volume/) | Uses hand tracking to control system volume. |
| [Image Compressor](Tools/image_compressor.py) | Compresses image files. |
| [Image Watermarker](Tools/image_watermarker.py) | Adds watermarks to images. |
| [Instagram Downloader](Tools/insta_down.py) | Downloads supported Instagram content. |
| [Jokes Generator](Tools/jokes.py) | Generates or retrieves jokes. |
| [Merge Images](Tools/mergeImages.py) | Combines images horizontally or vertically. |
| [Morse Code](Tools/morse_code.py) | Encodes and decodes Morse code. |
| [Multi-Platform Icon Generator](Tools/multi_platform_icongen.py) | Generates application icons for multiple platforms. |
| [Password Generator](Tools/PasswordGenerator.py) | Generates random passwords. |
| [Pomodoro Timer](Tools/Pomodoro%20Timer.py) | Implements a Pomodoro timer for focused work sessions and breaks. |
| [Python GUI Notepad](Tools/Python%20GUI%20Notepad.py) | A simple graphical text editor. |
| [QR Code Generator](Tools/QRcodeGen.py) | Generates QR codes from provided data. |
| [QR Code Ticket Generator](Tools/QR%20Ticket%20Generator/) | Generates QR-code-based tickets. |
| [QR Code with Logo](Tools/qr_with_logo.py) | Creates QR codes with a logo. |
| [Random Color Generator](Tools/RandColorGen.py) | Generates random colors. |
| [Random Song Generator](Tools/random_song_generator.py) | Selects songs based on the provided mood or input. |
| [Recently Accessed Files](Tools/recently_accessed_files.py) | Identifies recently accessed files. |
| [Subnetting Calculator](Tools/subnetting_calculator.py) | Calculates network information from an IP address and subnet mask. |
| [Countdown Timer](Tools/timer.py) | Implements a timer for specified durations. |
| [Umbrella Reminder](Tools/umbrellaReminder.py) | Provides an umbrella reminder. |
| [URL Shortener](Tools/urlshortener.py) | Generates shorter URLs from longer ones. |
| [Web Scraper](Tools/Web_Scraper.py) | Scrapes information from websites. |
| [Website Cloner](Tools/Website%20Cloner/) | Downloads and serves supported website content locally. |
| [Wikipedia Extractor](Tools/wikipedia_extractor.py) | Extracts information from Wikipedia. |
| [YouTube Downloader](Tools/youtubeDownloader.py) | Downloads supported YouTube media. |

## License

This repository includes a [LICENSE](LICENSE) file. Please review it before using, modifying, or redistributing the code.

When using or adapting code contributed by someone else, respect the applicable license and preserve any required attribution.

## Support

If you find something useful here, consider giving the repository a star.

If you encounter a bug or have an idea for an improvement, feel free to open an issue.

Thanks for visiting!