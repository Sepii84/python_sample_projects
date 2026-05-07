#number guessing game

import random

def main():
    low = 1
    high = 20
    random_num = random.randint(low, high)
    attempts = 0
    while True:
        try:
            guess = int(input("enter your guess: "))
        except ValueError:
            print("Invalid input")
            continue
        if guess < low or guess > high:
            print("Out of range")
            continue
        attempts += 1
        if guess > random_num:
            print("Too high")
        elif guess < random_num:
            print("Too low")
        else:
            print(f"Correct! Attempts: {attempts}")
            break
if __name__ == '__main__':
    main()