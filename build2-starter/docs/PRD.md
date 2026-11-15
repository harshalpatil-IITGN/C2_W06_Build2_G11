# What exactly are we building, and why this way?

**Owner:** Build Lead. **Closes:** ladder stages 3 and 5. **Length:** two pages and one diagram.

Write the options section on Wednesday, before the method table exists, and update it once the table is in. The architecture goes in on Thursday.

### 1. Who uses it, when, and what do they do with it?

> **Worked example.** The city operations lead opens the route table every evening, before routes are fixed, and adds the extra visits route by route. They overrule a route when a camp is cancelled at short notice.

**Our answer:**
The Revenue Manager at each property opens the 14-night overbooking table every morning at 08:00 AM before daily channel inventory allocations sync with distribution channels (OTAs, GDS, and direct hotel engines). They review the recommended oversell number ($k$) for each of the next 14 arrival dates and update room availability limits in the property management system (PMS) channel manager. They overrule a recommendation only when emergency inventory blocks occur (e.g. unexpected maintenance or late-arriving group contract changes) and log the reason in the PMS audit log.

### 2. Which two ways could we decide, what does each cost, which do we choose, and what would flip it?

> **Worked example.** (a) A lookup table: the failure rate by booking channel and lead-time band, summed per route. Half a day to build, nothing to retrain. (b) A learned model of each booking's chance of failing, summed per route. Two days to build, retrained monthly. We choose (b) because it cuts idle slots by a further 9% with the guardrail met; we would flip to (a) if the gap fell under 3% on the next quarter's data.

**Our answer:**
(a) A lookup table: historical cancellation rates binned by hotel property, arrival month, and market segment, multiplied by the night's active booked volume. Cost: half a day to build, 0ms compute, zero retraining infrastructure. (b) A learned probabilistic model (e.g. Logistic Regression / LightGBM) predicting each individual booking's cancellation probability from Bin 1 features, summed per night to produce expected cancellations $\mu$ and binomial variance $\sigma^2$, with an integer safety buffer $b$ calibrated on the Choose period to enforce the $\le 10/1,000$ walk ceiling. Cost: two days to build, under 1 second nightly inference, retrained quarterly. We choose (b) because individual booking attributes (lead time, deposit type, ADR, country) capture high cross-segment variance that flat segment averages miss, significantly lowering empty room losses while rigorously meeting the walk ceiling; we would flip to (a) if the proof-period cost saving of (b) over (a) fell under €1,500 per month.

### 3. What is our answer to the wish-list item?

_One paragraph with a number. Say which method the item would need and whether its output would change any number the client acts on._

**Our answer:**
The marketing team's wish-list item ("finding hidden guest types") requires an unsupervised customer segmentation method, such as K-Means clustering or Latent Class Analysis across lead times, party sizes, and special requests. We recommend keeping this out of the nightly overbooking engine: unsupervised clustering produces descriptive behavioral personas (e.g. 4 latent customer clusters), but it changes zero numbers that the revenue manager acts on because nightly overbooking depends strictly on the sum of cancellation probabilities and pooled hotel capacity. Adding a clustering pipeline introduces operational complexity and runtime latency without saving a single euro on the proof period; marketing segmentation should run as an offline quarterly CRM study.

### 4. What exactly is in the table the client reads?

> **Worked example.** One row per route and morning: route, date, slots booked, expected failures, buffer, extra visits to book, and a one-line reason.

**Our answer:**
One row per hotel and arrival night across the next 14 nights: arrival date, hotel, active booked rooms, expected cancellations ($\sum p_i$), safety buffer ($b$), recommended oversell rooms ($k = \max(0, \text{round}(\mu - b))$), and a one-line volatility status based on the night's spread ($\sigma = \sqrt{\sum p_i(1-p_i)}$).

### 5. Which inputs do we use, by bin?

_Point to `docs/COLUMNS.md` and list here only the columns the method reads, each with its bin._

