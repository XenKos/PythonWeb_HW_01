from classes import Field, Name, Phone, Birthday, Record, AddressBook
import re
import pickle
from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class UserInterface(ABC):  #Абстрактний клас для  користувальницького інтерфейсу
    @abstractmethod
    def print_contact_info(self, record): #Абстрактний метод для виведення інформації про контакт 
        pass

    @abstractmethod
    def print_command_info(self): #Абстрактний метод для виведення інформації про доступні команди
        pass

class ConsoleUserInterface(UserInterface): #Клас для консольного користувальницького інтерфейсу
    def print_contact_info(self, record):
        print(f"Contact name: {record.name}, phones: {', '.join(str(phone) for phone in record.phones)}")

    def print_command_info(self):
        print("Available commands:")
        print("  - hello: Print a welcome message")
        print("  - add: Add a new contact")
        print("  - change: Change a contact's phone number")
        print("  - find: Find record")
        print("  - delete: Delete record")
        print("  - all: Show all contacts")
        print("  - add-birthday: Added contact's Birthday date")
        print("  - show-birthday: Show contact's birthday")
        print("  - birthdays: Show upcoming birthdays for the next week")


def parse_input(user_input):
    parts = user_input.split(maxsplit=1)
    cmd = parts[0].strip().lower()
    args = parts[1].strip() if len(parts) > 1 else None
    return cmd, args


def main():
    book = AddressBook()
    book.load_data() 
    ui = ConsoleUserInterface()  # Ініціалізуємо консольний інтерфейс
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)  
         
        if command in ['exit', 'close']:
            print("Good bye!")
            break

        elif command == 'hello':
            print("How can I help you?")

        elif command == 'add':
            try:
                name, *phones = args.split()
                record = Record(name)
                for phone in phones:
                    if not re.match(r'^\d{10}$', phone):
                        raise ValueError("Invalid phone number format")
                    record.add_phone(phone)
                book.add_record(record)
                print("Contact added.")
            except ValueError as e:
                print(e)

        elif command == 'change':
            name, new_phone = args.split()
            record = book.find(name)
            if record:
                try:
                    record.edit_phone(record.phones[0].value, new_phone)
                    print("Contact updated.")
                except ValueError as e:
                    print(e)
            else:
                print("Contact not found.")

        elif command == 'phone':
            name = args.strip()
            record = book.find(name)
            if record:
                print(f"\n{name}'s phone number: {record.phones[0].value}")
            else:
                print("Contact not found.")

        elif command == 'find':
            name = args.strip()
            record = book.find(name)
            if record:
                 print(f"Found record: {record}")
            else:
                 print("Record not found.")

        elif command == 'delete':
            name = args.strip()
            if name in book.data:
                book.delete(name)
                print(f"Record '{name}' deleted successfully.")
            else:
                print("Record not found.")
                 
        elif command == 'all':
            if book:
                result = "All contacts:"
                for name, record in book.data.items():
                    result += f"\n{name}: {record.phones[0].value}"
                print(result)
            else:
                print("Phonebook is empty.")
      
        elif command == "add-birthday":
            if args:
                name, birthday_str = args.split()
                try:
                    record = book.find(name)
                    if record:
                        birthday = datetime.strptime(birthday_str, "%d.%m.%Y")
                        record.add_birthday(birthday)
                        print("Birthday's date added")
                    else:
                        print("Contact not found")
                except ValueError as e:
                    print(e)
            else:
                print("Invalid command format. Please provide name and birthday.")

        elif command == "show-birthday":
            name = args.strip()
            record = book.find(name)
            if record:
                if record.birthday:
                    print(f"{name}'s Birthday is: {record.birthday.strftime('%d.%m.%Y')}")
                else:
                    print(f"{name} has no registered birthday.")
            else:
                print("Contact not found.")

        elif command == "birthdays":
            upcoming_birthdays = book.get_upcoming_birthdays()
            if upcoming_birthdays:
                print("Users to greet in the next week:")
                for record in upcoming_birthdays:
                    print(record.name)
            else:
                print("No upcoming birthdays in the next week.")

        else:
            print("Invalid command. Please try again.")
    
if __name__ == "__main__":
    book = AddressBook()
    book.load_data()  # Завантаження даних перед початком роботи програми
    main()
    book.save_data()

   