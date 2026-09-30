"""مساحةُ التصحيف — **كم لفظًا يجمعه هيكلٌ واحد**، وثباتُ ترتيب العلامات.

**ما يقيسه**: التصحيفُ في جوهره أن يشترك لفظان في **الرسم المهمَل**، فلا
يفرّقهما إلّا الإعجامُ والضبط. فيُبنى الهيكلُ بـ`algebra.rasm.skeleton`،
وتُعَدّ الزمرُ التي تحمل أكثرَ من لفظ. **وتلك مساحةُ التصحيف مقيسةً.**

**ويقيس معها ثلاثةَ ثوابتَ للمدخل** يحرسها `test_script_guard`:
المدوّنةُ ليست `NFC`، وترتيبُ الشدّة والتنوين ترتيبُ الرسم، ولا مصيدةَ
من الستّ.

`AND_A_GROUP_IS_A_RISK_NOT_AN_ERROR`: **وحدُّه مُعلَن**: الزمرةُ **موضعُ
اشتباهٍ لا خطأ**. اجتماعُ لفظين في هيكلٍ واحدٍ يقول إنّ فقدَ النقط يُلبِس
بينهما، **ولا يقول إنّ أحدَهما مصحَّفٌ عن الآخر**. والحكمُ بالتصحيف
يحتاج شاهدًا خارجَ الرسم.

`AND_THE_MEASURE_IS_OF_THIS_CORPUS`: ويقيس **هذه البايتات** لا العربيّة.
"""

from __future__ import annotations

import argparse
import collections
import sys
import unicodedata as ud
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
MARKUP = "<sel>"
SHADDA = 0x0651
TANWIN = (0x064B, 0x064C, 0x064D)


def _rasm() -> object:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import rasm

    return rasm


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    rasm = _rasm()
    text = given.text.read_text(encoding="utf-8").replace(MARKUP, " ")

    print("═══ ثوابتُ المدخل — مقيسةً لا مفترَضة ═══")
    print(f"  مطبَّعةٌ NFC؟ {ud.is_normalized('NFC', text)}   (والمطلوب: لا)")
    marks = {chr(one) for one in TANWIN}
    written = sum(
        1
        for i in range(len(text) - 1)
        if ord(text[i]) == SHADDA and text[i + 1] in marks
    )
    canonical = sum(
        1
        for i in range(len(text) - 1)
        if text[i] in marks and ord(text[i + 1]) == SHADDA
    )
    print(f"  شدّةٌ ثمّ تنوين: {written} | تنوينٌ ثمّ شدّة: {canonical}")
    print("  (ccc الشدّة 33 والتنوين 27..29 — فالتطبيعُ يقلبها كلَّها)")
    found = rasm.traps(text)  # type: ignore[attr-defined]
    print(f"  مصائدُ المدخل: {len(found)} — {' · '.join(found) if found else 'لا شيء'}")
    print()

    words = text.split()
    groups: dict[str, set[str]] = collections.defaultdict(set)
    for one in words:
        key = rasm.skeleton(one)  # type: ignore[attr-defined]
        if key:
            groups[key].add(one)
    risky = {key: rows for key, rows in groups.items() if len(rows) > 1}

    print("═══ مساحةُ التصحيف ═══")
    print(f"  ألفاظٌ بالفراغ        : {len(words)}")
    print(f"  ألفاظٌ متمايزة        : {len(set(words))}")
    print(f"  هياكلُ متمايزة        : {len(groups)}")
    print(f"  هياكلُ تحمل أكثرَ من لفظ: {len(risky)}")
    covered = sum(len(rows) for rows in risky.values())
    print(f"  وألفاظٌ داخلَ الزمر    : {covered}")
    print(f"  وأكبرُ زمرة           : {max(len(rows) for rows in risky.values())}")
    print()
    print("  أوسعُ خمسِ زمر:")
    widest = sorted(risky.items(), key=lambda pair: (-len(pair[1]), pair[0]))
    for key, rows in widest[:5]:
        print(f"    {key} ({len(rows)}): " + " · ".join(sorted(rows)[:6]))
    print()

    print("═══ ما يلزم عن هذا ═══")
    print("  **الزمرةُ موضعُ اشتباهٍ لا خطأ**: اجتماعُ لفظين في هيكلٍ واحدٍ")
    print("  يقول إنّ فقدَ النقط يُلبِس بينهما، ولا يقول إنّ أحدَهما مصحَّف.")
    print("  **وثباتُ ترتيب العلامتين شرطٌ لكلّ ما بُنِي على الجوار**:")
    print("  نقطةُ تطبيعٍ واحدةٌ تقلبها، فيعود العدُّ صفرًا بلا شكوى.")
    print("  **وصفرُ المصائد مقيسٌ اليوم** — ولا يُفترَض غدًا.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
