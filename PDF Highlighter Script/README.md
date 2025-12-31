# PDF Keyword Highlighter

A command-line tool to highlight one or more keywords in a PDF file using PyMuPDF. Supports multiple keywords, optional case-sensitive search, and outputs per-page highlight statistics.

## Requirements
- Python `>=3.12`
- PyMuPDF: `pip install pymupdf`

## Usage
```bash
usage: Highlight keywords in PDF [-h] -i INPUT [-o OUTPUT] -k KEYS [KEYS ...] [-s]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input PDF
  -o OUTPUT, --output OUTPUT
                        Output PDF
  -k KEYS [KEYS ...], --keys KEYS [KEYS ...]
                        Keyword(s) to highlight. Sentences are not supported
  -s, --sensitive       Case-sensitive search
```
## Examples
```bash
python3 pdf_highlight.py -i input.pdf -k python code script -o highlighted.pdf

python3 pdf_highlight.py -i input.pdf -k Python -s -o output.pdf  # case-sensitive
```