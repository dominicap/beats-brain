import json
import os
import requests
import webbrowser


KEYS_LOCATION = os.path.abspath(os.path.join(__file__, "../.."))

with open(KEYS_LOCATION + '/.keys/keys.json') as keys:
    CLIENT_ID = json.load(keys)['spotify_client_id']

RESPONSE_TYPE = 'code'
REDIRECT_URI  = 'https://spotify.com'


def get_access_token():
    PARAMS = {'client_id': CLIENT_ID,
              'response_type': RESPONSE_TYPE,
              'redirect_uri': REDIRECT_URI}
    URL = 'https://accounts.spotify.com/authorize'

    response = requests.get(url=URL, params=PARAMS)
    webbrowser.open_new(response.url)


get_access_token()
