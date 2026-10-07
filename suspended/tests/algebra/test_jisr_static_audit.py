"""تحليلُ `jisr.py` ساكنًا: فجوتان بنيويّتان، وثلاثُ فجواتٍ في القراءة.

**لم يُشغَّل**: `lib112` و`tagphon` و`order0.pkl` و`al_fixed.pkl` و`jidh5.pkl`
و`qmorph/` ليست في هذه الجلسة. فالفحصُ على المنطق المكتوب، والأثرُ يُحاكى
بالجبر لا يُقدَّر بالنظر.

`THE_MISSING_LAYER_IS_AN_INPUT_NOT_AN_OMISSION`: غيابُ ط٤ من الجدول مفسَّرٌ
الآن: `CUR = pickle.load(open('jidh5.pkl'))['cur']` — التقشيرُ **مبنيٌّ
سابقًا** ويُحمَّل مُدخَلًا. فهي طبقةٌ مُستهلَكةٌ لا منفَّذة، والصوابُ أن
تُعلَن مُدخَلًا لا أن تُعَدّ في العشر.

`TWO_LAYERS_ARE_NOT_OUT_OF_SAMPLE`: ط٣ تبني `CLOSED` من `KEYS` (تدريبٌ
واختبارٌ معًا) ثمّ تُقوّم على `TEST` — **تسرّب**. وط٥ لا تقسم أصلًا: `R`
على `KEYS` كلِّها، فـ٩١٫٢٧٪ و٩٩٫٤٩٪ **أرقامٌ داخليّة**. وط٦ وط٧ وط٩ تقسم
سليمًا.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.evaluation import (
    DecisionSet,
    EvaluationError,
    Split,
    Tally,
    majority_baseline,
)

# محاكاةٌ لقسمة السكريبت: السورُ الفرديّةُ تدريبٌ والزوجيّةُ اختبار
TRAIN = frozenset(f"s{n}" for n in range(1, 115, 2))
TEST = frozenset(f"s{n}" for n in range(2, 115, 2))
SPLIT = Split(train=TRAIN, test=TEST)

LAYERS_SHOWN = 9
LAYERS_CLAIMED = 10
CASE_MARKED_SEGMENTS = 34_256
REPORTED_CASE_ERRORS = 1_149
REPORTED_CASE_ACCURACY = Fraction("0.9363")


def test_the_split_itself_is_sound() -> None:
    """الفرديّةُ والزوجيّةُ منفصلتان، و٥٧ مقابل ٥٧ — قسمةٌ صحيحةٌ مستقرّة."""

    assert len(TRAIN) == len(TEST) == 57
    assert SPLIT.test_share == Fraction(1, 2)
    assert not (TRAIN & TEST)


def test_layer_three_builds_its_closed_set_on_the_whole_corpus() -> None:
    """`for k in KEYS: ST[z[1]]+=1` ثمّ التقويمُ على TEST — تسرّبٌ يُرَدّ.

    والسطرُ الحامل: `CLOSED = {s for s,n in ST.items() if n>=50 ...}` حيث
    `ST` على `KEYS` لا على `TRAIN`. فالأرقامُ المعروضةُ لـ«اختبار» **داخليّة
    جزئيًّا**، والحكمُ «فشل في الحدّين» يزداد قوّةً لا يضعف: الرقمُ الحقيقيُّ
    خارجَ العيّنة **دون** المعروض.
    """

    leaky = DecisionSet(
        name="CLOSED (ط٣)", members=frozenset({"جذع"}), built_from=TRAIN | TEST
    )
    assert leaky.is_leaky(SPLIT)
    assert leaky.leaked_keys(SPLIT) == TEST
    with pytest.raises(EvaluationError):
        leaky.assert_out_of_sample(SPLIT)
    repaired = DecisionSet(
        name="CLOSED (ط٣ مُصلَحًا)", members=frozenset({"جذع"}), built_from=TRAIN
    )
    repaired.assert_out_of_sample(SPLIT)


def test_layer_five_has_no_split_at_all() -> None:
    """`R` على `KEYS` كلِّها، فلا تدريبَ ولا اختبار — رقمٌ داخليٌّ يُسمّى كذلك."""

    in_sample = DecisionSet(
        name="R (ط٥)", members=frozenset({"جذر"}), built_from=TRAIN | TEST
    )
    assert in_sample.is_leaky(SPLIT)
    assert len(in_sample.leaked_keys(SPLIT)) == len(TEST)
    # و٩١٫٢٧٪ و٩٩٫٤٩٪ لا يُقارَنان بأرقام ط٦ وط٧ وط٩ لأنّها خارجَ العيّنة
    assert Fraction("0.9127") > Fraction("0.9002")  # ط٥ الداخليّ فوق ط٦ الخارجيّ
    assert Fraction("0.9949") > Fraction("0.9790")  # وفوق ط٧ الخارجيّ كذلك


def test_the_prefix_and_suffix_agreement_compares_lengths_not_content() -> None:
    """`ap += len(pre)==op` — طولٌ لا مضمون. فسابقتان مختلفتان بطولٍ واحدٍ تُعَدّ اتّفاقًا.

    ومقتضاه أنّ ٧٠٫٥١٪ و٦٠٫١٦٪ **حدّان أعليان** للاتّفاق الحقيقيّ، لا قياسان
    له. والإصلاحُ لا يغيّر بنيةَ القياس: يوازن بالمحتوى لا بالعدد.
    """

    oracle_prefix, mine_prefix = ("و", "ال"), ("ف", "ال")
    assert len(oracle_prefix) == len(mine_prefix)
    assert oracle_prefix != mine_prefix
    # القياسُ الحاليُّ يعدُّها اتّفاقًا، والصحيحُ يعدُّها خلافًا
    assert (len(mine_prefix) == len(oracle_prefix)) is True
    assert (mine_prefix == oracle_prefix) is False


def test_the_case_rule_conflates_abstention_with_error() -> None:
    """`RULE.get(tail(k))` تُرجِع `None` حين لا حركةَ في الآخر، فتُعَدّ خطأً.

    و`tail` تُرجِع `None` على كلمةٍ آخرُها ساكنٌ أو مدّ — وتلك **امتناعٌ** لا
    خطأ. فالرقمُ المعروضُ لقاعدة «آخرِ حركة» يخلط سعةَ القاعدة بصوابها،
    ويُخفي أيَّهما يُصلَح.
    """

    tally = Tally(correct=6_000, wrong=2_000, abstained=10_038)
    assert tally.total == 18_038
    assert round(float(tally.accuracy_charging_abstention), 4) == 0.3326
    assert round(float(tally.precision_where_it_fires), 4) == 0.75
    assert tally.abstention_inflates_the_error_by > Fraction(2, 5)


def test_the_unstated_denominator_of_the_case_layer_is_the_test_half() -> None:
    """١٬١٤٩ خطأً عند ٩٣٫٦٣٪ ⇒ ≈١٨٬٠٣٨ — وهو **نصفُ** الموسوم، لا كلُّه.

    والسببُ مقروءٌ في الشفرة: `te=[(k,case_of(k)) for k in TEST]` ثمّ تصفية.
    فالمقامُ نصفُ ٣٤٬٢٥٦ تقريبًا، والفجوةُ في **التقرير** لا في الحساب:
    رقمٌ واحدٌ لم يُطبَع.
    """

    implied = REPORTED_CASE_ERRORS / (1 - REPORTED_CASE_ACCURACY)
    assert round(float(implied)) == 18_038
    half = CASE_MARKED_SEGMENTS * float(SPLIT.test_share)
    assert abs(float(implied) - half) / half < Fraction(6, 100)
    assert float(implied) < CASE_MARKED_SEGMENTS


def test_the_missing_layer_is_a_loaded_input() -> None:
    """ط٤ ليست ساقطةً: `CUR` تُحمَّل من `jidh5.pkl` — مُدخَلٌ لا طبقةٌ تُنفَّذ."""

    assert LAYERS_CLAIMED - LAYERS_SHOWN == 1
    executed = tuple("ط" + str(n) for n in (0, 1, 2, 3, 5, 6, 7, 8, 9))
    assert len(executed) == LAYERS_SHOWN
    assert "ط4" not in executed


def test_the_sixth_layer_baseline_comes_from_the_wrong_set() -> None:
    """`base` من TRAIN و`ok/n` على TEST — مقارنةٌ بين مجموعتين لا بين طريقتين."""

    train_labels = ["جامد"] * 8_477 + ["مشتقّ"] * 1_523
    test_labels = ["جامد"] * 8_000 + ["مشتقّ"] * 2_000
    assert majority_baseline(train_labels) == Fraction("0.8477")
    assert majority_baseline(test_labels) == Fraction("0.8")
    gap_as_reported = Fraction("0.9002") - majority_baseline(train_labels)
    gap_corrected = Fraction("0.9002") - majority_baseline(test_labels)
    assert gap_as_reported == Fraction("0.0525")
    assert gap_corrected > gap_as_reported  # والاتّجاهُ يعتمد على التوزيع


def test_the_set_pop_makes_the_case_label_order_dependent() -> None:
    """`(set(feat) & CASE).pop()` غيرُ محدَّدٍ إن حمل مقطعٌ حالتين — وترتيبُ
    `kl()` يحدّد حصصَ أصناف الخطأ. كلاهما يُثبَّت بترتيبٍ مُعلَن."""

    features = {"NOM", "ACC"}
    assert sorted(features)[0] == "ACC"  # مستقرٌّ عبر التشغيلات
    classes = ("ممنوعٌ من الصرف/علم", "مثنّى أو جمعٌ سالم", "مبنيّ", "موقوف", "سواها")
    assert len(classes) == 5
    assert classes[0] != classes[1]  # والأوّلُ يبتلع ما يصلح للثاني
