import pytesseract
from PIL import Image
from markitdown import MarkItDown
import pdf2image
import os
import sys

# Configure tesseract path
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract OCR\tesseract.exe'
poppler_path = r'D:\Release-25.07.0-0\poppler-25.07.0\Library\bin'

def detect_type(pdf_file):
    try:
        md = MarkItDown()
        result = md.convert(pdf_file)
        
        if len(result.text_content.strip()) < 50:
            return "image"
        else: 
            return "text"
    except Exception as e:
        print(f"Error detecting PDF type: {e}")
        return "image"
    
def convert_text_pdf(pdf_file, output_folder):
    try:
        md = MarkItDown()
        result = md.convert(pdf_file)

        md_filename = os.path.basename(pdf_file).replace('.pdf', '.md')
        output_path = os.path.join(output_folder, md_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"Converted {pdf_file} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_file}: {e}")
        return False

def convert_image_pdf(pdf_file, output_folder):
    try:
        pages = pdf2image.convert_from_path(pdf_file, dpi=300, poppler_path = poppler_path)

        pdf_name = os.path.basename(pdf_file)
        all_text = f"# {pdf_name}\n\n"

        for i, page in enumerate(pages):
            page = page.convert('L')

            text = pytesseract.image_to_string(
                page, 
                lang='vie',
                config='--oem 3 --psm 6'
            )

            if text.strip():
                all_text += f'## Trang {i+1}\n\n{text}\n\n'

        md_filename = os.path.basename(pdf_file).replace('.pdf', '.md')
        output_path = os.path.join(output_folder, md_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(all_text)
        
        print(f"Converted {pdf_file} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_file}: {e}")
        return False
    
def smart_convert_pdf(pdf_file, output_folder=r"D:\PythonProject\ToMD\Output"):
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_type = detect_type(pdf_file)
    print(f"Detected PDF type: {pdf_type}")
    
    if pdf_type == "text":
        return convert_text_pdf(pdf_file, output_folder)
    else:
        return convert_image_pdf(pdf_file, output_folder)

def main():
    data_folder = r'D:\PythonProject\ToMD\Data'
    
    if not os.path.exists(data_folder):
        print(f"Data folder not found: {data_folder}")
        return
    
    pdf_files = [f for f in os.listdir(data_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the data folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        full_path = os.path.join(data_folder, pdf_file)
        print(f"\nProcessing: {pdf_file}")
        
        success = smart_convert_pdf(full_path)
        if success:
            print("Conversion successful")
        else:
            print("Conversion failed")
            
        print("-" * 50)

if __name__ == "__main__":
    main()