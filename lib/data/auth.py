import json
import os
import sys

import spotipy
import spotipy.util as util

library = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(library)

import util.keys as keys


def get_token():
    client_id = keys.KEYS['spotify_client_id']
    client_secret = keys.KEYS['spotify_client_secret']

    username = input("Enter your Spotify user name: ")
    redirect_uri = 'https://spotify.com'

    token = util.prompt_for_user_token(username=username,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)

    return token
