import turtle
bruh = turtle.Turtle()
bruh.left(90)
bruh.speed('fastest')

bruh.hideturtle()        
bruh.penup()                
bruh.goto(0, -450)                 
bruh.pendown()




def tree(i):
    if i < 5:
        return
    else:
        bruh.forward(i)
        bruh.left(30)
        tree(3 * i/4)
        bruh.right(60)
        tree(3 * i/4)
        bruh.left(30)
        bruh.backward(i)


tree(250)

turtle.done()