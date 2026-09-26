"""شاهدُ فصلِ الوقف: المقامُ الثالثُ **مقيسًا لا مطروحًا**، وهويّةٌ تُغلِق.

**لِمَ شاهدٌ منفصل**: سقط شرطان في `c4ffe307…` — فزعمتُ أنّ خانةَ «بلا
علامة» مسكونةٌ بالوقف وأنّ الإنتروبيا ترتفع برفعه، **فجاء الأمران على
خلاف زعمي**. فالسؤالُ: ما حالُ أواخرِ الأسطر نفسِها؟

**ويُقاس المقامُ الثالث (ج) من المدوّنة مباشرةً**، ثمّ **يُقابَل بالطرح**
(أ) − (ب) — فإن اختلفا فأحدُ المقامين ليس ما أُعلِن.

**والهويّةُ المبرهَنة**: `H(أ) − Σ وزنٌ·H = I(الحال؛ أآخرُ السطر)`، وهي
قاعدةُ السلسلة. فيُقابَل الفرقُ بالربح الملحَق لدرجةٍ أولى في السجلّ —
**فإن أغلق فالمقامان مقسومانِ قسمةً تامّةً لا تقريبًا**.
"""

from __future__ import annotations

import argparse
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
SPLIT = REPOSITORY / "deposits" / "pausal_split_run.log"
VERSES = 6_236
BARE = "·"
CLOSES = 5e-6


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    if one and marked(one[-1]):
        return one[-1]
    return BARE


def shown(one: str) -> str:
    return one if one == BARE else f"{one} U+{ord(one):04X}"


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -math.fsum(
        (one / total) * math.log2(one / total) for one in counts.values() if one
    )


def deposited(stand: str) -> dict[str, int]:
    """خاناتُ مقامٍ كما أُودِعت — تُقرَأ ولا تُكتَب."""

    text = SPLIT.read_text(encoding="utf-8")
    block = text.split(f"— خاناتُ الحال في المجال ({stand}):", 1)[1].split("\n\n", 1)[0]
    rows = re.findall(r"^    (\S+)(?: U\+[0-9A-F]{4})? \| (\d+) \| نصيبٌ", block, re.M)
    if len(rows) != 8:
        raise SystemExit(f"خاناتُ ({stand}) {len(rows)} لا ثمانٍ")
    return {one: int(two) for one, two in rows}


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

    inner: Counter[str] = Counter()
    last: Counter[str] = Counter()
    for line in lines:
        row = [one for one in line.split() if arabic(one)]
        for place, token in enumerate(row):
            if place == len(row) - 1:
                last[ending(token)] += 1
            else:
                inner[ending(token)] += 1

    print("— المقامُ (ج) أواخرُ الأسطر — مقيسًا من المدوّنة لا مطروحًا")
    print(f"— ألفاظُه: {sum(last.values())} | وأسطرُ المجمَّد: {len(lines)}")
    print(f"— H(ج) = {entropy(last):.4f}")
    for state, number in last.most_common():
        print(f"    {shown(state)} | {number} | نصيبٌ {number / sum(last.values()):.4f}")

    whole = deposited("أ")
    kept_in = deposited("ب")
    print("\n— المقابلةُ بالطرح: (أ) − (ب) على المقام (ج)")
    astray = 0
    for state in sorted(last, key=lambda one: -last[one]):
        taken = whole[state] - kept_in[state]
        same = "مطابق" if taken == last[state] else "خالف"
        if taken != last[state]:
            astray += 1
        print(f"    {shown(state)} | مقيسٌ {last[state]} | مطروحٌ {taken} | {same}")
    print(f"— خاناتٌ خالفت: {astray}")
    print(
        f"— وألفاظُ (ب) مقيسةً: {sum(inner.values())} | ومُودَعةً: {sum(kept_in.values())}"
    )

    total = sum(whole.values())
    conditional = (
        sum(inner.values()) * entropy(inner) + sum(last.values()) * entropy(last)
    ) / total
    mutual = entropy(Counter(whole)) - conditional
    text = SPLIT.read_text(encoding="utf-8")
    found = re.search(r"— د1 «آخرُ السطر»: .*? ربحٌ ملحَقٌ \+([0-9.]+)", text)
    if found is None:
        raise SystemExit("لا شاهدَ في السجلّ لربح الدرجة الأولى الملحَق")
    first = float(found.group(1))
    drift = abs(mutual - first)
    print("\n— الهويّةُ: H(أ) − Σ وزنٌ·H = I(الحال؛ أآخرُ السطر)")
    print(f"— H(أ) = {entropy(Counter(whole)):.6f} | Σ وزنٌ·H = {conditional:.6f}")
    print(f"— I المُشتَقّ = {mutual:.6f} | والربحُ الملحَقُ المُودَع = {first:.6f}")
    print(f"— أقصى انحرافٍ عن الهويّة: {drift:.3e}")
    print(f"— أتُغلِق؟ {'نعم' if drift < CLOSES else 'لا'}")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ يونيكود — شريحةٌ ونقطةُ ترميز")
    print("  والمقامُ (ج) مسندٌ مُصرَّحٌ به: 6236 موضعًا، واحدٌ من كلّ سطر")
    print("  وهذا يقيس أواخرَ الأسطر ولا يُثبِت أنّها مواضعُ وقف")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
