import discord
import datetime
from discord import app_commands
from discord.ext import commands
from service.AudioService import skip, check_permission
from exception.MusicBotException import *

class skipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "skip", description = "音楽をスキップします")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            check_permission(interaction)
        except(
            UserNotJoinedException,
            NotJoinedException,
            NotSameVoiceChannelException
        ) as e:
            embed = discord.Embed(title="エラー", description=e, color=0xff1100)
            await interaction.followup.send(embed=embed)
            return
        
        await skip(interaction.guild)

        embed = discord.Embed(
            title="スキップ",
            description=f"{interaction.user.name}が曲をスキップ",
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(f"曲をスキップしました！")
        await interaction.channel.send(embed=embed)

            
async def setup(bot: commands.Bot):
    await bot.add_cog(skipCommand(bot))