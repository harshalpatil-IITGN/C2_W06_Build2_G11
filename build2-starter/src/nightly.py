"""Nightly overbooking recommendation engine.

Owner: Build Lead (Mihir).
Job: Generate the daily morning overbooking table for each hotel and arrival night,
loading the frozen winning model and safety buffer from models/chosen_model.joblib.

Run via:
    python src/nightly.py --from 2017-08-18 --nights 14
"""

import argparse
import datetime
import pathlib
import sys
import joblib
import numpy as np
import pandas as pd

SRC_DIR = pathlib.Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data import read_raw
from contract import nightly_table, night_cost, WALK_COST
from features import clean_bookings, get_bin1_features


def parse_args():
    parser = argparse.ArgumentParser(description="Generate nightly oversell recommendation table.")
    parser.add_argument(
        "--from",
        dest="from_date",
        type=str,
        default="2017-08-18",
        help="Start arrival date in YYYY-MM-DD format (default: 2017-08-18)",
    )
    parser.add_argument(
        "--nights",
        type=int,
        default=14,
        help="Number of consecutive arrival nights to recommend (default: 14)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=str(SRC_DIR.parent / "models" / "chosen_model.joblib"),
        help="Path to the saved chosen model package (default: models/chosen_model.joblib)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to raw bookings CSV (default: uses data/hotels.csv via read_raw())",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=str(SRC_DIR.parent / "evidence" / "nightly_recommendation.csv"),
        help="Output CSV path for the generated recommendation table",
    )
    return parser.parse_args()


def run_nightly(from_date_str: str, nights_count: int, model_path: str, data_path: str = None, out_path: str = None):
    print("=" * 95)
    print("BUILD 2 · REVENUE SCIENCE SQUAD · NIGHTLY OVERBOOKING ENGINE (MVP)")
    print("=" * 95)

    # 1. Load model artifact package
    pkg_file = pathlib.Path(model_path)
    if not pkg_file.exists():
        raise FileNotFoundError(
            f"Chosen model package not found at '{model_path}'. "
            "Please run 'python src/backtest.py' first to train and export the winning model package."
        )

    print(f"\n[1/4] Loading frozen model package from: {pkg_file.name}")
    pkg = joblib.load(pkg_file)
    model = pkg["model"]
    preprocessor = pkg["preprocessor"]
    buffer_b = pkg["buffer"]
    model_name = pkg.get("model_name", "Winning Model")
    print(f"      Model Name:     {model_name}")
    print(f"      Safety Buffer:  b* = {buffer_b}")

    # 2. Load and filter bookings
    start_dt = pd.to_datetime(from_date_str)
    end_dt = start_dt + datetime.timedelta(days=nights_count)
    print(f"\n[2/4] Loading bookings for horizon: {start_dt.strftime('%Y-%m-%d')} to {(end_dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')} ({nights_count} nights)...")

    if data_path:
        raw_df = pd.read_csv(data_path)
    else:
        raw_df = read_raw()

    df = clean_bookings(raw_df)

    # Filter target arrival window
    window_df = df[(df["arrival_date"] >= start_dt) & (df["arrival_date"] < end_dt)].copy()
    if len(window_df) == 0:
        raise ValueError(f"No bookings found in data between {start_dt.strftime('%Y-%m-%d')} and {end_dt.strftime('%Y-%m-%d')}.")

    print(f"      Found {len(window_df):,} bookings due to arrive in the requested window.")

    # 3. Predict cancellation probabilities using strictly Bin 1 features
    print("\n[3/4] Extracting Bin 1 features and generating cancellation probabilities...")
    X_window = preprocessor.transform(get_bin1_features(window_df))
    prob = model.predict_proba(X_window)[:, 1]
    window_df["pred_prob"] = prob

    # 4. Aggregate to hotel-night decision unit
    print("\n[4/4] Computing nightly overbooking recommendations (k = max(0, round(expected - b)))...")
    base_table = nightly_table(window_df, prob)

    # Calculate oversell k
    k_rec = np.maximum(0, np.round(base_table["expected"] - buffer_b)).astype(int)
    base_table["buffer_b"] = buffer_b
    base_table["oversell_k"] = k_rec

    # Reset index for clean display and export
    out_table = base_table.reset_index()
    out_table["arrival_date"] = pd.to_datetime(out_table["arrival_date"]).dt.strftime("%Y-%m-%d")

    # Display morning table
    print("\n" + "=" * 115)
    print(f"MORNING OVERBOOKING DESK TABLE ({start_dt.strftime('%Y-%m-%d')} to {(end_dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')})")
    print("=" * 115)
    print(f"{'Hotel':<14} | {'Arrival Date':<12} | {'Bookings':<8} | {'Exp Cancels':<11} | {'Spread':<8} | {'Buffer':<6} | {'Oversell (k)':<12} | {'Stay Value'}")
    print("-" * 115)
    for _, row in out_table.iterrows():
        print(
            f"{row['hotel']:<14} | "
            f"{row['arrival_date']:<12} | "
            f"{int(row['book']):>8d} | "
            f"{row['expected']:>11.1f} | "
            f"±{row['spread']:>6.2f} | "
            f"{int(row['buffer_b']):>6d} | "
            f"{int(row['oversell_k']):>12d} | "
            f"€{row['stay_value']:>9.2f}"
        )
    print("=" * 115)

    # If actual cancellations are known in this window, score the realized outcomes
    if "cancelled" in base_table.columns:
        cost_eval = night_cost(base_table, k_rec)
        print("\nREALIZED PERFORMANCE ON THIS 14-NIGHT WINDOW:")
        print(f"   - Total Rooms Oversold (Sum k): {k_rec.sum():,d} rooms")
        print(f"   - Actual Realized Cancels:      {int(base_table['cancelled'].sum()):,d} rooms")
        print(f"   - Realized Empty Rooms:         {cost_eval['empty_rooms']:,d}")
        print(f"   - Realized Walked Guests:       {cost_eval['walked_guests']:,d}")
        print(f"   - Realized Walk Rate:           {cost_eval['walks_per_1000']:.2f} per 1,000 arrivals (Ceiling <= 10.0: {'PASS' if cost_eval['ceiling_met'] else 'BREACHED'})")
        print(f"   - Realized Total Cost:          €{cost_eval['cost_eur']:,.2f}")

    # 5. Export to CSV evidence
    if out_path:
        out_file = pathlib.Path(out_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_table.to_csv(out_file, index=False)
        print(f"\n[OK] Nightly recommendation table exported to: {out_file}")

    return out_table


if __name__ == "__main__":
    args = parse_args()
    run_nightly(
        from_date_str=args.from_date,
        nights_count=args.nights,
        model_path=args.model,
        data_path=args.data,
        out_path=args.out,
    )
