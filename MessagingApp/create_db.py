from psycopg2 import connect
import argparse


DEFAULT_HOST = 'localhost'
DEFAULT_USER = 'postgres'
DEFAULT_PWD = 'coderslab'


def create_db():
    """

    :return: True if succesfully added
    """
    # parse arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u")
    arg_parser.add_argument("--host")
    arg_parser.add_argument("--pwd")

    args = arg_parser.parse_args()

    user = args.u if args.u else DEFAULT_USER
    host = args.host if args.host else DEFAULT_HOST
    pwd = args.pwd if args.pwd else DEFAULT_PWD

    # create a connection
    try:
        connection = connect(user=user, host=host, password=pwd)
        connection.autocommit = True
        cur = connection.cursor()
        # attempt to create a database
        cur.execute("CREATE DATABASE maly_test_db")
    except Exception as e:
        print('Error', e.pgcode, ":", e)
        cur.close()
        connection.close()
        if e.pgcode == '42P04':
            return True
        else:
            return False
    else:
        cur.close()
        connection.close()
        return True


if __name__ == "__main__":
    create_db()
