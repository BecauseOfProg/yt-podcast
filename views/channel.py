from utils.get_data import get_channel_data, get_playlist_data
from utils.render_feed import render_feed
from app import app
from flask import request
from g import DOMAIN


@app.route("/user/<user>",          defaults={'id_type': 'user',    'format': 'video'})
@app.route("/channel/<user>",       defaults={'id_type': 'channel', 'format': 'video'})
@app.route("/c/<user>",             defaults={'id_type': 'custom',  'format': 'video'})
@app.route("/user/<user>/audio",    defaults={'id_type': 'user',    'format': 'audio'})
@app.route("/channel/<user>/audio", defaults={'id_type': 'channel', 'format': 'audio'})
@app.route("/c/<user>/audio",       defaults={'id_type': 'custom',  'format': 'audio'})
def user(id_type, user, format):
    '''Generate a feed for a channel or user or custom URL'''
    channel_data = get_channel_data(id_type, user)

    try:
        uploads = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except IndexError:
        error = "It appears that "+user+" is not a valid "+id_type+"."
        return error

    uploads_data = get_playlist_data(uploads)
    return render_feed(uploads_data, channel_data, format)


@app.route("/playlist/<playlist_id>", defaults={'format': 'video'})
@app.route("/playlist/<playlist_id>/audio", defaults={'format': 'audio'})
@app.route("/playlist", defaults={'format': None, 'playlist_id': None})
def playlist(playlist_id, format):
    '''Generate a feed for a channel'''
    if playlist_id is None:
        playlist_id = request.args.get('list', '')
    if format is None:
        format = 'audio' if 'a' in request.args.to_dict() else 'video'

    try:
        playlist_data = get_playlist_data(playlist_id)
    except:
        error = "It appears that "+playlist_id+" is not a valid playlist."
        return error

    channel_id = playlist_data['items'][0]['snippet']['channelId']
    channel_data = get_channel_data('channel', channel_id)
    return render_feed(playlist_data, channel_data, format)
