# Imports
import discord
from dotenv import load_dotenv, find_dotenv
import os


# Client connection that connects to Discord
# used to interact with the Discord WebSocket and API.
client = discord.Client()


# Parse the .env file and then
# load the TOKEN as environment variables.
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


NOW_PLAYING = "lat!help"
