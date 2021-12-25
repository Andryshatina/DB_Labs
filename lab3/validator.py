import datetime


class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['cinema', 'hall', 'seat', 'session', 'movie']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'cinema' and key_name == 'cinema_id' \
                or table_name == 'hall' and key_name == 'number' \
                or table_name == 'movie' and key_name == 'movie_id' \
                or table_name == 'seat' and key_name == 'seat_id' \
                or table_name == 'session' and key_name == 'session_id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val):
        try:
            value = int(val)
            return value
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'session' and key in ['session_id', 'movie_id', 'number', 'time', 'cost']:
            return True
        elif table_name == 'movie' and key in ['movie_id', 'cinema_id', 'title', 'rating']:
            return True
        elif table_name == 'hall' and key in ['number', 'screen_size', 'number_of_seats']:
            return True
        elif table_name == 'cinema' and key in ['cinema_id', 'name', 'adress']:
            return True
        elif table_name == 'seat' and key in ['seat_id', 'number', 'row', 'seat_number', 'is_occupied']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'session':
            if key in ['session_id', 'movie_id', 'number']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'time':
                try:
                    arr = [int(x) for x in val.split(sep='.')]
                    datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
                except TypeError:
                    self.er_flag = True
                    self.error = f'{val} is not correct date value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'cost':
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct cost value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for session table'
                print(self.error)
                return False
        elif table_name == 'movie':
            if key in ['movie_id', 'cinema_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'title':
                return True
            elif key == 'rating':
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct cost value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for movie table'
                print(self.error)
                return False
        elif table_name == 'hall':
            if key in ['number', 'cinema_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'screen_size':
                return True
            elif key == 'number_of_seats':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct number of seats value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for hall table'
                print(self.error)
                return False
        elif table_name == 'seat':
            if key in ['seat_id', 'number']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'row':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct number of seats value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'seat_number':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct number of seats value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for hall table'
                print(self.error)
                return False
        elif table_name == 'cinema':
            if key == 'cinema_id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name', 'adress']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for cinema table'
                print(self.error)
                return False
