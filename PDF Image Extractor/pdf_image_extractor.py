import os
import argparse
import fitz  # PyMuPDF


def extract_images(pdf_path, output_root, dedup):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Failed to open {pdf_path}: {e}")
        return 0

    # Create output folder structure mirroring input
    rel_path = os.path.relpath(
        pdf_path, start=os.path.commonpath([pdf_path, output_root])
    )
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(output_root, os.path.dirname(rel_path), pdf_name)
    img_count = 0

    seen = set()
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            if dedup and xref in seen:
                continue
            if dedup:
                seen.add(xref)

            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image.get("ext", "png")
            if img_count == 0 and not os.path.exists(output_folder):
                os.makedirs(output_folder, exist_ok=True)
            img_count += 1
            img_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
            img_path = os.path.join(output_folder, img_filename)
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)
    doc.close()
    print(f"Extracted {img_count} images from {pdf_path} to {output_folder}")
    return img_count


def main():
    parser = argparse.ArgumentParser(
        description="Recursively extract images from all PDFs in a directory tree."
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Root directory to search for PDF files (default: script directory)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output directory for extracted images (default: <dir>/PDF)",
    )
    parser.add_argument(
        "--dedup",
        action="store_true",
        help="Enable deduplication of images per PDF (default: off, extract all images including duplicates).",
    )
    args = parser.parse_args()

    pdf_dir = os.path.abspath(args.dir)
    # Default output is <dir>/PDF
    output_root = (
        os.path.abspath(args.out) if args.out else os.path.join(pdf_dir, "PDF")
    )

    total_images = 0
    pdf_files = []
    for root, _, files in os.walk(pdf_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, f))

    for pdf_path in pdf_files:
        total_images += extract_images(pdf_path, output_root, args.dedup)

    print(
        f"---\nDone extracting images from all PDFs.\nTotal images extracted: {total_images}"
    )


if __name__ == "__main__":
    main()
