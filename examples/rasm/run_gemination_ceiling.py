"""سقفُ الساكن: شطرُ الشدّة **لا يكون آخرَ لفظه أبدًا** — فيَحُدُّ النسبةَ حدًّا.

**لماذا هذا التشغيل**: أُعلِن في تعليقِ طلب الدمج ‎#45 أنّ شرطًا سقط لأنّ
«تْ» جاءت آخرَ لفظها في `٠٫٢٧` فقط. وشُخِّص بعد التشغيل أنّ **٨١٧** منها
شطرُ شدّة. **ويُحقَّق ذلك ههنا مستقلًّا**، ويُقاس ما لم يُقَس: **السقفُ
الأعلى** الذي يفرضه ذلك البسطُ على النسبة نفسِها.

**والحدُّ مُبرهَنٌ لا مقيس**: شطرُ الشدّة الأوّلُ **يتبعه شطرُها الثاني في
اللفظ نفسِه بحكم البناء**، فلا يكون آخرَ لفظه ألبتّة. **فكلُّ شطرِ شدّةٍ في
المقام يخفض النسبةَ ولا يرفعها**، والسقفُ = (الجملةُ − الأشطار) ÷ الجملة.

**وذلك يُقاس للحرفين معًا** — للساكن الذي سقط شرطُه وللذي صمد — **كي لا
يُفحَص العطلُ حيث يضرُّ ويُترَك حيث ينفع**.

**ولا مدوّنةَ مكتوبةٌ بيد**: الحروفُ تُمرَّر بنقاط ترميزها، والوحدةُ
تُشتَقّ من البايتات.
"""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

VERSES = 6_236
SHADDA = "ّ"
SUKUN = "ْ"
WATCHED = ("0645", "062A")


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def pieces_of(word: str) -> list[tuple[str, bool]]:
    """(الوحدة، أهي شطرُ شدّةٍ أوّل) — والمشدَّدُ يُفَكّ شطرين."""

    found: list[tuple[str, bool]] = []
    index = 0
    while index < len(word):
        letter = word[index]
        if unicodedata.category(letter) == "Mn":
            index += 1
            continue
        marks = ""
        ahead = index + 1
        while ahead < len(word) and unicodedata.category(word[ahead]) == "Mn":
            marks += word[ahead]
            ahead += 1
        if SHADDA in marks:
            found.append((letter + SUKUN, True))
            found.append((letter + marks.replace(SHADDA, ""), False))
        else:
            found.append((letter + marks, False))
        index = ahead
    return found


def census(lines: list[str], point: str) -> dict[str, int]:
    unit = chr(int(point, 16)) + SUKUN
    tally = {"whole": 0, "final": 0, "twin": 0, "twin_final": 0}
    for line in lines:
        for word in line.split():
            if not arabic(word):
                continue
            found = pieces_of(word)
            for place, (piece, twin) in enumerate(found):
                if piece != unit:
                    continue
                tally["whole"] += 1
                tally["twin"] += twin
                if place == len(found) - 1:
                    tally["final"] += 1
                    tally["twin_final"] += twin
    return tally


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
    print("— الوحدةُ: حرفٌ مع علامته، والمشدَّدُ يُفَكّ شطرين")
    print("— والشطرُ الأوّلُ ساكنٌ بحكم البناء، ويتبعه الثاني في اللفظ نفسِه")
    for point in WATCHED:
        tally = census(lines, point)
        clean = tally["whole"] - tally["twin"]
        print(f"\n— الساكنُ U+{point}")
        print(f"    جملةً: {tally['whole']} | آخرَ لفظه: {tally['final']}")
        print(f"    النسبةُ كما تُعَدّ: {tally['final'] / tally['whole']:.4f}")
        print(f"    شطرُ شدّةٍ: {tally['twin']}")
        print(f"    ومنها آخرَ لفظه: {tally['twin_final']}")
        print(f"    مكتوبٌ في المدوّنة: {clean}")
        print(f"    النسبةُ بلا المشدَّد: {tally['final'] / clean:.4f}")
        print(f"    **السقفُ الأعلى الممكن**: {clean / tally['whole']:.4f}")
    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — نقطةُ ترميزٍ ووحدة")
    print("  والسقفُ حدٌّ مبرهَنٌ بالبناء لا مقيسٌ: شطرُ الشدّة لا يكون آخرًا")
    print("  وهذا يَحُدُّ شرطًا ولا يقلب حكمَه — والقلبُ يحتاج ختمًا جديدًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
