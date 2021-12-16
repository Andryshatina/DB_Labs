import datetime
import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                database="lab1",
                user='postgres',
                password="postgres",
                host='localhost',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_cinema(self) -> None:
        return self.get(f"SELECT * FROM public.\"cinema\"")

    def print_hall(self) -> None:
        return self.get(f"SELECT * FROM public.\"hall\"")

    def print_movie(self) -> None:
        return self.get(f"SELECT * FROM public.\"movie\"")

    def print_seat(self) -> None:
        return self.get(f"SELECT * FROM public.\"seat\"")

    def print_session(self) -> None:
        return self.get(f"SELECT * FROM public.\"session\"")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_session(self, key_value: int, movie_id: int, number: int, time: datetime.datetime,
                            cost: float) -> None:
        self.request(f"UPDATE public.\"session\" SET movie_id={movie_id}, number={number}, time=\'{time}\', "
                     f"cost={cost} WHERE session_id={key_value};")

    def update_data_movie(self, key_value: int, cinema_id: int, title: str, rating: float) -> None:
        self.request(f"UPDATE public.\"movie\" SET cinema_id={cinema_id}, title=\'{title}\', "
                     f"rating={rating} WHERE movie_id={key_value};")

    def update_data_hall(self, key_value: int, cinema_id: int, screen_size: str, number_of_seats: int) -> None:
        self.request(f"UPDATE public.\"hall\" SET cinema_id={cinema_id}, screen_size=\'{screen_size}\', "
                     f"number_of_seats={number_of_seats} WHERE number={key_value};")

    def update_data_seat(self, key_value: int, number: int, row: int, seat_number: int, is_occupied: int) -> None:
        if(is_occupied == 1):
            is_occupied1 = 'true'
        else:
            is_occupied1 = 'false'
        self.request(f"UPDATE public.\"seat\" SET number={number}, row={row}, seat_number={seat_number}, "
                     f"is_occupied={is_occupied1} WHERE seat_id={key_value};")

    def update_data_cinema(self, key_value: int, name: str, adress: str) -> None:
        self.request(f"UPDATE public.\"cinema\" SET name=\'{name}\', "
                     f"adress=\'{adress}\' WHERE cinema_id={key_value};")

    def insert_data_session(self, session_id: int, movie_id: int, number: int, time: datetime.datetime,
                            cost: float) -> None:
        self.request(f"insert into public.\"session\" (session_id, movie_id, number, time, cost) "
                     f"VALUES ({session_id}, {movie_id}, {number}, \'{time}\', {cost});")

    def insert_data_movie(self, movie_id: int, cinema_id: int, title: str, rating: float) -> None:
        self.request(f"insert into public.\"movie\" (movie_id, cinema_id, title, rating) "
                     f"VALUES ({movie_id}, {cinema_id}, \'{title}\', {rating});")

    def insert_data_hall(self, number: int, cinema_id: int, screen_size: str, number_of_seats: int) -> None:
        self.request(f"insert into public.\"hall\" (number, cinema_id, screen_size, number_of_seats) "
                     f"VALUES ({number}, {cinema_id}, \'{screen_size}\', {number_of_seats});")

    def insert_data_seat(self, seat_id: int, number: int, row: int, seat_number: int, is_occupied: int) -> None:
        if is_occupied == 1:
            is_occupied1 = 'true'
        else:
            is_occupied1 = 'false'
        self.request(f"insert into public.\"seat\" (seat_id, number, row, seat_number, is_occupied) "
                     f"VALUES ({seat_id}, {number}, {row}, {seat_number}, \'{is_occupied1}\');")

    def insert_data_cinema(self, cinema_id: int, name: str, adress: str) -> None:
        self.request(f"insert into public.\"cinema\" (cinema_id, name, adress) "
                     f"VALUES ({cinema_id}, \'{name}\', \'{adress}\');")

    def session_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"session\""
                         "select (SELECT MAX(session_id)+1 FROM public.\"session\"), "
                         "(SELECT movie_id FROM public.\"movie\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(movie_id) FROM public.\"movie\")-1)))), "
                         "(SELECT number FROM public.\"hall\" LIMIT 1 OFFSET (round(random() * "
                         "((SELECT COUNT(number) FROM public.\"hall\")-1)))), "
                         "(select timestamp '2018-01-10 10:00:00' + random() * "
                         "(timestamp '2021-01-20 20:00:00' - timestamp '2018-01-10 10:00:00')), "
                         "FLOOR(RANDOM()*(1000-20)+20);")

    def movie_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"movie\" select (SELECT (MAX(movie_id)+1) FROM public.\"movie\"), "
                         "(SELECT cinema_id FROM public.\"cinema\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(cinema_id) FROM public.\"cinema\")-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "FLOOR(RANDOM()*(11-1)+1);")

    def hall_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"hall\" select (SELECT MAX(number)+1 FROM public.\"hall\"), "
                         "(SELECT cinema_id FROM public.\"cinema\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(cinema_id) FROM public.\"cinema\")-1)))), "
                         "FLOOR(RANDOM()*(300-80)+80), "
                         "FLOOR(RANDOM()*(350-20)+20);")

    def cinema_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"cinema\" select (SELECT MAX(cinema_id)+1 FROM public.\"cinema\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def seat_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"seat\" select (SELECT MAX(seat_id)+1 FROM public.\"seat\"), "
                         "(SELECT number FROM public.\"hall\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(number) FROM public.\"hall\")-1)))), "
                         "FLOOR(RANDOM()*(51-1)+1), "
                         "FLOOR(RANDOM()*(350-1)+1), "
                         "(round(random())::int)::boolean;")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\""
                        f"where {search}")