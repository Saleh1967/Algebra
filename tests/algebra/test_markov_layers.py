"""أربعُ مبرهناتٍ على الطبقات، مُبرهَنةٌ على مادّةٍ مبنيّةٍ باليد.

**لا مدوّنةَ ههنا**: كلُّ مثالٍ في هذا الملفّ مصنوعٌ ليُظهِر المبرهنةَ أو
ينقضَها، فالفحصُ فحصُ **جبرٍ** لا فحصُ لغة. وما يُقاس على المصحف يُسجَّل
في شجرته.

`THE_IDENTITY_IS_PROVED_ON_BUILT_STREAMS_NOT_ASSUMED`: وحفظُ التدفّق
هُويّةٌ تُبرهَن بالاستقراء على الطول، فتُفحَص على تيارات متنوّعة — ولو
خُرِقت مرّةً لكان العطلُ في العادّ لا في المادّة.

`LUMPABILITY_IS_SHOWN_BOTH_WAYS`: ويُبنى مثالان: سلسلةٌ **تُكتَّل** بصفرِ
خلل، وأخرى **لا تُكتَّل** وإن تشابهت كتلُها ظاهرًا. فالشرطُ ليس تشابهَ
الأسماء بل استواءَ النصيب إلى كلّ كتلة.
"""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from algebra.markov_layers import (
    MARKOV_LAYER_NAMED_RESIDUALS,
    ContextReading,
    Layer,
    LayerError,
    bigram_census,
    conditional_entropy,
    context_reading,
    flow_defect,
    identity_layer,
    induced_map,
    lumpability,
    mutual_information,
    project_census,
    refines,
)

STREAMS: tuple[tuple[str, ...], ...] = (
    tuple("ababab"),
    tuple("aabbccaabb"),
    tuple("abcabcabcd"),
    tuple("aa"),
    tuple("xyzzyxyzzyx"),
)


@pytest.mark.parametrize("stream", STREAMS)
def test_flow_conservation_holds_on_every_built_stream(stream: tuple[str, ...]) -> None:
    """صادرُ الرمز ناقصَ وارده = [الأوّل] − [الأخير]، في كلّ رمزٍ وكلّ تيار."""

    assert set(flow_defect(stream).values()) == {0}


def test_flow_conservation_survives_every_projection() -> None:
    """الهُويّةُ محفوظةٌ تحت الإسقاط، فتصلح حارسًا لكلّ طبقةٍ لا للأساس وحدَه."""

    stream = tuple("abcabcabcd")
    layer = Layer(name="زوجيّ", projection={"a": "٠", "b": "١", "c": "٠", "d": "١"})
    assert set(flow_defect(layer.stream(stream)).values()) == {0}


def test_coarsening_cannot_add_information() -> None:
    """مبرهنةُ المعالجة: التخشينُ لا يرفع `I` — تُفحَص على سلسلةٍ مبنيّة."""

    stream = tuple("abcdabcdabdcabcd" * 8)
    fine = identity_layer(sorted(set(stream)))
    middle = Layer(name="وسط", projection={"a": "A", "b": "A", "c": "C", "d": "D"})
    coarse = Layer(name="خشن", projection={"a": "A", "b": "A", "c": "C", "d": "C"})

    assert refines(fine, middle) and refines(middle, coarse)
    census = bigram_census(stream)
    values = [
        mutual_information(project_census(census, one))
        for one in (fine, middle, coarse)
    ]
    assert values[0] >= values[1] - 1e-12 >= values[2] - 1e-12
    assert values[0] > values[2]  # وليس التساوي هو الحال دائمًا


def test_refinement_is_an_order_and_the_induced_map_is_refused_when_absent() -> None:
    """`φ` تُشتَقّ متى كان تخشينًا، وتُرَدّ متى قُطِعت كتلةٌ بين كتلتين."""

    fine = identity_layer(list("abcd"))
    coarse = Layer(name="خشن", projection={"a": "A", "b": "A", "c": "C", "d": "C"})
    crossing = Layer(name="قاطع", projection={"a": "A", "b": "C", "c": "A", "d": "C"})

    assert refines(fine, coarse) and refines(fine, crossing)
    assert induced_map(fine, coarse) == {"a": "A", "b": "A", "c": "C", "d": "C"}
    assert not refines(coarse, crossing)
    with pytest.raises(LayerError, match="ليست تخشينًا"):
        induced_map(coarse, crossing)


def test_a_strongly_lumpable_chain_has_zero_defect() -> None:
    """كتلتان يستوي نصيبُ عضويهما إلى كلّ كتلة — فالطبقةُ **مستوًى**."""

    # a وb كلاهما: نصفٌ إلى الكتلة A ونصفٌ إلى الكتلة B
    census = {
        ("a", "a"): 10,
        ("a", "b"): 10,
        ("a", "c"): 10,
        ("a", "d"): 10,
        ("b", "a"): 5,
        ("b", "b"): 15,
        ("b", "c"): 12,
        ("b", "d"): 8,
        ("c", "a"): 4,
        ("c", "c"): 16,
        ("d", "b"): 4,
        ("d", "d"): 16,
    }
    layer = Layer(name="كتلتان", projection={"a": "A", "b": "A", "c": "B", "d": "B"})
    reading = lumpability(census, layer)
    assert reading.defect == 0 and reading.is_strong
    assert reading.weighted == 0
    assert reading.compared_states == 4 and reading.excluded_states == 0


