#!/usr/bin/env python3
import re

import fire
import requests

import logging as logger

CONFIG = {
    'SERVER_ADDRESS': 'http://localhost',
    'SERVER_PORT': 5050
}


def interact():
    """
    Interactively call the model's server
    """

    address = f"{CONFIG['SERVER_ADDRESS']}:{CONFIG['SERVER_PORT']}"

    while True:

        raw_text = input("Model prompt >>> ")
        while not raw_text:
            print('Prompt should not be empty!')
            raw_text = input("Model prompt >>> ")

        if not server_up(address):
            logger.error(
                "\n--------"
                "\nThe server does not seem to be running!"
                "\n--------")
            break

        logger.info(raw_text)
        types = re.findall('\|(.+?)\|', raw_text)
        if len(types) == 0:
            types = ['short']
        types = ", ".join(types)
        if not raw_text.endswith("|>") and not raw_text.endswith("|> "):
            utterance = raw_text.split('|>')[-1]
        else:
            utterance = " "

        params = {
            'types': types,
            'utterance': utterance
        }

        response = requests.get(address, params=params)
        response_json = response.json()
        logger.info(response_json)
        sample = response_json['response'].strip()
        print(f"CLASS TOKENS: {types} | UTTERANCE: {utterance} |")
        print("RESPONSE: " + str(sample))


def server_up(server_address):
    try:
        status = requests.head(server_address).status_code
    except requests.exceptions.RequestException or requests.exceptions.ConnectionError:
        status = None
    return status == 200


if __name__ == '__main__':
    fire.Fire(interact)
