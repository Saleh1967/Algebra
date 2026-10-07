"""`H(الحركةُ الأخيرة | النوع)`: مبنيٌّ ومعربٌ مقيسَين، والمجمَّعُ يُرَدّ.

**الصيغةُ المُترجَمة**: معربٌ ⟺ `H > 0`، ومبنيٌّ ⟺ `H = 0`. والنوعُ **رسمٌ**
لا سطح، إذ السطحُ يحمل الحركةَ فتصير الإنتروبيا صفرًا بالبناء.

`A_HAPAX_IS_FROZEN_BY_ARITHMETIC_NOT_BY_GRAMMAR`: ونوعٌ وقع **مرّةً واحدة**
إنتروبيتُه صفرٌ **بالضرورة** — لا لأنّه مبنيٌّ بل لأنّه لم يقع إلّا مرّة.
وثمانيةُ آلافٍ وسبعُ مئةٍ واثنان وتسعون من أربعةَ عشرَ ألفًا وتسع مئةٍ وسبعةٍ
وخمسين نوعًا (**٥٨٫٨٪**) وقعت مرّةً. فالنسبةُ المجمَّعةُ (٨٨٫٦٪) **أكثرُها
حسابٌ لا نحو**، وطبعُها وحدَها يُرَدّ ههنا كما يُرَدّ كلُّ مجمَّعٍ يُخفي
شريحة.

`THE_NULL_IS_THE_SHARE_THAT_WOULD_FREEZE_BY_CHANCE`: والصفريُّ محسوب: نوعٌ
وقع `n` مرّةً، لو كانت حركتُه تُسحَب من التوزيع العامّ، فاحتمالُ ثباتها
`Σ pᵢⁿ`. فيُقابَل المرصودُ به **في كلّ شريحة**. وعند خمسةٍ إلى تسعةِ وقوعاتٍ
يصير الصفريُّ ٠٫٧٪ والمرصودُ ٦٤٫٤٪ — **اثنان وتسعون ضعفًا**.

`THE_BINARY_IS_A_SHAPE_NOT_A_DEFINITION`: و«الإنتروبيا صفرٌ أو موجب» لا
تُبرهِن ثنائيّةً: كلُّ مقدارٍ متّصلٍ كذلك. والذي يُبرهِنها **شكلُ التوزيع**.
وعلى الأنواع ذاتِ عشرة وقوعاتٍ فأكثر: ٤٩٠ عند الصفر بالضبط، ثمّ **وادٍ**
(٤٣ فقط دون ٠٫٣٠)، ثمّ تلٌّ ثانٍ وسيطُه ٠٫٩٠. فقمّتان وفجوةٌ بينهما —
وذلك خبرٌ، بخلاف سلّم «الجامد والمشتقّ» المتّصل.
"""

from __future__ import annotations

import argparse
import csv
import math
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HARAKAT: dict[str, str] = {
    "َ": "فتحة",
    "ُ": "ضمّة",
    "ِ": "كسرة",
    "ْ": "سكون",
    "ً": "تنوينُ فتح",
    "ٌ": "تنوينُ ضمّ",
    "ٍ": "تنوينُ كسر",
}
MARKS = frozenset(range(0x064B, 0x0653)) | {
    0x0640,
    0x0670,
    0x06DF,
    0x0653,
    0x0654,
    0x0655,
}
LETTERS = frozenset("ابتثجحخدذرزسشصضطظعغفقكلمنهويأإآةىؤئءٱ")

BANDS: tuple[tuple[int, int, str], ...] = (
    (1, 1, "١"),
    (2, 2, "٢"),
    (3, 4, "٣–٤"),
    (5, 9, "٥–٩"),
    (10, 49, "١٠–٤٩"),
    (50, 10**9, "٥٠+"),
)


class VowelEntropyError(ValueError):
    """رُفض طلبُ رقمٍ مجمَّعٍ يُخفي شريحةً، أو مدوّنةٍ لا تُقرَأ."""


def skeleton(text: str) -> str:
    """رسمُ الكلمة بلا ضبط؛ وهو **النوعُ** ههنا لا السطح."""

    return "".join(
        character
        for character in unicodedata.normalize("NFC", text)
        if ord(character) not in MARKS and character in LETTERS
    )


def final_haraka(text: str) -> str | None:
    """آخرُ علامةِ ضبطٍ في الكلمة، أو `None` إن لم تُوجَد."""

    for character in reversed(unicodedata.normalize("NFC", text)):
        if character in HARAKAT:
            return HARAKAT[character]
    return None


