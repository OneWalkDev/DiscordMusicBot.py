from model.AudioModel import AudioModel

class QueueModel():

    def __init__(self, guild_id):
        self.__guild_id = guild_id
        self.__queue = []
        self.__loop = False
        self.__queue_loop = False
        self.__shuffle = False

    def get_guild_id(self):
        return self.__guild_id
    
    def get(self):
        return self.__queue
    
    def add(self, audio_model: AudioModel):
        self.__queue.append(audio_model)

    def remove(self, key):
        return self.__queue.pop(key)

    def get_loop(self):
        return self.__loop
    
    def change_loop(self):
        self.__loop = not self.__loop    

    def get_queue_loop(self):
        return self.__queue_loop
    
    def change_queue_loop(self):
        self.__queue_loop = not self.__queue_loop
    
    def get_shuffle(self):
        return self.__shuffle

    def change_shuffle(self):
        self.__shuffle = not self.__shuffle