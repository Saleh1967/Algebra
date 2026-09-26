"""شُغِّل ختمُ `a581ddb9…`: **خمسةٌ من خمسة — ولا نقطةَ ترميزٍ بلا قناة، ولا خانةَ صامتة**.

`EVERY_CODE_POINT_HAS_ONE_CHANNEL`: نقاطُ الترميز **٧١١٬٩٣٤** كلُّها مُسنَدة،
**وغيرُ المُسنَد صفر** (ج١): هويّةُ وحدةٍ ٣٠٨٬٧٣٤، وحالةٌ ٢٠٥٬٨٤٨، وبنيةٌ
١٠٣٬٩٦٧، وسكونٌ مكتوب ٣٧٬٣٧٢، وشدّةٌ ٢٣٬٠١٦، وحاملٌ ٢١٬٧٥٩، وتنوينٌ ٨٬٨٩٤،
ومربوطةٌ ٢٬٣٤٤. **والأسطرُ كلُّها تُعاد** من الوحدات وقنوات الباقي (ج٢).

`AND_EVERY_ROLE_CELL_SPEAKS`: السجلُّ ١١٢ وحدةً × خمسةَ عشرَ مستوًى =
**١٬٦٨٠ خانة، والصامتةُ صفر** (ج٣). **والوحداتُ الـ١١٢ مرصودةٌ كلُّها.**

`WHAT_IS_FILLED_AND_WHAT_WAITS`: **سبعةُ مستوياتٍ** ملآنةٌ للوحدات كلِّها:
الترميزيّ والترتيبُ الأبجديّ (اصطلاح الشجرة)، والإملائيّ والحالُ وتحقّقُها
(بايتات)، والمخرجُ (مُودَع)، ونصُّ صاحب المستودع، والمدلولُ وحده (منقولٌ من
الكتاب: «لفظٌ مفردٌ مهمل»). **ومستويان** ملآنان لـ٣٦ وحدةً — حروفِ
«سألتمونيها» التسعة × الأحوال الأربع — من الجدول المُودَع غيرِ الموقَّع.
**وستّةٌ** `UNCLASSIFIED` كلُّها بأسبابها: قيمةُ الجُمَّل، والصفةُ (حاجز
`SIFA_TABLE_BYTES`)، والاشتقاقيّ، والصرفيّ، والنحويّ، والإعرابيّ. فالمملوءُ
**٨٥٦** خانة، والمعلَّقُ بسببه **٨٢٤**.

`NO_WORD_BEGINS_WITH_SUKUN_EXCEPT_NAMED_ONES`: ج٤ **صمد**: ١٩ من **٧٨٬٢٤٥**
لفظًا (٠٫٠٠٠٢٤). منها **سبعةَ عشرَ** من فواتح السور — «حم» سبعًا، و«طسم»
مرّتين، و«كهيعص» و«طه» و«طس» و«يس» و«ص» و«عسق» و«ق» و«ن» — **واثنان**
لامُ أمرٍ ساكنةٌ بعد «ثُمَّ»: «لْيَقْطَعْ» و«لْيَقْضُوا».

`AND_THIS_CONDITION_WAS_NOT_BLIND`: **وهذا عطلٌ يُسمّى**: ختمُ `72b39b4c…` في
الجلسة نفسها شُغِّل **قبل هذا الختم بسبعَ عشرةَ دقيقة**، وفي تشخيصه لامُ أمرٍ
ساكنةٌ أوّلَ اللفظ و«يس». ولم يُعلَن ذلك في استخراج هذا الختم. فحكمُ ج٤
**يُقرأ مع هذا العلم**: الشذوذُ الذي فيه كان بعضُه معروفًا قبله.

`THE_LETTER_DOES_NOT_STAND_ALONE_MARKED`: ج٥ **صمد صفرًا**: لا لفظَ من حرفٍ
واحدٍ عليه علامة. **والألفاظُ ذاتُ الحرف الواحد ثلاثةٌ كلُّها عارية**: «ص» و«ق»
و«ن» — فواتحُ سور، أسماءُ حروفٍ تُتهجّى لا حروفٌ متحرّكة.

`AND_THE_STREAM_MISPLACES_2_814_VOWELS`: **ووصفًا لا حكمًا**: ٢٬٨١٤ حرفًا عاريًا
يليه «اً» في لفظه — حالتُه في تيّار الـ١١٢ **سكون** وحركتُه في النطق **على
الألف بعده**. فالتيّارُ **صحيحٌ ترميزًا ومُنزاحٌ صوتًا** في هذه المواضع، وهو
أكبرُ ما يفصل المستوى الترميزيّ عن الصوتيّ في السجلّ.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_unit_roles_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_unit_roles.py"

pytestmark = requires_corpus

UNITS = 112
LEVELS = 15
CODE_POINTS = 711_934
CHANNELS = {
    "هويّة": 308_734,
    "حامل": 21_759,
    "مربوطة": 2_344,
    "حالة": 205_848,
    "سكون مكتوب": 37_372,
    "شدّة": 23_016,
    "تنوين": 8_894,
    "بنية": 103_967,
}
CELLS = 1_680
FILLED = 856
WAITING = 824
FILLED_EVERYWHERE = 7
FULLY_UNCLASSIFIED = 6
TABLE_UNITS = 36
TOKENS = 78_245
STARTING_WITH_SUKUN = {
    "حم": 7,
    "طسم": 2,
    "كهيعص": 1,
    "طه": 1,
    "لْيَقْطَعْ": 1,
    "لْيَقْضُوا": 1,
    "طس": 1,
    "يس": 1,
    "ص": 1,
    "عسق": 1,
    "ق": 1,
    "ن": 1,
}
OPENING_LETTERS = 17
COMMAND_LAMS = 2
SUKUN_SHARE = 0.00024
SINGLE_LETTERS = ["ص", "ق", "ن"]
DISPLACED = 2_814
EARLIER_SEAL = "72b39b4c"
"""الختمُ الذي شُغِّل قبل هذا بسبعَ عشرةَ دقيقةً ولم يُذكَر في استخراجه."""


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_unit_roles", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _raw() -> str:
    return CORPUS.read_text(encoding="utf-8")


@cache
def _registry() -> tuple[object, object]:
    return _reader().registry(_raw().rstrip("\n"))  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("a581ddb9")


def test_every_code_point_has_exactly_one_channel() -> None:
    """ج١: ٧١١٬٩٣٤ نقطةً، وغيرُ المُسنَد صفر."""

    reader = _reader()
    counts, unassigned = reader.partition(_raw())
    first = next(one for one in PREDICTIONS if one.identifier == "ج١")
    assert len(_raw()) == CODE_POINTS
    assert dict(counts) == CHANNELS
    assert sum(counts.values()) + unassigned == CODE_POINTS
    assert first.verdict(Fraction(unassigned)) is Verdict.MET


def test_every_line_is_rebuilt_from_the_channels() -> None:
    """ج٢: لا سطرَ يفوت الإعادة."""

    reader = _reader()
    depth = reader._load("run_surface_depth")
    second = next(one for one in PREDICTIONS if one.identifier == "ج٢")
    missed = depth.unrebuilt_lines(_raw().rstrip("\n"))
    assert second.verdict(Fraction(missed)) is Verdict.MET


def test_no_role_cell_is_silent() -> None:
    """ج٣: ١٬٦٨٠ خانةً، ولا صامتةَ فيها — والوحداتُ الـ١١٢ مرصودةٌ كلُّها."""

    reader = _reader()
    rows, found = _registry()
    third = next(one for one in PREDICTIONS if one.identifier == "ج٣")
    assert len(rows) == UNITS and len(found) == UNITS  # type: ignore[arg-type]
    assert len(reader.LEVELS) == LEVELS
    assert UNITS * LEVELS == CELLS
    assert third.verdict(Fraction(reader.silent_cells(rows))) is Verdict.MET


def test_what_is_filled_and_what_waits() -> None:
    """سبعةُ مستوياتٍ ملآنة، واثنان لـ٣٦ وحدة، وستّةٌ معلَّقةٌ بأسبابها."""

    reader = _reader()
    rows, _ = _registry()
    table = reader.coverage(rows)
    everywhere = [
        level for level, sources in table.items() if reader.UNCLASSIFIED not in sources
    ]
    nowhere = [
        level
        for level, sources in table.items()
        if set(sources) == {reader.UNCLASSIFIED}
    ]
    assert len(everywhere) == FILLED_EVERYWHERE
    assert len(nowhere) == FULLY_UNCLASSIFIED
    assert "صوتي: الصفة" in nowhere and "اشتقاقي" in nowhere
    assert table["وظيفي: الجدول المُودَع"][reader.DEPOSITED] == TABLE_UNITS
    waiting = sum(sources[reader.UNCLASSIFIED] for sources in table.values())
    assert (CELLS - waiting, waiting) == (FILLED, WAITING)


def test_no_word_begins_with_sukun_except_named_ones() -> None:
    """ج٤ صمد: ١٩ من ٧٨٬٢٤٥ — سبعةَ عشرَ فاتحةً ولامان للأمر."""

    reader = _reader()
    tokens, offending = reader.first_unit_census(_raw().rstrip("\n"))
    fourth = next(one for one in PREDICTIONS if one.identifier == "ج٤")
    assert tokens == TOKENS
    assert dict(Counter(offending)) == STARTING_WITH_SUKUN
    lams = sum(value for key, value in STARTING_WITH_SUKUN.items() if key[0] == "ل")
    assert (len(offending) - lams, lams) == (OPENING_LETTERS, COMMAND_LAMS)
    share = Fraction(len(offending), tokens)
    assert abs(float(share) - SUKUN_SHARE) < 5e-6
    assert fourth.verdict(share) is Verdict.MET
    earlier = REPOSITORY / "tests" / "arabic" / "test_letter_roles_seal.py"
    assert EARLIER_SEAL in earlier.read_text(encoding="utf-8")  # سابقٌ ومُسمًّى


def test_the_letter_does_not_stand_alone_marked() -> None:
    """ج٥ صمد صفرًا: لا حرفَ متحرّكًا لفظًا — والثلاثةُ العارية فواتح."""

    reader = _reader()
    marked, bare = reader.single_letter_tokens(_raw().rstrip("\n"))
    fifth = next(one for one in PREDICTIONS if one.identifier == "ج٥")
    assert sorted(bare) == SINGLE_LETTERS
    assert fifth.verdict(Fraction(len(marked))) is Verdict.MET


def test_the_stream_misplaces_the_vowels_written_on_the_alif() -> None:
    """وصفًا: ٢٬٨١٤ حرفًا حالتُه سكونٌ في التيّار وحركتُه على الألف بعده."""

    reader = _reader()
    moved = reader.displaced_by_tanwin(_raw().rstrip("\n"))
    assert sum(moved.values()) == DISPLACED


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء.

ج٤ مرّ وتعليلُه «الحالةُ تحمل قانونَ الابتداء» **مؤيَّدٌ بشواذّه المسمّاة**:
فواتحُ السور تُتهجّى أسماءَ حروف، ولامُ الأمر بعد «ثُمَّ» تُبتدأ في الوصل بما
قبلها. وج٥ مرّ صفرًا وشواهدُه العاريةُ الثلاثة فواتح.
"""
