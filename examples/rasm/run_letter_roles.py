"""أدوارُ حروف «سألتمونيها» في فضاء الـ١١٢ — تشغيلُ ختم `72b39b4c…`.

**ما يُقاس**: كلُّ وحدةٍ من الحروف التسعة (ا س ت ه م و ن ي ل بعد الطيّ) تقع
في خانةٍ من الجدول المُودَع — (حرف، موضع، حال) — ويُعَدّ لها **عددُ الأدوار
الممكنة** في خانتها. **ولا يُقاس الدورُ الصحيح**: لا مرجعَ مُودَعٌ له.

**والجدولُ مسوّدةٌ غيرُ موقَّعة**: يُقاس أثرُه ولا يُرقّي مستوى الكلمة.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType

REPOSITORY = Path(__file__).resolve().parents[2]
PEELER = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
TABLE = REPOSITORY / "deposits" / "letter_roles_draft.tsv"

MARKUP = "<sel>"
NINE = "استهمونيل"
STATES = {"َ": "فتحة", "ُ": "ضمة", "ِ": "كسرة", "ْ": "سكون"}
EMPTY = "—"

Cell = tuple[str, str, str]


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEELER)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def table() -> dict[Cell, frozenset[str]]:
    """الجدولُ المُودَع: (حرف، موضع، حال) ⟼ الأدوارُ الممكنة."""

    rows = [
        line.split("\t")
        for line in TABLE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ][1:]
    found: dict[Cell, frozenset[str]] = {}
    for letter, place, state, roles, _ in rows:
        found[(letter, place, state)] = (
            frozenset() if roles == EMPTY else frozenset(roles.split("،"))
        )
    return found


def inventory(roles: dict[Cell, frozenset[str]]) -> dict[str, frozenset[str]]:
    """رصيدُ الحرف: اتّحادُ أدوار خاناته في الجدول."""

    found: dict[str, set[str]] = defaultdict(set)
    for (letter, _, _), one in roles.items():
        found[letter] |= one
    return {letter: frozenset(one) for letter, one in found.items()}


def cells(text: str) -> Counter[Cell]:
    """خاناتُ الحروف التسعة كما تقع في المدوّنة، بعدّها."""

    peeler = _peeler()
    found: Counter[Cell] = Counter()
    for token in text.replace(MARKUP, " ").split():
        units, _ = peeler.peel(token)
        last = len(units) - 1
        for index, (letter, state) in enumerate(units):
            if letter not in NINE:
                continue
            if index == 0:
                place = "أوّل"
            elif index == last:
                place = "آخر"
            else:
                place = "وسط"
            found[(letter, place, STATES[state])] += 1
    return found


@dataclass(frozen=True, slots=True)
class Reading:
    """ما يُحكَم به على الشروط الخمسة، وما يُسرَد معه."""

    occurrences: int
    in_empty: int
    decided_letters: tuple[str, ...]
    single: int
    candidates: Fraction
    narrowing: Fraction
    per_letter: dict[str, tuple[int, Fraction, int, int]]
    empty_cells: dict[Cell, int]


def read(text: str) -> Reading:
    roles = table()
    stock = inventory(roles)
    seen = cells(text)
    total = sum(seen.values())
    in_empty = sum(count for cell, count in seen.items() if not roles[cell])
    single = sum(count for cell, count in seen.items() if len(roles[cell]) == 1)
    candidates = Fraction(
        sum(count * len(roles[cell]) for cell, count in seen.items()), total
    )
    narrowing = Fraction(
        sum(
            count * (len(stock[cell[0]]) - len(roles[cell]))
            for cell, count in seen.items()
        ),
        total,
    )
    decided = tuple(
        letter
        for letter in NINE
        if all(len(roles[cell]) == 1 for cell in seen if cell[0] == letter)
    )
    per_letter: dict[str, tuple[int, Fraction, int, int]] = {}
    for letter in NINE:
        mine = {cell: count for cell, count in seen.items() if cell[0] == letter}
        mass = sum(mine.values())
        mean = Fraction(sum(c * len(roles[cell]) for cell, c in mine.items()), mass)
        alone = sum(c for cell, c in mine.items() if len(roles[cell]) == 1)
        per_letter[letter] = (mass, mean, alone, len(stock[letter]))
    return Reading(
        occurrences=total,
        in_empty=in_empty,
        decided_letters=decided,
        single=single,
        candidates=candidates,
        narrowing=narrowing,
        per_letter=per_letter,
        empty_cells={cell: count for cell, count in seen.items() if not roles[cell]},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    reading = read(given.text.read_text(encoding="utf-8"))
    total = reading.occurrences
    print(f"مواضعُ الحروف التسعة: {total}")
    print(f"ر١ في خاناتٍ فارغة: {reading.in_empty} = {reading.in_empty / total:.5f}")
    print(f"   الخاناتُ الفارغة الواقعة: {reading.empty_cells}")
    print(f"ر٢ المحسومة: {len(reading.decided_letters)} {reading.decided_letters}")
    print(f"ر٣ في خانةٍ ذات دورٍ واحد: {reading.single} = {reading.single / total:.4f}")
    print(f"ر٤ متوسّطُ الأدوار الممكنة: {float(reading.candidates):.4f}")
    print(f"ر٥ متوسّطُ ما أسقطه الموقعُ والحال: {float(reading.narrowing):.4f}")
    print("\nالحرف | المواضع | متوسّطُ الأدوار | في خانةٍ ذات دورٍ واحد | الرصيد")
    for letter, (mass, mean, alone, stock) in reading.per_letter.items():
        print(f"  {letter} | {mass} | {float(mean):.4f} | {alone / mass:.4f} | {stock}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
