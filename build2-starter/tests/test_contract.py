"""Checks of the client's scoring rule on nights small enough to count by hand.

Read these as worked examples of docs/EVALUATION_CONTRACT.md. Run them with: pytest -q
"""
import pathlib
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import contract  # noqa: E402


def two_nights():
    """Night 1: four bookings, two cancel, each worth EUR 100 x 2 nights. Night 2: two bookings, none cancel."""
    return pd.DataFrame({
        "hotel": ["City Hotel"] * 6,
        "arrival_date": pd.to_datetime(["2016-08-01"] * 4 + ["2016-08-02"] * 2),
        "is_canceled": [1, 1, 0, 0, 0, 0],
        "adr": [100.0] * 4 + [50.0] * 2,
        "nights": [2] * 4 + [1] * 2,
    })


def test_nightly_table_sums_probabilities_per_night():
    nights = contract.nightly_table(two_nights(), prob=[0.5] * 4 + [0.1] * 2)
    first = nights.iloc[0]
    assert first["book"] == 4 and first["cancelled"] == 2
    assert first["expected"] == pytest.approx(2.0)      # 0.5 + 0.5 + 0.5 + 0.5
    assert first["spread"] == pytest.approx(1.0)        # sqrt(4 x 0.5 x 0.5)
    assert first["stay_value"] == pytest.approx(200.0)  # EUR 100 x 2 nights


def test_overselling_too_few_leaves_rooms_empty():
    nights = contract.nightly_table(two_nights(), prob=[0.5] * 6)
    result = contract.night_cost(nights, oversell=[1, 0])
    # Night 1: two cancelled, one resold, so one room stays empty at EUR 200. Night 2: nothing happens.
    assert result["empty_rooms"] == 1 and result["walked_guests"] == 0
    assert result["cost_eur"] == pytest.approx(200.0)
    assert result["ceiling_met"]


def test_overselling_too_many_walks_guests():
    nights = contract.nightly_table(two_nights(), prob=[0.5] * 6)
    result = contract.night_cost(nights, oversell=[3, 1])
    # Night 1: three sold beyond capacity, two cancelled, one guest walked. Night 2: one walked.
    assert result["empty_rooms"] == 0 and result["walked_guests"] == 2
    assert result["cost_eur"] == pytest.approx(600.0)    # 2 x EUR 300
    # 2 walks over 4 arrivals is 500 per 1,000, far above the ceiling of 10.
    assert result["walks_per_1000"] == pytest.approx(500.0)
    assert not result["ceiling_met"]


def test_periods_split_on_the_stated_dates():
    df = pd.DataFrame({"arrival_date": pd.to_datetime(["2016-06-30", "2016-07-01", "2016-12-31", "2017-01-01"])})
    train, choose, proof = contract.split_periods(df)
    assert list(train["arrival_date"].dt.strftime("%Y-%m-%d")) == ["2016-06-30"]
    assert list(choose["arrival_date"].dt.strftime("%Y-%m-%d")) == ["2016-07-01", "2016-12-31"]
    assert list(proof["arrival_date"].dt.strftime("%Y-%m-%d")) == ["2017-01-01"]


def test_bad_inputs_are_refused():
    bookings = two_nights()
    with pytest.raises(ValueError):
        contract.nightly_table(bookings, prob=[1.2] * 6)          # not a probability
    with pytest.raises(ValueError):
        contract.nightly_table(bookings, prob=[0.5] * 5)          # one probability too few
    nights = contract.nightly_table(bookings, prob=np.full(6, 0.5))
    with pytest.raises(ValueError):
        contract.night_cost(nights, oversell=[-1, 0])            # cannot sell a negative number of rooms
    with pytest.raises(ValueError):
        contract.night_cost(nights, oversell=[1.5, 0])           # rooms are sold whole
