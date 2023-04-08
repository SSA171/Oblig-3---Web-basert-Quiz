import mysql.connector
from mysql.connector import errorcode

class QuizReg:

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

    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def getAll(self):
        try:
            self.cursor.execute("SELECT * FROM quiz")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def getQuestion(self, id):
        try:
            self.cursor.execute("SELECT * FROM quiz WHERE  id=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def deleteQuestion(self, id):
        try:
            self.cursor.execute("DELETE FROM quiz WHERE  id=(%s)", (id,))
        except mysql.connector.Error as err:
                print(err)
