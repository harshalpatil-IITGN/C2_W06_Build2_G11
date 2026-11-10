# BUILD 2 · DESIGN RATIONALE & PANEL DEFENSE HANDBOOK
> **Author:** Harshal (Client Lead) · Team G4  
> **Audience:** Internal Team Alignment (Harshal, Gurunath, Vysag, Mihir) & Saturday Defense Panel Preparation

---

# PART 1: THE "WHY" BEHIND EVERY DESIGN CHOICE

### 1. Why the Decision Unit is the "Hotel-Arrival Night" (Not the Individual Booking)
- **Business Reality:** A hotel sells physical rooms from a common capacity pool. You cannot preemptively cancel an individual guest's reservation 14 days in advance simply because their predicted cancellation probability is 75%. Doing so violates contract terms, invites consumer litigation, and destroys brand reputation.
- **Pooling & Fungibility:** Once inside the property, standard rooms are fungible inventory. Cancellations pool across the entire hotel for that night. If Guest A arrives and Guest B cancels, Guest A takes the room. The only operational lever the Revenue Manager controls is opening extra rooms to the open market for that calendar arrival date.
- **Statistical Law of Large Numbers:** Individual binary outcomes ($y_i \in \{0, 1\}$) are inherently noisy. However, aggregating cancellation probabilities over an arrival night's book ($N \approx 50\text{--}150$ bookings) yields a well-behaved binomial distribution with expected cancellations $\mu = \sum p_i$ and variance $\sigma^2 = \sum p_i(1 - p_i)$. This transforms an erratic individual classification problem into a stable, quantifiable nightly inventory sizing decision.

---

### 2. Why We Reject the Vendor's "95% Accuracy" (Observation 3)
- **Asymmetric Loss Matrix:** Classification accuracy implicitly assigns identical penalties to False Positives (predicting cancellation when guest arrives) and False Negatives (predicting arrival when guest cancels).
  - *False Negative Error (Undersell):* Results in an unfilled room costing the night's average stay value ($\text{ADR} \times \text{nights} \approx €358$).
  - *False Positive Error (Oversell):* Results in walking a confirmed guest to another hotel at a direct cost of **€300**, PLUS the existential penalty of **disqualification** if the walk rate exceeds 10 per 1,000 arrivals.
- **The Threshold Trap:** A model with 95% classification accuracy using a standard 0.50 probability threshold can easily cause 15 walks per 1,000 arrivals on peak sold-out weekends, triggering immediate contract rejection under the client's brand standard. The client does not pay for classification accuracy; the client pays for **net euros saved under the strict $\le 10/1,000$ walk ceiling**.

---

### 3. Why We Reject the Marketing Wish-List (Hidden Guest Types)
- **The Scope Creep Trap:** The client's brief noted: *"Our marketing team would love to find our hidden guest types."*
- **Technical Justification:** Addressing this requires unsupervised clustering (e.g. K-Means, Latent Dirichlet Allocation, or Gaussian Mixture Models) across guest attributes.
- **Quantitative Business Justification:** Unsupervised clustering produces descriptive behavioral personas (e.g. "budget weekend couple" vs "corporate solo"), but **it outputs zero actionable numbers for nightly capacity allocation**. In our evaluation contract, the oversell decision $k$ depends strictly on aggregate expected cancellations $\mu$ and hotel capacity. Coupling an unsupervised clustering step to the live nightly pipeline increases runtime latency, adds failure points, and reduces explainability without saving a single euro on the proof period. It belongs in an offline CRM marketing project, not in a real-time nightly inventory allocation engine.

---

