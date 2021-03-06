import datetime
import time
import validator


class View:
    def __init__(self):
        self.valid = validator.Validator()

    def cannot_delete(self) -> None:
        print('this record is connected with another table, deleting will '
              'throw error')

    def sql_error(self, e) -> None:
        print("[INFO] Error while working with Postgresql", e)

    def insertion_error(self) -> None:
        print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def updation_error(self) -> None:
        print('Something went wrong (record with such id does not exist or inappropriate foreign key value)')

    def deletion_error(self) -> None:
        print('record with such id does not exist')

    def invalid_interval(self) -> None:
        print('invalid interval input')

    def print_time(self, start) -> None:
        print("--- %s seconds ---" % (time.time() - start))

    def print_search(self, result):
        print('search result:')
        for row in result:
            for i in range(0, len(row)):
                print(row[i])
            print('_______________________________________________________')

    def print_cinema(self, table):
        print('cinema table:')
        for row in table:
            print('cinema_id:', row[0], '\tname:', row[1], '\taddress:', row[2])
            print('_______________________________________________________')

    def print_hall(self, table):
        print('hall table:')
        for row in table:
            print('number:', row[0], '\tcinema_id:', row[1], '\tscreen_size:', row[2], '\tnumber_of_seats:', row[3])
            print('_______________________________________________________')

    def print_movie(self, table):
        print('movie table:')
        for row in table:
            print('movie_id:', row[0], '\tcinema_id:', row[1], '\ttitle:', row[2], '\trating:', row[3])
            print('_______________________________________________________')

    def print_seat(self, table):
        print('seat table:')
        for row in table:
            print('seat_id:', row[0], '\tnumber:', row[1], '\trow:', row[2], '\tseat_number:', row[3], '\tis_occupied:', row[4])
            print('_______________________________________________________')

    def print_session(self, table):
        print('session table:')
        for row in table:
            print('session_id:', row[0], '\tmovie_id:', row[1], '\tnumber:', row[2], '\ttime:', row[3], '\tcost:', row[4])
            print('_______________________________________________________')

    def print_help(self):
        print('print_table - outputs the specified table \n\targument (table_name) is required')
        print('delete_record - deletes the specified record from table \n'
              '\targuments (table_name, key_name, key_value) are required')
        print('update_record - updates record with specified id in table\n'
              '\tsession args (table_name, session_id, movie_id, number(id of hall), time, cost)\n'
              '\tmovie args (table_name, movie_id, cinema_id, title, rating)\n'
              '\thall args (table_name, number(id), cinema_id, screen_size, number_of_seats)\n'
              '\tseat args (table_name, seat_id, number(id of hall), row, seat_number, is_occupied)\n'
              '\tcinema args (table_name, cinema_id, name, adress)')
        print('insert_record - inserts record into specified table \n'
              '\tsession args (table_name, session_id, movie_id, number(id of hall), time, cost)\n'
              '\tmovie args (table_name, movie_id, cinema_id, title, rating)\n'
              '\thall args (table_name, number(id), cinema_id, screen_size, number_of_seats)\n'
              '\tseat args (table_name, seat_id, number(id of hall), row, seat_number, is_occupied)\n'
              '\tcinema args (table_name, cinema_id, name, adress)')
        print('generate_randomly - generates n random records in table\n'
              '\targuments (table_name, n) are required')
        print('search_records - search for records in two or more tables using one or more keys \n'
              '\targuments (table1_name, table2_name, table1_key, table2_key) are required, \n'
              '\tif you want to perform search in more tables: \n'
              '\t(table1_name, table2_name, table3_name, table1_key, table2_key, table3_key, table13_key) \n'
              '\t(table1_name, table2_name, table3_name, table4_name, table1_key, table2_key, table3_key, table13_key, '
              'table4_key, table24_key)')

    def proceed_search(self, search_num):
        search = ''
        for i in range(0, search_num):
            while True:
                search_type = input('specify the type of data you want to search for '
                                    '(numeric, string or date): ')
                if search_type == 'numeric' or search_type == 'string' or search_type == 'date':
                    break
            key = input('specify the name of key by which you`d like to perform search '
                        'in form: table_number.key_name: ')

            if search_type == 'numeric':
                a = input('specify the left end of search interval: ')
                b = input('specify the right end of search interval: ')
                if search == '':
                    search = self.numeric_search(a, b, key)
                else:
                    search += ' and ' + self.numeric_search(a, b, key)

            elif search_type == 'date':
                data = input('specify the left end of search interval '
                             'in form: year.month.day.hour.minute.second: ')
                datb = input('specify the right end of search interval '
                             'in form: year.month.day.hour.minute.second: ')
                if search == '':
                    search = self.date_search(data, datb, key)
                else:
                    search += ' and ' + self.date_search(data, datb, key)

            elif search_type == 'string':
                string = input('specify the string you`d like to search for: ')
                if search == '':
                    search = self.string_search(string, key)
                else:
                    search += ' and ' + self.string_search(string, key)
        return search

    def numeric_search(self, a: str, b: str, key: str):
        try:
            a, b = int(a), int(b)
        except ValueError:
            self.invalid_interval()
        else:
            return f"{a}<{key} and {key}<{b}"

    def date_search(self, a: str, b: str, key: str):
        try:
            arr = [int(x) for x in a.split(sep='.')]
            brr = [int(x) for x in b.split(sep='.')]
        except Exception:
            print(Exception)
            self.invalid_interval()
        else:
            return f"{key} BETWEEN \'{datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])}\' " \
                   f"AND \'{datetime.datetime(brr[0], brr[1], brr[2], brr[3], brr[4], brr[5])}\'"

    def string_search(self, string: str, key: str):
        return f"{key} LIKE \'{string}\'"

    def get_search_num(self):
        return input('specify the number of attributes you`d like to search by: ')

    def invalid_search_num(self):
        print('should be number different from 0')

    def argument_error(self):
        print('no required arguments specified')

    def wrong_table(self):
        print('wrong table name')

    def no_command(self):
        print('no command name specified, type help to see possible commands')

    def wrong_command(self):
        print('unknown command name, type help to see possible commands')