# -*- encoding: utf-8 -*-
# Util methods

import os
import time
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
        logging.error(f'\n🚨 Query failed: HTTP code {r.status_code}')


def wei_to_eth(num) -> float:

    return num / 1000000000000000000


def hex_to_int(num) -> int:

    return int(num, 16)


def open_abi(filepath) -> json:

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'\n🚨 Failed to parse: "{filepath}": {e}')


def format_price(price) -> str:

    return "{:.2f}".format(round(price, 2))


def format_path(dir_path, filename) -> str:

    return os.path.join(dir_path, filename)


def format_filename() -> str:

    return "arbitrage_" + time.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'


def save_results(destination, data) -> None:

    try:
        with open(destination, 'w') as f:
            for line in data:

                f.write(", ".join(line))
    except IOError as e:
        logging.error(f'\n🚨 Could not save {destination}: {e}')


def create_dir(result_dir) -> None:

    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)
    except OSError as e:
        logging.error(f'🚨 Could not create {result_dir}: {e}')
