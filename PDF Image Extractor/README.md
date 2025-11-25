# PDF Image Extractor

Recursively extracts all images from every PDF file in a directory tree, saving the images in a subfolder named `PDF` in the input root directory by default. Each PDF file is organized into its own folder, containing all images extracted from that document.

## Requirements

- Python 3.8+
- [PyMuPDF](https://pymupdf.readthedocs.io) (`pip install pymupdf`)

## Usage


1. Install dependencies:

   ```
   pip install pymupdf
   ```


2. Run the script:

    ```
    python pdf_image_extractor.py [--dir <input_dir>] [--out <output_dir>] [--dedup]
    ```

- `--dir <input_dir>`: Root directory to search for PDFs (default: script directory)
- `--out <output_dir>`: Output directory for images (default: `<dir>/PDF`)
- `--dedup`: Enable deduplication of images per PDF (default: off)

### Examples

Extract all images (including duplicates) from PDFs in `./my_pdfs`:

```
python pdf_image_extractor.py --dir ./my_pdfs
```

Extract only unique images per PDF, saving to a custom output folder:

```
python pdf_image_extractor.py --dir ./my_pdfs --out ./images --dedup
```

## Output Structure

- For each PDF, a folder named after the PDF (without extension) is created in the output directory, mirroring the original structure.
- Images are saved as `page<page_number>_img<image_index>.<ext>`.
