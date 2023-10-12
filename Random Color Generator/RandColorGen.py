import pygame
import random


def GenerateRandomColorValue():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


pygame.init()

height = 750
width = 750

canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Color Generator!")
isExit = False
canvas.fill((255, 255, 255))

font = pygame.font.Font(pygame.font.get_default_font(), 32)

# RGB Value
RGBText = font.render("RGB Value: (255 ,255 ,255)", True, (0, 0, 0))
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
            RGBText = font.render(RGBString, True, (0, 0, 0))
            hexText = font.render(hexString, True, (0, 0, 0))
            print(RGBString + "; " + hexString)

            canvas.fill(color)

    pygame.display.flip()
