# How many rooms can we keep selling each night?

**From:** Director of Revenue, a two-hotel group in Portugal (name withheld under NDA)

**To:** Revenue Science squad, RateGain

**About:** Cancellation-aware overbooking, proved on 2017

We run two hotels, a city hotel in Lisbon and a resort in the Algarve. Across the group, about one booking in four is cancelled, and a cancelled room that we fail to resell earns nothing that night.

Today our revenue manager oversells each night with a flat rule: the hotel's average cancellation rate times the night's bookings, less a few rooms for safety. We want a better rule, proved in euros.

## What are we asking for?

For every arrival night at each hotel, tell us how many rooms beyond capacity we can keep selling, so that cancellations stop leaving rooms empty, without walking more than one guest in a hundred.

## How will we judge your answer?

- A room left empty by a cancellation costs us what that guest had booked. We value it at the night's average booked stay: rate times nights.
- A guest who arrives to a full hotel is walked to another hotel at our expense, which costs us EUR 300 a guest.
- Our brand standard is at most 10 walked guests per 1,000 arrivals. A rule that breaks it is rejected, whatever it saves.
- Train on arrivals before 1 July 2016, choose your settings on July to December 2016, and prove your rule once on January to August 2017.
- Our analyst has written this scoring rule as code in `src/contract.py`. Use it as it is.

## What do we need back?

A table our revenue manager can open each morning, showing for each of the next fourteen nights at each hotel how many rooms to oversell. With it, the proof: what your rule would have cost us from January to August 2017, set beside what our flat rule cost, in euros and in rooms.

## What have we noticed?

Our teams noticed these. We have not checked them.

1. Finance says most prepaid, non-refundable bookings never turn into a stay. That cannot be right. Prepaid means guaranteed.
2. Last year a vendor gave the front desk a daily list of the bookings most likely to cancel. The desk stopped using it within a month.
3. The same vendor's demo showed 95% accuracy. In the lobby it never came close.

## What is on our wish list?

Our marketing team would love to find our hidden guest types.

## What data do you get?

Every booking for arrivals from July 2015 to August 2017, one row per booking: 119,390 bookings and 32 columns, downloaded in code by `python src/data.py`.

---

_About the setting._ RateGain Travel Technologies is a real company, listed on the National Stock Exchange of India (RATEGAIN), founded in 2004, headquartered in India, with more than 13,000 customers in over 160 countries. It supplied neither this brief nor this data. The bookings are the open Hotel Booking Demand datasets from two real, anonymised Portuguese hotels (Antonio, de Almeida and Nunes, _Data in Brief_ 22, 2019, CC BY 4.0). The walk cost, the walk ceiling and the brief itself are this course's construction for teaching.
