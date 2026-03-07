from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 25, "normal")

class Scoreboard(Turtle):
    def __init__(self, lives=3):
        super().__init__()
        self.score = 0
        self.lives = lives
        try:
            with open("data.txt") as data:
                self.highscore = int(data.read())
        except FileNotFoundError:
            with open("data.txt", "w") as data:
                data.write("0")
            self.highscore = 0
        self.color("white")
        self.penup()
        self.goto(0, 370)  # Move score/lives display to top for separation
        self.hideturtle()
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score}  HighScore: {self.highscore}  Lives: {self.lives}", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", "w") as data:
                data.write(f"{self.highscore}")
        self.score = 0
        self.update_score()

    def increase_score(self):
        self.score += 1
        self.update_score()

    def lose_life(self):
        self.lives -= 1
        self.update_score()

