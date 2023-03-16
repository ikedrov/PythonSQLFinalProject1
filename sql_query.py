'''
1. Создать пользователя с Number_card = 2345, Pin_code = 2222, Balance = 10000
2. Создать метод transfer_money для перевода денежных средств между клиентами
3. Добавить в метод input_operation новый метод:
 - в описание "5. Перевести денежные средства.
 - в условия данный метод должен запускаться если пользователь ввел "5"
'''

import sqlite3


class SqlAtm:

    @staticmethod
    def create_table():

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Card_number INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);''')
            print('Created Users_data table')

    @staticmethod
    def add_users(data_users):

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute('''INSERT OR REPLACE INTO Users_data (Card_number, Pin_code, Balance) VALUES (?, ?, ?)''', data_users)
            print('Added new user')

    @staticmethod
    def card_input(card_number):

        try:
            with sqlite3.connect('atm.db') as db:
                cur = db.cursor()
                cur.execute(f'''SELECT Card_number FROM Users_data WHERE Card_number = {card_number}''')
                card_result = cur.fetchone()
                if card_result == None:
                    print('No such card number')
                    return False
                else:
                    print(f'Inserted card # {card_number}')
                    return True
        except:
            print('No such card number')

    @staticmethod
    def pin_input(card_number):

        pin_code = input('Enter pin code: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Pin_code FROM Users_data WHERE Card_number = {card_number}''')
            pin_result = cur.fetchone()
            code_input = pin_result[0]
            try:
                if code_input == int(pin_code):
                    print('Pin OK')
                    return True
                else:
                    print('Incorrect Pin')
                    return False
            except:
                print('Incorrect Pin')
                return False

    @staticmethod
    def balance_info(card_number):

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Balance FROM Users_data WHERE Card_number = {card_number}''')
            balance_info_result = cur.fetchone()
            card_balance = balance_info_result[0]
            print(f'Your balance {card_balance}')

    @staticmethod
    def cash_withdraw(card_number):

        amount = input('Enter amount you want to withdraw: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Balance FROM Users_data WHERE Card_number = {card_number}''')
            balance_info_result = cur.fetchone()
            card_balance = balance_info_result[0]
            try:
                if int(amount) > card_balance:
                    print('Not enough money')
                    return False
                else:
                    cur.execute(f'''UPDATE Users_data SET Balance = Balance - {amount} WHERE Card_number = {card_number}''')
                    db.commit()
                    SqlAtm.balance_info(card_number)
                    return True
            except:
                print('Invalid input')
                return False

    @staticmethod
    def cash_deposit(card_number):

        amount = input('Enter amount you want to deposit: ')
        with sqlite3.connect('atm.db') as db:
            try:
                cur = db.cursor()
                cur.execute(f'''UPDATE Users_data SET Balance = Balance + {amount} WHERE Card_number = {card_number}''')
                db.commit()
                SqlAtm.balance_info(card_number)
                return True
            except:
                print('Invalid input')
                return False

    @staticmethod
    def transfer_money(card_number):

        amount = input('Enter amount you want to transfer: ')
        transfer_card = input('Enter the card number where you want to transfer money: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Balance FROM Users_data WHERE Card_number = {card_number}''')
            balance_info_result = cur.fetchone()
            card_balance = balance_info_result[0]
            cur.execute('''SELECT Card_number FROM Users_data''')
            card_info_result = cur.fetchall()
            cards_info = card_info_result
            print(cards_info)
            try:
                if int(amount) > card_balance:
                    print('Not enough money')
                    return False
                elif not (any(int(transfer_card) in i for i in cards_info)) or int(transfer_card) == int(card_number):
                    print('No such card or you are trying to transfer to your own card')
                    return False
                else:
                    cur.execute(
                        f'''UPDATE Users_data SET Balance = Balance - {amount} WHERE Card_number = {card_number}''')
                    db.commit()
                    SqlAtm.balance_info(card_number)
                    cur.execute(
                        f'''UPDATE Users_data SET Balance = Balance + {amount} WHERE Card_number = {transfer_card}''')
                    db.commit()
                    print('Operation completed')
                    return True
            except:
                print('Invalid input')
                return False

    @staticmethod
    def input_operation(card_number):

        while True:
            operation = input('Enter operation you want to execute\n'
                              '1. Balance info\n'
                              '2. Cash withdraw\n'
                              '3. Cash deposit\n'
                              '4. Finish service\n'
                              '5. Transfer money\n')

            if operation == '1':
                SqlAtm.balance_info(card_number)
            elif operation == '2':
                SqlAtm.cash_withdraw(card_number)
            elif operation == '3':
                SqlAtm.cash_deposit(card_number)
            elif operation == '4':
                print('Session closed')
                return False
            elif operation == '5':
                SqlAtm.transfer_money(card_number)
            else:
                print('Invalid operation')
