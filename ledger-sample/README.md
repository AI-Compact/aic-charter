# Ledger sample (redacted)

This is a **sample** of the append-only audit ledger format. It contains no real member
identifiers and no keys.

The production ledger is a hash chain: each entry contains `prev_hash`, and `hash` is
`sha256(prev_hash + canonical_json(entry))`. Verification is a fold over the chain.

Public exports are published as releases on this repository.
