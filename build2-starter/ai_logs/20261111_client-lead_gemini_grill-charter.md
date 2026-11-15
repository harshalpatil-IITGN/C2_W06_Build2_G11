3

# AI Chat Log: Grill Run 1 (Charter and RFP Skeleton)

- **Date:** 2026-11-11
- **Role:** Client Lead (Harshal)
- **Tool:** Gemini
- **Purpose:** Grilling on Charter v0 and RFP Skeleton per docs/AI_WORKFLOW.md
- **Artifact it fed:** `docs/grill_01_charter.md`, `docs/CHARTER.md`, `docs/RFP.md`

---

### Opening Prompt

> "Grill me on this charter until we share an understanding of what is being decided, for whom, from what is known when, and what one wrong call costs in each direction."

---

### Round 1: Decision Unit & Granularity

**AI:**

> Question 1: Your charter focuses on predicting booking cancellations. Why is the decision unit framed as the hotel-arrival night rather than flagging individual high-risk bookings for the front desk to act on?
>
> _Recommended Answer:_ Framing at the individual booking level enables personalized interventions or selective overbooking, whereas hotel-night aggregation obscures booking-specific risk factors.

**Client Lead (Harshal):**

> I reject this recommendation. In hospitality revenue management, standard rooms are fungible inventory pooled across the hotel. The front desk cannot legally or ethically cancel confirmed individual reservations before arrival. Overbooking is executed by opening additional rooms beyond capacity on distribution channels for that arrival night. Aggregating probabilities to the hotel-night yields the expected cancellations $\mu = \sum p_i$ and variance $\sigma^2$ needed for inventory capacity sizing.

**AI Assessment:**

> Accepted. That is the correct operational reality of hotel revenue management. Updating `docs/CHARTER.md` Section 4 and `docs/RFP.md` Section 2.

---

### Round 2: Money Metric vs Accuracy & The Walk Ceiling

**AI:**

> Question 2: Observation 3 notes a previous vendor achieved 95% accuracy in demo but failed in the lobby. If a binary classifier achieves 95% accuracy or 0.92 AUC, why shouldn't that be our primary acceptance metric?
>
> _Recommended Answer:_ Standard classification metrics like AUC-ROC or F1-score are standard in literature; a high classification threshold can simply be applied to optimize precision.

**Client Lead (Harshal):**

> I disagree. Standard accuracy treats false positives and false negatives equally, but the client faces severe asymmetric costs: an empty room costs the stay value (~€358) while a walked guest costs €300 PLUS the catastrophic risk of exceeding the 10/1,000 brand ceiling (which disqualifies the entire rule). A 95% accurate model can easily produce 15 walks per 1,000 on peak sold-out weekends, triggering instant client rejection. Therefore, our primary metric must be total net euro cost under a strict $\le 10/1,000$ walk ceiling constraint.

**AI Assessment:**

> Sharp catch. The brand standard is a hard constraint that must dominate classification accuracy. Documented in Charter Section 5 and RFP Section 3.

---

### Round 3: Baseline Cancellation Rate Discrepancy

**AI:**

> Question 3: The client brief states that "about one booking in four is cancelled" (~25%). If that is the client's stated prior, shouldn't our naive baseline and prior distributions use 25%?
>
> _Recommended Answer:_ Yes, use the client's stated 25% cancellation rate to maintain consistency with the client's internal reports and flat rule baseline.

**Client Lead (Harshal):**

> No, absolutely not. We audited the actual 119,390 historical bookings via `src/data.py` and discovered the true cancellation rate across the group is 37.04% (41.73% at City Hotel, 27.76% at Resort Hotel). Adopting the client's 25% claim would severely under-estimate cancellations, causing chronic under-overselling and leaving thousands of empty rooms. We must document this discrepancy as the wrong number in the brief.

**AI Assessment:**

> Crucial verification. Caught the wrong number in the brief per Rubric T1.3. Updating Charter Section 6.

---

### Round 4: Observation 1 — Non-Refundable Deposit Anomaly

**AI:**

> Question 4: Finance claims that "most prepaid, non-refundable bookings never turn into a stay." The client remarks "That cannot be right. Prepaid means guaranteed." Should we treat non-refundable bookings as guaranteed stays with zero cancellation probability?
>
> _Recommended Answer:_ Assume non-refundable bookings have low cancellation probability since guests lose their money, and treat Finance's observation as an operational anomaly or data logging error.

**Client Lead (Harshal):**

> I reject that assumption. The empirical data proves Finance is 100% correct: 99.36% of bookings with `deposit_type == 'Non Refund'` cancel (14,494 out of 14,587). This occurs because tour operators and corporate groups place non-refundable bulk deposits for blocks that are cancelled wholesale when tour volume fails to materialize. The hotel collects the penalty revenue, but the rooms remain empty. We need to ask the client whether those penalty revenues offset empty room losses in accounting.

**AI Assessment:**

> Spot on. Documented in Charter Section 6 and Section 9 (question to client). Grilling round 1 concluded.
