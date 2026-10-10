# python code to draw rainbow triangle using turtle
import turtle

# colors to be used in hexagon
colors = ("red", "yellow", "cyan", "green")

t = turtle.Turtle()

# creating tutle GUI screen
screen = turtle.Screen()
screen.bgcolor("black")

# setting the speed of the turtle
t.speed(10)

c = 0
for i in range(100):
    t.forward(i*10)
    t.right(114)
    t.color(colors[c])
    if c == 3:
        c = 0
    else:
        c += 1 