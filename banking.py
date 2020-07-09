import random
import _sqlite3

conn = _sqlite3.connect("card.s3db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS card (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                    number TEXT, 
                    pin TEXT,
                    balance INTEGER
                    )''')
conn.commit()


class Card:

    def __init__(self):
        self.data = []
        self.action = True
        self.start()
        self.log = 0

    def start(self):
        while self.action:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            inp = input()
            if inp == "0":
                print("Bye!")
                conn.close()
                self.action = False
            if inp == "1":
                self.create()
            if inp == "2":
                self.login()

    def create(self):
        pin = "".join([str(random.randint(0, 9)) for i in range(4)])
        account_identifier = "".join([str(random.randint(0, 9)) for i in range(9)])
        temp_numb = [int(i) for i in f"400000{account_identifier}"]
        for i in range(len(temp_numb)):
            if i % 2 != 1:
                temp_numb[i] *= 2
                if temp_numb[i] > 9:
                    temp_numb[i] -= 9
        if sum(temp_numb) % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - (sum(temp_numb) % 10)
        number = f"400000{account_identifier}{checksum}"
        balance = 0
        self.data.append(number)
        self.data.append(pin)
        self.data.append(balance)
        c.execute(f"INSERT INTO card (number, pin, balance) VALUES ({number},{pin},{balance})")
        conn.commit()
        print("Your card has been created")
        print("Your card number:")
        print(number)
        print("Your card PIN:")
        print(pin)
        print()

    def login(self):
        number_input = input("Enter your card number:")
        pin_input = input("Enter your PIN:")
        c.execute("SELECT number FROM card")
        items = c.fetchall()
        c.execute(f"SELECT pin FROM card WHERE number = {number_input}")
        item_pin = c.fetchone()
        for item in items:
            if number_input in item:
                items = number_input
        if number_input == items and pin_input in item_pin:
            print()
            print("You have successfully logged in!")
            print()
            self.log = number_input
            self.authorized()
        else:
            print()
            print("Wrong card number or PIN!")
            print()

    def authorized(self):
        while self.log != 0:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            inp = input()
            if inp == "1":
                self.balance()
            elif inp == "2":
                self.add_income()
            elif inp == "3":
                self.transfer()
            elif inp == "4":
                self.close_acc()
            elif inp == "5":
                print()
                print("You have successfully logged out!")
                print()
                break
            elif inp == "0":
                print("Bye!")
                conn.close()
                self.log = 0
                self.action = False

    def balance(self):
        c.execute(f"SELECT balance FROM card WHERE number = {self.log}")
        temp = c.fetchone()
        print()
        print(f"Balance: {temp[0]}")
        print()

    def add_income(self):
        print("Enter income:")
        to_add = int(input())
        c.execute(f"SELECT balance FROM card WHERE number = {self.log}")
        temp = c.fetchone()
        c.execute(f"UPDATE card SET balance = {temp[0] + to_add} WHERE number = {self.log}")
        conn.commit()
        print()
        print("Income was added!")
        print()

    def transfer(self):
        print("Transfer")
        print("Enter card number:")
        num = input()
        if self.luhn_check(num):
            c.execute(f"SELECT number FROM card WHERE number = {num}")
            temp = c.fetchone()
            try:
                a = temp[0] != num
            except TypeError:
                print("Such a card does not exist.")
                print()
            else:
                print("Enter how much money you want to transfer:")
                money = int(input())
                c.execute(f"SELECT balance FROM card WHERE number = {self.log}")
                temp = c.fetchone()
                if temp[0] >= money:
                    c.execute(f"UPDATE card SET balance = {temp[0] - money} WHERE number = {self.log}")
                    conn.commit()
                    c.execute(f"SELECT balance FROM card WHERE number = {num}")
                    t = c.fetchone()
                    c.execute(f"UPDATE card SET balance = {t[0] + money} WHERE number = {num}")
                    conn.commit()
                    print("Success!")
                    print()
                else:
                    print("Not enough money!")
                    print()
        else:
            print("Probably you made mistake in the card number. Please try again!")
            print()

    def close_acc(self):
        c.execute(f"DELETE FROM card WHERE number = {self.log}")
        conn.commit()
        self.log = 0
        print()
        print("The account has been closed!")
        print()

    def luhn_check(self, card_number):
        card_number = [int(i) for i in card_number]
        temp_numb = card_number[:-1]
        for i in range(len(temp_numb)):
            if i % 2 != 1:
                temp_numb[i] *= 2
                if temp_numb[i] > 9:
                    temp_numb[i] -= 9
        if sum(temp_numb) % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - (sum(temp_numb) % 10)
        return checksum == card_number[-1]


var = Card()
