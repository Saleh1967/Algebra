"""لامُ الناقص في الأُطُر المناوِبة — ختمُ `6aca9ee4…` مُشغَّلًا.

**الإطارُ يُقام بالمناوبة المرصودة، لا بقلعِ سابقة**: الناقصُ يُعرَف بأنّه
يُرى في البايتات نفسِها **بوجهَين** — لامٌ ظاهرةٌ (`دَعَا` · `رَمَى` ·
`دَعَوْتُ`) ولامٌ محذوفةٌ أمام تاء التأنيث الساكنة (`دَعَتْ` · `رَمَتْ`).
وما لا يناوب لا يدخل، فيسقط الجامدُ وحرفُ المعنى **بالبناء لا باستثناءٍ
يُسمّى**.

**والفصلُ عن السالم بعدّ الصوامت**: `كَتَبَتْ` ثلاثةُ صوامتَ قبل تاء
التأنيث، و`دَعَتْ` صامتان — فالثالثُ محذوفٌ لا مكتوب. وهو بعينه الفصلُ
الذي أقام إطارَ الأجوف في `run_neutral_witness.py`.

`THE_DELETED_LAM_IS_A_PLACE_NOT_AN_ABSENCE`: و∅ شاهدٌ بموضعه يُعَدّ كما
تُعَدّ أخواتُه، فدعوى «المحايدُ هو الحذف» تُقاس ولا تُروى.

`A_FILTER_THAT_FORBIDS_ITS_OWN_COUNTER_IS_A_TAUTOLOGY`: ومُرشِّحُ الأُطُر
**لا يذكر حروفَ العلّة ألبتّة** — شرطُه المناوبةُ وحدَها — ثمّ يُمسَح موضعُ
اللام على المدوّنة كلِّها فيُعَدّ كلُّ ما وقع فيه. فإن وقع غيرُ (ا و ي ∅)
**سُمّي بعينه وأُحصي، ولم يُكنَس قبل العدّ**.

`THE_MAQSURA_IS_FOLDED_BY_A_DECLARED_DECISION_AND_ITS_COUNT_IS_PRINTED`:
والألفُ المقصورةُ مردودةٌ إلى الألف — رسمٌ لها لا شاهدٌ خامس — **وعددُها
يُطبَع خامًا** فلا يُخفى القرار.

**والرقمُ الحاسم**: عددُ الموادّ المناوِبة، مقابلَ نقطة التعادل ١٨٣
المنقولة من قياس الإعلال: (٣٣٥ − ٤٥) ÷ log₂٣. والمقيسُ **حدٌّ أدنى**
لموادّ اللغة لا جردٌ لها؛ فمجاوزتُه تُقفِل السؤالَ، وعدمُها لا يفتحه
جوابًا.

**وحدُّ هذا التشغيل مُعلَن**: السوابقُ المتّصلةُ تُقلَع بجدولٍ مغلقٍ
مُعلَن، والرسمُ لا يفصلها عن أصل الكلمة. فتُعَدّ الأُطُرُ التي لا وجهَ
محذوفَ لها إلّا بعد قلعِ سابقةٍ **بابًا مسمًّى** ولا تُخفى.
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
SHADDA: Final[str] = "\u0651"

TAA: Final[str] = "\u062a"
MAQSURA: Final[str] = "\u0649"
ALIF: Final[str] = "\u0627"

WEAK: Final[frozenset[str]] = frozenset("اوي")
"""حروفُ اللام المعتلّة بعد ردّ المقصورة إلى الألف."""

DELETION: Final[str] = "∅"
"""الشاهدُ الرابع: اللامُ المحذوفة، وتُعَدّ بموضعها."""

WITNESSES: Final[tuple[str, ...]] = ("ا", "و", "ي", DELETION)
"""فضاءُ الشاهد المُعلَن قبل العدّ؛ وما خرج عنه **متطفّلٌ يُسمّى**."""

BREAK_EVEN: Final[int] = 183
"""نقطةُ التعادل المنقولةُ من قياس الإعلال: (٣٣٥ − ٤٥) ÷ log₂٣."""

HAMZA: Final[str] = "\u0621\u0623\u0625\u0622\u0624\u0626"
"""أسرةُ الهمزة — مُستبعَدةٌ من صامتَي الإطار بقرارٍ مُعلَن، لأنّ المهموزَ
بابٌ آخرُ في الإعلال لا يُخلَط بالناقص."""

_CONSONANT: Final[str] = "[\u0621-\u064a]"
_SOUND: Final[str] = f"(?![{HAMZA}{ALIF}\u0648\u064a{MAQSURA}]){_CONSONANT}"
"""صامتٌ أصليٌّ: لا همزةَ ولا حرفَ علّة — فطرفا الإطار لا يلتبسان باللام."""

PROCLITICS: Final[str] = (
    r"(?:[\u0648\u0641\u0643\u0633][\u064e]?"
    r"|\u0644[\u064e\u0650]?"
    r"|\u0628[\u0650]?)?"
)
"""السوابقُ المتّصلةُ المُعلَنة: وَ فَ كَ سَ لَ لِ بِ — وجدولُها مغلق."""

AGREEMENT: Final[str] = r"(?:تُ|تَ|تِ|تُمْ|تُمَا|تُنَّ|نَا|نَ)"
"""ضمائرُ الرفع المتّصلة؛ وهي علامةُ الفعل التي يقوم عليها الفصل."""

OBJECT: Final[str] = r"(?:هُ|هُمْ|هَا|كَ|كُمْ|كُم|نِي|نَا)?"
"""ضمائرُ النصب المتّصلة، وتُقبَل بعد ضمير الرفع ولا تُقلَع قبله."""

_HARAKA: Final[str] = f"[{FATHA}{DAMMA}{KASRA}]"

MADD_LAM: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + _HARAKA
    + f"({_SOUND})"
    + f"{_HARAKA}?"
    + f"([{ALIF}\u0648\u064a{MAQSURA}])"
    + "$"
)
"""اللامُ الظاهرةُ حرفَ مدٍّ في آخر اللفظ: `دَعَا` · `رَمَى` · `سَعَى`."""

BOUND_LAM: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + FATHA
    + f"({_SOUND})"
    + FATHA
    + "([\u0648\u064a])"
    + SUKUN
    + AGREEMENT
    + OBJECT
    + "$"
)
"""اللامُ الظاهرةُ ساكنةً قبل ضمير الرفع: `دَعَوْتُ` · `رَمَيْنَا`."""

DROPPED_LAM: Final[re.Pattern[str]] = re.compile(
    "^"
    + PROCLITICS
    + f"({_SOUND})"
    + _HARAKA
    + f"({_SOUND})"
    + FATHA
    + TAA
    + SUKUN
    + OBJECT
    + "$"
)
"""اللامُ المحذوفةُ أمام تاء التأنيث الساكنة: `دَعَتْ` · `رَمَتْ`.

