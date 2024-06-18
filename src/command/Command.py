INITIAL_EXTENSIONS = [
    'command.joinCommand',
    'command.playCommand',
    'command.leaveCommand',
    'command.skipCommand',
    'command.loopCommand',
    'command.playskipCommand',
    'command.shuffleCommand'
]

async def load_extension(bot):
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)