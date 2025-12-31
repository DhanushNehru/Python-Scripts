import argparse
import pymupdf as fitz
import string

def parse_args() -> argparse.Namespace:
    """Parses command-line arguments using `argparse.ArgumentParser()`.

    Returns:
        `argparse.Namespace`: Parsed arguments as attributes.
    """    
    parser = argparse.ArgumentParser("Highlight keywords in PDF")

    # add arguments to be accepted
    parser.add_argument("-i", "--input", type=str, required=True, help="Input PDF")
    parser.add_argument("-o", "--output", type=str, default="highlighted.pdf", help="Output PDF")
    parser.add_argument("-k", "--keys", type=str, required=True, nargs="+" ,help='Keyword(s) to highlight. Sentences are not supported')
    parser.add_argument("-s", "--sensitive", action="store_true", help='Case-sensitive search')

    return parser.parse_args()

def highlight_pdf(input_file : str, output_file : str, keywords : list[str], case_sensitive=False) -> dict[str, int]:
    """`Highlghts occurances of `keywords` in the PDF and saves a new file.

    Args:
        input_file (str): Path of the input PDF.
        output_file (str): Path for the output PDF(highlighted).
        keywords (list[str]): List of keywords to highlight
        case_sensitive (bool, optional): if True, matching is case-sensitive. Defaults to False.

    Returns:
        dict[str, int]: Page numbers and highlight counts.
    """    
    try:
        doc = fitz.open(input_file)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return {}
    
    stats = {}

    if case_sensitive:
        keyword_set = {key.strip() for key in keywords}
    else:
        keyword_set = {key.strip().lower() for key in keywords}

    for page in doc:
        hits = []
        page_no = f"Page {page.number + 1}"
        words = page.get_text("words")

        for word in words:
            rect = word[:4]
            match_word = word[4].strip(string.punctuation)
            if not case_sensitive:
                match_word = match_word.lower()
            
            if match_word in keyword_set:
                hits.append(rect)

        if hits:
            annotation = page.add_highlight_annot(hits)
            stats[page_no] = len(hits)

    doc.save(output_file, garbage=4, deflate=True, clean=True)
    doc.close()

    return stats

def print_stats(stats : dict) -> None:
    """Prints highlight statistics.

    Args:
        stats (dict): Page numbers and highlight counts.
    """    
    if not stats:
        print("\nNo matches found.\n")
        return
    total = sum(stats.values())

    print("\n" + "-"*28)
    print("HIGHLIGHT".center(28))
    print("-"*28)

    for page, count in stats.items():
        print(f"{page:18} | {count:3d}")
    print("-"*28)
    print(f"Total: {total} highlights\n")

if __name__ == "__main__":
    args = parse_args()
    print(f"Keywords: {", ".join(args.keys)}")
    print(f"Case-sensitive: {args.sensitive}")

    stats = highlight_pdf(args.input, args.output, args.keys, args.sensitive)
    print_stats(stats)