from MessagingApp.user import User
from psycopg2 import connect
from MessagingApp.database_defaults import DEFAULT_DBNAME, DEFAULT_HOST, DEFAULT_USER, DEFAULT_NEW_DBNAME, DEFAULT_PWD
from MessagingApp.lib.clcrypto import check_password
import argparse


def get_not_none_args(args):
    args_dict = vars(args)
    not_none_args_dict = {}
    for key in args_dict:
        if args_dict[key]:
            not_none_args_dict[key] = args_dict[key]
    return not_none_args_dict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Username for user that is to be created or modified.")
    parser.add_argument('-p', '--password', help="Password for user under username.")
    parser.add_argument('-n', '--new_pass', help="New password for user under username.")
    parser.add_argument('-l', '--list', help="List all users.")
    parser.add_argument('-d', '--delete', help="Delete user under username.")
    parser.add_argument('-e', '--edit', help="Edit user's password.", action="store_true")

    args = parser.parse_args()
    not_none_args = get_not_none_args(args)
    return not_none_args


def connect_to_database():
    try:
        # create a connection to create the database itself
        print(f'Connecting to {DEFAULT_NEW_DBNAME}...')
        connection = connect(user=DEFAULT_USER, host=DEFAULT_HOST, password=DEFAULT_PWD, dbname=DEFAULT_NEW_DBNAME)
        connection.autocommit = True
    except Exception as e:
            print('Error', e.pgcode, ":", e)
            connection.close()
            return None
    return connection


def create_user(connection, username, password):
    if connection:
        cur = connection.cursor()
        user = User.load_user_by_username(cur, username)

        if user:
            print(f"User {username} already exists! Failed to add a new user.")
            return False

        if len(password) < 8:
            print(f'Password too short. Failed to add a new user.')
            return False

        new_user = User(username, password)
        return new_user.save_to_db(cur)


def edit_user(connection, username, password, new_password):
    if connection:
        cur = connection.cursor()
        user = User.load_user_by_username(cur, username)

        if not user:
            print(f"User {username} does not exist! Failed to update password.")
            return False

        if not check_password(password, user.hashed_password):
            print("Wrong password.")
            return False

        if len(new_password) < 8:
            print("New password too short. Failed to update password.")
            return False

        user.set_password(new_password)
        return user.save_to_db(cur)



def delete_user(connection, username, password):
    pass


def list_all_users(connection):
    pass


def process_args(args):

    connection = connect_to_database()

    if args['username'] and args['password'] and len(args) == 2:
        if create_user(connection, args['username'], args['password']):
            print(f"{args['username']} added successfully.")

    if args['username'] and args['password'] and args['edit'] and args['new_pass'] and len(args) == 4:
        if edit_user(connection, args['username'], args['password'], args['new_pass']):
            print(f"{args['username']}'s password updated successfully.")
    #
    # if args['username'] and args['password'] and args['delete'] and len(args) == 3:
    #     return delete_user(connection, args['username'], args['password'])
    #
    # if args['list'] and len(args) == 1:
    #     return list_all_users(connection)



def main():

    # parse args
    args = parse_args()

    # do something based on input provided in args
    process_args(args)


if __name__ == "__main__":
    main()
