"""خاتمةُ الآية شرطًا لا أبجديّة — تشغيلُ ختم `26ae5b5b…`.

**الخللُ الذي يُعرَض**: في `248f10df…` قِيس مستوى السطر **أبجديّةً** —
كلُّ آيةٍ رمزٌ — فخرج ثمنُه المحجوزُ ٦٫٩٣٦٩ ومرتدُّه ٠٫٩٦٩٩، فقيل إنّه
أسوأُ الدرجات. **وذلك قياسُ الشيء في غير بابه**: خبرُ حدِّ الآية ليس في
جعلها ذرّةً تُشفَّر، بل في كونها **شرطًا** يقع عنده حقلُ الحال على توزيعٍ
آخر. **فالعتبةُ تمنع الترخيص ولا تمنع القياس.**

**فيُقاس ههنا شرطًا**: توزيعُ العلامة الأخيرة عند خاتمة الآية، مقابلَ
توزيعها عند خاتمة الكلمة؛ وإنتروبيا كلٍّ، والمعلوماتُ المتبادلةُ بين
الحال وكونِ الموضع خاتمةَ آية.

**والغيباتُ تُعَدّ بالاسم**: مواضعُ هيكلٍ بعينه بأرقام أسطرها، والآياتُ
وحيدةُ الكلمة، وما يبدأ منها بوحدتَي ا+ل.

**ولا فهرسَ سورٍ مُودَعٌ**: فالمواضعُ تُذكَر **برقم السطر** لا بسورةٍ
وآية — وما لا يُشتَقّ من البايتات لا يُكتَب.

**ولا اسمٌ لصنفٍ يدخل**: علاماتٌ ومواضعُ وبتّات.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MARKS: dict[str, str] = {
    "َ": "فتحة",
    "ُ": "ضمّة",
    "ِ": "كسرة",
    "ْ": "سكون",
    "ّ": "شدّة",
    "ٰ": "ألفٌ فوقيّة",
    "ً": "تنوين",
    "ٌ": "تنوين",
    "ٍ": "تنوين",
}
BARE = "بلا علامة"
SELECTOR = re.compile(r"<sel>")
VERSES = 6_236
SKELETON = "بسم"


def strip_marks(one: str) -> str:
    return "".join(c for c in one if unicodedata.category(c) != "Mn")


def ending(one: str) -> str:
    """صنفُ العلامة الأخيرة — أو «بلا علامة» إن خُتِم بحرف."""

    for character in reversed(one):
        if unicodedata.category(character) == "Mn":
            return MARKS.get(character, "علامةٌ أخرى")
        return BARE
    return BARE


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    return -math.fsum((one / total) * math.log2(one / total) for one in counts.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    lines = [
        one
        for one in given.text.read_text(encoding="utf-8").splitlines()
        if one.strip()
    ]
    print(f"— الأسطر: {len(lines)}")
    if len(lines) != VERSES:
        raise SystemExit(f"المدوّنةُ تبدّلت: {len(lines)} لا {VERSES}")

    words: list[str] = []
    tails: list[str] = []
    per_line: list[list[str]] = []
    for line in lines:
        row = [one for one in SELECTOR.sub(" ", line).split() if one]
        per_line.append(row)
        words.extend(row)
        tails.append(row[-1])
    print(f"— الكلمُ (بالفراغ، بلا وسوم): {len(words)}")

    at_verse: Counter[str] = Counter(ending(one) for one in tails)
    at_word: Counter[str] = Counter(ending(one) for one in words)
    verse_total = sum(at_verse.values())
    word_total = sum(at_word.values())

    print("\n— ١) توزيعُ العلامة الأخيرة")
    print("  الصنف | عند خاتمة الآية | عند خاتمة الكلمة")
    for name in sorted(set(at_verse) | set(at_word)):
        print(
            f"  {name} | {at_verse[name]} ({at_verse[name] / verse_total:.4f}) "
            f"| {at_word[name]} ({at_word[name] / word_total:.4f})"
        )
    verse_h = entropy(at_verse)
    word_h = entropy(at_word)
    print(f"  إنتروبيا الآية {verse_h:.4f} | إنتروبيا الكلمة {word_h:.4f}")
    print(f"  الفرقُ (آية − كلمة) {verse_h - word_h:+.4f}")
    for name in ("فتحة", "تنوين"):
        print(
            f"  {name}: آيةً {at_verse[name] / verse_total:.4f} "
            f"| كلمةً {at_word[name] / word_total:.4f}"
        )

    print("\n— ٢) ماركوف: الحالُ وكونُ الموضع خاتمةَ آية")
    joint: Counter[tuple[str, str]] = Counter()
    for row in per_line:
        for index, one in enumerate(row):
            joint[(ending(one), "خاتمة" if index == len(row) - 1 else "جوف")] += 1
    total = sum(joint.values())
    left: Counter[str] = Counter()
    right: Counter[str] = Counter()
    for (state, where), number in joint.items():
        left[state] += number
        right[where] += number
    carried = math.fsum(
        (number / total)
        * math.log2((number / total) / ((left[state] / total) * (right[where] / total)))
        for (state, where), number in joint.items()
    )
    inner = Counter(
        {state: number for (state, where), number in joint.items() if where == "جوف"}
    )
    print(f"  H(الحال) = {entropy(left):.6f}")
    print(f"  H(الحال | جوف) = {entropy(inner):.6f}")
    print(f"  H(الحال | خاتمة) = {verse_h:.6f}")
    given_where = (
        right["جوف"] / total * entropy(inner) + right["خاتمة"] / total * verse_h
    )
    print(f"  H(الحال | الموضع) = {given_where:.6f}")
    print(f"  I(الحال ; الموضع) = {carried:.6f} بتًّا للموضع")
    print(f"  ونصيبُ الخاتمة من المواضع {right['خاتمة'] / total:.6f}")
    print(f"  وجملةُ ما تحمله الخاتمةُ: {carried * total:.0f} بتًّا")

    print("\n— ٣) الاستقراء: الشرطُ لا يرفع الإنتروبيا")
    rise = max(entropy(inner) - entropy(left), verse_h - entropy(left))
    print(f"  H(الحال|جوف) − H(الحال) = {entropy(inner) - entropy(left):+.6f}")
    print(f"  H(الحال|خاتمة) − H(الحال) = {verse_h - entropy(left):+.6f}")
    print(f"  H(الحال|الموضع) − H(الحال) = {given_where - entropy(left):+.6f}")
    print(f"  أقصى ارتفاعٍ بالشرط: {rise:+.6f}")

    print("\n— ٤) الغيباتُ معدودةٌ بالاسم، وبأرقام الأسطر")
    found = [
        (index + 1, row.index(one) + 1, one)
        for index, row in enumerate(per_line)
        for one in row
        if strip_marks(one) == SKELETON
    ]
    print(f"  مواضعُ الهيكل «{SKELETON}»: {len(found)}")
    for line_no, place, shape in found:
        width = len(per_line[line_no - 1])
        print(f"    سطرُ {line_no} | موضعُ {place} من {width} | {shape}")
    alone = [index + 1 for index, row in enumerate(per_line) if len(row) == 1]
    print(f"  آياتٌ وحيدةُ الكلمة: {len(alone)}")
    lam = [one for one in alone if strip_marks(per_line[one - 1][0]).startswith("ال")]
    print(f"  منها ما يبدأ هيكليًّا بـ«ال»: {len(lam)} — أسطرُها {lam}")
    print(f"  وسائرُها: {len(alone) - len(lam)}")
    print("\n  ولا فهرسَ سورٍ مُودَعٌ، فلا تُذكَر سورةٌ وآيةٌ — أرقامُ الأسطر وحدَها")
    return 0


if __name__ == "__main__":
    sys.exit(main())
