"""شُغِّل ختمُ `945fd806…` بترتيبه كما خُتِم: **خمسةٌ من سبعة — وسقط ج٣ وج٥**.

**وعطلُه مكتوبٌ قبل العدّ** في الختم الثاني `34176d22…`: تقديمُ المدّ على
ألف الوصل يُسقِط لامَ «وَال/فَال/كَال» في الباقي. **فهذا التشغيلُ يُنشَر
بعلّته، لا يُستبدَل**، وحكمُ الختم المصحَّح في `test_surface_depth_refined_run`.

`THE_FLOOR_HOLDS`: لا سطرَ من ٦٬٢٣٦ يفوت التقشيرَ إلى الـ١١٢ والعودةَ منه
بايتةً بايتة (ج١)، والأصنافُ مع الباقي **تنغلق** على العُري ٨٠٬٤٧٧ بلا فجوة
(ج٢).

`AND_THE_DEFECT_SHOWS_EXACTLY_WHERE_I_SAID_IT_WOULD`: الباقي **٣٬٢٤٨**
(٠٫٠٤٠٤)، واللامُ فيه **١٬١٤٣** — و«وَاللَّهُ» وحدَها **٢٣٩** موضعًا. وفي
المصحَّح نزلت اللامُ إلى ٦٣٦ وخرجت «وَاللَّهُ» من الباقي كلَّه.

`AND_BOTH_FALLEN_CONDITIONS_FELL_FOR_ONE_REASON_FOUND_AFTER_LOOKING`: ج٣ سقط
(حدّي ٠٫٠٢)، وج٥ سقط: **٣٢٩** من **١٬٦٥٧** ميمًا عاريةً يليها غيرُ باءٍ ولا
ميم (٠٫١٩٨٦). والعلّةُ — **بعد النظر** — واحدةٌ فيهما: تنوينُ النصب في هذا
المجمَّد مكتوبٌ على الألف بعد الحرف، فيعرى الحرف. وتفصيلُها في التشغيل
المصحَّح.

`THE_OTHER_THREE_HELD`: ج٤ صفرٌ من **٥٬٦٠٢** نونًا عارية، وج٦ **١٣** من
**٥٬٠٧٣** لامًا، وج٧ صفرٌ من **٥٬٠٦٠**.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_surface_depth_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_surface_depth.py"

pytestmark = requires_corpus

ALPHABET = 112
"""الوحداتُ التي يُصعَد منها: ثمانيةٌ وعشرون حرفًا في أربع حالات."""
REFINED_SEAL_PREFIX = "34176d22"
"""الختمُ المصحَّح الذي كُتب عطلُ هذا فيه قبل العدّ."""

LINES = 6_236
BARE = 80_477
CLASSES = {
    "س١": 48_086,
    "س٢": 11_737,
    "س٣": 5_060,
    "س٤": 7_277,
    "س٥": 3_558,
    "س٦": 1_511,
}
RESIDUE = 3_248
RESIDUE_SHARE = 0.0404
LAM_IN_RESIDUE = 1_143
LAM_IN_REFINED_RESIDUE = 636
WA_ALLAHU_IN_RESIDUE = 239
WA_ALLAHU = "وَاللَّهُ"
"""«وَاللَّهُ» ببايتات المجمَّد: الشدّةُ قبل الفتحة."""

NUN = (0, 5_602)
MIM = (329, 1_657)
MIM_SHARE = 0.1986
LAM_BARE = (13, 5_073)
LAM_MARKED = (0, 5_060)

QUOTED_FALLEN = {
    "ج٣": "فالأنماطُ الستّةُ لا تستوعب الظاهرة",
    "ج٥": "إن عريت الميمُ قبل غير الباء والميم",
}
"""ما عُلِّق على سقوط ج٣ وج٥ بنصّ الختم — يسقط معهما عند موضع السقوط."""


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_surface_depth", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _reading() -> object:
    reader = _reader()
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return reader.read(text, reader.FIRST, reader.unrebuilt_lines(text))


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("945fd806")


def test_the_floor_rebuilds_and_the_classes_close() -> None:
    """ج١ وج٢ صمدا: لا سطرَ يفوت التقشير، ولا عارٍ يفوت القسمة."""

    reading = _reading()
    first = next(one for one in PREDICTIONS if one.identifier == "ج١")
    second = next(one for one in PREDICTIONS if one.identifier == "ج٢")
    assert reading.lines == LINES  # type: ignore[attr-defined]
    assert ALPHABET == 28 * 4
    assert reading.bare == BARE  # type: ignore[attr-defined]
    assert first.verdict(Fraction(reading.unrebuilt)) is Verdict.MET  # type: ignore[attr-defined]
    assert second.verdict(Fraction(reading.closure_gap)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_residue_fell_above_one_in_fifty() -> None:
    """ج٣ سقط: ٣٬٢٤٨ من ٨٠٬٤٧٧ — والباقي كما خُتِم لا كما يُحَبّ."""

    reading = _reading()
    third = next(one for one in PREDICTIONS if one.identifier == "ج٣")
    assert reading.classes == CLASSES  # type: ignore[attr-defined]
    assert reading.residue == RESIDUE  # type: ignore[attr-defined]
    share = Fraction(RESIDUE, BARE)
    assert abs(float(share) - RESIDUE_SHARE) < 5e-5
    assert third.verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج٣"] in third.falsifies


def test_the_defect_written_before_counting_is_what_the_residue_shows() -> None:
    """اللامُ ١٬١٤٣ في الباقي، و«وَاللَّهُ» ٢٣٩ — ونزلت إلى ٦٣٦ في المصحَّح."""

    reading = _reading()
    lam = dict(reading.residue_letters)["ل"]  # type: ignore[attr-defined]
    assert lam == LAM_IN_RESIDUE
    assert dict(reading.residue_tokens)[WA_ALLAHU] == WA_ALLAHU_IN_RESIDUE  # type: ignore[attr-defined]
    assert LAM_IN_REFINED_RESIDUE < LAM_IN_RESIDUE


def test_the_nun_and_lam_held_and_the_mim_fell() -> None:
    """ج٤ وج٦ وج٧ صمدت؛ ج٥ سقط بـ٣٢٩ من ١٬٦٥٧."""

    reading = _reading()
    fourth = next(one for one in PREDICTIONS if one.identifier == "ج٤")
    fifth = next(one for one in PREDICTIONS if one.identifier == "ج٥")
    sixth = next(one for one in PREDICTIONS if one.identifier == "ج٦")
    seventh = next(one for one in PREDICTIONS if one.identifier == "ج٧")
    nun = reading.nun_throat  # type: ignore[attr-defined]
    mim = reading.mim_other  # type: ignore[attr-defined]
    lam = reading.lam_not_before_shadda  # type: ignore[attr-defined]
    marked = reading.lam_marked_before_shadda  # type: ignore[attr-defined]
    assert (nun.hits, nun.base) == NUN
    assert (mim.hits, mim.base) == MIM
    assert (lam.hits, lam.base) == LAM_BARE
    assert (marked.hits, marked.base) == LAM_MARKED
    assert abs(float(mim.share) - MIM_SHARE) < 5e-5
    assert fourth.verdict(nun.share) is Verdict.MET
    assert fifth.verdict(mim.share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج٥"] in fifth.falsifies
    assert sixth.verdict(lam.share) is Verdict.MET
    assert seventh.verdict(marked.share) is Verdict.MET


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: ج٤ وج٦ وج٧ مؤيَّدةٌ بشواهدها."""
