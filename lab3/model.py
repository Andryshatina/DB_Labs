import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Cinema(Orders):
    __tablename__ = 'cinema'
    cinema_id = Column(Integer, primary_key=True)
    name = Column(String)
    adress = Column(String)
    halls = relationship("Hall")
    movies = relationship("Movie")

    def __init__(self, cinema_id, name, adress):
        self.cinema_id = cinema_id
        self.name = name
        self.adress = adress

    def __repr__(self):
        return "{:>10}{:>15}{:>35}" \
            .format(self.cinema_id, self.name, self.adress)


class Hall(Orders):
    __tablename__ = 'hall'
    number = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinema.cinema_id'))
    screen_size = Column(String)
    number_of_seats = Column(Integer)
    sessions = relationship("Sessions")
    seats = relationship("Seat")

    def __init__(self, number, cinema_id, screen_size, number_of_seats):
        self.number = number
        self.cinema_id = cinema_id
        self.screen_size = screen_size
        self.number_of_seats = number_of_seats

    def __repr__(self):
        return "{:>10}{:>10}{:>15}{:>10}" \
            .format(self.number, self.cinema_id, self.screen_size, self.number_of_seats)


class Movie(Orders):
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinema.cinema_id'))
    title = Column(String)
    rating = Column(Integer)
    sessions = relationship("Sessions")

    def __init__(self, movie_id, cinema_id, title, rating):
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.title = title
        self.rating = rating

    def __repr__(self):
        return "{:>10}{:>10}{:>25}{:>15}" \
            .format(self.movie_id, self.cinema_id, self.title, self.rating)


class Sessions(Orders):
    __tablename__ = 'session'
    session_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.movie_id'))
    number = Column(Integer, ForeignKey('hall.number'))
    time = Column(Date)
    cost = Column(Float)


    def __init__(self, session_id, movie_id, number, time, cost):
        self.session_id = session_id
        self.movie_id = movie_id
        self.number = number
        self.time = time
        self.cost = cost

    def __repr__(self):
        return "{:>10}{:>30}{:>10}\t\t{}{:>10}" \
            .format(self.session_id, self.movie_id, self.number, self.time, self.cost)


