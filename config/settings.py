# Imports
import discord
from dotenv import load_dotenv, find_dotenv
from os import getenv
# from discord.ext import commands

COMMAND_PREFIX = "?lat "


# Client connection that connects to Discord
# Enable discord intents presences
intents = discord.Intents.all()
intents.presences = True
client = discord.Client(intents=intents)
# client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


# Parse the .env file and then
# load the TOKEN as environment variables.
load_dotenv(find_dotenv())
TOKEN: str = getenv("TOKEN")


NOW_PLAYING: str = COMMAND_PREFIX + "commands"
