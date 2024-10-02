import PyPDF2
import os

class PDFMerger:
    def __init__(self):
        self.pdf_list = []

    def add_pdf(self, pdf_file):
        """Add a PDF file to the list if it's valid."""
        if os.path.isfile(pdf_file) and pdf_file.endswith('.pdf'):
            self.pdf_list.append(pdf_file)
            print(f'Added: {pdf_file}')
        else:
            print(f'Error: Invalid file - {pdf_file}')

    def merge_pdfs(self, output_filename):
        """Merge all added PDFs into a single output file."""
        pdf_writer = PyPDF2.PdfWriter()

        try:
            for pdf in self.pdf_list:
                pdf_reader = PyPDF2.PdfReader(pdf)
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])

            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f'Merged {len(self.pdf_list)} PDFs into "{output_filename}".')
        except Exception as e:
            print(f'Error during merging: {e}')
