"""شاهدُ المحذوف: الإطارُ لا يسترجعه، والحركةُ تحمله — مقيسًا بنموذجٍ عدميّ.

**ما يبني عليه**: أثبت `c46dfbe3…` أنّ دعوى «المحايدُ هو الحذف» ساقطةٌ
**بالغلبة**: ∅ رابعُ الشواهد لا أوّلُها (١٠٦ من ١٬٣٦٠). ولكنّ الدعوى كان
لها وجهٌ ثانٍ لم يُقَس هناك: «الحذفُ **مسترجَعٌ بالإطار**». وتلك دعوى
**استرجاعٍ** لا غلبة، ولا يحكم فيها عدُّ الحروف بل الإنتروبيا الشرطيّة.
وهذا التشغيلُ يقيسها على وجهَيها.

`THE_FRAME_DOES_NOT_RECOVER_WHAT_WAS_DELETED`: فيُسأل أوّلًا: هل يُنبئ
الإطارُ (صامتٌ أوّلُ · صامتٌ آخِرُ) بالمدّ الذي يظهر في سطوحه الممدودة؟
والجوابُ مقيسٌ: **لا**. وسببُه مرئيٌّ في البايتات: إطارُ (ق·ل) يجمع
`قَالَ` و`قِيلَ` و`يَقُولُ` — وهي **صورُ مادّةٍ واحدة**، لا موادُّ مختلفة.
فالمدُّ السطحيُّ تابعٌ للصورة، والصورةُ **ليست في الإطار**. فدعوى
الاسترجاع بالإطار ساقطةٌ بعددٍ لا بتأويل.

`BUT_THE_SHORTENED_STEM_CARRIES_ITS_OWN_WITNESS`: ثمّ يُسأل ثانيًا وهو
الأصل: إن لم يكن الشاهدُ في الإطار، فأين؟ والمرشَّحُ **حركةُ الجذع
المقصور** نفسِه — الضمّةُ في `قُلْنَا` والكسرةُ في `مِتْنَا`. وهي حركةٌ
**حاضرةٌ في البايتات**، فلا تُستورَد من جدولٍ ولا تُخمَّن.

`AND_THE_FINDING_IS_PRICED_AGAINST_A_NULL_NOT_ASSERTED`: والتوحّدُ وحدَه
لا يكفي: أكثرُ الأُطُر قليلُ السطوح، وإطارٌ ذو سطحٍ واحدٍ **مُوحَّدٌ
بالضرورة**. فيُقصَر الفحصُ على ما له سطحان فأكثر، ويُسعَّر بخلطِ الحركات
على الأُطُر خلطًا مكرَّرًا: كم مرّةً تبلغ الصدفةُ ما بلغه المرصود؟

**وحدُّ هذا التشغيل مُعلَن** ومقيسٌ مرّتين: أربعةُ أُطُرٍ لا مقصورَ لها
إلّا بعد قلعِ سابقةٍ (`سَمِعْنَا` · `وَسِعْتَ` · `وَحُسْنَ` · `وَخُضْتُمْ`)
وهي ليست جوفاءَ أصلًا. **فيُعادُ القياسُ بطرحها** ويُطبَع الوجهان معًا،
ولا يُختار أحسنُهما بعد النظر.

**وما لا يدّعيه هذا التشغيل**: أنّ الحركةَ **هي حرفُ الأصل**. فذلك يحتاج
جدولَ جذورٍ لا تحمله الشجرة، و`مِتْنَا` و`خِفْتُمْ` كسرتان في مادّتين
واويّتين عند الصناعة. والمقيسُ ههنا **إفادةُ الحركة عن الإطار** لا
تسميتُها، ولا يُزاد على المقيس حرفٌ.
"""

from __future__ import annotations

import argparse
import importlib.util
import random
import re
import sys
from collections import Counter, defaultdict
from math import log2
from pathlib import Path
from typing import Any, Final

WITNESS: Final[Path] = Path(__file__).resolve().parent / "run_neutral_witness.py"

REPLICATES: Final[int] = 20_000
"""عددُ الخلطات — مُعلَنٌ قبل التشغيل ولا يُزاد بعد رؤية الرقم."""

SEED: Final[int] = 20_260_927
"""بذرةُ الخلط — مكتوبةٌ كي يُعاد التشغيلُ بعينه."""

TESTABLE: Final[int] = 2
"""أدنى عددِ سطوحٍ يجعل الإطارَ قابلًا للفحص؛ وذو السطح الواحد مُوحَّدٌ
بالضرورة فلا يُعَدّ شاهدًا."""

NAMED: Final[dict[str, str]] = {"\u064f": "ضمّة", "\u0650": "كسرة"}
"""أسماءُ الحركتين للعرض؛ والحكمُ على البايتات لا على الأسماء."""


def witness_module() -> Any:
    spec = importlib.util.spec_from_file_location("run_neutral_witness", WITNESS)
    if spec is None or spec.loader is None:  # pragma: no cover - لا قارئ
        raise RuntimeError("لا قارئَ لشاهد الوسط")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def vowelled(reader: Any) -> re.Pattern[str]:
    """الجذعُ المقصورُ وحركتُه مأخوذةً — وهو `SHORTENED` بفارقِ أنّ الحركةَ تُلتقَط."""

    return re.compile(
        "^"
        + reader.PROCLITICS
        + f"({reader._SOUND})"
        + f"([{reader.DAMMA}{reader.KASRA}])"
        + f"((?![اويى]){reader._SOUND})"
        + reader.SUKUN
        + reader.AGREEMENT
        + reader.OBJECT
        + "$"
    )


