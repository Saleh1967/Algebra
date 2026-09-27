"""الحركةُ الأخيرة بشرط العامل — تشغيلُ ختم `c35956ef…`.

اللفظُ الذي يلي عاملًا منفصلًا في سطره: حرفَ جرٍّ (مِنْ، فِي، عَنْ، إِلَى،
عَلَى) أو «إِنَّ». وحركتُه الأخيرة حالُ آخرِ وحدةٍ فيه بعد طرح البنيويّ وذيل
التنوين. والتعريفاتُ كلُّها نصُّ الاستخراج في الختم.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
MARKUP = "<sel>"
FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
VOWELS = (FATHA, DAMMA, KASRA)
PREPOSITIONS = {
    ("من", KASRA),
    ("في", KASRA),
    ("عن", FATHA),
    ("علا", FATHA),
    ("الا", KASRA),
}
INNA = ("انن", KASRA)


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


def _letters(units: list, extras: list, structure: str) -> list[tuple[str, str, dict]]:
    return [
        (letter, state, extra)
        for (letter, state), extra in zip(units, extras, strict=True)
        if letter != structure and extra.get("تنوين") != "ذيل"
    ]


def kind(units: list, extras: list, structure: str) -> str | None:
    """«جر» أو «إنّ» أو لا شيء — بالهيكل والوحدة الأولى والشدّة."""

    found = _letters(units, extras, structure)
    if not found:
        return None
    skeleton = "".join(letter for letter, _, _ in found)
    first = found[0][1]
    doubled = any(extra.get("شدّة") == "نعم" for _, _, extra in found)
    if (skeleton, first) in PREPOSITIONS and not doubled:
        return "جر"
    if (skeleton, first) == INNA and doubled:
        return "إنّ"
    return None


def final_vowel(units: list, extras: list, structure: str) -> str | None:
    """حالُ آخرِ وحدةٍ غيرِ بنيويّة بلا ذيل التنوين، إن كانت حركة."""

    found = _letters(units, extras, structure)
    if not found:
        return None
    state = found[-1][1]
    return state if state in VOWELS else None


def census(text: str) -> dict[str, Counter[str]]:
    """لكلّ عامل: توزيعُ الحركة الأخيرة في اللفظ الذي يليه، ومعه ما لا حركةَ له."""

    peeler = _peeler()
    found: dict[str, Counter[str]] = {"جر": Counter(), "إنّ": Counter()}
    for line in text.split("\n"):
        tokens = line.replace(MARKUP, " ").split()
        peeled = [peeler.peel(token) for token in tokens]
        for here, after in zip(peeled, peeled[1:]):
            governor = kind(*here, peeler.STRUCTURE)
            if governor is None:
                continue
            vowel = final_vowel(*after, peeler.STRUCTURE)
            found[governor][vowel or "لا حركة"] += 1
    return found


def share(counts: Counter[str], vowel: str) -> tuple[int, int]:
    """(عددُ الحركة المسمّاة، عددُ ما ظهرت حركتُه)."""

    shown = sum(counts[one] for one in VOWELS)
    return (counts[vowel], shown)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"))
    names = {FATHA: "فتحة", DAMMA: "ضمة", KASRA: "كسرة"}
    for governor, counts in found.items():
        shown = sum(counts[one] for one in VOWELS)
        parts = " | ".join(f"{names[one]} {counts[one]}" for one in VOWELS)
        print(f"{governor}: ظاهرة {shown} ({parts}) | لا حركة {counts['لا حركة']}")
    kasra, shown = share(found["جر"], KASRA)
    print(f"ت١: كسرة بعد الجرّ {kasra}/{shown} = {kasra / shown:.4f}")
    fatha, after = share(found["إنّ"], FATHA)
    print(f"ت٢: فتحة بعد إنّ {fatha}/{after} = {fatha / after:.4f}")
    other, _ = share(found["إنّ"], KASRA)
    gap = kasra / shown - other / after
    print(f"ت٣: {kasra / shown:.4f} − {other / after:.4f} = {gap:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
