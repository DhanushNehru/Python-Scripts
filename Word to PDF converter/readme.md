Word to PDF Conversion Script Documentation

This Python script uses the docx2pdf library to convert Word documents to PDF format. Below are the details and usage instructions for the script:


Usage Instructions:

    Replace the paths in the word_files list with the actual file paths of your Word documents that you want to convert to PDF.
    Run the script.

Code Explanation:

    The script defines a function, convert_word_to_pdf, which converts Word documents to PDF using the docx2pdf library.
    For each Word file specified in the word_files list, the script calls the convert_word_to_pdf function to perform the conversion.
    The resulting PDF file is saved in the same location as the source Word document.

Ensure that you have the docx2pdf library installed to run this script successfully. This script is designed to handle multiple Word files. 

You can add as many file paths as needed to the word_files list. The script will convert each specified Word document to PDF format.

Note: You should replace the placeholder file paths in the word_files list with the actual file paths of your Word documents before running the script.
