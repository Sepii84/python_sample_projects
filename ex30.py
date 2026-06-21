# Keyboard Input Without Pressing Enter

import os
import time
import msvcrt

def draw_grid(width, height, x, y):
    print("#"*width)
    for i in range(height - 2):
        if y-1 == i:
            print("#" + " " * (x-1) + "O" + " " * (width - x - 2) + "#")
        else:
            print("#" + " " * (width-2) + "#")
    print("#"*width)

def handle_input(key, direction, running):
    if key == "w":
        direction = "up"
    elif key == "s":
        direction = "down"
    elif key == "a":
        direction = "left"
    elif key == "d":
        direction = "right"
    elif key == "q":
        running = False
    return direction, running

def move_player(x, y, direction):
    if direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    elif direction == "left":
        x -= 1
    elif direction == "right":
        x += 1
    return x, y

def wrap_position(x, y, width, height):
    if x <= 0:
        x = width - 2
    elif x >= width - 1:
        x = 1
    if y <= 0:
        y = height - 2
    elif y >= height - 1:
        y = 1
    return x, y

def main():
    width = 20
    height = 10
    x = 10
    y = 5
    direction = "right"
    running = True

    while running:
        os.system("cls")
        draw_grid(width, height, x, y)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8").lower()
            direction, running = handle_input(key, direction, running)
        x, y = move_player(x, y, direction)
        x, y = wrap_position(x, y, width, height)
        time.sleep(0.2)

if __name__ == "__main__":
    main()