class Seat(Orders):
    __tablename__ = 'seat'
    seat_id = Column(Integer, primary_key=True)
    number = Column(Integer, ForeignKey('hall.number'))
    row = Column(Integer)
    seat_number = Column(Integer)
    is_occupied = Column(Integer)

    def __init__(self, seat_id, number, row, seat_number, is_occupied):
        self.seat_id = seat_id
        self.number = number
        self.row = row
        self.seat_number = seat_number
        self.is_occupied = is_occupied

    def __repr__(self):
        return "{:>10}{:>10}{:>10}{:>10}{:>10}" \
            .format(self.seat_id, self.number, self.row, self.seat_number, self.is_occupied)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_session(self, key_value: int):
        return self.session.query(Sessions).filter_by(session_id=key_value).first()

    def find_fk_session(self, key_value: int, table_name: str):
        if table_name == "movie":
            return self.session.query(Sessions).filter_by(movie_id=key_value).first()
        elif table_name == "hall":
            return self.session.query(Sessions).filter_by(number=key_value).first()

    def find_pk_movie(self, key_value: int):
        return self.session.query(Movie).filter_by(movie_id=key_value).first()

    def find_fk_movie(self, key_value: int):
        return self.session.query(Movie).filter_by(cinema_id=key_value).first()

    def find_pk_hall(self, key_value: int):
        return self.session.query(Hall).filter_by(number=key_value).first()

    def find_fk_hall(self, key_value: int):
        return self.session.query(Hall).filter_by(cinema_id=key_value).first()

    def find_pk_seat(self, key_value: int):
        return self.session.query(Seat).filter_by(seat_id=key_value).first()

    def find_fk_seat(self, key_value: int):
        return self.session.query(Seat).filter_by(number=key_value).first()

    def find_pk_cinema(self, key_value: int):
        return self.session.query(Cinema).filter_by(cinema_id=key_value).first()

    def print_session(self):
        return self.session.query(Sessions).order_by(Sessions.session_id.asc()).all()

    def print_movie(self):
        return self.session.query(Movie).order_by(Movie.movie_id.asc()).all()

    def print_hall(self):
        return self.session.query(Hall).order_by(Hall.number.asc()).all()

    def print_cinema(self):
        return self.session.query(Cinema).order_by(Cinema.cinema_id.asc()).all()

    def print_seat(self):
        return self.session.query(Seat).order_by(Seat.seat_id.asc()).all()

    def delete_data_session(self, session_id) -> None:
        self.session.query(Sessions).filter_by(session_id=session_id).delete()
        self.session.commit()

    def delete_data_movie(self, movie_id) -> None:
        self.session.query(Movie).filter_by(movie_id=movie_id).delete()
        self.session.commit()

    def delete_data_hall(self, number) -> None:
        self.session.query(Hall).filter_by(number=number).delete()
        self.session.commit()

    def delete_data_cinema(self, cinema_id) -> None:
        self.session.query(Cinema).filter_by(cinema_id=cinema_id).delete()
        self.session.commit()

    def delete_data_seat(self, seat_id) -> None:
        self.session.query(Seat).filter_by(seat_id=seat_id).delete()
        self.session.commit()

    def update_data_session(self, session_id: int, movie_id: int, number: int, time: datetime.datetime, cost: float) -> None:
        self.session.query(Sessions).filter_by(session_id=session_id) \
            .update({Sessions.movie_id: movie_id, Sessions.number: number, Sessions.time: time,
                     Sessions.cost: cost})
        self.session.commit()

    def update_data_movie(self, movie_id: int, cinema_id: int, title: str, rating: int) -> None:
        self.session.query(Movie).filter_by(movie_id=movie_id) \
            .update({Movie.cinema_id: cinema_id, Movie.title: title, Movie.rating: rating})
        self.session.commit()

    def update_data_hall(self, number: int, cinema_id: int, screen_size: str, number_of_seats: int) -> None:
        self.session.query(Hall).filter_by(number=number) \
            .update({Hall.cinema_id: cinema_id, Hall.screen_size: screen_size, Hall.number_of_seats: number_of_seats})
        self.session.commit()

    def update_data_cinema(self, cinema_id: int, name: str, adress: str) -> None:
        self.session.query(Cinema).filter_by(cinema_id=cinema_id) \
            .update({Cinema.name: name, Cinema.adress: adress})
        self.session.commit()

    def update_data_seat(self, seat_id: int, number: int, row: int, seat_number: int, is_occupied: int) -> None:
        if (is_occupied == 1):
            is_occupied1 = 'true'
        else:
            is_occupied1 = 'false'
        self.session.query(Seat).filter_by(seat_id=seat_id) \
            .update({Seat.number: number, Seat.row: row, Seat.seat_number: seat_number, Seat.is_occupied: is_occupied1})
        self.session.commit()

    def insert_data_session(self, session_id: int, movie_id: int, number: int, time: datetime.datetime, cost: float) -> None:
        session1 = Sessions(session_id=session_id, movie_id=movie_id, number=number, time=time, cost=cost)
        self.session.add(session1)
        self.session.commit()

    def insert_data_movie(self, movie_id: int, cinema_id: int, title: str, rating: float) -> None:
        movie = Movie(movie_id=movie_id, cinema_id=cinema_id, title=title, rating=rating)
        self.session.add(movie)
        self.session.commit()

    def insert_data_hall(self, number: int, cinema_id: int, screen_size: str, number_of_seats: int) -> None:
        hall = Hall(number=number, cinema_id=cinema_id, screen_size=screen_size, number_of_seats=number_of_seats)
        self.session.add(hall)
        self.session.commit()

    def insert_data_cinema(self, cinema_id: int, name: str, adress: str) -> None:
        cinema = Cinema(cinema_id=cinema_id, name=name, adress=adress)
        self.session.add(cinema)
        self.session.commit()

    def insert_data_seat(self, seat_id: int, number: int, row: int, seat_number: int, is_occupied: int) -> None:
        if (is_occupied == 1):
            is_occupied1 = 'true'
        else:
            is_occupied1 = 'false'
        seat = Seat(seat_id=seat_id, number=number, row=row, seat_number=seat_number, is_occupied=is_occupied1)
        self.session.add(seat)
        self.session.commit()

    def session_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"session\""
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
            self.connection.execute(
                "insert into public.\"movie\" select (SELECT (MAX(movie_id)+1) FROM public.\"movie\"), "
                 "(SELECT cinema_id FROM public.\"cinema\" LIMIT 1 OFFSET "
                 "(round(random() *((SELECT COUNT(cinema_id) FROM public.\"cinema\")-1)))), "
                 "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                 "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                 "FLOOR(RANDOM()*(11-1)+1);")

    def hall_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"hall\" select (SELECT MAX(number)+1 FROM public.\"hall\"), "
                 "(SELECT cinema_id FROM public.\"cinema\" LIMIT 1 OFFSET "
                 "(round(random() *((SELECT COUNT(cinema_id) FROM public.\"cinema\")-1)))), "
                 "FLOOR(RANDOM()*(300-80)+80), "
                 "FLOOR(RANDOM()*(350-20)+20);")

    def cinema_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"cinema\" select (SELECT MAX(cinema_id)+1 FROM public.\"cinema\"), "
                 "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                 "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                 "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                 "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def seat_data_n_rand(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"seat\" select (SELECT MAX(seat_id)+1 FROM public.\"seat\"), "
                 "(SELECT number FROM public.\"hall\" LIMIT 1 OFFSET "
                 "(round(random() *((SELECT COUNT(number) FROM public.\"hall\")-1)))), "
                 "FLOOR(RANDOM()*(51-1)+1), "
                 "FLOOR(RANDOM()*(350-1)+1), "
                 "(round(random())::int)::boolean;")

    def search_data_two_tables(self):
        return self.session.query(Movie) \
            .join(Sessions) \
            .filter(and_(
                Sessions.session_id.between(0, 10),
                Movie.cinema_id.between(0, 6),
                Movie.rating.between(0, 10)
            )) \
            .all()

    def search_data_three_tables(self):
        start_date = datetime.datetime(2019, 11, 12)
        end_date = datetime.datetime(2020, 11, 1)
        return self.session.query(Sessions) \
            .join(Hall).join(Movie) \
            .filter(and_(
                Sessions.time.between(start_date, end_date),
                Movie.rating.between(0, 9),
                Hall.cinema_id.between(0, 8)
            )) \
            .all()