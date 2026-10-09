# Check an anchor on Tezos yourself

`tezos_anchor_check.py` answers one question without trusting us: **was this root anchored on the Tezos mainnet,
and when?** It needs only Python 3.10+ and its standard library. It needs nothing else of ours.

```
python tezos_anchor_check.py root 82e413861cde62c4fdafe6ca7f2d9b203dd7bb366f96c2a6d3a56a4867792855
python tezos_anchor_check.py leaves <leaf0> <leaf1> ...      # computes the root of an ANCHOR.md batch first
python tezos_anchor_check.py sums ../SHA256SUMS.txt          # the root of a folder (no network)
```

## How it decides

**Two kinds of source:**
- **the indexer (TzKT)** must list an applied `anchor_batch` call on contract
  `KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV` with exactly this root;
- **Tezos nodes run by other operators** (by default `rpc.tzbeta.net` and `mainnet.smartpy.io`; add your own with
  `--node`) must each hold that operation in that block, under the same block hash. The destination, the
  entrypoint, the root and the status `applied` must all match.

**The verdict.** The root passes only if at least one node **confirms** it and **no** node **contradicts** it. A
node that no longer keeps the block (a "rolling" node) is reported. It counts neither for nor against.

## Results on 10 October 2026

- **Offline:** `sums` reproduces both anchored roots, the pack root `048d5cc1…` (`../ANCHOR.md`) and the folder
  root `99f50ed2…` (`../key-revocation/ANCHOR.md`).
- **Live:** every anchor in our chain of states (14 roots) was confirmed by the indexer and by at least one
  independent node, and contradicted by none.

## Limits

- Old blocks are kept only by archive nodes. For an anchor years old, name an archive node with `--node`.
- The time given is the block time agreed by Tezos consensus. It is not a qualified time-stamp in the eIDAS sense.
- The tool shows that a root existed at that time. It shows nothing about what the root stands for; that is what
  the `verify.py` files and the `ANCHOR.md` leaves are for.

`SHA256SUMS.txt` in this folder covers both files except itself.
