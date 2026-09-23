"""المركّباتُ البسيطة: تعدادٌ شامل، وحدٌّ مؤشَّر، وشاهدُ أويلر.

يُثبِت هذا الاختبارُ عشرةَ أشياء: أنّ التعدادَ يُخرِج 1 و2 و9 و114 مركّبًا على
رأسٍ ورأسَين وثلاثةٍ وأربعة، وأنّ أعدادَ بيتي للسلسلة `(1,0)` وللمثلّث الأجوف
`(1,1)` وللمصمت `(1,0,0)`، وأنّ **سطحَ الرباعيّ كرةٌ** `(1,0,1)` والرباعيَّ
المصمتَ `(1,0,0,0)` — وهما ما يُظهِر أنّ التعميمَ عملٌ لا نسخ، وأنّ شاهدَ
أويلر يصدُق في كلّ ذلك، وأنّ حدًّا غيرَ مؤشَّرٍ يُخرِج المستحيلَ فيُرَدّ، وأنّ
مركّبًا غيرَ منغلقٍ أو فارغًا أو غيرَ مرتَّبٍ يُرفَض عند الإنشاء، وأنّ الهيكلَ
الأوّلَ يتطابق في الأجوف والمصمت فالرسمُ لا يفصل بينهما.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.simplicial import (
    SIMPLICIAL_NAMED_RESIDUALS,
    Complex,
    SimplicialError,
    betti_numbers,
    boundary_matrix,
    closure_of,
    enumerate_complexes,
    enumeration_passes,
    euler_characteristic,
    euler_witness_holds,
    matrix_rank,
    skeleton,
)

CHAIN = closure_of(((1, 2), (2, 3)), "سلسلة")
HOLLOW = closure_of(((1, 2), (1, 3), (2, 3)), "مثلّثٌ أجوف")
SOLID = closure_of(((1, 2, 3),), "مثلّثٌ مصمت")
SPHERE = closure_of(((1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)), "سطحُ رباعيّ")
BALL = closure_of(((1, 2, 3, 4),), "رباعيٌّ مصمت")


def test_the_enumeration_counts_complexes_on_n_vertices() -> None:
    """التعدادُ شاملٌ: 1، 2، 9، 114 — والتسعةُ هي حالةُ الثلاثة المعروفة."""

    assert [len(enumerate_complexes(n)) for n in (1, 2, 3, 4)] == [1, 2, 9, 114]
    assert all(len(complex_.vertices) == 3 for complex_ in enumerate_complexes(3))


def test_betti_numbers_of_the_small_complexes() -> None:
    """السلسلةُ بلا دورة، والأجوفُ فيه دورةٌ واحدة، والمصمتُ يملؤها."""

    assert betti_numbers(CHAIN) == (1, 0)
    assert betti_numbers(HOLLOW) == (1, 1)
    assert betti_numbers(SOLID) == (1, 0, 0)


def test_the_generalization_reaches_the_sphere() -> None:
    """سطحُ الرباعيّ كرةٌ `(1,0,1)`، والمصمتُ `(1,0,0,0)` — تعميمٌ لا نسخ."""

    assert betti_numbers(SPHERE) == (1, 0, 1)
    assert betti_numbers(BALL) == (1, 0, 0, 0)
    assert SPHERE.top_dimension == 2
    assert BALL.top_dimension == 3


def test_euler_is_an_independent_witness() -> None:
    """المَعيارُ من عدد الأوجه يوافق مجموعَ بيتي بالتناوب في الخمسة."""

    for complex_ in (CHAIN, HOLLOW, SOLID, SPHERE, BALL):
        assert euler_witness_holds(complex_)
    assert euler_characteristic(SPHERE) == 2
    assert euler_characteristic(BALL) == 1
    assert euler_characteristic(HOLLOW) == 0


def test_the_boundary_is_signed_and_composes_to_zero() -> None:
    """`∂₂` مؤشَّرةٌ، وكلُّ عمودٍ في `∂₁` يجمع إلى صفر، و`∂₁∘∂₂ = 0`."""

    second = boundary_matrix(SOLID, 2)
    assert [[str(value) for value in row] for row in second] == [["1"], ["-1"], ["1"]]
    first = boundary_matrix(SOLID, 1)
    for column in range(len(first[0])):
        assert sum(row[column] for row in first) == Fraction(0)
    product = [
        sum(first[row][middle] * second[middle][0] for middle in range(len(second)))
        for row in range(len(first))
    ]
    assert product == [Fraction(0)] * len(first)
    assert matrix_rank(second) == 1


def test_an_unsigned_incidence_matrix_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """إزالةُ الإشارة تُخرِج المستحيلَ، والحارسُ يرُدُّه قبل أن يُقرأ نتيجةً."""

    import algebra.simplicial as module

    def unsigned(complex_: Complex, dimension: int) -> list[list[Fraction]]:
        return [
            [abs(value) for value in row]
            for row in boundary_matrix(complex_, dimension)
        ]

    monkeypatch.setattr(module, "boundary_matrix", unsigned)
    with pytest.raises(SimplicialError):
        module.betti_numbers(HOLLOW)
    monkeypatch.undo()
    assert betti_numbers(HOLLOW) == (1, 1)


def test_a_complex_must_be_closed() -> None:
    """وجهٌ بلا أوجهه الأدنى يُرفَض، ولا يُكمَّل صمتًا."""

    with pytest.raises(SimplicialError):
        Complex(faces=frozenset({(1,), (2,), (3,), (1, 2), (2, 3), (1, 2, 3)}))


def test_empty_and_unordered_inputs_are_refused() -> None:
    """الفارغُ وغيرُ المرتَّبِ وذو الرأسِ المكرَّرِ ثلاثتُها مردودة."""

    with pytest.raises(SimplicialError):
        Complex(faces=frozenset())
    with pytest.raises(SimplicialError):
        Complex(faces=frozenset({(1,), (2,), (2, 1)}))
    with pytest.raises(SimplicialError):
        Complex(faces=frozenset({(1,), (1, 1)}))
    with pytest.raises(SimplicialError):
        closure_of(())


def test_a_graph_cannot_separate_the_hollow_from_the_solid() -> None:
    """الهيكلُ الأوّلُ نفسُه في الأجوف والمصمت، والمركّبان مختلفان."""

    assert skeleton(HOLLOW, 1) == skeleton(SOLID, 1)
    assert HOLLOW.faces != SOLID.faces
    assert skeleton(SPHERE, 1) == skeleton(BALL, 1)


def test_named_residuals_are_deposited() -> None:
    """البواقي المُسمّاةُ ثلاثٌ، ولا مكرَّرَ فيها."""

    assert len(SIMPLICIAL_NAMED_RESIDUALS) == 3
    assert len(set(SIMPLICIAL_NAMED_RESIDUALS)) == 3


def test_the_enumeration_is_priced_before_it_is_attempted() -> None:
    """السقفُ مُعلَنٌ والثمنُ محسوبٌ قبل الدفع، فلا تُحاوَل دورةٌ لا تنتهي.

    وكان التعدادُ بلا حارس: `n = 5` يدور ٦٧ مليونَ مرّة، و`n = 6` مئةً وأربعًا
    وأربعين مليونَ مليار. فوحدةٌ تزن بلوغَ اختبارٍ حدَّه لا يليق بها أن تحاول
    ما لا يُبلَغ — والرقمُ يُحسَب من `2 ** (2**n − n − 1)` لا يُجرَّب.
    """

    assert [enumeration_passes(n) for n in (1, 2, 3, 4)] == [1, 2, 16, 2_048]
    assert enumeration_passes(5) == 67_108_864
    assert enumeration_passes(6) == 144_115_188_075_855_872

    with pytest.raises(SimplicialError) as raised:
        enumerate_complexes(5)
    assert "67,108,864" in str(raised.value)
    assert "4,096" in str(raised.value)

    # ورفعُ السقف صريحٌ لا ضمنيّ، ويبقى الحدُّ الأدنى عاملًا
    assert len(enumerate_complexes(4, passes_at_most=2_048)) == 114
    with pytest.raises(SimplicialError):
        enumerate_complexes(4, passes_at_most=2_047)
