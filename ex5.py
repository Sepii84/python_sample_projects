# library book borrow system

class Book:

    def __init__(self, title, author):
        self.title = title.strip()
        self.author = author.strip()
        self.is_borrowed = False

    def __str__(self):
        if self.is_borrowed:
            return f"Title: {self.title}, Author: {self.author}, Status: Borrowed"
        return f"Title: {self.title}, Author: {self.author}, Status: Available"

class Library:

    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        print("Book added.")

    def show_books(self):
        if not self.books:
            print("No books available")
            return
        for book in self.books:
            print(book)

    def find_book(self, title):
        target_title = title.strip().lower()
        for book in self.books:
            if book.title.lower() == target_title:
                return book
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if not book:
            print("Book not found")
            return
        if book.is_borrowed:
            print("Book already borrowed")
            return
        book.is_borrowed = True
        print("Book borrowed.")

    def return_book(self, title):
        book = self.find_book(title)
        if not book:
            print("Book not found")
            return
        if not book.is_borrowed:
            print("Book was not borrowed")
            return
        book.is_borrowed = False
        print("Book returned.")

    def search_book(self, title):
        book = self.find_book(title)
        if not book:
            print("Book not found")
            return
        print(book)

def main():
    library = Library()
    while True:
        print("----------------------")
        try:
            choice = int(input("1) Add book\n"
                               "2) Show all books\n"
                               "3) Borrow book\n"
                               "4) Return book\n"
                               "5) Search by title\n"
                               "6) Exit\n"))
        except ValueError:
            print("Please enter a number between 1 and 6")
            continue
        match choice:
            case 1:
                title = input("Enter the title: ").strip()
                if not title:
                    print("Invalid book data")
                    continue
                author = input("Enter the author: ").strip()
                if not author:
                    print("Invalid book data")
                    continue
                library.add_book(title, author)
            case 2:
                library.show_books()
            case 3:
                title = input("Enter the book you want to borrow: ")
                library.borrow_book(title)
            case 4:
                title = input("Enter the book you want to return: ")
                library.return_book(title)
            case 5:
                title = input("Enter the title to search for: ")
                library.search_book(title)
            case 6:
                print("Goodbye!")
                break
            case _:
                print("Please enter a number between 1 and 6")

if __name__ == '__main__':
    main()