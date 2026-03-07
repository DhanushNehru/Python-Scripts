from turtle import Turtle
import random

GRID_SIZE = 20
GRID_MIN = -280
GRID_MAX = 280

class Food(Turtle):   #It refers to dot as food
    def __init__(self): 
        super().__init__()
        # Use 'circle' shape for apple
        self.shape("circle")
        self.penup()
        # Make food exactly 20x20 (same as snake segment)
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("red")  # Apple color
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        # Only place food on grid positions
        possible_x = [x for x in range(GRID_MIN, GRID_MAX + 1, GRID_SIZE)]
        possible_y = [y for y in range(GRID_MIN, GRID_MAX + 1, GRID_SIZE)]
        random_x = random.choice(possible_x)
        random_y = random.choice(possible_y)
        self.goto(random_x, random_y)

