import base64
import requests


class Secrets:
    def __init__(self):
        self.__client_id = 'ba85cdc0478c4a2ab28221b17c89354b'
        self.__client_secret = 'd101ba0ee42f491c883f9918d62114b8'

        self.__client_credentials = f"{self.__client_id}:{self.__client_secret}"
        self.__client_credentials_b64 = base64.b64encode(self.__client_credentials.encode()).decode()

        self.__token_url = 'https://accounts.spotify.com/api/token'
        self.__token_data = {
            'grant_type': 'client_credentials'
        }
        self.__token_headers = {
            'Authorization': f'Basic {self.__client_credentials_b64}'
        }
        self.__access_token = self.__fetch_access_token()

    def __fetch_access_token(self):
        req = requests.post(self.__token_url, data=self.__token_data, headers=self.__token_headers)
        response_data = req.json()
        return response_data['access_token']

    def __set_access_token(self):
        print('Setting access token')
        self.__access_token = self.__fetch_access_token()

    def refresh_access_token(self):
        self.__fetch_access_token()

    def get_access_token(self):
        return self.__access_token
