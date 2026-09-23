"""الإسنادُ تامٌّ أو يُرَدّ، والممتنعُ دعوًى، وما لا يُفرَّق يُخرَج صريحًا.

يُثبِت هذا الاختبارُ أنّ ثغرةً واحدةً تُسقِط الجدولَ في إنشائه؛ وأنّ الممتنعَ
يُعلَن ولا يُملأ ولا يُسأل عنه بفراغ؛ وأنّ صفّين بتوقيعٍ واحدٍ يُخرَجان
زمرةً؛ وأنّ العمودَ الفاصلَ يُسمّى.
"""

from __future__ import annotations

import pytest

from algebra.assignment import (
    ASSIGNMENT_NAMED_RESIDUALS,
    Assignment,
    AssignmentError,
)

ROWS = ("أ", "ب", "ج")
COLUMNS = ("س", "ص")
CELLS = (
    ("أ", "س", "١"),
    ("أ", "ص", "٢"),
    ("ب", "س", "١"),
    ("ب", "ص", "٢"),
    ("ج", "س", "١"),
)
TABLE = Assignment(rows=ROWS, columns=COLUMNS, cells=CELLS, forbidden=(("ج", "ص"),))


def test_a_hole_sinks_the_table_at_construction() -> None:
    """خليّةٌ غيرُ مذكورةٍ ثغرةٌ تُرَدّ، ولا تُقرأ «شائعًا» ولا «أصلًا»."""

    with pytest.raises(AssignmentError) as raised:
        Assignment(rows=ROWS, columns=COLUMNS, cells=CELLS)
    assert "ثغرات" in str(raised.value)


def test_a_forbidden_cell_is_declared_filled_never_and_asked_never() -> None:
    """الممتنعُ يُعلَن، ويُرَدّ ملؤه، ويُرَدّ سؤالُه — ولا يُرجَع فراغًا."""

    assert TABLE.covers_the_grid()
    assert TABLE.forbidden_count == 1
    assert TABLE.filled == 5
    with pytest.raises(AssignmentError):
        TABLE.value_at("ج", "ص")
    with pytest.raises(AssignmentError):
        Assignment(
            rows=ROWS,
            columns=COLUMNS,
            cells=(*CELLS, ("ج", "ص", "٣")),
            forbidden=(("ج", "ص"),),
        )
    assert TABLE.signature_of("ج") == ("١", None)


def test_rows_that_share_a_signature_are_reported_as_one_group() -> None:
    """«أ» و«ب» لا يفرّق بينهما الجدولُ، وذلك خبرٌ يُخرَج لا عيبٌ يُستر."""

    assert TABLE.indistinguishable_rows() == (("أ", "ب"),)
    assert TABLE.separating_columns("أ", "ب") == ()
    assert TABLE.separating_columns("أ", "ج") == ("ص",)


def test_what_is_not_a_table_is_refused() -> None:
    """محورٌ خالٍ أو مكرّر، وخليّةٌ بلا قيمة، وإحداثيٌّ غريب، وإسنادٌ مزدوج."""

    with pytest.raises(AssignmentError):
        Assignment(rows=(), columns=COLUMNS, cells=())
    with pytest.raises(AssignmentError):
        Assignment(rows=("أ", "أ"), columns=("س",), cells=(("أ", "س", "١"),))
    with pytest.raises(AssignmentError):
        Assignment(rows=("أ",), columns=("س",), cells=(("أ", "س", "  "),))
    with pytest.raises(AssignmentError):
        Assignment(rows=("أ",), columns=("س",), cells=(("ز", "س", "١"),))
    with pytest.raises(AssignmentError):
        Assignment(
            rows=("أ",), columns=("س",), cells=(("أ", "س", "١"), ("أ", "س", "٢"))
        )
    with pytest.raises(AssignmentError):
        TABLE.signature_of("ليس صفًّا")


def test_the_named_residuals_are_four_and_distinct() -> None:
    """البواقي المُسمّاةُ أربعٌ، ولا تكرارَ فيها."""

    assert len(ASSIGNMENT_NAMED_RESIDUALS) == 4
    assert len(set(ASSIGNMENT_NAMED_RESIDUALS)) == 4
