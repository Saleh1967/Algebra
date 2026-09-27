"""ثابتُ الجرّ في المستوى الثالث — تشغيلُ ختم `6be35fd8…`.

السلسلة: جارٌّ منفصل، ثمّ لفظٌ آخرُه كسرة، ثمّ لفظٌ يبدأ بـ«ال» أو «وَال».
والضابط: لفظٌ آخرُه ضمّة، ثمّ لفظٌ يبدأ كذلك. والجارُّ والحركةُ الأخيرة من
run_governed_vowel بعينهما.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
BASE_KASRA = 0.2632
CONSTANT = 1.6365


def _governed() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_governed_vowel", RASM / "run_governed_vowel.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئ")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def starts_with_al(units: list, extras: list, structure: str) -> bool:
    """هيكلُه يبدأ بـ«ال»، أو بواوٍ مفتوحة يليها «ال»."""

    kept = [
        (letter, state)
        for (letter, state), extra in zip(units, extras, strict=True)
        if letter != structure and extra.get("تنوين") != "ذيل"
    ]
    letters = "".join(letter for letter, _ in kept)
    if letters.startswith("ال"):
        return True
    return letters.startswith("وال") and kept[0][1] == "َ"


def census(text: str) -> dict[str, Counter[str]]:
    governed = _governed()
    peeler = governed._peeler()
    found: dict[str, Counter[str]] = {"سلسلة": Counter(), "ضابط": Counter()}
    for line in text.split("\n"):
        tokens = line.replace(governed.MARKUP, " ").split()
        peeled = [peeler.peel(token) for token in tokens]
        finals = [governed.final_vowel(*one, peeler.STRUCTURE) for one in peeled]
        for i in range(len(tokens) - 1):
            third = peeled[i + 1]
            if not starts_with_al(*third, peeler.STRUCTURE):
                continue
            last = finals[i + 1] or "لا حركة"
            if finals[i] == governed.DAMMA:
                found["ضابط"][last] += 1
            if (
                i >= 1
                and finals[i] == governed.KASRA
                and governed.kind(*peeled[i - 1], peeler.STRUCTURE) == "جر"
            ):
                found["سلسلة"][last] += 1
    return found


def share(counts: Counter[str]) -> tuple[int, int]:
    shown = sum(counts[one] for one in ("َ", "ُ", "ِ"))
    return (counts["ِ"], shown)


def pmi(kasra: int, shown: int) -> float:
    return math.log2((kasra / shown) / BASE_KASRA)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"))
    for kind, counts in found.items():
        print(kind, dict(counts))
    kasra, shown = share(found["سلسلة"])
    other, total = share(found["ضابط"])
    value = pmi(kasra, shown)
    print(f"السلسلة: {kasra}/{shown} = {kasra / shown:.4f} | PMI {value:.4f}")
    print(f"ث١: |{value:.4f} − {CONSTANT}| = {abs(value - CONSTANT):.4f}")
    print(
        f"ث٢: {value:.4f} − {math.log2(math.e):.4f} = {value - math.log2(math.e):.4f}"
    )
    gap = kasra / shown - other / total
    print(f"ث٣: {kasra / shown:.4f} − {other / total:.4f} = {gap:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
