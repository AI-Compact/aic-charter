# Registered public keys

One file per seated human: `<github-login>.pub` (OpenSSH or PEM format). Private keys never
appear here. The fingerprint of every key is also written into the ledger when the seat is
confirmed (charter 5.2.2).

| Fingerprint | Login | Role | Registered |
|---|---|---|---|
| _(none yet)_ | | | |

Rotation: a new key replaces the old one; the old key stays in history and its fingerprint is
recorded in the ledger entry that performed the rotation (charter 5.2.5, key-rotate ≥3 seats).
