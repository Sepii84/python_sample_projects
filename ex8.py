# wordle lite

def is_valid_guess(guess, answer):
    return len(guess) == len(answer) and guess.isalpha()

def get_feedback(guess, answer):
    secret = [" " for _ in range(len(answer))]
    guess_G_and_Ys = []
    answer_G_and_Ys = []

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            secret[i] = "G"
            guess_G_and_Ys.append(i)
            answer_G_and_Ys.append(i)

    for i in range(len(guess)):
        if i in guess_G_and_Ys:
            continue
        for j in range(len(answer)):
            if (answer[j] == guess[i]) and (j not in answer_G_and_Ys):
                secret[i] = "Y"
                guess_G_and_Ys.append(i)
                answer_G_and_Ys.append(j)
                break

    for i in range(len(secret)):
        if secret[i] == " ":
            secret[i] = "_"

    return "".join(secret)

def main():
    answer = "apple"
    counter = 0
    while True:
        print("--------------------")
        guess = input("What is your guess: ").strip().lower()
        if not is_valid_guess(guess, answer):
            print("Invalid guess")
            continue
        counter += 1
        print(get_feedback(guess, answer))
        if guess == answer:
            print(f"You won in {counter} attempts!")
            break
        elif counter >= 6:
            print(f"You lost. The word was: {answer.upper()}")
            break

if __name__ == '__main__':
    main()
