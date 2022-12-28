# =================================================================================================================================================================
# Configuration
discordBotToken = "MTA1Njg4MDEzMTgzNjIzMTc1MQ.GrH7J6.tEfOxOCllo2cB89LJKF3A1Yq9vH6Z--1o2-7tM"
moderatorID = ["461807010086780930"]
commandPrefix = "%"
channelQuestionID = 965868671908073514
timeleft = 30 # in minutes
# =================================================================================================================================================================

import discord
import sqlite3
import asyncio
import datetime
import time
import json
from discord.ext import commands
from discord_ui import UI, SlashOption

commandList = ["help", "question", "answer", "removeQuestion", "leaderboard"]

class database:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answers TEXT, correct_answer INTEGER, date TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, points INTEGER)")
            conn.commit()

    def addQuestion(self, question, answers, correct_answer):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO questions (question, answers, correct_answer, date) VALUES (?, ?, ?, ?)", (question, json.dumps(answers), correct_answer, datetime.datetime.now()))
            conn.commit()

    def getQuestions(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM questions")
            return c.fetchall()

    def getQuestion(self, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM questions WHERE id=?", (question_id,))
            return c.fetchone()

    def addRightAnswerToUser(self, user_id, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (id, name, points) VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET points=points+?", (user_id, "test", 0, 1))
            conn.commit()

    def addWrongAnswerToUser(self, user_id, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (id, name, points) VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET points=points-?", (user_id, "test", 0, 1))
            conn.commit()

    def addPointsToUser(self, user_id, points):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (id, name, points) VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET points=points+?", (user_id, "test", 0, points))
            conn.commit()

    def getPoints(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT points FROM users WHERE id=?", (user_id,))
            return c.fetchone()

    def getLeaderboard(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users ORDER BY points DESC")
            return c.fetchall()

    def removeQuestion(self, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM questions WHERE id=?", (question_id,))
            conn.commit()

    def IsQuestionOK(self):
        lastQuestion = self.getQuestions()[-1]
        if (datetime.datetime.now() - datetime.datetime.strptime(lastQuestion[4], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() > timeleft*60:
            return False
        else:
            return True

    def AlreadyAnswered(self, user_id, question_id):
        # check if the user already answered the question
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            if c.fetchone() is None:
                return False
            else:
                return True

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
        if command not in commandList:
            await message.channel.send("Invalid command")
        else:
            print(f"Command {command} executed by {message.author.name}")
            if command == "question":
                # print the question in the channelQuestionID channel and add it to the database
                # question "What is the capital of France?" "Paris;Lyon;Marseille;Lille" 0
                messageArgs = message.content[1:]
                question = messageArgs.split("\"")[1]
                answers = messageArgs.split("\"")[3].split(";")
                correct_answer = int(messageArgs.split("\"")[4])
                database.addQuestion(question, answers, correct_answer)
                embed = discord.Embed(title="Nouvelle question", description=question, color=0x00ff00)
                for i in range(len(answers)):
                    embed.add_field(name=f"Réponse {i}", value=answers[i], inline=False)
                embed.set_footer(text=f"Répondez avec {commandPrefix}answer <id de la réponse>")
                await client.get_channel(channelQuestionID).send(embed=embed)
            elif command == "answer":
                # check if the answer is correct and add the user to the right or wrong list
                # answer 1
                messageArgs = message.content[1:]
                answer = int(messageArgs.split(" ")[1])
                lastQuestion = database.getQuestions()[-1]
                if database.IsQuestionOK():
                    if not database.AlreadyAnswered(message.author.id, lastQuestion[0]):
                        if answer == lastQuestion[3]:
                            database.addRightAnswerToUser(message.author.id, lastQuestion[0])
                            points = calcPoint(lastQuestion[4])
                            database.addPointsToUser(message.author.id, points)
                            await message.add_reaction("✅")
                            await message.author.send(f"Bravo ! Vous avez gagné {points} points !")
                        else:
                            database.addWrongAnswerToUser(message.author.id, lastQuestion[0])
                            await message.author.send("Mauvaise réponse !")
                    else:
                        await message.author.send("Vous avez déjà répondu à cette question !")
                else:
                    await message.author.send("Il n'y a pas de question en cours !")
            elif command == "leaderboard":
                # print the leaderboard
                leaderboard = database.getLeaderboard()
                embed = discord.Embed(title="Classement", description="", color=0x00ff00)
                for i in range(len(leaderboard)):
                    embed.add_field(name=f"{i+1} - {leaderboard[i][1]}", value=leaderboard[i][2], inline=False)
                await message.channel.send(embed=embed)
            

def calcPoint(question_id):
    # 50 points for the correct answer reduced with time (1 point per minute)
    question = database.getQuestion(question_id)
    if question is None:
        return 0
    else:
        date = datetime.datetime.strptime(question[4], "%Y-%m-%d %H:%M:%S.%f")
        return 50 - int((datetime.datetime.now() - date).total_seconds()/60)

def getMessageById(message_id):
    return client.get_channel(channelQuestionID).fetch_message(message_id)

if __name__ == "__main__":
    database = database("questions.db")
    database.createTable()
    client.run(discordBotToken)
