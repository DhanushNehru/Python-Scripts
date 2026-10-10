import argparse
import pdfkit

class HTMLToPDFConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        try:
            pdfkit.from_file(self.input_file, self.output_file)
            print(f"Conversion successful. PDF saved as '{self.output_file}'")
        except Exception as e:
            print(f"Conversion failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert HTML to PDF using Python")
    parser.add_argument("input_file", help="Input HTML file to convert")
    parser.add_argument("output_file", help="Output PDF file name")
    parser.add_argument("--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    converter = HTMLToPDFConverter(args.input_file, args.output_file)
    converter.convert()

if __name__ == "__main__":
    main()
