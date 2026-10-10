import pygame
import random
import math


def GenerateRandomColorValue():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


def ReturnTextColor(colorValue):
    r = colorValue[0]
    g = colorValue[1]
    b = colorValue[2]
    colors = [r, g, b]

    i = 0
    for c in colors:
        c = c / 255.0
        if c <= 0.04045:
            c = c / 12.92
        else:
            c = math.pow(((c + 0.055) / 1.055), 2.4)
        colors[i] = c
        i += 1

    r = colors[0]
    g = colors[1]
    b = colors[2]

    L = 0.2126 * r + 0.7152 * g + 0.0722 * b

    shouldBeWhite = L > 0.179
    # shouldBeWhite = (r * 0.299 + g * 0.587 + b * 0.114) > 186
    
    if shouldBeWhite:
        return (0, 0, 0)
    else:
        return (255, 255, 255)


pygame.init()

height = 500
width = 500

canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Color Generator!")
isExit = False
canvas.fill((255, 255, 255))

font = pygame.font.Font(pygame.font.get_default_font(), 32)

# RGB Value
RGBText = font.render("RGB Value: (255, 255, 255)", True, (0, 0, 0))
RGBTextRect = RGBText.get_rect()
RGBTextRect.center = (width // 2, height // 2 - 20)

# Hex Value
hexText = font.render("Hex Value: #ffffff", True, (0, 0, 0))
hexTextRect = hexText.get_rect()
hexTextRect.center = (width // 2, height // 2 + 20)
hexTextRect.left = RGBTextRect.left


while not isExit:
    canvas.blit(RGBText, RGBTextRect)
    canvas.blit(hexText, hexTextRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isExit = True
        if event.type == pygame.MOUSEBUTTONUP:
            color = GenerateRandomColorValue()
            RGBString = "RGB Value: " + str(color)
            hexString = "Hex Value: " + str("#%02x%02x%02x" % color)
            TextColor = ReturnTextColor(color)
            RGBText = font.render(RGBString, True, TextColor)
            hexText = font.render(hexString, True, TextColor)
            print(RGBString + "; " + hexString)

            canvas.fill(color)

    pygame.display.flip()
