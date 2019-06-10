import requests


def search_track(token, query, limit=10):
    if token:
        headers = {'Authorization': "Bearer " + token}
        payload = {'q': query,
                   'limit': limit,
                   'type': 'track'}
        url = 'https://api.spotify.com/v1/search'

        response = requests.get(url=url, params=payload, headers=headers)
        return response.json()


def search_track(token, track_id):
    if token:
        headers = {'Authorization': "Bearer " + token}
        url = 'https://api.spotify.com/v1/tracks/' + track_id

        response = requests.get(url=url, headers=headers)
        return response.json()


def search_track_analysis(token, track_id):
    if token:
        headers = {'Authorization': "Bearer " + token}
        url = "https://api.spotify.com/v1/audio-analysis/" + track_id

        response = requests.get(url=url, headers=headers)
        return response.json()


def search_track_features(token, track_id):
    if token:
        headers = {'Authorization': "Bearer " + token}
        url = "https://api.spotify.com/v1/audio-features/" + track_id

        response = requests.get(url=url, headers=headers)
        return response.json()


def search_artist_analysis(token, artist_id):
    if token:
        headers = {'Authorization': "Bearer " + token}
        url = "https://api.spotify.com/v1/artists/" + artist_id

        response = requests.get(url=url, headers=headers)
        return response.json()


def search_artist_genres(token, track_id):
    analysis = search_track(token, track_id)
    # Finish this
