from utils.youtube_api_call import yt_api_call


def get_channel_data(id_type, user):
    '''Return a dictionary of channel data from a channel id, username or custom URL.'''
    if id_type == 'custom':
        # Search channels that might have custom part of URL in the snippet
        guess_channel = yt_api_call(
            path      = 'search',
            part      = 'snippet',
            id_type   = 'q',
            id_value  = user
        )

        # Get only returned channel IDs
        cIDs = [item['id']['channelId'] for item in guess_channel['items']]

        # Get more details of all returned channels
        guess_channel = yt_api_call(
            path      = 'channels',
            part      = 'snippet',
            id_type   = 'id',
            id_value  = ','.join(cIDs)
        )

        # Search for exact customUrl match in all channel details and set user variable
        for item in guess_channel['items']:
            if "customUrl" in item['snippet']:
                if ('@' + user).casefold()==item['snippet']["customUrl"].casefold():
                    user = item['id']
                    break

        # Variable user now has a channel ID; prepare for classical route
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
