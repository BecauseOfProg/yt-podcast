from utils.youtube_api_call import yt_api_call


def get_channel_data(id_type, user):
    '''Return a dictionary of channel data from a channel id, username or custom URL.'''
    if id_type == 'custom':
        guess_channel = yt_api_call(
            path      = 'search',
            part      = 'snippet',
            id_type   = 'q',
            id_value  = user
        )

        # Get first response and prepare classical route
        user = guess_channel.items[0].id.channelId
        id_type = 'channel'

    id_type = 'id' if id_type == 'channel' else 'forUsername'

    channel_data = yt_api_call(
        'channels', 'contentDetails,snippet', id_type, user
    )

    return channel_data


def get_playlist_data(playlist_id):
    '''Return a dictionary of playlist data from a playlist id.'''
    playlist_data = yt_api_call(
        'playlistItems', 'snippet', 'playlistId', playlist_id)
    return playlist_data
