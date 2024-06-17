class AudioModel:
    def __init__(self, name, url):
        self.__name = name
        self.__url = url

    def get_name(self):
        return self.__name
    
    def get_url(self):
        return self.__url