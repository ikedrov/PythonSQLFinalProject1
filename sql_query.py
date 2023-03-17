'''
1. Создать пользователя с Number_card = 2345, Pin_code = 2222, Balance = 10000
2. Создать метод transfer_money для перевода денежных средств между клиентами
3. Добавить в метод input_operation новый метод:
 - в описание "5. Перевести денежные средства.
 - в условия данный метод должен запускаться если пользователь ввел "5"
'''
'''1. Добавить в метод transfer_money метод report_operation_1, для фиксации отправки денежных средств другому клиенту
тип операции - type_operation = 3. Проверить что данный метод работает корректно
2. Создать файл report_2.csv, включающий поля Date, Payee, Type operation, Amount, Sender.
3. Создать метод report_operation_2, который будет принимать в себя следующие значения и помещать в report_2.csv
при успешной прохожднии операции по переводу денежных средств:
Data - now_date,
Payee - payee,
Type operation - type_operation, 3
Amount - amount,
Sender - number_card (отправитель)
4. Добавить в метод transfer_money метод report_operation_2'''
import csv
import datetime
import sqlite3

now_date = datetime.datetime.utcnow().strftime('%H:%M-%d.%m.%Y')


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
                    SqlAtm.operation_report_1(now_date, card_number, '1', amount, '')
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
                SqlAtm.operation_report_1(now_date, card_number, '2', amount, '')
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
                    SqlAtm.operation_report_1(now_date, card_number, '3', amount, '')
                    SqlAtm.operation_report_2(now_date, transfer_card, '3', amount, card_number)
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

    @staticmethod
    def operation_report_1(now_date, card_number, operation_type, amount, payee):

        user_data = [
            (now_date, card_number, operation_type, amount, payee)
        ]

        with open('report_1.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Data added to report')

    @staticmethod
    def operation_report_2(now_date, payee, operation_type, amount, sender):

        user_data = [
            (now_date, payee, operation_type, amount, sender)
        ]

        with open('report_2.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Data added to report')

'''Operation types
1. Cash withdraw
2. Cash deposit
3. Cash transfer'''
#SqlAtm.operation_report_2()