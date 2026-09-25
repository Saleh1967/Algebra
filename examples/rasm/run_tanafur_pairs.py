"""قراءةٌ موازيةٌ لختم التنافر `d44f23ce…` — على المدوّنة المجمَّدة.

**الختمُ لا يُستوفى ههنا، ويُصرَّح بذلك أوّلًا**: أوراكلُه يسمّي «عمودَ
الرسم من **المحاذاة الكاملة** ببصمته وإغلاقه»، و**المحاذاةُ ليست في
الشجرة**. فهذه قراءةٌ على مدوّنةٍ أخرى مُعلَنة، بالحدود نفسِها غيرَ
مبدَّلة — ومَن بدّل المادّةَ وأبقى الاسمَ أفسد الختمَ من حيث أراد حفظَه.

**ن٥ مستوفًى بتوقيع صاحب المستودع لا بقولي**: `tools/corpus_seal.py` يحمل
`reading_name="حفص عن عاصم"` بوسمِ مصدرٍ موقَّع. فالروايةُ مُسمّاةٌ في
إيداعٍ سابق، ولا أنسب أنا متنًا إلى راوٍ.

**الوحدةُ والهامشان** (قرارُ الختم بنصّه): اللقاءُ **داخلَ الكلمة** ولا يعبر
فراغًا؛ والمتوقَّعُ من **الكلم التي تحمل الزوج فعلًا** — أي ما طولُه حرفان
فأكثرُ — لا من الحروف كلِّها. والصفريُّ **يحفظ الهامشين الموضعيّين**: تُوزَّع
مواضعُ الحرفين توزيعًا منتظمًا على المواضع المؤهَّلة، فيُحفَظ عددُ كلّ حرفٍ
وطولُ كلّ كلمة.

**وسياسةُ الطيّ تُنشَر بوجهيها** (ن٤): مطويًّا (ة→ه، ى→ي، آ→ا، والكراسي
إلى الهمزة) ومفصولًا.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path

MARKS = frozenset({0x64B, 0x64C, 0x64D, 0x64E, 0x64F, 0x650, 0x651, 0x652, 0x670})
MARKUP = "<sel>"
PAIRS: tuple[tuple[str, str], ...] = (("ق", "ك"), ("س", "ش"), ("ب", "ف"))
REPLICATES = 2_000
SEED = 20_260_924
FOLD = {"ة": "ه", "ى": "ي", "آ": "ا", "أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء"}


def letters_of(token: str, folded: bool) -> list[str]:
    """حروفُ الكلمة بلا علامات، مطويّةً أو مفصولة."""

    bare = [
        one for one in token if ord(one) not in MARKS and 0x600 <= ord(one) <= 0x6FF
    ]
    return [FOLD.get(one, one) if folded else one for one in bare]


def eligible(text: str, folded: bool) -> list[list[str]]:
    """الكلمُ التي تحمل زوجًا فعلًا — حرفان فأكثر."""

    words = (letters_of(one, folded) for one in text.replace(MARKUP, " ").split())
    return [one for one in words if len(one) >= 2]


def observed(words: list[list[str]], pair: tuple[str, str]) -> int:
    first, second = pair
    return sum(1 for one in words if first in one and second in one)


def expected(words: list[list[str]], pair: tuple[str, str]) -> float:
    first, second = pair
    total = len(words)
    carrying_first = sum(1 for one in words if first in one)
    carrying_second = sum(1 for one in words if second in one)
    return carrying_first * carrying_second / total


def null_spread(words: list[list[str]], pair: tuple[str, str]) -> list[int]:
    """صفريٌّ يحفظ عددَ كلّ حرفٍ وطولَ كلّ كلمة — الهامشان الموضعيّان."""

    owner: list[int] = []
    for index, one in enumerate(words):
        owner.extend([index] * len(one))
    counts = Counter(letter for one in words for letter in one)
    first, second = pair
    many, few = counts[first], counts[second]
    draw = random.Random(SEED)
    places = len(owner)
    spread: list[int] = []
    for _ in range(REPLICATES):
        picked = draw.sample(range(places), many + few)
        left = {owner[one] for one in picked[:many]}
        right = {owner[one] for one in picked[many:]}
        spread.append(len(left & right))
    return spread


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    text = given.text.read_text(encoding="utf-8")
    print("**الختمُ `d44f23ce…` لا يُستوفى**: أوراكلُه يسمّي المحاذاةَ، وهي غائبة.")
    print("وهذه قراءةٌ موازيةٌ على المدوّنة المجمَّدة، بالحدود نفسِها.\n")
    for folded in (True, False):
        words = eligible(text, folded)
        policy = "مطويًّا" if folded else "مفصولًا"
        print(f"— سياسةُ الطيّ: {policy} | كلمٌ مؤهَّل: {len(words)}")
        for pair in PAIRS:
            seen = observed(words, pair)
            due = expected(words, pair)
            spread = null_spread(words, pair)
            below = sum(1 for one in spread if one <= seen)
            middle = sorted(spread)[len(spread) // 2]
            print(
                f"   {pair[0]}{pair[1]}: مرصودٌ {seen} | متوقَّعٌ {due:.1f} "
                f"| نسبة {seen / due:.4f} | وسيطُ الصفريّ {middle} "
                f"| مئينٌ {below / len(spread):.4f}"
            )
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
