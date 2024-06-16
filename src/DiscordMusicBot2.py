import discord
import asyncio
from config.Config import DISCORD_TOKEN, LOG
from command.Command import load_extension
from discord.ext import commands
import logging
import sys

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents = intents)

def enable_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

async def change_presence():
    vc_count = 0
    for guild in bot.guilds:
        for voice_channel in guild.voice_channels:
            if bot.user in [member.user for member in voice_channel.members]:
                vc_count += 1
    await bot.change_presence(activity=discord.Game(name=f"♫MusicPlayer♫ /join | {len(bot.guilds)} servers | {vc_count} vc"))

async def main():
    async with bot:
        await load_extension(bot)
        await bot.start(DISCORD_TOKEN)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"♫MusicPlayer♫ /join | {len(bot.guilds)} servers | 0 vc"))
    print('Running...') 

if __name__ == "__main__":
    if(LOG):
        enable_logging()
    asyncio.run(main())