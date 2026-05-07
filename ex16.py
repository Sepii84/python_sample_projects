# media library manager with JSON persistence

import json

class MediaItem:
    def __init__(self, title, creator, year):
        self.title = title
        self.creator = creator
        self.year = year


    def display(self, index):
        print(f"[{index}] Title: {self.title} | "
              f"Creator: {self.creator} | "
              f"Year: {self.year}")

    def to_dict(self):
        return {
            "type": "unknown",
            "title": self.title,
            "creator": self.creator,
            "year": self.year
        }

class Book(MediaItem):
    def __init__(self, title, creator, year, pages):
        super().__init__(title, creator, year)
        self.pages = pages

    def display(self, index):
        print(f"[{index}] Book: {self.title} | "
              f"Author: {self.creator} | "
              f"Year: {self.year} | "
              f"Pages: {self.pages}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "book",
            "pages": self.pages
        })
        return data

class Movie(MediaItem):
    def __init__(self, title, creator, year, duration):
        super().__init__(title, creator, year)
        self.duration = duration

    def display(self, index):
        print(f"[{index}] Movie: {self.title} | "
              f"Director: {self.creator} | "
              f"Year: {self.year} | "
              f"Duration: {self.duration} minutes")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "movie",
            "duration": self.duration
        })
        return data

def add_media():
    title = input("Enter the title: ").strip()
    if not title:
        print("Invalid media data")
        return None
    creator = input("Enter the creator: ").strip()
    if not creator:
        print("Invalid media data")
        return None
    try:
        year = int(input("Enter the year: "))
    except ValueError:
        print("Invalid media data")
        return None
    if year <= 0:
        print("Invalid media data")
        return None
    return title, creator, year

def add_book(medias):
    result = add_media()
    if not result:
        return
    title, creator, year = result

    try:
        pages = int(input("Enter the pages: "))
    except ValueError:
        print("Invalid pages")
        return
    if pages <= 0:
        print("Invalid pages")
        return
    medias.append(Book(title, creator, year, pages))
    print("Book added.")

def add_movie(medias):
    result = add_media()
    if not result:
        return
    title, creator, year = result

    try:
        duration = int(input("Enter the duration in minutes: "))
    except ValueError:
        print("Invalid duration")
        return
    if duration <= 0:
        print("Invalid duration")
        return
    medias.append(Movie(title, creator, year, duration))
    print("Movie added.")


def show_media(medias):
    if not medias:
        print("No media available")
        return
    for index, media in enumerate(medias, start=1):
        media.display(index)

def search_media(medias):
    if not medias:
        print("No media available")
        return
    keyword = input("Enter the keyword to search in titles: ").strip().lower()
    found = False
    for index, media in enumerate(medias, start=1):
        if keyword in media.title.lower():
            media.display(index)
            found = True
    if not found:
        print("No matching media")

def delete_media(medias):
    if not medias:
        print("No media available")
        return
    show_media(medias)
    try:
        deletion = int(input("Enter the number to delete: "))
    except ValueError:
        print("Invalid item number")
        return
    if deletion < 1 or deletion > len(medias):
        print("Invalid item number")
        return
    medias.pop(deletion - 1)
    print("Media item deleted.")

def save_to_file(medias):
    output_file = "media_library.json"
    try:
        with open(output_file, "w") as file:
            data = []
            for media in medias:
                data.append(media.to_dict())
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Media saved.")

def load_from_file():
    medias = []
    input_file = "media_library.json"
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
            for media in data:
                try:
                    if media["type"] == "book":
                        medias.append(Book(
                            media["title"],
                            media["creator"],
                            media["year"],
                            media["pages"]
                        ))
                    elif media["type"] == "movie":
                        medias.append(Movie(
                            media["title"],
                            media["creator"],
                            media["year"],
                            media["duration"]
                        ))
                except KeyError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    except json.JSONDecodeError:
        print("Invalid JSON file")
        return 
    print("Media loaded.")
    return medias

def main():
    medias = []
    while True:
        try:
            choice = int(input("1) Add book\n"
                               "2) Add movie\n"
                               "3) Show all media\n"
                               "4) Search by title\n"
                               "5) Delete media item\n"
                               "6) Save to JSON\n"
                               "7) Load from JSON\n"
                               "8) Exit\n"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                add_book(medias)
            case 2:
                add_movie(medias)
            case 3:
                show_media(medias)
            case 4:
                search_media(medias)
            case 5:
                delete_media(medias)
            case 6:
                save_to_file(medias)
            case 7:
                loaded_media = load_from_file()
                if loaded_media is not None:
                    medias = loaded_media
            case 8:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")
                continue

if __name__ == '__main__':
    main()