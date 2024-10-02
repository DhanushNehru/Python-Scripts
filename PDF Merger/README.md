Here is the `README.md` text specifically for the `pdf_merger` folder:

```markdown
# PDF Merger

## Overview

The **PDF Merger** is a Python script that allows you to merge multiple PDF files into a single file. It uses the `PyPDF2` library to handle PDF manipulation and provides an easy-to-use command-line interface to input the desired PDF files and specify the output location.

## How to Use

1. Clone the repository or download the script.
   ```bash
   git clone https://github.com/yourusername/python-scripts-repo
   ```

2. Navigate to the `pdf_merger` folder.
   ```bash
   cd pdf_merger
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python pdf_merger.py
   ```

5. The script will prompt you to enter the path to each PDF file you want to merge. After entering all PDF files, type `done` to proceed.

6. Specify the output directory and output filename for the merged PDF. The merged file will be saved at the location you specify.

## Example

```bash
Enter the path of a PDF file to merge (or type 'done' to finish): /path/to/file1.pdf
Enter the path of a PDF file to merge (or type 'done' to finish): /path/to/file2.pdf
Enter the path of a PDF file to merge (or type 'done' to finish): done
Enter the output directory (leave empty for current directory): /path/to/output/
Enter the output filename (e.g., merged.pdf): merged.pdf
```

The merged PDF will be saved as `/path/to/output/merged.pdf`.

## Prerequisites

- Python 3.x
- `PyPDF2` library

Install the prerequisites by running:
```bash
pip install PyPDF2
```

## Additional Features

- **Custom PDF order**: The script allows you to specify the order of the PDF files to merge.
- **Error Handling**: Handles invalid file inputs and provides meaningful error messages.
- **Output location**: You can specify the directory and filename for the merged PDF output.

## Contribution

Feel free to contribute by creating an issue and submitting a pull request. Ensure to update this README with any additional features or changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
```

You can copy and paste this directly into the `README.md` file for the `pdf_merger` folder. Let me know if you need further changes!