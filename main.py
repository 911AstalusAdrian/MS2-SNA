import base64
import requests
import datetime

client_id = 'ba85cdc0478c4a2ab28221b17c89354b'
client_secret = 'd101ba0ee42f491c883f9918d62114b8'

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type' : 'client_credentials'
}
token_headers = {
    'Authorization' : f'Basic {client_creds_b64}'
}

req = requests.post(token_url, data=token_data, headers=token_headers)
token_response_data = req.json()
access_token = token_response_data['access_token']

# print(req.status_code)
print(access_token)

