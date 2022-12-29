# =================================================================================================================================================================
# Configuration
discordBotToken = "MTA1Njg4MDEzMTgzNjIzMTc1MQ.GrH7J6.tEfOxOCllo2cB89LJKF3A1Yq9vH6Z--1o2-7tM"
moderatorID = ["461807010086780930"]
commandPrefix = "%"
channelQuestionID = 965868671908073515
timeleft = 30 # in minutes
# =================================================================================================================================================================

import discord
import sqlite3
import asyncio
import datetime
import time
import json
import requests

commandList = ["help", "question", "answer", "removeQuestion", "leaderboard"]

class database:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answers TEXT, correct_answer INTEGER, date TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, points INTEGER, idQuestion INTEGER)")
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

    def removeQuestion(self, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM questions WHERE id=?", (question_id,))
            conn.commit()

    def addUser(self, user_id):
        if self.getUser(user_id) == None:
            with sqlite3.connect(self.fileName) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO users (id, points, idQuestion) VALUES (?, ?, ?)", (user_id, 0, 0))
                conn.commit()

    def getUser(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            return c.fetchone()

    def addRightAnswerToUser(self, user_id, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET points=points+?, idQuestion=? WHERE id=?", (calcPoint(question_id), question_id, user_id))
            conn.commit()

    def addWrongAnswerToUser(self, user_id, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET idQuestion=? WHERE id=?", (question_id, user_id))
            conn.commit()
    
    def addQuestionToUser(self, user_id, question_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET idQuestion=? WHERE id=?", (question_id, user_id))
            conn.commit()

    def addPointsToUser(self, user_id, points):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET points=points+? WHERE id=?", (points, user_id))
            conn.commit()

    def removePointsToUser(self, user_id, points):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET points=points-? WHERE id=?", (points, user_id))
            conn.commit()

    def AlreadyAnswered(self, user_id, question_id):
        print(user_id, question_id)
        try:
            if self.getUser(user_id)[3] == question_id:
                return True
            else:
                return False
        except:
            self.addUser(user_id)
    
    def getLeaderboard(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users ORDER BY points DESC")
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
                embed = discord.Embed(title="Question", description=question, color=0x00ff00)
                for i in range(len(answers)):
                    embed.add_field(name=f"Answer {i}", value=answers[i], inline=False)
                embed.set_footer(text=f"Answer with {commandPrefix}answer <answer number> in {timeleft} minutes")
                msg = await client.get_channel(channelQuestionID).send(embed=embed)
                await message.add_reaction("✅")
            elif command == "answer":
                # check if the user has already answered to the question
                # answer 0
                print(database.getQuestions()[-1][0])
                if database.AlreadyAnswered(message.author.id, database.getQuestions()[-1][0]):
                    await message.channel.send("You already answered to this question")
                    await message.add_reaction("❌")
                else:
                    messageArgs = message.content[1:]
                    answer = int(messageArgs.split(" ")[1])
                    question = database.getQuestions()[-1]
                    if answer == question[3]:
                        await message.author.send(f"Correct answer")
                        await message.add_reaction("✅")
                        database.addRightAnswerToUser(message.author.id, question[0])
                        database.addPointsToUser(message.author.id, calcPoint(question[0]))
                        database.addQuestionToUser(message.author.id, question[0])
                    else:
                        await message.author.send(f"Incorrect answer")
                        await message.add_reaction("✅")
                        database.addWrongAnswerToUser(message.author.id, question[0])
                        database.addQuestionToUser(message.author.id, question[0])
            elif command == "leaderboard":
                # print the leaderboard
                leaderboard = database.getLeaderboard()
                embed = discord.Embed(title="Leaderboard", color=0x00ff00)
                print(leaderboard)
                for i in range(50):
                    embed.add_field(name=f"{i+1}. {getNameById(leaderboard[i][0])}", value=f"{leaderboard[i][1]} points", inline=False)
            
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

def getNameById(user_id):
    requete = requests.get(f"https://discord.com/api/v8/users/{user_id}", headers={"Authorization": f"Bot {discordBotToken}"})
    return requete.json()["username"]

if __name__ == "__main__":
    database = database("questions.db")
    database.createTable()
    client.run(discordBotToken)
