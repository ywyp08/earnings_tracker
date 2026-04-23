from datetime import datetime, timedelta
from typing import Annotated

import typer

from earnings_tracker.utils import load_data, save_data, convert_to_czk 
from earnings_tracker.config import get_default_currency 


app = typer.Typer(help="Earnings Tracker CLI for logging and reporting earnings.")


@app.command()
def earn(amount: float, currency: Annotated[str, typer.Argument()] = None):
    """
    Log new earning.
    """
    if currency is None:
        currency = get_default_currency()
    
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
def report(
        time_period: Annotated[str, typer.Argument()] = "day",
        date: Annotated[str, typer.Argument()] = datetime.now().strftime("%Y-%m-%d")
        ):
    
    """
    Report your earnings.
    """

    data = load_data()

    if time_period == "day":
        total = sum(
            entry["amount_czk"]
            for entry in data
            if entry["date"].startswith(date)
        )
        print(f"Day: {date}")

    elif time_period == "week":
        parsed_date = datetime.strptime(date[:10], "%Y-%m-%d")
        monday = parsed_date - timedelta(days=parsed_date.weekday())
        sunday = monday + timedelta(days=7)
        monday_str = monday.strftime("%Y-%m-%d")
        sunday_str = sunday.strftime("%Y-%m-%d")
        total = sum(
            entry["amount_czk"]
            for entry in data
            if monday_str <= entry["date"] < sunday_str
        )
        print(f"Week: {monday_str} – {(sunday - timedelta(days=1)).strftime('%Y-%m-%d')}")

    elif time_period == "month":
        month = date[:7]
        total = sum(
            entry["amount_czk"]
            for entry in data
            if entry["date"].startswith(month)
        )
        print(f"Month: {month}")

    elif time_period == "year":
        year = date[:4]
        total = sum(
            entry["amount_czk"]
            for entry in data
            if entry["date"].startswith(year)
        )
        print(f"Year: {year}")

    else:
        raise typer.BadParameter("time_period must be 'day', 'week', 'month', or 'year'")

    print(f"Earnings: {total:.2f} CZK")


def main():
    app()
