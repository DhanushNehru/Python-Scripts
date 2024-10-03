from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdfs, output):
    pdf_writer = PdfWriter()
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in range(len(reader.pages)):
            pdf_writer.add_page(reader.pages[page])

    with open(output, 'wb') as out:
        pdf_writer.write(out)

def split_pdf(pdf):
    reader = PdfReader(pdf)
    for page_num, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_filename = f'{pdf.split(".")[0]}_page_{page_num+1}.pdf'
        with open(output_filename, 'wb') as out:
            writer.write(out)

merge_pdfs(['file1.pdf', 'file2.pdf'], 'merged.pdf')
split_pdf('merged.pdf')
