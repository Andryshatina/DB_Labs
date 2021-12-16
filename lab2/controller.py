from psycopg2 import Error
import model
import view
import datetime
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'cinema':
                self.v.print_cinema(self.m.print_cinema())
            elif t_name == 'hall':
                self.v.print_hall(self.m.print_hall())
            elif t_name == 'movie':
                self.v.print_movie(self.m.print_movie())
            elif t_name == 'seat':
                self.v.print_seat(self.m.print_seat())
            elif t_name == 'session':
                self.v.print_session(self.m.print_session())

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        k_name = self.v.valid.check_pk_name(table_name, key_name)
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'movie':
                    count_s = self.m.find('session', k_name, value)[0]
                    if count_s:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'cinema':
                    count_h = self.m.find('hall', k_name, value)[0]
                    count_m = self.m.find('movie', k_name, value)[0]
                    if count_h or count_m:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'hall':
                    count_seat = self.m.find('seat', k_name, value)[0]
                    count_session = self.m.find('session', k_name, value)[0]
                    if count_seat or count_session:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_session(self, key: str, movie_id: str, number: str, time: str, cost: str):
        if self.v.valid.check_possible_keys('session', 'session_id', key):
            count_s = self.m.find('session', 'session_id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)
        if self.v.valid.check_possible_keys('movie', 'movie_id', movie_id):
            count_m = self.m.find('movie', 'movie_id', int(movie_id))
            m_val = self.v.valid.check_pk(movie_id, count_m)
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find('hall', 'number', int(number))
            h_val = self.v.valid.check_pk(number, count_h)

        if m_val and h_val and s_val and self.v.valid.check_possible_keys('session', 'cost', cost):
            try:
                arr = [int(x) for x in time.split(sep='.')]
                self.m.update_data_session(s_val, m_val, h_val,
                                           datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]),
                                           float(cost))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_movie(self, key: str, cinema_id: str, title: str, rating: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find('cinema', 'cinema_id', int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id, count_c)
        if self.v.valid.check_possible_keys('movie', 'movie_id', key):
            count_m = self.m.find('movie', 'movie_id', int(key))
            m_val = self.v.valid.check_pk(key, count_m)

        if c_val and m_val and self.v.valid.check_possible_keys('movie', 'rating', rating):
            try:
                self.m.update_data_movie(m_val, c_val, title, float(rating))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_hall(self, key: str, cinema_id: str, screen_size: str, number_of_seats: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find('cinema', 'cinema_id', int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id, count_c)
        if self.v.valid.check_possible_keys('hall', 'number', key):
            count_h = self.m.find('hall', 'number', int(key))
            h_val = self.v.valid.check_pk(key, count_h)

        if c_val and h_val:
            try:
                self.m.update_data_hall(h_val, c_val, screen_size, int(number_of_seats))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_cinema(self, key: str, name: str, adress: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            count_c = self.m.find('cinema', 'cinema_id', int(key))
            c_val = self.v.valid.check_pk(key, count_c)

        if c_val:
            try:
                self.m.update_data_cinema(c_val, name, adress)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_seat(self, key: str, number: str, row: str, seat_number: str, is_occupied: str):
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find('hall', 'number', int(number))
            h_val = self.v.valid.check_pk(number, count_h)
        if self.v.valid.check_possible_keys('seat', 'seat_id', key):
            count_s = self.m.find('seat', 'seat_id', int(key))
            s_val = self.v.valid.check_pk(key, count_s)

        if s_val and h_val :
            try:
                self.m.update_data_seat(s_val, h_val, int(row), int(seat_number), int(is_occupied))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_session(self, key: str, movie_id: str, number: str, time: str, cost: str):
        if self.v.valid.check_possible_keys('session', 'session_id', key):
            count_s = self.m.find('session', 'session_id', int(key))[0]
        if self.v.valid.check_possible_keys('movie', 'movie_id', movie_id):
            count_m = self.m.find('movie', 'movie_id', int(movie_id))
            m_val = self.v.valid.check_pk(movie_id, count_m)
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find('hall', 'number', int(number))
            h_val = self.v.valid.check_pk(number, count_h)

        if (not count_s or count_s == (0,)) and m_val and h_val \
                and self.v.valid.check_possible_keys('session', 'session_id', key) \
                and self.v.valid.check_possible_keys('session', 'cost', cost):
            try:
                arr = [int(x) for x in time.split(sep='.')]
                self.m.insert_data_session(int(key), m_val, h_val,
                                           datetime.datetime(arr[0], arr[1], arr[2],
                                                           arr[3], arr[4], arr[5]),
                                           float(cost))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_movie(self, key: str, cinema_id: str, title: str, rating: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find('cinema', 'cinema_id', int(cinema_id))
            c_val = self.v.valid.check_pk(int(cinema_id), count_c)
        if self.v.valid.check_possible_keys('movie', 'movie_id', key):
            count_m = self.m.find('movie', 'movie_id', int(key))[0]

        if (not count_m or count_m == (0,)) and c_val and self.v.valid.check_possible_keys('movie', 'movie_id', key) \
                and self.v.valid.check_possible_keys('movie', 'rating', rating):
            try:
                self.m.insert_data_movie(int(key), c_val, title, float(rating))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_hall(self, key: str, cinema_id: str, screen_size: str, number_of_seats: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find('cinema', 'cinema_id', int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id, count_c)
        if self.v.valid.check_possible_keys('hall', 'number', key):
            count_h = self.m.find('hall', 'number', int(key))[0]

        if (not count_h or count_h == (0,)) and c_val \
                and self.v.valid.check_possible_keys('hall', 'number', key):
            try:
                self.m.insert_data_hall(int(key), c_val, screen_size, int(number_of_seats))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_cinema(self, key: str, name: str, adress: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            count_c = self.m.find('cinema', 'cinema_id', int(key))[0]

        if (not count_c or count_c == (0,)) and self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            try:
                self.m.insert_data_cinema(int(key), name, adress)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_seat(self, key: str, number: str, row: str, seat_number: str, is_occupied: str):
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find('hall', 'number', int(number))
            h_val = self.v.valid.check_pk(number, count_h)
        if self.v.valid.check_possible_keys('seat', 'seat_id', key):
            count_s = self.m.find('seat', 'seat_id', int(key))[0]

        if (not count_s or count_s == (0,)) and h_val \
                and self.v.valid.check_possible_keys('seat', 'seat_id', key):
            try:
                self.m.insert_data_seat(int(key), h_val, int(row), int(seat_number), int(is_occupied))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'session':
                self.m.session_data_n_rand(n)
            elif t_name == 'movie':
                self.m.movie_data_n_rand(n)
            elif t_name == 'hall':
                self.m.hall_data_n_rand(n)
            elif t_name == 'cinema':
                self.m.cinema_data_n_rand(n)
            elif t_name == 'seat':
                self.m.seat_data_n_rand(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)

            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)