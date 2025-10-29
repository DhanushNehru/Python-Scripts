from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs(pdf_paths, output_path):
    """
    Merge multiple PDF files into a single PDF.

    Args:
        pdf_paths (list): List of input PDF file paths.
        output_path (str): Output file path for the merged PDF.
    """
    pdf_writer = PdfWriter()

    for path in pdf_paths:
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                pdf_writer.add_page(page)
        except Exception as e:
            print(f"Error reading {path}: {e}")

    try:
        with open(output_path, 'wb') as out_file:
            pdf_writer.write(out_file)
        print(f"Merged PDF saved to: {output_path}")
    except Exception as e:
        print(f"Error writing merged PDF: {e}")


def split_pdf(input_pdf):
    """
    Split a PDF into individual pages.

    Args:
        input_pdf (str): Path to the input PDF file.
    """
    try:
        reader = PdfReader(input_pdf)
        base_name = os.path.splitext(input_pdf)[0]

        for page_num, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            output_filename = f"{base_name}_page_{page_num}.pdf"
            with open(output_filename, 'wb') as out_file:
                writer.write(out_file)
            print(f"Saved: {output_filename}")
    except Exception as e:
        print(f"Error splitting PDF: {e}")


if __name__ == "__main__":
    # Example usage
    merge_pdfs(['file1.pdf', 'file2.pdf'], 'merged.pdf')
    split_pdf('merged.pdf')
