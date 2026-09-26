"""لازمُ جدول الأبواب — تشغيلُ ختم `9470c8f0…`.

**القسمةُ بالبايتات**: هيكلٌ **ثابتٌ** إن لم تُرَ له إلّا حالٌ واحدة، أو
**متبدّلٌ** إن رُئيت له أكثر — وكلاهما بخمسِ وقوعاتٍ فأكثر. **ولا يُسمّى
الثابتُ مبنيًّا ولا المتبدّلُ معربًا**: ذلك حكمُ الجدول، وهو المُتَّهَم.
"""

from __future__ import annotations

import argparse
import math
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
BARE = "·"
START = "⊢"
WITNESS = 1_000
LEAST = 5
SUKUN = "0652"
TANWEEN = ("064B", "064C", "064D")
MOVES = ("064E", "064F", "0650")


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    if one and marked(one[-1]):
        return one[-1]
    return BARE


def body(one: str) -> str:
    return one[:-1] if one and marked(one[-1]) else one


def skeleton(one: str) -> str:
    return "".join(two for two in one if not marked(two))


def shown(one: str) -> str:
    return one if one in (BARE, START) else f"{one} U+{ord(one):04X}"


def point_of(one: str) -> str:
    return BARE if one in (BARE, START) else f"{ord(one):04X}"


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
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


def attached(rows: list[tuple[str, str]]) -> float:
    blocks: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for key, state in rows:
        blocks[key][state] += 1
    total = len(rows)
    if total == 0:
        return 0.0
    return math.fsum(
        sum(one.values()) / total * entropy(one) for one in blocks.values()
    )


