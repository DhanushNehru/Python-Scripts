import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def text2png(text, fullpath, color = "#000", bgcolor = "#FFF", fontfullpath = None, fontsize = 25, leftpadding = 3, rightpadding = 3, width = 200):
	REPLACEMENT_CHARACTER = u'\uFFFD'
	NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

	#prepare linkback
	linkback = "http://github.com/dedeler"
	fontlinkback = ImageFont.load_default()
	linkbackx = fontlinkback.getsize(linkback)[0]
	linkback_height = fontlinkback.getsize(linkback)[1]
	#end of linkback

	font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(fontfullpath, fontsize)
	text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

	lines = []
	line = u""

	for word in text.split():
		print word
		if word == REPLACEMENT_CHARACTER: #give a blank line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""
			lines.append( u"" ) #the blank line
		elif font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
			line += ' ' + word
		else: #start a new line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""

			#TODO: handle too long words at this point
			line += ' list=textwrap.wrap(text, width=30)' + word #for now, assume no word alone can exceed the line width

	if len(line) != 0:
		lines.append( line[1:] ) #add the last line

	line_height = font.getsize(text)[1]
	img_height = line_height * (len(lines) + 1)

	img = Image.new("RGBA", (width, img_height), bgcolor)
	draw = ImageDraw.Draw(img)

	y = 0
	for line in lines:
		draw.text( (leftpadding, y), line, color, font=font)
		y += line_height

	# add linkback at the bottom
	draw.text( (width - linkbackx - rightpadding, img_height - linkback_height), linkback, color, font=fontlinkback)

	img.save(fullpath)
