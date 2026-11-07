"""Get the client's booking history and hand it over exactly as the hotels' system exported it.

The bookings are the public Hotel Booking Demand datasets: Antonio, N., de Almeida, A. and Nunes, L.
(2019). Hotel booking demand datasets. Data in Brief, 22, 41-49. https://doi.org/10.1016/j.dib.2018.11.126
The article and its data are open access under CC BY 4.0, so every copy of your work cites it.
The copy downloaded here is the cleaned-column version published by the TidyTuesday project
(checked 7 November 2026).
"""
import pathlib
import urllib.request

import pandas as pd

URL = ("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/"
       "data/2020/2020-02-11/hotels.csv")  # checked 7 November 2026
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
FILE = "hotels.csv"

# The outcome column: 1 if the booking was cancelled (including no-shows), 0 if the guest arrived.
TARGET = "is_canceled"

EXPECTED_ROWS = 119_390
EXPECTED_COLUMNS = 32


def download(data_dir=DATA_DIR):
    """Download the file the first time, reuse it after that, and return its path.

    Finished for you. The file is about 16 MB and lands in data/, which .gitignore keeps out of
    your repository, so every member downloads their own copy in their own Codespace.
    """
    data_dir = pathlib.Path(data_dir)
    path = data_dir / FILE
    if not path.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, path)
    return path


def read_raw(path=None):
    """Return every booking exactly as exported: no row removed, no value changed.

    Finished for you. Every cleaning choice after this point is your team's, and each one goes in
    docs/DECISIONS.md with its reason and the number of rows it touched.
    """
    df = pd.read_csv(path or download())
    if df.shape != (EXPECTED_ROWS, EXPECTED_COLUMNS):
        raise ValueError(
            f"Expected {EXPECTED_ROWS} rows and {EXPECTED_COLUMNS} columns, got {df.shape}. "
            "Delete data/hotels.csv and run again to download a fresh copy."
        )
    return df


def arrival_date(df):
    """Return the arrival date of every booking as one datetime column.

    Finished for you, because the export splits it across three columns (year, month name, day).
    """
    return pd.to_datetime(
        df["arrival_date_year"].astype(str) + "-" + df["arrival_date_month"] + "-"
        + df["arrival_date_day_of_month"].astype(str),
        format="%Y-%B-%d",
    )


if __name__ == "__main__":
    bookings = read_raw()
    print(f"{len(bookings):,} bookings, {bookings.shape[1]} columns")
    print(f"Arrivals from {arrival_date(bookings).min().date()} to {arrival_date(bookings).max().date()}")

# Test cases (run: python src/data.py)
# 1. Fresh Codespace, no data/hotels.csv -> downloads, prints "119,390 bookings, 32 columns" and
#    "Arrivals from 2015-07-01 to 2017-08-31".
# 2. Second run -> reuses the file and prints the same two lines without downloading.
# 3. A truncated data/hotels.csv -> ValueError naming the shape; delete the file and run again.
