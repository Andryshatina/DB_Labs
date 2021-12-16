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
            args = {"name": sys.argv[2], "key": sys.argv[3], "val": sys.argv[4]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["key"], args["val"])

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
        if len(sys.argv) in [6, 9]:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num > 0:
                    if len(sys.argv) == 6:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3],
                                "key1_name": sys.argv[4], "key2_name": sys.argv[5]}
                        c.search_two(args["table1_name"], args["table2_name"], args["key1_name"], args["key2_name"],
                                     c.v.proceed_search(search_num))
                    elif len(sys.argv) == 9:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3], "table3_name": sys.argv[4],
                                "key1_name": sys.argv[5], "key2_name": sys.argv[6], "key3_name": sys.argv[7],
                                "key13_name": sys.argv[8]}
                        c.search_three(args["table1_name"], args["table2_name"], args["table3_name"],
                                       args["key1_name"], args["key2_name"], args["key3_name"], args["key13_name"],
                                       c.v.proceed_search(search_num))
                else:
                    c.v.invalid_search_num()
        else:
            c.v.argument_error()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
