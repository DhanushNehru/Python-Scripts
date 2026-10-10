import os
from docx2pdf import convert

def convert_word_to_pdf(word_file_path):
    try:
        output_pdf_path = os.path.splitext(word_file_path)[0] + ".pdf"
        convert(word_file_path, output_pdf_path)
        print("Conversion successful. PDF saved")
    except Exception as e:
        print(f"Error occurred during conversion: {e}")

if __name__ == "__main__":
    # Replace the paths below with the actual paths of your Word files
    word_files = [
        r"enter word file location path 1",
        r"enter word file location path 2",
        r"enter word file location path 3",
        r"enter word file location path 4",
        r"enter word file location path 5",
        r"enter word file location path 6",
        r"enter word file location path 7",
        r"enter word file location path 8",
        r"enter word file location path 9",
        # you can add as many as you want
    ]

    for word_file_path in word_files:
        convert_word_to_pdf(word_file_path)
