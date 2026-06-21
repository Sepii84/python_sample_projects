# Terminal Auto-Refresh Animation

import os
import time

def draw_grid(width, height, x, y):
    print("#"*width)
    for i in range(height - 2):
        if y-1 == i:
            print("#" + " " * (x-1) + "O" + " " * (width - x - 2) + "#")
        else:
            print("#" + " " * (width-2) + "#")
    print("#"*width)

def main():
    width = 20
    height = 10
    x = 1
    y = 1

    while True:
        os.system("cls")
        draw_grid(width, height, x, y)
        if x == width - 2 and y == height - 2:
            x = 1
            y = 1
        elif x == width - 2:
            y += 1
            x = 1
        else:
            x += 1
        time.sleep(0.02)

if __name__ == "__main__":
    main()