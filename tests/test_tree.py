"""الشجرةُ المرخَّصة (`tools/gen_tree_index.py`، ADR ٢): القسمةُ تامّة، والزائدةُ تشير إلى أصلها.

التوقّعاتُ مكتوبةٌ باليد على شجرةٍ صغيرةٍ مصنوعة، لا محسوبةٌ بالمولِّد؛ ولكلّ شرطٍ طفرةٌ مرفوضةٌ باسمها.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("gen_tree_index", ROOT / "tools" / "gen_tree_index.py")
assert _spec and _spec.loader
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

E = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
HERE = [("a/x.py", "b1"), ("a/y.py", "b1"), ("b/z.py", "b2"), ("suspended/s.py", "b3"),
        ("CLAUDE.md", "b4"), ("e.py", E), ("f.py", E), ("m.py", "bG")]
GHANEM = [("m2.py", "bG"), ("CLAUDE.md", "b5")]

EXPECTED = {  # باليد، بترتيب الأصناف المعلَن
    "CLAUDE.md": ("مختلف_عن_الغانم", "alghanem"),
    "a/x.py": ("بقية", ""),
    "a/y.py": ("مكرر_داخلي", "a/x.py"),
    "b/z.py": ("بقية", ""),
    "e.py": ("فارغ", ""),
    "f.py": ("فارغ", ""),
    "m.py": ("مطابق_للغانم", "alghanem"),
    "suspended/s.py": ("معلق", ""),
}


def test_partition_by_hand() -> None:
    rows = T.classify(HERE, GHANEM)
    assert {r["path"]: (r["class"], r["origin"]) for r in rows} == EXPECTED
    assert T.verify(rows, HERE) == []


def test_empty_files_are_not_duplicates() -> None:
    # الطفرة: لو عُدَّ الفارغُ مكرَّرًا لصار f.py زائدةً لـe.py — وهو لا محتوى له يُنسخ
    rows = {r["path"]: r["class"] for r in T.classify(HERE, GHANEM)}
    assert rows["f.py"] == "فارغ" != "مكرر_داخلي"


def test_mutation_file_without_class() -> None:
    rows = T.classify(HERE, GHANEM)[1:]
    assert "FILE_WITHOUT_CLASS" in T.verify(rows, HERE)


def test_mutation_file_in_two_classes() -> None:
    rows = T.classify(HERE, GHANEM)
    rows.append({**rows[0], "class": "بقية"})
    assert "FILE_IN_TWO_CLASSES" in T.verify(rows, HERE)


def test_mutation_duplicate_pointing_to_itself() -> None:
    rows = [{**r, "origin": r["path"]} if r["class"] == "مكرر_داخلي" else r
            for r in T.classify(HERE, GHANEM)]
    assert "DUPLICATE_WITHOUT_ORIGIN:a/y.py" in T.verify(rows, HERE)


def test_mutation_undeclared_class() -> None:
    rows = [{**r, "class": "مرخص"} if r["path"] == "b/z.py" else r for r in T.classify(HERE, GHANEM)]
    assert "UNDECLARED_CLASS:b/z.py" in T.verify(rows, HERE)


def test_the_real_tree_is_partitioned_and_current() -> None:
    dep = json.loads((ROOT / "deposits" / "alghanem-tree.json").read_text(encoding="utf-8"))
    here = T.inventory()
    rows = T.classify(here, [tuple(x) for x in dep["files"]])
    assert T.verify(rows, here) == []
    assert sum(1 for _ in rows) == len(here)
    assert T.main(["--check"]) == 0
