"""جردُ العُري ومواضعِ الإعراب — عرضُ دعوى «جسر الإملاء» على البايتات.

**الدعوى** (§١): العُري التي كشفها تدقيقُ البايتات **ليست عشواءَ موزَّعة، بل
أصنافٌ غيرُ مسمّاة** — ألفُ «قَالَ» مدٌّ محمول، وألفُ «الْحَمْدُ» همزةُ وصل.

**وما يُقاس ههنا ثلاثةٌ**:

1. **جردُ العُري بالحرف** — فإن كانت أصنافًا تركّزت، وإن كانت عشواءَ انتشرت.
2. **تعيُّنُ ألف المدّ** — `H(حالة | ا، ما قبلَها فتحة)`. فدعوى «صفرِ بتٍّ
   شرطيّ» تُقاس ولا تُسلَّم، وما شذّ يُسمّى ولا يُطوى.
3. **موضعُ الإعراب مقابلَ كلّ موضع** — `H(حالة | حرف)` على **أواخر الكلم**
   وحدَها، بإزاء كلّ المواضع. فدعوى أنّ الفجوةَ «عند أواخر المُعرَبات»
   تُعطى نصيبَها من Δضبط عدًّا لا تقديرًا.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"
FATHA = "َ"
MADD = "اوي"
MARKUP = "<sel>"


def _audit() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للمواصفة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def bare_census(units: list[tuple[str, str]]) -> Counter[str]:
    """أيُّ الحروفِ تعرى، وكم؟"""

    return Counter(letter for letter, state in units if not state)


def after_fatha(units: list[tuple[str, str]], letter: str) -> Counter[str]:
    """توزيعُ حالةِ حرفٍ بعينه حين تسبقه فتحة."""

    found: Counter[str] = Counter()
    for index in range(1, len(units)):
        if units[index][0] == letter and units[index - 1][1] == FATHA:
            found[units[index][1]] += 1
    return found


def conditional(units: list[tuple[str, str]]) -> float:
    """H(حالة | حرف) على المجموعة المعطاة."""

    by_letter: dict[str, Counter[str]] = defaultdict(Counter)
    for letter, state in units:
        by_letter[letter][state] += 1
    total = len(units)
    return math.fsum(
        (sum(counts.values()) / total) * entropy(counts)
        for counts in by_letter.values()
    )


def final_units(text: str) -> list[tuple[str, str]]:
    """آخرُ موضعِ رسمٍ من كلّ كلمة — وهو موضعُ الإعراب."""

    audit = _audit()
    found: list[tuple[str, str]] = []
    for token in text.split():
        units = audit.rasm_units(token)  # type: ignore[attr-defined]
        if units:
            found.append(units[-1])
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    audit = _audit()
    text = given.text.read_text(encoding="utf-8").replace(MARKUP, " ")
    units = audit.rasm_units(text)  # type: ignore[attr-defined]

    census = bare_census(units)
    bare = sum(census.values())
    madd = sum(census[letter] for letter in MADD)
    print(f"مواضعُ الرسم: {len(units)} | العُري: {bare}")
    print(f"أكثرُها: {census.most_common(6)}")
    print(f"نصيبُ حروف المدّ (ا و ي): {madd / bare:.4f}")
    print(f"حروفٌ تعرى: {len(census)} من {len({letter for letter, _ in units})}")

    alif = after_fatha(units, "ا")
    seen = sum(alif.values())
    print(f"\nألفٌ بعد فتحة: {seen} موضعًا")
    print(f"  H(حالة) = {entropy(alif):.4f} بت | نصيبُ العُري {alif[''] / seen:.4f}")
    print(f"  والشاذُّ مسمًّى: {[one for one in alif if one]}")

    finals = final_units(text)
    print(f"\nكلُّ المواضع ({len(units)}): H(حالة|حرف) = {conditional(units):.4f}")
    print(f"أواخرُ الكلم ({len(finals)}): H(حالة|حرف) = {conditional(finals):.4f}")
    share = conditional(finals) * len(finals) / (conditional(units) * len(units))
    print(f"نصيبُ الأواخر من Δضبط: {share:.4f}")
    print(f"وlog2(3) = {math.log2(3):.4f} | log2(8) = {math.log2(8):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
