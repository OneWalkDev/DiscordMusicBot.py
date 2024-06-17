from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException
import yt_dlp
import discord

async def join(interaction):
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    
    if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
        raise AlreadyJoinedException()
        
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

def skip():
    #TODO
    pass

