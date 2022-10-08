from turtle import *
import random
speed(-1)
width(3)
colors = ['sky blue', 'navy', "steel blue", 'cyan']

def main():
    for i in range(0, 204, 2):
        random.shuffle(colors)
        color(colors[0])
        circle(10+i, 100, 2)

if __name__ == '__main__':
    ht()
    main()
    mainloop()
