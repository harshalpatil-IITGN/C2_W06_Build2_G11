# Product Roadmap: Post-Week 6 Production Rollout

**Owner:** Build Lead (Mihir Patel) & Client Lead (Harshal Patil). **When:** Delivery Handover.

---

## 1. Three-Week Production Execution Plan

The next three weeks transition the standalone CLI MVP into an enterprise-integrated, automated revenue science system across both hotel properties:

| Week | What we would build next | Why it matters to the client, with a number | Owner | Hours |
|---|---|---|---|---|
| **Week 7** | **PMS Integration & Automated Morning Batch Pipeline:** Automated cron job ingesting midnight snapshot from Opera PMS, running `nightly.py`, and emailing the morning table to General Managers by 06:00 AM. | Eliminates manual CSV export, saving **1.5 manager hours daily per property** (~€1,100/month in operational overhead) and preventing human transcription errors. | Build Lead (Mihir) | 22 |
| **Week 8** | **Room-Type Disaggregation & Upgrade Cascade Engine:** Disaggregate aggregate capacity into room types (Standard, Deluxe, Suites), modeling complimentary upgrade probabilities before triggering an external walk. | Decreases walk penalties by up to **28%** (saving an estimated **€15,000–€25,000 annually**) by absorbing oversell in vacant premium tiers instead of paying the €300 walk penalty. | Model Lead (Vysag) | 25 |
| **Week 9** | **Multi-Night Stay Displacement Dynamic Programming:** Joint arrival-duration modeling accounting for length-of-stay (LOS) constraints and multi-night shoulder leakage. | Prevents mid-stay room churning and captures an estimated additional **€80,000/year in spillover revenue** on high-demand 3-to-5 night summer holiday bookings. | Data Lead (Gurunath) & Model Lead (Vysag) | 28 |

---

## 2. Production Additions & Resource Allocation

Technical additions necessary to support enterprise operations, audit compliance, and system reliability:

| Addition | Owner | Hours | Target Milestone |
|---|---|---|---|
| **Two-Way PMS API Connector (Opera / Amadeus)** | Build Lead (Mihir) | 20 | Week 7.2 |
| **Interactive Streamlit Revenue Manager Cockpit** | Client Lead (Harshal) | 16 | Week 7.4 |
| **Event-Sourced Booking Log Ingestion (Bin 2 Activation)** | Data Lead (Gurunath) | 18 | Week 8.1 |
| **Room-Type Hierarchical Upgrade Matrix** | Model Lead (Vysag) | 16 | Week 8.3 |
| **Drift Monitoring & Continuous Calibration (Evidently AI)** | Build Lead (Mihir) | 14 | Week 9.1 |
| **Length-of-Stay Network Revenue Optimizer** | Model Lead (Vysag) | 20 | Week 9.4 |

---

## 3. Financial Summary for Executive Sponsor

- **Proved Backtest Value Delivered (MVP):** **€2,263,330 net savings** over the 8-month proof period (€282,916/month) compared to the current flat baseline rule, with 0 brand ceiling violations (9.94 walks / 1k arrivals).
- **Post-Week 6 Engineering Investment:** 104 engineering hours across 3 weeks (~€15,000 fully loaded implementation cost).
- **Expected Return on Investment (ROI):** Payback period is achieved in **less than 2 operational days**.
