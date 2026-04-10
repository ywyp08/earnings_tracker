from datetime import datetime, timedelta
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
        week = date[:10]
        total = sum(
            entry["amount_czk"]
            for entry in data
            if entry["date"] >= week and entry["date"] < (datetime.strptime(week, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
        )
        print(f"Week starting: {week}")

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
