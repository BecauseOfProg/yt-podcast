from utils.youtube_api_call import yt_api_call
from flask import render_template
from g import DOMAIN
import datetime
import isodate


def render_feed(playlist_data, channel_data, podcast_type):
    '''Render the RSS feed from the playlist data,
    channel data, and desired podcast type (audio or video).'''

    video_ids = [item['snippet']['resourceId']['videoId']
                 for item in playlist_data['items']]
    videos_data = yt_api_call(
        'videos', 'snippet,contentDetails', 'id', ','.join(video_ids))

    for item in videos_data['items']:
        # Reformat publication dates for RSS (RFC 2822)
        date_ISO = item['snippet']['publishedAt']
        d = datetime.datetime.strptime(date_ISO, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_RFC = d.strftime('%a, %d %b %Y %H:%M:%S +0000')
        item['snippet']['publishedAt'] = date_RFC
        # Reformat file duration for iTunes
        duration_iso = item['contentDetails']['duration']
        parsed = isodate.parse_duration(duration_iso)
        item['contentDetails']['duration'] = str(parsed)

    # Add channel data to video data to make single context
    videos_data['channel_data'] = channel_data
    # Add media type
    videos_data['podcast_type'] = podcast_type
    # Add media extension
    videos_data['media_extension'] = 'm4a' if podcast_type == 'audio' else 'mp4'
    return render_template('feed.xml', videos_data=videos_data, DOMAIN=DOMAIN)
