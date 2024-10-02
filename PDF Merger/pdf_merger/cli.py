from pdf_merger.merger import PDFMerger
import os

def get_pdf_order(pdf_list):
    """Prompt the user to specify the order of PDFs to merge."""
    print("\nCurrent PDF files:")
    for idx, pdf in enumerate(pdf_list):
        print(f"{idx + 1}: {pdf}")

    order_input = input("Enter the numbers of the PDFs in the desired order (comma-separated, e.g., 1,3,2): ")
    
    try:
        order = [int(num) - 1 for num in order_input.split(',')]
        ordered_pdfs = [pdf_list[i] for i in order if i < len(pdf_list)]
        return ordered_pdfs
    except ValueError:
        print("Error: Invalid input. Please enter numbers only.")
        return []

def main():
    print("Welcome to the PDF Merger!")

    merger = PDFMerger()

    while True:
        pdf_file = input("Enter the path of a PDF file to merge (or type 'done' to finish): ")
        if pdf_file.lower() == 'done':
            break
        merger.add_pdf(pdf_file)

    if not merger.pdf_list:
        print("No valid PDF files to merge. Exiting...")
        return

    output_path = input("Enter the output directory (leave empty for current directory): ")
    output_filename = input("Enter the output filename (e.g., merged.pdf): ")
    
    if not output_filename.endswith('.pdf'):
        output_filename += '.pdf'

    if output_path:
        output_filename = os.path.join(output_path, output_filename)

    ordered_pdfs = get_pdf_order(merger.pdf_list)

    if not ordered_pdfs:
        print("No valid order provided. Exiting...")
        return

    merger.pdf_list = ordered_pdfs 
    merger.merge_pdfs(output_filename)
