# What would the client have asked a vendor for, in writing?

**Owner:** Client Lead. **Closes:** ladder stage 2. **Length:** one to two pages.

You write this request for proposal as the client would have issued it, so that both sides agree on what is being bought before anything is built. Vendor teams often draft the request with the client in B2B sales; treat that as the convention here. Keep the client's voice and the client's units: rooms, euros, walks.

### 1. What is the background, in three sentences?

> **Worked example.** Our home-collection unit runs about 300 routes a morning in three cities. Roughly one booked patient in seven is not home when the phlebotomist arrives, and each idle slot costs us about Rs 450. We overbook today by gut feel, route by route.

**Our answer:**
Our hospitality group operates two properties in Portugal—a Lisbon city hotel and an Algarve resort—experiencing an overall cancellation rate of approximately 37%, where cancelled rooms that remain unsold generate zero revenue. Today our revenue managers determine overbooking using a blunt flat formula (average cancellation rate times bookings less a safety buffer), which lacks night-by-night adaptability and costs thousands in vacant rooms. We require a data-driven, cancellation-aware overbooking decision rule proved in euros that optimizes net revenue while strictly safeguarding our brand standard.

### 2. What must the solution do?

_Five lines at most, each one a verb the client can check._

> **Worked example.** (1) Give the number of extra visits to book on each route for tomorrow morning. (2) Run on the bookings file we export at the end of each day. (3) Show the reason for each route's number in one line. (4) Report idle slots and turned-away patients for the past month. (5) Let the operations lead overrule a route and record why.

**Our answer:**
1. **Compute** daily the optimal whole number of rooms beyond capacity ($k$) to oversell for each hotel across the next fourteen arrival nights.
2. **Ingest** only booking characteristics established on booking day, rejecting any data generated post-booking or at check-in.
3. **Minimize** the combined euro cost of unfilled rooms (average stay value) and walked guests (€300 per walk) against our current flat baseline.
4. **Constrain** walked guests strictly to no more than 10 per 1,000 arrivals across all evaluated operational windows.
5. **Output** an automated, single-command morning table for the revenue manager showing recommended oversell levels and expected cancellations.

### 3. How good must it be, and on which period?

_Acceptance thresholds in business units, with the period each is measured on._

> **Worked example.** On the last three months of bookings, held back until the end: idle slots per route-morning at least 25% below today's gut-feel rule, with at most 5 patients turned away per 1,000 completed visits.

**Our answer:**
On the held-out 8-month proof period (1 January 2017 to 31 August 2017), the proposed rule must achieve a total error bill in euros strictly lower than the client's flat-rule baseline, while maintaining a walk rate of at most 10.0 walked guests per 1,000 arrivals. Any rule exceeding 10.0 walks per 1,000 arrivals on this period is categorically disqualified. Model settings and buffers must be frozen on the July–December 2016 period before running on the proof period once.

### 4. Within which limits and rules?

> **Worked example.** Use only what is known when the route is fixed. Patient data stays in our systems. The run takes under five minutes on a laptop. A route lead can read the reason for any number.

**Our answer:**
The decision engine must use only Bin 1 features (known on booking day); no check-in, outcome, or amendable post-booking columns may enter the model. Scoring must strictly follow `src/contract.py` using €300 per walked guest and nightly average stay values. The nightly run must execute in under five minutes on standard hardware without external cloud dependencies.

### 5. What data do we provide?

> **Worked example.** Eighteen months of visit bookings, one row per booking, with the booking channel, slot, pincode, payment type, test panel and outcome.

**Our answer:**
A complete historical dataset of 119,390 booking records across 32 columns covering arrivals from 1 July 2015 to 31 August 2017, containing booking channels, lead times, deposit types, customer classifications, average daily rates, and actual cancellation outcomes.

### 6. How will we judge proposals?

> **Worked example.** On the acceptance thresholds above, then on how clearly the vendor explains a wrong call, then on the cost to run.

**Our answer:**
First on whether the walk rate remains strictly under 10.0 walks per 1,000 arrivals on the proof period; second on net euro savings compared to the flat-rule baseline; third on audit integrity (no data leakage, reproducible pipeline, clear explanation of why simpler or complex models won).

### 7. What is the timeline?

> **Worked example.** A proof of concept in one week, a pilot on one city for a month, then a decision.

**Our answer:**
Five working days: Day 1 paper frame and data audit; Day 2 PRD options and multi-method POC backtest; Day 3 MVP nightly CLI delivery; Day 4 evidence verification and AI benchmark; Day 5 executive presentation and defense.

### 8. What may the vendor ask us?

> **Worked example.** How each outcome is recorded and by whom; which routes changed shape during the period; what a turned-away patient costs beyond the voucher.

**Our answer:**
Whether non-refundable group deposit penalties collected upon cancellation offset empty room losses in accounting; whether walk partner agreements provide guaranteed capacity in high season; and whether overbooking limits differ by individual room categories.

### 9. What is on the wish list?

_Copy the client's wish-list item exactly. Your answer to it belongs in the PRD, not here._

**Our answer:**
Our marketing team would love to find our hidden guest types.