وصامتان اثنان قبل التاء هما الفصلُ عن السالم: `كَتَبَتْ` ثلاثةٌ.
"""

BARE_DROPPED: Final[re.Pattern[str]] = re.compile(
    "^"
    + f"({_SOUND})"
    + _HARAKA
    + f"({_SOUND})"
    + FATHA
    + TAA
    + SUKUN
    + OBJECT
    + "$"
)
"""الوجهُ المحذوفُ بلا سابقةٍ تُقلَع — وهو القراءةُ التي لا تحتمل غيرَها."""

LAM_PLACE: Final[re.Pattern[str]] = re.compile(
    "^" + PROCLITICS + f"({_SOUND})" + _HARAKA + f"({_SOUND})" + f"{_HARAKA}?" + "(.)$"
)
"""مسحُ موضع اللام: أيُّ حرفٍ وقع بعد صامتَي الإطار — ولا شرطَ على جنسه.

وهذا هو العدّادُ الذي **يجوز أن يسقط**: لا يذكر حروفَ العلّة في شرطه،
فما وقع فيه من غيرها متطفّلٌ مرصودٌ يُسمّى بعينه.
"""

PARTICLES: Final[tuple[str, ...]] = (
    "عَلَى",
    "إِلَى",
    "حَتَّى",
    "لَدَى",
    "مَتَى",
    "أَنَّى",
    "بَلَى",
)
"""حروفُ معنًى وأسماءٌ مبنيّةٌ تنتهي بألفٍ مقصورة — جدولٌ مغلقٌ مُعلَن."""


def read_tokens(corpus: Path) -> list[str]:
    """ألفاظُ المدوّنة بشكلها؛ والوسمُ مطروحٌ ولا يُعَدّ لفظًا."""

    text = corpus.read_text(encoding="utf-8")
    return [one for one in text.replace(f" {MARKUP} ", " ").split() if one != MARKUP]


def folded(letter: str) -> str:
    """ردُّ المقصورة إلى الألف — قرارٌ مُعلَنٌ قبل العدّ، وخامُها مطبوع."""

    return ALIF if letter == MAQSURA else letter


def visible_lam(word: str) -> tuple[tuple[str, str], str] | None:
    """إطارُ اللفظ وشاهدُه إن كانت لامُه ظاهرةً بأحد وجهَيها."""

    found = MADD_LAM.match(word)
    if found is not None:
        return (found.group(1), found.group(2)), found.group(3)
    found = BOUND_LAM.match(word)
    if found is not None:
        return (found.group(1), found.group(2)), found.group(3)
    return None


def dropped_lam(word: str) -> tuple[str, str] | None:
    """إطارُ اللفظ إن كانت لامُه محذوفةً؛ وإلّا فلا إطارَ يُنسَب إليه."""

    found = DROPPED_LAM.match(word)
    return (found.group(1), found.group(2)) if found else None


def alternating(
    tokens: list[str],
) -> tuple[dict[tuple[str, str], Counter[str]], set[tuple[str, str]], Counter[str]]:
    """الأُطُرُ المناوِبة: ما رُئي بلامٍ ظاهرةٍ ومحذوفةٍ معًا، مع شواهدِها.

    والمناوبةُ **هي** الوسمُ الصرفيّ ههنا: ما لا يناوب لا يدخل.
    ويُرَدُّ الخامُ (قبل ردّ المقصورة) كي لا يُخفى القرارُ المُعلَن.
    """

    witnessed: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    raw: Counter[str] = Counter()
    visible: set[tuple[str, str]] = set()
    dropped: set[tuple[str, str]] = set()
    for word in tokens:
        reading = visible_lam(word)
        if reading is not None:
            frame, lam = reading
            witnessed[frame][folded(lam)] += 1
            raw[lam] += 1
            visible.add(frame)
        frame = dropped_lam(word)
        if frame is not None:
            witnessed[frame][DELETION] += 1
            raw[DELETION] += 1
            dropped.add(frame)
    return witnessed, visible & dropped, raw


def lam_census(
    tokens: list[str], frames: set[tuple[str, str]]
) -> dict[tuple[str, str], Counter[str]]:
    """كلُّ ما وقع موضعَ اللام في هذه الأُطُر — بلا شرطٍ على جنسه."""

    seen: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for word in tokens:
        found = LAM_PLACE.match(word)
        if found is None:
            continue
        frame = (found.group(1), found.group(2))
        if frame in frames:
            seen[frame][folded(found.group(3))] += 1
    return seen


def proclitic_only(
    tokens: list[str], frames: set[tuple[str, str]]
) -> set[tuple[str, str]]:
    """أُطُرٌ لا وجهَ محذوفَ لها إلّا بعد قلعِ سابقة — وهي حدُّ التشغيل."""

    grounded: set[tuple[str, str]] = set()
    for word in tokens:
        found = BARE_DROPPED.match(word)
        if found is not None:
            grounded.add((found.group(1), found.group(2)))
    return frames - grounded


def particles_admitted(frames: set[tuple[str, str]]) -> list[str]:
    """حروفُ المعاني المُعلَنة التي وجدت لنفسها إطارًا مناوِبًا — إن وُجِدت."""

    admitted: list[str] = []
    for one in PARTICLES:
        reading = visible_lam(one)
        if reading is not None and reading[0] in frames:
            admitted.append(one)
    return admitted


def entropy(spread: Counter[str]) -> float:
    """إنتروبيا توزيعٍ مرصود بالبتّات؛ والفارغُ صفرٌ لا خطأ."""

    total = sum(spread.values())
    if total == 0:
        return 0.0
    return -sum(
        count / total * log2(count / total) for count in spread.values() if count
    )


def measured_ceiling(tokens: list[str]) -> Counter[str]:
    """موضعُ اللام مرصودًا على الأُطُر كلِّها — سقفُ المقارنة لا `log₂28`."""

    spread: Counter[str] = Counter()
    for word in tokens:
        found = LAM_PLACE.match(word)
        if found is not None:
            spread[folded(found.group(3))] += 1
    return spread


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    tokens = read_tokens(given.text)
    witnessed, frames, raw = alternating(tokens)
    census = lam_census(tokens, frames)

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
    borrowed = proclitic_only(tokens, frames)
    admitted = particles_admitted(frames)

    print(f"ألفاظ: {len(tokens)}")
    print(f"موادُّ مناوِبة: {len(frames)} | سطوحُ الشاهد: {held}")
    print(f"الخامُ قبل ردّ المقصورة: {dict(raw.most_common())}")
    print("الشاهدُ (و∅ معدودٌ فيه):", dict(witness.most_common()))
    if held:
        leader, lead = witness.most_common(1)[0]
        print(f"الغالب: {leader} — {lead}/{held} = {lead / held:.4f}")
        print(f"ا − و = {witness['ا'] - witness['و']}")
    print(
        f"المتطفّل: {strayed}/{total}"
        + (f" = {strayed / total:.4f}" if total else ""),
        dict(intruder.most_common()),
    )
    print(
        "حكمُ الصفر الشرطيّ:",
        "صفرٌ شرطيّ ✓"
        if not strayed
        else f"**سقط** — متطفّلُه {dict(intruder.most_common(3))}",
    )
    print(f"حروفُ المعاني الداخلة: {len(admitted)} {admitted}")
    print(f"أُطُرٌ لا محذوفَ لها إلّا بعد سابقة: {len(borrowed)}", sorted(borrowed))
    verdict = (
        "**لا يشتري** — الحدُّ الأدنى وحدَه يجاوز التعادل"
        if len(frames) > BREAK_EVEN
        else "السؤالُ مفتوح — الحدُّ الأدنى دون التعادل، والمدوّنةُ ليست اللغة"
    )
    print(f"الموادُّ {len(frames)} مقابلَ التعادل {BREAK_EVEN}: {verdict}")
    shadow, roof = entropy(witness), entropy(measured_ceiling(tokens))
    print(f"H(شاهد) = {shadow:.4f} بت | H(موضعٌ مرصود) = {roof:.4f} بت")
    if roof:
        print(f"الضغطُ المقيس: {shadow / roof:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
