from urllib.parse import urlencode
from g import KEY
import requests

# Youtube API URLs
ENDPOINT = 'https://www.googleapis.com/youtube/v3/'


def yt_api_call(path, part, id_type, id_value):
    """Make a call to the Youtube API."""

    params = {'key': KEY,
              id_type: id_value,
              'part': part,
              'maxResults': 50}

    data_url = (ENDPOINT + path + '?' + urlencode(params))

    r = requests.get(data_url)
    data = r.json()
    return data
