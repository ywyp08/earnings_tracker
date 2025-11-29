#!/usr/bin/env python3

import requests
import sys
from datetime import datetime
import json
import os
import typer

app = typer.Typer()

FILE_PATH = os.path.expanduser('./data/earnings.json')


#Helper functions

def load_data():
    """Load earnings data."""

    if not os.path.exists(FILE_PATH):
        return[]
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        typer.echo("ERROR: earnings.json is corrupted.")
        typer.echo(f"Path: {FILE_PATH}")
        raise typer.Exit(code=1)


def save_data(data):
    """Save earnings data."""

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def convert_to_czk(amount, currency):
    """Convert given amount from specific currency to CZK."""

    url = f'https://api.exchangerate-api.com/v4/latest/{currency.upper()}'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from the API.")
            return None
        data = response.json()
        if 'CZK' in data['rates']:
            rate = data['rates']['CZK']
            converted_amount = amount * rate
            return converted_amount
        else:
            typer.echo(f"CZK rate not found for {currency}.")
            return none
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


#Commands

@app.command()
def earn(amount: float, currency: str):
    """Log today's earning."""

    currency = currency.lower()
    if currency == "czk":
        amount_czk = amount
    else:
        amount_czk = convert_to_czk(amount, currency)

    entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount_czk": amount_czk,
            "source_currency": currency,
            "original_amount": amount
    }

    data = load_data()
    data.append(entry)
    save_data(data)

    typer.echo(f"Logged: {entry}")

@app.command()
def report():
    """Show total earnings for the current month."""

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
        f"Total Earnings: {total_earnings:.2f} CZK"
    )

    print(report)

if __name__ == "__main__":
   app() 
