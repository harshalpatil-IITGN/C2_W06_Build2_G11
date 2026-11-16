# AI Session Log — Model Lead Audit, Backtest Fix & Nightly MVP

- **Date:** 2026-11-17
- **Role:** Model Lead (Vysag) — covering Data Lead Bin 1 audit & Build Lead nightly MVP
- **Tool:** Gemini
- **Branch:** `vysag/model-and-nightly-mvp`

## Summary of Prompts & Decisions

1. **Codebase & PRD Audit (`src/features.py`, `src/backtest.py`, `src/nightly.py`):**
   - Audited the 32-column dataset (`hotels.csv`) in VS Code Data Wrangler and verified the three-bin temporal split (Bin 1 fixed at booking; Bin 2 amendable; Bin 3 post-outcome leakage quarantined).
   - Identified a discrepancy between `docs/PRD.md` Section 5 and `src/features.py`: `total_of_special_requests` was listed in the PRD as a Bin 1 numeric feature but omitted from `NUMERIC_FEATURES`. Fixed in commit `7b71e8c`.

2. **Enforcing Strict No-Peeking Evaluation (`src/backtest.py`):**
   - Identified that model winner selection was previously filtering `Ceiling Met` on the held-out Proof period (`2017`) rather than selecting strictly on the Choose period (`2016 H2`).
   - Added `roc_auc_score` (AUC) and nightly room `mean_absolute_error` (MAE) to the comparative evaluation table as required by Slide 5 and the Stage 4 rubric.
   - Observed an important empirical result: Gradient Boosting (`b* = -2`) won on the 2016 Choose period (`8.26` walks/1,000) but drifted to `12.35` walks/1,000 on 2017 (breaching the `<= 10.0` ceiling), whereas Logistic Regression (`AUC = 0.823`, `b* = -3`) stayed safely inside the ceiling at `7.30` walks/1,000 and saved `EUR 1,727,698.41` (`EUR 215,962.30 / month`). Committed in `388de3e`.

3. **Nightly Engine Volatility Status & PRD Sync (`src/nightly.py`, `docs/PRD.md`):**
   - Added the spread-based `volatility_status` column ($\sigma = \sqrt{\sum p_i(1-p_i)} \ge 3.5$) to the morning overbooking table and synced Section 7 of `docs/PRD.md` with the proved results. Committed in `3a500b6`.