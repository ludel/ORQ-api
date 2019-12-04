import sqlite3


class User:

    @staticmethod
    def init(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        query = """
            create table user (
                id INTEGER constraint user_pk primary key autoincrement,
                email VARCHAR(255) not null,
                password VARCHAR(255) not null,
                watchlist VARCHAR(255)
            );
        """

        try:
            cursor.execute(query)
        except sqlite3.OperationalError:
            print('Table user already exist')
        else:
            conn.commit()

        cursor.close()
