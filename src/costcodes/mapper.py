"""Map free text cost descriptions to MasterFormat divisions."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from .rules import DIVISIONS, KEYWORDS


@dataclass(frozen=True)
class Match:
    """Result for one description."""

    division: str | None
    name: str
    score: int
    runner_up: str | None

    @property
    def confidence(self) -> str:
        """high when one division clearly leads, low when tied or weak, none if no match."""
        if self.division is None:
            return "none"
        if self.runner_up is not None:
            return "low"
        return "high" if self.score >= 2 else "medium"


def _count(text: str, keyword: str) -> int:
    """Count whole-word occurrences of a keyword (or phrase) in text."""
    pattern = r"(?<![a-z0-9])" + re.escape(keyword.strip()) + r"(?:s|es)?(?![a-z0-9])"
    return len(re.findall(pattern, text))


def classify(description: str) -> Match:
    """Pick the division with the most keyword hits; longer keywords weigh more.

    A tie for first place is reported through runner_up so the caller can review it.
    """
    text = description.lower()
    scores: dict[str, int] = {}
    for division, words in KEYWORDS.items():
        score = sum(_count(text, w) * (2 if " " in w.strip() else 1) for w in words)
        if score:
            scores[division] = score
    if not scores:
        return Match(None, "Unclassified", 0, None)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    best, best_score = ranked[0]
    tied = ranked[1][0] if len(ranked) > 1 and ranked[1][1] == best_score else None
    return Match(best, DIVISIONS[best], best_score, tied)


def read_costs(path: str | Path, column: str = "description", amount: str = "amount") -> list[dict]:
    """Read a cost CSV; every row gets 'description' and a float 'amount' (0 if absent)."""
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if column not in (reader.fieldnames or []):
            raise ValueError(f"column {column!r} not found; columns are {reader.fieldnames}")
        for row in reader:
            raw = (row.get(amount) or "0").replace(",", "").replace("$", "").strip() or "0"
            try:
                value = float(raw)
            except ValueError as error:
                raise ValueError(f"bad amount {row.get(amount)!r} in row {row}") from error
            rows.append({**row, "description": row[column], "amount": value})
    return rows


def map_rows(rows: list[dict]) -> list[dict]:
    """Add division, division_name and confidence to each row."""
    mapped = []
    for row in rows:
        match = classify(row["description"])
        mapped.append({**row, "division": match.division or "", "division_name": match.name,
                       "confidence": match.confidence})
    return mapped


def summarize(mapped: list[dict]) -> list[tuple[str, str, int, float]]:
    """Totals per division as (division, name, line count, amount), unclassified last."""
    totals: dict[str, list] = {}
    for row in mapped:
        entry = totals.setdefault(row["division"], [row["division_name"], 0, 0.0])
        entry[1] += 1
        entry[2] += row["amount"]
    ordered = sorted(totals.items(), key=lambda kv: (kv[0] == "", kv[0]))
    return [(code or "--", name, count, amount) for code, (name, count, amount) in ordered]
