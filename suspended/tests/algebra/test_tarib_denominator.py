"""المقامُ وصل خمسةً: حكمُ التسجيل على نفسه قبل أن يُقاس رقمٌ واحد.

**ما وصل**: قائمةُ المعرَّبات بمقامٍ مُعلَنٍ في رأسها. وبعد إخراج الأعلام
**بنصّ التسجيل المختوم** يبقى نطاقُ الاختبار **خمسةَ ألفاظ**. والخلافيّون
مكتوبون صفوفًا خارج العدّ لا محذوفين.

`THE_SEAL_JUDGES_ITS_OWN_MATERIAL_BEFORE_ANY_NUMBER`: وشرطُ ع٤ في التسجيل
`3a7ccdc9…` يقول: «عددُ الأنواع في أصغر خانةٍ من خانات المقارنة ≥ ١٢»، وأنّ
دونه **تُعلَن القراءةُ ضعيفةَ الشهادة**. وخمسةٌ مقسومةً كفّتين أكبرُ ما
تعطيه أصغرُ خانةٍ **اثنان**. فع٤ **ساقطٌ بالمقام وحدَه**، مشتقًّا من
`Prediction.verdict` لا مكتوبًا بيد، وقبل أن يُقاس بتٌّ واحد. فالسؤال «أخمسةٌ
مقامٌ يحمل فصلًا؟» **مُجابٌ داخلَ الختم**، ولم يكن التسجيلُ ليُسأل لولا أنّه
كُتِب قبل المادّة.

`TWO_FLOORS_NOT_ONE_AND_THE_HIGHER_GOVERNS`: وأرضيّةُ ١/٢٠٠١ المسجَّلةُ
أرضيّةُ **آلة**. وللمادّة أرضيّةٌ ثانية: إن كان الصفريُّ تبديلَ الوسمين على
الخمسة فقيمُ `p` مضروبةٌ في `1/C(5, k)`، وأحسنُها **١/١٠**. فالتكرارُ ألفان
يعيد زيارةَ عشرة تراتيبَ لا غير. وأصغرُ مادّةٍ تبلغ ١/٢٠٠١ **أربعةَ عشرَ
لفظًا** بقسمةٍ متوازنة، وأصغرُ ما يبلغ ٠٫٠٥ **ستّة**. فلفظٌ واحدٌ زائدٌ يبدّل
صنفَ الحكم — وذلك خبرٌ عن السؤال لا عن العربيّة.

`THE_SEAL_NAMED_THE_MATCHING_VARIABLE_AND_LEFT_THE_RANDOMISATION_UNIT_BARE`:
وعيبٌ في تسجيلي أنا يُسمّى ههنا. عدَّ التسجيلُ متغيّراتِ المطابقة ثلاثةً
وأمر بنشر الثلاثة، **ولم يُعدِّد وحدةَ العشوَنة**: أتُبدَّل الوسومُ على
الخمسة، أم تُسحَب نظائرُ مطابقةٌ من خارجها؟ وهما أرضيّتان مختلفتان كما
أعلاه، فالرقمُ غيرُ معيَّنٍ بالختم وحدَه. وعلاجُه علاجُ أخيه المسجَّل: تُعدَّد
الوحدتان وتُشغَّل ستُّ خاناتٍ ويُنشَر الستّ — لا تُختار واحدةٌ بعد رؤيتها.
وهذا **تعدادُ مجالٍ أُغفِل**، لا تبديلُ حدٍّ بعد النظر؛ والبصمةُ شاهدةٌ إذ
لم يُمَسَّ حدٌّ واحد.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from test_provenance import MUSHAF
from test_tarib_preregistration import MATCHING_VARIABLES, PREDICTIONS, REPLICATES

from algebra.attainability import (
    AttainabilityError,
    governing_floor,
    label_permutation_floor,
    permutation_floor,
    smallest_material_for,
)
from algebra.provenance import Reading
from algebra.results import Vacancy
from algebra.signified import Verdict

# ما وصل في رأس القائمة: نطاقُ الاختبار بعد إخراج الأعلام بنصّ التسجيل
IN_SCOPE: tuple[str, ...] = ("سجّيل", "قسطاس", "سربيل", "القطر", "التابوت")

DISPUTED_OUT: tuple[str, ...] = ("عيسى", "موسى", "هارون")
"""الخلافيّون المكتوبون خارج العدّ؛ والقائمةُ الواصلةُ منقوطةٌ في آخرها.

