from MessagingApp.user import User
from MessagingApp.message import Message
from psycopg2 import connect
from MessagingApp.database_defaults import DEFAULT_DBNAME, DEFAULT_HOST, DEFAULT_USER, DEFAULT_NEW_DBNAME, DEFAULT_PWD
from MessagingApp.lib.clcrypto import check_password
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Username of the sender.")
    parser.add_argument('-p', '--password', help="Password of the sender.")
    parser.add_argument('-t', '--to', help="Username of the message receiver.")
    parser.add_argument('-l', '--list', help="List all user's messages", action="store_true")
    parser.add_argument('-s', '--send', help="Message content.")

    args = parser.parse_args()
    return args


def connect_to_database():
    try:
        connection = connect(user=DEFAULT_USER, host=DEFAULT_HOST, password=DEFAULT_PWD, dbname=DEFAULT_NEW_DBNAME)
        connection.autocommit = True
    except Exception as e:
        print('Error', e.pgcode, ":", e)
        connection.close()
        return None
    return connection


def list_all_messages(connection, username, password):
    pass


def send_message(connection, username, password, to, msg_text):
    if connection:
        cur = connection.cursor()
        from_user = User.load_user_by_username(cur, username)
        to_user = User.load_user_by_username(cur, to)

        if not from_user:
            print(f"User {username} (sender) does not exist! Failed to send the message.")
            return False

        if not to_user:
            print(f"User {to} (receiver) does not exist! Failed to send the message.")
            return False

        if not check_password(password, from_user.hashed_password):
            print("Wrong password.")
            return False

        if len(msg_text) > 255:
            print("Message too long! Failed to send the message.")
            return False

        msg = Message(from_user.id, to_user.id, msg_text)
        return msg.save_to_db(cur)


def process_args(args):

    connection = connect_to_database()

    if args.username and args.password and args.list:
        list_all_messages(connection, args.username, args.password)
    elif args.username and args.password and args.to and args.send:
        send_message(connection, args.username, args.password, args.to, args.send)



def main():

    # parse args
    args = parse_args()

    # do something based on input provided in args
    process_args(args)


if __name__ == "__main__":
    main()
