"""Command line for the cost code mapper."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .mapper import classify, map_rows, read_costs, summarize


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(prog="costcodes", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    look = sub.add_parser("lookup", help="classify one description")
    look.add_argument("text")

    for name, help_text in (("map", "label every row with a division"),
                            ("summary", "totals per division")):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("csv", type=Path)
        cmd.add_argument("--column", default="description")
        cmd.add_argument("--amount", default="amount")
    sub.choices["map"].add_argument("--out", type=Path, help="write the labeled CSV here")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line; return the exit code."""
    args = build_parser().parse_args(argv)
    if args.cmd == "lookup":
        m = classify(args.text)
        extra = f"  (tied with {m.runner_up})" if m.runner_up else ""
        print(f"{m.division or '--'}  {m.name}  [{m.confidence}]{extra}")
        return 0
    try:
        mapped = map_rows(read_costs(args.csv, args.column, args.amount))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.cmd == "summary":
        for code, name, count, amount in summarize(mapped):
            print(f"{code:<3} {name:<42} {count:>3} lines {amount:>13,.2f}")
        print(f"{'':<3} {'Total':<42} {len(mapped):>3} lines {sum(r['amount'] for r in mapped):>13,.2f}")
        return 0
    for row in mapped:
        print(f"{row['division'] or '--':<3} {row['confidence']:<7} {row['description']}")
    if args.out:
        with args.out.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(mapped[0]) if mapped else [])
            writer.writeheader()
            writer.writerows(mapped)
        print(f"wrote {len(mapped)} rows to {args.out}")
    review = sum(1 for r in mapped if r["confidence"] in ("low", "none"))
    print(f"{review} of {len(mapped)} rows need review")
    return 0
