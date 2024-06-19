import discord
import datetime
from discord import app_commands
from discord.ext import commands
from service.AudioService import get_status_dict, check_permission
from exception.MusicBotException import *

class statusCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "status", description = "現在の設定状況を確認します")
    async def play(self, interaction: discord.Interaction):
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
        
        status = get_status_dict(interaction.guild)

        description =  "シャッフル: {}\n".format('オン' if status['shuffle'] == True else 'オフ')
        description += "ループ: {}\n".format('オン' if status['loop'] == True else 'オフ')
        description += "キューループ: {}\n".format('オン' if status['qloop'] == True else 'オフ')

        embed = discord.Embed(
            title="現在の設定",
            description=description,
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(embed=embed)


            
async def setup(bot: commands.Bot):
    await bot.add_cog(statusCommand(bot))