import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

LOG = os.getenv('LOG') == "True" or os.getenv("LOG") == "true"