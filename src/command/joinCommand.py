import discord
from discord import app_commands
from discord.ext import commands

from DiscordMusicBot2 import change_presence
import service.AudioService as AudioService
from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException

class joinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "join", description = "VCに参加します")
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
    await bot.add_cog(joinCommand(bot))