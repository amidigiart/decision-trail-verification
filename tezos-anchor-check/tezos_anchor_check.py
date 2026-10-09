#!/usr/bin/env python3
"""
tezos_anchor_check.py — check, without trusting us, that a Merkle root was anchored on Tezos mainnet, and when.

Python 3.10+ standard library only. No code of ours is needed: the Merkle scheme is short and written out below.

What it checks for a root:
  1. an indexer (TzKT) lists an applied `anchor_batch` call on the contract with exactly this root, and names its
     operation hash, block level, block hash and time;
  2. each Tezos node you name (default: two public nodes run by different operators than the indexer) has that
     operation in that block: same operation hash, destination = the contract, entrypoint = anchor_batch,
     parameter = the root, status = applied, and the block hash at that level is the one the indexer gave.
The root passes only if at least one node CONFIRMS it and NO node CONTRADICTS it. A node that does not keep the
block any more (a "rolling" node keeps only recent blocks) or does not answer is reported, but it is neither a
confirmation nor a contradiction. Anything else is printed and the exit code is 1.

Usage:
  python tezos_anchor_check.py root <64-hex root>
  python tezos_anchor_check.py leaves <hex> <hex> ...          # computes the root of these leaves first
  python tezos_anchor_check.py sums SHA256SUMS.txt             # prints the root of a folder's SHA256SUMS (no network)
  options: --contract KT1...  --indexer URL  --node URL (repeatable)  --json

Merkle scheme (the same as verify.py and every ANCHOR.md): leaf = SHA-256(0x00 || h), node = SHA-256(0x01 || left ||
right), an odd node at the end of a level is promoted unchanged; leaves in the order given.

Limits: public nodes in "rolling" mode keep only recent blocks; for an old anchor name an archive node with --node.
The time is the block time (Tezos consensus), not a qualified time-stamp in the eIDAS sense.

License: Proprietary — all rights reserved (free to run for verification)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Callable

CONTRACT = "KT1S1YVjwGy4iFcbrN7QgTFY5sdGDhDAMZBV"
INDEXER = "https://api.tzkt.io/v1"
NODES = ["https://rpc.tzbeta.net", "https://mainnet.smartpy.io"]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MANAGER_PASS = 3                                    # validation pass of transactions in a block
NOT_KEPT = "unreachable or block not kept"


def merkle_root(hashes: list[str]) -> str:
    for h in hashes:
        if not HEX64.match(h):
            raise ValueError(f"not a lowercase 64-hex SHA-256: {h!r}")
    level = [hashlib.sha256(b"\x00" + bytes.fromhex(h)).digest() for h in hashes]
    if not level:
        raise ValueError("no leaves")
    while len(level) > 1:
        level = [hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest() if i + 1 < len(level) else level[i]
                 for i in range(0, len(level), 2)]
    return level[0].hex()


def sums_root(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return merkle_root([line.split()[0] for line in f if line.strip()])


def http_get(url: str, attempts: int = 3):
    """GET JSON; a network error or a 5xx/429 answer is retried (public nodes are sometimes briefly busy). A 404 is
    final: the node does not have it."""
    req = urllib.request.Request(url, headers={"User-Agent": "tezos-anchor-check/1.0", "Accept": "application/json"})
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or i == attempts - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if i == attempts - 1:
                raise
        time.sleep(2 * (i + 1))


def check_root(root: str, contract: str = CONTRACT, indexer: str = INDEXER, nodes: list[str] | None = None,
               get: Callable[[str], object] = http_get) -> dict:
    """{"ok": bool, "anchor": {...} | None, "nodes": {url: "confirmed" | reason}, "problems": [...]}"""
    if not HEX64.match(root):
        raise ValueError("the root must be 64 lowercase hex characters")
    nodes = NODES if nodes is None else nodes
    rep = {"root": root, "contract": contract, "ok": False, "anchor": None, "nodes": {}, "problems": []}
    try:
        found = get(f"{indexer}/operations/transactions?target={contract}&entrypoint=anchor_batch&status=applied"
                    f"&parameter={root}&select=hash,level,timestamp,parameter,block")
    except Exception as e:                                                     # noqa: BLE001
        rep["problems"].append(f"indexer unreachable: {e}")
        return rep
    found = [o for o in found if (o.get("parameter") or {}).get("value") == root]
    if not found:
        rep["problems"].append("the indexer knows no applied anchor_batch with this root on this contract")
        return rep
    a = found[0]
    rep["anchor"] = {"operation": a["hash"], "level": a["level"], "block": a["block"], "time_utc": a["timestamp"],
                     "also_anchored_in": [o["hash"] for o in found[1:]]}
    for node in nodes:
        rep["nodes"][node] = _confirm_on_node(node, root, contract, a, get)
    confirmed = [n for n, v in rep["nodes"].items() if v == "confirmed"]
    silent = {n: v for n, v in rep["nodes"].items() if v.startswith(NOT_KEPT)}
    contra = {n: v for n, v in rep["nodes"].items() if n not in confirmed and n not in silent}
    rep["problems"] += [f"{n}: {v}" for n, v in contra.items()]
    rep["silent_nodes"] = sorted(silent)
    if not confirmed:
        rep["problems"].append("no node confirmed it: the indexer alone is not enough")
    rep["ok"] = bool(confirmed) and not contra
    return rep


def _confirm_on_node(node: str, root: str, contract: str, a: dict, get) -> str:
    try:
        header = get(f"{node}/chains/main/blocks/{a['level']}/header")
        ops = get(f"{node}/chains/main/blocks/{a['level']}/operations/{MANAGER_PASS}")
    except Exception as e:                                                     # noqa: BLE001
        return f"{NOT_KEPT} ({e})"
    if header.get("hash") != a["block"]:
        return f"block at level {a['level']} is {header.get('hash')}, the indexer said {a['block']}"
    op = next((o for o in ops if o.get("hash") == a["hash"]), None)
    if op is None:
        return f"operation {a['hash']} is not in block {a['block']}"
    for c in op.get("contents", []):
        p = c.get("parameters") or {}
        value = (p.get("value") or {})
        value = value.get("string") or value.get("bytes")
        if (c.get("kind") == "transaction" and c.get("destination") == contract
                and p.get("entrypoint") == "anchor_batch" and value == root):
            status = ((c.get("metadata") or {}).get("operation_result") or {}).get("status")
            return "confirmed" if status == "applied" else f"operation status is {status!r}"
    return "the operation carries no anchor_batch of this root to this contract"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cmd", choices=["root", "leaves", "sums"])
    ap.add_argument("args", nargs="+")
    ap.add_argument("--contract", default=CONTRACT)
    ap.add_argument("--indexer", default=INDEXER)
    ap.add_argument("--node", action="append", help="Tezos node RPC URL (repeatable; default: two public nodes)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "sums":
        print(sums_root(a.args[0]))
        return 0
    args = [x.strip() for x in a.args]
    root = args[0] if a.cmd == "root" else merkle_root(args)
    if a.cmd == "leaves":
        print(f"root of {len(args)} leaves: {root}")
    rep = check_root(root, a.contract, a.indexer, a.node or NODES)
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        an = rep["anchor"]
        if an:
            print(f"anchored: operation {an['operation']}, block {an['level']} ({an['block']}), {an['time_utc']}")
        for n, v in rep["nodes"].items():
            print(f"  {n}: {v}")
        for p in rep["problems"]:
            print(f"  PROBLEM: {p}")
        n_ok = sum(v == "confirmed" for v in rep["nodes"].values())
        print(f"CONFIRMED by the indexer and {n_ok} node(s), contradicted by none" if rep["ok"] else "NOT CONFIRMED")
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
