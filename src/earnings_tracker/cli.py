from datetime import datetime
from typing import Annotated

import typer

from earnings_tracker.utils import load_data, save_data, convert_to_czk 


app = typer.Typer(help="Earnings Tracker CLI for logging and reporting earnings.")


@app.command()
def earn(amount: float, currency: str):
    """
    Log new earning.
    """
    try:
        amount_czk = convert_to_czk(amount, currency)
    except ValueError:
        typer.echo("Error: conversion failed (check currency or network)")
        raise typer.Exit(1)
    
    data = load_data()
    entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount": amount,
            "currency": currency,
            "amount_czk": amount_czk
    }
    data.append(entry)
    save_data(data)
    print(f"Logged: {entry}")


@app.command()
def report(time_period: Annotated[str, typer.Argument()] = datetime.now().strftime("%Y-%m")):
    """
    Report your earnings.
    """
    data = load_data()
    total = sum(
            entry["amount_czk"]
            for entry in data
            if entry["date"].startswith(time_period)
    )
    print(f"Month: {time_period}")
    print(f"Earnings: {total:.2f} CZK")


def main():
    app()
