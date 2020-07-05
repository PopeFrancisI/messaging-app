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
    return args


def main():

    # parse args
    args = parse_args()
    


if __name__ == "__main__":
    main()
