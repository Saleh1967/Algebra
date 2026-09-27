"""أثرُ العامل على الوحدة الأخيرة — تشغيلُ ختم `89cba549…`.

**ولا اسمَ بابٍ في هذا السجلّ**: المقيسُ **متتاليةُ نقاطٍ**
`0625 0650 0646 0651 064E`، وما يُعَدّ **حالُ الوحدة الأخيرة من اللفظ
التالي** بنقطتها. ولا يُقال إنّ التاليَ اسمٌ ولا خبر.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
BARE = "·"
SKELETON = ("0625", "0646")
TARGET = ("0625", "0650", "0646", "0651", "064E")
SHADDA = "0651"
CARRIES = ("064E", "064B")
CORPUS_BARE_SHARE = 0.3108  # من deposits/context_ladder_run.log — المدوّنةُ كلُّها


def points(one: str) -> tuple[str, ...]:
    return tuple(f"{ord(c):04X}" for c in one)


def skeleton(one: str) -> tuple[str, ...]:
    return tuple(f"{ord(c):04X}" for c in one if unicodedata.category(c) != "Mn")


def arabic(one: str) -> bool:
    return any(unicodedata.name(c, "").startswith("ARABIC") for c in one)


def state(one: str) -> str:
    if not one:
        return BARE
    last = one[-1]
    return f"{ord(last):04X}" if unicodedata.category(last) == "Mn" else BARE


def lines_of(text: str) -> list[list[str]]:
    return [
        [one for one in line.split() if arabic(one)]
        for line in text.splitlines()
        if line.strip()
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    lines = lines_of(given.text.read_text(encoding="utf-8"))
    tokens = sum(len(one) for one in lines)
    print(f"— الأسطر: {len(lines)} | الألفاظ: {tokens}")
    print(f"— الشكلُ المقصود: {' '.join(TARGET)}")
    print(f"— الهيكلُ المشترك: {' '.join(SKELETON)}")
    print()

    shapes: Counter[tuple[str, ...]] = Counter()
    for row in lines:
        for one in row:
            if skeleton(one) == SKELETON:
                shapes[points(one)] += 1
    print("— أشكالُ الهيكل المشترك، وعددُ وقوعِ كلٍّ")
    for shape, number in sorted(shapes.items()):
        mark = " ← المقصود" if shape == TARGET else ""
        print(f"  {' '.join(shape)}: {number}{mark}")
    doubled = [one for one in shapes if SHADDA in one and one != TARGET]
    print(f"  أشكالٌ فيها {SHADDA} وليست المقصودَ: {len(doubled)}")
    if doubled:
        for one in doubled:
            print(f"    {' '.join(one)}")
    print()

    here = shapes.get(TARGET, 0)
    after: Counter[str] = Counter()
    followers: Counter[tuple[str, ...]] = Counter()
    alone = 0
    for row in lines:
        for index, one in enumerate(row):
            if points(one) != TARGET:
                continue
            if index + 1 >= len(row):
                alone += 1
                continue
            following = row[index + 1]
            after[state(following)] += 1
            followers[skeleton(following)] += 1

    print(f"— وقوعاتُ الشكل: {here}")
    print(f"  منها بلا تالٍ في سطرها: {alone}")
    measured = sum(after.values())
    print(f"  ولها تالٍ: {measured}")
    if here != measured + alone:
        raise SystemExit("العدُّ لا يُغلِق: وقوعاتٌ ضائعة")
    if not measured:
        raise SystemExit("لا تالٍ لأيّ وقوع — ولا نصيبَ يُقسَم")
    print()

    print("— حالُ الوحدة الأخيرة من التالي، نقطةً نقطة")
    for mark, number in sorted(after.items(), key=lambda one: (-one[1], one[0])):
        print(f"  {mark}: {number} | نصيبٌ {number / measured:.4f}")
    print()

    carried = sum(after.get(one, 0) for one in CARRIES)
    bare = after.get(BARE, 0)
    other = measured - carried - bare
    print("— النِّصَبُ الثلاثة")
    print(
        f"  حاملٌ للأثر {{{', '.join(CARRIES)}}}: {carried} "
        f"| نصيبٌ {carried / measured:.4f}"
    )
    print(f"  حالٌ Mn غيرُهما: {other} | نصيبٌ {other / measured:.4f}")
    print(f"  عارٍ {BARE}: {bare} | نصيبٌ {bare / measured:.4f}")
    if carried + other + bare != measured:
        raise SystemExit("النِّصَبُ لا تُغلِق على الواحد")
    print(f"  ومجموعُ النصيب: {(carried + other + bare) / measured:.6f}")
    print()

    print("— مقابلةُ العُري بعامّة المدوّنة")
    print(f"  عُريُ المدوّنة كلِّها (من context_ladder_run.log): {CORPUS_BARE_SHARE:.4f}")
    print(f"  وعُريُ التالي ههنا: {bare / measured:.4f}")
    print(f"  فالفرقُ: {bare / measured - CORPUS_BARE_SHARE:+.4f}")
    print()

    # **وتفكيكُ النِّصَب بهياكلها**: النصيبُ وحدَه لا يقول **ما** وقع فيه،
    # ومن روى تفكيكًا بلا شاهدٍ روى ما لا سجلَّ له.
    split: dict[str, Counter[tuple[str, ...]]] = {
        "حامل": Counter(),
        "أخرى": Counter(),
        "عارٍ": Counter(),
    }
    for row in lines:
        for index, one in enumerate(row):
            if points(one) != TARGET or index + 1 >= len(row):
                continue
            following = row[index + 1]
            mark = state(following)
            where = "حامل" if mark in CARRIES else ("عارٍ" if mark == BARE else "أخرى")
            split[where][skeleton(following)] += 1
    print("— تفكيكُ كلّ نِصبٍ بهياكله، أكثرُها ورودًا خمسًا")
    for where in ("حامل", "أخرى", "عارٍ"):
        total = sum(split[where].values())
        print(f"  {where} ({total}):")
        for shape, number in split[where].most_common(5):
            print(f"    {' '.join(shape)}: {number}")
        top = sum(number for _, number in split[where].most_common(2))
        if total:
            print(f"    ونصيبُ أكثرِ اثنين من هذا النِّصب: {top / total:.4f}")
    print()

    print(f"— هياكلُ التالي المتمايزة: {len(followers)}")
    print("  وأكثرُها ورودًا خمسًا (هيكلًا بنقاطه):")
    for shape, number in followers.most_common(5):
        print(f"    {' '.join(shape)}: {number}")
    print()

    print("— ما لا يُدَّعى")
    print(f"  العُريُ خليطٌ UNCLASSIFIED: {bare} موضعًا يُعَدّ ولا يُفرَز —")
    print("  فيه ما لا تتبدّل خاتمتُه، وما علامتُه مقدَّرة، وما كُتِب")
    print("  تنوينُه على الألف الذي بعده. وفرزُه يحتاج جردًا مُودَعًا.")
    print("  وتعيينُ الدور فوق هذا القياس: المقيسُ الجارُ التالي لا التركيب،")
    print("  فما قدَّمه الترتيبُ يقع في النِّصَب ويُعَدّ فيها ولا يُفرَز.")
    print("  وشكلٌ واحدٌ لا يُعمَّم: هذا ما تحمله الوحدةُ بعد هذا الشكل")
    print("  في هذا المجمَّد، ولا يُقال «هكذا الإعراب».")
    return 0


if __name__ == "__main__":
    sys.exit(main())
