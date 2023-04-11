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

    def getQuiz(self,title):
        try:
            self.cursor.execute("SELECT * FROM Quiz WHERE title=(%s)", (title,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
                result = None
        return result

    def getAllQuiz(self):
        try:
            self.cursor.execute("SELECT * FROM Quiz")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
                result = None
        return result
    
    def getQuizId(self, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM Quiz WHERE idQuiz=(%s)", (quiz_id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
                result = None
        return result

    def getQuestionAll(self, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM Questions WHERE quiz_id=(%s)", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result
    
    def getOptionsAll(self, quest_id):
        try:
            self.cursor.execute("SELECT * FROM Options WHERE quest_id=(%s)", (quest_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result
    
    def getOptId(self, idOpt):
        try:
            self.cursor.execute("SELECT * FROM Options WHERE idOpt=(%s)", (idOpt,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result