**Our answer:**
As audited in `docs/COLUMNS.md`, we strictly read Bin 1 columns (known on booking day and fixed): `hotel`, `lead_time`, `arrival_date_year`, `arrival_date_month`, `arrival_date_day_of_month`, `stays_in_weekend_nights`, `stays_in_week_nights`, `adults`, `children`, `meal`, `country`, `market_segment`, `distribution_channel`, `is_repeated_guest`, `previous_cancellations`, `previous_bookings_not_canceled`, `reserved_room_type`, `deposit_type`, `customer_type`, `adr`, and `total_of_special_requests`. All Bin 2 amendable columns (`agent`, `company`, `days_in_waiting_list`, `required_car_parking_spaces`) are excluded from MVP inputs. Bin 3 columns (`is_canceled`, `assigned_room_type`, `booking_changes`, `reservation_status`, `reservation_status_date`) are strictly quarantined as target leakage.

### 6. Where do the numbers come from, and how is the buffer set and frozen?

> **Worked example.** Each booking gets a probability of failing; the probabilities are summed per route; the buffer is the number of slots subtracted from that sum, chosen on the choose period as the cheapest buffer that keeps the guardrail, then frozen for the proof period.

**Our answer:**
Each active booking receives a cancellation probability $p_i$ from the model trained on arrivals before 1 July 2016. Probabilities are aggregated per hotel-night via `src/contract.py` to yield expected cancellations $\mu = \sum p_i$. The safety buffer $b$ is selected on the Choose period (July to December 2016) by grid-searching the buffer that minimizes total euro error cost subject to walk rate $\le 10.0$ per 1,000 arrivals. Once selected, $b$ is frozen and applied without modification to the proof period (January to August 2017).

### 7. What is the error bill on the proof period?

_Euros, rooms and walks per 1,000 for the chosen rule and for the client's flat rule, from `python src/backtest.py`._

| Rule | Empty rooms | Walked guests | Walks per 1,000 | Cost (EUR) | Saving a month against the flat rule (EUR) |
|---|---|---|---|---|---|
| Client's flat rule | TBD | TBD | TBD | TBD | 0 |
| Our chosen rule | TBD | TBD | TBD | TBD | TBD |

*(Note: Populated automatically when `python src/backtest.py` executes on the proof period during POC stage).*

### 8. What does the system look like, first as a black box and then inside?

_Two drawings. The black box: what goes in, what comes out, who reads it. The white box: every step from the bookings file to the table, with the file or function that does it. Then list what production would add._

**Our diagram:** `docs/architecture.png`

**What production would add:**
(1) Automated real-time PMS API connector instead of static CSV export. (2) Daily monitoring alert when actual walk rate on trailing 30 days exceeds 7.0 per 1,000 arrivals. (3) Role-based override interface logging revenue manager overrides directly to database for retraining feedback.

### 9. What are the limits?

> **Worked example.** Runs in under five minutes on a laptop; every number has a one-line reason; no patient name leaves the lab's systems.

**Our answer:**
Nightly execution completes in under 30 seconds on a standard laptop; operates entirely offline with zero external cloud API dependencies; processes only anonymized PMS booking records with no guest PII (personally identifiable information).

### 10. What could go wrong?

> **Worked example.** Camps cancelled at short notice cluster on the same routes; the failure rate drifts after a price change; route leads stop trusting the table after one bad morning.

**Our answer:**
(1) Lumpy group cancellations: large tour operator groups cancel all at once, creating binomial independence violations (mitigated by tracking group deposit flags). (2) Seasonal regime shift: winter occupancy at Algarve Resort drops dramatically, making overbooking recommendations irrelevant if total demand is far below capacity. (3) Revenue manager mistrust: a single walked guest incident during high season could lead the manager to discard model recommendations and revert to intuition.

### 11. What is out of scope?

**Our answer:**
Dynamic ADR repricing, individual guest-level front desk cancellation rejections, room-type upgrades or reassignment logistics, and long-term physical room capacity adjustments.
