from psycopg2 import Error
import model
import view
import datetime


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

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            count = 0
            k_val = self.v.valid.check_pk(value)
            if t_name == 'session' and k_val:
                count = self.m.find_pk_session(k_val)
            elif t_name == 'movie' and k_val:
                count = self.m.find_pk_movie(k_val)
            elif t_name == 'hall' and k_val:
                count = self.m.find_pk_hall(k_val)
            elif t_name == 'cinema' and k_val:
                count = self.m.find_pk_cinema(k_val)
            elif t_name == 'seat' and k_val:
                count = self.m.find_pk_seat(k_val)
            if count:
                if t_name == 'movie':
                    count_s = self.m.find_fk_session(k_val, t_name)
                    if count_s:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_movie(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'cinema':
                    count_h = self.m.find_fk_hall(k_val)
                    count_m = self.m.find_fk_movie(k_val)
                    if count_h or count_m:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_cinema(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'hall':
                    count_seat = self.m.find_fk_seat(k_val)
                    count_session = self.m.find_fk_session(k_val, t_name)
                    if count_seat or count_session:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_hall(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'seat':
                    try:
                        self.m.delete_data_seat(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_session(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_session(self, key: str, movie_id: str, number: str, time: str, cost: str):
        if self.v.valid.check_possible_keys('session', 'session_id', key):
            count_s = self.m.find_pk_session(int(key))
            s_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('movie', 'movie_id', movie_id):
            count_m = self.m.find_pk_movie(int(movie_id))
            m_val = self.v.valid.check_pk(movie_id)
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find_pk_hall(int(number))
            h_val = self.v.valid.check_pk(number)

        if count_s and count_m and count_h and \
                m_val and h_val and s_val and self.v.valid.check_possible_keys('session', 'cost', cost):
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
            count_c = self.m.find_pk_cinema(int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id)
        if self.v.valid.check_possible_keys('movie', 'movie_id', key):
            count_m = self.m.find_pk_movie(int(key))
            m_val = self.v.valid.check_pk(key)

        if count_m and count_c and c_val and m_val and self.v.valid.check_possible_keys('movie', 'rating', rating):
            try:
                self.m.update_data_movie(m_val, c_val, title, float(rating))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_hall(self, key: str, cinema_id: str, screen_size: str, number_of_seats: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find_pk_cinema(int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id)
        if self.v.valid.check_possible_keys('hall', 'number', key):
            count_h = self.m.find_pk_hall(int(key))
            h_val = self.v.valid.check_pk(key)

        if count_h and count_c and c_val and h_val:
            try:
                self.m.update_data_hall(h_val, c_val, screen_size, int(number_of_seats))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_cinema(self, key: str, name: str, adress: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            count_c = self.m.find_pk_cinema(int(key))
            c_val = self.v.valid.check_pk(key)

        if c_val and count_c:
            try:
                self.m.update_data_cinema(c_val, name, adress)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_seat(self, key: str, number: str, row: str, seat_number: str, is_occupied: str):
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find_pk_hall(int(number))
            h_val = self.v.valid.check_pk(number)
        if self.v.valid.check_possible_keys('seat', 'seat_id', key):
            count_s = self.m.find_pk_seat(int(key))
            s_val = self.v.valid.check_pk(key)

        if count_s and count_h and s_val and h_val :
            try:
                self.m.update_data_seat(s_val, h_val, int(row), int(seat_number), int(is_occupied))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_session(self, key: str, movie_id: str, number: str, time: str, cost: str):
        if self.v.valid.check_possible_keys('session', 'session_id', key):
            count_s = self.m.find_pk_session(int(key))
        if self.v.valid.check_possible_keys('movie', 'movie_id', movie_id):
            count_m = self.m.find_pk_movie(int(movie_id))
            m_val = self.v.valid.check_pk(movie_id)
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find_pk_hall(int(number))
            h_val = self.v.valid.check_pk(number)

        if (not count_s) and count_h and count_m and m_val and h_val \
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
            count_c = self.m.find_pk_cinema(int(cinema_id))
            c_val = self.v.valid.check_pk(int(cinema_id))
        if self.v.valid.check_possible_keys('movie', 'movie_id', key):
            count_m = self.m.find_pk_movie(int(key))

        if (not count_m) and count_c and c_val and self.v.valid.check_possible_keys('movie', 'movie_id', key) \
                and self.v.valid.check_possible_keys('movie', 'rating', rating):
            try:
                self.m.insert_data_movie(int(key), c_val, title, float(rating))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_hall(self, key: str, cinema_id: str, screen_size: str, number_of_seats: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', cinema_id):
            count_c = self.m.find_pk_cinema(int(cinema_id))
            c_val = self.v.valid.check_pk(cinema_id)
        if self.v.valid.check_possible_keys('hall', 'number', key):
            count_h = self.m.find_pk_hall(int(key))

        if (not count_h) and count_c and c_val \
                and self.v.valid.check_possible_keys('hall', 'number', key):
            try:
                self.m.insert_data_hall(int(key), c_val, screen_size, int(number_of_seats))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_cinema(self, key: str, name: str, adress: str):
        if self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            count_c = self.m.find_pk_cinema(int(key))

        if (not count_c) and self.v.valid.check_possible_keys('cinema', 'cinema_id', key):
            try:
                self.m.insert_data_cinema(int(key), name, adress)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_seat(self, key: str, number: str, row: str, seat_number: str, is_occupied: str):
        if self.v.valid.check_possible_keys('hall', 'number', number):
            count_h = self.m.find_pk_hall(int(number))
            h_val = self.v.valid.check_pk(number)
        if self.v.valid.check_possible_keys('seat', 'seat_id', key):
            count_s = self.m.find_pk_seat(int(key))

        if (not count_s) and h_val and count_h \
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

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_all(self):
        result = self.m.search_data_all_tables()
        self.v.print_search(result)
