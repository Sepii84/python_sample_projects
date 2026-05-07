#student score tracker

class Student:

    def __init__(self, name):
        self.name = name
        self.scores = []

    def add_score(self, score):
        if score > 100 or score < 0:
            print("Score must be between 0 and 100")
            return
        self.scores.append(score)
        print("Score added.")

    def show_scores(self):
        if not self.scores: #same as if len(self.scores) == 0:
            print("No scores available")
            return 
        print(f"Scores: {self.scores}")

    def get_average(self):
        if not self.scores:
            print("No scores available")
            return
        avg = round(sum(self.scores) / len(self.scores), 2)
        print(f"Average: {avg}")

    def get_high_low(self):
        if not self.scores:
            print("No scores available")
            return
        lowest = min(self.scores)
        highest = max(self.scores)
        print(f"Highest: {highest:.1f}")
        print(f"Lowest: {lowest:.1f}")


def main():
    name = input("What is the student name? ")
    student = Student(name)
    while True:
        try:
            choice = int(input("1) Add a score\n"
                       "2) Show all scores\n"
                       "3) Show average score\n"
                       "4) Show highest and lowest score\n"
                       "5) Exit\n"))
        except ValueError:
            print("Please enter a number from 1 to 5")
            continue
        match choice:
            case 1:
                try:
                    score = float(input("Enter the grade you want to add: "))
                except ValueError:
                    print("Invalid score")
                    continue
                student.add_score(score)
            case 2:
                student.show_scores()
            case 3:
                student.get_average()
            case 4:
                student.get_high_low()
            case 5:
                print("Goodbye!")
                break
            case _:
                print("Please enter a number from 1 to 5")
                continue

if __name__ == '__main__':
    main()