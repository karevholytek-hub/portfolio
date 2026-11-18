#!/usr/bin/env python3
"""QA manifest linter and fail-closed release gate. Green lint NEVER means ready."""
import argparse
import hashlib
import json
import re
from pathlib import Path

GATES = tuple("G%02d" % i for i in range(1, 9))
STATES = {"PASS", "FAIL", "UNVERIFIED", "N/A"}


def inspect(doc, root, *, release=False):
    root = Path(root).resolve()
    gates = doc.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        return ["Exactly G01-G08 required"]
    errors = []
    sha = doc.get("candidate_sha256")
    if sha is not None and not (isinstance(sha,str) and re.fullmatch("[0-9a-fA-F]{64}",sha)):
        errors.append("Invalid candidate_sha256")
    for gid in GATES:
        record = gates[gid]
        if not isinstance(record, dict):
            errors.append(gid + ": must be object")
            continue
        state = record.get("status")
        if state not in STATES:
            errors.append(gid + ": invalid status")
        proof = record.get("evidence")
        if not isinstance(proof, list):
            errors.append(gid + ": evidence must be list")
            continue
        if state == "PASS":
            if not proof:
                errors.append(gid + ": false PASS without evidence")
            for item in proof:
                if not isinstance(item, dict) or not isinstance(item.get("file"),str) or not isinstance(item.get("sha256"),str):
                    errors.append(gid + ": evidence requires file+sha256")
                    continue
                f = (root / item["file"]).resolve()
                if not f.is_relative_to(root) or not f.is_file():
                    errors.append(gid + ": proof missing or outside project")
                    continue
                if hashlib.sha256(f.read_bytes()).hexdigest() != item["sha256"].lower():
                    errors.append(gid + ": evidence SHA256 mismatch")
    if release:
        if doc.get("release_ready") is not True: errors.append("release_ready is false")
        if not sha: errors.append("Final build checksum required")
        if str(doc.get("candidate_version","")).startswith("prototype"):
            errors.append("Rejected prototype cannot be a release")
        for gid in GATES:
            if isinstance(gates.get(gid),dict) and gates[gid].get("status") != "PASS":
                errors.append(gid + ": not PASS")
        page = root / "index.html"
        if not page.is_file():
            errors.append("index.html not found")
        elif sha and hashlib.sha256(page.read_bytes()).hexdigest() != sha.lower():
            errors.append("candidate_sha256 does not match final index.html")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["lint","release"], default="lint")
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    try:
        doc = json.loads((args.root/"qa"/"release.json").read_text(encoding="utf8"))
    except (OSError, ValueError) as e:
        print("QA ERROR:",e)
        return 1
    errs = inspect(doc,args.root,release=args.mode=="release")
    if errs:
        print("REJECTED:")
        for error in errs: print(" -", error)
        return 1
    if args.mode=="lint":
        print("Manifest syntactically valid. Release state: %s. No visual approval implied." %
              ("CANDIDATE" if doc.get("release_ready") else "BLOCKED"))
    else:
        print("Mechanical release evidence checks pass. Human visual review still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