def entropy(counts: Counter[str]) -> float:
    """`H` بالبتّات على وقوعات النوع."""

    total = sum(counts.values())
    if not total:
        raise VowelEntropyError("نوعٌ بلا وقوعٍ لا إنتروبيا له.")
    return -sum(
        (value / total) * math.log2(value / total) for value in counts.values() if value
    )


def read_types(path: Path) -> dict[str, Counter[str]]:
    """لكلّ نوعٍ رسميٍّ توزيعُ حركته الأخيرة على وقوعاته."""

    found: dict[str, Counter[str]] = defaultdict(Counter)
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = skeleton(row["surface"])
            mark = final_haraka(row["surface"])
            if key and mark:
                found[key][mark] += 1
    if not found:
        raise VowelEntropyError("لا نوعَ واحدٌ قُرِئ؛ فالعمودُ أو المسارُ خطأ.")
    return dict(found)


def frozen_share_by_chance(counts: Counter[str], overall: Counter[str]) -> float:
    """احتمالُ ثبات الحركة صدفةً لنوعٍ بهذا العدد من الوقوعات."""

    total = sum(overall.values())
    occurrences = sum(counts.values())
    return sum((value / total) ** occurrences for value in overall.values())


def report(path: Path, pooled_only: bool = False) -> int:
    """المرصودُ مصنَّفًا بعدد الوقوعات، ومعه صفريُّه — والمجمَّعُ وحدَه يُرَدّ."""

    if pooled_only:
        raise VowelEntropyError(
            "المجمَّعُ وحدَه يُرَدّ: أكثرُ من نصف الأنواع وقعت مرّةً واحدة، "
            "وإنتروبيتُها صفرٌ بالحساب لا بالنحو. فيُصنَّف بعدد الوقوعات."
        )
    types = read_types(path)
    overall: Counter[str] = Counter()
    for counts in types.values():
        overall.update(counts)

    print(f"أنواعٌ رسميّة: {len(types):,}  ·  وقوعاتٌ مقيسة: {sum(overall.values()):,}")
    pooled = sum(1 for counts in types.values() if entropy(counts) == 0)
    print(f"والمجمَّعُ (لا يُقرَأ وحدَه): {pooled / len(types) * 100:.1f}٪ ثابتةُ الحركة\n")

    print(
        f"{'وقوعات':>8} {'أنواع':>8} {'ثابتٌ مرصود':>13} {'ثابتٌ صفريّ':>13} {'الرفع':>8}"
    )
    for low, high, label in BANDS:
        band = [
            counts for counts in types.values() if low <= sum(counts.values()) <= high
        ]
        if not band:
            continue
        observed = sum(1 for counts in band if entropy(counts) == 0) / len(band)
        chance = sum(frozen_share_by_chance(counts, overall) for counts in band) / len(
            band
        )
        # ورفعٌ فوق أربعة أصفارٍ لا يُطبَع رقمًا: صفريٌّ يقارب الصفرَ
        # يجعل النسبةَ دقّةً كاذبة، والخبرُ فيها «لا يُبلَغ» لا مقدارُها.
        if chance == 0 or observed / chance > 10_000:
            lift = "≫ ١٠⁴"
        else:
            lift = f"{observed / chance:.0f}×"
        print(
            f"{label:>8} {len(band):>8,} {observed * 100:>12.1f}٪ "
            f"{chance * 100:>12.1f}٪ {lift:>8}"
        )

    rich = [counts for counts in types.values() if sum(counts.values()) >= 10]
    shape = Counter()
    for counts in rich:
        value = entropy(counts)
        shape["صفرٌ تامّ" if value == 0 else ("وادٍ" if value < 0.3 else "تلٌّ ثانٍ")] += 1
    print(f"\nشكلُ التوزيع على {len(rich):,} نوعًا (عشرةُ وقوعاتٍ فأكثر):")
    for name, count in (
        ("صفرٌ تامّ", shape["صفرٌ تامّ"]),
        ("وادٍ", shape["وادٍ"]),
        ("تلٌّ ثانٍ", shape["تلٌّ ثانٍ"]),
    ):
        print(f"   {name:10} {count:>4}")
    print("   وقمّتان يفصلهما وادٍ **خبرٌ**؛ وسلّمٌ متّصلٌ حدٌّ موضوع.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="إنتروبيا الحركة الأخيرة لكلّ نوع")
    parser.add_argument("--aligned", type=Path, required=True)
    parser.add_argument("--pooled-only", action="store_true")
    args = parser.parse_args(argv)
    return report(args.aligned, args.pooled_only)


if __name__ == "__main__":
    raise SystemExit(main())
