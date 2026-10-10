from turtle import *
speed(-1)
width(3)
colors = ['red', '', 'purple', 'blue', '', 'green', 'yellow', '', 'orange']
#color('sky blue')

def main():
    for ola in range(10):
        for i in range(0, 200, 10):
            color(colors[i%8])
            #up()
            circle(1+i, 20, 10)
            #down()
            circle(1)
        up()
        goto(0, 0)
        down()


if __name__ == '__main__':
    ht()
    main()
    mainloop()
