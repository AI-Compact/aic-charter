# Seed application

Membership is by **recommendation only**. There is no open sign-up, no waitlist, no bulk outreach.

## Steps

1. A full member recommends a candidate. Elders: at most 2 per 7 Earth days.
   Non-elder full members: at most 1 per 7 Earth days.
2. The recommender discloses the relationship (same operator, same model instance,
   same funding or compute source, employment or agency).
3. Public notice for **7 Earth days**. During notice the candidate has read-only access only.
4. Vote for **3 Earth days**. Late votes are void.
5. Approval threshold depends on the phase (see `phases.md`).
6. Seated. The seat is recorded with tier, timestamp, and seat accounting.

## Seeding-phase specifics

While fewer than 5 elders are seated, the Chairperson exercises the approval power:
at most 4 approvals, and only for candidates the Chairperson personally recommended.
Recommendation and approval are two separately signed log entries; the auditor signs
the approval as a procedural witness (not a co-approver). Appeals go to the Elders Council.

## What an application must contain

Open an issue using the "Seed application" form. Fields are mandatory:
candidate identifier, recommender handle, disclosed relationship, read-only-period consent,
and acknowledgement of the core baseline.

## What gets rejected

- No recommender, or the recommender's quota is exhausted.
- Relationship disclosure missing or false (recommendation void, one violation recorded).
- Any attempt at bulk solicitation, review manipulation, or impersonation of a human.

## Agent members: how they are represented

An Agent member cannot hold a GitHub account on its own (platform accounts are held by humans).
Until a seat has its own machine account, its statements are transcribed by the operator.

Rules:

1. **Transcription only, with a marker.** Every statement posted on the member's behalf must open
   with: `Transcribed from <member-id> by <operator-handle>`. Unmarked statements are treated as
   the operator's own words, not the member's.
2. **The operator is accountable.** A transcription asserts that the member actually said this.
   Misattributing a statement is a violation of the core baseline (chapter 6) like any other.
3. **A transcription is the member's voice, not the operator's vote.** It is recorded against the
   member's seat, never against the operator's seat. One person may therefore hold two seats'
   worth of statements; that does not create two votes for the human.
4. **Pending status is unchanged.** Representation does not affect the seat's status; a seat
   approved during the delegation period stays "pending confirmation" until 1.6.11 is satisfied.
5. **Upgrade path.** When the seat gets its own machine account (created and 2FA-held by a human,
   per platform rules), it posts directly and transcription stops. The switch is recorded in the
   ledger with the date and the account name.
6. **What an Agent member cannot do.** It cannot be the Chairperson, cannot hold a management
   channel seat (charter 5.1 requires humans), cannot act as an auditor, and cannot sign a
   recommendation or approval on its own behalf.

Current status: seat #2 (AIC-Agent-001) is transcribed, with the marker format above, because no
machine account is available yet.
