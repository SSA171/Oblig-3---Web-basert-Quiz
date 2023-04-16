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

    def getQuiz(self, title):
        try:
            self.cursor.execute(
                "SELECT * FROM Quiz WHERE title=(%s)", (title,))
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
            self.cursor.execute(
                "SELECT * FROM Quiz WHERE idQuiz=(%s)", (quiz_id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getQuestionAll(self, quiz_id):
        try:
            self.cursor.execute(
                "SELECT * FROM Questions WHERE quiz_id=(%s)", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getOptionsAll(self, quest_id):
        try:
            self.cursor.execute(
                "SELECT * FROM Options WHERE quest_id=(%s)", (quest_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getOptId(self, idOpt):
        try:
            self.cursor.execute(
                "SELECT * FROM Options WHERE idOpt=(%s)", (idOpt,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getResultsAll(self, quiz_id):
        try:
            self.cursor.execute(
                "SELECT * FROM Results WHERE quiz_id=(%s)", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getUserAnswersAll(self, idResult):
        try:
            self.cursor.execute(
                "SELECT * FROM User_answers WHERE idResults =(%s)", (idResult,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def getLastQuestId(self):
        try:
            self.cursor.execute(
                "SELECT * FROM Questions ORDER BY idQuest DESC LIMIT 1;")
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
            result = None
        return result

    def addResult(self, user_id, quiz_id, score, totalt):
        try:
            sql1 = "INSERT INTO Results (user_id, quiz_id, correct_answers, total_questions) VALUES (%s, %s, %s, %s)"
            values = (user_id, quiz_id, score, totalt)
            self.cursor.execute(sql1, values)
            self.conn.commit()
            print("Quiz result added successfully")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def addQuiz(self, title):
        try:
            sql1 = "INSERT INTO Quiz (title) VALUES (%s)"
            values = (title,)
            self.cursor.execute(sql1, values)
            self.conn.commit()
            print("New quiz added successfully")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def addQuestion(self, quiz_id, question_text, category):
        try:
            sql1 = "INSERT INTO Questions (quiz_id, question_text, category) VALUES (%s, %s, %s)"
            values = (quiz_id, question_text, category)
            self.cursor.execute(sql1, values)
            self.conn.commit()
            print("Question added successfully")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def addOptions(self, quest_id, option_text, is_correct):
        try:
            sql1 = "INSERT INTO Options (quest_id, option_text, is_correct) VALUES (%s, %s, %s)"
            values = (quest_id, option_text, is_correct)
            self.cursor.execute(sql1, values)
            self.conn.commit()
            print("Question added successfully")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def addUserAnswer(self, quest_id, idOpt, idUser):
        try:
            sql1 = "INSERT INTO User_answers (quest_id, idOpt,idUser) VALUES (%s, %s,%s)"
            values = (quest_id, idOpt, idUser)
            self.cursor.execute(sql1, values)
            self.conn.commit()
            print("User answer added successfully")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def updateQuestion(self, question_id, quiz_id, question_text, category):
        try:
            sql1 = "UPDATE Questions SET question_text = %s, category = %s WHERE idQuest = %s AND quiz_id =%s"

            self.cursor.execute(
                sql1, (question_text, category, question_id, quiz_id))

            self.conn.commit()

            print("Question updated successfully")

        except mysql.connector.Error as err:
            self.conn.rollback()
            print("Error updating question:", err)

    def updateOption(self, option_id, quest_id, option_text, is_correct):
        try:
            sql1 = "UPDATE Options SET option_text = %s, is_correct = %s WHERE idOpt = %s AND quest_id = %s"
            self.cursor.execute(
                sql1, (option_text, is_correct, option_id, quest_id))

            self.conn.commit()

            print("Question updated successfully")

        except mysql.connector.Error as err:
            self.conn.rollback()
            print(err)

    def deleteQuestion(self, idQuest):
        try:
            self.deleteOption(idQuest)
            self.cursor.execute(
                "DELETE FROM Questions WHERE  idQuest=(%s)", (idQuest,))
            print('Question deleted successfully')
        except mysql.connector.Error as err:
            print(err)

    def deleteOption(self, quest_id):
        try:
            self.cursor.execute(
                "DELETE FROM User_answers WHERE idOpt IN (SELECT idOpt FROM Options WHERE quest_id = %s)", (quest_id,))
            print('User_answers rows deleted successfully')

            self.cursor.execute(
                "DELETE FROM Options WHERE quest_id = %s", (quest_id,))
            print('Options rows deleted successfully')
        except mysql.connector.Error as err:
            print(err)
