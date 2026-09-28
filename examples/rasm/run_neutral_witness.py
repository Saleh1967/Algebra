"""شاهدُ الوسط في الأُطُر المناوِبة: ∅ معدودٌ، والمتطفّلُ يُعَدّ ولا يُستبعَد.

**العطلُ الذي يعالجه هذا التشغيل**: قياسٌ سابقٌ سأل «أيُّ حرفٍ يغلب وسطَ
العائلة الجوفاء» فأجاب «الألف»، وبُني على جوابه أنّ **المحايدَ هو الحذف**.
وفي ذلك القياس ثلاثةُ أعطالٍ كلُّها في الإجراء لا في الحساب:

`A_FRAME_THAT_STRIPS_A_LETTER_IS_NOT_A_MORPHOLOGICAL_FRAME`: كان الجذعُ
يُبلَغ **بقلع أوّل حرفٍ** إن كان من (ي ت ن أ ا)، بلا وزنٍ ولا وسم. فصار
`نِسَاءَكُمْ` جوفاءَ إطارُها (س·ء)، و`شَيْءٍ` أختًا لـ`شَاءَ` في إطارٍ واحد —
وهما مادّتان. وأكبرُ عائلةٍ في ذلك القياس (ش·ء) كانت **٦٩٪ من سطوحه**.

`AN_ELEMENT_THAT_IS_NEVER_COUNTED_IS_NEVER_TESTED`: والدعوى «المحايدُ هو
**الحذف**»، والعدّادُ يُحصي الحروفَ الحاضرةَ وحدَها. فـ∅ لم يدخل العدَّ
بموضعٍ واحد، ودعوى الحذف **لم تُختبَر** — لا ثبتت ولا سقطت.

`A_ZERO_WHOSE_FILTER_FORBIDS_ITS_OWN_COUNTER_IS_A_TAUTOLOGY`: والعائلاتُ
كانت تُرشَّح بشرط `all(الوسطُ حرفُ علّة)`، ثمّ يُسأل: أفي الوسط غيرُ العلّة؟
فالصفرُ مشتقٌّ من الشرط لا من البايتات، والفحصُ **لا يملك صورةَ فشل**.

وهذا التشغيلُ يرفع الثلاثةَ بثلاثةِ قرارات، ولا يستورد وسمًا من خارج
البايتات المجمَّدة:

1. **الإطارُ يُقام بالمناوبة المرصودة، لا بالقلع**: الأجوفُ يُعرَف بأنّه
   يُرى في المدوّنة **بوجهَين**: جذعٌ ممدود (`قَالَ`، `قِيلَ`، `يَقُولُ`)
   وجذعٌ مقصورٌ يليه ضميرُ رفعٍ متّصل (`قُلْنَا`). والاسمُ الجامدُ لا
   يناوب، فـ`شَيْء` لا مقصورَ له — **فيسقط الإطارُ عنه بلا استثناءٍ يُسمّى**.
2. **∅ شاهدٌ رابع**: الوجهُ المقصورُ يُعَدّ بموضعه، فالحذفُ مقيسٌ لا مُغفَل.
3. **الترشيحُ لا يذكر المتطفّل**: شرطُ القبول هو المناوبةُ وحدَها، ثمّ
   **يُمسَح وسطُ الإطار على المدوّنة كلِّها** ويُعَدّ كلُّ ما وقع فيه. فإن
   وقع غيرُ (ا و ي ∅) **سقط الصفرُ الشرطيّ ويُسمّى صاحبُه**.

**والسقفُ يُقاس ولا يُفترَض**: تُقابَل إنتروبيا الشاهد بإنتروبيا الوسط
**مرصودةً على الأُطُر كلِّها**، لا بـ`log₂28` — فالسقفُ المنفوخُ يصنع ضغطًا
منفوخًا.

**وحدُّ هذا التشغيل مُعلَن**: السوابقُ المتّصلة (وَ فَ كَ سَ لَ بِ) تُقلَع
بجدولٍ مُعلَن، والعربيّةُ لا تفصل بين السابقة وأصلِ الكلمة بعلامة. فقد
يُقرأ `وَسِعْتَ` (و·س·ع) جذعًا مقصورًا لـ(س·ع)، ولا يميّزه الرسمُ وحدَه.
وهذا **مقيسٌ في المخرَج بابًا مسمًّى** (`أُطُرٌ بلا مقصورٍ فعليّ`)، ولا
يُخفى ولا يُصلَح بوسمٍ غيرِ محمولٍ في الشجرة.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from math import log2
from pathlib import Path
from typing import Final

MARKUP: Final[str] = "<sel>"

FATHA: Final[str] = "\u064e"
DAMMA: Final[str] = "\u064f"
KASRA: Final[str] = "\u0650"
SUKUN: Final[str] = "\u0652"

WEAK: Final[frozenset[str]] = frozenset("اوي")
"""حروفُ المدّ الثلاثةُ التي تقع شاهدًا حاضرًا في الوسط."""

DELETION: Final[str] = "∅"
"""الشاهدُ الرابع: الحذف. ويُعَدّ بموضعه كما تُعَدّ أخواتُه."""

WITNESSES: Final[tuple[str, ...]] = ("ا", "و", "ي", DELETION)
"""فضاءُ الشاهد المُعلَن قبل العدّ؛ وما خرج عنه **متطفّلٌ يُسمّى**."""

HAMZA: Final[str] = "\u0621\u0623\u0625\u0622\u0624\u0626\u0649"
"""أسرةُ الهمزة والمقصورة — مُستبعَدةٌ من طرفَي الإطار بقرارٍ مُعلَن،
لأنّ المهموزَ بابٌ آخرُ في الإعلال لا يُخلَط بالأجوف."""

_CONSONANT: Final[str] = "[\u0621-\u064a]"
_SOUND: Final[str] = f"(?![{HAMZA}]){_CONSONANT}"

PROCLITICS: Final[str] = (
    r"(?:[\u0648\u0641\u0643\u0633][\u064e]?"
    r"|\u0644[\u064e\u0650]?"
    r"|\u0628[\u0650]?)?"
)
"""السوابقُ المتّصلةُ المُعلَنة: وَ فَ كَ سَ لَ لِ بِ — وجدولُها مغلق."""

AGREEMENT: Final[str] = r"(?:تُ|تَ|تِ|تُمْ|تُمَا|تُنَّ|نَا|نَ)"
"""ضمائرُ الرفع المتّصلة؛ وهي علامةُ الفعل التي يقوم عليها الفصل."""

OBJECT: Final[str] = r"(?:نَا|هُ|هُمْ|هَا|كَ|كُمْ|كُم|نِي)?"
"""ضمائرُ النصب المتّصلة، وتُقبَل بعد ضمير الرفع ولا تُقلَع قبله."""

MADD_OF: Final[dict[str, str]] = {"ا": FATHA, "و": DAMMA, "ي": KASRA}
"""المدُّ من جنس حركته؛ وما خالف جنسَه فليس مدًّا بل حرفًا صامتًا."""

SHORTENED: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + f"[{DAMMA}{KASRA}]"
    + f"((?![اويى]){_SOUND})"
    + SUKUN
    + AGREEMENT
    + OBJECT
    + "$"
)
"""الجذعُ المقصور: صامتان بينهما حركةٌ قصيرة، ثمّ سكونٌ فضميرُ رفع.

