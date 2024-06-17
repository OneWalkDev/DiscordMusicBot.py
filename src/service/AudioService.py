from exception.MusicBotException import AlreadyJoinedException, UserNotJoinedException

async def join(interaction):
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    
    if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
        raise AlreadyJoinedException()
        
    await interaction.user.voice.channel.connect()

