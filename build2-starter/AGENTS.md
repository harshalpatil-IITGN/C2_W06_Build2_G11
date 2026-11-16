# Instructions for coding agents

Follow these rules whenever you work in this project.

## project rules

1. **Protect the client's scoring rule.** Read `src/contract.py` and use it as provided. Do not change its formulas, costs, time splits, or walk ceiling.
2. **Use the hotel-night as the decision unit.** Produce and evaluate one oversell recommendation for each hotel and arrival night; aggregate booking-level probabilities to that level.
3. **Prevent target leakage.** Use only features approved in the first bin of `docs/COLUMNS.md` for the MVP. Never use `is_canceled` or other after-outcome fields as prediction inputs.
4. **Respect the chronological evaluation.** Fit on Train, choose model settings and the buffer on Choose, and keep Proof held back until the final evaluation. Do not tune from Proof results.
5. **Keep training and nightly inference consistent.** Use the same feature preparation and oversell/buffer policy in `src/backtest.py` and `src/nightly.py`.
6. **Freeze the selected method for nightly runs.** `src/nightly.py` must load the model and buffer saved by the backtest; it must not train or tune them.
7. **Judge methods by the client's business rule.** Compare methods on the same nights and report euros, empty rooms, walked guests, and walks per 1,000. A method above the 10-walks-per-1,000 ceiling is unacceptable, even if its euro cost is lower.
8. **Keep data decisions traceable.** Do not silently drop rows, fill values, change categories, or alter features. Record data-cleaning and feature decisions, their reasons, and affected row counts in `docs/DECISIONS.md`.
9. **Make changes easy to review.** Keep the implementation small and focused. Do not edit unrelated files or add dependencies without a clear project need.

## Coding guidelines

- **Think before coding.** Read the relevant files related to this project, understand the expected behavior, and state assumptions that affect the result.
- **Prefer the simplest working change.** Avoid extra abstractions, frameworks, dependencies, and features that the assignment does not need.
- **Make focused edits.** Change only what is needed for the requested behavior. Preserve existing conventions and avoid unrelated refactoring.
- **Work toward a clear outcome.** Define what success looks like, implement toward it, and report what changed and what remains unresolved.
- **Handle uncertainty honestly.** Ask the team when an unresolved product or model decision changes the behavior; do not invent business rules.
- **Keep outputs reproducible.** Use explicit inputs and settings, deterministic choices where practical, and clear errors when required files or columns are missing.
- **Do not claim checks you did not run.** Report the exact commands and results when asked to verify a change.

## Required project commands

Run these from the repository root when the related code is ready:

```bash
python src/backtest.py
python src/nightly.py --from 2017-08-18 --nights 14
```

`src/contract.py` is the evaluation source of truth. If another project document conflicts with its implemented scoring rule, flag the conflict for the team instead of changing the contract.
