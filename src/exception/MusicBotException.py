class MusicBotException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class AlreadyJoinedException(MusicBotException):
    def __str__(self):
        return (
            "botがすでにボイスチャットに参加しています。"
        )
    
class UserNotJoinedException(MusicBotException):
    def __str__(self):
        return (
            "ユーザーがボイスチャットに接続されていません"
        )
    
class NotJoinedException(MusicBotException):
    def __str__(self) -> str:
        return (
            "botがボイスチャットに参加していません。"
        )
    
class MusicInQueueNotFoundException(MusicBotException):
    def __str__(self) -> str:
        return (
            "キューに曲が存在しません"
        )