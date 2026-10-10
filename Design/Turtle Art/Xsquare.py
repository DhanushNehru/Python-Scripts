import turtle
turtle.speed(-1)
for l in range(300):
    turtle.pencolor('red')
    turtle.penup()
    turtle.forward(60)
    turtle.pendown()
    turtle.forward(l)
    turtle.left(90)
    turtle.hideturtle()
