# Minimum Viable Product (MVP): Hotel Overbooking Recommendations

## 1. Executive summary

Build a small, reproducible command-line tool that turns a bookings file and a previously selected cancellation model into a 14-night table of room-overbooking recommendations. For every hotel-arrival night, the tool estimates how many booked guests will cancel, applies a safety buffer selected during validation, and recommends a non-negative integer number of rooms to sell beyond capacity.

The business objective is to reduce the cost of rooms left empty after cancellations while respecting the client’s strict limit of **10 walked guests per 1,000 realized arrivals**. The client’s scoring contract assigns **€300 per walked guest** and values an empty room using that night’s average booked stay value. The walk limit is a hard acceptance constraint: a lower euro cost does not make a method acceptable if it exceeds the limit.

The MVP is complete when a fresh checkout can run `src/nightly.py` using the committed saved method and buffer, without fitting or tuning a model, and write the requested table using only approved booking-time inputs.

## 2. The user problem and user story

**User story**: As a hotel revenue manager, before setting inventory limits, I want a clear oversell recommendation for each hotel and each of the next 14 arrival nights, so that I can reduce rooms lost to cancellations while controlling the risk of walking arriving guests.

**Current alternative:** A flat rule based on a hotel’s historical cancellation rate and a fixed safety reduction. That rule provides little night-level risk differentiation.

**Product decision:** For night `t` at hotel `h`, recommend an integer `k(h,t) >= 0`: the number of rooms beyond physical capacity that may be sold. The unit is the hotel-night because room capacity and the client’s error bill are evaluated at that pooled level; booking-level probabilities are inputs to this decision, not the final action.

## 3. Product goals:

### Goals

1. Produce an actionable recommendation table for a requested date range, with one row per hotel and arrival night.
2. Use a frozen, reproducible method chosen using the project’s time-based train/choose/proof protocol.
3. Keep post-outcome information out of model inputs.
4. Make recommendations traceable to expected cancellations and a saved safety buffer.
5. Report model performance in business terms: euros, empty rooms, walked guests, and walks per 1,000 arrivals.

## 4. MVP scope and workflow

### Inputs

- The project bookings CSV, loaded through the provided data pipeline.
- The requested first arrival date and number of nights.
- The agreed feature transformation implemented by `src/features.py`.

The model may use only columns audited as known and fixed at booking (Bin 1 in `docs/COLUMNS.md`). non required fields are excluded from the MVP for a stable, conservative feature contract. Fields written after the outcome, including `is_canceled`, are labels or evaluation fields only and must never be model inputs. The exact final feature list is owned by the Data Lead’s column audit and must match `src/features.py`.

### Runtime flow:
1. Parse and validate the command-line date and night count.
2. Load the bookings and saved model configuration; fail with a readable error if required files or fields are missing.
3. Select bookings for the requested arrival dates and prepare model inputs using the shared feature code.
4. Predict cancellation probability `p_i` for each booking in the selected night’s book.
5. Aggregate by hotel and arrival date:
   - Expected cancellations: `mu = sum(p_i)`.
   - Independent-booking spread estimate: `sigma = sqrt(sum(p_i * (1 - p_i)))`.
6. Apply the chosen method’s frozen buffer to calculate a non-negative integer oversell recommendation. The formula and rounding rule must be identical to the one Vaysag evaluates in `src/backtest.py`; do not independently invent a second policy in `nightly.py`.
7. Write the recommendation table to a documented output path (CSV by default) and print a concise success message and row count.

**Required invocation:**

```bash
python src/nightly.py --from 2017-08-18 --nights 14
```

### Required output

One row per hotel and requested arrival night, with at least:

| Field | Meaning |
|---|---|
| `arrival_date` | Arrival calendar date |
| `hotel` | Property identifier (city or resort) |
| `book` | Number of bookings represented in the input for that night |
| `expected_cancellations` | Sum of predicted cancellation probabilities |
| `buffer` | Frozen non-negative room buffer selected on the Choose period |
| `recommended_oversell` | Final whole-number `k`, at least zero |

The PRD may include `spread` and a short volatility explanation if the implementation supports them. Do not imply that spread is a guarantee or that individual cancellation outcomes are independent; independence is only the contract’s spread calculation assumption.

## 5. Model and decision design

### Prediction target

For each booking, predict `is_canceled` as a binary outcome using only permitted booking-time data. This dataset’s `is_canceled` label includes cancellations and no-shows as defined by the project contract. The product does not make a guest-level action. It aggregates booking probabilities to estimate cancellation volume for a hotel-night.

### Candidate methods to compare

The team’s backtest should compare these methods on the same scored hotel-nights under the unchanged `src/contract.py`:

1. **Client flat rule:** hotel-specific cancellation rate calculated on Train, multiplied by that night’s book, then adjusted by a safety margin selected on Choose.
2. **Lookup baseline:** historical cancellation rates for an agreed set of stable segments (e.g. hotel, arrival month, and market segment), with sparse cells backed off to a broader rate. Specify the minimum support and fallback rule before proof.
3. **Logistic Regression:** interpretable probabilistic baseline. Use a preprocessing pipeline for categorical and numeric fields, and deterministic settings. It is a useful benchmark because its probability output is naturally linked to log loss; still assess calibration on held-out time data.
4. **Histogram Gradient Boosting classifier:** nonlinear candidate that can learn interactions and nonlinear effects. Scikit-learn documents probability output through `predict_proba`; categorical encoding and missing-value handling must be explicit and consistent with the installed version.

These are candidate methods, not a claim that one will win. The selected model must be the method supported by your measured Choose and Proof results. If the project’s installed dependencies or team implementation use another learned method, record the reason and compare at least two learned methods as the rubric requires.

