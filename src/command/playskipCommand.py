import discord
import datetime
from discord import app_commands
from discord.ext import commands
from DiscordMusicBot2 import change_presence
from utils.YoutubeUtils import *
from exception.MusicBotException import MusicInQueueNotFoundException
from model.AudioModel import AudioModel
from service.AudioService import add_queue, check_permission
from exception.MusicBotException import *

class playskipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "playskip", description = "キューの一番最初に曲を追加します")
    async def playskip(self, interaction: discord.Interaction, song_name:str):
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
        
        await change_presence(self.bot)

        if not is_youtube_url(song_name):
            await self.add_video(interaction, song_name)

        video_match = get_video_match(song_name)
        playlist_match = get_playlist_match(song_name)
        if video_match:
            video_id = get_video_id(video_match)
            await self.add_video(interaction, video_id)
        elif playlist_match:
            await interaction.followup.send(f"プレイリストは追加できません")
            pass

    async def add_video(self, interaction: discord.Interaction, song_name:str):
        search_result = search_from_keyword(song_name)
        if(len(search_result) == 0):
            await interaction.followup.send("検索結果が存在しませんでした。見つからない場合はURLを指定してください", ephemeral=True)
            return 
        
        url = get_url(search_result, 0)
        title = get_title(search_result, 0)

        audio_model = AudioModel(title, url)
        
        embed = discord.Embed(
            title=f"{interaction.user.name}が追加",
            description=title,
            color=0x3ded97,
            timestamp=datetime.datetime.now()
        )

        await interaction.followup.send(f"追加しました！")
        await interaction.channel.send(embed=embed)
        await add_queue(interaction.guild, audio_model, self.bot, True)

async def setup(bot: commands.Bot):
    await bot.add_cog(playskipCommand(bot))