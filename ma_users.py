from MessagingApp.user import User
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Username for user that is to be created or modified.")
    parser.add_argument('-p', '--password', help="Password for user under username.")
    parser.add_argument('-n', '--new_pass', help="New password for user under username.")
    parser.add_argument('-l', '--list', help="List all users.")
    parser.add_argument('-d', '--delete', help="Delete user under username.")
    parser.add_argument('-e', '--edit', help="Edit user's password.")

    args = parser.parse_args()
    print(args)
    return args


def create_user():
    pass


def process_args(args):
    if args.username and args.password:
        return create_user()


def main():

    # parse args
    args = parse_args()

    # do something based on input provided in args
    process_args(args)


if __name__ == "__main__":
    main()
