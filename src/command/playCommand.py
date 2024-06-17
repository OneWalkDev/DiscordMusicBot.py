import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands
from config.Config import GUILD_ID
from DiscordMusicBot2 import change_presence
from service.YoutubeService import search, get_url, get_title
import service.AudioService as AudioService
from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException


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
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        except(
            AlreadyJoinedException
        ) as e:
            pass
        
        await interaction.response.defer(ephemeral=True)
        await change_presence(self.bot)
        if interaction.guild.voice_client.is_playing():
            await interaction.response.send_message("再生中です...", ephemeral=True)
            return
        search_result = search(song_name)
        url = get_url(search_result, 0)
        title = get_title(search_result, 0)

        await interaction.channel.send(f"追加 >> {title}")

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            secret = url
            info = ydl.extract_info(secret, download=False)
            url2 = info['url']
            print(url2)
            source = discord.FFmpegPCMAudio(url2)
            vc = interaction.guild.voice_client
            await vc.play(source)
        await interaction.response.send_message("再生しました!", ephemeral=True)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(playCommand(bot))