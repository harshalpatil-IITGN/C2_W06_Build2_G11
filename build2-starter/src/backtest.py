"""Backtesting engine and multi-method evaluation comparison.

Owner: Model Lead (Vysag).
Job: Train candidate models on the train period (< July 2016), tune safety buffers and
select the winning model on the choose period (July-Dec 2016) under the walk ceiling
(<= 10 / 1,000 arrivals), evaluate strictly ONCE on the proof period (Jan-Aug 2017),
print the comparative method table, and save the chosen model to models/chosen_model.joblib.

Run via:
    python src/backtest.py
"""

import pathlib
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, mean_absolute_error

SRC_DIR = pathlib.Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data import read_raw
from contract import split_periods, nightly_table, night_cost
from features import clean_bookings, get_bin1_features, build_preprocessor

MODELS_DIR = SRC_DIR.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
CHOSEN_MODEL_PATH = MODELS_DIR / "chosen_model.joblib"


def run_backtest():
    print("=" * 125)
    print("BUILD 2 · REVENUE SCIENCE SQUAD · MODEL EVALUATION & BACKTEST")
    print("=" * 125)

    # 1. Load and prepare data
    print("\n[1/5] Loading historical bookings and enforcing chronological splits...")
    raw = read_raw()
    df = clean_bookings(raw)
    train_df, choose_df, proof_df = split_periods(df)

    print(f"      Train split (< 2016-07-01):      {len(train_df):>6,} bookings")
    print(f"      Choose split (2016-07 to 2016-12): {len(choose_df):>6,} bookings")
    print(f"      Proof split (>= 2017-01-01):     {len(proof_df):>6,} bookings")

    # 2. Extract strictly Bin 1 features
    print("\n[2/5] Extracting Bin 1 features (zero lookahead leakage)...")
    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(get_bin1_features(train_df))
    y_train = train_df["is_canceled"].values

    X_choose = preprocessor.transform(get_bin1_features(choose_df))
    X_proof = preprocessor.transform(get_bin1_features(proof_df))
    y_proof = proof_df["is_canceled"].values

    # 3. Fit Candidate Models on Train Split
    print("\n[3/5] Fitting candidate models on Train split...")
    hotel_rates = train_df.groupby("hotel")["is_canceled"].mean().to_dict()

    lookup = train_df.groupby(["hotel", "arrival_date_month", "market_segment"])["is_canceled"].mean()
    overall_rate = train_df["is_canceled"].mean()

    def lookup_predict(sub_df):
        keys = list(zip(sub_df["hotel"], sub_df["arrival_date_month"], sub_df["market_segment"]))
        return np.array([lookup.get(k, overall_rate) for k in keys])

    print("      Fitting Method 3: Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)

    print("      Fitting Method 4: HistGradientBoosting Ensemble...")
    hgb_model = HistGradientBoostingClassifier(random_state=42, max_iter=100)
    hgb_model.fit(X_train, y_train)

    methods = {
        "Client Flat Rule": {
            "choose_p": np.array([hotel_rates[h] for h in choose_df["hotel"]]),
            "proof_p": np.array([hotel_rates[h] for h in proof_df["hotel"]]),
            "model_obj": hotel_rates,
        },
        "Lookup Table": {
            "choose_p": lookup_predict(choose_df),
            "proof_p": lookup_predict(proof_df),
            "model_obj": lookup,
        },
        "Logistic Regression": {
            "choose_p": lr_model.predict_proba(X_choose)[:, 1],
            "proof_p": lr_model.predict_proba(X_proof)[:, 1],
            "model_obj": lr_model,
        },
        "Gradient Boosting": {
            "choose_p": hgb_model.predict_proba(X_choose)[:, 1],
            "proof_p": hgb_model.predict_proba(X_proof)[:, 1],
            "model_obj": hgb_model,
        },
    }

    # 4. Tune Safety Buffers & Pick Winner on Choose Period
    print("\n[4/5] Tuning safety buffers on Choose split (minimizing EUR loss under <= 10 walks/1,000)...")
    choose_summary = {}
    for name, data in methods.items():
        table_ch = nightly_table(choose_df, data["choose_p"])
        best_cost = float("inf")
        best_b = 0
        best_res = None
        for b in range(-5, 40):
            k = np.maximum(0, np.round(table_ch["expected"] - b))
            res = night_cost(table_ch, k)
            if res["ceiling_met"] and res["cost_eur"] < best_cost:
                best_cost = res["cost_eur"]
                best_b = b
                best_res = res
        choose_summary[name] = {
            "buffer": best_b,
            "choose_cost": best_cost,
            "choose_res": best_res,
        }
        print(
            f"      {name:<22} -> Buffer b* = {best_b:>2} "
            f"(Choose Cost: EUR {best_res['cost_eur']:>10,.2f}, Walks/1k: {best_res['walks_per_1000']:>4.2f})"
        )

    winner_name = min(choose_summary.keys(), key=lambda m: choose_summary[m]["choose_cost"])
    winner_buffer = choose_summary[winner_name]["buffer"]

    # 5. Score Proof Period ONCE with Frozen Buffers
    print("\n[5/5] Scoring Proof Period ONCE with frozen models and buffers...")
    raw_results = []
    for name, data in methods.items():
        b_star = choose_summary[name]["buffer"]
        table_pr = nightly_table(proof_df, data["proof_p"])
        k_pr = np.maximum(0, np.round(table_pr["expected"] - b_star))
        res_pr = night_cost(table_pr, k_pr)

        auc_score = roc_auc_score(y_proof, data["proof_p"])
        mae_rooms = mean_absolute_error(table_pr["cancelled"], table_pr["expected"])

        raw_results.append({
            "Method": name,
            "Buffer b*": b_star,
            "AUC": auc_score,
            "MAE (Rooms)": mae_rooms,
            "Empty Rooms": res_pr["empty_rooms"],
            "Walked Guests": res_pr["walked_guests"],
            "Walks/1,000": res_pr["walks_per_1000"],
            "Total Cost (EUR)": res_pr["cost_eur"],
            "Ceiling Met": res_pr["ceiling_met"],
        })

    flat_cost = next(r["Total Cost (EUR)"] for r in raw_results if r["Method"] == "Client Flat Rule")
    for r in raw_results:
        r["Savings (EUR)"] = flat_cost - r["Total Cost (EUR)"]

    results_df = pd.DataFrame(raw_results)

    print("\n" + "=" * 125)
    print("PROVED RESULTS TABLE (Held-Out Proof Period: Jan 1 - Aug 31, 2017)")
    print("=" * 125)
    print(
        f"{'Method':<21} | {'Buf':>4} | {'AUC':>6} | {'MAE':>5} | {'Empty':>6} | "
        f"{'Walks':>5} | {'Walks/1k':>8} | {'Cost (EUR)':>13} | {'Savings (EUR)':>13} | {'Ceiling'}"
    )
    print("-" * 125)
    for _, r in results_df.iterrows():
        met_str = "PASS (<=10)" if r["Ceiling Met"] else "REJECT (>10)"
        print(
            f"{r['Method']:<21} | {r['Buffer b*']:>4} | {r['AUC']:>6.3f} | {r['MAE (Rooms)']:>5.2f} | "
            f"{r['Empty Rooms']:>6,d} | {r['Walked Guests']:>5,d} | {r['Walks/1,000']:>8.2f} | "
            f"EUR {r['Total Cost (EUR)']:>9,.2f} | EUR {r['Savings (EUR)']:>9,.2f} | {met_str}"
        )
    print("=" * 125)

    winner = next(r for r in raw_results if r["Method"] == winner_name)
    print(f"\nCHOSEN ON 2016 H2 & PROVED ON 2017: {winner_name} (Buffer b* = {winner_buffer})")
    print(f"        Proof Cost:   EUR {winner['Total Cost (EUR)']:,.2f}")
    print(f"        Net Savings:  EUR {winner['Savings (EUR)']:,.2f} over flat rule (EUR {winner['Savings (EUR)'] / 8:,.2f} / month)")
    print(f"        Walk Rate:    {winner['Walks/1,000']:.2f} per 1,000 arrivals (Ceiling <= 10.0: {'PASS' if winner['Ceiling Met'] else 'BREACHED'})")

    # 6. Save chosen model and artifacts
    chosen_package = {
        "model_name": winner_name,
        "model": methods[winner_name]["model_obj"],
        "preprocessor": preprocessor,
        "buffer": winner_buffer,
        "bin1_features": get_bin1_features(train_df).columns.tolist(),
        "proof_metrics": winner,
    }
    joblib.dump(chosen_package, CHOSEN_MODEL_PATH)
    print(f"\n[OK] Chosen model and frozen buffer exported to: {CHOSEN_MODEL_PATH}")

    evidence_dir = SRC_DIR.parent / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(evidence_dir / "backtest_results.csv", index=False)
    print(f"[OK] Backtest table evidence saved to: {evidence_dir / 'backtest_results.csv'}")

    return results_df


if __name__ == "__main__":
    run_backtest()