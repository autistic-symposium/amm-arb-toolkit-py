# -*- encoding: utf-8 -*-
# Util methods


import json
import logging
import requests
from urllib.parse import urljoin


def craft_url(url, endpoint) -> str:

    return urljoin(url, endpoint)


def send_request(url, data=None, params=None) -> dict:

    if not params:
        params = {'header': 'Content-Type: application/json'}

    try:
        r = requests.post(url, data=data, params=params)

    except requests.exceptions.HTTPError as e:
        raise Exception(f'{url}: {e.response.text}')
    if r.status_code == 200:
        return r.json()
    else:
        logging.error(f'🚨 Query failed: HTTP code {r.status_code}')


def wei_to_eth(num) -> float:

    return num / 1000000000000000000


def hex_to_int(num) -> int:

    return int(num, 16)


def open_abi(filepath) -> json:

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'🚨 Failed to parse: "{filepath}" {e}')
