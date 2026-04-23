import json
import os
import urllib.request
from urllib.error import URLError, HTTPError

from .config import get_data_file_path


FILE_PATH = get_data_file_path()


def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_data(data):
    folder = os.path.dirname(FILE_PATH)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def convert_to_default(amount, currency, target_currency):
    url = f'https://api.exchangerate-api.com/v4/latest/{currency.upper()}'
    try:
        response = urllib.request.urlopen(url)
        data = json.load(response)
        rate = data['rates'][target_currency.upper()]
    except (HTTPError, URLError, KeyError, ValueError):
        raise ValueError("currency conversion failed")
    return amount * rate, rate
