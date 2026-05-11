import yt_dlp
import re

_YDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'skip_download': True,
}

def search_from_keyword(keyword, limit=5):
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{keyword}", download=False)
    if not info:
        return []
    return [e for e in info.get('entries', []) if e]

def search_from_url(url):
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        return ydl.extract_info(url, download=False)

def get_url(result, key):
    entry = result[key]
    return f"https://www.youtube.com/watch?v={entry['id']}"

def get_title(result, key):
    return result[key]['title']

def is_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=|playlist\?list=|user/|channel/|c/)?([^&=%\?]{11})?'
    )
    return youtube_regex.match(url) is not None

def get_video_match(url):
    video_id_pattern = re.compile(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    return video_id_pattern.search(url)

def get_video_id(video_match):
    return video_match.group(1)

def get_playlist_match(url):
    playlist_id_pattern = re.compile(r'(?:list=)([0-9A-Za-z_-]+).*')
    return playlist_id_pattern.search(url)

def get_playlist_id(playlist_match):
    return playlist_match.group(1)

def get_playlist(playlist_url):
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        return ydl.extract_info(playlist_url, download=False)

def extract_video_url_from_playlist_video(playlist_video_url):
    video_id_pattern = re.compile(r'(v=|\/)([0-9A-Za-z_-]{11})')
    match = video_id_pattern.search(playlist_video_url)

    if match:
        video_id = match.group(2)
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("有効なYouTube動画URLではありません")
