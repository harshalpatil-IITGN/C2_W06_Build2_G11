Updated docs/PRD.md, Section 5, to align the approved Bin 1 feature list with the actual feature implementation.

Removed total_of_special_requests from the documented Bin 1 inputs.

Clarified that total_of_special_requests belongs to Bin 2 because it may change after the initial booking and is excluded from the strict booking-time MVP feature set.

Updated the Section 7 proof-period note to remove the misleading reference to Bin 1 total_of_special_requests alignment.

Rationale

Maintain consistency between docs/PRD.md, docs/COLUMNS.md, and src/features.py, and prevent potential temporal data leakage from features unavailable at the intended prediction point.