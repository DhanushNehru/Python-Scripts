
# Importing necessary libraries
import os
import shutil
import string
from PyPDF2 import PdfReader

# Function to extract PDF metadata
def extract_pdf_metadata(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        num_pages = len(reader.pages)
        title = metadata.get('/Title', 'Unknown Title')
        author = metadata.get('/Author', 'Unknown Author')
        return {'title': title, 'author': author, 'num_pages': num_pages}
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

# Function to organize PDFs into subfolders based on author
def organize_pdfs_by_author(source_folder):
    pdf_files = [f for f in os.listdir(source_folder) if f.endswith('.pdf')]
    summary = {}
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(source_folder, pdf_file)
        metadata = extract_pdf_metadata(pdf_path)
        
        if metadata:
            author_folder = os.path.join(source_folder, sanitize_filename(metadata['author']))
            if not os.path.exists(author_folder):
                os.makedirs(author_folder)
            
            new_pdf_name = f"{sanitize_filename(metadata['author'])} - {sanitize_filename(metadata['title'])}.pdf"
            new_pdf_path = os.path.join(author_folder, new_pdf_name)
            
            shutil.move(pdf_path, new_pdf_path)
            
            if metadata['author'] in summary:
                summary[metadata['author']] += 1
            else:
                summary[metadata['author']] = 1
    
    return summary

# Function to sanitize filenames to remove invalid characters
def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)
    return sanitized_filename.strip()

# Function to generate a summary report
def generate_summary_report(summary, report_path):
    with open(report_path, 'w') as report_file:
        for author, count in summary.items():
            report_file.write(f"Author: {author}, PDFs: {count}\n")

# Main function to execute the organizer
def main():
    source_folder = '/path/to/pdf/folder'
    report_path = '/path/to/summary/report.txt'
    summary = organize_pdfs_by_author(source_folder)
    generate_summary_report(summary, report_path)
    print("PDF organization and summary report generation complete.")

if __name__ == "__main__":
    main()
