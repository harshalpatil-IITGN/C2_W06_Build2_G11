# AI Grilling Session: PRD, Build Plan & Operational Delivery Architecture

- **Date:** 2026-11-12
- **Role:** Build Lead (Mihir Patel)
- **Participant:** Client Lead (Harshal Patil)
- **Tool:** Claude 3.5 Sonnet / Antigravity
- **Target Artifact:** `docs/grill_02_prd.md`, `docs/BUILD_PLAN.md`, `docs/ROADMAP.md`

---

## Session Transcript

### Prompt (Mihir):
> We are preparing our PRD and Build Plan for Build 2 (hotel overbooking system). Grill us hard as an aggressive revenue management VP and technical auditor. Focus on:
> 1. Target leakage in Bin 2 features in live nightly runs.
> 2. Single-arrival night evaluation vs multi-night length of stay.
> 3. Why our optimal buffer b* is negative (-1) for Gradient Boosting vs positive (+16) for the flat baseline.
> 4. Operational disaster recovery if nightly.py crashes at 06:00 AM.

### Auditor Response:
> Let's dissect your architecture.
> 
> **Challenge 1:** In offline experiments, including Bin 2 features (`booking_changes`, `days_in_waiting_list`) increases AUC from 0.79 to 0.84. If you have those features in your raw CSV, why throw them away in `nightly.py`? Aren't you leaving predictive power on the table?
> 
> **Mihir's Team Answer:** In a historical dump, `booking_changes` accumulates changes made right up to checkout. In a live morning run, we only have data up to 06:00 AM on check-in day. Without a timestamped event log table, any modification field risks leaking future information into morning decisions. We choose guaranteed zero leakage over synthetic offline metric gains.
> 
> **Challenge 2:** A guest books for 5 nights and cancels. Your contractual unit is hotel-arrival night. You oversell on night 1, but what about nights 2, 3, 4, 5? Those room-nights stay empty, costing money. How does your MVP address length-of-stay displacement?
> 
> **Mihir's Team Answer:** The contract specifically scores hotel-arrival nights. Trying to solve multi-night joint dynamic programming in a 5-day sprint would compromise system stability and verification. We deliver a verified, rock-solid single-night MVP that meets all contractual rules, and place multi-night length-of-stay dynamic programming into Week 9 of our production roadmap.
> 
> **Challenge 3:** A hotel GM is looking at your output table. They see `Buffer b* = -1`, meaning oversell $k = \text{expected} - (-1) = \text{expected} + 1$. They say: "A buffer should protect me from walks! Why are you adding rooms beyond your expected cancels?"
> 
> **Mihir's Team Answer:** We explain that $b^*$ is an asymmetric cost tuner. In well-calibrated machine learning models, expected cancellations $\sum p_i$ are mathematically sharper than heuristic rules. Because the €300 walk penalty is balanced against the stay value (€100–€150), setting $b^* = -1$ maximizes revenue capture while still strictly keeping walks below the 10.0 per 1,000 arrivals brand ceiling (realized proof rate: 9.94 / 1k).
> 
> **Challenge 4:** It is 06:05 AM. The front desk manager runs `python src/nightly.py --from 2017-08-18 --nights 14`, but the job crashes with a segmentation fault or missing model file. What happens? Do they guess?
> 
> **Mihir's Team Answer:** We implement graceful degradation. If model loading fails, `nightly.py` alerts the user and automatically falls back to the Client Flat Rule ($b^* = 16$), which requires only booking counts and passes the ceiling at 6.70 walks/1k. The desk is never left stranded.
