"""فصلُ الوقف عن الجوار — تشغيلُ ختم `c4ffe307…`.

**الأسئلةُ مقروءةٌ من `deposits/context_ladder_run.log` بترتيبها**، ولا
يُعاد اختيارٌ جشع. والمجالان: (أ) كلُّ المواضع، (ب) ما ليس آخرَ سطره.

**ولا اسمَ يدخل السجلّ**: المحرفُ شريحةٌ ونقطةُ ترميز، **وقيمُ الأسئلة
مُشتَقّةٌ من نقاط الترميز المكتوبةِ في السجلّ لا من حرفٍ يُكتَب بيد**.
"""

from __future__ import annotations

import argparse
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LADDER = REPOSITORY / "deposits" / "context_ladder_run.log"
VERSES = 6_236
BARE = "·"
START = "⊢"
WITNESS = 1_000
NAMES = {
    0: "حالُ السابق",
    1: "حرفُ خاتمةِ السابق",
    2: "حالُ ما قبله",
    3: "أوّلُ السطر",
    4: "آخرُ السطر",
}


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


def questions_from_log() -> list[tuple[int, str]]:
    """الأسئلةُ بترتيبها من السجلّ — والقيمةُ من نقطة الترميز لا من حرفٍ يُكتَب."""

    text = LADDER.read_text(encoding="utf-8")
    asked = re.findall(r"^— د(\d+) «(.+?)»:", text, re.M)
    order: list[tuple[int, str]] = []
    for step, question in asked:
        if step == "0":
            continue
        head, _, tail = question.partition(" = ")
        index = next(one for one, two in NAMES.items() if two == head)
        if not tail:
            order.append((index, ""))
            continue
        point = re.search(r"U\+([0-9A-F]{4})$", tail)
        if point is not None:
            order.append((index, chr(int(point.group(1), 16))))
        elif tail in (BARE, START):
            order.append((index, tail))
        else:
            raise SystemExit(f"قيمةٌ لا تُشتَقّ من نقطة ترميز: {tail!r}")
    if not order:
        raise SystemExit("لا أسئلةَ في سجلّ السلّم")
    return order


def ask(fact: tuple[str, str, str, bool, bool], which: tuple[int, str]) -> bool:
    index, value = which
    if index in (3, 4):
        return bool(fact[index])
    return bool(fact[index] == value)


def label(which: tuple[int, str]) -> str:
    index, value = which
    if index in (3, 4):
        return NAMES[index]
    return f"{NAMES[index]} = {shown(value)}"


