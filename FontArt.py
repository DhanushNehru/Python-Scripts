import os
from pyfiglet import Figlet
text = Figlet(font="slant")
os.system("cls")
os.system("mode con: cols=75 lines=30")
print(text.renderText("Dhanush N"))