## 6. Data protocol and evaluation

Use the supplied time split by arrival date:

| Period | Dates | Permitted use |
|---|---|---|
| Train | Before 2016-07-01 | Fit preprocessing and candidate models; estimate baseline rates |
| Choose | 2016-07-01 through 2016-12-31 | Select model settings and the integer buffer; check the walk ceiling |
| Proof | 2017-01-01 through 2017-08-31 | One final evaluation after freezing decisions |

The evaluation contract defines the per-night cost. If `A` is cancellations, `k` is oversell, and `V` is mean booked stay value for the night:

- Empty rooms: `max(A - k, 0)`.
- Walked guests: `max(k - A, 0)`.
- Night cost: `empty_rooms * V + walked_guests * €300`.
- Period walk rate: `1,000 * total_walked / total_realized_arrivals`.
- Acceptability: period walk rate must be at most 10 per 1,000.

Every method must score the same nights and use the same client contract. Report the flat-rule baseline beside the selected rule. On Proof, show euros, empty rooms, walked guests, walks per 1,000, ceiling status, and saving versus the flat rule. Do not change the model, buffer, or feature rules after seeing Proof without disclosing both runs, as required by the evaluation contract.

## 7. Functional requirements

- **FR1:** Accept `--from` and `--nights` arguments and validate them.
- **FR2:** Load model and buffer saved by the final backtest; do not fit or tune in the nightly command.
- **FR3:** Reuse the same feature preparation used by model training.
- **FR4:** Reject missing required model artifacts, columns, or invalid dates with an actionable error.
- **FR5:** Use only the approved first-bin feature columns for prediction.
- **FR6:** Produce one output row for each hotel-night represented in the requested horizon, including zero-book nights if the agreed product contract requires them; document the chosen behavior.
- **FR7:** Output the required fields in a stable, documented CSV format.
- **FR8:** Ensure probabilities are finite and within `[0, 1]`, and `recommended_oversell` is a non-negative integer.
- **FR9:** Include a reproducibility note (model artifact/version and buffer) in logs or metadata without exposing guest-identifying information.

## 8. Non-functional requirements

- Runs locally from the repository root with documented dependencies.
- Deterministic output for identical input, saved artifact, and package environment.
- No network call required during nightly inference.
- No guest names or direct personal identifiers in output; use only the anonymized project dataset.
- Clear separation between training/backtesting (`src/backtest.py`) and inference (`src/nightly.py`).
- Fast enough for the small course dataset; no premature infrastructure or service deployment.

## 9. Acceptance criteria / definition of done

The MVP is accepted when all of the following are true:

1. `python src/backtest.py` compares the client flat rule, lookup baseline, and at least two learn ed methods under the provided contract.
2. Model fitting uses Train; model/buffer selection uses Choose; the Proof result is generated only after decisions are frozen.
3. The backtest writes the chosen model and buffer to committed artifacts under `models/`.
4. `python src/nightly.py --from 2017-08-18 --nights 14` completes from a fresh checkout without retraining and writes the 14-night output table.
5. Prediction uses only features allowed by `docs/COLUMNS.md`; the target and post-outcome columns are excluded.
6. The nightly policy and backtest policy implement the same buffer and integer conversion.
7. The evaluation reports euros, rooms, walks, and the walk-rate ceiling beside the flat baseline.
8. The Build Lead’s challenger reviews the pipeline, confirms it matches the feature audit and PRD, and records the checked commit hash in `README.md`.
9. Evidence for the presentation is saved in `evidence/`; the architecture diagram matches the implemented files and functions.

The rubric does not require the learned model to beat every baseline to earn credit; it requires an honest, reproducible comparison and correct application of the business rule. Do not claim success until actual results support it.

## 10. Risks, assumptions, and limitations

| Risk or assumption | Product response |
|---|---|
| Late columns can leak the outcome | Enforce the column audit; use only first-bin inputs in MVP. |
| Cancellation patterns shift by season, hotel, or channel | Use chronological evaluation; report hotel-level and period limitations; propose monitoring as future work. |
| Cancellation events may be correlated (e.g. group blocks) | Treat independent Bernoulli spread as a simplifying estimate; note group-level correlation as a limitation. |
| Segment lookup cells may be sparse | Predefine minimum support and a fallback to broader rates; log the decision. |
| Probability ranking may not imply good calibration | Inspect calibration and nightly cancellation-count error where feasible; select on the contractual cost and ceiling. |
| The dataset reflects two anonymized Portuguese properties and historical bookings | Do not claim direct generalization to other hotels or current operations without fresh validation. |
| Proof uses final booking books, not actual information available each morning | State the full-night caveat; a live product needs timestamped booking snapshots and rolling re-evaluation. |
| `k` may be misunderstood as a guaranteed safe limit | Label it a recommendation under historical evidence, not a guarantee; the manager remains accountable for inventory decisions. |


Before implementation, agree on the artifact format, feature function signature, model positive-class probability convention, buffer field name, output path, and whether absent hotel-night combinations should be emitted. Record final decisions in the relevant project documents.

## 12. Build sequence

1. Confirm interface decisions with the Data and Model Leads.
2. Complete the POC/backtest comparison and freeze method plus buffer using Choose data.
3. Save and commit the model artifact/configuration.
4. Implement the nightly command around the shared feature and inference interfaces.
5. Run the required commands and reconcile the nightly policy with the backtest.
6. Capture command/output evidence; update PRD, build plan, architecture, and README sign-off.
7. Present the system with the full-night caveat and measured Proof results.

