# PDF Merger and Splitter

This Python script allows you to merge multiple PDF files into a single PDF and split a PDF file into individual pages. It utilizes the `PyPDF2` library for handling PDF files.

## Features

- **Merge PDFs**: Combine multiple PDF files into one.
- **Split PDF**: Divide a single PDF file into separate pages, saving each page as a new PDF file.

## Requirements

Make sure you have Python installed on your machine. This script also requires the `PyPDF2` library. You can install it using pip:

```bash
pip install PyPDF2
```

# Usage
## Merging PDFs
- Place the PDF files you want to merge in the same directory as the script.
- Modify the merge_pdfs function call in the script to include the names of the PDF files you want to merge. For example:
  ```bash
    merge_pdfs(['file1.pdf', 'file2.pdf'], 'merged.pdf')
   ```
- Run the script:
     ```bash
     python pdf_merger_splitter.py
   ```
## Splitting PDFs
- After merging, the script automatically splits the merged PDF file (merged.pdf) into separate pages. Each page will be saved as a new PDF file named merged_page_X.pdf, where X is the page number.
- You can also split any PDF file by calling the split_pdf function in the script:
  ```bash
    split_pdf('your_pdf_file.pdf')
   ```
- Run the script to create separate PDF files for each page.
