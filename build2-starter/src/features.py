"""Feature engineering and preprocessing pipeline for cancellation prediction.

Owner: Data Lead (Gurunath).
Job: Clean the bookings and return strictly Bin 1 features for model training,
ensuring zero data leakage and full reproducibility across backtest and nightly inference.
All data cleaning choices are logged in docs/DECISIONS.md.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Bin 1 Features: Fixed and known on the day of booking
NUMERIC_FEATURES = [
    "lead_time",
    "arrival_date_year",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "adr",
]

CATEGORICAL_FEATURES = [
    "hotel",
    "arrival_date_month",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "reserved_room_type",
    "deposit_type",
    "customer_type",
]

BIN1_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def clean_bookings(df: pd.DataFrame, drop_anomalies: bool = False) -> pd.DataFrame:
    """Clean the raw bookings dataframe and ensure required contract fields exist.

    All choices logged in docs/DECISIONS.md.
    """
    df = df.copy()

    # Fill missing values
    if "children" in df.columns:
        df["children"] = df["children"].fillna(0)
    if "country" in df.columns:
        df["country"] = df["country"].fillna("Unknown")

    # Fix negative ADR anomaly (1 row has ADR = -6.38)
    if "adr" in df.columns:
        df["adr"] = df["adr"].clip(lower=0.0)

    # Ensure arrival_date exists
    if "arrival_date" not in df.columns:
        if "arrival_date_year" in df.columns and "arrival_date_month" in df.columns and "arrival_date_day_of_month" in df.columns:
            df["arrival_date"] = pd.to_datetime(
                df["arrival_date_year"].astype(str)
                + "-"
                + df["arrival_date_month"]
                + "-"
                + df["arrival_date_day_of_month"].astype(str),
                format="%Y-%B-%d",
            )

    # Ensure stay length exists
    if "nights" not in df.columns:
        if "stays_in_weekend_nights" in df.columns and "stays_in_week_nights" in df.columns:
            df["nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

    if drop_anomalies:
        # Drop phantom bookings with 0 total guests (180 rows in full dataset)
        zero_guests = (df["adults"] == 0) & (df["children"] == 0) & (df["babies"] == 0)
        df = df[~zero_guests].copy()

    return df


def get_bin1_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return only Bin 1 features, strictly quarantining Bin 2 and Bin 3 columns."""
    clean_df = clean_bookings(df)
    missing = [c for c in BIN1_FEATURES if c not in clean_df.columns]
    if missing:
        raise ValueError(f"Dataframe missing required Bin 1 features: {missing}")
    return clean_df[BIN1_FEATURES]


def build_preprocessor() -> ColumnTransformer:
    """Create a ColumnTransformer pipeline for Bin 1 features.
    
    Categoricals are one-hot encoded with handle_unknown='ignore'.
    Numerics are standardized.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )


if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from data import read_raw
    raw = read_raw()
    cleaned = clean_bookings(raw)
    X = get_bin1_features(cleaned)
    print(f"Features extraction successful: {X.shape[0]:,} rows, {X.shape[1]} Bin 1 features.")
    preprocessor = build_preprocessor()
    X_trans = preprocessor.fit_transform(X)
    print(f"Preprocessing transform successful: output shape = {X_trans.shape}")

