# What is the project, in one page?

**Owner:** Client Lead. **Closes:** ladder stages 0 and 1. **Length:** one page. **Version 0** is written on paper on Tuesday, with no AI, and typed in here before any AI tool is opened.

Answer each question in one to three sentences. The worked example comes from a different business on purpose (home sample collection at a diagnostics chain, with made-up numbers), so it shows the standard of an answer without giving you the hotel's.

### 1. Who is the client, and who pays whom?

> **Worked example.** The client is the home-collection unit of a diagnostics chain. Patients pay per test (B2C); partner hospitals and corporate health camps pay on monthly invoices (B2B). We are the analytics vendor, and the unit head renews us only if idle phlebotomist slots fall.

**Our answer:**
The client is the Director of Revenue of a two-hotel group in Portugal (a Lisbon city hotel and an Algarve resort). Guests pay either directly or through OTAs (B2C); tour operators, groups, and corporate desks pay negotiated rates or block invoices (B2B). We are RateGain's revenue science squad, and the client renews our contract only if our cancellation-aware overbooking policy reduces euro losses from empty rooms without violating the guest walk ceiling.

### 2. Who decides, how often, and what does one wrong call cost in each direction?

> **Worked example.** The city operations lead fixes each route's bookings every evening for the next morning. An empty slot costs about Rs 450 of phlebotomist time and fuel. A patient we cannot reach in time costs about Rs 600 in a voucher and a rebooking, plus a complaint.

**Our answer:**
The hotel revenue manager decides every morning for each hotel and each of the next 14 arrival nights how many rooms beyond physical capacity ($k$) to keep selling. An undersell decision ($k < \text{cancellations}$) leaves rooms empty at a cost equal to the night's average booked stay value ($\text{ADR} \times \text{nights}$, averaging ~€358). An oversell decision ($k > \text{cancellations}$) walks arriving guests to competitor hotels at a direct cost of €300 per walked guest, risking rejection if the rate exceeds 10 walks per 1,000 arrivals.

### 3. What is decided, from what is known when, about which outcome?

> **Worked example.** How many extra visits to book on each route for tomorrow morning, from the bookings known at the end of today, about how many booked patients will not be there when the phlebotomist arrives.

**Our answer:**
How many rooms beyond capacity to oversell for each hotel on each arrival night, determined from the active bookings on the books using only features known on booking day (Bin 1), about how many currently booked guests for that arrival night will cancel or no-show before check-in.

### 4. What is the unit of decision, and why that unit?

> **Worked example.** The route-morning: one phlebotomist, one morning, about 12 slots. The overbooking is set per route, so per-patient answers are only useful once they are added up per route.

**Our answer:**
The hotel-arrival night: one property on one calendar arrival date. Overbooking is executed at the total hotel capacity level across inventory channels; cancellations and room allocations pool across all arrivals for that night, so individual per-booking cancellation probabilities only become actionable when aggregated to the night.

### 5. What are the north star and the guardrail?

_Give each one a numerator, a denominator, a window and the exclusions. Draw the metric tree underneath: the north star at the top, the two costs below it, the guardrail beside it._

> **Worked example.** North star: idle slots per route-morning, averaged over a calendar month, excluding routes the lab cancelled. Guardrail: patients turned away per 1,000 completed visits, per calendar month, all routes, at most 5.

**Our answer:**
- **North Star Metric:** Total net cost of cancellation errors in euros (€).
  - Numerator: $\sum (\text{empty rooms} \times \text{stay value}) + \sum (\text{walked guests} \times €300)$
  - Denominator: Total arrival nights in the evaluation window
  - Window: Scored split period (Train: < 2016-07-01; Choose: 2016-07-01 to 2016-12-31; Proof: 2017-01-01 to 2017-08-31)
  - Exclusions: Nights with zero scheduled arrivals.
- **Guardrail Metric:** Walk rate per 1,000 realized arrivals.
  - Numerator: Total walked guests = $\sum \max(0, k - \text{cancelled})$
  - Denominator: Total arriving guests = $\sum (\text{book} - \text{cancelled})$
  - Window: Scored evaluation split window
  - Exclusions: Nights with zero arrivals
  - Constraint: Strict ceiling $\le 10.0$ walks per 1,000 arrivals (exceeding this rejects the model regardless of savings).

