import discord
from discord import app_commands
from discord.ext import commands
from config.Config import GUILD_ID
from DiscordMusicBot2 import change_presence

class testCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=discord.Object(GUILD_ID))

    @app_commands.command(name = "join", description = "VCに参加します")
    @app_commands.guilds(GUILD_ID)
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("VCに接続されていません", ephemeral=True)
            return
        
        await interaction.user.voice.channel.connect()
        await change_presence()
        await interaction.response.send_message("VCに接続しました！", ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(testCommand(bot))