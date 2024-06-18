from exception.MusicBotException import *
import yt_dlp
import discord
from manager.QueueManager import QueueManager
from model.AudioModel import AudioModel
from model.QueueModel import QueueModel

queue_manager = QueueManager.get_instance()

async def join(interaction):
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    
    if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
        raise AlreadyJoinedException()
    
    queue_manager.register_queue(interaction.guild.id, QueueModel(interaction.guild.id))
    await interaction.user.voice.channel.connect()

async def play(voice_client, audio_model):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    }

    url = audio_model.get_url()

    print(url)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            url2 = info_dict['url'] if 'url' in info_dict else info_dict['formats'][0]['url']
            print(url2)

            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }

            source = discord.FFmpegPCMAudio(url2, **ffmpeg_options)
            source = discord.PCMVolumeTransformer(source, volume=1.0)
            voice_client.play(source)
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False


async def add_queue(guild, audio_model: AudioModel):
    guild_id = guild.id
    if not queue_manager.is_exists_queue(guild_id):
        queue_manager.register_queue(guild_id, QueueModel(guild_id))
        
    queue = queue_manager.get_queue(guild_id)
    
    if len(queue.get()) == 0:
        await play(guild.voice_client, audio_model)

    queue.add(audio_model)