def kept(
    taught: list[tuple[str, str]], asked: list[tuple[str, str]], states: list[str]
) -> float:
    blocks: defaultdict[str, Counter[str]] = defaultdict(Counter)
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

    answers: list[str] = []
    halves: list[int] = []
    shapes: list[str] = []
    bones: list[str] = []
    before: list[str] = []
    for number, line in enumerate(lines):
        row = [one for one in line.split() if arabic(one)]
        for place, token in enumerate(row):
            answers.append(ending(token))
            halves.append(number % 2)
            shapes.append(body(token))
            bones.append(skeleton(token))
            before.append(ending(row[place - 1]) if place else START)

    seen: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for bone, state in zip(bones, answers):
        seen[bone][state] += 1
    steady = {
        one
        for one, states in seen.items()
        if sum(states.values()) >= LEAST and len(states) == 1
    }
    shifting = {
        one
        for one, states in seen.items()
        if sum(states.values()) >= LEAST and len(states) > 1
    }

    whole = list(range(len(answers)))
    fixed = [one for one in whole if bones[one] in steady]
    varies = [one for one in whole if bones[one] in shifting]
    outside = [
        one for one in whole if bones[one] not in steady and bones[one] not in shifting
    ]

    print(f"— الأسطر: {len(lines)}")
    print("— حدُّ اللفظ: فيه حرفٌ عربيّ (المُصحَّح من 494465d1…)")
    print(f"— الألفاظ: {len(answers)}")
    print(f"— هياكلُ متمايزة: {len(seen)} | وشرطُ القسمة: {LEAST} وقوعاتٍ فأكثر")
    print(f"— هياكلُ ثابتة: {len(steady)} | هياكلُ متبدّلة: {len(shifting)}")
    print(f"— المسندُ (ثابتة): {len(fixed)}")
    print(f"— المسندُ (متبدّلة): {len(varies)}")
    print(f"— خارجُ القسمة (دون الشرط): {len(outside)}")
    print(f"— مجموعُها: {len(fixed) + len(varies) + len(outside)}")

    every = sorted(set(answers))
    stands = (("ثابتة", fixed), ("متبدّلة", varies))

    shares: dict[str, dict[str, float]] = {}
    for label, where in stands:
        counts = Counter(answers[one] for one in where)
        shares[label] = {point_of(one): two / len(where) for one, two in counts.items()}
        print(f"\n— خاناتُ الحال على المسند ({label}): H = {entropy(counts):.4f}")
        for state, number in counts.most_common():
            print(f"    {shown(state)} | {number} | نصيبٌ {number / len(where):.4f}")

    print("")
    for label, where in stands:
        worst = -float("inf")
        running: Counter[str] = Counter()
        for index, one in enumerate(where, start=1):
            running[answers[one]] += 1
            if index >= WITNESS:
                worst = max(worst, arrangements(running) - index * entropy(running))
        print(f"— أقصى (log₂ التباديل − N·H) بعد ألفٍ في ({label}) = {worst:.6f}")

    def measure(keys: list[str], where: list[int]) -> tuple[float, float]:
        rows = [(keys[one], answers[one]) for one in where]
        here = attached(rows)
        even = [(keys[one], answers[one]) for one in where if halves[one] == 0]
        odd = [(keys[one], answers[one]) for one in where if halves[one] == 1]
        out = (kept(even, odd, every) + kept(odd, even, every)) / 2
        return here, out

    print("\n— الإنتروبيا الشرطيّةُ في كلّ مسندٍ على نفسه")
    print("  المسند | المتغيّر | ملحَقة | محجوزة")
    inside: dict[tuple[str, str], float] = {}
    outside_cost: dict[tuple[str, str], float] = {}
    nothing = [""] * len(answers)
    for label, where in stands:
        for name, keys in (
            ("لا شيء", nothing),
            ("الهيكل", bones),
            ("(ه) الصورةُ منقوصةً", shapes),
            ("(ر) حالُ السابق", before),
        ):
            here, out = measure(keys, where)
            inside[(label, name)] = here
            outside_cost[(label, name)] = out
            print(f"  {label} | {name} | {here:.6f} | {out:.6f}")

    print("\n— لوازمُ الجدول، مقيسةً")
    skeleton_fixed = inside[("ثابتة", "الهيكل")]
    print(f"— H(الحال|الهيكل) على الثابتة ملحَقةً: {skeleton_fixed:.6f}")
    for label, _ in stands:
        base = outside_cost[(label, "لا شيء")]
        near = base - outside_cost[(label, "(ر) حالُ السابق")]
        shape = base - outside_cost[(label, "(ه) الصورةُ منقوصةً")]
        print(f"— I(الحال؛ر) محجوزةً على ({label}): {near:+.6f}")
        print(f"— I(الحال؛ه) محجوزةً على ({label}): {shape:+.6f}")
        print(f"— الفرقُ (ر − ه) على ({label}): {near - shape:+.6f}")

    tanween = {
        one: math.fsum(shares[one].get(two, 0.0) for two in TANWEEN) for one in shares
    }
    moves = {
        one: math.fsum(shares[one].get(two, 0.0) for two in MOVES) for one in shares
    }
    print(
        f"\n— نصيبُ التنوين: ثابتة {tanween['ثابتة']:.6f}"
        f" | متبدّلة {tanween['متبدّلة']:.6f}"
    )
    print(f"— وفرقُه (متبدّلة − ثابتة): {tanween['متبدّلة'] - tanween['ثابتة']:+.6f}")
    quiet = {one: shares[one].get(SUKUN, 0.0) for one in shares}
    print(
        f"— نصيبُ السكون: ثابتة {quiet['ثابتة']:.6f}" f" | متبدّلة {quiet['متبدّلة']:.6f}"
    )
    print(f"— وفرقُه (ثابتة − متبدّلة): {quiet['ثابتة'] - quiet['متبدّلة']:+.6f}")
    print(f"— نصيبُ الحركات الثلاث في المتبدّلة: {moves['متبدّلة']:.6f}")
    bareness = {one: shares[one].get(BARE, 0.0) for one in shares}
    joined = bareness["ثابتة"] + quiet["ثابتة"]
    print(f"— نصيبُ («بلا علامة» + السكون) في الثابتة: {joined:.6f}")
    # **والهامشُ فوق النصف يُطبَع**: صمودٌ بهامشٍ رقيقٍ يُذكَر هامشُه،
    # وإلّا قُرِئ كصمودٍ واسعٍ وهو ليس به
    print(f"— وهامشُ الحركات الثلاث فوق النصف: {moves['متبدّلة'] - 0.5:+.6f}")
    print(f"— وهامشُ («بلا علامة» + السكون) فوق النصف: {joined - 0.5:+.6f}")
    print("— محارفُ الحال الداخلةُ في متغيّر: 0")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — شريحةٌ ونقطةُ ترميز")
    print("  والقسمةُ بالبايتات: ثابتٌ ومتبدّلٌ، لا حكمَ بابٍ يُسمّى")
    print("  وكلُّ مقدارٍ على مسنده، ولا يُطرَح عبرَ المسندين")
    print("  وسقوطُ لازمٍ سقوطُ فرضٍ مُودَعٍ لا سقوطُ لغة")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