def climb(
    facts: list[tuple[str, str, str, bool, bool]],
    answers: list[str],
    halves: list[int],
    where: list[int],
    order: list[tuple[int, str]],
    every: list[str],
    stand: str,
) -> list[tuple[str, float, float]]:
    """تُطبَّق الأسئلةُ بترتيبها على مسندٍ واحد — ولا يُعاد اختيار."""

    keys: list[tuple[bool, ...]] = [() for _ in facts]
    even = [one for one in where if halves[one] == 0]
    odd = [one for one in where if halves[one] == 1]

    def split(rows: list[int]) -> list[tuple[tuple[bool, ...], str]]:
        return [(keys[one], answers[one]) for one in rows]

    def outside() -> float:
        return (
            kept(split(even), split(odd), every) + kept(split(odd), split(even), every)
        ) / 2

    here_in = attached(split(where))
    here_out = outside()
    print(f"\n— مقامُ {stand}: ألفاظٌ {len(where)}")
    print(f"— د٠ بلا سؤال: ملحَقة {here_in:.4f} | محجوزة {here_out:.4f}")
    steps: list[tuple[str, float, float]] = []
    for depth, which in enumerate(order, start=1):
        keys = [keys[one] + (ask(facts[one], which),) for one in range(len(facts))]
        after_in = attached(split(where))
        after_out = outside()
        gain_in = here_in - after_in
        gain_out = here_out - after_out
        blocks = len({keys[one] for one in where})
        print(
            f"— د{depth} «{label(which)}»: ملحَقة {after_in:.4f}"
            f" | محجوزة {after_out:.4f} | ربحٌ ملحَقٌ {gain_in:+.6f}"
            f" | ربحٌ محجوزٌ {gain_out:+.6f} | كتلٌ {blocks}"
        )
        steps.append((label(which), gain_in, gain_out))
        here_in, here_out = after_in, after_out
    return steps


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
    order = questions_from_log()
    print(f"— الأسطر: {len(lines)}")
    print("— حدُّ اللفظ: فيه حرفٌ عربيّ (المُصحَّح من 494465d1…)")
    print(f"— الأسئلةُ مقروءةٌ من السجلّ بترتيبها: {len(order)} — ولا اختيارَ جشع")

    facts: list[tuple[str, str, str, bool, bool]] = []
    answers: list[str] = []
    halves: list[int] = []
    for number, line in enumerate(lines):
        row = [one for one in line.split() if arabic(one)]
        for place, token in enumerate(row):
            before = ending(row[place - 1]) if place else START
            letter = final_letter(row[place - 1]) if place else START
            older = ending(row[place - 2]) if place >= 2 else START
            facts.append((before, letter, older, place == 0, place == len(row) - 1))
            answers.append(ending(token))
            halves.append(number % 2)

    whole = list(range(len(facts)))
    inner = [one for one in whole if not facts[one][4]]
    print(f"— المجال (أ) كلُّ المواضع: {len(whole)}")
    print(f"— المجال (ب) ما ليس آخرَ سطره: {len(inner)}")
    # **ولا يُسمّى «المرفوع»**: اللفظُ يلتبس بحكم بابٍ نحويّ،
    # وحارسُ المنع ردَّه — فيُسمّى بما لا يحمل حكمًا
    print(f"— الخارجُ عن (ب): {len(whole) - len(inner)}")

    every = sorted(set(answers))
    for stand, where in (("أ", whole), ("ب", inner)):
        counts = Counter(answers[one] for one in where)
        print(f"\n— خاناتُ الحال في المجال ({stand}): H = {entropy(counts):.4f}")
        for state, number in counts.most_common():
            print(f"    {shown(state)} | {number} | نصيبٌ {number / len(where):.4f}")

    slack: dict[str, float] = {}
    for stand, where in (("أ", whole), ("ب", inner)):
        seen: Counter[str] = Counter()
        worst = -float("inf")
        for index, one in enumerate(where, start=1):
            seen[answers[one]] += 1
            if index >= WITNESS:
                worst = max(worst, arrangements(seen) - index * entropy(seen))
        slack[stand] = worst
        print(f"\n— أقصى (log₂ التباديل − N·H) بعد ألف في ({stand}) = {worst:.6f}")

    walks = {
        stand: climb(facts, answers, halves, where, order, every, stand)
        for stand, where in (("أ", whole), ("ب", inner))
    }

    print("\n— المقابلةُ بتّةً بتّة: كسبٌ محجوزٌ في كلّ مقامٍ على مسنده")
    print("  البتّة | في (أ) | في (ب) | أعاشت؟")
    alive = 0
    for index, (name, _, gain_a) in enumerate(walks["أ"], start=1):
        gain_b = walks["ب"][index - 1][2]
        living = "نعم" if gain_b > 0 else "لا"
        if index > 1 and gain_b > 0:
            alive += 1
        print(f"  د{index} «{name}» | {gain_a:+.6f} | {gain_b:+.6f} | {living}")

    rest_a = math.fsum(one[2] for one in walks["أ"][1:])
    rest_b = math.fsum(one[2] for one in walks["ب"][1:])
    dead = len(walks["ب"]) - 1 - alive
    best = max(walks["ب"][1:], key=lambda one: one[2])
    print(f"\n— كسبُ «آخرُ السطر» في (ب): {walks['ب'][0][2]:+.6f}")
    print(f"— مجموعُ الإحدى عشرة في (أ): {rest_a:+.6f}")
    print(f"— مجموعُ الإحدى عشرة في (ب): {rest_b:+.6f}")
    print(f"— بتّاتٌ ماتت في (ب): {dead}")
    print(f"— أكبرُ بتّةٍ في (ب): «{best[0]}» بـ{best[2]:+.6f}")
    print(f"— أهي عن حال السابق؟ {'نعم' if best[0].startswith(NAMES[0]) else 'لا'}")
    print("— بايتاتُ الموضع المسؤولِ عنه الداخلةُ في سؤال: 0")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — شريحةٌ ونقطةُ ترميز")
    print("  ولا يُطرَح مقدارٌ من مقدارٍ عبرَ المقامين — كلُّ كسبٍ على مسنده")
    print("  وهذا يفصل الوقفَ عن غيره ولا يُثبِت أنّ غيرَه إعراب")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
