"""النسخةُ الرابعة: أربعُ بصمات، وجسرٌ بثلاثة مقادير، وجدولٌ يتّزن بتقريبه.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ النسخَ الأربعَ مُودَعةٌ ببصماتٍ
متمايزة، وأنّ جسرَ الحلق ورد بثلاثة مقادير في ثلاثة أقسام، وأنّ الأثرَ ضعُف
والدلالةَ اشتدّت معًا فلزم كِبَرُ العيّنة، وأنّ جدولَ النوافذ يتّزن في
مستوياته الثلاثة داخل مجال تقريبه وأضيقَها المفصلُ الصرفيّ، وأنّ عمودَ «غير
مفسَّر» صفرٌ في الثلاثة، وأنّ بقيّةَ الابتداء تُطابِق مجموعَ حالاتها
المُسمّاة، وأنّ خليّتين في ٥ل صفرٌ تامّ، وأنّ نفيَ الفراكتاليّة وإثباتَها
قسمةٌ لا تناقض — وأنّ نفيًا وإثباتًا على المحمول نفسِه يُرَدّ.
"""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.slgae_deposit import SlgaeDepositError
from alghanem.arabic.slgae_fourth_version_deposit import (
    FRACTALITY_DIVISION,
    GUTTURAL_BRIDGE_READINGS,
    ONSET_TOTAL,
    ONSET_WITH_WRITTEN_WASLA,
    VCV_LEVELS,
    BridgeReading,
    FractalityDivision,
    compare_bridges,
    derive_exact_zero_cells,
    derive_onset_check,
    derive_window_balances,
    slgae_v4_digest,
    slgae_v4_path,
    version_chain_with_fourth,
)


def test_the_four_versions_are_deposited_with_distinct_digests() -> None:
    """النسخُ الأربعُ مُودَعةٌ معًا، وبصماتُها مقروءةٌ من الملفّات ومتمايزة."""

    chain = version_chain_with_fourth()

    assert len(chain) == 4
    assert len({digest for _path, digest in chain}) == 4
    assert slgae_v4_digest() == hashlib.sha256(slgae_v4_path().read_bytes()).hexdigest()


def test_the_bridge_carries_three_published_magnitudes() -> None:
    """جسرٌ واحدٌ بثلاثة مقادير في ثلاثة أقسام، كلٌّ بموضعه."""

    readings = GUTTURAL_BRIDGE_READINGS

    assert len(readings) == 3
    assert len({reading.section for reading in readings}) == 3
    assert all(reading.with_guttural > reading.without_guttural for reading in readings)
    assert [round(reading.odds_ratio, 2) for reading in readings] == [
        1.39,
        20.81,
        15.11,
    ]


def test_a_weaker_effect_with_a_stronger_p_implies_a_larger_sample() -> None:
    """ضعُف الأثرُ واشتدّت الدلالةُ معًا، ولا يجتمعان إلّا بعيّنةٍ أكبر."""

    comparison = compare_bridges()

    assert comparison.effect_weakened
    assert comparison.significance_strengthened
    assert comparison.implies_a_larger_sample
    assert comparison.odds_ratio_change == pytest.approx(-0.274, abs=0.001)


def test_the_window_table_balances_within_its_rounding() -> None:
    """الصفوفُ الثلاثةُ تتّزن بعد حساب مجال التقريب، وأضيقُها المفصل."""

    balances = derive_window_balances()

    assert len(balances) == 3
    assert all(balance.balances for balance in balances)
    tightest = min(balances, key=lambda balance: balance.nearest_edge_slack)
    assert tightest.level == "المفصل الصرفي"
    assert tightest.nearest_edge_slack == pytest.approx(33.0, abs=1.0)


def test_no_level_leaves_an_unexplained_window() -> None:
    """عمودُ «غير مفسَّر» صفرٌ في المستويات الثلاثة، وهو دعوى قابلة للنقض."""

    assert [row.unexplained for row in VCV_LEVELS] == [0, 0, 0]
    assert [row.excess for row in VCV_LEVELS] == [96, 4, 2694]


def test_the_onset_remainder_matches_its_named_cases() -> None:
    """بقيّةُ الابتداء بالطرح تُطابِق مجموعَ حالاتها المُسمّاة، بلا فضلة."""

    check = derive_onset_check()

    assert ONSET_TOTAL - ONSET_WITH_WRITTEN_WASLA == 4
    assert check.subtraction == check.named_sum == 4
    assert check.matches


def test_two_cells_are_an_exact_zero_ratio() -> None:
    """خليّتان قيمتُهما صفرٌ تامّ، وصفرُ النسبة صفرُ مشاهدةٍ لا ضعفُ أثر."""

    zeros = derive_exact_zero_cells()

    assert len(zeros) == 2
    assert all(index == 1 for _name, index in zeros)
    assert {name for name, _index in zeros} == {"ضمة ثم واو صامتة", "ضمة ثم ياء"}


def test_a_denial_and_an_affirmation_of_the_same_predicate_are_refused() -> None:
    """القسمةُ تحتاج محمولَين مختلفَين؛ وعلى المحمول نفسِه تناقضٌ يُرَدّ."""

    assert not FRACTALITY_DIVISION.is_a_contradiction
    assert FRACTALITY_DIVISION.resolution_quoted == "العدد فراكتالي، والنوع معجمي"

    with pytest.raises(SlgaeDepositError, match="تناقضٌ لا قسمة"):
        FractalityDivision(
            denied_for="الشيءُ نفسُه",
            denied_in="أ",
            affirmed_for="الشيءُ نفسُه",
            affirmed_in="ب",
            resolution_quoted="لا شيء",
            is_a_contradiction=False,
        )


def test_a_ratio_outside_its_range_is_refused() -> None:
    """نسبةُ الفتح بين الصفر والواحد حصرًا، وخارجُها يُرَدّ لا يُقصَر."""

    with pytest.raises(SlgaeDepositError, match="بين الصفر والواحد"):
        BridgeReading(
            section="قسم",
            scope="مجال",
            with_guttural=1.0,
            without_guttural=0.5,
            p_value=None,
        )
