# python code to draw rainbow hexagon using turtle
import turtle

# colors to be used in hexagon
colors = ("red", "yellow", "cyan", "green", "pink", "white")

t = turtle.Turtle()

# creating tutle GUI screen
screen = turtle.Screen()
screen.bgcolor("black")

# setting the speed of the turtle
t.speed(15)

for i in range(400):
    t.color(colors[i%6])
    t.forward(i*1.5)
    t.left(59)
    t.width(3)