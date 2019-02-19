from utils.youtube_api_call import yt_api_call


def get_channel_data(id_type, user):
    '''Return a dictionary of channel data from a channel id or username.'''
    id_type = 'id' if id_type == 'channel' else 'forUsername'
    channel_data = yt_api_call('channels', 'contentDetails,snippet', id_type, user)
    return channel_data


def get_playlist_data(playlist_id):
    '''Return a dictionary of playlist data from a playlist id.'''
    playlist_data = yt_api_call('playlistItems', 'snippet', 'playlistId', playlist_id)
    return playlist_data
