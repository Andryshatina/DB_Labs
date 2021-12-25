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
            print(row)

    def print_cinema(self, table):
        print('cinema table:')
        print("%13s%10s%35s" % ("cinema_id", "name", "adress"))
        for row in table:
            print(row)

    def print_hall(self, table):
        print('hall table:')
        print("%13s%10s%15s%18s" % ("number", "cinema_id", "screen_size", "number_of_seats"))
        for row in table:
            print(row)

    def print_movie(self, table):
        print('movie table:')
        print("%10s%12s%19s%25s" % ("movie_id", "cinema_id", "title", "rating"))
        for row in table:
            print(row)

    def print_seat(self, table):
        print('seat table:')
        print("%12s%10s%8s%10s%15s" % ("seat_id", "number", "row", "seat", "is_occupied"))
        for row in table:
            print(row)

    def print_session(self, table):
        print('session table:')
        print("%10s%32s%10s%28s%12s" % ("session_id", "movie_id", "number", "time", "cost"))
        for row in table:
            print(row)

    def print_help(self):
        print('print_table - outputs the specified table \n\targument (table_name) is required')
        print('delete_record - deletes the specified record from table \n'
              '\targuments (table_name, key_name, key_value) are required')
        print('update_record - updates record with specified id in table\n'
              '\tProduct args (table_name, id_product, title, price, category, id_catalog, id_order)\n'
              '\tOrder args (table_name, id_order, customer_name, id_shop, date)\n'
              '\tCatalog args (table_name, id_catalog, name, id_shop, pid_catalog)\n'
              '\tShop args (table_name, id_shop, address, name)')
        print('insert_record - inserts record into specified table \n'
              '\tProduct args (table_name, id_product, title, price, category, id_catalog, id_order)\n'
              '\tOrder args (table_name, id_order, customer_name, id_shop, date)\n'
              '\tCatalog args (table_name, id_catalog, name, id_shop, pid_catalog)\n'
              '\tShop args (table_name, id_shop, address, name)')
        print('generate_randomly - generates n random records in table\n'
              '\targuments (table_name, n) are required')
        print('search_records - search for records in two or more tables using one or more keys \n'
              '\targuments (table1_name, table2_name, table1_key, table2_key) are required, \n'
              '\tif you want to perform search in more tables: \n'
              '\t(table1_name, table2_name, table3_name, table1_key, table2_key, table3_key, table13_key) \n'
              '\t(table1_name, table2_name, table3_name, table4_name, table1_key, table2_key, table3_key, table13_key, '
              'table4_key, table24_key)')


    def get_search_num(self):
        return input('specify the number of tables you`d like to search in: ')

    def invalid_search_num(self):
        print('should be number from 2 to 4')

    def argument_error(self):
        print('no required arguments specified')

    def wrong_table(self):
        print('wrong table name')

    def no_command(self):
        print('no command name specified, type help to see possible commands')

    def wrong_command(self):
        print('unknown command name, type help to see possible commands')