"""
Independent verifier for an exported decision trail (VTT pilot demonstrator, v2).

Written separately from the code that produces the trail: it imports nothing from it and re-implements the
hashing, the hash chain, the Merkle scheme and the signature checks from the specification below, so a third
party can rewrite it in another language and get the same answers.

Specification
- profile       = the export names its algorithms (crypto-agility). Accepted profiles:
                    v1-classic  record_hash sha256, merkle sha256/leaf00-node01/promote-odd, sig [ed25519]
                    v2-hybrid   record_hash sha256, merkle sha256/leaf00-node01/promote-odd, sig [ed25519, ml-dsa-65]
                  anything else is refused; a deployment may accept only v2-hybrid (accept=...)
- record hash   = SHA-256 of the canonical JSON (sorted keys, no spaces, UTF-8) of the record without "hash"
- chain         = each record's "prev" is the previous record's hash; the first is 64 zeros; "seq" counts from 0
- time          = record times never go backwards (a record written now cannot claim an earlier time)
- checkpoint    = Merkle root over the record hashes first_seq..last_seq:
                  leaf = SHA-256(0x00 || hash bytes), node = SHA-256(0x01 || left || right),
                  an odd node at the end of a level is promoted unchanged
- witness       = the list of roots the external witness received ("node:root"); a checkpoint not in it,
                  and every record after the last witnessed checkpoint, is reported as unwitnessed
- authorization = every algorithm of the profile signs the canonical JSON of
                  {"action", "authorizes", "sig_alg"} with the authority key of that algorithm
                  (ed25519: RFC 8032; ml-dsa-65: FIPS 204); all must verify; each authorization is single-use;
                  an action must point to an earlier authorization, which must point to an earlier recommendation
- merged        = records a partitioned node kept locally; their own chain is re-verified the same way

Usage:  python verify.py <trail.json> <witness.json> <authority_keys.json>
Exit code 0 = the trail verifies; 1 = it does not (the errors are printed). Requires: cryptography, pqcrypto.

Copyright (c) 2026 Mihai Roșca (BRIDGRAI). All rights reserved, except: anyone may run, read and
re-implement this verifier in order to check the data published with it.
"""
from __future__ import annotations

import hashlib
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ZERO = "00" * 32
KNOWN_PROFILES = {
    "v1-classic": {"record_hash": "sha256", "merkle": "sha256/leaf00-node01/promote-odd", "sig": ["ed25519"]},
    "v2-hybrid": {"record_hash": "sha256", "merkle": "sha256/leaf00-node01/promote-odd", "sig": ["ed25519", "ml-dsa-65"]},
}


def _canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _h(obj) -> str:
    return hashlib.sha256(_canon(obj)).hexdigest()


def _root(hashes: list[str]) -> str:
    level = [hashlib.sha256(b"\x00" + bytes.fromhex(x)).digest() for x in hashes]
    if not level:
        return ZERO
    while len(level) > 1:
        level = [hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest() if i + 1 < len(level) else level[i]
                 for i in range(0, len(level), 2)]
    return level[0].hex()


def _sig_error(body: dict, keys: dict, algs: list[str]) -> str | None:
    if body.get("sig_alg") != algs:
        return f"signature algorithms {body.get('sig_alg')} differ from the profile {algs}"
    msg = _canon({"authorizes": body.get("authorizes"), "action": body.get("action"), "sig_alg": algs})
    for alg in algs:
        sig, key = (body.get("signatures") or {}).get(alg), keys.get(alg)
        if not sig or not key:
            return f"no {alg} signature or key"
        try:
            if alg == "ed25519":
                Ed25519PublicKey.from_public_bytes(bytes.fromhex(key)).verify(bytes.fromhex(sig), msg)
            elif alg == "ml-dsa-65":
                from pqcrypto.sign import ml_dsa_65
                # pqcrypto < 1.0 returns True/False; pqcrypto >= 1.0 returns None and raises on a bad signature
                if ml_dsa_65.verify(bytes.fromhex(key), msg, bytes.fromhex(sig)) is False:
                    return "ml-dsa-65 signature does not verify"
            else:
                return f"unknown signature algorithm {alg}"
        except Exception:
            return f"{alg} signature does not verify"
    return None


