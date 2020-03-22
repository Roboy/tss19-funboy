import requests

import logging as logger

CONFIG = {
    'SERVER_ADDRESS': 'http://localhost',
    'SERVER_PORT': 5050
}


class Joker:
    address = f"{CONFIG['SERVER_ADDRESS']}:{CONFIG['SERVER_PORT']}"

    def render(self, types):
        if not server_up(self.address):
            logger.error(
                "\n--------"
                "\nThe server does not seem to be running!"
                "\n--------")
            return ""

        types = ", ".join(types)
        params = {
            'types': types,
            'utterance': " "
        }
        response = requests.get(self.address, params=params)
        response_json = response.json()
        logger.info(response_json)
        sample = response_json['response'].strip()
        logger.info(f"CLASS TOKENS: {types} | RESPONSE: {sample} |")
        return sample


def server_up(server_address):
    try:
        status = requests.head(server_address).status_code
    except requests.exceptions.RequestException or requests.exceptions.ConnectionError:
        status = None
    return status == 200