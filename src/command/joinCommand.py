import discord
from discord import app_commands
from discord.ext import commands
from config.Config import GUILD_ID
from DiscordMusicBot2 import change_presence
import service.AudioService as AudioService
from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException

class testCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=discord.Object(GUILD_ID))

    @app_commands.command(name = "join", description = "VCに参加します")
    @app_commands.guilds(GUILD_ID)
    async def join(self, interaction: discord.Interaction):
        try:
            await AudioService.join(interaction)
        except(
            AlreadyJoinedException,
            UserNotJoinedException
        ) as e:
            embed = discord.Embed(title="エラー",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await change_presence(self.bot)
        embed = discord.Embed(title="成功",description="接続しました",color=0x3ded97)
        await interaction.response.send_message(embed=embed, ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(testCommand(bot))