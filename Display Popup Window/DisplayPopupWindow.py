# !/usr/bin/python3
import tkinter
from PIL import ImageTk, Image as image

window = tkinter.Tk()
window.title("Dhanush Automated Script")
text = tkinter.Label(window, text = " Time to Walk !!! ", 
    bg="#0a8ca6",
    fg="#8c180b", 
    font="<> 20",
    pady=70,
    padx=70
    )
text.pack();

#Get height & weight
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Get half of screen width & height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)

window.geometry("+{}+{}".format(positionRight, positionDown))

window.configure(bg="#db7c23")

window.mainloop()