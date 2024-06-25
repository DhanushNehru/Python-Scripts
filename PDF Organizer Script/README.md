# PDF Organizer Script

### Description

The PDF Organizer is a Python script designed to help you manage your collection of PDF files efficiently. It analyzes each PDF file in a specified directory, reading metadata such as titles and authors, and organizes the files into subfolders based on these metadata categories. Additionally, it renames the PDFs according to a consistent format ("Author - Title.pdf") and generates a summary report of the folder's contents, including a count of PDFs per category.

## Features

### Metadata Extraction:

Reads metadata from PDF files to get the title, author, and number of pages.

### Dynamic Organization: 

Automatically creates subfolders for different authors and moves the PDFs into these folders.

### File Renaming: 

Renames PDF files following a consistent naming convention for easier identification.

### Summary Report:

Generates a report detailing the organization process, including the number of PDFs processed and sorted by category.

## Prerequisites

Before you can use the PDF Organizer script, you need to have Python installed on your system. Additionally, the script depends on the PyPDF2 library for reading PDF metadata.

## Installation

1. Install Python
2. Install PyPDF2: Run the following command to install the PyPDF2 library: pip install PyPDF2

## Usage

1. Place the pdf_organizer.py script in a directory of your choice.
2. Open a terminal or command prompt and navigate to the directory where the script is located.
3. Run the script with Python by executing the following command: python pdf_organizer.py
4. Before running the script, make sure to modify the source_folder variable in the script to point to the directory containing your PDF files and the report_path variable to where you want the summary report to be saved.
