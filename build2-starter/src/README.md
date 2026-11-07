# What lives in src, and who writes it?

| File | Status | Owner | Its one job |
|---|---|---|---|
| `data.py` | Given | | Download the bookings and read them exactly as exported |
| `contract.py` | Given, never edited | | The client's scoring rule |
| `features.py` | Yours | Data Lead | Clean the bookings and return the columns your methods may use, with every choice logged in `docs/DECISIONS.md` |
| `backtest.py` | Yours | Model Lead | Fit every method on the train period, choose each buffer on the choose period, run the proof once, print the method table, and save the chosen method and its buffer to `models/`, which you commit |
| `nightly.py` | Yours | Build Lead | Read a bookings file and the saved method, and write the oversell table for the nights asked for |

The project ends with these two commands working from a fresh Codespace. Commit `models/` after the final `backtest.py` run, so that `nightly.py` runs from a fresh checkout without retraining, which is how slide 7 runs live:

```bash
python src/backtest.py
python src/nightly.py --from 2017-08-18 --nights 14
```
