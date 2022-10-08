from turtle import *
speed(-1)
width(3)
color('sky blue')

def main():
    for ola in range(20):
        for i in range(0, 100, 10):
            up()
            circle(2+i, 50, 2)
            down()
            circle(1)
        up()
        goto(0, 0)
        down()


if __name__ == '__main__':
    ht()
    main()
    mainloop()
