import json
import os
import urllib.request

FILE_PATH = os.path.expanduser("./data/earnings.json")


def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def convert_to_czk(amount, currency):
    url = f'https://api.exchangerate-api.com/v4/latest/{currency.upper()}'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    rate = data['rates']['CZK']
    amount_czk = amount * rate
    return amount_czk
