from tkinter import *
import turtle
from tkinter import messagebox
from tkinter.ttk import *
import time
win=Tk()
win.title('Windows Logo')
win.geometry('250x150')
a= Label(win,text='Do u want old windows logo?')
a.grid(column=0,row=0)
selected = IntVar()
rad1 = Radiobutton(win,text=' Yes', value=1, variable=selected)
rad2 = Radiobutton(win,text=' No', value=2, variable=selected)
rad1.grid(column=0,row=1)
rad2.grid(column=0,row=2)
def click():
    if selected.get()==1:
        g,b='green','blue'
    elif selected.get()==2:
        g,b='light green','light blue'
    else:
        messagebox.showinfo('ERROR', 'Enter yes or no')
        win.mainloop()
    start=time.time()
    t=turtle.Turtle()
    t.shape('square')
    t.resizemode('user')
    t.shapesize(0.1,0.1,0.1)
    t.speed(-1)
    t.pensize(5)
    t.fillcolor('yellow')
    t.begin_fill()
    for p in range(7):
        t.forward(50)
        t.right(90)
    t.end_fill()
    t.penup()
    t.forward(60)
    t.pendown()
    t.fillcolor(g)
    t.begin_fill()
    for h in range(7):
        t.forward(50)
        t.right(90)
    t.end_fill()
    t.penup()
    t.forward(60)
    t.pendown()
    t.fillcolor('red')
    t.begin_fill()
    for v in range(7):
        t.forward(50)
        t.right(90)
    t.end_fill()
    t.penup()
    t.forward(60)
    t.pendown()
    t.fillcolor(b)
    t.begin_fill()
    for k in range(5):
        t.forward(50)
        t.right(90)
    t.end_fill()
    t.hideturtle()
    end=time.time()
    value=str(end-start)
    r.config(text='Completd in '+value+' seconds')
h= Button(win,text='Enter',command=click)
h.grid(column=0,row=4)
r=Label(win,text='')
r.grid(column=0,row=3)
#quit
quit1 = Button(win, text="QUIT",command=win.destroy)
quit1.grid(sticky=S)
                              
win.mainloop()

