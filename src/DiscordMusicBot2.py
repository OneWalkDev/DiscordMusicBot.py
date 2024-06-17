import discord
import asyncio
from config.Config import DISCORD_TOKEN, LOG
from command.Command import load_extension
from discord.ext import commands
from logger.Logger import enable_logging
from service.YoutubeService import search

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents = intents)

async def main():
    async with bot:
        await load_extension(bot)
        await bot.start(DISCORD_TOKEN)

async def change_presence(bot):
    vc_count = 0
    for guild in bot.guilds:
        for voice_channel in guild.voice_channels:
            if bot.user in [member._user for member in voice_channel.members]:
                vc_count += 1
    await bot.change_presence(activity=discord.Game(name=f"♫MusicPlayer♫ /join | {len(bot.guilds)} servers | {str(vc_count)} vc"))

@bot.event
async def on_ready():
    await change_presence(bot)
    print('Running...') 

if __name__ == "__main__":
    if(LOG):
        enable_logging()
    asyncio.run(main())