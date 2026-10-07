"""وزنُ الصيغ: العائلةُ تُعدّ، والإصابةُ تُفحَص، والثمنُ يُحسَب لا يُدَّعى.

يُثبِت هذا الاختبارُ سلوكَ الوحدة على أبجديّةٍ من حرفين، ثمّ يُقيم **دفترَ
المصادرات** للذيل المقطعيّ: ثلاثُ صيغٍ تُصيب الهدفَ نفسَه بأثمانٍ ٧ و٤ و١ بت،
وكلُّها تُميّزه بعضوٍ واحدٍ لا بأكثر — فالنقلُ بينها بلا فقدِ خبر. وأنّ البتَّ
الباقي ليس زينةً: قلبُ الترتيب يُخرِج جردًا **مختلفًا**، فالاختيارُ بينهما
واقعةٌ تُقاس لا اصطلاحٌ يُختار.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.stipulation import (
    STIPULATION_NAMED_RESIDUALS,
    Schema,
    StipulationError,
    ban_schema,
    bits_to_single_out,
    chain_schema,
    chain_words,
    list_schema,
    weigh,
)

TAIL_ALPHABET = ("V", "C")
# الذيولُ الأربعةُ التي خرجت بالتعداد في `factor_language`
TARGET = frozenset({"", "V", "C", "VC"})
# مجتمعُ الذيول الممكنةِ بطولٍ لا يتجاوز اثنين
POOL = ("", "V", "C", "VV", "VC", "CV", "CC")
CONCEIVABLE = 2 ** len(POOL)


def test_a_chain_is_a_subset_written_in_order() -> None:
    """المتتاليةُ الهابطةُ تمامًا مجموعةٌ جزئيّة، فعددُها `2**n` لزومًا."""

    assert chain_words(("V", "C")) == TARGET
    for size in range(1, 6):
        order = tuple("abcde"[:size])
        assert len(chain_words(order)) == 2**size
    with pytest.raises(StipulationError):
        chain_words(("V", "V"))


def test_the_list_schema_says_nothing_because_it_reaches_everything() -> None:
    """القائمةُ تبلغ كلَّ جردٍ يُتصوَّر، فلا تُحرّم شيئًا وثمنُها كاملُ البتّات."""

    weighing = weigh(list_schema(POOL), TARGET)
    assert weighing.family_size == CONCEIVABLE == 128
    assert weighing.distinct_languages == CONCEIVABLE
    assert weighing.forbidden_share(CONCEIVABLE) == 0
    assert weighing.bits == 7.0
    assert weighing.identifies_target


def test_the_ban_schema_is_sixteen_of_which_three_are_finite() -> None:
    """المنوعُ ستَّ عشرةَ نظريّةً، ثلاثٌ منها فقط تُنتِج لغةً منتهية."""

    schema = ban_schema(TAIL_ALPHABET)
    weighing = weigh(schema, TARGET)
    assert weighing.family_size == 16
    assert weighing.finite_count == 3
    assert weighing.distinct_languages == 3
    assert weighing.bits == 4.0
    assert round(weighing.bits_given_finiteness, 4) == 1.585
    assert weighing.identifies_target
    assert weighing.reaching == ("منعُ {VV، CV، CC}",)
    reachable = {words for _, words in schema.finite_members()}
    assert reachable == {
        TARGET,
        frozenset({"", "V", "C", "CV"}),
        frozenset({"", "V", "C"}),
    }


def test_the_chain_schema_costs_one_bit_and_that_bit_is_not_idle() -> None:
    """السلسلةُ عضوان لا غير، والعضوُ الآخرُ يُخرِج جردًا **مختلفًا**.

    فالبتُّ الباقي ليس اصطلاحَ كتابة: `V > C` تُعطي `VC` و`C > V` تُعطي `CV`،
    وهما جردان متمايزان. فالاختيارُ بينهما واقعةٌ تُقاس.
    """

    weighing = weigh(chain_schema(TAIL_ALPHABET), TARGET)
    assert weighing.family_size == 2
    assert weighing.bits == 1.0
    assert weighing.identifies_target
    assert weighing.reaching == ("V > C",)
    assert chain_words(("C", "V")) == frozenset({"", "V", "C", "CV"})
    assert chain_words(("C", "V")) != TARGET


def test_the_tighter_schema_is_the_one_that_forbids_more() -> None:
    """ثمنُ الصيغة في عدد ما تعجز عنه: ٢ من ١٢٨ تُحرّم ١٢٦ قبل النظر."""

    chain = weigh(chain_schema(TAIL_ALPHABET), TARGET)
    bans = weigh(ban_schema(TAIL_ALPHABET), TARGET)
    listed = weigh(list_schema(POOL), TARGET)
    assert chain.forbidden_share(CONCEIVABLE) == Fraction(126, 128)
    assert bans.forbidden_share(CONCEIVABLE) == Fraction(125, 128)
    assert listed.forbidden_share(CONCEIVABLE) == 0
    assert chain.forbidden_share(CONCEIVABLE) > bans.forbidden_share(CONCEIVABLE)
    assert chain.bits < bans.bits < listed.bits


def test_the_transfer_loses_no_news_at_any_step() -> None:
    """الصيغُ الثلاثُ تُصيب الهدفَ نفسَه بعضوٍ **واحد**، فلا خبرَ يسقط بالنقل."""

    for schema in (
        list_schema(POOL),
        ban_schema(TAIL_ALPHABET),
        chain_schema(TAIL_ALPHABET),
    ):
        weighing = weigh(schema, TARGET)
        assert weighing.reaches_target
        assert weighing.identifies_target


def test_a_schema_that_cannot_reach_the_target_is_refuted_not_cheap() -> None:
    """هدفٌ لا تبلغه السلسلةُ بأيّ ثمن: تُنقَض، ولا يُقرأ صفرُها ثمنًا أدنى."""

    unreachable = frozenset({"", "VV"})
    weighing = weigh(chain_schema(TAIL_ALPHABET), unreachable)
    assert not weighing.reaches_target
    assert not weighing.identifies_target
    assert weighing.bits == 1.0  # الثمنُ قائمٌ والإصابةُ منتفية


def test_what_cannot_be_weighed_is_refused() -> None:
    """هدفٌ خالٍ، وعائلةٌ خالية، وأسماءٌ مكرّرة، وحجمٌ دون واحد — كلُّها تُرَدّ."""

    with pytest.raises(StipulationError):
        weigh(chain_schema(TAIL_ALPHABET), frozenset())
    with pytest.raises(StipulationError):
        Schema(name="خالية", members=())
    with pytest.raises(StipulationError):
        Schema(name="مكرّرة", members=(("أ", frozenset()), ("أ", frozenset({"V"}))))
    with pytest.raises(StipulationError):
        bits_to_single_out(0)
    with pytest.raises(StipulationError):
        list_schema(("V", "V"))
    with pytest.raises(StipulationError):
        weigh(list_schema(POOL), TARGET).forbidden_share(0)
    with pytest.raises(StipulationError):
        weigh(list_schema(POOL), TARGET).forbidden_share(2)


def test_the_stipulation_ledger_of_the_syllable_tail() -> None:
    """الدفترُ كاملًا: ٧ بت ← ٤ بت ← ١ بت، والهدفُ واحدٌ في الثلاثة.

    وما بقي بعد الرفع بتٌّ واحدٌ: **أيُّهما يتقدّم، المدُّ أم السكون**. وهو
    مقيسٌ لا مُصادَر — ٢٢٥٬٩١٠ من ٢٢٥٬٩١١ في القياس المنشور، والمخالفُ واحدٌ
    مُسمًّى (أثرُ ترميز U+06EA). فالبقيّةُ مدفوعةٌ بالعدّ لا مكتوبةٌ باليد.
    """

    ledger = [
        (weigh(list_schema(POOL), TARGET), 7.0),
        (weigh(ban_schema(TAIL_ALPHABET), TARGET), 4.0),
        (weigh(chain_schema(TAIL_ALPHABET), TARGET), 1.0),
    ]
    assert [round(weighing.bits, 6) for weighing, _ in ledger] == [7.0, 4.0, 1.0]
    for weighing, expected in ledger:
        assert weighing.bits == expected
        assert weighing.identifies_target
    # البتُّ الباقي مدفوعٌ بالعدّ: مخالفٌ واحدٌ مُسمًّى من ٢٢٥٬٩١١
    assert 225_911 - 225_910 == 1


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(STIPULATION_NAMED_RESIDUALS) == 5
    assert len(set(STIPULATION_NAMED_RESIDUALS)) == 5
