"""تصعيدُ صنفِ العدد بتّةً بتّة — على التوزيع المُودَع في أنبوبٍ آخر.

**لا قياسَ جديدًا ههنا**: لا تشجيرَ في هذه الشجرة. وإنّما **إعادةُ اشتقاقٍ**
من الأعداد المعروضة في `deposits/number_rule_note.md`، **وتصعيدٌ بتّةً
بتّة** على التوزيع نفسِه.
"""

from __future__ import annotations

import argparse
import itertools
import math
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\| (\S+) \| ([٠-٩]+) \| ([٠-٩]+) \|$", re.MULTILINE)
EASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
WESTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")

# مخرجُ المعدود: زوجُ (حالةٍ، عددٍ) كما تقتضيه القاعدةُ المُودَعة لكلّ صنف
EXPECTED: dict[str, str] = {
    "٣–١٠": "مجرور-جمع",
    "١١–١٩": "منصوب-مفرد",
    "عقود": "منصوب-مفرد",
    "مئة/ألف": "مجرور-مفرد",
}
ASTRAY = "مجرور-مفرد"
"""مخرجُ المخالفات الثلاث، مقروءًا من نصّ الإيداع: جموعُ تكسيرٍ وُسِمت مفردًا."""


def eastern(one: object) -> str:
    return str(one).translate(WESTERN)


def entropy(counts: list[int]) -> float:
    """`H` من عدٍّ خام؛ والصفرُ يُردّ **صفرًا لا سالبَ صفر**.

    **وعيبُ العرض ليس عيبًا صغيرًا**: `-0.0000` يُقرَأ سالبًا وهو صفر،
    وذاك «صدقٌ يُقرَأ كذبًا» — وهو العطلُ الثامنَ عشر بعينه.
    """

    total = sum(counts)
    if total == 0:
        return 0.0
    found = -math.fsum((one / total) * math.log2(one / total) for one in counts if one)
    return 0.0 if found == 0.0 else found


def wilson(hits: int, tries: int) -> tuple[float, float]:
    """مجالُ ويلسن ٩٥٪ — يُشتَقّ ولا يُنقَل."""

    if tries == 0:
        return 0.0, 1.0
    z = 1.959963984540054
    share = hits / tries
    middle = share + z * z / (2 * tries)
    spread = z * math.sqrt(share * (1 - share) / tries + z * z / (4 * tries * tries))
    weight = 1 + z * z / tries
    return (middle - spread) / weight, (middle + spread) / weight


def read_table(deposit: Path) -> list[tuple[str, int, int]]:
    """(الصنف، المواضع، المطابق) من جدول الإيداع — بنمطٍ لا كتابةً."""

    found = ROW.findall(deposit.read_text(encoding="utf-8"))
    return [
        (one, int(two.translate(EASTERN)), int(three.translate(EASTERN)))
        for one, two, three in found
    ]


def outcomes(rows: list[tuple[str, int, int]]) -> dict[str, dict[str, int]]:
    """الصنفُ ⟶ توزيعُ مخرج المعدود؛ والمخالفُ يأخذ مخرجَ المخالفات."""

    out: dict[str, dict[str, int]] = {}
    for name, places, right in rows:
        table: dict[str, int] = {}
        table[EXPECTED[name]] = table.get(EXPECTED[name], 0) + right
        if places - right:
            table[ASTRAY] = table.get(ASTRAY, 0) + (places - right)
        out[name] = table
    return out


def blocked(table: dict[str, dict[str, int]], groups: list[frozenset[str]]) -> float:
    """H(المخرج | الكتلة) على قسمةٍ معطاة."""

    whole = sum(sum(one.values()) for one in table.values())
    total = 0.0
    for group in groups:
        merged: dict[str, int] = {}
        for name in group:
            for key, count in table[name].items():
                merged[key] = merged.get(key, 0) + count
        size = sum(merged.values())
        if size:
            total += size / whole * entropy(list(merged.values()))
    return total


