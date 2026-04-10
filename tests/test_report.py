from typer.testing import CliRunner
from earnings_tracker.cli import app, load_data


runner = CliRunner()


def mock_data():
    return [
        {"date": "2026-04-10", "amount_czk": 100},
        {"date": "2026-04-10", "amount_czk": 50},
        {"date": "2026-04-09", "amount_czk": 30},
        {"date": "2026-03-15", "amount_czk": 20}
    ]


# report command tests

def test_report_day(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)

    result = runner.invoke(app, ["report", "day", "2026-04-10"])

    assert result.exit_code == 0
    assert "Day: 2026-04-10" in result.output
    assert "150.00 CZK" in result.output


def test_report_month(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)

    result = runner.invoke(app, ["report", "month", "2026-04"])

    assert result.exit_code == 0
    assert "Month: 2026-04" in result.output
    assert "180.00 CZK" in result.output


def test_report_year(monkeypatch):
    monkeypatch.setattr("earnings_tracker.cli.load_data", mock_data)

    result = runner.invoke(app, ["report", "year", "2026-04-10"])

    assert result.exit_code == 0
    assert "Year: 2026" in result.output
    assert "200.00 CZK" in result.output