from flask import redirect
from app import app

import youtube_dl

ydl_opts_audio = {
    'verbose': False,
    'format': '140/best',
    'outtmpl': '%(id)s%(ext)s'
}

ydl_opts_video = {
    'verbose': False,
    'format': '22/best',
    'outtmpl': '%(id)s%(ext)s'
}

BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='
API_URL = "https://panel.becauseofprog.fr/youtube-dl/download?url="
FORMAT_VIDEO = "&format=best%5Bprotocol%3Dhttps%5D%2Fbest%5Bprotocol%3Dhttp%5D"
FORMAT_AUDIO = "&format=bestaudio[ext=m4a]"

@app.route("/download/<media_type>/<video_id>.<suffix>")
def stream_url(media_type, video_id, suffix):
    '''Redirect for media download'''
    if media_type == 'video':
        r = API_URL + BASE_VIDEO_URL + video_id + FORMAT_VIDEO
    elif media_type == "audio":
        r = API_URL + BASE_VIDEO_URL + video_id + FORMAT_AUDIO
    else:
        return("Unsupported format.")

    return redirect(r)

@app.route("/youtube-dl/<media_type>/<video_id>.<suffix>")
def yt_dl(media_type, video_id, suffix):
    '''Redirect for media download'''

    if media_type == 'video':
        with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
            result = ydl.extract_info(video_id, download=False)
        r = result['url']

        
    elif media_type == "audio":
        with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
            result = ydl.extract_info(video_id, download=False)
        r = result['url']
    else:
        return("Unsupported format.")

    return redirect(r)
