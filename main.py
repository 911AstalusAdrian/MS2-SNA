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
    artists_list = {}
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
            response_json = r.json()
            print(f"Next URL: {response_json['artists']['next']}\n\n")
            artists = response_json['artists']['items']
            for artist in artists:
                print(f"Adding {artist['name']} with ID {artist_id}")
                artist_details = {
                    'number': artist_id,
                    'spotify_id': artist['id']
                }
                artists_list[f"{artist['name']}"] = artist_details
                # artists_list.append(artist_details)
                artist_id += 1

            offset += 20
        except:
            offset += 20
            continue

    return artists_list


def get_song_features(features):
    feature_names = []
    for feature in features:
        feature_names.append(feature['name'])
    return feature_names


def get_song_names(songs):
    for song in songs:
        artists = get_song_features(song['artists'])
        print(f"{song['name']} - {artists}")


def get_artist_songs(artist_name):
    header = {
        'Authorization': f'Bearer {secrets.get_access_token()}'
    }
    endpoint = 'https://api.spotify.com/v1/search'
    data = urlencode({
        'q': f'artist:{artist_name}',
        'type': 'track',
        'limit': '50'
    })
    lookup = f'{endpoint}?{data}'

    request = requests.get(lookup, headers=header)
    json_response = request.json()
    return json_response['tracks']['items']


def get_artist_features(artist_name):
    features = []
    songs = get_artist_songs(artist_name)
    for song in songs:
        song_features = get_song_features(song['artists'])
        song_features.remove(artist_name)
        features.append(song_features)
    return features


if __name__ == '__main__':

    artist = 'Drake'

    json_path = 'data/artist_data.json'
    secrets = Secrets()

    if os.path.getsize(json_path) == 0:
        artists = fetch_500_artists()
        save_artists(artists, json_path)
    else:
        artists = load_artists(json_path)

    drake_songs = get_artist_songs(artist)
    artist_features = get_artist_features(artist)

    artist_id = artists[artist]['number']

    for artist_feature in artist_features:
        print(artist_feature)
        '''
        Check if each artist_feature not empty
        Parse artist_feature
        for each element, get the id
        create a tuple with artist_id
        save tuple
        '''

