from flask import redirect
from app import app

import yt_dlp as youtube_dl

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

@app.route("/download/<media_type>/<video_id>.<suffix>")
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
