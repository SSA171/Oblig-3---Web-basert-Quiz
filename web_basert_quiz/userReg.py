import mysql.connector
from mysql.connector import errorcode

class UserReg:

    def __init__(self) -> None:

        dbconfig = {'host': '127.0.0.1',
                    'user': 'user',
                    'password': 'test',
                    'database': 'myDb', }

        self.configuration = dbconfig

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def getUser(self, username):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
                result = None
        return result