"""دورةُ الحال على الخاتمة — تشغيلُ ختم `7773c03f…`.

**ما يُقاس**: حالُ الخاتمة على كلّ لفظ؛ وثباتُه وتبدّلُه على الهياكل؛
وخلوُّ خانته عند حروفٍ بعينها؛ ونصيبُ الثلاث ممّا سواها؛ وسلسلةُ ماركوف
داخلَ السطر بحدّيها المبرهَنين.

**ولا اسمَ بابٍ نحويٍّ يدخل**: علاماتٌ ومواضعُ وبتّات.
"""

from __future__ import annotations

import argparse
import math
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
LEAST = 5
BASMALA = "بسم"
THREE = ("َ", "ُ", "ِ")
BARE = "بلا علامة"


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def skeleton(one: str) -> str:
    return "".join(two for two in one if not marked(two))


def ending(one: str) -> str:
    """حالُ الخاتمة: آخرُ محرفٍ إن كان علامةً، وإلّا «بلا علامة»."""

    if one and marked(one[-1]):
        return one[-1]
    return BARE


def final_letter(one: str) -> str:
    for two in reversed(one):
        if not marked(two):
            return two
    return ""


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -math.fsum(
        (one / total) * math.log2(one / total) for one in counts.values() if one
    )


def arrangements(counts: Counter[str]) -> float:
    """log₂ عددِ التباديل المتمايزة — `log₂ N! − Σ log₂ nᵢ!`."""

    total = sum(counts.values())
    if total == 0:
        return 0.0
    return (
        math.lgamma(total + 1)
        - math.fsum(math.lgamma(one + 1) for one in counts.values())
    ) / math.log(2)


def conditional(pairs: Counter[tuple[str, str]]) -> tuple[float, float]:
    """(H(التالي)، H(التالي | السابق)) — بالهامش **الأيمن**."""

    total = sum(pairs.values())
    if total == 0:
        return 0.0, 0.0
    right: Counter[str] = Counter()
    left: Counter[str] = Counter()
    for (before, after), number in pairs.items():
        right[after] += number
        left[before] += number
    after_entropy = entropy(right)
    held = 0.0
    for (before, after), number in pairs.items():
        joint = number / total
        held -= joint * math.log2(number / left[before])
    return after_entropy, held


def mutual(pairs: Counter[tuple[str, str]]) -> float:
    after_entropy, held = conditional(pairs)
    return after_entropy - held


def smoothed(
    pairs: Counter[tuple[str, str]], states: list[str]
) -> Counter[tuple[str, str]]:
    """تنعيمُ لابلاس على الجداء الكامل — فلا خانةَ صفرٌ تُبطِل القسمة."""

    out: Counter[tuple[str, str]] = Counter()
    for before in states:
        for after in states:
            out[(before, after)] = pairs.get((before, after), 0) + 1
    return out


