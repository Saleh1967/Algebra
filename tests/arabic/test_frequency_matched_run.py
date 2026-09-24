"""شُغِّل `5e3656d5…`: **و٣ سقط** — فالصفريُّ سُمِّي مطابقًا ولم يُطابق.

**والختمُ نفسُه نصّ على هذا الباب**: و٣ يُسقِط «قابليّةَ قراءة و١ وو٢».
فمئينُ G1 ٠٫٠١١ ومئينُ G5 ٠٫٩٧٨ — وكلاهما في الجهة المكتوبة له — **ولا
يُقرآن**؛ إذ الآلةُ التي أخرجتهما مفحوصةٌ بشرطها فسقطت. ومن قرأ رقمًا من
صفريٍّ ثبت عطلُه فقد **أخفى العطلَ باسم إصلاحه**، وذلك نصُّ بند و٣.

`THE_MATCHING_FAILED_ON_ONE_GROUP_AND_THE_CAUSE_IS_ARITHMETIC_NOT_LUCK`:
والسببُ يُعيَّن بدقّةٍ لا يُوصَف: G3 «طرفيّة» حرفان — ل ون — **وكلاهما في
الطبقة الأولى**، وهي سبعةُ حروفٍ رتبُها ٠…٦. ورتبتاهما ١ و٢، فمتوسّطُهما
١٫٥؛ ومتوسّطُ رتبةِ زوجٍ يُسحَب من السبعة **٣٫٠** بالضبط. فالفرقُ **١٫٥
حتميٌّ بالحساب**، والحدُّ المختومُ ١. والمقيسُ ١٫٥٢٠٠ — أي ١٫٥ وضوضاءُ
السحب.

`MORE_DRAWS_WOULD_MOVE_IT_TOWARDS_THE_FAILURE_NOT_AWAY_FROM_IT`: فليست
علّتُه قلّةَ السحبات: زيادتُها تُقرِّب المقيسَ من ١٫٥ لا من ١. وطبقةٌ من
سبعةِ حروفٍ **أخشنُ من أن تُطابِق مجموعةً من حرفين**؛ والمطابقةُ في الاسم
لا في العدد.

`THE_REPAIR_IS_A_SIXTH_SEAL_NOT_A_REREADING_OF_THIS_ONE`: والإصلاحُ
معلومٌ — طبقاتٌ أدقُّ، أو إخراجُ مجموعةٍ تستنفد طبقتَها — **ولا يُكتَب
ههنا**. فمن أصلح الآلةَ بعد رؤية أرقامها ثمّ قرأ الأرقامَ نفسَها فقد اختار
الإصلاحَ بها. فيُسجَّل السقوطُ كما خرج، ويُبنى السادسُ **قبلَ** تشغيله.

`AND_WHAT_IS_DESCRIBED_HERE_IS_OUTSIDE_EVERY_SEAL`: وما دون الأحكام —
الطبقاتُ، والتشابهاتُ، وترتيبُ المئينات — **وصفٌ مُعلَنٌ خارجَ كلّ ختم**،
يُنشَر ولا يُحتَجّ به حكمًا.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from algebra.signified import Prediction, Verdict

REPOSITORY = Path(__file__).resolve().parents[2]
CORPUS = REPOSITORY / "corpora" / "quran-simple-enhanced.txt"

pytestmark = pytest.mark.skipif(
    not CORPUS.is_file(),
    reason="بايتاتُ المدوّنة المُجمَّدة غيرُ مستقبَلةٍ في هذه الشجرة",
)

MATCHED_SEAL = "5e3656d53a1dceed7a151d1067813087e5b6f14faed6635c51729f8d1e5c4e27"

# الطبقاتُ الأربعُ كما خرجت، من الأشيع لاحقًا؛ سبعةٌ في كلٍّ
STRATA: tuple[str, ...] = ("النميوه", "ربتكعفق", "سدذحجخش", "صضزثطغظ")

# (المجموعة، تشابهُها، مئينُها المطابق، طبقاتُها، فرقُ متوسّط الرتبة)
MEASURED: tuple[tuple[str, Fraction, Fraction, dict[int, int], Fraction], ...] = (
    (
        "G1 حلق",
        Fraction(5_792, 10_000),
        Fraction(11, 1_000),
        {0: 2, 1: 1, 2: 2, 3: 1},
        Fraction(8_248, 10_000),
    ),
    (
        "G2 جاحظيّة",
        Fraction(6_853, 10_000),
        Fraction(463, 1_000),
        {0: 1, 2: 2, 3: 1},
        Fraction(7_494, 10_000),
    ),
    (
        "G3 طرفيّة",
        Fraction(8_561, 10_000),
        Fraction(855, 1_000),
        {0: 2},
        Fraction(15_200, 10_000),
    ),
    (
        "G5 الباقي",
        Fraction(7_482, 10_000),
        Fraction(978, 1_000),
        {0: 2, 1: 5, 2: 3, 3: 5},
        Fraction(1_279, 10_000),
    ),
)

WORST_RANK_GAP = Fraction(15_200, 10_000)
DRAWS = 2_000

# رتبتا ل ون داخلَ الطبقة الأولى، ومتوسّطُ رتبةِ زوجٍ من سبعةٍ رتبُها ٠…٦
EDGE_RANKS = (1, 2)
STRATUM_SIZE = 7
EXPECTED_STRUCTURAL_GAP = Fraction(3, 2)


def _prediction(identifier: str) -> Prediction:
    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    name = "test_frequency_matched_preregistration"
    spec = importlib.util.spec_from_file_location(name, path / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    assert module.MATCHED_SEAL == MATCHED_SEAL
    for one in module.PREDICTIONS:
        if one.identifier.startswith(identifier):
            found: Prediction = one
            return found
    raise AssertionError(identifier)


def _percentile(name: str) -> Fraction:
    for group, _, percentile, _, _ in MEASURED:
        if group.startswith(name):
            return percentile
    raise AssertionError(name)


def test_the_matching_condition_fell() -> None:
    """و٣ سقط: ١٫٥٢٠٠ فوق الحدّ ١ — والصفريُّ لم يُطابق."""

    third = _prediction("و٣")
    assert third.verdict(WORST_RANK_GAP) is Verdict.FALSIFIED
    assert WORST_RANK_GAP > Fraction(1)
    assert "يُخفي العطلَ باسم إصلاحه" in third.falsifies


def test_the_two_directions_land_where_written_and_still_are_not_readable() -> None:
    """و١ ٠٫٠١١ وو٢ ٠٫٩٧٨ — في جهتيهما، **ولا يُقرآن** بنصّ و٣."""

    first, second = _prediction("و١"), _prediction("و٢")
    assert first.verdict(_percentile("G1")) is Verdict.MET
    assert second.verdict(_percentile("G5")) is Verdict.MET

    # وما أسقطه و٣ هو **قابليّةُ قراءتهما**، لا اتّجاهُهما
    assert "قابليّةَ قراءة و١ وو٢" in _prediction("و٣").falsifies
    readable = _prediction("و٣").verdict(WORST_RANK_GAP) is Verdict.MET
    assert not readable


def test_the_fourth_condition_was_met_and_does_not_rescue_the_third() -> None:
    """و٤ ألفا سحبةٍ متحقّق — وكثرةُ السحب لا تُصلِح مطابقةً مُعطَّلة."""

    assert _prediction("و٤").verdict(Fraction(DRAWS)) is Verdict.MET
    assert DRAWS == 2_000


def test_the_gap_is_structural_arithmetic_not_a_shortage_of_draws() -> None:
    """١٫٥ فرقٌ حتميّ: زوجٌ رتبتاه ١ و٢ من سبعةٍ متوسّطُها ٣٫٠."""

    drawn_mean = Fraction(sum(range(STRATUM_SIZE)), STRATUM_SIZE)
    observed_mean = Fraction(sum(EDGE_RANKS), len(EDGE_RANKS))
    assert drawn_mean == Fraction(3)
    assert observed_mean == Fraction(3, 2)
    assert drawn_mean - observed_mean == EXPECTED_STRUCTURAL_GAP

    # والمقيسُ ١٫٥٢٠٠: هو الفرقُ الحتميُّ وضوضاءُ السحب، ولا سبيلَ به دون ١
    assert abs(WORST_RANK_GAP - EXPECTED_STRUCTURAL_GAP) < Fraction(5, 100)
    assert EXPECTED_STRUCTURAL_GAP > _prediction("و٣").threshold


def test_the_group_that_broke_it_exhausts_its_own_stratum_class() -> None:
    """G3 حرفان كلاهما في طبقةٍ واحدةٍ — أخشنُ حالٍ للمطابقة، وأكبرُ فرق."""

    by_gap = sorted(MEASURED, key=lambda row: row[4])
    assert by_gap[-1][0].startswith("G3")
    assert by_gap[0][0].startswith("G5")

    _, _, _, occupancy, _ = by_gap[-1]
    assert occupancy == {0: 2} and sum(occupancy.values()) == 2
    # وأوسعُ المجموعات توزيعًا على الطبقات أصغرُها فرقًا
    assert len(by_gap[0][3]) == 4


def test_the_strata_are_seven_apiece_and_partition_the_alphabet() -> None:
    """أربعُ طبقاتٍ سبعًا سبعًا، لا اشتراكَ ولا نقص — والعدّ مفحوص."""

    assert len(STRATA) == 4
    assert all(len(one) == 7 for one in STRATA)
    letters = "".join(STRATA)
    assert len(letters) == 28 == len(set(letters))
    assert set(letters) == set("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
    assert STRATA[0][0] == "ا"  # أشيعُها لاحقًا


def test_the_order_of_the_percentiles_is_published_as_description_only() -> None:
    """G1 أدنى المئينات وG5 أعلاها — وصفٌ يُنشَر ولا يُحتَجّ به حكمًا."""

    ordered = sorted(MEASURED, key=lambda row: row[2])
    assert ordered[0][0].startswith("G1")
    assert ordered[-1][0].startswith("G5")

    # والتشابهُ نفسُه يرتّب غيرَ هذا الترتيب — فالمئينُ مضبوطٌ بالحجم والطبقة
    by_similarity = sorted(MEASURED, key=lambda row: row[1])
    assert by_similarity[0][0].startswith("G1")
    assert by_similarity[-1][0].startswith("G3")


def test_the_repair_is_not_written_here() -> None:
    """الإصلاحُ يُختَم سادسًا قبل تشغيله؛ وهذا الملفُّ سجلُّ سقوطٍ لا تصحيح."""

    reserved = "طبقاتٌ أدقُّ، أو إخراجُ مجموعةٍ تستنفد طبقتَها"
    assert __doc__ is not None and reserved in __doc__
    # ولا يُعاد تفسيرُ بندٍ بعد رؤية رقمه: الحدُّ يبقى ١ كما خُتِم
    assert _prediction("و٣").threshold == Fraction(1)
