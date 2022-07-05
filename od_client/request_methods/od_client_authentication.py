import requests
from typing import Union, List, Dict

from od_client.utils.server_utils import client_config


class ODAuthentication:
    """Authentication by username and password

    Args:
        username: the username of user that was provided
        password: the password of user that was provided

    """

    def __init__(self, username: str, password: str) -> None:
        self.host_port = f"{client_config['host']}:{client_config['port']}"
        url = f'{self.host_port}/sign-in'
        self.username = username
        self.password = password
        self.user_data = {
            'username': self.username,
            'password': self.password,
        }
        results = requests.post(url, json=self.user_data)
        if results.status_code == 200:
            print(f"Successfully signed-in with username {username}")
        else:
            raise ValueError(results.json()['detail'])

    def new_token(self) -> Union[Dict[str, str], None]:
        """Getting a new token

        Returns:
            dict that contains token and its expiration date

        """
        url = f'{self.host_port}/new-token'
        results = requests.post(url, json=self.user_data)
        if results.status_code == 200:
            token = results.json()
            print(f"Successfully received a new token: {token['token']} "
                  f"that expires {token['expires'].split('T')[0]}")
            return {
                'token': token['token'],
                'expires': token['expires'].split('T')[0]
            }
        else:
            raise ValueError(results.json()['detail'])

    def all_tokens(self) -> Union[List[Dict[str, str]], None]:
        """Getting information all tokens that belong to user

        Returns:
            list that contains tokens and their expiration date

        """
        url = f'{self.host_port}/my-tokens'
        results = requests.post(url, json=self.user_data)
        if results.status_code == 200:
            print("Successfully received all tokens")
            tokens = results.json()['tokens']
            tokens = [
                {
                    'token': token_info['token'],
                    'expires': token_info['expires'].split('T')[0]
                } for token_info in tokens
            ]
            return tokens
        else:
            raise ValueError(results.json()['detail'])

    def recognized_seconds_by_user(
        self,
        date: str = 'month'
    ) -> Union[Dict[str, float], None]:
        """Getting the number of recognized seconds by user

        Returns:
            dict that contains the number of recognized seconds
            for Short Mode (key 'short_mode') and Long Mode (key 'long_mode')
            as well as their sum ('all')

        """
        if date != 'month' and date != 'all':
            raise ValueError("Date must be either 'month' or 'all'")
        url = f'{self.host_port}/recognized-seconds-by-user'
        body = self.user_data.copy()
        body['type'] = date
        results = requests.post(url, json=body)
        if results.status_code == 200:
            if date == 'month':
                print("Successfully received the number"
                      "of recognized seconds for the last month:")
            else:
                print("Successfully received the number"
                      "of recognized seconds for all period:")
            recognized_seconds = results.json()
            for key in recognized_seconds.keys():
                recognized_seconds[key] = round(recognized_seconds[key], 2)
            print(f"For Short Mode: {recognized_seconds['short_mode']}\n"
                  f"For Long Mode: {recognized_seconds['long_mode']}\n"
                  f"Overall: {recognized_seconds['all']}")
            return recognized_seconds
        else:
            raise ValueError(results.json()['detail'])
