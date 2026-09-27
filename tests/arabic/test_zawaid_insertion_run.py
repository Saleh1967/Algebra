"""شُغِّل ختمُ `113fc280…`: **سقطت الثلاثة — والأداةُ قاست المصادفةَ لا الزيادة**.

`THE_ADDED_LETTERS_LOOK_RANDOM`: الصورُ ١٤٬٦٢٠، والأزواجُ ٥٣٬٦٤٢، والحروفُ
المُضافة ١١٩٬٤٩٠. ز١ **سقط**: من التسعة أو ب ف ك أو تكريرًا ٠٫٨١٤٨ — وخطُّ
الأساس المكتوب قبل العدّ ٠٫٨١٢٥. فسقط معه: «فالزيادةُ لا تنحصر في
«سألتمونيها»» — **بقدر ما قاسته هذه الأداة**.

`THE_ATTACHED_ARE_NOT_ONLY_AT_THE_EDGE`: ز٢ **سقط**: ب ف ك على الطرف ٠٫٨٤٢٨.
فسقط معه: «فهي تدخل الوزنَ كما تدخله التسعة» — بالقيد نفسه.

`AND_THE_RATES_DO_NOT_SEPARATE`: ز٣ **سقط**: أدنى معدّلٍ في التسعة (اللام)
٠٫٦٢١٦، وأعلى معدّلٍ في غيرها (الصاد) ١٫٤٤٥٥. فسقط معه: «فذلك الحرفُ يعمل
عملَ الزوائد».

`WHY — AFTER_THE_RUN`: **تشخيصٌ لا حكم**. أكثرُ الأزواج **مصادفةٌ بين جذرين**
لا اشتقاق: «بورا ⊂ ثبورا»، «طريا ⊂ طريقا»، «يرون ⊂ يضرون». وكلّما قلّت
المصادفةُ صعدت الإشارة: بحرفٍ مُضافٍ واحد وقصيرةٍ من خمسة أحرفٍ فأكثر
(**٣٬٦٤٠** زوجًا) يصير النصيبُ **٠٫٩٢٩٩**. ومعدّلُ ز٣ مَعيبٌ بطبعه: حرفٌ كثيرٌ
أصلًا كاللام والنون والألف يُقسَم زائدُه على كثرته فيبدو أقلَّ زيادةً من حرفٍ
نادر. **فالأزواجُ بالتضمين لا تعزل الاشتقاقَ عن المصادفة**، واختبارُ
«سألتمونيها» حرفًا حرفًا يحتاج ما يعيّن الجذر — **جدولَ الجذور**، وهو غيرُ
مُودَعٍ في الشجرة.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_zawaid_insertion_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_zawaid_insertion.py"

pytestmark = requires_corpus

FORMS, PAIRS, ADDED = 14_620, 53_642, 119_490
GOOD = 97_356
BASELINE = 0.8125
SHARE = 0.8148
ATTACHED, ON_EDGE = 12_345, 10_404
EDGE_SHARE = 0.8428
LOWEST_ZAWAID, HIGHEST_OTHER = 0.6216, 1.4455
ONE_ADDED_LONG_PAIRS = 3_640
ONE_ADDED_LONG_SHARE = 0.9299
QUOTED_FALLEN = {
    "ز١": "فالزيادةُ لا تنحصر في «سألتمونيها»",
    "ز٢": "فهي تدخل الوزنَ كما تدخله التسعة",
    "ز٣": "فذلك الحرفُ يعمل عملَ الزوائد",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_zawaid_insertion", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _measures() -> dict[str, object]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().measures(text)  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("113fc280")


def test_the_added_letters_look_like_the_baseline() -> None:
    """ز١ سقط: ٠٫٨١٤٨ وخطُّ الأساس ٠٫٨١٢٥."""

    m = _measures()
    assert (m["forms"], m["pairs"], m["added"]) == (FORMS, PAIRS, ADDED)
    assert m["good"] == GOOD
    share = Fraction(GOOD, ADDED)
    assert abs(float(share) - SHARE) < 5e-5
    assert SHARE - BASELINE < 0.01
    first = next(one for one in PREDICTIONS if one.identifier == "ز١")
    assert first.verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ز١"] in first.falsifies


def test_the_attached_letters_are_not_only_at_the_edge() -> None:
    """ز٢ سقط: ٠٫٨٤٢٨."""

    m = _measures()
    assert (m["on_edge"], m["attached"]) == (ON_EDGE, ATTACHED)
    share = Fraction(ON_EDGE, ATTACHED)
    assert abs(float(share) - EDGE_SHARE) < 5e-5
    second = next(one for one in PREDICTIONS if one.identifier == "ز٢")
    assert second.verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ز٢"] in second.falsifies


def test_the_rates_do_not_separate_the_nine() -> None:
    """ز٣ سقط: أدنى التسعة ٠٫٦٢١٦ وأعلى غيرها ١٫٤٤٥٥."""

    m = _measures()
    assert abs(m["lowest_zawaid"] - LOWEST_ZAWAID) < 5e-5
    assert abs(m["highest_other"] - HIGHEST_OTHER) < 5e-5
    gap = Fraction(m["lowest_zawaid"]).limit_denominator(10**9) - Fraction(
        m["highest_other"]
    ).limit_denominator(10**9)
    third = next(one for one in PREDICTIONS if one.identifier == "ز٣")
    assert third.verdict(gap) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ز٣"] in third.falsifies


def test_the_signal_rises_as_coincidence_falls() -> None:
    """تشخيصًا: بحرفٍ مُضافٍ واحد وقصيرةٍ من خمسة يصير النصيبُ ٠٫٩٢٩٩."""

    reader = _reader()
    matched = _measures()["matched"]
    chosen = [one for one in matched if len(one[2]) == 1 and len(one[0]) >= 5]
    assert len(chosen) == ONE_ADDED_LONG_PAIRS
    added = reader.added_letters(chosen)
    kept = reader.ZAWAID | reader.ATTACHED
    good = sum(1 for letter, _, _, repeated in added if letter in kept or repeated)
    assert abs(good / len(added) - ONE_ADDED_LONG_SHARE) < 5e-5


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء؛ فلم يمرّ شرط."""
