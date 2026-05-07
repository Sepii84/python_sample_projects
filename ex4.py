# contact book manager

class Contact:
    contact_list = []

    def __init__(self, name, phone, age):
        self.name = name.strip()
        self.phone = phone
        self.age = age
        Contact.contact_list.append(self)

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Age: {self.age}"

    @classmethod
    def search(cls, name):
        target_name = name.strip().lower()
        for contact in cls.contact_list:
            if contact.name.lower() == target_name:
                print(contact)
                return
        print("Contact not found")

    @classmethod
    def display(cls):
        if not cls.contact_list:
            print("No contacts available")
            return
        for contact in cls.contact_list:
            print(contact)

    @classmethod
    def delete(cls, name):
        target_name = name.strip().lower()
        for contact in cls.contact_list:
            if contact.name.lower() == target_name:
                cls.contact_list.remove(contact)
                print("Contact deleted.")
                return
        print("Contact not found")

def main():
    while True:
        try:
            choice = int(input("1) Add a contact\n"
                               "2) Show all contacts\n"
                               "3) Search by name\n"
                               "4) Delete contact by name\n"
                               "5) Exit\n"))
        except ValueError:
            print("Please enter a number between 1 and 5")
            continue
        match choice:
            case 1:
                name = (input("Enter the name: ")).strip()
                if not name:
                    print("Invalid name")
                    continue
                phone = input("Enter the phone number: ")
                try:
                    age = int(input("Enter the age: "))
                except ValueError:
                    print("Invalid age")
                    continue
                if age <= 0:
                    print("Invalid age")
                    continue
                Contact(name, phone, age)
                print("Contact added.")
            case 2:
                Contact.display()
            case 3:
                name = input("Enter the name of the contact: ")
                Contact.search(name)
            case 4:
                name = input("Enter the name of the contact to delete: ")
                Contact.delete(name)
            case 5:
                print("Goodbye!")
                break
            case _:
                print("Please enter a number between 1 and 5")

if __name__ == '__main__':
    main()