"""التقشيرُ إلى ١١٢ = ٢٨ × ٤، وإعادةُ البناء **بايتةً بايتة**، ودفترُ البتّات.

**الدعوى المفحوصة**: المدوّنةُ تُقشَّر إلى وحداتِ (صامتٍ + حركة) من ١١٢،
وتُعاد بلا فقد. وههنا تُبنى الآلةُ وتُختبَر المساواةُ **على البايتات لا على
الوصف**: `rebuild(peel(x)) == x` حرفًا بحرف، وإلّا سقطت الدعوى.

**استقراءٌ لها (FOR)**: القشرُ يُبنى بالاستقراء على الموضع — كلُّ حرفٍ مع ما
لحقه من علامات يُعطي وحدةً أو وحدتين بقاعدةٍ معلنة.

**واستقراءٌ عليها (ON)**: المساواةُ تُبرهن بالاستقراء على الطول — الأساسُ
وحدةٌ واحدة، والخطوةُ أنّ إعادةَ بناء الذيل لا تمسّ الرأس. وتُفحَص
بالتشغيل، لا بالدعوى.

**القواعدُ المعلنة**:

1. **العُريُ سكونٌ**: حرفٌ بلا علامةٍ حالتُه السكون — فليس خارجَ الفضاء.
2. **الشدّةُ وحدتان**: ساكنٌ ثمّ متحرّك.
3. **التنوينُ وحدتان**: حركةٌ ثمّ نونٌ ساكنة.
4. **الأبجديّةُ ثمانيةٌ وعشرون**: وأسرةُ الألف (ء أ إ آ ؤ ئ ى) تُطوى إلى ا،
   والتاءُ المربوطةُ إلى ه.

**والمطويُّ لا يُمحى بل يُقيَّد في قناةِ بقيّةٍ مسمّاة**، وكلُّ قناةٍ
تُحصى بتّاتُها ويُسأل: **أهي خبرٌ أم قاعدة؟** — بقياس إنتروبيتها مشروطةً
بالسياق. فما نزل إلى الصفر **قاعدةٌ تُستغنى عنها**، وما بقي **خبرٌ يُحمَل**.
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE28 = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
VOWELS = (FATHA, DAMMA, KASRA, SUKUN)
TANWIN = {"ً": FATHA, "ٌ": DAMMA, "ٍ": KASRA}
SHADDA = "ّ"
ALIF_FAMILY = "اءأإآؤئى"
FOLD = {**{one: "ا" for one in ALIF_FAMILY}, "ة": "ه"}
STRUCTURE = "#"
Unit = tuple[str, str]
Extra = dict[str, str]


def peel(text: str) -> tuple[list[Unit], list[Extra]]:
    """البايتاتُ ⟼ وحداتُ (صامت، حركة) وقنواتُ بقيّةٍ محاذيةٌ لها."""

    units: list[Unit] = []
    extras: list[Extra] = []
    index = 0
    length = len(text)
    while index < length:
        letter = text[index]
        if letter not in FOLD and letter not in BASE28:
            units.append((STRUCTURE, letter))
            extras.append({})
            index += 1
            continue
        base = FOLD.get(letter, letter)
        tail: list[str] = []
        after = index + 1
        while after < length and text[after] in (SHADDA, *VOWELS, *TANWIN):
            tail.append(text[after])
            after += 1
        note: Extra = {}
        if base == "ا":
            note["حامل"] = letter
        if base == "ه":
            note["مربوطة"] = letter
        doubled = SHADDA in tail
        rest = [one for one in tail if one != SHADDA]
        mark = rest[0] if rest else ""
        if doubled:
            units.append((base, SUKUN))
            extras.append({**note, "شدّة": "نعم"})
            note = {}
        if mark in TANWIN:
            units.append((base, TANWIN[mark]))
            extras.append({**note, "تنوين": mark})
            units.append(("ن", SUKUN))
            extras.append({"تنوين": "ذيل"})
        elif mark in ("", SUKUN):
            units.append((base, SUKUN))
            extras.append({**note, "سكون": "عارٍ" if mark == "" else "مكتوب"})
        else:
            units.append((base, mark))
            extras.append(note)
        index = after
    return (units, extras)


def spans(text: str) -> list[tuple[int, int]]:
    """مدى كلّ وحدةٍ في البايتات الأصليّة — فتُعرَض الوحدةُ بحروفها لا بتمثيلها.

    **العلّةُ**: التقشيرُ يقرأ العُريَ سكونًا ويوسّع الشدّة، فطباعةُ الوحدة
    من تمثيلها تُخرِج صورةً **ليست في المصحف** (`اْلْلْلَهُ` مكانَ `اللَّهُ`).
    والمدى يُعيدها إلى بايتاتها، فلا تُعرَض صورةٌ لم تُكتَب.
    """

    found: list[tuple[int, int]] = []
    index = 0
    length = len(text)
    while index < length:
        letter = text[index]
        if letter not in FOLD and letter not in BASE28:
            found.append((index, index + 1))
            index += 1
            continue
        after = index + 1
        tail: list[str] = []
        while after < length and text[after] in (SHADDA, *VOWELS, *TANWIN):
            tail.append(text[after])
            after += 1
        doubled = SHADDA in tail
        rest = [one for one in tail if one != SHADDA]
        mark = rest[0] if rest else ""
        if doubled:
            found.append((index, index))  # الشطرُ الساكنُ لا بايتةَ له وحدَه
        if mark in TANWIN:
            found.append((index, after))
            found.append((after, after))  # نونُ التنوين مُضمَرةٌ في العلامة
        else:
            found.append((index, after))
        index = after
    return found


def rebuild(units: list[Unit], extras: list[Extra]) -> str:
    """الوحداتُ والبقايا ⟼ البايتاتُ نفسُها."""

    out: list[str] = []
    index = 0
    while index < len(units):
        base, value = units[index]
        note = extras[index]
        if base == STRUCTURE:
            out.append(value)
            index += 1
            continue
        if note.get("تنوين") == "ذيل":
            index += 1
            continue
        glyph = note.get("حامل") or note.get("مربوطة") or base
        if note.get("شدّة") == "نعم":
            following = extras[index + 1]
            next_value = units[index + 1][1]
            after = following.get("تنوين")
            out.append(glyph + SHADDA)
            if after and after != "ذيل":
                out.append(after)
                index += 3
            elif next_value == SUKUN and following.get("سكون") == "عارٍ":
                index += 2
            else:
                out.append(next_value)
                index += 2
            continue
        stamped = note.get("تنوين")
        if stamped and stamped != "ذيل":
            out.append(glyph + stamped)
            index += 2
            continue
        if value == SUKUN and note.get("سكون") == "عارٍ":
            out.append(glyph)
        else:
            out.append(glyph + value)
        index += 1
    return "".join(out)


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def channel(extras: list[Extra], key: str) -> Counter[str]:
    return Counter(one[key] for one in extras if key in one)


def sites(units: list[Unit], extras: list[Extra], key: str) -> list[tuple[int, str]]:
    """**مواضعُ القرار كما يراها فاكُّ الشفرة** — لا المواضعُ المثبَتةُ وحدَها.

    وهذا هو التصحيح: قناةٌ تُحصى على ما وقع فيه الحدثُ فقط تعطي صفرًا
    كاذبًا، إذ لا بديلَ فيها. والقناةُ الصادقةُ تُحصى على **كلّ موضعٍ
    يحتمل الحدثَ وضدَّه**.
    """

    found: list[tuple[int, str]] = []
    if key == "شدّة":
        for place in range(len(units) - 1):
            base, value = units[place]
            if base == STRUCTURE or value != SUKUN:
                continue
            if units[place + 1][0] == base:
                found.append((place, extras[place].get("شدّة", "لا")))
    elif key == "تنوين":
        for place in range(1, len(units)):
            if units[place] != ("ن", SUKUN):
                continue
            ahead = units[place + 1][0] if place + 1 < len(units) else STRUCTURE
            behind = units[place - 1]
            if ahead != STRUCTURE or behind[0] == STRUCTURE or behind[1] == SUKUN:
                continue
            mark = extras[place - 1].get("تنوين")
            found.append((place, "نعم" if mark and mark != "ذيل" else "لا"))
    else:
        for place, note in enumerate(extras):
            if key in note:
                found.append((place, note[key]))
    return found


def conditioned(
    units: list[Unit], extras: list[Extra], key: str
) -> tuple[int, float, float]:
    """(المواضع، H₀، H مشروطةً بالحرف وحركةِ ما قبل)."""

    found = sites(units, extras, key)
    if not found:
        return (0, 0.0, 0.0)
    table: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    plain: Counter[str] = Counter()
    for place, value in found:
        base, vowel = units[place]
        before = units[place - 1][1] if place else "^"
        table[(base, vowel, before)][value] += 1
        plain[value] += 1
    mass = sum(plain.values())
    inside = math.fsum(
        sum(one.values()) / mass * entropy(one) for one in table.values()
    )
    return (mass, entropy(plain), inside)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    raw = given.text.read_text(encoding="utf-8")
    units, extras = peel(raw)
    back = rebuild(units, extras)
    cv = [one for one in units if one[0] != STRUCTURE]
    alphabet = {one for one in cv}

    print(f"إعادةُ البناء بايتةً بايتة: {'**مطابقة**' if back == raw else 'مختلفة'}")
    print(f"وحداتُ CV: {len(cv)} | بنيويّة: {len(units) - len(cv)}")
    print(f"أبجديّةُ الوحدات المرصودة: {len(alphabet)} (والمعلنةُ {28 * 4})")
    print(
        f"H(وحدة) = {entropy(Counter(f'{a}{b}' for a, b in cv)):.4f} بت | "
        f"السقفُ log2(112) = {math.log2(112):.4f}"
    )

    print("\nالقناة | مواضعُ القرار | H₀ | Hمشروطة | بتّاتٌ بعد الشرط")
    total = 0.0
    for key in ("حامل", "مربوطة", "سكون", "تنوين", "شدّة"):
        places, plain, inside = conditioned(units, extras, key)
        bits = inside * places
        total += bits
        print(f"  {key}: {places} | {plain:.4f} | {inside:.4f} | {bits:.0f}")
    body = entropy(Counter(f"{a}{b}" for a, b in cv)) * len(cv)
    print(
        f"\nتيّارُ CV: {body:.0f} بتًّا | البقايا: {total:.0f} بتًّا "
        f"| نصيبُ البقايا: {total / (body + total):.4f}"
    )
    return 0 if back == raw else 1


if __name__ == "__main__":
    sys.exit(main())
