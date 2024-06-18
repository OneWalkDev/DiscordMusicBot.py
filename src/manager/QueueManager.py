from model.QueueModel import QueueModel

class QueueManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QueueManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__container = {} 
        return cls._instance

    def register_queue(self, guild_id, queue: QueueModel):
        self.__container[guild_id] = queue

    def get_queue(self, guild_id):
        return self.__container.get(guild_id)
    
    def remove_queue(self, guild_id):
        return self.__container.pop(guild_id)
    
    def is_exists_queue(self, guild_id):
        return guild_id in self.__container

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.__container = {}
        return cls._instance