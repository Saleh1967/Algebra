"""سقفُ «الباقي ثابتًا»: **تسعةُ هياكلَ تمتنع بالبناء** — فالسقفُ دون الواحد.

**العطل ٢٦ في هذه الشجرة**: شرطان (ح١٢ وط١٢) يقيسان **نصيبَ ما بقي ثابتًا
في النصفين من ثابتِ النصف الزوجيّ**. ومقامُهما يحمل هياكلَ **لا تظهر في
النصف الفرديّ بالكلّيّة**، والحسابُ يشترط لعضو البسط أن تكون له حالٌ واحدةٌ
في الفرديّ — **فالغائبُ يمتنع بالبناء أن يدخل البسط**.

**فالسقفُ** `(المقام − الغائب) ÷ المقام` **لا الواحد**. ويُقاس ههنا للحدّين
معًا (حدُّ «كلّ متتاليةٍ بلا فراغ» وحدُّ «فيه حرفٌ عربيّ»)، **ويُعاد
المُودَعُ بعينه** كي يُعلَم أنّ القسمةَ هي هي.

**وما يلزم عنه**: النسبةُ المُعلَنةُ **حدٌّ أدنى**، والنسبةُ على الحاضر في
النصفين أعلى. **ولا يقلب ذلك حكمًا مختومًا** — الحكمُ باقٍ كما خُتِم، وهذا
**يُصحّح سقفًا ويُعلِن حدًّا أدنى**، لا يُعيد تفسيرَ شرط.
"""

from __future__ import annotations

import argparse
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
BARE = "·"
LEAST = 5


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    return one[-1] if one and marked(one[-1]) else BARE


def skeleton(one: str) -> str:
    return "".join(two for two in one if not marked(two))


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
    print(f"— شرطُ القسمة: {LEAST} وقوعاتٍ فأكثرَ في النصف الزوجيّ")
    for label, whole_words in (
        ("كلُّ متتاليةٍ بلا فراغ — مسندُ ح١٢", True),
        ("فيه حرفٌ عربيّ — مسندُ ط١٢", False),
    ):
        even: defaultdict[str, Counter[str]] = defaultdict(Counter)
        odd: defaultdict[str, Counter[str]] = defaultdict(Counter)
        for number, line in enumerate(lines):
            for word in line.split():
                if not whole_words and not arabic(word):
                    continue
                where = even if number % 2 == 0 else odd
                where[skeleton(word)][ending(word)] += 1
        steady = {
            one
            for one, seen in even.items()
            if sum(seen.values()) >= LEAST and len(seen) == 1
        }
        absent = {one for one in steady if one not in odd}
        both = {
            one
            for one in steady
            if one in odd
            and len(odd[one]) == 1
            and next(iter(odd[one])) == next(iter(even[one]))
        }
        present = len(steady) - len(absent)
        print(f"\n— {label}")
        print(f"    ثابتُ الزوجيّ (المقام): {len(steady)}")
        print(f"    غائبٌ عن الفرديّ بالكلّيّة: {len(absent)}")
        print(f"    باقٍ ثابتًا (البسط): {len(both)}")
        print(f"    النسبةُ كما أُودِعت: {len(both) / len(steady):.4f}")
        print(f"    **السقفُ**: {present}/{len(steady)} = {present / len(steady):.6f}")
        print(f"    والنسبةُ على الحاضر في النصفين: {len(both) / present:.4f}")
    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ — هياكلُ وشرائحُ حالٍ وعدّادات")
    print("  والسقفُ حدٌّ مبرهَنٌ بالبناء: الغائبُ لا يكون «باقيًا ثابتًا»")
    print("  ولا يقلب هذا حكمًا مختومًا — يُصحّح سقفًا ويُعلِن حدًّا أدنى")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
