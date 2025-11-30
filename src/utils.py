import json
import os

FILE_PATH = os.path.expanduser("./data/earnings.json")


def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
