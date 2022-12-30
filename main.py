# =================================================================================================================================================================
# Configuration
discordBotToken = "MTA1Njg4MDEzMTgzNjIzMTc1MQ.GrH7J6.tEfOxOCllo2cB89LJKF3A1Yq9vH6Z--1o2-7tM"
moderatorID = [461807010086780930, 374173210519928832,280804426376151041]
commandPrefix = "<"
channelQuestionID = 1058101751120674967
timeleft = 30 # in minutes
# =================================================================================================================================================================

import discord
import sqlite3
import asyncio
import datetime
import time
import json
import requests

commandList = ["help", "question", "answer", "leaderboard", "addpoints", "removepoints"]

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
        try:
            if self.getUser(user_id)[2] == question_id:
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

class LogCommandDB:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, command TEXT, user TEXT, date TEXT)")
            conn.commit()

    def addLog(self, command, user):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO logs (command, user, date) VALUES (?, ?, ?)", (command, user, datetime.datetime.now()))
            conn.commit()
        print(f"Command {command} was executed by {user} at {datetime.datetime.now()}")

    def getLogs(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs")
            return c.fetchall()

    def getLogsByCommand(self, command):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=?", (command,))
            return c.fetchall()

    def getLogsByUser(self, user):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE user=?", (user,))
            return c.fetchall()

    def getLogsByDate(self, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE date=?", (date,))
            return c.fetchall()

    def getLogsByDateRange(self, date1, date2):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE date BETWEEN ? AND ?", (date1, date2))
            return c.fetchall()

    def getLogsByCommandAndUser(self, command, user):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=? AND user=?", (command, user))
            return c.fetchall()

    def getLogsByCommandAndDate(self, command, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=? AND date=?", (command, date))
            return c.fetchall()

    def getLogsByCommandAndDateRange(self, command, date1, date2):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=? AND date BETWEEN ? AND ?", (command, date1, date2))
            return c.fetchall()

    def getLogsByUserAndDate(self, user, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE user=? AND date=?", (user, date))
            return c.fetchall()

    def getLogsByUserAndDateRange(self, user, date1, date2):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE user=? AND date BETWEEN ? AND ?", (user, date1, date2))
            return c.fetchall()

    def getLogsByCommandAndUserAndDate(self, command, user, date):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=? AND user=? AND date=?", (command, user, date))
            return c.fetchall()

    def getLogsByCommandAndUserAndDateRange(self, command, user, date1, date2):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE command=? AND user=? AND date BETWEEN ? AND ?", (command, user, date1, date2))
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
            logDB.addLog(command, message.author.name)
            if command == "question" and message.author.id in moderatorID:
                messageArgs = message.content[1:]
                question = messageArgs.split("\"")[1]
                answers = messageArgs.split("\"")[3].split(";")
                correct_answer = int(messageArgs.split("\"")[4])
                database.addQuestion(question, answers, correct_answer)
                embed = discord.Embed(title="Question", description=question, color=0x00ff00)
                for i in range(len(answers)):
                    embed.add_field(name=f"Réponse n°{i}", value=answers[i], inline=False)
                embed.set_footer(text=f"Répondez avec le {commandPrefix}answer <numéro de réponse> en {timeleft} de minutes")
                msg = await client.get_channel(channelQuestionID).send(embed=embed)
                await message.add_reaction("✅")
            elif command == "question":
                await message.channel.send("Vous n'avez pas les permissions pour utiliser cette commande !")
                await message.add_reaction("❌")
            elif command == "answer":
                if database.AlreadyAnswered(message.author.id, database.getQuestions()[-1][0]):
                    await message.author.send("Vous avez déjà répondu à cette question !")
                    await message.add_reaction("❌")
                else:
                    messageArgs = message.content[1:]
                    answer = int(messageArgs.split(" ")[1])
                    question = database.getQuestions()[-1]
                    if answer == question[3]:
                        pointsEarned = calcPoint(question[0])
                        await message.author.send(f"Bonne réponse ! Vous avez gagné {pointsEarned} points !")
                        await message.add_reaction("✅")
                        database.addRightAnswerToUser(message.author.id, question[0])
                        database.addQuestionToUser(message.author.id, question[0])
                    else:
                        await message.author.send(f"Mauvaise réponse, la bonne réponse était la réponse n°{question[3]}")
                        await message.add_reaction("✅")
                        database.addWrongAnswerToUser(message.author.id, question[0])
                        database.addQuestionToUser(message.author.id, question[0])
                await message.delete()
            elif command == "leaderboard":
                leaderboard = database.getLeaderboard()
                embed = discord.Embed(title="Leaderboard", color=0x00ff00)
                for i in range(min(10, len(leaderboard))):
                    embed.add_field(name=f"{int(i)+1}. {await get_username(leaderboard[i][0])}", value=f"{leaderboard[i][1]} points", inline=False)
                await message.channel.send(embed=embed)
            elif command == "addpoints" and message.author.id in moderatorID:
                messageArgs = message.content[1:]
                user = messageArgs.split(" ")[1]
                points = int(messageArgs.split(" ")[2])
                if database.getUser(user) == None:
                    await message.channel.send("Cet utilisateur n'existe pas ou n'a pas encore répondu à une question !")
                    await message.add_reaction("❌")
                else:
                    database.addPointsToUser(user, points)
                    await message.add_reaction("✅")
            elif command == "addpoints":
                print(message.author.id)
                print(moderatorID)
                await message.channel.send("Vous n'avez pas les permissions pour utiliser cette commande !")
                await message.add_reaction("❌")
            elif command == "removepoints" and message.author.id in moderatorID:
                messageArgs = message.content[1:]
                user = messageArgs.split(" ")[1]
                points = int(messageArgs.split(" ")[2])
                if database.getUser(user) == None:
                    await message.channel.send("Cet utilisateur n'existe pas ou n'a pas encore répondu à une question !")
                    await message.add_reaction("❌")
                else:
                    database.removePointsToUser(user, points)
                    await message.add_reaction("✅")
            elif command == "removepoints":
                await message.channel.send("Vous n'avez pas les permissions pour utiliser cette commande !")
                await message.add_reaction("❌")
            elif command == "help":
                embed = discord.Embed(title="Help", color=0x00ff00)
                embed.add_field(name=f"{commandPrefix}answer <numéro de la réponse>", value="Répond à la question", inline=False)
                embed.add_field(name=f"{commandPrefix}leaderboard", value="Affiche le leaderboard", inline=False)
                if message.author.id in moderatorID:
                    embed.add_field(name=f"{commandPrefix}question \"<question>\" \"<réponse 1>;<réponse 2>;...\" <numéro de la bonne réponse>", value="Pose une question", inline=False)
                    embed.add_field(name=f"{commandPrefix}addpoints <user> <nombre de points>", value="Ajoute des points à un utilisateur", inline=False)
                    embed.add_field(name=f"{commandPrefix}removepoints <user> <nombre de points>", value="Retire des points à un utilisateur", inline=False)
                await message.channel.send(embed=embed)
                            
def calcPoint(question_id):
    question = database.getQuestion(question_id)
    if question is None:
        return 0
    else:
        date = datetime.datetime.strptime(question[4], "%Y-%m-%d %H:%M:%S.%f")
        return 50 - int((datetime.datetime.now() - date).total_seconds()/60)

def getMessageById(message_id):
    return client.get_channel(channelQuestionID).fetch_message(message_id)

async def get_username(user_id: int):
    user = await client.fetch_user(user_id)
    return user.name

async def StatusChanger():
    await client.wait_until_ready()
    while not client.is_closed():
        leaderboard = database.getLeaderboard()
        status = ""
        for i in range(min(3, len(leaderboard))):
            status = status + f"{int(i)+1}. {await get_username(leaderboard[i][0])}" + " - " + f"{leaderboard[i][1]} points" + " | "
        status = status[:-2]
        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)

if __name__ == "__main__":
    database = database("quest-user.db")
    database.createTable()
    logDB=LogCommandDB("log.db")
    logDB.createTable()
    StatusChangerTask = client.loop.create_task(StatusChanger())
    client.run(discordBotToken)
