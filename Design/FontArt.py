from os import system, name
from pyfiglet import Figlet

system("cls" if name == "nt" else "clear")
print(Figlet(font="slant").renderText("Font Art"))

try:
    text = input("Enter Text : ")
    font = input("Enter Font ('help' or 'h' for list): ")
    fonts = Figlet().getFonts()
    size = len(fonts)


    if font.lower() == "help" or font.lower() == "h":
        for i in range(0, size):
            print(f"{i} : {fonts[i]}")
        choice = int(input("Enter number (0-{size}) : "))
        font = fonts[choice]
    if not font:
        font = "slant"
    if not text:
        text = "Ansh"


    system("cls" if name == "nt" else "clear")
    print(Figlet(font=font).renderText(text))

except KeyboardInterrupt:
    system("cls" if name == "nt" else "clear")
    print(Figlet(font="slant").renderText("Byee"))