### 4. The Full-Night Caveat (Rubric T1.5)
- **The Economic Insight:** Overbooking creates economic value **only when the hotel is operating near physical capacity**.
- **The Seasonal Divergence:** In January, the Algarve Resort averages only 35.4 arrivals per night against physical capacity. When a 250-room hotel has only 50 bookings on the books, overbooking carries **zero walk risk**, but it also generates **zero incremental revenue**—any cancellations simply expand existing vacancy.
- **Caveat Requirement:** Our proof-period euro savings must carry the explicit caveat that overbooking value is heavily concentrated during high-occupancy periods (approx. 45% of nights at Lisbon City Hotel and peak summer months at Algarve Resort).

---

### 5. Why a Time Split (Not a Random Split) and Bin 1 Features Only
- **Temporal Integrity:** Randomly splitting cross-sectional booking data leaks future seasonal trends, macro demand shocks, and repeat-guest history into training folds. We enforce a chronological split: Train (< July 2016), Choose (July–Dec 2016), and Prove (Jan–Aug 2017).
- **Zero Lookahead Leakage:** Bin 3 columns (`reservation_status`, `assigned_room_type`, `booking_changes`) are recorded during check-in or post-outcome. Training on them produces superhuman backtest accuracy that instantly collapses in live production.

---

# PART 2: PANEL CROSS-EXAMINATION DEFENSE PLAYBOOK

| # | Panel Question | Underlying Trap | Defending Answer & Mechanism |
|---|---|---|---|
| **1** | *"Why is your unit the night and not the booking?"* | Checking if you treated this as an academic classification competition. | *"Because rooms are fungible inventory. The hotel cannot deny a guest a room weeks in advance based on an individual cancellation probability. Cancellations pool across the property on that arrival night, so the revenue manager acts on total capacity by opening $k$ rooms to the market."* |
| **2** | *"If walking a guest cost €1,000 instead of €300, what would change in your system?"* | Checking if your pipeline understands asymmetric cost trade-offs. | *"Our safety buffer $b$ would increase, making our overbooking policy $k$ more conservative. When walk penalties rise, the expected loss from a single walked guest quickly overtakes the revenue of an extra room stay (€358), forcing $k$ downward to stay safely below the brand ceiling."* |
| **3** | *"Why did you discard Bin 3 features if they produced higher AUC?"* | Probing for data leakage awareness. | *"Because Bin 3 features like `reservation_status` and `booking_changes` are recorded at check-in or after the stay. In real production, 14 days before arrival, those values do not exist. Using them would represent catastrophic lookahead leakage that would fail in the lobby."* |
| **4** | *"What happens in January, when the Algarve Resort is not full?"* | Testing the Full-Night Caveat (Rubric T1.5). | *"In January, Algarve Resort arrivals average only 35.4 per night. Overbooking recommendations become moot ($k=0$) because physical capacity comfortably absorbs all variance without any walk risk. Our savings carry the caveat that overbooking value concentrates on peak, near-full nights."* |
| **5** | *"Which number in the brief was wrong, and how did you find it?"* | Checking Rubric T1.3 (Brief Verification). | *"The brief claimed about 1 in 4 bookings cancel (~25%). By executing `src/data.py` on the 119,390 bookings, we proved the actual group-wide cancellation rate is 37.04% (41.73% at City Hotel and 27.76% at Resort). Building on 25% would have drastically under-oversold rooms."* |
| **6** | *"Finance claimed non-refundable prepaid bookings never turn into a stay. Were they right?"* | Checking Observation 1. | *"Finance was completely correct. In the data, bookings with `deposit_type == 'Non Refund'` exhibit a 99.36% cancellation rate (14,494 out of 14,587 cancelled). This is driven by wholesale group tour operators purchasing non-refundable blocks that get cancelled en masse when tours fail to fill."* |
| **7** | *"Why not use deep learning or complex neural networks?"* | Testing simplicity and explainability discipline. | *"Tabular booking data with Bin 1 features is governed by strong linear and tree-based decision boundaries (lead time, ADR, deposit type). A calibrated linear/tree model executes in milliseconds, provides clear feature importances for front-desk trust, and avoids overfitting the temporal drift seen between 2016 and 2017."* |