def refine(groups: list[frozenset[str]], asked: frozenset[str]) -> list[frozenset[str]]:
    out: list[frozenset[str]] = []
    for group in groups:
        yes, no = group & asked, group - asked
        out.extend(one for one in (yes, no) if one)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule", type=Path, required=True)
    given = parser.parse_args()

    rows = read_table(given.rule)
    if len(rows) != 4:
        raise SystemExit(f"جدولُ الإيداع أربعةُ صفوفٍ لا {len(rows)}")
    places = sum(one for _, one, _ in rows)
    right = sum(one for _, _, one in rows)
    print("— لا قياسَ جديدًا: إعادةُ اشتقاقٍ من أعدادٍ معروضةٍ في أنبوبٍ آخر")
    print(f"— المواضعُ ذاتُ الحافّة: {places} | المطابقُ للقاعدة: {right}")
    for name, count, hit in rows:
        print(
            f"    {name:8s} مواضعُ {count:2d} | مطابقٌ {hit:2d}"
            f" | H = {entropy([hit, count - hit]):.4f}"
        )

    table = outcomes(rows)
    whole: dict[str, int] = {}
    for one in table.values():
        for key, count in one.items():
            whole[key] = whole.get(key, 0) + count
    print(f"\n— مخرجاتُ المعدود المُشتَقّة: {len(whole)}")
    for key in sorted(whole, key=lambda one: -whole[one]):
        print(f"    {key:12s} {whole[key]:2d} | نصيبٌ {whole[key] / places:.6f}")
    flat = entropy(list(whole.values()))
    full = blocked(table, [frozenset({one}) for one, _, _ in rows])
    print(f"  H(المعدود) بلا شرط = {flat:.4f}")
    print(f"  H(المعدود | صنفِ العدد) = {full:.4f}")
    print(f"  الكسب = {flat - full:+.4f} = {(flat - full) / flat:.4%} من الحيرة")

    names = [one for one, _, _ in rows]
    print("\n— induction ON: تعدادٌ تامٌّ، والمبرهنةُ مُصانةٌ عند كلّ قسمة")
    worst = 0.0
    for size in range(1, len(names)):
        for chosen in itertools.combinations(names, size):
            asked = frozenset(chosen)
            here = blocked(table, refine([frozenset(names)], asked))
            worst = max(worst, here - flat)
    print(f"  أقصى (H مشروطةً − H بلا شرط) على كلّ قسمةٍ ثنائيّة: {worst:+.6f}")
    print("  والشرطُ لا يرفع الإنتروبيا — مبرهنةٌ، وقد صِينت في القسمات كلِّها")

    print("\n— التصعيدُ بتّةً بتّة: سؤالٌ ثنائيٌّ واحدٌ في كلّ درجة")
    groups = [frozenset(names)]
    here = flat
    print(f"  د٠ بلا سؤال: H = {here:.6f} | كتلةٌ 1")
    asked_before: list[frozenset[str]] = []
    for depth in range(1, len(names)):
        best: tuple[float, frozenset[str]] | None = None
        for size in range(1, len(names)):
            for chosen in itertools.combinations(names, size):
                asked = frozenset(chosen)
                if asked in asked_before or frozenset(names) - asked in asked_before:
                    continue
                after = blocked(table, refine(groups, asked))
                if best is None or here - after > best[0]:
                    best = (here - after, asked)
        if best is None or best[0] <= 1e-12:
            print(f"  الوقوف: لا سؤالَ يربح عند الدرجة {depth}")
            break
        gain, asked = best
        groups = refine(groups, asked)
        asked_before.append(asked)
        here -= gain
        shown = " و".join(sorted(asked))
        print(
            f"  د{depth} «أمن {shown}؟»: H = {here:.6f}"
            f" | ربحٌ {gain:+.6f} | كتلٌ {len(groups)}"
        )
    print(f"  بلغ التصعيدُ الشرطَ التامَّ: {abs(here - full) < 1e-12}")
    print(
        f"  عددُ البتّات المصروفة: {len(asked_before)}"
        f" | والسقفُ الخام ⌈log₂{len(names)}⌉ = {(len(names) - 1).bit_length()}"
    )

    print("\n— induction FOR: ما أعلنه الأنبوبُ عن المحجوز")
    for hits, tries, label in ((12, 15, "القاعدة"), (8, 15, "الأغلبُ الأعمى")):
        low, high = wilson(hits, tries)
        print(
            f"    {label:14s} {hits}/{tries} = {hits / tries:.4%}"
            f" | ويلسن ٩٥٪ [{low:.4%} , {high:.4%}]"
        )
    low_rule, high_rule = wilson(12, 15)
    low_blind, high_blind = wilson(8, 15)
    print(f"  أيتداخل المجالان؟ {low_rule <= high_blind}")
    print("  فالعيّنةُ أصغرُ من أن تحمل دعوى تنبّؤ — وهو إعلانُ الأنبوب نفسِه")

    print("\n— ما لا يُدَّعى")
    print("  لا تشجيرَ في هذه الشجرة: لا يُعاد القياسُ، ويُعاد الحسابُ وحدَه")
    print("  ولا تُوقَّع القاعدةُ المنقولة ولا تعليلُ المخالفات الثلاث")
    print(f"  والمقامُ {places} موضعًا: تعدادٌ تامٌّ عليه، لا حكمٌ على العربيّة")
    print(f"  ومخرجاتُ المعدود قراءةٌ لي تُعيد {flat:.4f} بلا بقيّة — لا نصُّ الأنبوب")
    return 0


if __name__ == "__main__":
    sys.exit(main())