def entropy(spread: Counter[str]) -> float:
    """إنتروبيا توزيعٍ مرصود بالبتّات؛ والفارغُ صفرٌ لا خطأ."""

    total = sum(spread.values())
    if total == 0:
        return 0.0
    return -sum(
        count / total * log2(count / total) for count in spread.values() if count
    )


def conditional(by_frame: dict[tuple[str, str], Counter[str]]) -> float:
    """الإنتروبيا الشرطيّةُ على الإطار، موزونةً بسطوح كلّ إطار."""

    total = sum(sum(one.values()) for one in by_frame.values())
    if total == 0:
        return 0.0
    return sum(
        sum(one.values()) / total * entropy(one) for one in by_frame.values() if one
    )


def madd_by_frame(
    reader: Any, tokens: list[str], frames: set[tuple[str, str]]
) -> dict[tuple[str, str], Counter[str]]:
    """المدُّ الظاهرُ في السطوح الممدودة، موزَّعًا على الأُطُر."""

    seen: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for word in tokens:
        reading = reader.extended_frame(word)
        if reading is not None and reading[0] in frames:
            seen[reading[0]][reading[1]] += 1
    return seen


def vowel_rows(
    reader: Any, tokens: list[str], frames: set[tuple[str, str]]
) -> list[tuple[tuple[str, str], str]]:
    """كلُّ جذعٍ مقصورٍ في هذه الأُطُر، مقرونًا بحركته."""

    shape = vowelled(reader)
    rows: list[tuple[tuple[str, str], str]] = []
    for word in tokens:
        found = shape.match(word)
        if found is not None:
            frame = (found.group(1), found.group(3))
            if frame in frames:
                rows.append((frame, found.group(2)))
    return rows


def grouped(
    rows: list[tuple[tuple[str, str], str]],
) -> dict[tuple[str, str], Counter[str]]:
    """الحركاتُ موزَّعةً على الأُطُر."""

    seen: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for frame, vowel in rows:
        seen[frame][vowel] += 1
    return seen


def uniform(by_frame: dict[tuple[str, str], Counter[str]]) -> tuple[int, int, int]:
    """(المُوحَّدة، القابلةُ للفحص، سطوحُها) — وذاتُ السطح الواحد لا تُعَدّ."""

    able = {
        frame: one for frame, one in by_frame.items() if sum(one.values()) >= TESTABLE
    }
    return (
        sum(1 for one in able.values() if len(one) == 1),
        len(able),
        sum(sum(one.values()) for one in able.values()),
    )


def null_reading(rows: list[tuple[tuple[str, str], str]], reached: int) -> float:
    """كم مرّةً تبلغ الصدفةُ ما بلغه المرصود؟ — خلطُ الحركات على الأُطُر."""

    frames = [frame for frame, _ in rows]
    vowels = [vowel for _, vowel in rows]
    rng = random.Random(SEED)
    beat = 0
    for _ in range(REPLICATES):
        shuffled = vowels[:]
        rng.shuffle(shuffled)
        met, _able, _held = uniform(grouped(list(zip(frames, shuffled))))
        if met >= reached:
            beat += 1
    return (beat + 1) / (REPLICATES + 1)


def _report(
    rows: list[tuple[tuple[str, str], str]], tag: str
) -> tuple[int, int, float]:
    met, able, held = uniform(grouped(rows))
    told = null_reading(rows, met)
    print(
        f"{tag}: مُوحَّدةٌ {met} من {able} إطارًا قابلًا للفحص "
        f"(سطوحٌ {held}) | p = {told:.5f}"
    )
    return met, able, told


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    reader = witness_module()
    tokens = reader.read_tokens(given.text)
    _, frames = reader.alternating(tokens)
    borrowed = reader.proclitic_only(tokens, frames)

    madd = madd_by_frame(reader, tokens, frames)
    recovered = sum(1 for frame in frames if len(madd[frame]) == 1)
    print(f"أُطُرٌ مناوِبة: {len(frames)} | ملتبسُ السابقة: {len(borrowed)}")
    print(
        f"أُطُرٌ يسترجع إطارُها مدَّها: {recovered} من {len(frames)} | "
        f"H(المدّ | الإطار) = {conditional(madd):.4f} بت"
    )

    rows = vowel_rows(reader, tokens, frames)
    spread: Counter[str] = Counter(vowel for _, vowel in rows)
    print(
        "حركاتُ الجذع المقصور:",
        {NAMED[one]: count for one, count in spread.most_common()},
        f"من {len(rows)}",
    )
    load, left = entropy(spread), conditional(grouped(rows))
    print(f"H(حركة) = {load:.4f} بت | H(حركة | إطار) = {left:.4f} بت")
    print(f"إفادةُ الإطار عن الحركة: {load - left:.4f} بت")

    _report(rows, "الكلُّ            ")
    _report([one for one in rows if one[0] not in borrowed], "بلا ملتبسِ السابقة")
    return 0


if __name__ == "__main__":
    sys.exit(main())
