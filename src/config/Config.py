import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GLOBAL = os.getenv('GLOBAL')
GUILD_ID = int(os.getenv('GUILD_ID'))

LOG = os.getenv('LOG') == "True" or os.getenv("LOG") == "true"