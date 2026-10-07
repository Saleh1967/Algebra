"""ما تحدّده صورةُ اللفظ، وما يزيده جارُه بعدها — تشغيلُ ختم `0410f435…`.

**لا اسمَ يدخل السجلّ**: المحرفُ شريحةٌ ونقطةُ ترميز، والمتغيّراتُ
شرائحُ من المجمَّد، **والحكمُ على المحجوز والملحَقُ مُسمًّى منتفخًا**.
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
LENGTHENING = ("0627", "0648", "064A")


def ladder_gain() -> float:
    """كسبُ السلّم محجوزًا — **مقروءٌ من سجلّه لا مكتوبٌ بيد**."""

    found = re.search(
        r"مجموعُ الكسب المحجوز: \+([0-9.]+)", LADDER.read_text(encoding="utf-8")
    )
    if found is None:
        raise SystemExit("لا شاهدَ في سجلّ السلّم لمجموع الكسب المحجوز")
    return float(found.group(1))


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    if one and marked(one[-1]):
        return one[-1]
    return BARE


def body(one: str) -> str:
    """(ه) اللفظُ منقوصًا آخرَ محرفٍ إن كان علامة — ولا يحمل المحذوف."""

    return one[:-1] if one and marked(one[-1]) else one


def skeleton(one: str) -> str:
    """(ج) اللفظُ مجرَّدًا من كلّ علامة — تكتيلٌ لـ(ه) بحكم البناء."""

    return "".join(two for two in one if not marked(two))


def final_letter(one: str) -> str:
    for two in reversed(one):
        if not marked(two):
            return two
    return BARE


def shown(one: str) -> str:
    return one if one in (BARE, START) else f"{one} U+{ord(one):04X}"


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


def attached(rows: list[tuple[str, str]]) -> float:
    """H(الحال | المتغيّر) على العيّنة نفسِها — **منتفخٌ بسَعة الفضاء**."""

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
    tails: Counter[str] = Counter()
    for number, line in enumerate(lines):
        row = [one for one in line.split() if arabic(one)]
        for place, token in enumerate(row):
            answers.append(ending(token))
            halves.append(number % 2)
            shapes.append(body(token))
            bones.append(skeleton(token))
            before.append(ending(row[place - 1]) if place else START)
            if ending(token) == BARE:
                tails[final_letter(token)] += 1

    print(f"— الأسطر: {len(lines)}")
    print("— حدُّ اللفظ: فيه حرفٌ عربيّ (المُصحَّح من 494465d1…)")
    print(f"— الألفاظ: {len(answers)} | والمسندُ واحدٌ في كلّ مقدار")
    states: Counter[str] = Counter(answers)
    print(f"— خاناتُ الحال: {len(states)} | H = {entropy(states):.4f}")
    print(f"— صورُ (ه) منقوصةَ العلامة: {len(set(shapes))}")
    print(f"— صورُ (ج) مجرَّدةً: {len(set(bones))}")
    print(f"— قيمُ (ر) حالِ السابق: {len(set(before))}")

    seen: Counter[str] = Counter()
    worst = -float("inf")
    for index, state in enumerate(answers, start=1):
        seen[state] += 1
        if index >= WITNESS:
            worst = max(worst, arrangements(seen) - index * entropy(seen))
    print(f"— أقصى (log₂ التباديل − N·H) بعد ألف = {worst:.6f}")

    every = sorted(states)
    even = [one for one in range(len(answers)) if halves[one] == 0]
    odd = [one for one in range(len(answers)) if halves[one] == 1]

    def measure(keys: list[str]) -> tuple[float, float]:
        rows = list(zip(keys, answers))
        here = attached(rows)
        pick = [rows[one] for one in even]
        rest = [rows[one] for one in odd]
        out = (kept(pick, rest, every) + kept(rest, pick, every)) / 2
        return here, out

    nothing = [""] * len(answers)
    together = [f"{one}\x1f{two}" for one, two in zip(shapes, before)]
    field = {
        "لا شيء": nothing,
        "(ه) الصورةُ منقوصةً": shapes,
        "(ج) الهيكلُ مجرَّدًا": bones,
        "(ر) حالُ السابق": before,
        "(ه، ر) معًا": together,
    }
    inside: dict[str, float] = {}
    outside: dict[str, float] = {}
    print("\n— الإنتروبيا الشرطيّةُ لكلّ متغيّر — والمسندُ واحد")
    print("  المتغيّر | قيمُه | ملحَقةٌ (منتفخة) | محجوزة")
    for name, keys in field.items():
        here, out = measure(keys)
        inside[name] = here
        outside[name] = out
        print(f"  {name} | {len(set(keys))} | {here:.6f} | {out:.6f}")

    base_in = inside["لا شيء"]
    base_out = outside["لا شيء"]
    print("\n— المعلوماتُ المتبادلة = ناقصُ الشرطيّة عن المجرّدة")
    print("  المتغيّر | ملحَقةٌ (منتفخة) | محجوزة")
    for name in field:
        if name == "لا شيء":
            continue
        print(
            f"  {name} | {base_in - inside[name]:+.6f}"
            f" | {base_out - outside[name]:+.6f}"
        )

    shape_out = base_out - outside["(ه) الصورةُ منقوصةً"]
    bone_out = base_out - outside["(ج) الهيكلُ مجرَّدًا"]
    near_out = base_out - outside["(ر) حالُ السابق"]
    both_out = base_out - outside["(ه، ر) معًا"]
    added = both_out - shape_out
    print(f"\n— I(الحال؛ه) محجوزةً: {shape_out:+.6f}")
    print(f"— I(الحال؛ج) محجوزةً: {bone_out:+.6f}")
    print(f"— I(الحال؛ر) محجوزةً: {near_out:+.6f}")
    print(f"— I(الحال؛ه) − I(الحال؛ر) محجوزتين: {shape_out - near_out:+.6f}")
    print(f"— I(الحال؛ر | ه) محجوزةً: {added:+.6f}")
    share = added / near_out if near_out else 0.0
    print(f"— وما بقي للجار بعد الصورة نسبةً إلى وحده: {share:.6f}")
    ladder = ladder_gain()
    print(f"— وكسبُ السلّم كلِّه محجوزًا (مقروءًا من سجلّه): +{ladder:.6f}")
    print(f"— أتفوق الصورةُ السلّمَ؟ {'نعم' if shape_out > ladder else 'لا'}")
    print(f"— نصيبُ (ه) من الحقل محجوزًا: {shape_out / base_in:.4f}")
    print(f"— نصيبُ (ج) من الحقل محجوزًا: {bone_out / base_in:.4f}")
    print(f"— نصيبُ (ر) من الحقل محجوزًا: {near_out / base_in:.4f}")
    # **الحدُّ الأعلى** لِما يزيده الجارُ بعد الصورة: ملحَقٌ منتفخٌ
    # مُسمًّى قبل النظر، ويُعرَض لأنّ المحجوزَ سالبٌ بعقاب السَّعة
    ceiling = inside["(ه) الصورةُ منقوصةً"] - inside["(ه، ر) معًا"]
    print(f"— وسقفُ ما يزيده الجارُ بعد الصورة ملحَقًا: +{ceiling:.6f}")
    print(f"— ونصيبُ السقفِ من الحقل: {ceiling / base_in:.4f}")
    print("— محارفُ العلامة الأخيرة الداخلةُ في متغيّر: 0")

    print(f"\n— تشقيقُ خانة «{BARE}» بحرف خاتمتها — بايتاتٌ لا تفسير")
    whole = sum(tails.values())
    print(f"— ألفاظُ الخانة: {whole} | نصيبُها من الكلّ {whole / len(answers):.4f}")
    for letter, number in tails.most_common(8):
        print(f"    {shown(letter)} | {number} | نصيبٌ {number / whole:.4f}")
    stretch = sum(
        number
        for letter, number in tails.items()
        if letter != BARE and f"{ord(letter):04X}" in LENGTHENING
    )
    print(f"— أقسامُها: {len(tails)}")
    print(f"— نصيبُ حروف المدّ الثلاثة منها: {stretch / whole:.6f}")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — شريحةٌ ونقطةُ ترميز")
    print("  والملحَقةُ منتفخةٌ بسَعة الفضاء، والحكمُ على المحجوز وحدَه")
    print("  وهذا يقيس سقفَ القراءة التركيبيّة ولا يُسمّي بابًا ولا حكمًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
