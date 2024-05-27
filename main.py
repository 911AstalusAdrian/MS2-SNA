import os
import json
import requests
import csv
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


def clean_feature_list(feature_list):
    flat_list = [feature for sublist in feature_list for feature in sublist]
    unique_list = set(flat_list)
    return list(unique_list)


def get_artist_features(artist_name):
    features = []
    songs = get_artist_songs(artist_name)
    for song in songs:
        song_features = get_song_features(song['artists'])
        if artist_name in song_features:
            song_features.remove(artist_name)
        features.append(song_features)

    features = clean_feature_list(features)

    return features


def get_artist_feature_tuples(artist, feature_list, file):
    tuple_list = []
    artist_number = file[artist]['number']
    for each_feature in feature_list:
        if each_feature in file.keys():
            tuple_list.append((artist_number, file[each_feature]['number']))
    return tuple_list


def clean_tuples(tuple_list):
    unique_pairs = set()
    unique_list = []

    for a, b in tuple_list:
        pair = tuple(sorted((a, b)))
        if pair not in unique_pairs:
            unique_pairs.add(pair)
            unique_list.append(pair)

    return unique_list


def save_to_csv(tuple_list, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ArtistA', 'ArtistB'])
        for tup in tuple_list:
            writer.writerow(tup)


if __name__ == '__main__':
    all_feature_tuples = []
    json_path = 'data/artist_data.json'
    csv_path = 'data/data.csv'
    secrets = Secrets()

    if os.path.getsize(json_path) == 0:
        artists = fetch_500_artists()
        save_artists(artists, json_path)
    else:
        artists = load_artists(json_path)

    for artist_name, artist_data in artists.items():
        artist_features = get_artist_features(artist_name)
        features_tuples = get_artist_feature_tuples(artist_name, artist_features, artists)
        print(f'Checking on {artist_name}...')
        all_feature_tuples += features_tuples

    print(len(all_feature_tuples))
    cleaned_feature_tuples = clean_tuples(all_feature_tuples)
    save_to_csv(cleaned_feature_tuples, csv_path)
