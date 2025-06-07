import os
import re
import requests
import PyPDF2

def download_pdf(url, local_filename):
    """Download PDF from a URL to a local file."""
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        # Apply text cleaning after extraction
        return clean_extracted_text(text)
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        return None

def clean_extracted_text(text):
    """Clean and format the extracted text."""
    # Remove line breaks in the middle of sentences
    cleaned_text = re.sub(r'(?<!\.)\n(?!\n)', ' ', text)  # Replace single line breaks with space
    # Remove multiple spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Preserve paragraphs by keeping double newlines
    cleaned_text = re.sub(r'\n{2,}', '\n\n', cleaned_text)
    return cleaned_text.strip()

def convert_pdf_to_txt(pdf_path, save_to_file=True, output_folder="output_texts"):
    """Convert a single PDF to text, optionally saving to a file."""
    try:
        # Check if the path is a URL or local file
        if pdf_path.startswith("http"):
            # Download PDF to a temporary location
            local_pdf = os.path.join(output_folder, pdf_path.split('/')[-1])
            download_pdf(pdf_path, local_pdf)
            text = extract_text_from_pdf(local_pdf)
            os.remove(local_pdf)  # Remove the temporary file
        else:
            # Handle local file
            text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Print the cleaned text
            print(f"\nExtracted text:\n{text}\n")

            if save_to_file:
                # Save the extracted text to a .txt file
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                output_file = os.path.join(output_folder, f"{base_name}.txt")
                with open(output_file, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
                print(f"Text successfully saved to: {output_file}")
        else:
            print(f"Could not extract text from: {pdf_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

    
def count_words_in_pdf(pdf_path):
       try:
           with open(pdf_path, 'rb') as pdf_file:
               pdf_reader = PyPDF2.PdfReader(pdf_file)
               text = ""
               for page_num in range(len(pdf_reader.pages)):
                   page = pdf_reader.pages[page_num]
                   text += page.extract_text()

               # Remove extra whitespaces and split into words
               words = re.findall(r'\b\w+\b', text.lower())
               return len(words)
       except FileNotFoundError:
           return "Error: PDF file not found."
       except Exception as e:
           return f"An error occurred: {e}"

# Example usage:

#example pdf from internet
#pdf = "https://fase.org.br/wp-content/uploads/2014/05/exemplo-de-pdf.pdf"

#example local pdf
pdf = "D:/repos/Python-Scripts/PDF to text/Atividade 28 Fev.pdf"

# Convert PDF to text and save the cleaned text to a file
convert_pdf_to_txt(pdf)
word_count = count_words_in_pdf(pdf)
print(f"Total word count in the PDF: {word_count}")
