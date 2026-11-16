# What did we decide, and why?

Two tables. The first is the Week 1 decisions log for the data: every cleaning or filtering choice, its reason and how many rows it touched. The second records team decisions and objections under the rule in `docs/ROLES.md`. Add rows; never delete them.

## Which data decisions did we make?

**Owner:** Data Lead.

| Date | Decision | Reason, with the number that justified it | Rows touched | Logged by |
|---|---|---|---|---|
| 2026-11-14 | Impute missing `children` with 0 | Only 4 bookings lacked children counts; default assumption is zero minor dependents. | 4 | Gurunath (Data Lead) |
| 2026-11-14 | Impute missing `country` with 'Unknown' | 488 bookings lacked country codes; assigning explicit category retains full book without dropping rows. | 488 | Gurunath (Data Lead) |
| 2026-11-14 | Clip negative ADR to 0.0 | 1 booking had an erroneous rate of -6.38 (refund adjustment); price cannot be negative. | 1 | Gurunath (Data Lead) |
| 2026-11-14 | Retain zero-guest phantom bookings | 180 bookings recorded 0 adults, 0 children, and 0 babies; retained because evaluation contract scores all exported bookings. | 180 | Gurunath (Data Lead) |
| 2026-11-14 | Restrict model training matrix strictly to Bin 1 features | Quarantining Bin 2 and Bin 3 columns (`assigned_room_type`, `booking_changes`, `reservation_status`) eliminates lookahead leakage (which falsely inflates AUC to 0.8416). | 119,390 | Gurunath (Data Lead) |

## Which team decisions and objections did we log?

**Owner:** whoever made the decision. An objection is three lines: what I object to, why, what I propose.

| Date | Artifact | Decision or objection | Raised by | Answer, within 15 minutes | Settled by |
|---|---|---|---|---|---|
| 2026-11-08 | docs/ROLES.md | Role assignments: Harshal (Client Lead), Gurunath (Data Lead), Vysag (Model Lead), Mihir (Build Lead). Challenger pairs: Client ↔ Model, Data ↔ Build. | Harshal | Agreed by consensus. Assignment logged and locked for the week. | Team consensus |
| 2026-11-11 | docs/PRD.md | Object: the model inputs include required_car_parking_spaces, country, adr and total_of_special_requests. Why: parking is recorded at arrival (all 7,416 bookings with parking arrived, 0% cancelled), and the others can change after booking. Propose: remove them from the inputs until the column audit confirms. | Vysag | | |
