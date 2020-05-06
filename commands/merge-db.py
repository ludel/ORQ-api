import sqlite3
import uuid


def main(new_db, old_db):
    new = sqlite3.connect(new_db)
    new_db_cursor = new.cursor()

    old = sqlite3.connect(old_db)
    old_db_cursor = old.cursor()

    for row in old_db_cursor.execute('SELECT email, password FROM user'):
        email = row[0]
        password = row[1]
        token = uuid.uuid4().hex
        print(email)
        new_db_cursor.execute(f'INSERT INTO user(email, password, token) VALUES (?,?,?)', [email, password, token])

    new.commit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--new",
        type=str
    )
    parser.add_argument(
        "-o",
        "--old",
        type=str,
    )

    args = parser.parse_args()
    main(args.new, args.old)