فهؤلاء **حدٌّ أدنى محقَّق** لا حصرًا: ما بعد النقاط لم يصلني، ولا يُعَدُّ
ما لم يُقرَأ. والمقامُ خمسةٌ على كلّ حال، إذ العدُّ في النطاق لا خارجه.
"""

DENOMINATOR = len(IN_SCOPE)
SMALLEST_CELL_CONDITION = PREDICTIONS[3]
SEALED_FLOOR = permutation_floor(REPLICATES)


def _smallest_cell(marked: int) -> int:
    return min(marked, DENOMINATOR - marked)


def test_the_delivered_denominator_is_five_and_the_excluded_are_written_rows() -> None:
    """خمسةٌ في النطاق، والخارجون مكتوبون — والحذفُ غيرُ الإخراج المُعلَن."""

    assert DENOMINATOR == 5
    assert len(set(IN_SCOPE)) == DENOMINATOR
    assert not set(IN_SCOPE) & set(DISPUTED_OUT)
    assert len(DISPUTED_OUT) >= 3  # حدٌّ أدنى: القائمةُ الواصلةُ منقوطةُ الآخر


def test_the_fourth_sealed_condition_is_decided_by_the_denominator_alone() -> None:
    """ع٤ يسقط تحت كلّ قسمةٍ ممكنة: أكبرُ أصغرِ خانةٍ اثنان، والحدُّ اثنا عشر.

    والحكمُ مُشتَقٌّ من `Prediction.verdict`، ولا رقمَ مقيسٌ دخل فيه.
    """

    assert SMALLEST_CELL_CONDITION.identifier.startswith("ع٤")
    assert SMALLEST_CELL_CONDITION.threshold == Fraction(12)

    cells = {marked: _smallest_cell(marked) for marked in range(1, DENOMINATOR)}
    assert max(cells.values()) == 2
    for observed in cells.values():
        verdict = SMALLEST_CELL_CONDITION.verdict(Fraction(observed))
        assert verdict is Verdict.FALSIFIED

    # ونصُّ ما يُسقِطه ع٤ ليس الدعوى بل قابليّةَ القراءة
    assert "قابليّةَ القراءة" in SMALLEST_CELL_CONDITION.falsifies
    assert "ضعيفَ الشهادة" in SMALLEST_CELL_CONDITION.falsifies


def test_an_empty_pan_is_a_vacancy_not_a_high_floor() -> None:
    """قسمتان من ستٍّ تُفرِغان كفّةً: لا اختبارَ فيهما، والخلوُّ يُسمّى جنسَه."""

    for marked in (0, DENOMINATOR):
        with pytest.raises(AttainabilityError):
            label_permutation_floor(marked, DENOMINATOR)
        assert Vacancy.UNREACHABLE.value == "لا تُبلَغ بما في اليد"

    splits = range(0, DENOMINATOR + 1)
    empty = [one for one in splits if one in (0, DENOMINATOR)]
    assert len(list(splits)) == 6 and len(empty) == 2


def test_the_material_floor_governs_and_the_sealed_floor_is_unreachable() -> None:
    """أحسنُ أرضيّةٍ على خمسةٍ ١/١٠، وهي أعلى من ١/٢٠٠١ بمئتي ضعفٍ وزيادة."""

    floors = {
        marked: label_permutation_floor(marked, DENOMINATOR)
        for marked in range(1, DENOMINATOR)
    }
    assert floors == {
        1: Fraction(1, 5),
        2: Fraction(1, 10),
        3: Fraction(1, 10),
        4: Fraction(1, 5),
    }
    best = min(floors.values())
    assert best == Fraction(1, 10)

    assert SEALED_FLOOR == Fraction(1, 2_001)
    assert best / SEALED_FLOOR == Fraction(2_001, 10)
    for marked in range(1, DENOMINATOR):
        assert governing_floor(marked, DENOMINATOR, REPLICATES) == floors[marked]


def test_one_more_word_changes_the_class_and_fourteen_reach_the_sealed_floor() -> None:
    """ستّةٌ تبلغ ٠٫٠٥، وأربعةَ عشرَ تبلغ ١/٢٠٠١ — والمادّةُ وحدَها تُصلِحها."""

    assert smallest_material_for(Fraction(1, 20)) == 6
    assert label_permutation_floor(3, 6) == Fraction(1, 20)

    assert smallest_material_for(SEALED_FLOOR) == 14
    assert label_permutation_floor(7, 14) <= SEALED_FLOOR
    assert label_permutation_floor(6, 13) > SEALED_FLOOR

    # ورفعُ التكرار لا يمسّ شيئًا من هذا: المادّةُ هي القيد
    assert governing_floor(2, DENOMINATOR, 1_000_000) == Fraction(1, 10)


def test_the_randomisation_unit_was_never_enumerated_in_the_seal() -> None:
    """ثلاثةُ متغيّراتِ مطابقةٍ معدودة، ووحدةُ العشوَنة غيرُ معدودة — فتُعدَّد.

    وحاصلُ التعدادين ستُّ خاناتٍ تُنشَر كلُّها، كما نُشِرت الثلاثُ قبلها.
    """

    assert len(MATCHING_VARIABLES) == 3
    randomisation_units = ("تبديلُ الوسمين على الخمسة", "سحبُ نظائرَ من خارجها")
    assert len(set(randomisation_units)) == 2

    cells = len(MATCHING_VARIABLES) * len(randomisation_units)
    assert cells == 6

    # ولا خانةَ منها تُختار بعد رؤيتها: الجداءُ كاملٌ أو لا يُقرأ
    sealed_statistics = {one.statistic for one in PREDICTIONS[:3]}
    assert len(sealed_statistics) == 3
    assert all("مطابق" in one for one in sealed_statistics)


def test_the_first_three_conditions_remain_runnable_under_the_weak_reading() -> None:
    """ع١–ع٣ تُشغَّل وتُنشَر بأرضيّتها؛ وسقوطُ ع٤ يحكم قراءتَها لا تشغيلَها."""

    runnable = [one for one in PREDICTIONS[:3] if "مطابق" in one.statistic]
    assert len(runnable) == 3

    # وحدُّ ع٣ أدنى الثلاثة، وهو وحدَه يحمل الدعوى بتمامها
    assert runnable[2].threshold == Fraction(20, 100)
    assert "بتمامها" in runnable[2].falsifies

    # ويُنشَر مع كلٍّ منها الأرضيّةُ الحاكمةُ لا المسجَّلةُ وحدَها
    assert governing_floor(2, DENOMINATOR, REPLICATES) > SEALED_FLOOR


def test_the_proposed_stamp_names_a_statistic_the_seal_does_not() -> None:
    """الختمُ المقترَح «مقاسُ التقارب الصوتيّ»، والمسجَّلُ «بتٌّ لكلّ وحدة».

    وهما مقياسان لا مقياس، فالرقمُ الخارجُ تحت الأوّل ليس الرقمَ المختومَ
    تحت الثاني. ولا يُصلِح ذلك تبديلُ الختم بعد الخروج، بل تسميةُ المقياس
    قبله — وهو مُسمًّى في التسجيل سلفًا.
    """

    sealed_unit = "بالبتّ للوحدة"
    proposed_unit = "مقاسُ التقارب الصوتيّ"
    assert sealed_unit in PREDICTIONS[0].statistic
    assert proposed_unit not in PREDICTIONS[0].statistic
    assert sealed_unit != proposed_unit

    # ولا يُختَم رقمٌ قبل أن يوجد: `Reading` لا تُبنى بلا قيمة
    with pytest.raises(TypeError):
        Reading(  # type: ignore[call-arg]
            statistic=PREDICTIONS[0].statistic, unit=sealed_unit, corpus=MUSHAF
        )
