"""Builds the entry for the One Sentence for a Traveler from 1800 bounty.

Reads the sentence from entry.txt beside this script, checks the house gate
(1..200 characters, not blank), copies it into the makefun output directory
and prints a small receipt as JSON.
"""
import json
import os
from pathlib import Path

GATE_MIN = 1
GATE_MAX = 200


def collect():
    where = Path(__file__).resolve().parent
    raw = (where / "entry.txt").read_text(encoding="utf-8")
    text = raw.strip()
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise SystemExit(f"gate fail: {len(text)} chars, need {GATE_MIN}..{GATE_MAX}")
    return text


def deliver(text):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    target = Path(out_dir) if out_dir else Path(__file__).resolve().parent
    target.mkdir(parents=True, exist_ok=True)
    (target / "entry.txt").write_text(text + "\n", encoding="utf-8", newline="\n")
    return target / "entry.txt"


def main():
    sentence = collect()
    landed = deliver(sentence)
    print(json.dumps({
        "ok": True,
        "chars": len(sentence),
        "words": len(sentence.split()),
        "wrote": str(landed),
        "preview": sentence[:60],
    }))


if __name__ == "__main__":
    main()
