from sql_query import SqlAtm


class Atm:

    def atm_logic(self):

        SqlAtm.create_table()
#        SqlAtm.add_users((1234, 1111, 10000))
#        SqlAtm.add_users((2345, 2222, 10000))
        card_number = input('Card number: ')
        while True:
            if SqlAtm.card_input(card_number):
                if SqlAtm.pin_input(card_number):
                    SqlAtm.input_operation(card_number)
                    break
                else:
                    break
            else:
                break

start = Atm()
start.atm_logic()

