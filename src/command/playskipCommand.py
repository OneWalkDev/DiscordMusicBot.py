import discord
import datetime
from discord import app_commands
from discord.ext import commands
from DiscordMusicBot2 import change_presence
from utils.YoutubeUtils import search, get_url, get_title
from exception.MusicBotException import MusicInQueueNotFoundException
from model.AudioModel import AudioModel
from service.AudioService import add_queue

class playskipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "playskip", description = "キューの一番最初に曲を追加します")
    async def play(self, interaction: discord.Interaction, song_name:str):
        await interaction.response.defer(ephemeral=True)

        if interaction.user.voice is None:
            embed = discord.Embed(title="エラー",description="あなた自身がVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)

        if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
            embed = discord.Embed(title="エラー",description="botがVCに参加していません",color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        await change_presence(self.bot)

        search_result = search(song_name)
        if(len(search_result) == 0):
            await interaction.followup.send("検索結果が存在しませんでした。見つからない場合はURLを指定してください", ephemeral=True)
            return 
        
        url = get_url(search_result, 0)
        title = get_title(search_result, 0)

        audio_model = AudioModel(title, url)
        
        embed = discord.Embed(
            title=f"{interaction.user.name}がキューの最初に曲を追加",
            description=title,
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(f"キューの最初に曲を追加しました！")
        await interaction.channel.send(embed=embed)
        try:
            await add_queue(interaction.guild, audio_model, self.bot, True)
        except (
            MusicInQueueNotFoundException
        ) as e:
            embed = discord.Embed(title="エラー",description=e,color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
            
async def setup(bot: commands.Bot):
    await bot.add_cog(playskipCommand(bot))