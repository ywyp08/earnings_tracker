from datetime import datetime

from .utils import *


def earn(args):
    """
    Log an earning.

    arguments:
    amount
    currency
    """

    data = load_data()
    amount_czk = convert_to_czk(args.amount, args.currency)
    entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount": args.amount,
            "currency": args.currency,
            "amount_czk": amount_czk
    }
    data.append(entry)
    save_data(data)
    print(f"Logged: {entry}")


def report(args):
    """
    Print earnings report.

    arguments:
    [time_period]
    """

    time_period = args.time_period or datetime.now().strftime("%Y-%m")
    data = load_data()
    total = 0.0
    
    for entry in data:
        if entry["date"].startswith(time_period):
            total += entry["amount_czk"]

    print(f"Month: {time_period}")
    print(f"Earnings: {total:.2f} CZK")
