from psycopg2 import connect
import argparse


DEFAULT_HOST = 'localhost'
DEFAULT_USER = 'postgres'
DEFAULT_PWD = 'coderslab'
DEFAULT_DBNAME = 'postgres'
DEFAULT_NEW_DBNAME = "messaging_app_db"


def parse_args():
    """
    Parses console arguments.

    :return: returns ArgParser's Namespace object
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u")
    arg_parser.add_argument("--host")
    arg_parser.add_argument("-p")
    arg_parser.add_argument("--dbname", help="New database name.")

    args = arg_parser.parse_args()

    return args


def create_db():
    """
    Logs in as specified user (console args) and creates a database and all required tables.

    :return: True if succesfully added or database already present, false otherwise
    """
    # parse arguments
    args = parse_args()

    user = args.u if args.u else DEFAULT_USER
    host = args.host if args.host else DEFAULT_HOST
    pwd = args.p if args.p else DEFAULT_PWD
    dbname = DEFAULT_DBNAME
    new_dbname = args.dbname if args.dbname else DEFAULT_NEW_DBNAME

    try:
        # create a connection to create the database itself
        print(f'Connecting to {dbname}...')
        connection = connect(user=user, host=host, password=pwd)
        connection.autocommit = True
        cur = connection.cursor()
        # attempt to create a database
        sql = f"CREATE DATABASE {new_dbname}"
        cur.execute(sql)
    except Exception as e:
        if e.pgcode == '42P04':
            print(f'Database {new_dbname} already exists.')
        else:
            print('Error', e.pgcode, ":", e)
            cur.close()
            connection.close()
            return False

    cur.close()
    connection.close()

    try:
        # connect to newly created database
        print(f'Connecting to {new_dbname}...')
        connection = connect(user=user, host=host, password=pwd, dbname=new_dbname)
        connection.autocommit = True
        cur = connection.cursor()
    except Exception as e:
        print('Error', e.pgcode, ":", e)
        cur.close()
        connection.close()
        return False

    # create Users table
    try:
        print("Creating Users table.")
        sql = """
        CREATE TABLE Users (
            id SERIAL PRIMARY KEY ,
            username VARCHAR(255),
            hashed_password VARCHAR(80)
        )
        """
        cur.execute(sql)
    except Exception as e:
        if e.pgcode == '42P07':
            print(f'Table Users already exists.')
        else:
            print('Error', e.pgcode, ":", e)
            cur.close()
            connection.close()
            return False

    try:
        print("Creating Messages table.")
        sql = """
            CREATE TABLE Messages (
                id SERIAL PRIMARY KEY ,
                from_id INT REFERENCES Users(id),
                to_id INT REFERENCES Users(id),
                creation_date TIMESTAMP 
            )
        """
        cur.execute(sql)
    except Exception as e:
        if e.pgcode == '42P07':
            print(f'Table Messages already exists.')
        else:
            print('Error', e.pgcode, ":", e)
            cur.close()
            connection.close()
            return False

    cur.close()
    connection.close()
    print(f'Database {new_dbname} succesfully created!')
    return True


if __name__ == "__main__":
    create_db()
