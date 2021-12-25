import controller as con
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "val": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["val"])

    elif command == 'insert_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'session':
                args["movie_id"], args["number"], args["time"], args["cost"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["name"] == 'movie':
                args["cinema_id"], args["title"], args["rating"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'hall':
                args["cinema_id"], args["screen_size"], args["number_of_seats"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'cinema':
                args["name1"], args["adress"] = \
                    sys.argv[4], sys.argv[5]
            elif args["name"] == 'seat':
                args["number"], args["row"], args["seat_number"], args["is_occupied"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'session':
                c.insert_session(args["key"], args["movie_id"], args["number"], args["time"], args["cost"])
            elif args["name"] == 'movie':
                c.insert_movie(args["key"], args["cinema_id"], args["title"], args["rating"])
            elif args["name"] == 'hall':
                c.insert_hall(args["key"], args["cinema_id"], args["screen_size"], args["number_of_seats"])
            elif args["name"] == 'cinema':
                c.insert_cinema(args["key"], args["name1"], args["adress"])
            elif args["name"] == 'seat':
                c.insert_seat(args["key"], args["number"], args["row"], args["seat_number"], args["is_occupied"])

    elif command == 'update_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'session':
                args["movie_id"], args["number"], args["time"], args["cost"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["name"] == 'movie':
                args["cinema_id"], args["title"], args["rating"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'hall':
                args["cinema_id"], args["screen_size"], args["number_of_seats"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'seat':
                args["number"], args["row"], args["seat_number"], args["is_occupied"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
            elif args["name"] == 'cinema':
                args["name1"], args["adress"] = \
                    sys.argv[4], sys.argv[5]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'session':
                c.update_session(args["key"], args["movie_id"], args["number"], args["time"], args["cost"])
            elif args["name"] == 'movie':
                c.update_movie(args["key"], args["cinema_id"], args["title"], args["rating"])
            elif args["name"] == 'hall':
                c.update_hall(args["key"], args["cinema_id"], args["screen_size"], args["number_of_seats"])
            elif args["name"] == 'seat':
                c.update_seat(args["key"], args["number"], args["row"], args["seat_number"], args["is_occupied"])
            elif args["name"] == 'cinema':
                c.update_cinema(args["key"], args["name1"], args["adress"])

    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])

    elif command == 'search_records':
        while True:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3]:
                    break
                else:
                    c.v.invalid_search_num()
        if search_num == 2:
            c.search_two()
        elif search_num == 3:
            c.search_three()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