def _chain_errors(records: list[dict], where: str) -> list[str]:
    errors, prev, last_t = [], ZERO, None
    for i, r in enumerate(records):
        body = {k: v for k, v in r.items() if k != "hash"}
        if r.get("seq") != i:
            errors.append(f"{where}: record {i} has seq {r.get('seq')} (missing, extra or reordered record)")
        if r.get("prev") != prev:
            errors.append(f"{where}: record {i} does not follow the previous record")
        if _h(body) != r.get("hash"):
            errors.append(f"{where}: record {i} content does not match its hash")
        if last_t is not None and isinstance(r.get("t"), (int, float)) and r["t"] < last_t:
            errors.append(f"{where}: record {i} claims an earlier time than the record before it (backdated)")
        prev, last_t = r.get("hash"), r.get("t", last_t)
    return errors


def verify(export: dict, witnessed_roots: list[str], authority_keys: dict, accept: tuple = tuple(KNOWN_PROFILES)) -> dict:
    records, node = export["records"], export["node"]
    name = export.get("profile_name")
    if name not in accept or export.get("profile") != KNOWN_PROFILES.get(name):
        return {"node": node, "records": len(records), "ok": False, "unwitnessed_records": len(records),
                "signatures_ok": 0, "signatures_bad": 0, "profile": name,
                "errors": [f"{node}: profile {name!r} is unknown, altered or not accepted here"]}
    algs = KNOWN_PROFILES[name]["sig"]
    errors = _chain_errors(records, node)
    witnessed = set(witnessed_roots)

    covered_to = -1
    for cp in export["checkpoints"]:
        span = records[cp["first_seq"]:cp["last_seq"] + 1]
        if len(span) != cp["count"] or _root([r["hash"] for r in span]) != cp["root"]:
            errors.append(f"{node}: checkpoint {cp['first_seq']}-{cp['last_seq']} does not match the records")
            continue
        if f"{node}:{cp['root']}" not in witnessed:
            errors.append(f"{node}: checkpoint {cp['first_seq']}-{cp['last_seq']} root was never given to the witness")
            continue
        if cp["first_seq"] == covered_to + 1:
            covered_to = cp["last_seq"]
    unwitnessed = len(records) - (covered_to + 1)

    seen: dict[str, dict] = {}
    used_signatures: set[str] = set()
    used_authorizations: set[str] = set()
    signatures_ok = signatures_bad = 0
    for r in records:
        b = r["body"]
        if r["kind"] == "authorization":
            target = seen.get(b.get("authorizes"))
            err = _sig_error(b, authority_keys, algs)
            if err:
                signatures_bad += 1
                errors.append(f"{node}: record {r['seq']} authorization: {err}")
            else:
                signatures_ok += 1
            if not target or target["kind"] != "recommendation":
                errors.append(f"{node}: record {r['seq']} authorizes no earlier recommendation")
            if not b.get("declined"):
                sid = (b.get("signatures") or {}).get("ed25519")
                if sid in used_signatures:
                    errors.append(f"{node}: record {r['seq']} repeats an authorization already given (replay)")
                used_signatures.add(sid)
        if r["kind"] == "action":
            auth = seen.get(b.get("authorization"))
            if not auth or auth["kind"] != "authorization" or auth["body"].get("declined"):
                errors.append(f"{node}: record {r['seq']} action without an earlier authorization")
            elif b.get("authorization") in used_authorizations:
                errors.append(f"{node}: record {r['seq']} reuses an authorization (replay)")
            used_authorizations.add(b.get("authorization"))
        if r["kind"] == "gap":
            merged = [m["body"]["original"] for m in records if m["kind"] == "merged"
                      and m["body"].get("from_node") == b["from_node"]]
            errors += _chain_errors(merged, f"{b['from_node']} (merged)")
            if merged and merged[-1]["hash"] != b["local_head"]:
                errors.append(f"{b['from_node']} (merged): last record is not the local head declared at the gap")
        seen[r["hash"]] = r
    return {"node": node, "records": len(records), "ok": not errors, "errors": errors, "profile": name,
            "unwitnessed_records": unwitnessed, "signatures_ok": signatures_ok, "signatures_bad": signatures_bad}


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        trail = json.load(f)
    with open(sys.argv[2], encoding="utf-8") as f:
        witness = json.load(f)
    with open(sys.argv[3], encoding="utf-8") as f:
        keys = json.load(f)
    rep = verify(trail, witness, keys)
    print(json.dumps({k: v for k, v in rep.items() if k != "errors"}, indent=1))
    for e in rep["errors"][:20]:
        print("ERROR", e)
    sys.exit(0 if rep["ok"] else 1)
