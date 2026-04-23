# Earnings Tracker

A command-line tool for tracking and reporting earnings in multiple currencies, with automatic conversion to CZK.

## Features

- Log earnings with amounts in various currencies
- Automatic currency conversion to CZK using real-time exchange rates
- Generate reports for daily, weekly, monthly, or yearly earnings
- Data stored locally in JSON format
- Simple CLI interface

## Installation

1. Ensure you have Python 3.9 or later installed.
2. Clone or download this repository.
3. Install the package in editable mode:

   ```bash
   pip install -e .
   ```

This will install the `money` command globally.

## Usage

### Logging Earnings

To log a new earning:

```bash
money earn <amount> [currency]
```

If currency is omitted, it uses the default from config (default: CZK).

Example:

```bash
money earn 100 usd
money earn 50  # Uses default currency
```

This logs the amount, converts it to CZK using the current exchange rate, and saves it with today's date.

### Generating Reports

To view earnings reports:

```bash
money report [time_period] [date]
```

- `time_period`: `day`, `week`, `month`, or `year` (defaults to `day`)
- `date`: Optional date in YYYY-MM-DD format (defaults to today)

Examples:

```bash
# Today's earnings
money report day

# Earnings for a specific day
money report day 2026-04-10

# Weekly earnings (week containing the date)
money report week 2026-04-10

# Monthly earnings
money report month 2026-04

# Yearly earnings
money report year 2026
```

## Configuration

The app uses a config file at `~/.config/earnings_tracker/config.toml` for user settings. If it doesn't exist, defaults are used.

Copy the example `config.toml` from the project root to `~/.config/earnings_tracker/config.toml` and edit:

- `default_currency`: Default currency for earnings (e.g., "EUR")
- `data_file_path`: Path to store earnings data (default: `~/.local/share/earnings_tracker/earnings.json`)

Example config:

```toml
default_currency = "EUR"
data_file_path = "~/earnings.json"
```

## Dependencies

- `typer`: For CLI interface
- Internet connection for currency conversion (uses exchangerate-api.com)

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

- `src/earnings_tracker/`: Main package
  - `cli.py`: Command-line interface
  - `utils.py`: Utility functions for data handling and currency conversion
- `tests/`: Unit tests
- `pyproject.toml`: Project configuration

## License

[Specify license here, e.g., MIT]
