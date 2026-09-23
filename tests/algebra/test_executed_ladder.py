"""السُّلَّمُ منفَّذًا: عشرُ طبقاتٍ أُعلِنت، وتسعٌ عُرِضت — وفحصُ ما عُرِض.

**ما يُقاس ههنا**: اتّساقُ تقرير التنفيذ مع نفسه ومع ما أُودِع من قبل. لا
مدوَّنةَ تُقرَأ ولا عرّافَ يُفتَح: أرقامُ التقرير تُعاد بالحساب، وما لا يُعاد
يُسمّى.

`A_FAILED_PREDICTION_MAY_BE_GOOD_NEWS`: «فشل» حكمٌ على **التنبّؤ** لا على
الجسر. وط١ فشل لأنّ المقيسَ **جاوز** المتوقَّع (٦٤٫٨٠٪ على تنبّؤٍ دون ٥٠٪)،
وط٣ فشل لأنّه **قصّر**. والكلمةُ واحدةٌ والخبرانِ متعاكسان، فيُطبَع اتّجاهُ
الإخفاق مع الحكم دائمًا.

`A_JOINT_IS_NOT_THE_PRODUCT_UNLESS_MEASURED`: اتّفاقُ الحدّين معًا ٣٩٫٤٦٪
دون حاصلِ ضربهما ٤٢٫٤٢٪. فالاتّفاقان **مترابطان سلبًا**، وذلك خبرٌ لا يظهر
من الرقمين منفردين.

`AN_ERROR_COUNT_DECLARES_ITS_DENOMINATOR`: ١٬١٤٩ خطأً عند ٩٣٫٦٣٪ يستلزم
مقامًا نحوَ ١٨٬٠٣٨ — لا ٣٤٬٢٥٦ التي وُسِمت إعرابًا. والمقامُ رقمٌ واحدٌ
يُنشَر، لا يُستنبَط.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.bridge import Bridge, BridgeError, Crossing, Ladder, Level
from algebra.reconciliation import Partition, rounds_to
from algebra.signified import Direction, Prediction, Verdict

ORACLE = "quran-morphology — POS ثلاثةٌ (N/V/P) وإعرابٌ موسومٌ في ٣٤٬٢٥٦ مقطعًا"

# ---------------------------------------------- الطبقاتُ كما عُرِضت في الجدول
SHOWN_LAYERS = ("ط٠", "ط١", "ط٢", "ط٣", "ط٥", "ط٦", "ط٧", "ط٨", "ط٩")
DECLARED_LAYERS = 10

MEASURED = {
    "ط١ الاسترجاع": Fraction("0.6480"),
    "ط٢ الحدّان معًا": Fraction("0.3946"),
    "ط٣ الدقّة": Fraction("0.7578"),
    "ط٣ الاستدعاء": Fraction("0.2592"),
    "ط٥ الجذر": Fraction("0.9127"),
    "ط٦ الجمود": Fraction("0.9002"),
    "ط٧ القسمة": Fraction("0.9790"),
    "ط٨ الجملة": Fraction("0.9738"),
    "ط٩ العلامة": Fraction("0.9363"),
}
BASELINES = {
    "ط٦": Fraction("0.8477"),
    "ط٧": Fraction("0.5277"),
    "ط٧ الجديد": Fraction("0.5387"),
    "ط٩": Fraction("0.3734"),
}


def _prediction(name: str, threshold: str, direction: Direction) -> Prediction:
    return Prediction(
        identifier=name,
        statistic="نسبةٌ مقيسة",
        threshold=Fraction(threshold),
        direction=direction,
        falsifies=f"تنبّؤَ {name} وحدَه، لا الجسرَ",
    )


def test_ten_layers_are_declared_and_nine_are_shown() -> None:
    """التقريرُ يقول «عشرُ طبقات» ويعرض تسعًا: ط٤ غائبةٌ عن الجدول.

    والفجوةُ ليست ترتيبًا: الأرقامُ تقفز من ط٣ إلى ط٥. فإمّا أنّ ط٤ نُفِّذت
    ولم تُعرَض، وإمّا أنّ العددَ تسعٌ — والجدولُ لا يفصل بينهما.
    """

    shown = Partition(parts=(len(SHOWN_LAYERS),), declared_total=DECLARED_LAYERS)
    assert shown.residue == 1
    assert "ط٤" not in SHOWN_LAYERS
    numbers = [
        int(name[1:].translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
        for name in SHOWN_LAYERS
    ]
    assert numbers == [0, 1, 2, 3, 5, 6, 7, 8, 9]
    assert 4 not in numbers


def test_the_direction_of_each_failure_is_opposite() -> None:
    """ط١ فشل لأنّه **جاوز**، وط٣ فشل لأنّه **قصّر** — والحكمُ واحد.

    فلو قُرِئت الكلمةُ وحدَها لظُنَّ الجسران سواءً؛ وهما متعاكسان.
    """

    over = _prediction("ط١", "0.50", Direction.AT_MOST)
    under = _prediction("ط٣ الدقّة", "0.85", Direction.AT_LEAST)
    assert over.verdict(MEASURED["ط١ الاسترجاع"]) is Verdict.FALSIFIED
    assert under.verdict(MEASURED["ط٣ الدقّة"]) is Verdict.FALSIFIED
    assert MEASURED["ط١ الاسترجاع"] > over.threshold  # جاوز
    assert MEASURED["ط٣ الدقّة"] < under.threshold  # قصّر


def test_the_six_met_predictions_clear_their_thresholds() -> None:
    """ط٥ وط٦ وط٧ وط٨ وط٩ تتحقّق، وط٦ بهامشٍ على العتبة بعينها."""

    assert (
        _prediction("ط٥", "0.85", Direction.AT_LEAST).verdict(MEASURED["ط٥ الجذر"])
        is Verdict.MET
    )
    margin = MEASURED["ط٦ الجمود"] - BASELINES["ط٦"]
    assert rounds_to(margin * 100, 2) == Fraction("5.25")
    assert margin < Fraction(6, 100)  # هامشٌ على العتبة لا فوقها بكثير
    for key, base in (("ط٧ القسمة", "ط٧"), ("ط٩ العلامة", "ط٩")):
        assert MEASURED[key] > BASELINES[base] + Fraction(35, 100)


def test_the_two_border_agreements_are_negatively_associated() -> None:
    """٣٩٫٤٦٪ دون حاصلِ الضرب ٤٢٫٤٢٪، وداخلَ حدَّي فريشيه — فالترابطُ سالب."""

    prefix, suffix = Fraction("0.7051"), Fraction("0.6016")
    joint = MEASURED["ط٢ الحدّان معًا"]
    product = prefix * suffix
    assert rounds_to(product * 100, 4) == Fraction("42.4188")
    assert joint < product
    assert rounds_to((product - joint) * 100, 2) == Fraction("2.96")
    assert prefix + suffix - 1 <= joint <= min(prefix, suffix)


def test_the_over_stripping_causes_do_not_exhaust_the_count() -> None:
    """الأصنافُ الثلاثةُ ٦٤٫٤٪ من ١٥٬١٧٤، و٥٬٤٠٢ غيرُ مُسمًّى.

    فقولُ «أزيدُ ما أقشّره هو بعينه العلامةُ الإعرابيّة» يصدق على **ثلثين**،
    والثلثُ الباقي لم يُسمَّ. وذلك لا ينقض الاكتشاف — ولكنّه يحدّه.
    """

    total = 15_174
    named = tuple(
        round(total * Fraction(share) / 100) for share in ("32.1", "26.4", "5.9")
    )
    assert named == (4_871, 4_006, 895)
    accounted = Partition(parts=named, declared_total=total)
    assert accounted.measured_total == 9_772
    assert accounted.residue == 5_402
    assert rounds_to(Fraction(sum(named) * 100, total), 1) == Fraction("64.4")


def test_the_case_layer_does_not_declare_its_denominator() -> None:
    """١٬١٤٩ خطأً عند ٩٣٫٦٣٪ يستلزم مقامًا ≈١٨٬٠٣٨، لا ٣٤٬٢٥٦ الموسومة."""

    errors, accuracy = 1_149, MEASURED["ط٩ العلامة"]
    implied = errors / (1 - accuracy)
    assert round(float(implied)) == 18_038
    on_marked = 34_256 * (1 - accuracy)
    assert round(float(on_marked)) == 2_182
    assert float(implied) < 34_256
    with pytest.raises(BridgeError):
        Crossing(bridge="ط٩", given=34_256, mapped=34_256 - errors)


def test_the_error_profile_matches_the_deposited_case_table() -> None:
    """أصنافُ الخطأ الأربعةُ هي بعينها ما يخرج عن توقيع المفرد في جدول الإعراب.

    المثنّى وجمعُ المذكّر السالم (٤٧٫١٪) يفترقان عن المفرد في **الحالات
    الثلاث**؛ والممنوعُ من الصرف (١١٫٤٪) في الجرّ وحدَه؛ والمبنيُّ والموقوفُ
    خارجَ الجدول أصلًا. فالخطأُ يقع حيث تكون العلامةُ **حرفًا أو حذفًا** لا
    حركةً — وهو ما يُخرِجه الجدولُ المُودَعُ بالحساب لا بالسرد.
    """

    shares = (
        ("المثنّى وجمعُ المذكّر السالم", Fraction("47.1")),
        ("المبنيّ", Fraction("18.6")),
        ("الممنوعُ من الصرف", Fraction("11.4")),
        ("الموقوف", Fraction("4.1")),
    )
    assert sum(share for _, share in shares) == Fraction("81.2")
    assert shares[0][1] > sum(share for _, share in shares[1:])
    counts = tuple(round(1_149 * share / 100) for _, share in shares)
    assert counts == (541, 214, 131, 47)
    assert sum(counts) == 933


def test_the_symbol_count_reproduces_an_earlier_independent_deposit() -> None:
    """٣٤١٬٢٤٩ رمزًا — عينُ Σ k·n_k من توزيع الأطوال المُودَع في تدقيقٍ سابق."""

    histogram = {
        1: 4,
        2: 8_098,
        3: 16_034,
        4: 17_865,
        5: 17_289,
        6: 10_616,
        7: 5_440,
        8: 1_598,
        9: 380,
        10: 93,
        11: 12,
    }
    assert sum(length * count for length, count in histogram.items()) == 341_249
    assert sum(histogram.values()) == 77_429


def test_the_word_count_of_the_component_layer_matches_no_declared_unit() -> None:
    """٤١٬٧١٩ ليست وقوعاتٍ ولا صورًا ولا مقاطعَ صرفيّةً ولا موسومًا إعرابًا."""

    for declared in (77_429, 18_993, 130_030, 34_256):
        assert 41_719 != declared
    assert rounds_to(Fraction(13_039 * 100, 41_719), 1) == Fraction("31.3")
    assert rounds_to(Fraction(41_719 * 100, 77_429), 2) == Fraction("53.88")


def test_the_executed_ladder_is_traversable_where_the_declared_one_was_not() -> None:
    """بعد العرّاف صارت الجسورُ العشرةُ مبنيّةً، فيُبلَغ أعلى السُّلَّم من أسفله."""

    levels = tuple(
        Level(name)
        for name in (
            "الشيفرة",
            "الوحدات",
            "الإملاء",
            "المكوّنات",
            "الأدوات",
            "الجذع",
            "الجذر",
            "الجمود",
            "القسمة",
            "الجملة",
            "العلامة",
        )
    )
    executed = Ladder(
        bridges=tuple(
            Bridge(f"ط{index}", source, target)
            for index, (source, target) in enumerate(
                zip(levels, levels[1:], strict=False)
            )
        )
    )
    assert len(executed.bridges) == 10
    assert executed.is_traversable
    assert executed.first_gap is None
    assert executed.oracles_required() == ()
    assert len(executed.reachable_levels()) == 11
    assert executed.built_but_unreached() == ()
    assert ORACLE.startswith("quran-morphology")
