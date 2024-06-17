INITIAL_EXTENSIONS = [
    'command.joinCommand',
    'command.playCommand'
]

async def load_extension(bot):
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)