وصامتان اثنان قبل السكون هما الفصلُ عن السليم: `كَتَبْتُ` ثلاثةُ صوامتَ
قبله، و`قُلْتُ` صامتان — فالوسطُ محذوفٌ ههنا لا مكتوب.
"""

EXTENDED: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + f"([{FATHA}{DAMMA}{KASRA}])"
    + "([اوي])"
    + f"({_SOUND})"
)
"""الجذعُ الممدود: صامتٌ فحركةٌ فمدٌّ من جنسها فصامت."""

MIDDLE: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + f"[{FATHA}{DAMMA}{KASRA}]"
    + f"({_CONSONANT})"
    + f"({_SOUND})"
)
"""مسحُ الوسط: أيُّ حرفٍ وقع بين طرفَي الإطار — ولا شرطَ عليه.

وهذا هو العدّادُ الذي **يجوز أن يسقط**: لا يذكر حروفَ العلّة في شرطه،
فما وقع فيه من غيرها متطفّلٌ مرصود.
"""


def read_tokens(corpus: Path) -> list[str]:
    """ألفاظُ المدوّنة بشكلها؛ والوسمُ مطروحٌ ولا يُعَدّ لفظًا."""

    text = corpus.read_text(encoding="utf-8")
    return [one for one in text.replace(f" {MARKUP} ", " ").split() if one != MARKUP]


def shortened_frame(word: str) -> tuple[str, str] | None:
    """إطارُ اللفظ إن كان جذعًا مقصورًا؛ وإلّا فلا إطارَ يُنسَب إليه."""

    found = SHORTENED.match(word)
    return (found.group(1), found.group(2)) if found else None


def extended_frame(word: str) -> tuple[tuple[str, str], str] | None:
    """إطارُ اللفظ وشاهدُه إن كان جذعًا ممدودًا بمدٍّ من جنس حركته."""

    found = EXTENDED.match(word)
    if found is None or MADD_OF[found.group(3)] != found.group(2):
        return None
    return (found.group(1), found.group(4)), found.group(3)


def alternating(
    tokens: list[str],
) -> tuple[dict[tuple[str, str], Counter[str]], set[tuple[str, str]]]:
    """الأُطُرُ المناوِبة: ما رُئي مقصورًا وممدودًا معًا، مع شواهدِها.

    والمناوبةُ **هي** الوسمُ الصرفيّ ههنا: جامدٌ لا يقصُر، فلا يدخل.
    """

    witnessed: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    shortened: set[tuple[str, str]] = set()
    extended: set[tuple[str, str]] = set()
    for word in tokens:
        frame = shortened_frame(word)
        if frame is not None:
            witnessed[frame][DELETION] += 1
            shortened.add(frame)
        reading = extended_frame(word)
        if reading is not None:
            frame, madd = reading
            witnessed[frame][madd] += 1
            extended.add(frame)
    return witnessed, shortened & extended


BARE_SHORTENED: Final[re.Pattern[str]] = re.compile(
    "^"
    + f"({_SOUND})"
    + f"[{DAMMA}{KASRA}]"
    + f"((?![اويى]){_SOUND})"
    + SUKUN
    + AGREEMENT
    + OBJECT
    + "$"
)
"""الجذعُ المقصورُ بلا سابقةٍ تُقلَع — وهو القراءةُ التي لا تحتمل غيرَها."""


def proclitic_only(
    tokens: list[str], frames: set[tuple[str, str]]
) -> set[tuple[str, str]]:
    """أُطُرٌ لا مقصورَ لها إلّا بعد قلعِ سابقة — وهي حدُّ هذا التشغيل.

    فالرسمُ لا يفصل السابقةَ عن أصل الكلمة، و`سَمِعْنَا` (س·م·ع) تُقرأ
    مقصورًا لـ(م·ع) إن قُلِعت السين. فتُعَدّ هذه الأُطُرُ **ولا تُخفى**،
    ولا تُصلَح بوسمٍ لا تحمله الشجرة.
    """

    grounded: set[tuple[str, str]] = set()
    for word in tokens:
        found = BARE_SHORTENED.match(word)
        if found is not None:
            grounded.add((found.group(1), found.group(2)))
    return frames - grounded


def middle_census(
    tokens: list[str], frames: set[tuple[str, str]]
) -> dict[tuple[str, str], Counter[str]]:
    """كلُّ ما وقع وسطَ هذه الأُطُر في المدوّنة — بلا شرطٍ على جنسه."""

    seen: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for word in tokens:
        found = MIDDLE.match(word)
        if found is None:
            continue
        frame = (found.group(1), found.group(3))
        if frame in frames:
            seen[frame][found.group(2)] += 1
    return seen


def entropy(spread: Counter[str]) -> float:
    """إنتروبيا توزيعٍ مرصود بالبتّات؛ والفارغُ صفرٌ لا خطأ."""

    total = sum(spread.values())
    if total == 0:
        return 0.0
    return -sum(
        count / total * log2(count / total) for count in spread.values() if count
    )


def measured_ceiling(tokens: list[str]) -> Counter[str]:
    """الوسطُ مرصودًا على الأُطُر كلِّها — سقفُ المقارنة، لا `log₂28`."""

    spread: Counter[str] = Counter()
    for word in tokens:
        found = MIDDLE.match(word)
        if found is not None:
            spread[found.group(2)] += 1
    return spread


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    tokens = read_tokens(given.text)
    witnessed, frames = alternating(tokens)
    census = middle_census(tokens, frames)

    witness: Counter[str] = Counter()
    intruder: Counter[str] = Counter()
    for frame in frames:
        witness[DELETION] += witnessed[frame][DELETION]
        for letter, count in census[frame].items():
            if letter in WEAK:
                witness[letter] += count
            else:
                intruder[letter] += count

    held = sum(witness.values())
    strayed = sum(intruder.values())
    total = held + strayed
    ceiling = measured_ceiling(tokens)
    borrowed = proclitic_only(tokens, frames)

    print(f"ألفاظ: {len(tokens)}")
    print(f"أُطُرٌ مناوِبة: {len(frames)} | سطوحُ الشاهد: {held}")
    print(f"أُطُرٌ لا مقصورَ لها إلّا بعد سابقة: {len(borrowed)}", sorted(borrowed))
    print("الشاهدُ (و∅ معدودٌ فيه):", dict(witness.most_common()))
    leader, lead = witness.most_common(1)[0]
    print(f"الغالب: {leader} — {lead}/{held} = {lead / held:.4f}")
    print(
        f"المتطفّل: {strayed}/{total} = {strayed / total:.4f}",
        dict(intruder.most_common()),
    )
    print(
        "حكمُ الصفر الشرطيّ:",
        "صفرٌ شرطيّ ✓"
        if not strayed
        else f"**سقط** — متطفّلُه {dict(intruder.most_common(3))}",
    )
    shadow, roof = entropy(witness), entropy(ceiling)
    print(f"H(شاهد) = {shadow:.4f} بت | H(وسطٌ مرصود) = {roof:.4f} بت")
    print(f"الضغطُ المقيس: {shadow / roof:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
