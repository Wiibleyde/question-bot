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

commandList = ["help", "ping", "question", "finish", "top"]

class ScoreDB:
    def __init__(self, fileName):
        self.fileName = fileName

    def createTable(self):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, user_id INTEGER, score INTEGER, last_updated INTEGER)")
            conn.commit()

    def addScore(self, user_id, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scores (user_id, score, last_updated) VALUES (?, ?, ?)", (user_id, score, int(time.time())))
            conn.commit()

    def updateScore(self, user_id, score):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("UPDATE scores SET score = ?, last_updated = ? WHERE user_id = ?", (score, int(time.time()), user_id))
            conn.commit()

    def getScore(self, user_id):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT score FROM scores WHERE user_id = ?", (user_id,))
            return c.fetchone()

    def getTopScores(self, limit):
        with sqlite3.connect(self.fileName) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
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
    if message.content.startswith("%"):
        if message.content[1:].split(" ")[0] not in commandList:
            await client.send_message(message.channel, "Invalid command. Type `%help` for a list of commands.")
        else:
            if message.content[1:].split(" ")[0] == "help":
                embed = discord.Embed(title="Help", description="List of commands", color=0x00ff00)
                for command in commandList:
                    embed.add_field(name=command, value="Description", inline=False)
                await client.send_message(message.channel, embed=embed)
            elif message.content[1:].split(" ")[0] == "ping":
                await client.send_message(message.channel, "Pong!")
            elif message.content[1:].split(" ")[0] == "question":
                # %question "Question" "Answer 1;Answer 2;Answer 3;Answer 4" "Correct Answer Number"
                if len(message.content[1:].split(" ")) < 4:
                    await client.send_message(message.channel, "Invalid command. Type `%help` for a list of commands.")
                else:
                    question = message.content[1:].split(" ")[1]
                    answers = message.content[1:].split(" ")[2].split(";")
                    correctAnswer = int(message.content[1:].split(" ")[3])
                    if correctAnswer > len(answers):
                        await client.send_message(message.channel, "Invalid command. Type `%help` for a list of commands.")
                    else:
                        embed = discord.Embed(title="Question", description=question, color=0x00ff00)
                        embed.add_field(name="Answers", value=" ".join([f"{i+1}. {answers[i]}" for i in range(len(answers))]), inline=False)
                        await client.send_message(message.channel, embed=embed)
                        await client.send_message(message.channel, f"Correct answer: {correctAnswer}")
            elif message.content[1:].split(" ")[0] == "finish":
                if message.author.id in moderatorID:
                    await client.send_message(message.channel, "Finished!")
                else:
                    await client.send_message(message.channel, "You don't have permission to use this command.")
            elif message.content[1:].split(" ")[0] == "top":
                if len(message.content[1:].split(" ")) < 2:
                    await client.send_message(message.channel, "Invalid command. Type `%help` for a list of commands.")
                else:
                    limit = int(message.content[1:].split(" ")[1])
                    topScores = scoreDB.getTopScores(limit)
                    embed = discord.Embed(title="Top Scores", description="List of top scores", color=0x00ff00)
                    for i in range(len(topScores)):
                        embed.add_field(name=f"{i+1}. {client.get_user(topScores[i][0]).name}", value=f"{topScores[i][1]} points", inline=False)
                    await client.send_message(message.channel, embed=embed)

if __name__ == "__main__":
    scoreDB = ScoreDB("scores.db")
    scoreDB.createTable()
    client.run(discordBotToken)
