# Earnings Tracker

A simple command-line tool to log earnings in different currencies and view reports in CZK.

## Quick Start

Requires Python 3.9 or later.

Install the package from the project root:

```bash
pip install -e .
```

Check the CLI help:

```bash
money --help
```

Log earnings:

```bash
money earn 100 usd
```

View today’s report:

```bash
money report day
```

## Commands

`money earn <amount> [currency]`
- Logs an earning in the given currency.
- If `currency` is omitted, the default currency from the config is used.

`money report [time_period] [date]`
- Shows earnings converted to CZK.
- `time_period` can be `day`, `week`, `month`, or `year`.
- `date` is optional and uses `YYYY-MM-DD` format.

## Examples

```bash
money earn 100 usd
money earn 50
money report day
money report month 2026-05
```