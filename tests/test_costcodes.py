from pathlib import Path

import pytest

from costcodes.cli import main
from costcodes.mapper import classify, map_rows, read_costs, summarize
from costcodes.rules import DIVISIONS, KEYWORDS

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "costs.csv"


def test_every_keyword_division_is_named():
    assert set(KEYWORDS) <= set(DIVISIONS)


@pytest.mark.parametrize("text,division", [
    ("Concrete slab patch", "03"),
    ("Replace roof membrane", "07"),
    ("Sprinkler head relocation", "21"),
    ("Domestic water piping", "22"),
    ("Install new elevator controller", "14"),
    ("Fire alarm devices", "28"),
])
def test_classify_known(text, division):
    assert classify(text).division == division


def test_no_match_is_unclassified():
    m = classify("Miscellaneous items")
    assert m.division is None and m.confidence == "none"


def test_empty_text():
    assert classify("").division is None


def test_case_and_plural_insensitive():
    assert classify("DOORS and Windows").division == "08"


def test_whole_word_only():
    assert classify("Subpanel").division is None


def test_tie_lowers_confidence():
    m = classify("concrete and roof")
    assert m.runner_up is not None and m.confidence == "low"


def test_phrase_weighs_more_than_single_word():
    assert classify("fire alarm panel").division == "28"


def test_read_costs_missing_column(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_costs(p)


def test_read_costs_bad_amount(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text("description,amount\nconcrete,abc\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_costs(p)


def test_summary_totals_match_input():
    mapped = map_rows(read_costs(EXAMPLE))
    total = sum(r["amount"] for r in mapped)
    assert sum(a for *_, a in summarize(mapped)) == pytest.approx(total)
    assert summarize(mapped)[-1][0] == "--"


def test_cli_lookup(capsys):
    assert main(["lookup", "boiler replacement"]) == 0
    assert capsys.readouterr().out.startswith("23")


def test_cli_map_writes_csv(tmp_path, capsys):
    out = tmp_path / "o.csv"
    assert main(["map", str(EXAMPLE), "--out", str(out)]) == 0
    assert "division_name" in out.read_text(encoding="utf-8").splitlines()[0]


def test_cli_missing_file(capsys):
    assert main(["summary", "missing.csv"]) == 2
