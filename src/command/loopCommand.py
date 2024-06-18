import discord
import datetime
from discord import app_commands
from discord.ext import commands
from service.AudioService import loop

class loopCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "loop", description = "1曲ループを設定します")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.voice is None:
            embed = discord.Embed(title="エラー",description="あなた自身がVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)

        if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
            embed = discord.Embed(title="エラー",description="botがVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        setting_loop = loop(interaction.guild)

        if setting_loop:
            setting_loop_str = "オン"
        else:
            setting_loop_str = "オフ"

        embed = discord.Embed(
            title="設定",
            description=f"{interaction.user.name}が1曲ループを{setting_loop_str}にしました",
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(f"1曲ループを{setting_loop_str}にしました")
        await interaction.channel.send(embed=embed)

            
async def setup(bot: commands.Bot):
    await bot.add_cog(loopCommand(bot))