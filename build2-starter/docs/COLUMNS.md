# Which columns did the hotel know on the day of booking?

**Owner:** Data Lead. **Closes:** part of ladder stage 1. **Used by:** `src/features.py`, the PRD and slide 4.

Put every column in exactly one bin, by when the hotel learns its value:

1. **Fixed at booking**: known on the day the booking is made, and it does not change.
2. **Amendable**: known at booking but it can change before arrival, or it is only partly known at booking.
3. **After the fact**: written at check-in, during the stay, or when the outcome is already known.

Only the first bin feeds the MVP. A second-bin column may be tried with its caveat written beside it. A third-bin column never feeds a method. The dataset article (Antonio, de Almeida and Nunes, 2019) says how several columns were recorded; cite it where it settles a bin.

The evidence column holds the number or the source that settled the bin, for example a rate you computed, or a sentence from the dataset article.

| Column                             | Bin (1, 2 or 3) | Why | Evidence |
| ---------------------------------- | --------------- | --- | -------- |
| `hotel`                          | 1 | Hotel property (City Hotel or Resort Hotel) is chosen at booking and never changes. | Antonio et al. (2019), Table 1: static property identifier. |
| `is_canceled`                    | 3 | The target outcome itself (1 = canceled / no-show, 0 = stayed). Recorded only after arrival date or cancellation event. | Ground truth label; recording time $t \ge \text{arrival}$ or post-cancellation. |
| `lead_time`                      | 1 | Number of days elapsed between booking entry date and arrival date. Fixed on booking day. | Computed at reservation creation: booking date minus arrival date. |
| `arrival_date_year`              | 1 | Calendar year of scheduled arrival. Fixed on booking day. | Antonio et al. (2019), Table 1. |
| `arrival_date_month`             | 1 | Calendar month of scheduled arrival. Fixed on booking day. | Antonio et al. (2019), Table 1. |
| `arrival_date_week_number`       | 1 | ISO week number of scheduled arrival. Fixed on booking day. | Derived directly from arrival date. |
| `arrival_date_day_of_month`      | 1 | Day of arrival date. Fixed on booking day. | Antonio et al. (2019), Table 1. |
| `stays_in_weekend_nights`        | 1 | Number of weekend nights (Sat/Sun) booked by the guest. Fixed at reservation creation. | Part of requested stay length on booking contract. |
| `stays_in_week_nights`           | 1 | Number of weekday nights (Mon–Fri) booked by the guest. Fixed at reservation creation. | Part of requested stay length on booking contract. |
| `adults`                         | 1 | Number of adults declared on the reservation at booking. | Customer declaration at booking creation. |
| `children`                       | 1 | Number of children declared on the reservation at booking. | Customer declaration at booking creation; 4 missing values imputed as 0. |
| `babies`                         | 1 | Number of babies declared on the reservation at booking. | Customer declaration at booking creation. |
| `meal`                           | 1 | Contracted meal package (BB, FB, HB, SC/Undefined = Self Catering). Agreed at booking. | Antonio et al. (2019), Section 2: SC and Undefined indicate no meal package. |
| `country`                        | 1 | Country of origin of the booking contact/guest. Captured at booking. | Antonio et al. (2019), Table 1; 488 missing values imputed as 'Unknown'. |
| `market_segment`                 | 1 | Market designation channel (Direct, Corporate, Online TA, Offline TA/TO, Groups, Aviation). Fixed at booking. | Set by sales channel when booking is logged. |
| `distribution_channel`           | 1 | Booking intermediary mechanism (Direct, Corporate, TA/TO, GDS). Fixed at booking. | Set by channel manager at booking time. |
| `is_repeated_guest`              | 1 | Boolean flag (1/0) stating whether guest stayed before. Determined by PMS profile lookup at booking. | PMS customer profile matching at reservation entry. |
| `previous_cancellations`         | 1 | Historical count of cancellations by customer prior to this booking. Known at booking. | PMS profile historical accumulator prior to current transaction. |
| `previous_bookings_not_canceled` | 1 | Historical count of confirmed stays by customer prior to this booking. Known at booking. | PMS profile historical accumulator prior to current transaction. |
| `reserved_room_type`             | 1 | Room type requested and confirmed to guest at booking creation. | Contracted room tier on booking confirmation. |
| `assigned_room_type`             | 3 | Room type assigned at check-in desk. Can differ from reserved room type due to desk upgrade or overbooking. | Antonio et al. (2019), Section 2: explicitly set at check-in; strong lookahead indicator of physical check-in. |
| `booking_changes`                | 2 | Cumulative amendments made to the booking between creation and check-in/cancellation. | Antonio et al. (2019), Section 2: accumulates over time ($t > \text{booking}$); zero on booking day. |
| `deposit_type`                   | 1 | Deposit requirement: No Deposit, Non Refund, Refundable. Established at booking. | Payment term terms set on booking confirmation. |
| `agent`                          | 2 | Travel agency ID. Can be assigned, changed, or credited between booking and arrival. | 16,340 nulls mean booked without agent (Antonio et al., 2019); subject to channel re-routing. |
| `company`                        | 2 | Corporate account ID paying or booking the room. Can be amended prior to final corporate invoicing. | 112,593 nulls mean booked without company; can change post-booking. |
| `days_in_waiting_list`           | 2 | Number of days booking sat on waitlist before confirmation. Can change while pending. | Operational queuing metric that evolves dynamically post-booking. |
| `customer_type`                  | 1 | Booking category (Transient, Transient-Party, Contract, Group). Set at contract creation. | Contractual relationship established at reservation creation. |
| `adr`                            | 1 | Average Daily Rate (total room revenue divided by nights). Quoted and locked at booking. | Contracted rate on reservation; 1 negative value (-6.38) and 1,959 zero ADR complimentary bookings. |
| `required_car_parking_spaces`    | 2 | Number of parking spots requested. Frequently added by guest closer to arrival date. | Customer amenity request amendable post-booking. |
| `total_of_special_requests`      | 2 | Number of special requests (high floor, twin bed, etc.). Frequently added dynamically post-booking. | Antonio et al. (2019), Section 2: accumulates up to arrival day. |
| `reservation_status`             | 3 | Final state of reservation: Canceled, Check-Out, No-Show. Set on arrival or cancellation. | Target leakage: Check-Out encodes physical arrival with 100% precision. |
| `reservation_status_date`        | 3 | Date when reservation status reached its final value. Set on arrival date or cancellation date. | Direct timestamp of the outcome event; post-booking leakage. |

## What happens to a method when the late columns go in?

_Train the same method twice on the same split, once with first-bin columns only and once with the second and third bins added. Then run the first version once more on a random split. Record the three AUCs here and say which one the client should believe._

| Run | Columns        | Split  | AUC on the proof period |
| --- | -------------- | ------ | ----------------------- |
| A   | First bin only | Time   | 0.7571                  |
| B   | All three bins | Time   | 0.8416                  |
| C   | First bin only | Random | 0.8500                  |

**Which run should the client believe?**  
The client should believe **Run A (AUC = 0.7571)**. Run A is the only evaluation that strictly mimics live production conditions: it uses only features established on booking day (Bin 1) and predicts forward across a chronological hold-out period (arrivals in 2017). Run B is contaminated with lookahead target leakage from late columns (`assigned_room_type`, `reservation_status_date`), creating an illusion of high predictive power that will fail in the lobby. Run C produces an inflated AUC (0.8500) because random splitting leaks temporal seasonality, repeat-guest trajectories, and macroeconomic demand shocks from the future into the past.
