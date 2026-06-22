# Moving Snake Body for v1 snake game

import os
import time
import msvcrt
import random

def get_new_head(head_x, head_y, direction):
    new_head_x = head_x
    new_head_y = head_y
    if direction == "up":
        new_head_y -= 1
    elif direction == "down":
        new_head_y += 1
    elif direction == "left":
        new_head_x -= 1
    elif direction == "right":
        new_head_x += 1
    return [new_head_x, new_head_y]

def check_loss(width, height, snake, head_x, head_y, running):
    if head_x < 0 or head_x >= width - 2 or head_y < 0 or head_y >= height - 2:
        running = False
    if snake[0] in snake[1:]:
        running = False
    return running

def generate_apple(width, height, snake):
    while True:
        apple_x = random.randint(0, width - 3)
        apple_y = random.randint(0, height - 3)
        if [apple_x, apple_y] not in snake:
            return apple_x, apple_y

def draw_grid(width, height, snake, apple_x, apple_y):
    print("# "*width)
    for i in range(height - 2):
        print("#", end=" ")
        for j in range(width - 2):
            if [j, i] in snake:
                if [j, i] == snake[0]:
                    print("O", end=" ")
                else:
                    print("o", end=" ")
            elif [j, i] == [apple_x, apple_y]:
                print("x", end=" ")
            else:
                print(" ", end=" ")
        print("#")
    print("# "*width)

def handle_input(key, direction, running):
    if key == "w":
        if direction != "down":
            direction = "up"
    elif key == "s":
        if direction != "up":
            direction = "down"
    elif key == "a":
        if direction != "right":
            direction = "left"
    elif key == "d":
        if direction != "left":
            direction = "right"
    elif key == "q":
        running = False
    return direction, running

def main():
    width = 20
    height = 10
    snake = [[10, 5], [9, 5], [8, 5]]
    head_x, head_y = snake[0]
    direction = "right"
    running = True
    apple_x, apple_y = generate_apple(width, height, snake)

    while running:
        os.system("cls")
        draw_grid(width, height, snake, apple_x, apple_y)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8").lower()
            direction, running = handle_input(key, direction, running)
        new_head = get_new_head(head_x, head_y, direction)
        snake.insert(0, new_head)
        head_x, head_y = new_head
        if head_x == apple_x and head_y == apple_y:
            apple_x, apple_y = generate_apple(width, height, snake)
        else:
            snake.pop()
        running = check_loss(width, height, snake, head_x, head_y, running)
        time.sleep(0.3)

if __name__ == "__main__":
    main()