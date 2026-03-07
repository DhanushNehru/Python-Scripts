from turtle import Screen, Turtle
from food import Food
from snake import Snake
from scoreboard import Scoreboard
import _tkinter
import time

screen = Screen()

from turtle import Screen, Turtle
from food import Food
from snake import Snake
from scoreboard import Scoreboard
import _tkinter
import time

screen = Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# Block movement until countdown ends
allow_movement = False

# --- Turtles for UI ---
start_turtle = Turtle()
start_turtle.hideturtle()
start_turtle.penup()
start_turtle.color("white")

button_turtle = Turtle()
button_turtle.hideturtle()
button_turtle.penup()
button_turtle.color("white")
button_turtle.shape("square")
button_turtle.shapesize(stretch_wid=2, stretch_len=8)

pause_turtle = Turtle()
pause_turtle.hideturtle()
pause_turtle.penup()
pause_turtle.color("yellow")

countdown_turtle = Turtle()
countdown_turtle.hideturtle()
countdown_turtle.penup()
countdown_turtle.color("yellow")
countdown_turtle.goto(0, 0)

bottom_text_turtle = Turtle()
bottom_text_turtle.hideturtle()
bottom_text_turtle.penup()
bottom_text_turtle.color("white")

# --- Game State ---
game_started = False
is_paused = False
is_game_on = True
is_game_over = False

GAME_SPEED = 80
ANIMATION_SPEED = 80
GRID_SIZE = 20
PLAY_AREA_LIMIT = 360
next_direction = None

# --- UI Functions ---
def show_start_screen():
    clear_all_text()
    global game_started, is_paused, is_game_on, is_game_over
    game_started = False
    is_paused = False
    is_game_on = True
    is_game_over = False
    start_turtle.goto(0, 100)
    start_turtle.write("SNAKE GAME", align="center", font=("Courier", 48, "bold"))
    button_turtle.goto(0, -50)
    button_turtle.showturtle()
    button_turtle.write("PRESS SPACE TO START", align="center", font=("Courier", 32, "bold"))
    show_bottom_text("SPACE to pause | P for new game | Q to quit")

def show_pause_explanation():
    pause_turtle.clear()
    pause_turtle.goto(0, 100)
    pause_turtle.write("PAUSED", align="center", font=("Courier", 48, "bold"))
    pause_turtle.goto(0, 0)
    pause_turtle.write("SPACE: Resume\nQ: Quit\nP: New Game", align="center", font=("Courier", 24, "normal"))

def show_gameover_explanation():
    pause_turtle.clear()
    pause_turtle.goto(0, 0)
    pause_turtle.write("GAME OVER\nPress SPACE to return to title", align="center", font=("Courier", 32, "bold"))
    show_bottom_text("SPACE to return to title")

def show_bottom_text(text):
    bottom_text_turtle.clear()
    bottom_text_turtle.goto(0, -380)
    bottom_text_turtle.write(text, align="center", font=("Courier", 18, "normal"))

def clear_all_text():
    start_turtle.clear()
    button_turtle.clear()
    pause_turtle.clear()
    countdown_turtle.clear()
    bottom_text_turtle.clear()
# --- Pause/Resume/Quit/New Game ---
def handle_space():
    global game_started, is_paused, is_game_over
    if is_game_over:
        is_game_over = False
        clear_all_text()
        show_start_screen()
        return
    if not game_started:
        clear_all_text()
        start_game()
    elif not is_paused:
        is_paused = True
        show_pause_explanation()
    else:
        is_paused = False
        pause_turtle.clear()
        show_bottom_text("SPACE to pause | P for new game | Q to quit")

def handle_q():
    global is_paused
    if is_paused:
        screen.bye()

