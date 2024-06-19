from exception.MusicBotException import *
import yt_dlp
import discord
import asyncio
import random
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

async def leave(interaction):
    if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
        raise NotJoinedException()
    
    queue_manager.remove_queue(interaction.guild.id)
    await interaction.guild.voice_client.disconnect()

async def play(guild, audio_model, bot):
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
            guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(next(guild, bot), bot.loop))

    except Exception as e:
        print(f"Error: {e}")

async def next(guild, bot):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)

    if queue.get_shuffle():
        in_queue = queue.get()
        selected = random.choice(in_queue[1:])
        in_queue.remove(selected)
        in_queue.insert(1, selected)
        
    if queue.get_queue_loop():
        queue.add(queue.get()[0])

    if not queue.get_loop():
        queue.remove(0)

    if len(queue.get()) != 0:
        audio_model = queue.get()[0]
        await play(guild, audio_model, bot)

async def add_queue(guild, audio_model: AudioModel, bot, first = False):
    guild_id = guild.id
    if not queue_manager.is_exists_queue(guild_id):
        queue_manager.register_queue(guild_id, QueueModel(guild_id))
        
    queue = queue_manager.get_queue(guild_id)

    if first:
        if len(queue.get()) == 0:
            raise MusicInQueueNotFoundException()
        queue.insert(audio_model, 1)
        return
    
    if len(queue.get()) == 0:
        await play(guild, audio_model, bot)
    
    queue.add(audio_model)

async def skip(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)
    
    if guild.voice_client.is_playing():
        guild.voice_client.stop()

def delete(guild, queue_id):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    guild_queue = queue_manager.get_queue(guild.id)
    queue = guild_queue.get()

    if 1 <= queue_id < len(queue):
        delete_audio_model = queue[queue_id]
        guild_queue.remove(queue_id)
        return delete_audio_model
    else:
        raise ValueError("キュー番号が存在しません。")
    

def loop(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)
    
    queue.change_loop()
    return queue.get_loop()

def queue_loop(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)
    
    queue.change_queue_loop()
    return queue.get_queue_loop()

def shuffle(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)
    
    queue.change_shuffle()
    return queue.get_shuffle()

def get_status_dict(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id)

    return {
        "shuffle": queue.get_shuffle,
        "loop": queue.get_loop,
        "qloop": queue.get_queue_loop
    }

def check_permission(interaction):
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    elif interaction.guild.voice_client is None or not interaction.guild.voice_client.is_connected():
        raise NotJoinedException()
    elif interaction.user.voice.channel != interaction.guild.voice_client.channel:
        raise NotSameVoiceChannelException()
    
def get_queue(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    return queue_manager.get_queue(guild.id).get()

def get_now_playing_title(guild):
    if not queue_manager.is_exists_queue(guild.id):
        queue_manager.register_queue(guild.id, QueueModel(guild.id))

    queue = queue_manager.get_queue(guild.id).get()

    if len(queue) == 0:
        return "現在再生されているものはありません。"
    
    return queue[0].get_title()
