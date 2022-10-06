from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

context=[]
img="img.jpg"

doc = SimpleDocTemplate("result.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)


im = Image(img, 2*inch, 2*inch)
context.append(im)

context.append(Spacer(3, 20))


styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

with open('input.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        context.append(Paragraph(line, styles["Normal"]))

doc.build(context)
