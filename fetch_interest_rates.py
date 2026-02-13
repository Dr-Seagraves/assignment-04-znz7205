"""
Fetch monthly interest rates from FRED (Federal Reserve Economic Data).

Downloads: Federal Funds Rate, 30-Year Mortgage Rate, Prime Loan Rate.
Saves to: data/interest_rates_monthly.csv (next to this script).

Install: pip install pandas requests
"""
import os
from pathlib import Path

import pandas as pd
import requests

# -----------------------------------------------------------------------------
# SETTINGS – edit these as needed
# -----------------------------------------------------------------------------

# FRED API key (free at https://fred.stlouisfed.org/docs/api/api_key.html)
# Option 1: Put your key here (works for you; don't commit if sharing code)
FRED_API_KEY = "673ae4f1821466fd69190f4724867af4"

# Option 2: If FRED_API_KEY above is empty, the script will use the FRED_API_KEY
#            environment variable (set in terminal or .env file).

# Interest rate series to download: (FRED series id, column name in output file)
SERIES = [
    ("FEDFUNDS", "fed_funds"),       # Federal Funds Rate
    ("MORTGAGE30US", "mortgage_30y"),  # 30-Year Mortgage Rate
    ("MPRIME", "prime_rate"),         # Prime Loan Rate
]

# Date range: matched to REIT sample (REIT_sample_*.csv in data folder)
# If no REIT file exists, uses 2004-01-01 through today
START_DATE = ""   # Empty = auto from REIT data
END_DATE = ""     # Empty = auto from REIT data

# FRED API URL (no need to change)
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

# -----------------------------------------------------------------------------
# SCRIPT – no need to edit below
# -----------------------------------------------------------------------------


def fetch_one_series(series_id: str, api_key: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch one interest rate series from FRED."""
    params = {
        "api_key": api_key,
        "series_id": series_id,
        "observation_start": start_date,
        "observation_end": end_date,
        "file_type": "json",
    }
    response = requests.get(FRED_URL, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    rows = []
    for obs in data.get("observations", []):
        val = obs.get("value")
        if val == "." or val is None:
            continue
        try:
            rows.append({"date": obs["date"], "value": float(val)})
        except (ValueError, TypeError):
            continue

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def _get_date_range_from_reit(data_dir: Path) -> tuple[str, str]:
    """Get start/end dates from REIT_sample_*.csv to match sample period."""
    candidates = list(data_dir.glob("REIT_sample_*.csv"))
    if not candidates:
        return "2004-01-01", pd.Timestamp.now().strftime("%Y-%m-%d")
    path = max(candidates, key=lambda p: p.stat().st_mtime)
    df = pd.read_csv(path, nrows=10000)
    # Annual files have 'year'; monthly files have 'date'
    if "year" in df.columns:
        y_min, y_max = df["year"].min(), df["year"].max()
        return f"{int(y_min)}-01-01", f"{int(y_max)}-12-31"
    if "date" in df.columns:
        dates = pd.to_datetime(df["date"], errors="coerce").dropna()
        if not dates.empty:
            return dates.min().strftime("%Y-%m-%d"), dates.max().strftime("%Y-%m-%d")
    return "2004-01-01", pd.Timestamp.now().strftime("%Y-%m-%d")


def main():
    """Fetch interest rates from FRED and save to data folder."""
    api_key = FRED_API_KEY or os.environ.get("FRED_API_KEY")
    if not api_key:
        print("ERROR: You need a FRED API key.")
        print("  1. Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("  2. Either: Set FRED_API_KEY = 'your_key' at the top of this script")
        print("     Or:    set FRED_API_KEY=your_key  in your terminal (or .env file)")
        raise SystemExit(1)

    # Data folder is next to this script (e.g., classroom-template/data/)
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    start = START_DATE or None
    end = END_DATE or None
    if not start or not end:
        start, end = _get_date_range_from_reit(data_dir)
        print(f"Date range (from REIT data): {start} to {end}")

    print("Fetching interest rates from FRED...")
    all_series = []
    for series_id, col_name in SERIES:
        df = fetch_one_series(series_id, api_key, start, end)
        df = df.rename(columns={"value": col_name})
        df = df.set_index("date")
        all_series.append(df)

    # Combine into one table (align by date, use last value per month for weekly series)
    combined = pd.concat(all_series, axis=1)
    combined = combined.groupby(combined.index.to_period("M")).last()
    combined.index = combined.index.to_timestamp("M")
    combined = combined.dropna(how="all")

    # Save to data folder
    out_file = data_dir / "interest_rates_monthly.csv"
    combined.reset_index().to_csv(out_file, index=False)

    print("Done!")
    print("  Saved to:", out_file)
    print("  Date range:", combined.index.min().strftime("%Y-%m"), "to", combined.index.max().strftime("%Y-%m"))
    print("  Rows:", len(combined))
    print("\nLast 5 months:")
    print(combined.tail().to_string())


if __name__ == "__main__":
    main()
