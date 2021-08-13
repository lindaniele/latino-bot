import os
from dotenv import load_dotenv, find_dotenv

# The prefix that will be used to parse commands.
COMMAND_PREFIX = "?lat "

# The bot token.
load_dotenv(find_dotenv())
BOT_TOKEN = os.getenv("TOKEN")

# The now playing game.
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
