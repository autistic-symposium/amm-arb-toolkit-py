# -*- encoding: utf-8 -*-
# Util methods for this package

import os
import time
import json
import logging
import requests
from urllib.parse import urljoin


def craft_url(url, endpoint) -> str:
    """Add an url to an endpoint."""

    return urljoin(url, endpoint)


def send_request(url, data=None, params=None) -> dict:
    """Wrapper for requests package."""

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
    """Convert a value in wei to eth."""

    return num / 1000000000000000000


def hex_to_int(num) -> int:
    """Convert a value in hex to integer."""

    return int(num, 16)


def open_abi(filepath) -> json:
    """Load and parse an ABI file."""

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'\n🚨 Failed to parse: "{filepath}": {e}')


def format_perc(value) -> str:
    """Format a percentage float to a well-suitable string."""

    return "%.8f%%" % (100 * value)


def format_price(value) -> str:
    """Format a price float to a well-suitable rounded string."""

    return "{:.2f}".format(round(value, 2))


def format_path(dir_path, filename) -> str:
    """Format a OS full filepath."""

    return os.path.join(dir_path, filename)


def get_time_now() -> str:
    """Get current OS time and return a well-suitable string."""

    return time.strftime("%Y-%m-%d_%H-%M-%S")


def format_filename() -> str:
    """Format the name for the results file with current time."""

    return "arbitrage_" + get_time_now() + '.txt'


def save_results(destination, data) -> None:
    """Save data from memory to a destination in disk."""

    try:
        with open(destination, 'w') as f:
            for line in data:
                f.write(str(line) + '\n')
    except IOError as e:
        logging.error(f'\n🚨 Could not save {destination}: {e}')


def create_dir(result_dir) -> None:
    """Check whether a directory exists and create it if needed."""

    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)
    except OSError as e:
        logging.error(f'🚨 Could not create {result_dir}: {e}')
