from flask import redirect
from app import app

BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='
API_URL = "https://panel.becauseofprog.fr/youtube-dl/download?"
FORMAT_VIDEO = "&format=best%5Bprotocol%3Dhttps%5D%2Fbest%5Bprotocol%3Dhttp%5D"
FORMAT_AUDIO = ""

@app.route("/download/<media_type>/<video_id>.<suffix>")
def stream_url(media_type, video_id, suffix):
    '''Redirect for media download'''
    if media_type == 'video':
        r = API_URL + BASE_VIDEO_URL + video_id + FORMAT_VIDEO
    elif media_type = "audio":
        r = API_URL + BASE_VIDEO_URL + video_id + FORMAT_VIDEO
    else:
        return("Format non pris en charge.")

    return redirect(r)