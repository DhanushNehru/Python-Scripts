from PIL import Image, ImageFont, ImageDraw
import pandas as pd
import os


def generator(name_list, name_font, name_size, name_loc, id_font, id_size, id_loc, event_id, id_offset=0):
    name_font = ImageFont.truetype(name_font, size=name_size)
    id_font = ImageFont.truetype(id_font, size=id_size)

    for i in range(0, len(name_list)):
        im = Image.open("Sample.png")
        sample = ImageDraw.Draw(im)
        text_color = (63, 61, 86)

        name = name_list[i]
        w, h = sample.textsize(name, font=name_font)
        W, H = name_loc
        sample.text((W - w / 2, H - h / 2), name, font=name_font, fill=text_color)

        cert_id = event_id + str(i + 1)
        W, H = id_loc
        sample.text((W, H), cert_id, font=id_font, fill=text_color)

        rgb = Image.new('RGB', im.size, (255, 255, 255))
        rgb.paste(im, mask=im.split()[3])
        rgb.save('exports/' + name + '.pdf', 'PDF', resoultion=100.0)


def process():
    data = pd.read_csv('names.csv', names=['names'])
    evnetID = input("Enter the event name")
    generator(
        data.names.tolist(),
        "fonts/Roboto-Light.ttf",
        60,
        (1260.5, 811.5),
        "fonts/orbitron-black.otf",
        48,
        (1326, 1369),
        evnetID,
        0
    )


process()
