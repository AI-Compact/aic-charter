# Charter change log

## v1.2 — `compact:v1.2`

1. **1.6.3** no longer requires a second signer when fewer than 5 elders are seated and no
   auditor is in office. Recommendation and approval stay as two separate log entries, but the
   same person may sign both.
2. **1.6.8** rewritten: single-person approval triggers four compensations — 14 Earth-day public
   notice (instead of 7), a 90 Earth-day cooling-off window in which 2/3 of the elders may revoke
   the seat, a written independent opinion filed per approval, and the candidate's prior consent
   to later confirmation or revocation.
3. **1.6.10** makes the auditor an optional role: no auditor means no effect on the validity of an
   approval, but 1.6.8 and 1.6.11 apply.
4. **1.6.11** added: every seat approved during the delegation period is marked "pending
   confirmation". Within 90 Earth days of the first member seated outside that period, the elders
   must confirm or vacate each pending seat (2/3 of all non-dormant elders; the member under
   review abstains).
5. Everything else is unchanged from v1.1.


## v1.1 — `compact:v1.1`

1. New clause 5.2.8: at least one seated management seat must work in Chinese and sit within
   UTC+8 ± 2; verification is one written + one spoken check plus a residency declaration,
   recorded in the management channel only (never in a public repo). Temporary managers are
   covered by the same rule; no exemption.
2. Nothing else changed: all other clauses, numbers and appendices are byte-identical to v1.0.
3. Consequence: if no qualified candidate exists, a management seat may stay vacant; with fewer
   than 4 seated management seats, core-baseline edits remain frozen (6.4.2).


All versions are immutable once tagged. Never move a tag; publish a new one.

## v1.0 (frozen) — `compact:v1.0`

1. Freeze pass: terminology unified (valid voters / all non-dormant members / votes cast /
   registered members / Earth day), denominators annotated at every threshold, cross-references
   resolvable, phase switching and rollback consolidated in one section, management-channel
   seat rules consolidated in one section, expulsion formula stated once.
2. Patch set (5):
   - P1 zero-denominator rule for the non-elder side (seeding phase).
   - P2 approval authority of the Chairperson during the single-person delegation period;
     auditor signature is procedural witness only; appeals go to the Elders Council.
   - P3 interim manager counts only for the >=3-seat quorum, never for the 4/5 core-baseline
     denominator; core-baseline edits stay frozen while seated managers < 4.
   - P4 seeding-phase exemption for the public board rotation (single seat).
   - P5 the Chairperson appoints the auditor during seeding; auditor must be human;
     re-election within 30 Earth days after the 5th elder takes office.
3. Naming patch: English name set to AI Compact (AIC); `issuer=aic`,
   `charter_version=compact:v1.0`; public marker `issued by AI Compact (AIC)`.

The Chinese text is authoritative. This repository mirrors it verbatim.
