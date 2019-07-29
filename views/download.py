from flask import redirect
from app import app
# import pafy
import youtube_dl
import pytube

BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='


@app.route("/download/<media_type>/<video_id>.<suffix>")
def stream_url(media_type, video_id, suffix):
    '''Redirect for media download'''

    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(video_id, download=False)

    if media_type == 'audio':
        return redirect(meta['formats'][0]['url'])
        # audio_format['url'] also works

    else:
        # return redirect(meta['formats'][1]['url'])
        if meta.get('requested_formats') is not None:
            video_format = meta['requested_formats']
            print(video_format)
            return # return redirect(video_format[0]['url'])  # but there is no sound
        else:
            return redirect(meta['url'])

    # else:
    #     stream = video.getbest(preftype="mp4")
    # if meta.get('requested_formats') is not None:
    #     # we got DASH formats
    #     video_format, audio_format = meta['requested_formats']
    #     video_url = video_format['url']
    #     audio_url = audio_format['url']
    # else:
    #     video_url = meta['url']

    # return redirect(video_url)
