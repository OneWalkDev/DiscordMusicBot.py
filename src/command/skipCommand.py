import discord
import datetime
from discord import app_commands
from discord.ext import commands
from service.AudioService import skip

class skipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "skip", description = "音楽をスキップします")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.voice is None:
            embed = discord.Embed(title="エラー",description="あなた自身がVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)

        if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
            embed = discord.Embed(title="エラー",description="botがVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        await skip(interaction.guild, self.bot)

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