def test_a_chain_that_is_not_lumpable_is_named_a_shadow() -> None:
    """يختلف نصيبُ عضوين من كتلةٍ واحدة، فالطبقةُ **ظلٌّ** لا مستوى."""

    census = {
        ("a", "a"): 20,
        ("a", "b"): 20,
        ("b", "c"): 40,
        ("c", "c"): 10,
        ("d", "d"): 10,
    }
    layer = Layer(name="كتلتان", projection={"a": "A", "b": "A", "c": "B", "d": "B"})
    reading = lumpability(census, layer)
    assert reading.defect == 1 and not reading.is_strong
    assert reading.worst_block == "A"
    assert reading.weighted > 0


def test_the_floor_excludes_thin_rows_and_counts_them() -> None:
    """صفٌّ بوقوعٍ واحدٍ يعطي فرقًا واحدًا بالندرة؛ فالأرضيّةُ تُخرِجه معدودًا."""

    census = {
        ("a", "a"): 50,
        ("a", "c"): 50,
        ("b", "a"): 51,
        ("b", "c"): 49,
        ("t", "c"): 1,
        ("c", "c"): 10,
    }
    layer = Layer(name="كتلة", projection={"a": "A", "b": "A", "t": "A", "c": "B"})
    raw = lumpability(census, layer)
    held = lumpability(census, layer, floor=10)
    assert raw.defect == Fraction(51, 100) > held.defect == Fraction(1, 100)
    assert raw.excluded_states == 0 and held.excluded_states == 1
    assert held.floor == 10 and raw.floor == 1
    with pytest.raises(LayerError, match="أرضيّةُ الصادر"):
        lumpability(census, layer, floor=0)


def test_the_context_entropy_falls_with_order_and_carries_its_denominator() -> None:
    """`h_k` تتناقص بالرتبة، ومعها عددُ السياقات ومتوسّطُ نصيبها."""

    stream = tuple("abcabcabcabcabcabc" * 4)
    readings = [context_reading(stream, order) for order in (1, 2, 3)]
    for earlier, later in zip(readings, readings[1:], strict=False):
        assert later.entropy <= earlier.entropy + 1e-12
        assert later.contexts >= earlier.contexts
    assert isinstance(readings[0], ContextReading)
    assert readings[0].mean_count > 10 and readings[0].is_readable
    thin = context_reading(tuple("abcdefghij"), 3)
    assert thin.mean_count < 10 and not thin.is_readable


def test_conditional_entropy_agrees_with_information_and_marginals() -> None:
    """`I = H(Y) − H(Y|X)` — تُفحَص الهُويّةُ عدديًّا لا تُدَّعى."""

    stream = tuple("aabbabbaababbaab" * 6)
    census = bigram_census(stream)
    total = sum(census.values())
    followers: dict[str, int] = {}
    for (_, second), number in census.items():
        followers[second] = followers.get(second, 0) + number
    marginal = -sum(
        (number / total) * math.log2(number / total) for number in followers.values()
    )
    assert (
        abs(mutual_information(census) - (marginal - conditional_entropy(census)))
        < 1e-9
    )


def test_the_layer_refuses_what_it_was_not_given() -> None:
    """رمزٌ خارجَ المجال، وإسقاطٌ خاوٍ، وأبجديّتان — ثلاثةُ ردود."""

    layer = Layer(name="طبقة", projection={"a": "A"})
    with pytest.raises(LayerError, match="خارجَ مجال"):
        layer.of("z")
    with pytest.raises(LayerError, match="بلا إسقاطٍ مُودَع"):
        Layer(name="بلا", projection={})
    with pytest.raises(LayerError, match="بلا اسمٍ"):
        Layer(name="  ", projection={"a": "A"})
    with pytest.raises(LayerError, match="رمزٌ خاوٍ"):
        Layer(name="خاوٍ", projection={"a": ""})
    with pytest.raises(LayerError, match="أبجديّتين"):
        refines(layer, Layer(name="أخرى", projection={"b": "B"}))
    with pytest.raises(LayerError, match="دون رمزين"):
        bigram_census(("a",))


def test_the_named_residuals_are_five_and_distinct() -> None:
    """خمسةُ بواقٍ مُسمّاة، ولا اسمَ يتكرّر."""

    assert len(MARKOV_LAYER_NAMED_RESIDUALS) == 5
    assert len(set(MARKOV_LAYER_NAMED_RESIDUALS)) == 5
    joined = " ".join(MARKOV_LAYER_NAMED_RESIDUALS)
    for name in (
        "ALayerIsAProjectionAndNothingMore",
        "CoarseningCannotAddInformation",
        "ALayerWithoutLumpabilityIsAShadowNotALevel",
        "AnEmpiricalEntropyFallsBySparsityNotOnlyByStructure",
        "FlowConservationIsAnIdentityNotAFinding",
    ):
        assert name in joined


def test_the_identity_layer_is_the_top_of_the_order() -> None:
    """الطبقةُ الذرّيّةُ تخشِّنها كلُّ طبقةٍ على أبجديّتها، وهي مستوًى دائمًا."""

    alphabet = list("abc")
    fine = identity_layer(alphabet)
    for projection in ({"a": "A", "b": "A", "c": "A"}, {"a": "A", "b": "B", "c": "B"}):
        assert refines(fine, Layer(name="خشن", projection=projection))
    census = {("a", "b"): 3, ("b", "c"): 3, ("c", "a"): 3}
    assert lumpability(census, fine).is_strong
    assert Fraction(lumpability(census, fine).weighted) == 0
    with pytest.raises(LayerError, match="أبجديّةٌ خالية"):
        identity_layer([])
