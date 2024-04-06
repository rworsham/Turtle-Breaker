from turtle import Screen, Turtle

COLORS = ["yellow", "green", "orange", "red"]
FONT = ("Courier", 24, "normal")
STARTING_POSITION = (0, -450)
BRICK_STARTING_POSITION = (-350, 200)
MOVE_DISTANCE = 100


class Scoreboard(Turtle):
    def __init__(self, lives):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.goto(x=-500, y=460)
        self.lives = lives
        self.score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score} | Lives: {self.lives}", align='left',font=FONT)


    def game_over(self):
        self.clear()
        self.goto(0,0)
        self.write(f"Score: {self.score} | Lives: {self.lives} | GAME OVER", align='center',font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_score()

    def decrease_lives(self):
        self.lives -= 1
        self.update_score()

    def reset(self):
        self.clear()
        self.score = 0
        self.update_score()


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(1,6,10)
        self.penup()
        self.color("deep sky blue")
        self.goto_start()
        self.setheading(0)

    def move_forward(self):
        while not player.xcor() >= 440:
            return self.forward(MOVE_DISTANCE)

    def move_backward(self):
        while not player.xcor() <= -440:
            return self.backward(MOVE_DISTANCE)

    def goto_start(self):
        self.goto(STARTING_POSITION)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.x_move = 6
        self.y_move = 6
        self.move_speed = 3

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.1

    def reset_position(self):
        self.goto(0, 150)
        self.move_speed = 0.1
        self.bounce_x()


class Brick(Turtle):
    def __init__(self, x_cor, y_cor):
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=3)
        if y_cor <= 232:
            self.color(COLORS[0])
        elif y_cor <= 296:
            self.color(COLORS[1])
        elif y_cor <= 360:
            self.color(COLORS[2])
        else:
            self.color(COLORS[3])
        self.goto(x=x_cor, y=y_cor)
        self.left_wall = self.xcor() - 25
        self.right_wall = self.xcor() + 25
        self.upper_wall = self.ycor() + 10
        self.bottom_wall = self.ycor() - 10


class Bricks:
    def __init__(self):
        self.y_start = 200
        self.y_end = 440
        self.bricks = []
        self.create_all_lanes()

    def create_lane(self, y_cor):
        for i in range(-475, 475, 63):
            brick = Brick(i, y_cor)
            self.bricks.append(brick)

    def create_all_lanes(self):
        for i in range(self.y_start, self.y_end, 32):
            self.create_lane(i)


screen = Screen()
screen.setup(width=1000.0, height=1000.0)
screen.bgcolor("dim gray")
screen.title("Breaker")
screen.tracer(0)
score = Scoreboard(lives=5)
player = Player()
ball = Ball()
bricks = Bricks()
screen.listen()
screen.onkeypress(player.move_forward, "Right")
screen.onkeypress(player.move_backward, "Left")
game_is_on = True
while game_is_on:
    screen.update()
    ball.move()

    if ball.xcor() > 500 or ball.xcor() < -500:
        ball.bounce_x()

    if ball.ycor() < -500:
        ball.reset_position()
        score.decrease_lives()

        if score.lives == 0:
            score.game_over()
            game_is_on = False

    if ball.ycor() > 500:
        ball.bounce_y()

    if ball.distance(player) < 60 and ball.ycor() < -430:

        if player.xcor() > 0:
            if ball.xcor() > player.xcor():
                ball.bounce_x()
                ball.bounce_y()

            else:
                ball.bounce_y()

        elif player.xcor() < 0:

            if ball.xcor() < player.xcor():
                ball.bounce_x()
                ball.bounce_y()

            else:
                ball.bounce_y()

        else:
            if ball.xcor() > player.xcor():
                ball.bounce_x()
                ball.bounce_y()

            elif ball.xcor() < player.xcor():
                ball.bounce_x()
                ball.bounce_y()

            else:
                ball.bounce_y()

    for brick in bricks.bricks:
        if ball.distance(brick) < 40:
            score.increase_score()
            brick.clear()
            brick.goto(3000, 3000)
            bricks.bricks.remove(brick)

            if ball.xcor() < brick.left_wall:
                ball.bounce_x()

            elif ball.xcor() > brick.right_wall:
                ball.bounce_x()

            elif ball.ycor() < brick.bottom_wall:
                ball.bounce_y()

            elif ball.ycor() > brick.upper_wall:
                ball.bounce_y()


screen.exitonclick()
