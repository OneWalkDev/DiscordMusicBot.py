INITIAL_EXTENSIONS = [
    'command.deleteCommand',
    'command.joinCommand',
    'command.leaveCommand',
    'command.loopCommand',
    'command.playCommand',
    'command.playskipCommand',
    'command.qloopCommand',
    'command.queueCommand',
    'command.shuffleCommand',
    'command.skipCommand',
    'command.statusCommand'
]

async def load_extension(bot):
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)