import discord
from discord.ext import commands

intents = discord.intents.deault()
intents.message_content = True
bot = commands.Bot(command_prefix = '/', intents = intents)

