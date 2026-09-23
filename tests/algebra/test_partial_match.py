"""الثقبُ بمجالٍ: المطابقةُ لا تتّسع، والغيابُ يبقى بيانًا عن اللغة.

يُثبِت هذا الاختبارُ أربعةً: أنّ ثقبًا بلا مجالٍ **يُرَدّ في الإنشاء**؛ وأنّ
الطولَ ردٌّ قاطعٌ لا درجةُ تشابه؛ وأنّ ما يضيفه ثقبٌ بلا مجالٍ **يُعَدّ**
عنصرًا عنصرًا؛ وأنّ تحويلًا يُدَّعى تمامُه يرفع خطأَه المُسمّى لا `KeyError`.
"""

from __future__ import annotations

import pytest

from algebra.partial_match import (
    PARTIAL_MATCH_NAMED_RESIDUALS,
    Hole,
    PartialMatchError,
    matches,
    spurious_matches,
    total_map,
    unify,
)

# مواضعُ الشكل: حركةٌ ظاهرةٌ أو سكونٌ أو مدّ
UNIVERSE = ("Va", "Vu", "Vi", "C", "M")
# والصامتُ المجهولُ حالتُه إمّا محرَّكٌ وإمّا ساكن — ولا يكون مدًّا أبدًا
CONSONANT = Hole(name="صامتٌ مجهولُ الحركة", domain=frozenset({"Va", "Vu", "Vi", "C"}))
POOL = (
    ("Va", "M", "C"),
    ("Va", "Va", "C"),
    ("Va", "C", "C"),
    ("Va", "Vi", "C"),
    ("Va", "Vu", "C"),
    ("Va", "C"),
)


def test_a_hole_without_a_domain_is_refused_at_construction() -> None:
    """«أيُّ شيء» دعوًى لا حياد، فتُرَدّ قبل أن تُستعمَل."""

    with pytest.raises(PartialMatchError):
        Hole(name="مفتوح", domain=frozenset())
    with pytest.raises(PartialMatchError):
        Hole(name="   ", domain=frozenset({"C"}))
    assert CONSONANT.admits("C")
    assert not CONSONANT.admits("M")


def test_a_length_mismatch_is_a_flat_refusal() -> None:
    """اختلافُ الطول ردٌّ قاطع، ولا يُقرَّب نمطٌ بإسقاط موضع."""

    assert not unify(("Va", CONSONANT, "C"), ("Va", "C"))
    assert not unify(("Va", CONSONANT), ("Va", "C", "C"))
    assert unify(("Va", CONSONANT, "C"), ("Va", "C", "C"))


def test_the_restricted_hole_keeps_the_impossible_candidate_out() -> None:
    """الصامتُ المجهولُ يطابق أربعةً، والخامسُ مدٌّ فلا يُقبَل."""

    found = matches(("Va", CONSONANT, "C"), POOL)
    assert len(found) == 4
    assert ("Va", "M", "C") not in found
    assert ("Va", "C", "C") in found


def test_the_widening_is_counted_candidate_by_candidate() -> None:
    """ما يضيفه ثقبٌ بلا مجالٍ يُعَدّ، ولا يُقدَّر ولا يُهمَل بوصفه صغيرًا."""

    added = spurious_matches(("Va", CONSONANT, "C"), POOL, UNIVERSE)
    assert added == (("Va", "M", "C"),)
    assert len(added) == 1
    widened = len(matches(("Va", CONSONANT, "C"), POOL)) + len(added)
    assert widened == 5
    with pytest.raises(PartialMatchError):
        spurious_matches(("Va", CONSONANT), POOL, ())


def test_two_holes_widen_more_than_one() -> None:
    """التضخّمُ يتراكم بعدد الثقوب، فيُقاس على النمط لا على الموضع."""

    pool = tuple((first, second) for first in UNIVERSE for second in UNIVERSE)
    one = matches((CONSONANT, "C"), pool)
    two = matches((CONSONANT, CONSONANT), pool)
    assert len(one) == 4
    assert len(two) == 16
    assert len(spurious_matches((CONSONANT, "C"), pool, UNIVERSE)) == 1
    assert len(spurious_matches((CONSONANT, CONSONANT), pool, UNIVERSE)) == 9


def test_a_total_map_names_what_left_its_domain() -> None:
    """`KeyError` عاريةٌ لا تقول شيئًا؛ والخطأُ المُسمّى يقول الرمزَ والمجال."""

    table = {"a": "Va", "u": "Vu", "i": "Vi", "0": "C"}
    assert total_map(table, ("a", "0", "i")) == ("Va", "C", "Vi")
    with pytest.raises(PartialMatchError) as raised:
        total_map(table, ("a", "M"))
    assert "M" in str(raised.value)
    assert "a" in str(raised.value)


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(PARTIAL_MATCH_NAMED_RESIDUALS) == 5
    assert len(set(PARTIAL_MATCH_NAMED_RESIDUALS)) == 5
