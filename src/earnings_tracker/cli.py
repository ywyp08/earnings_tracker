from datetime import datetime
from typing import Annotated

import typer

from earnings_tracker.utils import load_data, save_data, convert_to_czk 

app = typer.Typer()


@app.command()
def earn(amount: float, currency: str):
    data = load_data()
    amount_czk = convert_to_czk(amount, currency)
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
