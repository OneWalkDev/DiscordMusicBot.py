import discord
import datetime
from discord import app_commands
from discord.ext import commands
from service.AudioService import shuffle, check_permission
from exception.MusicBotException import *

class shuffleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "shuffle", description = "シャッフルを設定します")
    async def shuffle(self, interaction: discord.Interaction):
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
        
        setting_loop = shuffle(interaction.guild)

        if setting_loop:
            setting_loop_str = "オン"
        else:
            setting_loop_str = "オフ"

        embed = discord.Embed(
            title="設定",
            description=f"{interaction.user.name}がキューループを{setting_loop_str}にしました",
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(f"キューループを{setting_loop_str}にしました")
        await interaction.channel.send(embed=embed)

            
async def setup(bot: commands.Bot):
    await bot.add_cog(shuffleCommand(bot))