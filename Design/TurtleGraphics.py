#Python Turtle Graphics 
import turtle
window=turtle.Screen()

window.bgcolor("pink")
dhanush=turtle.Turtle()
dhanush.shape("turtle")
dhanush.color("green")
dhanush.speed(5)
def draw_square(dhanush):
    for i in range(1,5):
        dhanush.forward(100)
        dhanush.left(90)
for i in range(1,38):
    draw_square(dhanush)
    dhanush.right(10)
dhanush.forward(300)
