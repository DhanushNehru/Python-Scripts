from os import system, name
from pyfiglet import Figlet

fonts = Figlet().getFonts()
font = input("Enter the font (or 'help' for fonts): ").strip()

system("cls" if name == "nt" else "clear")

if not font:
    text = Figlet(font="slant")
    print(text.renderText("Ansh"))

elif font.lower() in ("help", "h"):
    print(fonts)

elif font in fonts:
    text = Figlet(font=font)
    print(text.renderText("Ansh"))

else:
    print("Invalid font!")
