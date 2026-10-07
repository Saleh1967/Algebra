"""تنفيذُ شرط الإبطال الرابع: أربعةٌ تُعيد القسمةَ، ومانعُ التعيين بنيويّ.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ فضاءَ الوصف والقسمةَ الهدفَ مقروءان من
القوالب المُودَعة لا مكتوبَين، وأنّ أربعةً من ثمانيةِ مرشّحاتٍ تُعيد القسمةَ
بلا خطأٍ في قالب، وأنّ ثلاثةً منها لا تعدّ السواكنَ فالشرطُ الرابعُ **فَعَل**،
وأنّ الأربعةَ الساقطةَ تسقط بمواضعَ مُسمّاة، وأنّ `s` و`μ` دالّةٌ واحدةٌ على
مدًى أوسعَ من القوالب، وأنّ الموضعَ الفاصلَ بدايتان وأنّ اللغةَ ترخّص واحدةً
فالمانعُ بنيويّ، وأنّ التخصيصَ لا يتعيّن مع بقاء القسمة، وأنّ حكمًا يخالف
مواضعَ اختلافه يُرَدّ.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.closure_identifiability import (
    CANDIDATES,
    FALSIFIER_INDEX,
    SEPARATING_ONSET,
    CandidateVerdict,
    SeparatingConfiguration,
    derive_candidate_verdicts,
    derive_identifiability,
    derive_separating_configuration,
    feature_space,
    s_and_mu_agree_everywhere,
    target_partition,
)
from alghanem.arabic.closure_window_reduction import (
    TEMPLATES,
    WHAT_WOULD_FALSIFY_THE_REDUCTION,
)
from alghanem.arabic.slgae_deposit import SlgaeDepositError


def test_the_space_and_the_target_are_read_from_the_templates() -> None:
    """فضاءُ الوصف ستُّ نقاطٍ، والقسمةُ الهدفُ مقروءةٌ بالتشغيل لا مكتوبة."""

    space = feature_space()
    target = target_partition()

    assert len(space) == 6
    assert space == ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1))
    assert set(target) == {row.name for row in TEMPLATES}
    assert sum(target.values()) == 3


def test_four_of_eight_candidates_reproduce_the_partition() -> None:
    """أربعةٌ من ثمانيةٍ تُعيد القسمةَ بلا خطأٍ في قالبٍ واحد."""

    verdicts = derive_candidate_verdicts()

    assert len(verdicts) == len(CANDIDATES) == 8
    assert sum(1 for item in verdicts if item.reproduces_partition) == 4


def test_the_fourth_falsifier_fires() -> None:
    """ثلاثةٌ من المُعيدةِ لا تعدّ السواكن، فالشرطُ الرابعُ فَعَل."""

    reading = derive_identifiability()

    assert reading.falsifier_text == WHAT_WOULD_FALSIFY_THE_REDUCTION[FALSIFIER_INDEX]
    assert len(reading.reproducing) == 4
    assert len(reading.reproducing_without_counting) == 3
    assert reading.falsifier_fires


def test_the_specialization_is_not_identifiable_but_the_partition_stands() -> None:
    """التخصيصُ لا يتعيّن، والقسمةُ قائمةٌ على حالها."""

    reading = derive_identifiability()
    target = target_partition()

    assert not reading.specialization_is_identifiable
    assert [name for name, closes in target.items() if closes] == [
        "CV",
        "CVV",
        "CVC",
    ]


def test_the_failing_candidates_fail_at_named_templates() -> None:
    """كلُّ ساقطٍ يسقط بموضعٍ مُسمًّى، ولا يسقط بلا موضع."""

    failing = [
        item for item in derive_candidate_verdicts() if not item.reproduces_partition
    ]

    assert len(failing) == 4
    assert all(item.divergences for item in failing)
    by_name = {item.name: item.divergences for item in failing}
    assert by_name["حدُّ الإغلاق وحدَه"] == ("CVVC",)
    assert by_name["قِصَرُ النواة وحدَه"] == ("CVV", "CVCC")


def test_s_and_mu_are_one_function_beyond_the_six() -> None:
    """`μ = s + 1`، فتتّفقان على مدًى أوسعَ من القوالب لا على عيّنةٍ منها."""

    assert s_and_mu_agree_everywhere()
    assert s_and_mu_agree_everywhere(max_coda=40)

    with pytest.raises(SlgaeDepositError, match="لا يقلّ عن اثنين"):
        s_and_mu_agree_everywhere(max_coda=1)


def test_the_separating_configuration_is_forbidden_by_the_edge_law() -> None:
    """بدايتان تفصلان المقياسَين، واللغةُ ترخّص واحدةً؛ فالمانعُ بنيويّ."""

    configuration = derive_separating_configuration()

    assert configuration.onset_count == SEPARATING_ONSET == 2
    assert configuration.licensed_onset_count == 1
    assert configuration.separates
    assert "قانونُ الحواف" in configuration.why_unavailable

    with pytest.raises(SlgaeDepositError, match="لا يكون متعذّرًا"):
        SeparatingConfiguration(
            onset_count=1,
            separates=True,
            why_unavailable="سبب",
            licensed_onset_count=1,
        )


def test_a_verdict_contradicting_its_divergences_is_refused() -> None:
    """مرشَّحٌ «يُعيد القسمة» مع اختلافٍ مسجَّلٍ حكمٌ لا يُشتَقّ، فيُرَدّ."""

    with pytest.raises(SlgaeDepositError, match="يخالف مواضعَ اختلافه"):
        CandidateVerdict(
            name="مرشَّح",
            counts_consonants=True,
            reproduces_partition=True,
            divergences=("CVC",),
        )
