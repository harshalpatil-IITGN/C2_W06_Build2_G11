# Build Plan: From First Test to Client Production

**Owner:** Build Lead (Mihir Patel). **Closes:** Ladder stages 4 and 6. **Length:** One page.

---

## 1. Development Stages & Evidence Milestones

Three iterative stages executed across the 5-day build cycle. Hours planned vs. actual hours used logged below:

| Stage | What is built | Owner | Hours planned | Hours used | Done when | Evidence file |
|---|---|---|---|---|---|---|
| **POC** | Baseline rules & multi-model comparison engine (`backtest.py`), scikit-learn preprocessor on Bin 1 features, safety buffer grid search. | Model Lead (Vysag) & Data Lead (Gurunath) | 12 | 14 | Every candidate method prints from `python src/backtest.py` on the proof period, scored by `src/contract.py`, with the walk ceiling checked. | [`evidence/backtest_results.csv`](file:///e:/IITGN_Projects/Week_6/C2_W06_Build2_G4/build2-starter/evidence/backtest_results.csv) & `models/chosen_model.joblib` |
| **MVP** | CLI morning desk overbooking engine (`nightly.py`) reading raw CSV and running inference with frozen model package. | Build Lead (Mihir) & Client Lead (Harshal) | 10 | 9 | `python src/nightly.py --from 2017-08-18 --nights 14` outputs 14-night morning desk table with oversell $k$, reading only first-bin columns, signed by challenger. | [`evidence/nightly_recommendation.csv`](file:///e:/IITGN_Projects/Week_6/C2_W06_Build2_G4/build2-starter/evidence/nightly_recommendation.csv) |
| **Final** | Performance metrics notebook (`01_model_performance.ipynb`), multi-night stay caveat evaluation, production roadmap, and presentation defense deck. | Full Squad (All 4 Leads) | 8 | 8 | Uncertainty spread compared with rooms buffer, multi-night stay caveat documented, and production roadmap complete. | [`notebooks/01_model_performance.ipynb`](file:///e:/IITGN_Projects/Week_6/C2_W06_Build2_G4/build2-starter/notebooks/01_model_performance.ipynb) & [`docs/ROADMAP.md`](file:///e:/IITGN_Projects/Week_6/C2_W06_Build2_G4/build2-starter/docs/ROADMAP.md) |

---

## 2. What Would Production Add That the MVP Leaves Out?

The MVP solves single-arrival-night inventory risk. Production deployment requires operational integration:

| Addition | Why it matters | Owner | Hours |
|---|---|---|---|
| **PMS Two-Way Sync API** | Real-time bi-directional connection to Opera PMS to ingest live booking modifications/cancellations and push $k$ limits directly into central reservation distribution. | Build Lead (Mihir) | 20 |
| **Multi-Night Stay Displacement Optimization** | Current contract treats each arrival night independently; multi-night bookings that cancel create inventory holes across multiple future nights requiring joint network-revenue dynamic programming. | Model Lead (Vysag) | 24 |
| **Room-Category Fungibility Engine** | Bookings are assigned to specific room types (Suites vs. Standard). Production must optimize intra-hotel complimentary upgrades before walking guests to competitor hotels. | Data Lead (Gurunath) | 16 |
| **Live Web Dashboard for Desk Managers** | An interactive Streamlit/React morning cockpit displaying confidence bands ($\pm \text{spread}$), audit logs, and one-click manual buffer override toggles. | Client Lead (Harshal) | 14 |
| **Automated Retraining & Concept Drift Pipeline** | Weekly pipeline with evidently/MLflow monitoring macro trends, seasonal shifts, and alert triggers when cancellation behavior shifts significantly. | Build Lead (Mihir) | 18 |

---

## 3. What Did We Cut, and Why?

1. **Cut: Bin 2 Booking Modification Features (e.g., `booking_changes`, `days_in_waiting_list`).**  
   - *Reason:* While Bin 2 features yielded a modest increase in historical AUC in offline experiments, they change dynamically over the booking lifecycle. In the absence of an event-sourced audit table (timestamped change log) in the client's raw feed, using static snapshot counts introduces severe lookahead leakage into a morning inference run. We strictly enforced Bin 1 to guarantee zero data leakage.

2. **Cut: Continuous Intra-Day Dynamic Pricing / Real-Time Re-tuning.**  
   - *Reason:* The client contract evaluates a fixed daily oversell decision ($k$ per hotel-night). Continuous intraday re-optimization adds operational complexity without adding value to the morning desk handoff process.

3. **Cut: Deep Neural Network / TabNet Architectures.**  
   - *Reason:* Tabular tree ensembles (`HistGradientBoostingClassifier`) converged in $< 3$ seconds, required zero GPU hardware, yielded higher calibration stability than deep networks, and export to a lightweight 1.2 MB artifact executable in any standard Python environment.

4. **Cut: Individual Booking Customer Re-targeting.**  
   - *Reason:* GDPR and privacy compliance constraints: the model functions strictly at the inventory aggregate level without storing or processing personally identifiable guest information (PII).
