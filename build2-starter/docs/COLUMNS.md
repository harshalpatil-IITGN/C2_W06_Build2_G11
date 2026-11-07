# Which columns did the hotel know on the day of booking?

**Owner:** Data Lead. **Closes:** part of ladder stage 1. **Used by:** `src/features.py`, the PRD and slide 4.

Put every column in exactly one bin, by when the hotel learns its value:

1. **Fixed at booking**: known on the day the booking is made, and it does not change.
2. **Amendable**: known at booking but it can change before arrival, or it is only partly known at booking.
3. **After the fact**: written at check-in, during the stay, or when the outcome is already known.

Only the first bin feeds the MVP. A second-bin column may be tried with its caveat written beside it. A third-bin column never feeds a method. The dataset article (Antonio, de Almeida and Nunes, 2019) says how several columns were recorded; cite it where it settles a bin.

The evidence column holds the number or the source that settled the bin, for example a rate you computed, or a sentence from the dataset article.

| Column | Bin (1, 2 or 3) | Why | Evidence |
|---|---|---|---|
| `hotel` | | | |
| `is_canceled` | | | |
| `lead_time` | | | |
| `arrival_date_year` | | | |
| `arrival_date_month` | | | |
| `arrival_date_week_number` | | | |
| `arrival_date_day_of_month` | | | |
| `stays_in_weekend_nights` | | | |
| `stays_in_week_nights` | | | |
| `adults` | | | |
| `children` | | | |
| `babies` | | | |
| `meal` | | | |
| `country` | | | |
| `market_segment` | | | |
| `distribution_channel` | | | |
| `is_repeated_guest` | | | |
| `previous_cancellations` | | | |
| `previous_bookings_not_canceled` | | | |
| `reserved_room_type` | | | |
| `assigned_room_type` | | | |
| `booking_changes` | | | |
| `deposit_type` | | | |
| `agent` | | | |
| `company` | | | |
| `days_in_waiting_list` | | | |
| `customer_type` | | | |
| `adr` | | | |
| `required_car_parking_spaces` | | | |
| `total_of_special_requests` | | | |
| `reservation_status` | | | |
| `reservation_status_date` | | | |

## What happens to a method when the late columns go in?

_Train the same method twice on the same split, once with first-bin columns only and once with the second and third bins added. Then run the first version once more on a random split. Record the three AUCs here and say which one the client should believe._

| Run | Columns | Split | AUC on the proof period |
|---|---|---|---|
| A | First bin only | Time | |
| B | All three bins | Time | |
| C | First bin only | Random | |
