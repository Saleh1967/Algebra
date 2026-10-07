"""سلّمُ السياق بتّةً بتّة بلا تسريب — تشغيلُ ختم `d568a91d…`.

**لا اسمَ يدخل السجلّ**: المحرفُ **شريحةٌ ونقطةُ ترميز**، والسياقُ **ما
مضى وحدَه**، والأسئلةُ **دوالُّ في البايتات**.
"""

from __future__ import annotations

import argparse
import math
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
BARE = "·"
START = "⊢"
MOST = 12
WITNESS = 1_000


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    if one and marked(one[-1]):
        return one[-1]
    return BARE


def final_letter(one: str) -> str:
    for two in reversed(one):
        if not marked(two):
            return two
    return BARE


def shown(one: str) -> str:
    """صورةُ المحرف: شريحتُه ونقطةُ ترميزه — **ولا اسمَ يونيكود**."""

    if one in (BARE, START):
        return one
    return f"{one} U+{ord(one):04X}"


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


def attached(rows: list[tuple[tuple[bool, ...], str]]) -> float:
    """H(الحال | الكتلة) على العيّنة نفسِها."""

    blocks: defaultdict[tuple[bool, ...], Counter[str]] = defaultdict(Counter)
    for key, state in rows:
        blocks[key][state] += 1
    total = len(rows)
    if total == 0:
        return 0.0
    return math.fsum(
        sum(one.values()) / total * entropy(one) for one in blocks.values()
    )


