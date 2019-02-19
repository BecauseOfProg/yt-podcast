from flask import redirect
from app import app
import pafy

BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='


@app.route("/download/<media_type>/<video_id>.<suffix>")
def stream_url(media_type, video_id, suffix):
    '''Redirect for media download'''
    video = pafy.new(BASE_VIDEO_URL + video_id)
    if media_type == 'audio':
        stream = video.getbestaudio(preftype="m4a")
    else:
        stream = video.getbest(preftype="mp4")

    return redirect(stream.url)
