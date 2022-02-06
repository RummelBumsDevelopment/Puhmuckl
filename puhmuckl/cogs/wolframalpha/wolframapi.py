import requests
import logging
from util import config

class WolframResponse:
    API_ENDPOINT = "http://api.wolframalpha.com/v2/query?appid={0}&input={1}"

    def __init__(self, query: str):
        self.query = query
        self.send()

    def send(self):
        response = requests.get(
            WolframResponse.API_ENDPOINT.format(config.get_auth_config('wolframalpha'), self.query)
        )
        logging.debug(response.text)