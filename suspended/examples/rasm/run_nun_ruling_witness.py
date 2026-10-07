"""أحكامُ النون والتنوين **مُشتَقّةً من الرسم وحدَه** — لا من طبقةِ صوت.

**الدعوى التي يُقابِلها**: فصلٌ في شجرةٍ جارةٍ حجز سبعةَ أجناسٍ صوتيّةٍ
بحجّة أنّ «الرسمَ لا يكتبها»، وفيها **الإظهارُ والإخفاءُ والقلقلة**.
وحلقةُ سجلِّهم تقول: «لا مولِّدَ في هذه الشجرة يُخرِج عددًا لواحدةٍ من
السبع». **وذلك صادقٌ عن شجرتهم، ولا يلزم منه أنّ الرسمَ لا يحملها.**

**وههنا المولِّد.** والحكمُ لا يُقرأ من حضور العلامة وحدَه، بل **من
حضورها وغيابها معًا**: في هذه المدوّنة **النونُ الموسومةُ بالسكون لا تقع
قبل حرفِ إخفاءٍ ولا إقلابٍ قطّ، والنونُ العاطلةُ لا تقع قبل حرفِ إظهارٍ
قطّ** — توزيعٌ تكامليٌّ يُطبَع ههنا بعينه فيُرى.

`EVERY_LETTER_IS_A_CODEPOINT_NEVER_TYPED`: **ولا حرفَ عربيًّا مكتوبًا
بيدٍ في هذا الملفّ**. الأصنافُ نقاطُ ترميزٍ بأرقامها، والمدوّنةُ تُشرَّح
بايتاتٍ — فلا يدخل القياسَ حرفٌ من ذاكرتي (المادّة ٩).

`AND_THE_MEASURE_IS_OF_THIS_CORPUS_NOT_OF_A_LANGUAGE`: **وحدُّه مُعلَن**:
يقيس **هذه البايتات**، لا العربيّةَ ولا القراءة. و«صفرُ وقوعٍ» ليس
«امتناعًا»: ما لم يقع ههنا قد يقع في رسمٍ آخر. ولا يقول الخرجُ إنّ
الحكمَ **مسموع** — يقول إنّه **مُشتَقٌّ من الرسم بلا زيادة**.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MARKUP = "<sel>"
NOON = 0x0646
SUKUN = 0x0652
SHADDA = 0x0651
HARAKA = frozenset({0x064E, 0x064F, 0x0650})
TANWIN = frozenset({0x064B, 0x064C, 0x064D})
MARK = HARAKA | TANWIN | {SUKUN, SHADDA}

IZHAR = frozenset(
    {
        0x0621,
        0x0622,
        0x0623,
        0x0624,
        0x0625,
        0x0626,
        0x0647,
        0x0639,
        0x062D,
        0x063A,
        0x062E,
    }
)
IDGHAM = frozenset({0x064A, 0x0631, 0x0645, 0x0644, 0x0648, 0x0646})
IQLAB = frozenset({0x0628})
IKHFA = frozenset(
    {
        0x062A,
        0x062B,
        0x062C,
        0x062F,
        0x0630,
        0x0632,
        0x0633,
        0x0634,
        0x0635,
        0x0636,
        0x0637,
        0x0638,
        0x0641,
        0x0642,
        0x0643,
    }
)
QALQALA = frozenset({0x0642, 0x0637, 0x0628, 0x062C, 0x062F})
CLASSES = (("إظهار", IZHAR), ("إدغام", IDGHAM), ("إقلاب", IQLAB), ("إخفاء", IKHFA))
REACH = 9


def letters_only(one: str) -> bool:
    return unicodedata.category(one) == "Lo"


def following_letter(text: list[str], index: int) -> int | None:
    """أوّلُ حرفٍ بعد الموضع — تُقفَز العلاماتُ والفواصلُ ولا يُتجاوَز المدى."""

    for step in range(index + 1, min(index + REACH, len(text))):
        if letters_only(text[step]):
            return ord(text[step])
    return None


def ruling_of(point: int | None) -> str:
    if point is None:
        return "لا تاليَ له"
    for name, members in CLASSES:
        if point in members:
            return name
    return f"حاملٌ لا صنفَ له U+{point:04X}"


def worn_by(text: list[str], index: int) -> str:
    """ما تحمله النونُ — والعُريُ صنفٌ مُسمًّى لا فراغٌ يُهمَل."""

    after = ord(text[index + 1]) if index + 1 < len(text) else -1
    if after == SHADDA:
        return "شدّة"
    if after == SUKUN:
        return "سكون"
    if after in HARAKA:
        return "حركة"
    if after in TANWIN:
        return "تنوين"
    return "عُري"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    text = list(given.text.read_text(encoding="utf-8").replace(MARKUP, " "))

    points = Counter(ord(one) for one in text if letters_only(one))
    print(f"— حروفُ الرسم: {sum(points.values())} | نقاطٌ متمايزة: {len(points)}")
    print(f"— النون U+{NOON:04X}: {points[NOON]}")
    print()

    print("═══ ما تحمله كلُّ نونٍ — والعُريُ صنفٌ مُسمًّى ═══")
    worn: Counter[str] = Counter()
    for index, one in enumerate(text):
        if ord(one) == NOON:
            worn[worn_by(text, index)] += 1
    for name, count in worn.most_common():
        print(f"  {name:<8} {count}")
    print()

    print("═══ التوزيعُ التكامليّ — الموسومةُ بالسكون ⟷ العاطلة ═══")
    split: dict[str, Counter[str]] = {"سكون": Counter(), "عُري": Counter()}
    for index, one in enumerate(text):
        if ord(one) != NOON:
            continue
        kind = worn_by(text, index)
        if kind in split:
            split[kind][ruling_of(following_letter(text, index))] += 1
    for kind, rows in split.items():
        shown = " · ".join(f"{a} {b}" for a, b in rows.most_common())
        print(f"  نونٌ بـ«{kind}»: {shown}")
    marked = set(split["سكون"]) & {"إخفاء", "إقلاب"}
    bare = set(split["عُري"]) & {"إظهار"}
    print(f"  تقاطعُ الموسومة مع (إخفاء·إقلاب): {len(marked)}")
    print(f"  وتقاطعُ العاطلة مع (إظهار): {len(bare)}")
    print("  **فالعلامةُ وغيابُها يقسمان الأحكامَ قسمةً لا تتداخل** إن كانا صفرين")
    print()

    print("═══ الأحكامُ الأربعةُ مجموعةً — نونًا وتنوينًا ═══")
    whole: Counter[str] = Counter()
    source: Counter[tuple[str, str]] = Counter()
    for index, one in enumerate(text):
        point = ord(one)
        if point == NOON and worn_by(text, index) in {"سكون", "عُري"}:
            trigger = "نونٌ ساكنة"
        elif point in TANWIN:
            trigger = "تنوين"
        else:
            continue
        name = ruling_of(following_letter(text, index))
        whole[name] += 1
        source[(trigger, name)] += 1
    for name, count in whole.most_common():
        print(f"  {name:<22} {count}")
    print(f"  {'المجموع':<22} {sum(whole.values())}")
    print()
    for pair, count in sorted(source.items(), key=lambda one: -one[1]):
        print(f"    {pair[0]:<12} ⟶ {pair[1]:<22} {count}")
    print()

    held = sum(
        1
        for index, one in enumerate(text)
        if ord(one) in QALQALA
        and index + 1 < len(text)
        and ord(text[index + 1]) == SUKUN
    )
    print("═══ القلقلة — دالّةٌ تامّةٌ في الرسم ═══")
    print(f"  حرفٌ من الخمسةِ يليه U+{SUKUN:04X}: {held}")
    print("  (هُويّةُ الحرفِ وعلامةُ السكون، ولا شيءَ ثالث)")
    print()

    print("═══ ما يلزم عن هذا ═══")
    print("  **أربعةٌ ممّا حُجِز مقيسٌ من الرسم وحدَه** — الإظهارُ والإخفاءُ")
    print("  والإقلابُ والقلقلة. فـ«لا مولِّدَ في شجرتنا» صادقٌ عن شجرةٍ،")
    print("  **ولا يلزم منه أنّ الرسمَ لا يحمل الحكم**.")
    print("  والحكمُ يُقرَأ من العلامة **وغيابِها**، فالغيابُ بصمةٌ إن كان")
    print("  توزيعُه تكامليًّا مشهودًا — وهو مطبوعٌ أعلاه لا مُدَّعًى.")
    print("  **وما يبقى محجوزًا بحقّ**: الإمالةُ والرومُ والإشمام، ومعها")
    print("  المقاديرُ والمراتب — فتلك لا يكتبها هذا الرسم.")
    print("  ولا يقول هذا إنّ الحكمَ **مسموع**: يقول إنّه **مُشتَقّ**.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
