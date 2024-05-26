import os
import json
import requests
from urllib.parse import urlencode

from secrets import Secrets


def load_artists(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []


def save_artists(artists, filename):
    with open(filename, 'w') as file:
        json.dump(artists, file, indent=4)


def add_artist(number, name, spotify_id):
    json_file = 'data/artist_data.json'
    artists = load_artists(json_file)
    artist = {
        'number': number,
        'name': name,
        'spotify_id': spotify_id
    }
    artists.append(artist)
    save_artists(artists, json_file)


def fetch_500_artists():
    artists_list = []
    header = {
        'Authorization': f'Bearer {secrets.get_access_token()}'
    }

    endpoint = 'https://api.spotify.com/v1/search'
    offset = 0
    artist_id = 1

    for i in range(25):
        data = urlencode({
            'q': 'year:2023',
            'type': 'artist',
            'market': 'US',
            'limit': '20',
            'offset': offset
        })
        lookup = f'{endpoint}?{data}'  # ok
        print(f"Lookup for loop {i}: {lookup}")

        try:

            r = requests.get(lookup, headers=header)
            print(f"Response: {r.status_code}")
            response_json = r.json()
            print(f"Next URL: {response_json['artists']['next']}\n\n")
            artists = response_json['artists']['items']
            for artist in artists:
                print(f"Adding {artist['name']} with ID {artist_id}")
                artist_details = {
                    'number': artist_id,
                    'name': artist['name'],
                    'spotify_id': artist['id']
                }
                artists_list.append(artist_details)
                artist_id += 1

            offset += 20
        except:
            offset += 20
            continue

    return artists_list


if __name__ == '__main__':
    secrets = Secrets()
    artists = fetch_500_artists()
    # print(artists)
    save_artists(artists, 'data/artist_data.json')
