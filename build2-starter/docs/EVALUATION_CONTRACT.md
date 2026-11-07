# How will the client score any rule we propose?

The client scores every proposal the same way, whichever method produced it. `src/contract.py` holds this rule as code. Read it, use it, and do not change it. Everything the rule leaves open is your team's decision.

## What is the unit?

One hotel on one arrival night. A night's book is every booking your team scores whose arrival date is that night.

## What does a rule decide?

The oversell count _k_ for each night: how many rooms beyond capacity to keep selling. It is a whole number, zero or more.

## What does one night cost?

Let _A_ be the number of that night's bookings that cancelled (`is_canceled` = 1, which includes no-shows).

| Quantity | Formula |
|---|---|
| Empty rooms | max(_A_ − _k_, 0) |
| Walked guests | max(_k_ − _A_, 0) |
| Stay value _V_ | the mean of `adr` × `nights` over the night's bookings, where `nights` = `stays_in_weekend_nights` + `stays_in_week_nights` |
| Walk cost _W_ | EUR 300 per walked guest |
| Cost of the night | empty rooms × _V_ + walked guests × _W_ |

## When is a rule acceptable?

Walks per 1,000 arrivals = 1,000 × walked guests ÷ arrivals, over the whole period, where arrivals are the scored bookings that did not cancel. A rule is acceptable only at 10 or fewer. A rule that saves more euros but breaks the ceiling is rejected.

## Which data may we use, and when?

| Period | Arrival dates | What it is for |
|---|---|---|
| Train | before 1 July 2016 | Fit your methods |
| Choose | 1 July 2016 to 31 December 2016 | Pick settings and the buffer, and check the ceiling here |
| Proof | 1 January 2017 to 31 August 2017 | Run once, at the end, and report what happens, walks included |

You may refit on train and choose together before the proof run, as long as you keep every setting you picked. If you change anything after seeing proof results, say so on slide 5 and report both runs.

## What does `src/contract.py` give us?

| Function | What it returns |
|---|---|
| `split_periods(df)` | The train, choose and proof bookings, by arrival date |
| `nightly_table(bookings, prob)` | One row per hotel and night: `book` (bookings due), `cancelled` (what happened), `expected` (the sum of your probabilities), `spread` (the standard deviation of that sum if bookings cancel independently) and `stay_value` (_V_) |
| `night_cost(nights, oversell)` | The cost in euros, empty rooms, walked guests, walks per 1,000, whether the ceiling was met, and the number of nights |

It does not choose which bookings you score, which columns you use, where your probabilities come from, how you turn them into _k_, or your buffer.

## What is the client's current rule?

The flat rule: each hotel's cancellation rate, times the night's bookings, less a fixed number of rooms for safety. Formalise it exactly that way, with its rate taken from the train period and its safety margin chosen on the choose period under the ceiling, the same way you choose your own. Every saving you report is a saving against this rule, never against selling nothing extra.

## What does the client want to read each morning?

One row per hotel and arrival night, for the next fourteen nights: the hotel, the night, the bookings on the book, the expected cancellations, the buffer, and the oversell count. Your PRD may add columns if the revenue manager would use them.

The rule scores each night's final book, meaning every booking ever made for that night, so the fourteen-night run treats every booking as already on the book. Fourteen days before arrival only about half of a night's final book is actually there, so a run that uses only the bookings known on the morning it runs is the natural next step, and your roadmap may name it.

## What must every result report?

Euros, rooms and walks per 1,000, side by side, on the proof period. A euro figure without its rooms and walks is not accepted.
