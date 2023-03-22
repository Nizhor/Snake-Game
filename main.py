from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "#000000"
FOOD_COLOUR = "#8E26DE"
BACKGROUND_COLOUR = "#808080"

class Snake():
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([(i * -SPACE_SIZE), 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="Snake")
            self.squares.append(square)

class Food:
    def __init__(self, snake_coordinates):
        all_coordinates = [[x * SPACE_SIZE, y * SPACE_SIZE] for x in range(GAME_WIDTH // SPACE_SIZE) for y in range(GAME_HEIGHT // SPACE_SIZE)]
        available_coordinates = [coord for coord in all_coordinates if coord not in snake_coordinates]
        self.coordinates = random.choice(available_coordinates)

        x, y = self.coordinates
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food(snake.coordinates)
    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake) or check_win(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

    global changed_direction
    changed_direction = False

def change_direction(new_direction):
    global direction, changed_direction

    if changed_direction:
        return

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    changed_direction = True

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

def check_win(snake):
    return len(snake.coordinates) == (GAME_WIDTH // SPACE_SIZE) * (GAME_HEIGHT // SPACE_SIZE)

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="Game Over")
    window.after(500, reset_game)

def reset_game():
    canvas.delete(ALL)
    global snake
    global food
    global score
    global direction
    global changed_direction

    score = 0
    direction = 'down'
    changed_direction = False

    label.config(text="Score:{}".format(score))
    canvas.pack()

    snake = Snake()
    food = Food(snake.coordinates)

    next_turn(snake, food)

window = Tk()

window.title("Snake Game")

window.resizable(False, False)

score = 0
direction = 'down'
changed_direction = False

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food(snake.coordinates)

next_turn(snake, food)

window.mainloop()
