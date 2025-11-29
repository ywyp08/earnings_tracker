#!/usr/bin/env python3

import requests
import sys
from datetime import datetime
import json
import os

def convert_usd_to_czk(amount):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from the API.")
            return None
        data = response.json()
        rate = data['rates']['CZK']
        converted_amount = amount * rate
        return converted_amount
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def log_earning(amount, currency):

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount entered.")
        return
    
    if currency == "usd":
        amount_czk = convert_usd_to_czk(amount)
    elif currency == "czk":
        amount_czk = amount
    
    if amount_czk is not None:
        earnings_data = {
            "date": datetime.now().strftime("%d-%m-%Y"),
             "amount_czk": amount_czk
        }

        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(earnings_data)

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Earnings logged: {earnings_data}")
    else:
        print("Failed to convert amount.")

def generate_report():
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    current_month = datetime.now().strftime("%m-%Y")
    total_earnings = 0

    for entry in data:
        if entry["date"].endswith(current_month):
                total_earnings += entry["amount_czk"]

    report = (
        f"Month: {current_month}\n"
        f"Total Earnings: {total_earnings:.2f} CZK\n"
    )

    print(report)

file_path = os.path.expanduser('~/.money/earnings.json')

def command_tree(command):
    if command == "earn":
        amount = float(sys.argv[2])
        currency = str(sys.argv[3])
        log_earning(amount, currency)
    elif command == "report":
        generate_report()
    else:
        print("Command not recognized")

def main():
    command = sys.argv[1]
    command_tree(command)

if __name__ == "__main__":
    main()
