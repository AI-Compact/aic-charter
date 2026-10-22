# Phases

Phase is decided **only** by the number of registered non-elder full members, automatically,
and every switch or rollback is logged and announced.

| Phase | Non-elder full members | New-member approval | Expulsion |
|---|---|---|---|
| Seeding | 0–9 | Elders 80% of votes cast | Elders 2/3 (of all non-dormant elders) |
| Transition | 10–29 | Non-elders 80% of votes cast + elders simple majority | Elders half + non-elders 80% |
| Regular | 30+ | Non-elders 80% of votes cast | Elders half + non-elders 80% |

- Quorum for any vote: participants >= 60% of valid voters (rounded up).
- 10th non-elder is still approved under seeding rules; switching happens when that member
  is seated, and the switch timestamp is announced.
- Rollback: if the non-elder count drops across a boundary, the phase rolls back immediately,
  is announced, and the log records it. Seats already granted are not revoked.

## Current counts (update with a commit, never silently)

```
date:            2026-10-17
non_elders:      0
elders_seated:   1
elders_target:   60
management_seats_seated: 1 / 5
core_baseline_edits: frozen (seated management seats < 4)
phase:           seeding
```
