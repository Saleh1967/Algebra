"""مركّبُ التفاعل: ل١ و ل٢ و ل٣ مفحوصةً بالتعداد، والمستحيلُ مردودًا.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ المركّباتَ على ثلاثة رؤوسٍ **تسعةٌ**
بالتعداد الشامل وأنّ ما يحتوي السلسلةَ منها **ثلاثةٌ**، وأنّ الوجهَ الثلاثيَّ
لا يدخل إلّا بأضلاعه الثلاثة، وأنّ السلسلةَ المُودَعةَ واحدةٌ في التعداد
ومسارَي الضلعَين الآخَرين لا يُسمّيان باسمها، وأنّ الهيكلَ الأوّلَ يتطابق في
المثلّث الزوجيّ والتفاعل الثلاثيّ فالرسمُ لا يفصل بينهما (ل٢)، وأنّ أعدادَ
بيتي `(1,0)` و`(1,1)` و`(1,0,0)` (ل٣)، وأنّ مصفوفةَ الحدّ **مؤشَّرةٌ** فيجمع
كلُّ عمودٍ إلى صفرٍ ويكون `∂₁∘∂₂ = 0`، وأنّ عددَ بيتي المستحيلَ يُرَدُّ عند
الحساب لا يُخرَج، وأنّ مركّبًا غيرَ منغلقٍ على أوجهه الأدنى يُرفَض عند
الإنشاء، وأنّ خلايا الطبقات على الجذور المُودَعة صفرٌ أو واحدٌ — وهو سندُ ت٣.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

import alghanem.arabic.interaction_complex_lemmas as module
from alghanem.arabic.interaction_complex_lemmas import (
    CHAIN,
    CHAIN_EDGES,
    COMPLEX_LEMMAS_NAMED_RESIDUALS,
    FULL,
    PAIR,
    VERTICES,
    ComplexLemmaError,
    InteractionComplex,
    betti_numbers,
    boundary_matrix,
    complexes_above_the_chain,
    enumerate_complexes,
    first_skeleton,
    matrix_rank,
    strata_cells_are_binary,
)


def test_nine_complexes_and_three_above_the_chain() -> None:
    """ل١: تسعةٌ بالتعداد، وثلاثةٌ فوق السلسلة، والاحتواءُ مُشتَقٌّ لا مكتوب."""

    complexes = enumerate_complexes()
    assert len(complexes) == 9
    assert len({complex_.faces for complex_ in complexes}) == 9
    above = complexes_above_the_chain()
    assert [complex_.name for complex_ in above] == ["Δ_chain", "Δ_pair", "Δ_full"]
    assert all(CHAIN.faces <= complex_.faces for complex_ in above)


def test_the_triangle_enters_only_with_its_three_edges() -> None:
    """الوجهُ الثلاثيُّ يقتضي `13`؛ ولا مركّبَ بوجهٍ بلا أوجهه الأدنى."""

    assert (
        sum(1 for complex_ in enumerate_complexes() if complex_.top_dimension == 2) == 1
    )
    with pytest.raises(ComplexLemmaError):
        InteractionComplex(
            name="ناقص",
            faces=frozenset({(1,), (2,), (3,), (1, 2), (2, 3), (1, 2, 3)}),
        )


def test_the_deposited_chain_is_named_alone() -> None:
    """مساراتُ الضلعَين ثلاثةٌ، وواحدٌ منها سلسلةُ مركوف؛ فلا يُسمّى غيرُه بها."""

    names = [complex_.name for complex_ in enumerate_complexes()]
    assert names.count("Δ_chain") == 1
    two_edge = [
        complex_
        for complex_ in enumerate_complexes()
        if len(complex_.faces_of_dimension(1)) == 2
    ]
    assert len(two_edge) == 3
    assert CHAIN.faces_of_dimension(1) == CHAIN_EDGES


def test_a_graph_cannot_separate_the_hollow_from_the_filled() -> None:
    """ل٢: الهيكلُ الأوّلُ نفسُه، والمركّبان مختلفان؛ فالفصلُ ليس للرسم."""

    assert first_skeleton(PAIR) == first_skeleton(FULL)
    assert PAIR.faces != FULL.faces
    assert len(first_skeleton(FULL)) == len(VERTICES) + 3


def test_betti_numbers_with_a_signed_boundary() -> None:
    """ل٣: الدورةُ تظهر في الزوجيّ ويملؤها الوجهُ الثلاثيّ."""

    assert betti_numbers(CHAIN) == (1, 0)
    assert betti_numbers(PAIR) == (1, 1)
    assert betti_numbers(FULL) == (1, 0, 0)


def test_the_boundary_is_signed_and_composes_to_zero() -> None:
    """الإشارةُ ليست زينة: كلُّ عمودٍ يجمع إلى صفرٍ، و`∂₁∘∂₂ = 0`."""

    second = boundary_matrix(FULL, 2)
    assert [[str(value) for value in row] for row in second] == [["1"], ["-1"], ["1"]]
    first = boundary_matrix(FULL, 1)
    for column in range(len(first[0])):
        assert sum(row[column] for row in first) == Fraction(0)
    product = [
        sum(first[row][middle] * second[middle][0] for middle in range(len(second)))
        for row in range(len(first))
    ]
    assert product == [Fraction(0)] * len(first)
    assert matrix_rank(second) == 1


def test_impossible_betti_values_are_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """حدٌّ غيرُ مؤشَّرٍ يُخرِج المستحيل؛ والحارسُ يرُدُّه قبل أن يُقرأ نتيجةً."""

    def unsigned(complex_: InteractionComplex, dimension: int) -> list[list[Fraction]]:
        return [
            [abs(value) for value in row]
            for row in boundary_matrix(complex_, dimension)
        ]

    monkeypatch.setattr(module, "boundary_matrix", unsigned)
    with pytest.raises(ComplexLemmaError):
        module.betti_numbers(PAIR)
    monkeypatch.undo()
    assert betti_numbers(PAIR) == (1, 1)


def test_an_empty_complex_is_refused() -> None:
    """مركّبٌ بلا وجهٍ ليس مركّبًا، ولا يُحمَل على أقربِ مقبول."""

    with pytest.raises(ComplexLemmaError):
        InteractionComplex(name="فارغ", faces=frozenset())


def test_the_uniformity_rests_on_root_distinctness() -> None:
    """سندُ ت٣ مقيسٌ على الجذور المُودَعة: خلايا الطبقات صفرٌ أو واحد."""

    assert strata_cells_are_binary() is True


def test_named_residuals_are_deposited() -> None:
    """البواقي المُسمّاةُ سبعٌ، ولا مكرَّرَ فيها."""

    assert len(COMPLEX_LEMMAS_NAMED_RESIDUALS) == 7
    assert len(set(COMPLEX_LEMMAS_NAMED_RESIDUALS)) == 7
