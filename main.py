import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import datetime
import sqlite3
import os
import sys

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
        if not os.path.isfile(self.fileName):
            self.createConfig()
            print("Config file created")
            print("Please fill in the config file and restart the bot")
            sys.exit()

    def createConfig(self):
        with open(self.fileName, "w") as json_file:
            json.dump({"Bot Info": {"Token": "", "Prefix": "!"}, "Server Information": {"Timeleft": 50}, "maintenance": "False"}, json_file, indent=4)

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
            
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")
    StatusChanger.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        print(f"Commands: {synced}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="question", description="Pose une question à la communauté")
async def question(interaction: discord.Interaction, question: str, rightanswer: int, reponse1: str, reponse2: str, reponse3: str = None, reponse4: str = None):
    logDB.addLog("question", interaction.user.id)
    if ObjConfig.getConfigItem("maintenance") == "True":
        await interaction.user.send("Le bot est en maintenance !")
        return
    if interaction.user.guild_permissions.administrator == False:
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande", ephemeral=True)
        return
    database.addQuestion(question, [reponse1, reponse2, reponse3, reponse4], rightanswer)
    embed = discord.Embed(title="Question", description=question, color=0x00ff00)
    embed.add_field(name="Réponse 1", value=reponse1, inline=False)
    embed.add_field(name="Réponse 2", value=reponse2, inline=False)
    if reponse3 != None:
        embed.add_field(name="Réponse 3", value=reponse3, inline=False)
    if reponse4 != None:
        embed.add_field(name="Réponse 4", value=reponse4, inline=False)
    if reponse3 == None and reponse4 != None:
        embed.add_field(name="Réponse 3", value="Réponse 3", inline=False)
    embed.set_footer(text=f"Question posée par {interaction.user.name}, pour répondre : /reponse")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reponse", description="Répond à une question")
async def reponse(interaction: discord.Interaction, reponse: int):
    logDB.addLog("reponse", interaction.user.id)
    if ObjConfig.getConfigItem("maintenance") == "True":
        await interaction.user.send("Le bot est en maintenance !")
        return
    if database.AlreadyAnswered(interaction.user.id, database.getQuestions()[-1][0]):
        await interaction.user.send("Vous avez déjà répondu à cette question !")
    else:
        question = database.getQuestions()[-1]
        rightAnswer = question[3]
        if reponse == rightAnswer:
            pointsEarned = calcPoint(question[0])
            database.addRightAnswerToUser(interaction.user.id, question[0])
            database.addQuestionToUser(interaction.user.id, question[0])
            await interaction.user.send(f"Bonne réponse ! Vous avez gagné {pointsEarned} points !")
        else:
            database.addWrongAnswerToUser(interaction.user.id, question[0])
            database.addQuestionToUser(interaction.user.id, question[0])
            await interaction.user.send(f"Mauvaise réponse ! La bonne réponse était {question[3]}")
    await interaction.response.send_message("Réponse envoyée !", ephemeral=True)

@bot.tree.command(name="classement", description="Affiche le classement")
async def classement(interaction: discord.Interaction):
    logDB.addLog("classement", interaction.user.id)
    leaderboard = database.getLeaderboard()
    embed = discord.Embed(title="Leaderboard", color=0x00ff00)
    for i in range(min(10, len(leaderboard))):
        embed.add_field(name=f"{int(i)+1}. {await get_username(leaderboard[i][0])}", value=f"{leaderboard[i][1]} points", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addpoints", description="Ajoute des points à un utilisateur")
async def addpoints(interaction: discord.Interaction, user: discord.User, points: int):
    logDB.addLog("addpoints", interaction.user.id)
    if interaction.user.guild_permissions.administrator:
        if database.getUser(user.id) == None:
            await interaction.response.send_message("Cet utilisateur n'existe pas ou n'a pas encore répondu à une question !")
        else:
            database.addPointsToUser(user.id, points)
            await interaction.response.send_message(f"Vous avez ajouté {points} points à {user.name}")
    else:
        await interaction.user.send("Vous n'avez pas la permission d'utiliser cette commande !")
    await interaction.delete_original_response()

@bot.tree.command(name="removepoints", description="Retire des points à un utilisateur")
async def removepoints(interaction: discord.Interaction, user: discord.User, points: int):
    logDB.addLog("removepoints", interaction.user.id)
    if interaction.user.guild_permissions.administrator:
        if database.getUser(user.id) == None:
            await interaction.response.send_message("Cet utilisateur n'existe pas ou n'a pas encore répondu à une question !")
        else:
            database.removePointsToUser(user.id, points)
            await interaction.response.send_message(f"Vous avez retiré {points} points à {user.name}")
    else:
        await interaction.user.send("Vous n'avez pas la permission d'utiliser cette commande !")

@bot.tree.command(name="maintenance", description="Active/Désactive la maintenance")
async def maintenance(interaction: discord.Interaction, onoff: bool):
    logDB.addLog("maintenance", interaction.user.id)
    if interaction.user.guild_permissions.administrator:
        if onoff:
            ObjConfig.setConfigItem("maintenance", "True")
            await interaction.response.send_message("La maintenance est activée !")
        else:
            ObjConfig.setConfigItem("maintenance", "False")
            await interaction.response.send_message("La maintenance est désactivée !")
    else:
        await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande !")
                               
def calcPoint(question_id):
    question = database.getQuestion(question_id)
    if question is None:
        return 0
    else:
        date = datetime.datetime.strptime(question[4], "%Y-%m-%d %H:%M:%S.%f")
        return 50 - int((datetime.datetime.now() - date).total_seconds()/60)

async def get_username(user_id: int):
    user = await bot.fetch_user(user_id)
    return user.name

@tasks.loop(seconds=5)
async def StatusChanger():
    if ObjConfig.getConfigItem('maintenance') == "True":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="En maintenance"))
    else:
        first = database.getLeaderboard()[0]
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{await get_username(first[0])} ({first[1]} points)"))

def loadConfigToVar():
    global discordBotToken, commandPrefix, timeleft, maintenance, ObjConfig
    ObjConfig = Config('conf.json')
    discordBotToken = ObjConfig.loadConfig()['Bot Info']['Token']
    # moderatorID = ObjConfig.loadConfig()['ModeratorList']
    commandPrefix = ObjConfig.loadConfig()['Bot Info']['Prefix']
    timeleft = ObjConfig.loadConfig()['Server Information']['Timeleft']
    maintenance = ObjConfig.getConfigItem('maintenance')

if __name__ == "__main__":
    database = mainDB("quest-user.db")
    database.createTable()
    logDB=LogCommandDB("log.db")
    logDB.createTable()
    loadConfigToVar()
    print("Configuration chargée !")
    print(f"Token : {discordBotToken}")
    # print(f"Moderator ID : {moderatorID}")
    print(f"Command Prefix : {commandPrefix}")
    print(f"Timeleft : {timeleft}")
    print(f"Maintenance : {maintenance}")
    bot.run(discordBotToken)
