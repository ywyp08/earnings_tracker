#!/usr/bin/env python3

import requests
from datetime import datetime
import json
import os
import typer
from typing_extensions import Annotated

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
            typer.echo(f"Error: Received status code {response.status_code} from the API.")
            return None
        data = response.json()
        if 'CZK' in data['rates']:
            rate = data['rates']['CZK']
            converted_amount = amount * rate
            return converted_amount
        else:
            typer.echo(f"CZK rate not found for {currency}.")
            return None
    except Exception as e:
        typer.echo(f"An error occurred: {e}")
        return None


#Commands

@app.command()
def earn(amount: float, currency: str):
    """Log today's earning."""

    data = load_data()
    entry = {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "original_amount": amount,
            "original_currency": currency,
            "amount_czk": convert_to_czk(amount, currency)
    }
    data.append(entry)
    save_data(data)
    typer.echo(f"Logged: {entry}")


@app.command()
def report(time_period: Annotated[str, typer.Argument()] = datetime.now().strftime("%m-%Y")):
    """Show total earnings for the current month."""

    data = load_data()
    total_earnings = 0.0
    if time_period is None:
        time_period = datetime.now().strftime("%m-%Y")
    for entry in data:
        if entry["date"].endswith(time_period):
                total_earnings += entry["amount_czk"]
    report = (
        f"Month: {time_period}\n"
        f"Total Earnings: {total_earnings:.2f} CZK"
    )
    typer.echo(report)


if __name__ == "__main__":
   app() 
