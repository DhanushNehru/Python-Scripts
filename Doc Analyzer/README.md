
# Word Document Analyzer

A simple Python program that analyzes Microsoft Word (`.docx`) documents and displays the number of paragraphs, words, and characters in a file.

## Features

- **Paragraph Count:** Counts the total number of paragraphs.
- **Word Count:** Calculates the total number of words.
- **Character Count:** Calculates the total number of characters, including spaces and newline separators.
- **Error Handling:** Handles missing files and errors when reading Word documents.
- **Interactive Input:** Prompts the user to enter a Word document's file path.

## Requirements

- Python 3.7 or later
- `python-docx` library
- A Microsoft Word document in `.docx` format

## Installation

### 1. Install Python

Download Python from the official website:

https://www.python.org/downloads/

### 2. Install the Required Library

Run the following command in your terminal:

```bash
pip install python-docx
```

### 3. Project Structure

```text
word-document-analyzer/
├── README.md
└── analyzer.py
```

## Usage

1. Open a terminal or command prompt.
2. Navigate to your project directory.
3. Run the program:

   ```bash
   python analyzer.py
   ```

4. Enter the path to your Word document when prompted:

   ```text
   Enter Word file path (.docx): example.docx
   ```

### Example Output

```text
Enter Word file path (.docx): example.docx
Lines (paragraphs): 12
Words: 245
Characters: 1480
```

*Note: The output values are examples and will vary depending on the document.*

## How It Works

1. Opens the Word document using the `python-docx` library.
2. Extracts text from all document paragraphs.
3. Counts paragraphs using `len(doc.paragraphs)`.
4. Counts words using `len(text.split())`.
5. Counts characters using `len(text)`.
6. Handles missing files and other reading errors.

## Error Handling

- **File not found:** Displays `File not found.` when the specified file does not exist.
- **Other errors:** Displays an error message if the Word document cannot be read.

## Limitations

- Supports `.docx` files only, not older `.doc` files.
- Does not count text inside tables, headers, footers, or text boxes.
- Counts paragraphs, not visual lines displayed on a page.
- Character counts include spaces and newline separators between paragraphs.
- Does not modify the original document.

## Technologies Used

- **Python** — Programming language.
- **python-docx** — Library for reading Microsoft Word documents.

## License

This project is available for personal and educational use. Add an open-source license, such as the MIT License, if you intend to distribute it under those terms.