Metric Tree:
```
                      [Total Error Bill (€)] (North Star - Minimize)
                             /         \
                            /           \
              [Empty Room Cost]       [Walk Penalty Cost]
            (empty rooms × stay_val)    (walks × €300)
                                              |
                                  [Walk Rate ≤ 10 / 1,000] (Guardrail)
```

### 6. Which numbers in the brief did we check, and what did the data say?

_Every number in the brief gets a row. A number you could not check gets a question to the client instead._

> **Worked example.**
>
> | Number in the brief | What we checked | What the data said | What we do about it |
> |---|---|---|---|
> | "A home visit takes 20 minutes" | Median time from arrival to sample scan | 26 minutes; 20 is the planned slot length | Plan on the record, not the plan |

| Number in the brief | What we checked | What the data said | What we do about it |
|---|---|---|---|
| "About one booking in four is cancelled" (~25%) | `df['is_canceled'].mean()` across all 119,390 bookings | **37.04%** cancelled (44,224 bookings; City: 41.73%, Resort: 27.76%) | **Brief number is wrong.** Calibrate baselines and prior rates to 37.04%, not 25%. |
| "119,390 bookings and 32 columns" | `df.shape` of raw export via `src/data.py` | Exactly 119,390 rows and 32 columns | Verified; data pipeline matches exact export schema. |
| "Train < 1 July 2016, choose July–Dec 2016, prove Jan–Aug 2017" | Row counts per split date via `src/contract.py` | Train: 49,157 bookings (35.77% cancel); Choose: 29,546 (36.87% cancel); Proof: 40,687 (38.70% cancel) | Use exact time splits; tune buffers strictly on Choose; freeze and run Proof once. |
| "A guest walked costs EUR 300" | Checked against `src/contract.py` constant `WALK_COST` | `WALK_COST = 300.0` euros | Implemented as fixed constant in error bill computation. |
| "Brand standard at most 10 walked guests per 1,000 arrivals" | Checked against `src/contract.py` constant `WALK_CEILING` | `WALK_CEILING = 10.0` per 1,000 arrivals | Implemented as strict boolean filter in evaluation (`ceiling_met`). |
| "Finance says most prepaid non-refundable bookings never turn into a stay" | `df.groupby('deposit_type')['is_canceled'].mean()` | **99.36%** of 'Non Refund' bookings cancel (14,494 of 14,587 cancel; 99.32% in Groups, 99.94% in Offline TA/TO) | Finance is correct. Treat non-refundable deposits as near-certain cancellations from tour operator blocks. |
| "Vendor showed 95% accuracy" | Evaluated classification accuracy vs business money metric | Accuracy ignores class imbalance and asymmetric error costs (€300 walk vs €358 stay) | Reject classification accuracy; evaluate strictly by total euro cost under 10/1,000 ceiling. |

### 7. What is out of scope?

> **Worked example.** Pricing of home visits, phlebotomist hiring, and routes outside the three metro cities.

**Our answer:**
Dynamic ADR pricing, per-booking direct intervention or guest-level front desk rejections, room-type upgrades/reassignments, and seasonal staffing or physical capacity expansion.

### 8. Who owns what on this team?

| Role | Name | Owns |
|---|---|---|
| Client Lead | Harshal | `docs/CHARTER.md`, `docs/RFP.md`, Slides 1, 2, 3, 10, business metrics |
| Data Lead | Gurunath | `docs/COLUMNS.md`, `src/features.py`, AI benchmark comparison, `docs/DECISIONS.md` |
| Model Lead | Vysag | `src/backtest.py`, 4 methods table, buffer selection on choose split, Slides 5, 6 |
| Build Lead | Mihir | `docs/PRD.md`, `docs/BUILD_PLAN.md`, `src/nightly.py`, `AGENTS.md`, Slides 7, 8 |

### 9. What is the one question we are sending the client?

> **Worked example.** "Is a no-show recorded by the phlebotomist at the door, or by the call centre the next day?"

**Our answer:**
"When a group booking with a 'Non Refund' deposit cancels, does the hotel retain 100% of the room revenue as a non-refundable penalty fee, and if so, should those revenues be credited against the empty-room loss calculation in the net revenue accounting?"