def kept(
    taught: list[tuple[tuple[bool, ...], str]],
    asked: list[tuple[tuple[bool, ...], str]],
    states: list[str],
) -> float:
    """ثمنُ الحال على المحجوز بشفرةٍ قُدِّرت على الآخر — تنعيمُ لابلاس."""

    blocks: defaultdict[tuple[bool, ...], Counter[str]] = defaultdict(Counter)
    for key, state in taught:
        blocks[key][state] += 1
    if not asked:
        return 0.0
    cost = 0.0
    for key, state in asked:
        seen = blocks.get(key, Counter())
        denominator = sum(seen.values()) + len(states)
        cost -= math.log2((seen.get(state, 0) + 1) / denominator)
    return cost / len(asked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
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
    print("— السياقُ: ما مضى وحدَه؛ ولا شيءَ من بايتات الموضع المسؤولِ عنه")

    # (حالُ السابق، حرفُ خاتمة السابق، حالُ ما قبله، أوّلُ السطر، آخرُه) ⟶ الحال
    facts: list[tuple[str, str, str, bool, bool]] = []
    answers: list[str] = []
    halves: list[int] = []
    states: Counter[str] = Counter()
    counted = 0
    most_slack = -float("inf")

    for number, line in enumerate(lines):
        row = [one for one in line.split() if arabic(one)]
        for place, token in enumerate(row):
            before = ending(row[place - 1]) if place else START
            letter = final_letter(row[place - 1]) if place else START
            older = ending(row[place - 2]) if place >= 2 else START
            facts.append((before, letter, older, place == 0, place == len(row) - 1))
            answers.append(ending(token))
            halves.append(number % 2)
            states[ending(token)] += 1
            counted += 1
        if counted >= WITNESS:
            most_slack = max(
                most_slack, arrangements(states) - counted * entropy(states)
            )

    print(f"— الألفاظ: {len(answers)} | وعبرَ العدّادات {counted}")
    print(f"— خاناتُ الحال: {len(states)} | H = {entropy(states):.4f}")
    for state, number in states.most_common():
        print(f"    {shown(state)} | {number} | نصيبٌ {number / counted:.4f}")

    every = sorted(states)
    questions: list[tuple[int, str]] = []
    for index in (0, 2):
        for value in sorted({one[index] for one in facts}):
            questions.append((index, value))
    for value in sorted({one[1] for one in facts}):
        questions.append((1, value))
    questions.append((3, ""))
    questions.append((4, ""))
    print(f"\n— الأسئلةُ المتاحة: {len(questions)} (قيمُها مجموعةٌ من المجمَّد)")

    def ask(fact: tuple[str, str, str, bool, bool], which: tuple[int, str]) -> bool:
        index, value = which
        if index in (3, 4):
            return bool(fact[index])
        return bool(fact[index] == value)

    names = {
        0: "حالُ السابق",
        1: "حرفُ خاتمةِ السابق",
        2: "حالُ ما قبله",
        3: "أوّلُ السطر",
        4: "آخرُ السطر",
    }
    keys: list[tuple[bool, ...]] = [() for _ in facts]
    chosen: list[tuple[int, str]] = []
    trail: list[tuple[float, float, float, float, int]] = []

    def split(where: list[int]) -> list[tuple[tuple[bool, ...], str]]:
        return [(keys[one], answers[one]) for one in where]

    even = [one for one in range(len(facts)) if halves[one] == 0]
    odd = [one for one in range(len(facts)) if halves[one] == 1]
    here_in = attached(split(list(range(len(facts)))))
    here_out = (
        kept(split(even), split(odd), every) + kept(split(odd), split(even), every)
    ) / 2
    trail.append((here_in, here_out, 0.0, 0.0, 1))
    print(f"\n— د٠ بلا سؤال: ملحَقة {here_in:.4f} | محجوزة {here_out:.4f} | كتلةٌ 1")

    for depth in range(1, MOST + 1):
        best: tuple[float, float, float, tuple[int, str], list[tuple[bool, ...]]] | None
        best = None
        for which in questions:
            if which in chosen:
                continue
            trial = [keys[one] + (ask(facts[one], which),) for one in range(len(facts))]
            saved = keys
            keys = trial
            gain_out = (
                here_out
                - (
                    kept(split(even), split(odd), every)
                    + kept(split(odd), split(even), every)
                )
                / 2
            )
            gain_in = here_in - attached(split(list(range(len(facts)))))
            keys = saved
            if best is None or gain_out > best[0]:
                best = (gain_out, gain_in, 0.0, which, trial)
        if best is None or best[0] <= 0:
            print(f"  الوقوف: لا سؤالَ يربح محجوزًا عند الدرجة {depth}")
            break
        gain_out, gain_in, _, which, trial = best
        keys = trial
        chosen.append(which)
        here_in -= gain_in
        here_out -= gain_out
        blocks = len(set(keys))
        trail.append((here_in, here_out, gain_in, gain_out, blocks))
        index, value = which
        label = names[index] if index in (3, 4) else f"{names[index]} = {shown(value)}"
        print(
            f"— د{depth} «{label}»: ملحَقة {here_in:.4f} | محجوزة {here_out:.4f}"
            f" | ربحٌ ملحَقٌ {gain_in:+.4f} | ربحٌ محجوزٌ {gain_out:+.4f}"
            f" | كتلٌ {blocks}"
        )

    print(f"\n— الدرجاتُ المبلوغة: {len(chosen)}")
    print(f"  مجموعُ الكسب المحجوز: {sum(one[3] for one in trail):+.6f}")
    print(f"  مجموعُ الكسب الملحَق: {sum(one[2] for one in trail):+.6f}")
    if chosen:
        share = trail[1][3] / sum(one[3] for one in trail)
        print(f"  نصيبُ الدرجة الأولى من الكسب المحجوز: {share:.4f}")
    lowest_in = min(one[2] for one in trail[1:]) if chosen else 0.0
    print(f"  أدنى ربحٍ ملحَق: {lowest_in:+.6f}")
    print(f"  أدنى (محجوزة − ملحَقة): " f"{min(one[1] - one[0] for one in trail):+.6f}")
    print(f"  كتلُ آخر درجة: {trail[-1][4]}")
    print(f"  أقصى (log₂ التباديل − N·H) بعد ألف = {most_slack:+.6f}")
    tally: Counter[str] = Counter(names[one] for one, _ in chosen)
    for name in sorted(tally):
        print(f"  أسئلةُ «{name}»: {tally[name]}")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — شريحةٌ ونقطةُ ترميز")
    print("  ولا قائمةَ مُودَعةٌ ولا صورةٌ منقولةٌ عن نصٍّ خارجيّ")
    print("  والجشعُ غيرُ مبرهَن: ما بُلِغ حدٌّ أدنى، ولا يُقال «لا يُبلَغ»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
