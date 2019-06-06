from lib.data import auth
from lib.data import search


def main():
    token = auth.get_token()
    query = input('Search for a track: ')

    search_results = search.search_track(token, query)

    index = 1
    for item in search_results['tracks']['items']:
        print(str(index) + ": " + item['name'] + \
              " - " + item['album']['artists'][0]['name'])
        index += 1

    print()

    track_index = int(input('Please enter the number to a track: '))
    while track_index not in range(1, index):
        track_index = int(input('Please enter the number to a track: '))

    track_id = search_results['tracks']['items'][track_index - 1]['id']

    track_analysis = search.search_track_analysis(token, track_id)
    track_features = search.search_track_features(token, track_id)


if __name__ == '__main__':
    main()