def crossed(pairs: Counter[tuple[str, str]], held: Counter[tuple[str, str]]) -> float:
    """I المقيسةُ على `held` بتقديرٍ من `pairs` — الانتحالُ يُقاس لا يُفترَض."""

    states = sorted(
        {one for one, _ in pairs}
        | {two for _, two in pairs}
        | {one for one, _ in held}
        | {two for _, two in held}
    )
    model = smoothed(pairs, states)
    total = sum(model.values())
    left: Counter[str] = Counter()
    right: Counter[str] = Counter()
    for (before, after), number in model.items():
        left[before] += number
        right[after] += number
    seen = sum(held.values())
    if seen == 0:
        return 0.0
    out = 0.0
    for (before, after), number in held.items():
        joint = model[(before, after)] / total
        apart = (left[before] / total) * (right[after] / total)
        out += (number / seen) * math.log2(joint / apart)
    return out


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

    tokens_by_line = [one.split() for one in lines]
    by_line = sum(len(one) for one in tokens_by_line)

    states: Counter[str] = Counter()
    letters: Counter[str] = Counter()
    joint_letter: Counter[tuple[str, str]] = Counter()
    per_skeleton: defaultdict[str, Counter[str]] = defaultdict(Counter)
    pairs: Counter[tuple[str, str]] = Counter()
    even_pairs: Counter[tuple[str, str]] = Counter()
    odd_pairs: Counter[tuple[str, str]] = Counter()
    even_skeleton: defaultdict[str, Counter[str]] = defaultdict(Counter)
    odd_skeleton: defaultdict[str, Counter[str]] = defaultdict(Counter)
    basmala = 0
    basmala_first = 0
    markup = 0
    markup_forms: Counter[str] = Counter()
    basmala_where: list[tuple[int, int, str]] = []

    least_gap = float("inf")
    most_slack = -float("inf")
    settled_gap = float("inf")
    settled_slack = -float("inf")
    counted = 0

    for number, tokens in enumerate(tokens_by_line):
        for position, token in enumerate(tokens):
            bones = skeleton(token)
            state = ending(token)
            states[state] += 1
            letters[final_letter(token)] += 1
            joint_letter[(final_letter(token), state)] += 1
            per_skeleton[bones][state] += 1
            (even_skeleton if number % 2 == 0 else odd_skeleton)[bones][state] += 1
            if bones == BASMALA:
                basmala += 1
                if position == 0:
                    basmala_first += 1
                else:
                    basmala_where.append((number + 1, position, token))
            if not any("ARABIC" in unicodedata.name(two, "") for two in token):
                markup += 1
                markup_forms[token] += 1
            counted += 1
            if position:
                before = ending(tokens[position - 1])
                pairs[(before, state)] += 1
                (even_pairs if number % 2 == 0 else odd_pairs)[(before, state)] += 1
        after_entropy, held = conditional(pairs)
        gap = after_entropy - held
        slack = arrangements(states) - counted * entropy(states)
        least_gap = min(least_gap, gap)
        most_slack = max(most_slack, slack)
        if counted >= 1_000:
            settled_gap = min(settled_gap, gap)
            settled_slack = max(settled_slack, slack)

    print(f"— الألفاظ: عبرَ العدّادات {counted} | عبرَ الأسطر {by_line}")
    print(f"  |فرقٌ| = {abs(counted - by_line)}")
    print(f"  بسم = {basmala} | منها في صدر السطر {basmala_first}")
    for line_number, place, token in basmala_where:
        print(f"    سطرُ {line_number} | موضعُ {place} | {token}")
    print(f"  ألفاظُ الترقيم (لا حرفَ عربيًّا فيها): {markup}")
    for one, number in sorted(markup_forms.items()):
        print(f"    {one} | وقوعاتٌ {number}")
    print(f"  هياكلُ متمايزة: {len(per_skeleton)}")

    print("\n— حالُ الخاتمة")
    for state, number in states.most_common():
        name = unicodedata.name(state, "بلا علامة") if state != BARE else BARE
        print(
            f"    {state if state != BARE else '·'} ({name}) {number}"
            f" | نصيبٌ {number / counted:.4f}"
        )
    three = sum(states[one] for one in THREE)
    print(f"  نصيبُ الثلاث: {three} من {counted} = {three / counted:.4f}")
    print(f"  H(الحال) = {entropy(states):.4f}")

    print("\n— induction on: الشرطُ لا يرفع الإنتروبيا، والتباديلُ دون N·H")
    print(f"  أدنى (H(التالي) − H(التالي|السابق)) = {least_gap:+.17e}")
    print(f"  أقصى (log₂ التباديل − N·H) = {most_slack:+.17e}")
    print("  والطرفان يقعان عند أوّل الحلقة حيث الحدُّ واحدٌ — فيُعادان " "بعد ألفِ لفظ:")
    print(f"    أدنى فرقٍ بعد ألف = {settled_gap:+.6f}")
    print(f"    أقصى فسحةٍ بعد ألف = {settled_slack:+.6f}")
    print(
        f"    وعند الختام: فرقٌ {after_entropy - held:+.6f} | فسحةٌ "
        f"{arrangements(states) - counted * entropy(states):+.6f}"
    )

    after_entropy, held = conditional(pairs)
    print("\n— ماركوف داخلَ السطر")
    print(f"  أزواجٌ {sum(pairs.values())}")
    print(f"  H(التالي) {after_entropy:.4f} | H(التالي|السابق) {held:.4f}")
    print(f"  I = {mutual(pairs):.4f}")

    inside = crossed(even_pairs, even_pairs)
    outside = crossed(even_pairs, odd_pairs)
    print(
        f"  ملحَقة {inside:.4f} | محجوزة {outside:.4f}" f" | فرقٌ {outside - inside:+.4f}"
    )

    letter_joint = mutual(joint_letter)
    print(f"\n— I(الحال؛ حرفُ الخاتمة) = {letter_joint:.4f}")
    print(f"  حروفُ خاتمةٍ متمايزة: {len(letters)}")

    borne: defaultdict[str, set[str]] = defaultdict(set)
    for (letter, state), seen in joint_letter.items():
        if seen:
            borne[letter].add(state)
    blind = sorted(
        one
        for one, number in letters.items()
        if number >= LEAST and borne[one] == {BARE}
    )
    print(f"  حروفٌ (٥ وقوعاتٍ فأكثر) لا تحمل حالًا ألبتّة: {len(blind)}")
    for one in blind:
        print(f"    {one} | وقوعاتٌ {letters[one]}")

    steady = [
        one
        for one, seen in per_skeleton.items()
        if sum(seen.values()) >= LEAST and len(seen) == 1
    ]
    moving = [
        one
        for one, seen in per_skeleton.items()
        if sum(seen.values()) >= LEAST and len(seen) > 1
    ]
    enough = len(steady) + len(moving)
    steady_mass = sum(sum(per_skeleton[one].values()) for one in steady)
    moving_mass = sum(sum(per_skeleton[one].values()) for one in moving)
    print(f"\n— ثباتُ الحال (بقيد {LEAST} وقوعاتٍ فأكثر)")
    print(f"  هياكلُ بالقيد: {enough} | ثابتةٌ {len(steady)} | متبدّلةٌ {len(moving)}")
    print(f"  نصيبُ الثابت من الهياكل: {len(steady) / enough:.4f}")
    print(f"  كتلةُ الثابت {steady_mass} | كتلةُ المتبدّل {moving_mass}")
    print(f"  نصيبُ كتلة الثابت من الألفاظ: {steady_mass / counted:.4f}")

    even_steady = {
        one
        for one, seen in even_skeleton.items()
        if sum(seen.values()) >= LEAST and len(seen) == 1
    }
    both = {
        one
        for one in even_steady
        if len(odd_skeleton[one]) == 1
        and next(iter(odd_skeleton[one])) == next(iter(even_skeleton[one]))
    }
    carried = len(both) / len(even_steady) if even_steady else 0.0
    print(
        f"  ثابتُ الزوجيّ {len(even_steady)} | باقٍ ثابتًا في الفرديّ {len(both)}"
        f" | نصيبٌ {carried:.4f}"
    )

    print("\n— ما لا يُشتَقّ")
    print("  الأصليّةُ والفرعيّة: لا جدولَ أبوابٍ مُودَعٌ — خلوٌّ مُصنَّفٌ " "«فحصُها مُعيَّنٌ ولم يُجرَ»")
    print("  المبنيُّ والمعرب: المقيسُ ثباتُ علامةٍ لا حكمُ باب — " "قابليّةٌ للقراءة لا قراءة")
    return 0


if __name__ == "__main__":
    sys.exit(main())
