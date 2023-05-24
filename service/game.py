import sqlite3

from .const import CONST

class GameDatabaseService:
    def __init__(self,filename):
        self.filename = CONST.DATA_PATH + filename
        self.createDatabase()

    def createDatabase(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT)"
        req1 = "CREATE TABLE IF NOT EXISTS answers (id INTEGER PRIMARY KEY AUTOINCREMENT, idQuestion INTEGER, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT)"
        req2 = "CREATE TABLE IF NOT EXISTS rightAnswers(id INTEGER PRIMARY KEY AUTOINCREMENT, idQuestion INTEGER, rightAnswerId INTEGER)"
        req3 = "CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY AUTOINCREMENT, discordId INTEGER, points INTEGER, rightAnswers TEXT, wrongAnswers TEXT, date TEXT)"
        c.execute(req0)
        c.execute(req1)
        c.execute(req2)
        c.execute(req3)
        conn.close()

    def addQuestion(self,question, rightAnswer, answer1, answer2, answer3=None, answer4=None):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "INSERT INTO questions (question) VALUES (?)"
        c.execute(req0,(question,))
        idQuestion = c.lastrowid
        req1 = "INSERT INTO answers (idQuestion, answer1, answer2, answer3, answer4) VALUES (?,?,?,?,?)"
        c.execute(req1,(idQuestion,answer1,answer2,answer3,answer4))
        req2 = "INSERT INTO rightAnswers (idQuestion, rightAnswerId) VALUES (?,?)"
        c.execute(req2,(idQuestion,rightAnswer))
        conn.commit()
        conn.close()

    def removeQuestion(self,questionId):
        # delete the question in ALL tables
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "DELETE FROM questions WHERE id = ?"
        c.execute(req0,(questionId,))
        req1 = "DELETE FROM answers WHERE idQuestion = ?"
        c.execute(req1,(questionId,))
        req2 = "DELETE FROM rightAnswers WHERE idQuestion = ?"
        c.execute(req2,(questionId,))
        conn.commit()
        conn.close()

    def getQuestion(self,questionId):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM questions WHERE id = ?"
        c.execute(req0,(questionId,))
        question = c.fetchone()
        req1 = "SELECT * FROM answers WHERE idQuestion = ?"
        c.execute(req1,(questionId,))
        answers = c.fetchone()
        req2 = "SELECT * FROM rightAnswers WHERE idQuestion = ?"
        c.execute(req2,(questionId,))
        rightAnswer = c.fetchone()
        conn.close()
        return question,answers,rightAnswer
    
    def addPointToUser(self,discordUserId,points):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM scores WHERE discordId = ?"
        c.execute(req0,(discordUserId,))
        user = c.fetchone()
        if user is None:
            req1 = "INSERT INTO scores (discordId, points) VALUES (?,?)"
            c.execute(req1,(discordUserId,points))
        else:
            req2 = "UPDATE scores SET points = ? WHERE discordId = ?"
            c.execute(req2,(user[2]+points,discordUserId))
        conn.commit()
        conn.close()

    def addRightAnswerToUser(self,discordUserId,questionId):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM scores WHERE discordId = ?"
        c.execute(req0,(discordUserId,))
        user = c.fetchone()
        if user is None:
            req1 = "INSERT INTO scores (discordId, rightAnswers) VALUES (?,?)"
            c.execute(req1,(discordUserId,str(questionId)))
        else:
            req2 = "UPDATE scores SET rightAnswers = ? WHERE discordId = ?"
            c.execute(req2,(user[4]+","+str(questionId),discordUserId))
        conn.commit()
        conn.close()

    def addWrongAnswerToUser(self,discordUserId,questionId):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM scores WHERE discordId = ?"
        c.execute(req0,(discordUserId,))
        user = c.fetchone()
        if user is None:
            req1 = "INSERT INTO scores (discordId, wrongAnswers) VALUES (?,?)"
            c.execute(req1,(discordUserId,str(questionId)))
        else:
            req2 = "UPDATE scores SET wrongAnswers = ? WHERE discordId = ?"
            c.execute(req2,(user[5]+","+str(questionId),discordUserId))
        conn.commit()
        conn.close()

    def getScore(self,discordUserId):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM scores WHERE discordId = ?"
        c.execute(req0,(discordUserId,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getTop10(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        req0 = "SELECT * FROM scores ORDER BY points DESC LIMIT 10"
        c.execute(req0)
        users = c.fetchall()
        conn.close()
        return users
