from typer.testing import CliRunner
from earnings_tracker.cli import app


runner = CliRunner()


def mock_data():
    return [
        {
            "date": "2026-04-10",
            "amount": 50.0,
            "currency": "USD",
            "amount_default": 100,
            "currency_default": "CZK",
            "rate_to_default": 2.0
        },
        {
            "date": "2026-04-10",
            "amount": 25.0,
            "currency": "EUR",
            "amount_default": 50,
            "currency_default": "CZK",
            "rate_to_default": 2.0
        },
        {
            "date": "2026-04-09",
            "amount": 10.0,
            "currency": "USD",
            "amount_default": 30,
            "currency_default": "CZK",
            "rate_to_default": 3.0
        },
        {
            "date": "2026-03-15",
            "amount": 5.0,
            "currency": "GBP",
            "amount_default": 20,
            "currency_default": "CZK",
            "rate_to_default": 4.0
        }
    ]


# report command tests

def test_report_day(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)
    monkeypatch.setattr("earnings_tracker.cli.get_default_currency", lambda: "USD")

    result = runner.invoke(app, ["report", "day", "2026-04-10"])

    assert result.exit_code == 0
    assert "Day: 2026-04-10" in result.output
    assert "150.00 USD" in result.output


def test_report_month(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)
    monkeypatch.setattr("earnings_tracker.cli.get_default_currency", lambda: "USD")

    result = runner.invoke(app, ["report", "month", "2026-04"])

    assert result.exit_code == 0
    assert "Month: 2026-04" in result.output
    assert "180.00 USD" in result.output


def test_report_year(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)
    monkeypatch.setattr("earnings_tracker.cli.get_default_currency", lambda: "USD")

    result = runner.invoke(app, ["report", "year", "2026-04-10"])

    assert result.exit_code == 0
    assert "Year: 2026" in result.output
    assert "200.00 USD" in result.output


def test_report_week(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)
    monkeypatch.setattr("earnings_tracker.cli.get_default_currency", lambda: "USD")

    result = runner.invoke(app, ["report", "week", "2026-04-10"])

    assert result.exit_code == 0
    assert "Week:" in result.output
    assert "180.00 USD" in result.output  # 100 + 50 + 30 from Apr 10 and 9