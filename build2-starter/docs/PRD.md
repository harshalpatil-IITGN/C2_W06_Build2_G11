# What exactly are we building, and why this way?

**Owner:** Build Lead. **Closes:** ladder stages 3 and 5. **Length:** two pages and one diagram.

Write the options section on Wednesday, before the method table exists, and update it once the table is in. The architecture goes in on Thursday.

### 1. Who uses it, when, and what do they do with it?

> **Worked example.** The city operations lead opens the route table every evening, before routes are fixed, and adds the extra visits route by route. They overrule a route when a camp is cancelled at short notice.

**Our answer:**

<!-- answer:3 -->

### 2. Which two ways could we decide, what does each cost, which do we choose, and what would flip it?

> **Worked example.** (a) A lookup table: the failure rate by booking channel and lead-time band, summed per route. Half a day to build, nothing to retrain. (b) A learned model of each booking's chance of failing, summed per route. Two days to build, retrained monthly. We choose (b) because it cuts idle slots by a further 9% with the guardrail met; we would flip to (a) if the gap fell under 3% on the next quarter's data.

**Our answer:**

<!-- answer:4 -->

### 3. What is our answer to the wish-list item?

_One paragraph with a number. Say which method the item would need and whether its output would change any number the client acts on._

**Our answer:**

<!-- answer:3 -->

### 4. What exactly is in the table the client reads?

> **Worked example.** One row per route and morning: route, date, slots booked, expected failures, buffer, extra visits to book, and a one-line reason.

**Our answer:**

<!-- answer:2 -->

### 5. Which inputs do we use, by bin?

_Point to `docs/COLUMNS.md` and list here only the columns the method reads, each with its bin._

**Our answer:**

<!-- answer:3 -->

### 6. Where do the numbers come from, and how is the buffer set and frozen?

> **Worked example.** Each booking gets a probability of failing; the probabilities are summed per route; the buffer is the number of slots subtracted from that sum, chosen on the choose period as the cheapest buffer that keeps the guardrail, then frozen for the proof period.

**Our answer:**

<!-- answer:3 -->

### 7. What is the error bill on the proof period?

_Euros, rooms and walks per 1,000 for the chosen rule and for the client's flat rule, from `python src/backtest.py`._

| Rule | Empty rooms | Walked guests | Walks per 1,000 | Cost (EUR) | Saving a month against the flat rule (EUR) |
|---|---|---|---|---|---|
| Client's flat rule | | | | | 0 |
| Our chosen rule | | | | | |

### 8. What does the system look like, first as a black box and then inside?

_Two drawings. The black box: what goes in, what comes out, who reads it. The white box: every step from the bookings file to the table, with the file or function that does it. Then list what production would add._

**Our diagram:** `docs/architecture.png`

**What production would add:**

<!-- answer:3 -->

### 9. What are the limits?

> **Worked example.** Runs in under five minutes on a laptop; every number has a one-line reason; no patient name leaves the lab's systems.

**Our answer:**

<!-- answer:2 -->

### 10. What could go wrong?

> **Worked example.** Camps cancelled at short notice cluster on the same routes; the failure rate drifts after a price change; route leads stop trusting the table after one bad morning.

**Our answer:**

<!-- answer:3 -->

### 11. What is out of scope?

**Our answer:**

<!-- answer:2 -->
