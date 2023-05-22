from service.game import GameDatabaseService
from service.const import CONST
from service.logger import LoggerService
from service.config import ConfigService

import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.tree.command(name="question", description="Ajoutez une question")
@commands.has_role("Master")
async def question(ctx, question:str, channel:discord.TextChannel, rightAnswer:int, answer1:str, answer2:str, answer3:str=None, answer4:str=None):
    game.addQuestion(question,rightAnswer,answer1,answer2,answer3,answer4)

if __name__=='__main__':
    logger = LoggerService(True)
    logger.addLogs("Info","Bot is starting")
    config = ConfigService("config.yml")
    game = GameDatabaseService("database.db")
    bot.run(config.getKey("bot_token"))
