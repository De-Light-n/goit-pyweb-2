from datetime import datetime, date, timedelta
from collections import UserDict
from abc import ABC

class Field(ABC):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
	def __init__(self, value):
         super().__init__(value)


class Phone(Field):
    def __init__(self, value:str):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Not enough numbers in phone number.")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone:str):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone:str):
        for item in self.phones:
            if phone == item.value:
                self.phones.remove(item)
                return
    
    def edit_phone(self, old, new):
        for phone in self.phones:
            if old == phone.value:
                self.remove_phone(old)
                self.add_phone(new)
                return
        raise ValueError
   
    def find_phone(self, phone:str)->Phone|None:
        for i in self.phones:
            if i.value == phone:
                return i
        return None
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data.update({record.name.value:record})
        
    def find(self, name:str)->Record|None:
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name, None)
    
    def __str__(self) -> str:
        string = "\nYour address book\n--------------------------\n"
        for value in self.data.values():
            string += str(value) + "\n"
        string += "--------------------------\n"
        return string

    #get_upcoming_birthdays section
    @staticmethod
    def string_to_date(date_string):
        return datetime.strptime(date_string, "%Y.%m.%d").date()

    @staticmethod
    def date_to_string(date):
        return date.strftime("%d.%m.%Y")

    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for name, contact in self.data.items():
            if contact.birthday:
                birthday_this_year = contact.birthday.value.replace(year=today.year).date()
                if birthday_this_year < today:
                    birthday_this_year += timedelta(days=366)
                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                    congratulation_date_str = self.date_to_string(birthday_this_year)
                    upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays
    
    def __getstate__(self):
        state = self.__dict__
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        
