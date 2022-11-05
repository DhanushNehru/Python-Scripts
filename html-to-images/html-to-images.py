from html2image import Html2Image

hti = Html2Image()

file = str(input('Enter the directory of your html file: '))
img = str(input('Enter the name of your image including file format: '))
background = str(input('(OPTIONAL) Enter the background color you would like: '))
if len(background)>0:
    css = ('body {background: %s;}' % (background))
    with open(file, errors='ignore') as f:
        hti.screenshot(f.read(), css_str=css, save_as=img)
else:
    with open(file, errors='ignore') as f:
        hti.screenshot(f.read(), save_as=img)