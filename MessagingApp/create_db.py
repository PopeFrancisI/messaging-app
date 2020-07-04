from psycopg2 import connect
import argparse


DEFAULT_HOST = 'localhost'
DEFAULT_USER = 'postgres'
DEFAULT_PWD = 'coderslab'
DEFAULT_DBNAME = "messaging_app_db"


def create_db():
    """
    Logs as specified user (console args) and creates a database.

    :return: True if succesfully added or database already present, false otherwise
    """
    # parse arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u")
    arg_parser.add_argument("--host")
    arg_parser.add_argument("-p")
    arg_parser.add_argument("--dbname", help="New database name.")

    args = arg_parser.parse_args()

    user = args.u if args.u else DEFAULT_USER
    host = args.host if args.host else DEFAULT_HOST
    pwd = args.p if args.p else DEFAULT_PWD
    dbname = args.dbname if args.dbname else DEFAULT_DBNAME

    try:
        # create a connection
        connection = connect(user=user, host=host, password=pwd)
        connection.autocommit = True
        cur = connection.cursor()
        # attempt to create a database
        sql = f"CREATE DATABASE {dbname}"
        cur.execute(sql)
    except Exception as e:
        cur.close()
        connection.close()
        if e.pgcode == '42P04':
            print(f'Database {dbname} is already present.')
            return True
        else:
            print('Error', e.pgcode, ":", e)
            return False
    else:
        cur.close()
        connection.close()
        print(f'Database {dbname} succesfully created!')
        return True


if __name__ == "__main__":
    create_db()
