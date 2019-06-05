import requests

from pprint import pprint

from lib.data import auth
from lib.data import search


def main():
    token = auth.get_token()
    query = input('Please enter a track name: ')

    results = search.search_track(token, query)


if __name__ == '__main__':
    main()
