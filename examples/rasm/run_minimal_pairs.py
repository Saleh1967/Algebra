"""الأزواجُ الدنيا في الحال — تشغيلُ ختم `51bd90a4…`.

صنفان من الألفاظ متطابقا الحروف موضعًا موضعًا، يختلفان في حال وحدةٍ واحدة.
والتعريفاتُ كلُّها نصُّ الاستخراج في الختم.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
MARKUP = "<sel>"
LEAST = 5

Units = tuple[tuple[str, str], ...]


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_cv_peel", RASM / "run_cv_peel.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def types(text: str) -> dict[Units, str]:
    """كلُّ صنفٍ مختلف الوحدات، ومعه أوّلُ لفظٍ ظهر به."""

    peeler = _peeler()
    found: dict[Units, str] = {}
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            kept = tuple(
                (letter, state)
                for (letter, state), extra in zip(units, extras, strict=True)
                if letter != peeler.STRUCTURE and extra.get("تنوين") != "ذيل"
            )
            if kept:
                found.setdefault(kept, token)
    return found


def pairs(found: dict[Units, str]) -> list[tuple[int, int, str, str]]:
    """(الطول، موضعُ الاختلاف، اللفظ الأوّل، اللفظ الثاني) لكلّ زوجٍ أدنى."""

    groups: dict[tuple[str, ...], list[Units]] = defaultdict(list)
    for kept in found:
        groups[tuple(letter for letter, _ in kept)].append(kept)
    out: list[tuple[int, int, str, str]] = []
    for members in groups.values():
        for one, two in combinations(members, 2):
            where = [i for i, (a, b) in enumerate(zip(one, two, strict=True)) if a != b]
            if len(where) == 1:
                out.append((len(one), where[0], found[one], found[two]))
    return out


def place(length: int, where: int) -> str:
    """الأولى، أو الثانية، أو الأخيرة، أو الوسط."""

    if where == length - 1:
        return "الأخيرة"
    if where == 0:
        return "الأولى"
    if where == 1:
        return "الثانية"
    return "الوسط"


def verdicts(found: list[tuple[int, int, str, str]]) -> dict[str, Fraction]:
    """م١ وم٢ وم٣ على أزواج المقام، ومعها ما يُعرَض."""

    scope = [(length, where) for length, where, _, _ in found if length >= LEAST]
    total = len(scope)
    places = Counter(place(length, where) for length, where in scope)
    edges = Fraction(total - places["الوسط"], total)
    uniform = sum(Fraction(3, length) for length, _ in scope) / total
    by_index: Counter[int] = Counter()
    for length, where in scope:
        by_index[-1 if where == length - 1 else where] += 1
    last = by_index[-1]
    other = max(count for index, count in by_index.items() if index != -1)
    return {
        "الأزواج": Fraction(len(found)),
        "المقام": Fraction(total),
        "م١": edges,
        "التساوي": uniform,
        "م٢": edges - uniform,
        "م٣": Fraction(last - other, total),
        "الأخيرة": Fraction(places["الأخيرة"], total),
        "الأولى": Fraction(places["الأولى"], total),
        "الثانية": Fraction(places["الثانية"], total),
        "الوسط": Fraction(places["الوسط"], total),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    found = pairs(types(given.text.read_text(encoding="utf-8").rstrip("\n")))
    for name, value in verdicts(found).items():
        print(
            f"{name}: {float(value):.4f}"
            if value.denominator != 1
            else f"{name}: {value}"
        )
    shown: dict[str, list[str]] = defaultdict(list)
    for length, where, one, two in found:
        if length >= LEAST and len(shown[place(length, where)]) < 12:
            shown[place(length, where)].append(f"{one}/{two}")
    for name, examples in shown.items():
        print(f"  {name}: {' · '.join(examples)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
