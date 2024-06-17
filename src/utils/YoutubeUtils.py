from youtubesearchpython import VideosSearch

def search(keyword, limit = 5):
    videosSearch = VideosSearch(keyword, limit = limit)
    return videosSearch.result()

def get_url(result, key):
    return result["result"][key]["link"]

def get_title(result, key):
    return result["result"][key]["title"]