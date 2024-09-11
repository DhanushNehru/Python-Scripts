from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf_with_emoji(output_filename, emoji, font_path):
    # Create a canvas for the PDF
    c = canvas.Canvas(output_filename, pagesize=letter)

    # Register a custom emoji font
    pdfmetrics.registerFont(TTFont('EmojiFont', font_path))
    
    # Set the font for the emoji
    c.setFont('EmojiFont', 36)

    # Add the emoji to the PDF
    c.drawString(100, 400, emoji)

    # Save the PDF
    c.save()

if __name__ == "__main__":
    output_filename = "emoji.pdf"
    emoji = "😊"  # Replace with the emoji you want to display
    font_path ="/Users/shru/Python-Scripts/Emoji/Emoji.ttf"  # Replace with the path to your emoji font

    create_pdf_with_emoji(output_filename, emoji, font_path)
