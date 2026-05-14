import streamlit as st
from datetime import datetime, timedelta
from earnings_tracker.utils import load_data, save_data, convert_to_default
from earnings_tracker.config import get_default_currency

st.title("Earnings Tracker")

st.header("Log Earnings")
amount = st.number_input("Amount", min_value=0.0, step=0.01)
currency = st.text_input("Currency", value=get_default_currency())
if st.button("Log Earnings"):
    target_currency = get_default_currency()
    try:
        amount_default, rate = convert_to_default(amount, currency, target_currency)
    except ValueError:
        st.error("Error: conversion failed (check currency or network)")
        st.stop()
    
    data = load_data()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "currency": currency,
        "amount_default": amount_default,
        "currency_default": target_currency,
        "rate_to_default": rate
    }
    data.append(entry)
    save_data(data)
    st.success(f"Earned: {entry['amount_default']} {entry['currency_default']}")
    st.rerun()

st.header("Earnings Report")
period = st.selectbox("Period", ["day", "week", "month"])
date = st.date_input("Start Date", value=datetime.now().date())
if st.button("Generate Report"):
    data = load_data()
    default_currency = get_default_currency()
    date_str = date.strftime("%Y-%m-%d")
    
    if period == "day":
        total = sum(
            entry.get("amount_default", 0)
            for entry in data
            if entry["date"].startswith(date_str)
        )
        st.write(f"Day: {date_str}")
    
    elif period == "week":
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        monday = parsed_date - timedelta(days=parsed_date.weekday())
        sunday = monday + timedelta(days=7)
        monday_str = monday.strftime("%Y-%m-%d")
        sunday_str = sunday.strftime("%Y-%m-%d")
        total = sum(
            entry.get("amount_default", 0)
            for entry in data
            if monday_str <= entry["date"] < sunday_str
        )
        st.write(f"Week: {monday_str} – {(sunday - timedelta(days=1)).strftime('%Y-%m-%d')}")
    
    elif period == "month":
        month = date_str[:7]
        total = sum(
            entry.get("amount_default", 0)
            for entry in data
            if entry["date"].startswith(month)
        )
        st.write(f"Month: {month}")
    
    st.write(f"Total: {total} {default_currency}")

st.header("All Earnings")
data = load_data()
st.dataframe(data)