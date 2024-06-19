import discord
from discord import app_commands
from discord.ext import commands
from utils.YoutubeUtils import *
from service.AudioService import delete, check_permission
from exception.MusicBotException import *
import datetime

class deleteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "delete", description = "キューから音楽を削除します。")
    @app_commands.describe(queue_id="/queueで表示される番号を入力してください")
    async def delete(self, interaction: discord.Interaction, queue_id:int):
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
        
        try:
            delete_audio = delete(interaction.guild, queue_id)
            embed = discord.Embed(
                title="削除",
                description=f"{interaction.user.name}が「{delete_audio.get_title()}」を削除しました！",
                color=0x3ded97,
                timestamp=datetime.datetime.now()
            )
            await interaction.followup.send(f"「{delete_audio.get_title()}」を削除しました！")
            await interaction.channel.send(embed=embed)
        except(
            ValueError
        ) as e:
            embed = discord.Embed(title="エラー", description=e, color=0xff1100)
            await interaction.followup.send(embed=embed)
            return
        

            
async def setup(bot: commands.Bot):
    await bot.add_cog(deleteCommand(bot))