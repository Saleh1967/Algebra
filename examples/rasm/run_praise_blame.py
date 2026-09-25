"""لوازمُ مسوّدةٍ منقولةٍ في حقل الحال — تشغيلُ ختم `efb2eac8…`.

**الصورُ تُقرأ من الإيداع بنمطٍ ولا تُكتَب ههنا**، وتُعرَض **شرائحَ من
المجمَّد بضبطها** لا حروفًا تُركَّب.

**ولا اسمَ بابٍ نحويٍّ يدخل السجلّ**: صورٌ ومواضعُ وعلاماتٌ وبتّات.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
BARE = "بلا علامة"
ROW = re.compile(r"^\| (\S+) \| (.+) \|$", re.MULTILINE)
SOURCE = "المقال"


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def skeleton(one: str) -> str:
    return "".join(two for two in one if not marked(two))


def ending(one: str) -> str:
    if one and marked(one[-1]):
        return one[-1]
    return BARE


def read_shapes(deposit: Path) -> list[str]:
    """أعمدةُ «الهيكل» من جدول الإيداع — بنمطٍ، لا كتابةً."""

    found = ROW.findall(deposit.read_text(encoding="utf-8"))
    kept = [one for one, where in found if arabic(one) and where.startswith(SOURCE)]
    if len(kept) != len(found):
        print(f"— صفوفٌ لا تحمل مصدرًا فأُسقِطت: {len(found) - len(kept)}")
    return kept


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -math.fsum(
        (one / total) * math.log2(one / total) for one in counts.values() if one
    )


def arrangements(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return (
        math.lgamma(total + 1)
        - math.fsum(math.lgamma(one + 1) for one in counts.values())
    ) / math.log(2)


def conditioned(pairs: Counter[tuple[str, str]]) -> float:
    """H(الحال | الشرط) — على العيّنة نفسِها."""

    total = sum(pairs.values())
    if total == 0:
        return 0.0
    given: Counter[str] = Counter()
    for (key, _), number in pairs.items():
        given[key] += number
    return -math.fsum(
        (number / total) * math.log2(number / given[key])
        for (key, _), number in pairs.items()
    )


def held_out(
    taught: Counter[tuple[str, str]], asked: Counter[tuple[str, str]], states: list[str]
) -> float:
    """ثمنُ الحال على المحجوز بشفرةٍ قُدِّرت على الآخر — تنعيمُ لابلاس."""

    given: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for (key, state), number in taught.items():
        given[key][state] += number
    keys = {one for one, _ in taught} | {one for one, _ in asked}
    total = sum(asked.values())
    if total == 0:
        return 0.0
    cost = 0.0
    for (key, state), number in asked.items():
        seen = given.get(key, Counter())
        denominator = sum(seen.values()) + len(states)
        cost -= number * math.log2((seen.get(state, 0) + 1) / denominator)
    assert keys  # كلُّ مفتاحٍ مرئيٍّ أو منعَّم، ولا خانةَ صفرٌ تُبطِل القسمة
    return cost / total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--rule", type=Path, required=True)
    given = parser.parse_args()

    lines = [
        one
        for one in given.text.read_text(encoding="utf-8").splitlines()
        if one.strip()
    ]
    if len(lines) != VERSES:
        raise SystemExit(f"المدوّنةُ تبدّلت: {len(lines)} لا {VERSES}")
    print(f"— الأسطر: {len(lines)}")
    print("— حدُّ اللفظ: فيه حرفٌ عربيّ (المُصحَّح من 494465d1…)")

    shapes = read_shapes(given.rule)
    print(f"— الصورُ المُودَعة: {len(shapes)} (مقروءةً من الإيداع)")

    rows = [[two for two in one.split() if arabic(two)] for one in lines]
    tokens = sum(len(one) for one in rows)
    print(f"— الألفاظ: {tokens}")

    seen_shapes: Counter[str] = Counter()
    slices: defaultdict[str, Counter[str]] = defaultdict(Counter)
    states: Counter[str] = Counter()
    after: Counter[str] = Counter()
    third: Counter[str] = Counter()
    at_head = 0

    # الدرجاتُ الخمس: (مفتاحُ الشرط، الحال)
    levels: list[Counter[tuple[str, str]]] = [Counter() for _ in range(5)]
    halves: list[list[Counter[tuple[str, str]]]] = [
        [Counter() for _ in range(5)] for _ in range(2)
    ]
    counted = 0
    most_slack = -float("inf")

    for number, row in enumerate(rows):
        for place, token in enumerate(row):
            bones = skeleton(token)
            state = ending(token)
            states[state] += 1
            counted += 1
            if bones in shapes:
                seen_shapes[bones] += 1
                slices[bones][token] += 1
                if place == 0:
                    at_head += 1
            near = ""
            step = 0
            for back in (1, 2):
                if place - back >= 0 and skeleton(row[place - back]) in shapes:
                    near = skeleton(row[place - back])
                    step = back
                    break
            before = ending(row[place - 1]) if place else "بدء"
            keys = (
                "·",
                "نعم" if near else "لا",
                near or "لا",
                f"{near}|{step}" if near else "لا",
                f"{near}|{step}|{before}" if near else f"لا|{before}",
            )
            for depth, key in enumerate(keys):
                levels[depth][(key, state)] += 1
                halves[number % 2][depth][(key, state)] += 1
            if near and step == 1:
                after[state] += 1
            if near and step == 2:
                third[state] += 1
        if counted >= 1_000:
            most_slack = max(
                most_slack, arrangements(states) - counted * entropy(states)
            )

    missing = sorted(one for one in shapes if one not in seen_shapes)
    print(f"\n— الصورُ الموجودة: {len(seen_shapes)} | الغائبة: {len(missing)}")
    for one in sorted(seen_shapes, key=lambda two: -seen_shapes[two]):
        forms = " · ".join(sorted(slices[one]))
        print(f"    وقوعاتٌ {seen_shapes[one]:5d} | شرائحُها: {forms}")
    for one in missing:
        print(f"    غائبةٌ باسمها: {one}")
    print(f"  وفي صدر السطر: {at_head} من {sum(seen_shapes.values())}")

    print(f"\n— حقلُ الحال العامّ: H = {entropy(states):.4f}")
    print(
        f"— الموضعُ التالي للصورة: مواضعُ {sum(after.values())}"
        f" | H = {entropy(after):.4f}"
    )
    for state, count in after.most_common():
        shown = "·" if state == BARE else state
        print(f"    {shown} {count} | نصيبٌ {count / sum(after.values()):.4f}")
    print(
        f"— الموضعُ الثالث: مواضعُ {sum(third.values())}" f" | H = {entropy(third):.4f}"
    )
    for state, count in third.most_common():
        shown = "·" if state == BARE else state
        print(f"    {shown} {count} | نصيبٌ {count / sum(third.values()):.4f}")

    names = [
        "د٠ بلا شرط",
        "د١ بتّةُ الجوار",
        "د٢ هويّةُ الصورة",
        "د٣ الصورةُ والموضع",
        "د٤ ومعهما حالُ السابق",
    ]
    every = sorted(states)
    print("\n— التصعيد بتّةً بتّة")
    attached = [conditioned(one) for one in levels]
    kept = [
        (
            held_out(halves[0][depth], halves[1][depth], every)
            + held_out(halves[1][depth], halves[0][depth], every)
        )
        / 2
        for depth in range(5)
    ]
    for depth, name in enumerate(names):
        step_in = attached[depth - 1] - attached[depth] if depth else 0.0
        step_out = kept[depth - 1] - kept[depth] if depth else 0.0
        print(
            f"    {name}: ملحَقة {attached[depth]:.4f}"
            f" | محجوزة {kept[depth]:.4f}"
            f" | ربحٌ ملحَقٌ {step_in:+.4f} | ربحٌ محجوزٌ {step_out:+.4f}"
        )
    falls_in = min(attached[depth - 1] - attached[depth] for depth in range(1, 5))
    falls_out = sum(1 for depth in range(1, 5) if kept[depth] < kept[depth - 1])
    print(f"  أدنى ربحٍ ملحَق: {falls_in:+.6f}")
    print(f"  درجاتٌ ينزل فيها المحجوز: {falls_out} من 4")
    print(
        f"  أدنى (المحجوزة − الملحَقة): "
        f"{min(kept[one] - attached[one] for one in range(5)):+.6f}"
    )
    print(f"  I(الحال ؛ بتّةُ الجوار) = {attached[0] - attached[1]:.6f}")
    print(f"  أقصى (log₂ التباديل − N·H) بعد ألف = {most_slack:+.6f}")

    print("\n— ما لا يفصل فيه هذا القياس")
    print(
        "  الأعاريبُ الأربعةُ للمخصوص المتأخّر: الحروفُ واحدةٌ والعلاماتُ "
        "واحدة — لا ترجيحَ في البتّات"
    )
    print("  والمسوّدةُ غيرُ موقَّعة: مُدخَلٌ يُختبَر لا حكمٌ يُبنى عليه")
    return 0


if __name__ == "__main__":
    sys.exit(main())
