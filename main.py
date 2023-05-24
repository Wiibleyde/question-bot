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
async def question(interaction:discord.Interaction, question:str, channel:discord.TextChannel, rightAnswer:int, answer1:str, answer2:str, answer3:str=None, answer4:str=None):
    game.addQuestion(question,rightAnswer,answer1,answer2,answer3,answer4)
    channel = bot.get_channel(channel.id)
    embed = discord.Embed(title=question)
    embed.add_field(name="Réponse 1", value=answer1, inline=False)
    embed.add_field(name="Réponse 2", value=answer2, inline=False)
    if answer3 != None:
        embed.add_field(name="Réponse 3", value=answer3, inline=False)
    if answer4 != None:
        embed.add_field(name="Réponse 4", value=answer4, inline=False)
    await channel.send(embed=embed)
    # add buttons
    buttons = []
    for i in range(1,5):
        buttons.append(discord.ui.Button(label=str(i), custom_id=str(i)))
    view = discord.ui.View()
    view.add_item(buttons[0])
    view.add_item(buttons[1])
    if answer3 != None:
        view.add_item(buttons[2])
    if answer4 != None:
        view.add_item(buttons[3])
    await channel.send("Choisissez votre réponse", view=view)
    await interaction.response.send_message("Question ajoutée", ephemeral=True)

if __name__=='__main__':
    logger = LoggerService(True)
    logger.addLogs("Info","Bot is starting")
    config = ConfigService("config.yml")
    game = GameDatabaseService("database.db")
    bot.run(config.getKey("bot_token"))
