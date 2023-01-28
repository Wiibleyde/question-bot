import discord
import sqlite3
import asyncio
import datetime
import json
import sys
import os
import time

commandList = ["help", "question", "answer", "leaderboard", "addpoints", "removepoints", "maintenance"]

class mainDB:
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

class Config:
    def __init__(self, fileName):
        self.fileName = fileName

    def loadConfig(self):
        with open(self.fileName) as json_file:
            return json.load(json_file)

    def getConfigItem(self, item):
        with open(self.fileName) as json_file:
            return json.load(json_file)[item]

    def setConfigItem(self, item, value):
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            data[item] = value
        with open(self.fileName, "w") as json_file:
            json.dump(data, json_file)

    def addConfigItem(self, item, value):
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            data[item] = value
        with open(self.fileName, "w") as json_file:
            json.dump(data, json_file)

    def removeConfigItem(self, item):
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            del data[item]
        with open(self.fileName, "w") as json_file:
            json.dump(data, json_file)
            
client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):
    try:
        if message.content.startswith(commandPrefix):
            command = message.content[1:].split(" ")[0]
            maintenance = ObjConfig.getConfigItem("maintenance")
            if maintenance == True and message.author.id not in moderatorID:
                await message.channel.send("Le bot est en maintenance !")
                await message.add_reaction("❌")
                return
            if maintenance == True and message.author.id in moderatorID:
                await message.channel.send("Le bot est en maintenance !")
                await message.add_reaction("⚠")
            if command not in commandList:
                await message.channel.send("Invalid command")
            else:
                logDB.addLog(command, message.author.name)
                if command == "question" and message.author.id in moderatorID:
                    messageArgs = message.content[1:]
                    question = messageArgs.split("\"")[1]
                    if question == "":
                        await message.channel.send("La question n'est pas valide !")
                        await message.add_reaction("❌")
                        return
                    answers = messageArgs.split("\"")[3].split(";")
                    if len(answers) < 2:
                        await message.channel.send("Il n'y a pas assez de réponses !")
                        await message.add_reaction("❌")
                        return
                    correct_answer = int(messageArgs.split("\"")[4])-1
                    if correct_answer > len(answers) or correct_answer < 0:
                        await message.channel.send("La réponse correcte n'est pas valide !")
                        await message.add_reaction("❌")
                        return
                    database.addQuestion(question, answers, correct_answer)
                    embed = discord.Embed(title="Question", description=question, color=0x00ff00)
                    for i in range(len(answers)):
                        embed.add_field(name=f"Réponse n°{i+1}", value=answers[i], inline=False)
                    embed.set_footer(text=f"Répondez avec le {commandPrefix}answer <numéro de réponse> en moins de {timeleft} minutes")
                    channel = client.get_channel(int(channelQuestionID))
                    await channel.send(embed=embed)
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
                        try:
                            answer = int(messageArgs.split(" ")[1])-1
                        except:
                            await message.author.send("La réponse n'est pas valide !")
                            await message.add_reaction("❌")
                            return
                        question = database.getQuestions()[-1]
                        if answer == question[3]:
                            pointsEarned = calcPoint(question[0])
                            await message.author.send(f"Bonne réponse ! Vous avez gagné {pointsEarned} points !")
                            await message.add_reaction("✅")
                            database.addRightAnswerToUser(message.author.id, question[0])
                            database.addQuestionToUser(message.author.id, question[0])
                        else:
                            await message.author.send(f"Mauvaise réponse, la bonne réponse était la réponse n°{question[3]+1}")
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
                    try:
                        points = int(messageArgs.split(" ")[2])
                    except:
                        await message.channel.send("Le nombre de points n'est pas valide !")
                        await message.add_reaction("❌")
                        return
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
                    try:
                        points = int(messageArgs.split(" ")[2])
                    except:
                        await message.channel.send("Le nombre de points n'est pas valide !")
                        await message.add_reaction("❌")
                        return
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
                        embed.add_field(name=f"{commandPrefix}addpoints <user_id> <nombre de points>", value="Ajoute des points à un utilisateur", inline=False)
                        embed.add_field(name=f"{commandPrefix}removepoints <user_id> <nombre de points>", value="Retire des points à un utilisateur", inline=False)
                        embed.add_field(name=f"{commandPrefix}maintenance", value="Active/désactive le mode maintenance", inline=False)
                    await message.channel.send(embed=embed)
                elif command == "maintenance" and message.author.id in moderatorID:
                    maintenance = ObjConfig.getConfigItem('maintenance')
                    if maintenance == "True":
                        ObjConfig.setConfigItem('maintenance', 'False')
                        await message.channel.send("Le mode maintenance est désormais désactivé !")
                        # restartProgram()
                    else:
                        ObjConfig.setConfigItem('maintenance', 'True')
                        await message.channel.send("Le mode maintenance est désormais activé !")
                elif command == "maintenance":
                    await message.channel.send("Vous n'avez pas les permissions pour utiliser cette commande !")
                    await message.add_reaction("❌")
                else:
                    await message.channel.send("Commande inconnue !")
                    await message.add_reaction("❌")
    except Exception as e:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="Error", value=e, inline=False)
        await message.channel.send(embed=embed)

