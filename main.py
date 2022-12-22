# =================================================================================================================================================================
# Configuration
discordBotToken = "TOKEN"
moderatorID = ["461807010086780930"]
commandPrefix = "%"
# =================================================================================================================================================================

import discord
import sqlite3
import asyncio
import datetime
import time
import json
from discord.ext import commands
from discord_ui import UI, SlashOption

commandList = ["help", "ping", "question", "finish", "top"]

class ScoreDB:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, user_id INTEGER, score INTEGER, right_answers_questions_ids TEXT, wrong_answers_questions_ids TEXT, date text)")
            conn.commit()

    def addScore(self, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scores (user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date) VALUES (?, ?, ?, ?, ?)", (user_id, score, json.dumps(right_answers_questions_ids), json.dumps(wrong_answers_questions_ids), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def getScore(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT score FROM scores WHERE user_id = ?", (user_id,))
            return c.fetchone()

    def getScores(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores")
            return c.fetchall()

    def getScoresByDate(self, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE date LIKE ?", (f"%{date}%",))
            return c.fetchall()

    def getScoresByUser(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ?", (user_id,))
            return c.fetchall()

    def getScoresByScore(self, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE score = ?", (score,))
            return c.fetchall()

    def getScoresByRightAnswersQuestionsIDs(self, right_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE right_answers_questions_ids = ?", (json.dumps(right_answers_questions_ids),))
            return c.fetchall()

    def getScoresByWrongAnswersQuestionsIDs(self, wrong_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE wrong_answers_questions_ids = ?", (json.dumps(wrong_answers_questions_ids),))
            return c.fetchall()

    def getScoresByDateAndUser(self, date, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE date LIKE ? AND user_id = ?", (f"%{date}%", user_id))
            return c.fetchall()

    def getScoresByDateAndScore(self, date, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE date LIKE ? AND score = ?", (f"%{date}%", score))
            return c.fetchall()

    def getScoresByDateAndRightAnswersQuestionsIDs(self, date, right_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE date LIKE ? AND right_answers_questions_ids = ?", (f"%{date}%", json.dumps(right_answers_questions_ids)))
            return c.fetchall()

    def getScoresByDateAndWrongAnswersQuestionsIDs(self, date, wrong_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE date LIKE ? AND wrong_answers_questions_ids = ?", (f"%{date}%", json.dumps(wrong_answers_questions_ids)))
            return c.fetchall()

    def getScoresByUserAndScore(self, user_id, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND score = ?", (user_id, score))
            return c.fetchall()

    def getScoresByUserAndRightAnswersQuestionsIDs(self, user_id, right_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND right_answers_questions_ids = ?", (user_id, json.dumps(right_answers_questions_ids)))
            return c.fetchall()

    def getScoresByUserAndWrongAnswersQuestionsIDs(self, user_id, wrong_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND wrong_answers_questions_ids = ?", (user_id, json.dumps(wrong_answers_questions_ids)))
            return c.fetchall()

    def getScoresByUserAndDateAndScore(self, user_id, date, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND date LIKE ? AND score = ?", (user_id, f"%{date}%", score))
            return c.fetchall()

    def getScoresByUserAndDateAndRightAnswersQuestionsIDs(self, user_id, date, right_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND date LIKE ? AND right_answers_questions_ids = ?", (user_id, f"%{date}%", json.dumps(right_answers_questions_ids)))
            return c.fetchall()

    def getScoresByUserAndDateAndWrongAnswersQuestionsIDs(self, user_id, date, wrong_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND date LIKE ? AND wrong_answers_questions_ids = ?", (user_id, f"%{date}%", json.dumps(wrong_answers_questions_ids)))
            return c.fetchall()

    def getScoresByUserAndScoreAndRightAnswersQuestionsIDs(self, user_id, score, right_answers_questions_ids):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, user_id, score, right_answers_questions_ids, wrong_answers_questions_ids, date FROM scores WHERE user_id = ? AND score = ? AND right_answers_questions_ids = ?", (user_id, score, json.dumps(right_answers_questions_ids)))
            return c.fetchall()

class QuestionDB:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answers TEXT, correct_answer INTEGER, date text, users_right_ids TEXT, users_wrong_ids TEXT)")
            conn.commit()

    def addQuestion(self, question, answers, correct_answer):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO questions (question, answers, correct_answer, date, users_right_ids, users_wrong_ids) VALUES (?, ?, ?, ?, ?, ?)", (question, json.dumps(answers), correct_answer, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), json.dumps([]), json.dumps([])))
            conn.commit()

    def addRightAnswer(self, question_id, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT users_right_ids FROM questions WHERE id = ?", (question_id,))
            users_right_ids = json.loads(c.fetchone()[0])
            users_right_ids.append(user_id)
            c.execute("UPDATE questions SET users_right_ids = ? WHERE id = ?", (json.dumps(users_right_ids), question_id))
            conn.commit()

    def addWrongAnswer(self, question_id, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT users_wrong_ids FROM questions WHERE id = ?", (question_id,))
            users_wrong_ids = json.loads(c.fetchone()[0])
            users_wrong_ids.append(user_id)
            c.execute("UPDATE questions SET users_wrong_ids = ? WHERE id = ?", (json.dumps(users_wrong_ids), question_id))
            conn.commit()

    def getQuestion(self, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT question, answers, correct_answer, date, users_right_ids, users_wrong_ids FROM questions WHERE id = ?", (question_id,))
            return c.fetchone()

    def getQuestions(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, question, answers, correct_answer, date, users_right_ids, users_wrong_ids FROM questions")
            return c.fetchall()

    def getQuestionsByUser(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, question, answers, correct_answer, date, users_right_ids, users_wrong_ids FROM questions WHERE users_right_ids LIKE ? OR users_wrong_ids LIKE ?", (f"%{user_id}%", f"%{user_id}%"))
            return c.fetchall()

    def getQuestionsByDate(self, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, question, answers, correct_answer, date, users_right_ids, users_wrong_ids FROM questions WHERE date LIKE ?", (f"%{date}%",))
            return c.fetchall()

    def getQuestionsByDateRange(self, date_from, date_to):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT id, question, answers, correct_answer, date, users_right_ids, users_wrong_ids FROM questions WHERE date BETWEEN ? AND ?", (date_from, date_to))
            return c.fetchall()

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):
    if message.content.startswith(commandPrefix):
        command = message.content[1:].split(" ")[0]
        args = message.content[1:].split(" ")[1:]
        if command not in commandList:
            await message.channel.send("Invalid command")
        else:
            if command == "question"

if __name__ == "__main__":
    scoreDB = ScoreDB("scores.db")
    scoreDB.createTable()
    client.run(discordBotToken)
