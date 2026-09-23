"""العيّنةُ المشروطة: نصفُ جدولٍ يُرَدّ، والموضعُ لا «أو» فيه.

يُثبِت هذا الاختبارُ أربعةً: أنّ قياسَ الاقتران على عيّنةٍ منتقاةٍ بمصدرٍ
**يُرَدّ في المتن**؛ وأنّ عددًا خارجيًّا يَحُدّ المجهولَ من أسفل؛ وأنّ موضعًا
فيه «أو» أو بلا فحصٍ فاصلٍ يُرَدّ في الإنشاء؛ وأنّ قسمةً حُسِمت كلُّها
والأثرُ قائمٌ **ناقصةٌ لا تامّة**.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.selection import (
    SELECTION_NAMED_RESIDUALS,
    ConditionedTable,
    Locus,
    SelectionError,
    partition_of_loci,
)

HALF = ConditionedTable(
    condition="المصدرُ الأوّلُ قال نعم",
    absent_row="المصدرُ الأوّلُ قال لا",
    positive=0,
    negative=107,
    outside_positive_total=218,
)


def test_association_is_refused_on_half_a_table() -> None:
    """الردُّ في المتن لا في هامش، ويُسمّي الصفَّ الغائب."""

    assert not HALF.association_is_measurable
    assert HALF.missing_cells == 2
    assert HALF.observed_total == 107
    with pytest.raises(SelectionError) as raised:
        HALF.assert_measurable()
    assert "المصدرُ الأوّلُ قال لا" in str(raised.value)


def test_an_outside_count_bounds_the_missing_cell_from_below() -> None:
    """٢١٨ خارجًا و٠ مرصودًا ⇒ الخليّةُ الغائبةُ ≥ ٢١٨، و**كلُّ** العمود هرب."""

    assert HALF.missing_positive_at_least() == 218
    assert HALF.zero_is_about_selection_not_the_column()
    assert HALF.share_of_the_column_that_escaped() == 1
    partial = ConditionedTable(
        condition="ش",
        absent_row="لا ش",
        positive=50,
        negative=10,
        outside_positive_total=218,
    )
    assert partial.missing_positive_at_least() == 168
    assert not partial.zero_is_about_selection_not_the_column()
    assert partial.share_of_the_column_that_escaped() == Fraction(168, 218)


def test_without_an_outside_count_the_unknown_stays_unbounded() -> None:
    """بلا عددٍ خارجيٍّ لا يُحَدّ المجهولُ، ولا يُقدَّر بصفرٍ ولا بغيره."""

    blind = ConditionedTable(condition="ش", absent_row="لا ش", positive=0, negative=107)
    with pytest.raises(SelectionError):
        blind.missing_positive_at_least()
    with pytest.raises(SelectionError):
        blind.share_of_the_column_that_escaped()
    assert not blind.zero_is_about_selection_not_the_column()


def test_an_outside_count_below_the_observed_is_refused() -> None:
    """عددٌ خارجيٌّ دون المرصود يعني مجتمعين مختلفين، فيُرَدّ."""

    with pytest.raises(SelectionError):
        ConditionedTable(
            condition="ش",
            absent_row="لا ش",
            positive=50,
            negative=1,
            outside_positive_total=10,
        )
    with pytest.raises(SelectionError):
        ConditionedTable(condition="ش", absent_row="لا ش", positive=0, negative=0)
    with pytest.raises(SelectionError):
        ConditionedTable(condition="  ", absent_row="لا ش", positive=1, negative=0)


def test_a_locus_with_an_or_in_it_is_refused() -> None:
    """«أ أو ب» امتناعٌ عن القسمة لا خانةٌ فيها."""

    with pytest.raises(SelectionError):
        Locus(name="أ أو ب", settled=False, deciding_test="فحص")
    with pytest.raises(SelectionError):
        Locus(name="أ/ب", settled=False, deciding_test="فحص")
    with pytest.raises(SelectionError):
        Locus(name="أ", settled=False, deciding_test="   ")
    assert Locus(name="أ", settled=False, deciding_test="فحص").name == "أ"


def test_a_partition_needs_distinct_tests_and_one_open_locus() -> None:
    """موضعان بفحصٍ واحدٍ موضعٌ واحد، وقسمةٌ كلُّها محسومةٌ والأثرُ قائمٌ ناقصة."""

    good = (
        Locus(name="أ", settled=True, deciding_test="ف١"),
        Locus(name="ب", settled=False, deciding_test="ف٢"),
    )
    assert partition_of_loci(good) == good
    with pytest.raises(SelectionError):
        partition_of_loci(
            (
                Locus(name="أ", settled=False, deciding_test="ف"),
                Locus(name="ب", settled=False, deciding_test="ف"),
            )
        )
    with pytest.raises(SelectionError):
        partition_of_loci(
            (
                Locus(name="أ", settled=True, deciding_test="ف١"),
                Locus(name="ب", settled=True, deciding_test="ف٢"),
            )
        )
    with pytest.raises(SelectionError):
        partition_of_loci(())


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(SELECTION_NAMED_RESIDUALS) == 5
    assert len(set(SELECTION_NAMED_RESIDUALS)) == 5
