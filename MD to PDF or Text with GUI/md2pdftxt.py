import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import pypandoc
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

class MarkdownConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Converter")
        self.setGeometry(300, 300, 400, 150)

        layout = QVBoxLayout()
        self.button = QPushButton("Select Markdown File")
        self.button.clicked.connect(self.select_file)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Register a Unicode font for PDF
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))  # Japanese font that supports wide Unicode range

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md)")
        if file_path:
            self.convert_file(file_path)

    def convert_file(self, file_path):
        save_type, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "PDF Files (*.pdf);;Text Files (*.txt)"
        )
        if save_type:
            if save_type.endswith(".pdf"):
                self.convert_to_pdf(file_path, save_type)
            elif save_type.endswith(".txt"):
                self.convert_to_text(file_path, save_type)
            else:
                QMessageBox.warning(self, "Error", "Please select a valid file type.")

    def convert_to_text(self, md_path, output_path):
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            output = pypandoc.convert_text(md_content, 'plain', format='md', extra_args=['--standalone'])
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            QMessageBox.information(self, "Success", "Markdown converted to Text successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert: {e}")

    def convert_to_pdf(self, md_path, output_path):
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            text = pypandoc.convert_text(md_content, 'plain', format='md', extra_args=['--standalone'])
            doc = SimpleDocTemplate(output_path)
            styles = getSampleStyleSheet()
            story = [Paragraph(line, styles["Normal"]) for line in text.split("\n")]
            doc.build(story)
            QMessageBox.information(self, "Success", "Markdown converted to PDF successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownConverter()
    window.show()
    sys.exit(app.exec())
