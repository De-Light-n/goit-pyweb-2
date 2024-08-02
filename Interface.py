from abc import ABC, abstractmethod
import pickle

from address_book import AddressBook, Record


def input_error(func):
    """Decorator that returns the error text without stopping the program
    Args:
        func
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments was gained."
        except Exception as e:
            return  f"{e}"
    return inner

class Interface(ABC):
    """Abstract interface class
    """
    @abstractmethod
    def add_contact(self, args):
        pass

    @abstractmethod
    def change_contact(self, args):
        pass

    @abstractmethod
    def show_all(self):
        pass

    @abstractmethod
    def add_birthday(self, args):
        pass

    @abstractmethod
    def show_birthday(self, args):
        pass

    @abstractmethod
    def birthdays(self):
        pass

    @abstractmethod
    def show_help(self):
        pass
    
    @abstractmethod
    def show_phone(self, args):
        pass
    
class ConsoleInterfase(Interface):
    def __init__(self, filename = "addressbook.pkl"):
        self.filename = filename
        self.book = self.load_data()
    
    def save_data(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.book, f)
            
    def load_data(self):
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()
    
    @input_error
    def add_contact(self, args):
        name, phone, *_ = args
        record = self.book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    @input_error
    def change_contact(self, args):
        name, old_phone, new_phone, *_ = args
        record = self.book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return "Contact changed"
        else:
            return "Contact not founded"

    @input_error
    def show_all(self):
        return self.book

    @input_error
    def add_birthday(self, args):
        name, birthday, *_ = args
        record = self.book.find(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        else:
            return "Contact not founded"

    @input_error
    def show_birthday(self, args):
        record = self.book.find(args[0])
        if record:
            return record.birthday
        else:
            return "Contact not founded"

    @input_error
    def birthdays(self):
        bds = self.book.get_upcoming_birthdays()
        if bds:
            string = ""
            for contact in bds:
                string += f"{contact["name"]}: {contact["congratulation_date"]}\n"
            return string
        else:
            return "There is not upcoming birthdays"

    @input_error
    def show_help(self):
        return "How can I help you?\nComands:\nadd [name] [phone]\nchange [name] [old phone] [new phone] \
                    \nphone [name] \nall\nadd-birthday [name] [date in format 'DD.MM.YYYY']\nshow-birthday [name]\
                    \nbirthdays\nexit\nclose"
    
    @input_error
    def show_phone(self, args):
        record = self.book.find(args[0])
        if record:
            return record
        else:
            return "Contact not founded"

    @staticmethod
    @input_error
    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args


    def activate(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print(self.show_help())

            elif command == "add":
                print(self.add_contact(args))

            elif command == "change":
                print(self.change_contact(args))

            elif command == "phone":
                print(self.show_phone(args))

            elif command == "all":
                print(self.show_all())

            elif command == "add-birthday":
                print(self.add_birthday(args))

            elif command == "show-birthday":
                print(self.show_birthday(args))

            elif command == "birthdays":
                print(self.birthdays())

            else:
                print("Invalid command.")
                
        self.save_data()

if __name__ == "__main__":
    user = ConsoleInterfase()
    user.activate()