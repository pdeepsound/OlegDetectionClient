import requests
import base64
from typing import Union

import pandas as pd

from od_client.utils.server_utils import client_config
from od_client.utils.recognizer_utils import results_id_to_human


class ODRecognizer:
    """Getting access to the system by token

    Args:
        token: the API token

    """

    def __init__(self, token: str) -> None:
        self.host_port = f"{client_config['host']}:{client_config['port']}"
        url = f'{self.host_port}/check-token'
        self.token = token
        self.token_data = {
            'token': self.token,
        }
        results = requests.post(url, json=self.token_data)
        if results.status_code == 200:
            print("Token is valid")
        else:
            raise ValueError(results.json()['detail'])

    def recognized_seconds_by_token(self):
        """Getting the number of recognized seconds by token

        Returns:
            dict that contains the number of recognized seconds
            for Short Mode (key 'short_mode') and Long Mode (key 'long_mode')
            as well as their sum ('all')

        """
        url = f'{self.host_port}/recognized-seconds-by-token'
        results = requests.post(url, json=self.token_data)
        if results.status_code == 200:
            print("Successfully received the number"
                  "of recognized seconds for the token:")
            recognized_seconds = results.json()
            for key in recognized_seconds.keys():
                recognized_seconds[key] = round(recognized_seconds[key], 2)
            print(f"For Short Mode: {recognized_seconds['short_mode']}\n"
                  f"For Long Mode: {recognized_seconds['long_mode']}\n"
                  f"Overall: {recognized_seconds['all']}")
            return recognized_seconds
        else:
            raise ValueError(results.json()['detail'])

    def token_information(self):
        """Getting information about the token

        Returns:
            dict that contains the owner of the token and expiration date

        """
        url = f'{self.host_port}/token-information'
        results = requests.post(url, json=self.token_data)
        if results.status_code == 200:
            print("Successfully received information about the token")
            token_info = results.json()
            token_info['expires'] = token_info['expires'].split('T')[0]
            print(f"Owner: {token_info['owner']}")
            print(f"Expires: {token_info['expires']}")
            return token_info
        else:
            raise ValueError(results.json()['detail'])

    def recognize(
        self,
        audio_bytes: bytes,
        sr: int,
        dtype: str,
        mode: str = 'short'
    ) -> Union[pd.DataFrame, str, None]:
        """Recognizing audio

        Args:
            audio_bytes: bytes of the audio clip
            sr: sample rate of the audio clip
            dtype: the audio bit depth ('int8' or 'int16' or 'int32')
            mode: recognition mode ('short' or 'long')

        Returns:
            for mode='short':
                str ('oleg' or 'not_oleg')
                    if the audio clip contain speech, else None
            for mode='long':
                pandas.DataFrame (start, end, duration, confidence, results)
                    if the audio clip contain speech, else None

        """
        if mode != 'short' and mode != 'long':
            raise ValueError("Mode must be either 'short' or 'long'")
        url = f'{self.host_port}/recognize'
        decoded_bytes = base64.b64encode(audio_bytes).decode('ascii')
        body = {
            'lenght': mode,
            'token': self.token,
            'audio': decoded_bytes,
            'sr': sr,
            'dtype': dtype,
        }
        results = requests.post(url, json=body)
        if results.status_code == 200:
            results_predict = results.json()
            if mode == 'short' and results_predict['results_id'] != 0:
                return results_id_to_human[results_predict['results_id']]
            elif mode == 'long' and results_predict is not None:
                table = pd.read_json(results.json())
                table['results'] = table.results_id.apply(
                    lambda x: results_id_to_human[x]
                )
                table = table.drop(['results_id'], axis=1)
                return table
            else:
                print("Audio data does not contain speech")
                return None
        else:
            raise ValueError(results.json()['detail'])
