from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from emojipy import Emoji
import re

Emoji.unicode_alt = False

def create_emoji_pdf(txt, size):
    txt = Emoji.to_image(txt)
    txt = txt.replace('class="emojione " style="" ', 'height=%s width=%s' %(size, size))
    return re.sub('alt="'+Emoji.shortcode_regexp+'"', '', txt)

txt_file = "Hello World 😂👍😂🙌😉🤳🤷‍♀️🙌😁🎂🐱‍👤🤳✔💋🐱‍👓🐱‍👓😃🎁"
symbola_font = TTFont('Symbola', 'Symbola_hint.ttf')
pdfmetrics.registerFont(symbola_font)
width, height = defaultPageSize
styles = getSampleStyleSheet()
styles["Title"].fontName = 'Symbola'
style = styles["Title"]
content = create_emoji_pdf(Emoji.to_image(txt_file), style.fontSize)
para = Paragraph(content, style)
canv = canvas.Canvas('emoji.pdf')
para.wrap(width, height)
para.drawOn(canv, 0, height/2)
canv.save()