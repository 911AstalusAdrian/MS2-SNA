import base64
import requests
import datetime
from urllib.parse import urlencode

# client_id = 'ba85cdc0478c4a2ab28221b17c89354b'
# client_secret = 'd101ba0ee42f491c883f9918d62114b8'

# client_creds = f"{client_id}:{client_secret}"
# client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

# token_url = 'https://accounts.spotify.com/api/token'
# token_data = {
#     'grant_type' : 'client_credentials'
# }
# token_headers = {
#     'Authorization' : f'Basic {client_creds_b64}'
# }

# req = requests.post(token_url, data=token_data, headers=token_headers)
# token_response_data = req.json()
# access_token = token_response_data['access_token']
# # Nice to have: script that each hour refreshes the access token
# print(access_token)



access_token = 'BQC4DBD9tPaSRWebyEHWkVp72bJvOunqbj-PIs6pSxcNBJFu4XgGOxuQS2dO_dXmYZ3vHuWDTUS2j6hxQODX8RhtReuuwiekwUQeHL5DR0Rv4dTyicI'

headers = {
    'Authorization':f'Bearer {access_token}'
}

endpoint = 'https://api.spotify.com/v1/search'
offset = 0
artist_id = 1

for i in range(25):
    data = urlencode({
    'q' : 'year:2023',
    'type' : 'artist',
    'market' : 'US',
    'limit': '20', 
    'offset': offset
    })

    lookup = f'{endpoint}?{data}' # ok
    print(f"Lookup for loop {i}: {lookup}")

    try:

        r = requests.get(lookup, headers=headers)
        response_json = r.json()
        print(f"Next URL: {response_json['artists']['next']}\n\n")
        artists = response_json['artists']['items']
        for artist in artists:
            print(f"{artist_id})  Artist name: {artist['name']}, Artist id: {artist['id']}")
            artist_id += 1

        offset += 20
    except:
        offset += 20
        continue