def calcPoint(question_id):
    question = database.getQuestion(question_id)
    if question is None:
        return 0
    else:
        date = datetime.datetime.strptime(question[4], "%Y-%m-%d %H:%M:%S.%f")
        return 50 - int((datetime.datetime.now() - date).total_seconds()/60)

def getMessageById(message_id):
    return client.get_channel(int(channelQuestionID)).fetch_message(message_id)

async def get_username(user_id: int):
    user = await client.fetch_user(user_id)
    return user.name

async def StatusChanger():
    await client.wait_until_ready()
    while not client.is_closed():
        maintenance = ObjConfig.getConfigItem('maintenance')
        if maintenance == "True":
            await client.change_presence(activity=discord.Game(name="Maintenance"))
            await asyncio.sleep(3)
            continue
        leaderboard = database.getLeaderboard()
        status = ""
        for i in range(min(3, len(leaderboard))):
            status = status + f"{int(i)+1}. {await get_username(leaderboard[i][0])}" + " - " + f"{leaderboard[i][1]} points" + " | "
        status = status[:-2]
        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(3)

def loadConfigToVar():
    global discordBotToken, channelQuestionID, moderatorID, commandPrefix, timeleft, maintenance, ObjConfig, serverID
    ObjConfig = Config('config.json')
    discordBotToken = ObjConfig.loadConfig()['Bot Info']['Token']
    channelQuestionID = ObjConfig.loadConfig()['Server Information']['QuestionChannel']
    moderatorID = ObjConfig.loadConfig()['ModeratorList']
    commandPrefix = ObjConfig.loadConfig()['Bot Info']['Prefix']
    timeleft = ObjConfig.loadConfig()['Server Information']['Timeleft']
    serverID = ObjConfig.loadConfig()['Server Information']['ServerID']
    maintenance = ObjConfig.setConfigItem('maintenance', 'False')

if __name__ == "__main__":
    database = mainDB("quest-user.db")
    database.createTable()
    logDB=LogCommandDB("log.db")
    logDB.createTable()
    StatusChangerTask = client.loop.create_task(StatusChanger())
    loadConfigToVar()
    print("Configuration chargée !")
    print(f"Token : {discordBotToken}")
    print(f"Channel Question ID : {channelQuestionID}")
    print(f"Moderator ID : {moderatorID}")
    print(f"Command Prefix : {commandPrefix}")
    print(f"Timeleft : {timeleft}")
    print(f"Server ID : {serverID}")
    print(f"Maintenance : {maintenance}")
    client.run(discordBotToken)

