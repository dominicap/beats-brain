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