def handle_p():
    global is_game_on, game_started, is_paused, next_direction, scoreboard, snake, food, GAME_SPEED, ANIMATION_SPEED, allow_movement
    if is_paused:
        is_game_on = True
        game_started = True
        is_paused = False
        next_direction = None
        pause_turtle.clear()
        scoreboard.clear()
        snake.reset()
        food.refresh()
        scoreboard.lives = 3
        scoreboard.score = 0
        scoreboard.update_score()
        GAME_SPEED = 80
        ANIMATION_SPEED = 80
        allow_movement = False
        show_bottom_text("SPACE to pause | P for new game | Q to quit")
        show_countdown()

screen.onkey(handle_space, "space")
screen.onkey(handle_q, "q")
screen.onkey(handle_p, "p")

# --- Start logic ---
def start_game():
    global game_started
    if game_started:
        return
    game_started = True
    clear_all_text()
    button_turtle.hideturtle()  # Hide the button after starting
    show_countdown()

# --- Countdown ---
def show_countdown():
    global allow_movement
    allow_movement = False
    for i in range(3, 0, -1):
        countdown_turtle.clear()
        countdown_turtle.write(str(i), align="center", font=("Courier", 64, "bold"))
        screen.update()
        time.sleep(1)
    countdown_turtle.clear()
    screen.update()
    allow_movement = True
    start_snake_game()

# --- Game Setup ---
food = Food()
snake = Snake()
scoreboard = Scoreboard(lives=3)

screen.listen()

def set_up():
    global next_direction
    if allow_movement:
        next_direction = 'up'
def set_down():
    global next_direction
    if allow_movement:
        next_direction = 'down'
def set_left():
    global next_direction
    if allow_movement:
        next_direction = 'left'
def set_right():
    global next_direction
    if allow_movement:
        next_direction = 'right'

screen.onkey(set_up, "Up")
screen.onkey(set_down, "Down")
screen.onkey(set_left, "Left")
screen.onkey(set_right, "Right")

def move_and_update():
    try:
        food.showturtle()
        for segment in snake.segments:
            segment.showturtle()
        screen.update()
    except _tkinter.TclError:
        print("Game closed.")
        global is_game_on
        is_game_on = False

def apply_next_direction():
    global next_direction
    if next_direction == 'up':
        snake.up()
    elif next_direction == 'down':
        snake.down()
    elif next_direction == 'left':
        snake.left()
    elif next_direction == 'right':
        snake.right()
    next_direction = None

def game_loop():
    global is_game_on, is_game_over
    try:
        if is_game_on and game_started and not is_paused and not is_game_over:
            move_and_update()
            apply_next_direction()
            snake.move()
            # detect collision with the food (exact grid match)
            if (round(snake.head.xcor()) == round(food.xcor()) and round(snake.head.ycor()) == round(food.ycor())):
                food.refresh()
                snake.extend()
                scoreboard.increase_score()
            # detect collision with the wall
            if (
                snake.head.xcor() > PLAY_AREA_LIMIT or snake.head.xcor() < -PLAY_AREA_LIMIT or
                snake.head.ycor() > PLAY_AREA_LIMIT or snake.head.ycor() < -PLAY_AREA_LIMIT
            ):
                scoreboard.lose_life()
                if scoreboard.lives == 0:
                    is_game_on = False
                    is_game_over = True
                    clear_all_text()
                    show_gameover_explanation()
                else:
                    snake.reset()
            # detect collision with the tail
            for segment in snake.segments[1:]:
                if snake.head.distance(segment) < 10:
                    scoreboard.lose_life()
                    if scoreboard.lives == 0:
                        is_game_on = False
                        is_game_over = True
                        clear_all_text()
                        show_gameover_explanation()
                    else:
                        snake.reset()
                    break
        screen.ontimer(game_loop, GAME_SPEED)
    except _tkinter.TclError:
        print("Game closed.")
        is_game_on = False

def start_snake_game():
    show_bottom_text("SPACE to pause | P for new game | Q to quit")
    screen.ontimer(game_loop, GAME_SPEED)
    screen.exitonclick()

if __name__ == "__main__":
    show_start_screen()
    screen.mainloop()