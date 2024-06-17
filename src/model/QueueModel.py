class Queue():

    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.queue = []
        self.loop = False
        self.queue_loop = False
        self.shuffle = False

