import discord
import datetime
from discord import app_commands
from discord.ext import commands
from config.Config import GUILD_ID
from DiscordMusicBot2 import change_presence
from utils.YoutubeUtils import search, get_url, get_title
import service.AudioService as AudioService
from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException
from model.AudioModel import AudioModel
from service.AudioService import play

class playCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=discord.Object(GUILD_ID))

    @app_commands.command(name = "play", description = "音楽を再生します")
    @app_commands.describe(song_name="URLか曲名を入力してください")
    @app_commands.guilds(GUILD_ID)
    async def play(self, interaction: discord.Interaction, song_name:str):
        try:
            await AudioService.join(interaction)
        except(
            UserNotJoinedException
        ) as e:
            embed = discord.Embed(title="エラー",description=e,color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        except(
            AlreadyJoinedException
        ) as e:
            pass
        
        await interaction.response.defer(ephemeral=True)
        await change_presence(self.bot)

        search_result = search(song_name)
        if(len(search_result) == 0):
            await interaction.followup.send("検索結果が存在しませんでした。見つからない場合はURLを指定してください", ephemeral=True)
            return 
        
        url = get_url(search_result, 0)
        title = get_title(search_result, 0)

        audio_model = AudioModel(title, url)

        await interaction.followup.send(f"追加しました！")

        embed = discord.Embed(title=f"{interaction.user.name}が追加",description=title,color=0x3ded97, timestamp=datetime.datetime.now())
        await interaction.channel.send(embed=embed, ephemeral=True)
        await play(interaction, audio_model)


            
async def setup(bot: commands.Bot):
    await bot.add_cog(playCommand(bot))