# How do we get from a first test to something the client can run?

**Owner:** Build Lead. **Closes:** ladder stages 4 and 6. **Length:** one page.

Three stages, each with an owner, an hour budget, a line that says when it is done, and the file that proves it. Fill the table on Wednesday morning and update the hours as you go.

| Stage | What is built | Owner | Hours planned | Hours used | Done when | Evidence file |
|---|---|---|---|---|---|---|
| POC | | | | | Every method you tried prints from `python src/backtest.py` on the proof period, scored by `src/contract.py`, with the ceiling checked | |
| MVP | | | | | `python src/nightly.py --from 2017-08-18 --nights 14` writes the nightly table from a bookings file, reading only first-bin columns, signed by the challenger | |
| Final | | | | | The uncertainty buffer is compared with the rooms buffer, the full-night caveat is computed, and the roadmap is written | |

In the team of three, the final stage is the full-night caveat and the roadmap, because the uncertainty buffer is excused.

> **Worked example (one row, home collection).** POC: a lookup table and a learned model, each summed per route and scored on the held-back months. Owner: Model Lead. Planned 9 hours, used 11. Done when one command prints both against today's rule. Evidence: `src/backtest.py` and `evidence/poc_table.png`.

## What would production add that the MVP leaves out?

_One line each, with the role that would own it and an hour estimate. These become the roadmap._

| Addition | Why it matters | Owner | Hours |
|---|---|---|---|
| | | | |

## What did we cut, and why?

_Anything you planned and dropped, with the reason. A cut you explain is not a gap._

<!-- answer:3 -->
