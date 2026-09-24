"""تدقيقُ تقرير التوليد داخليًّا: سبعةُ أرقامٍ تتّسق، وواحدٌ يحتاج جوابًا.

**ما يُقاس ههنا وما لا يُقاس**: لا جدولَ جذورٍ عندي ولا مولِّد، فلا يُقوَّم
القياسُ ولا تُعاد ٤٣٫٨٢٪. يُفحَص شيءٌ واحد: أنّ أرقامَ التقرير **متّسقةٌ
فيما بينها**. وذلك كلُّ ما يحتمله ما بين يديّ.

`SEVEN_FIGURES_RECOMPUTE_EXACTLY`: ١٬٠٨٠ × ١٣٥ = ١٤٥٬٨٠٠ · ٥٬٦٠٣ ÷ ١٤٥٬٨٠٠
= ٣٫٨٤٪ · ٧٩٫٣٧ − ٦١٫٣١ = ١٨٫٠٦ · ٤٧٫٢١ − ٤٧٫١٥ = +٠٫٠٦ · ٣٨٫٦٤ − ٢٣٫٤٥ =
+١٥٫١٩ · ٤٧٫٢١ − ٣٨٫٦٤ = ٨٫٥٧ · ١٠٠ − ٤٦ = ٥٤٫٠. سبعةٌ من سبعة.

`THE_LOSS_SPLIT_DOES_NOT_SUM_TO_THE_LOSS`: قيل «فصلتُ الخسارةَ قسمين…
فكانت التغطيةُ ٣٨٫٧٪ **من الخسارة**». والقسمان يجمعان إلى ٥٠٫٤ لا إلى ١٠٠.
وبعد إدخال اللِّمّة يجمعان إلى ٥٦٫١. فإمّا أنّهما **من المقام** لا من
الخسارة، وإمّا أنّ ثلثًا لم يُسمَّ.

`THE_ONLY_CONSISTENT_READING_IMPLIES_A_REGRESSION`: والقراءةُ التي تُصدِّق
التقريرَ بنفسه هي «**من المقام**»: ١٠٠ − ٢٠٫٦ − ٣٥٫٥ = ٤٣٫٩٠، وهي ٤٣٫٨٢
المُعلَنةُ إلى ثُمن نقطة. وتلزم منها على الحالة السابقة: ١٠٠ − ٣٨٫٧ − ١١٫٧
= **٤٩٫٦٠٪**.

فإدخالُ اللِّمّة محورًا ثالثًا **رفع سقفَ التغطية ١٨٫٠٦ نقطة وخفض الدقّةَ
المحقَّقةَ ٥٫٧٨ نقطة**. وذلك لا ينقض الخبرَ اللغويّ — «البابُ لا يُستنتَج من
بقيّة خانات الجذر» يبقى مقيسًا بسقف التغطية — لكنّه يقلب حكمَ **المكسب**:
المحورُ الثالثُ ليس مكسبًا صافيًا بعدُ، بل **مبادلةٌ خسرت**. ومفتاحٌ أغنى
يُقلّل الشواهدَ في كلّ خانةٍ فيسوء الاختيارُ وإن اتّسعت التغطية.

`THE_SHIFT_OF_THE_LOSS_IS_THE_SAME_FACT_READ_TWICE`: قيل «انقلب موضعُ
الخسارة… فالهدفُ التالي الاختيارُ لا التغطية». وهو صحيح؛ ويلزم منه أنّ
الاختيارَ **ساء ٢٣٫٨ نقطة** (١١٫٧ ← ٣٥٫٥) مقابلَ تحسُّن التغطية ١٨٫١
(٣٨٫٧ ← ٢٠٫٦). والفرقُ بينهما هو الانحدارُ نفسُه: ٥٫٧ نقطة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

ROOTS, SLOTS, FILLED = 1_080, 135, 5_603
REPORTED_ACCURACY = Fraction("0.4382")
REPORTED_BASELINE = Fraction("0.1786")

CEILING_ROOT_ONLY = Fraction("0.6131")
CEILING_WITH_LEMMA = Fraction("0.7937")

SOUND_FREE, SOUND_SHAPED = Fraction("0.4715"), Fraction("0.4721")
WEAK_FREE, WEAK_SHAPED = Fraction("0.2345"), Fraction("0.3864")

# قسمةُ الخسارة كما وردت: (تغطية، اختيار)
SPLIT_BEFORE = (Fraction("0.387"), Fraction("0.117"))
SPLIT_AFTER = (Fraction("0.206"), Fraction("0.355"))


def test_the_grid_and_its_emptiness_recompute() -> None:
    """١٬٠٨٠ × ١٣٥ = ١٤٥٬٨٠٠، والمملوءُ ٣٫٨٤٪ — فستّةٌ وتسعون بالمئة فراغ."""

    cells = ROOTS * SLOTS
    assert cells == 145_800
    density = Fraction(FILLED, cells)
    assert rounds_to(density * 100, 2) == Fraction("3.84")
    assert rounds_to((1 - density) * 100, 1) == Fraction("96.2")


def test_the_lemma_axis_raises_the_ceiling_by_eighteen_points() -> None:
    """٧٩٫٣٧ − ٦١٫٣١ = ١٨٫٠٦ نقطة من سقف التغطية — والرقمُ يُعاد."""

    gain = CEILING_WITH_LEMMA - CEILING_ROOT_ONLY
    assert rounds_to(gain * 100, 2) == Fraction("18.06")
    assert CEILING_WITH_LEMMA < 1  # ويبقى عشرون بالمئة خارجَ المتناول


def test_the_shape_constraint_is_aimed_and_hits_only_the_weak() -> None:
    """+٠٫٠٦ على السالم و+١٥٫١٩ على المعتلّ — أثرٌ مصوَّبٌ لا عامّ."""

    sound = (SOUND_SHAPED - SOUND_FREE) * 100
    weak = (WEAK_SHAPED - WEAK_FREE) * 100
    assert rounds_to(sound, 2) == Fraction("0.06")
    assert rounds_to(weak, 2) == Fraction("15.19")
    assert weak > sound * 200

    # والتنبّؤ (ب) «الفرقُ بين السالم والمعتلّ > ٢٠ نقطة» ساقط
    remaining_gap = (SOUND_SHAPED - WEAK_SHAPED) * 100
    assert rounds_to(remaining_gap, 2) == Fraction("8.57")
    assert remaining_gap < 20


def test_the_loss_split_does_not_sum_to_the_loss() -> None:
    """القسمان يجمعان إلى ٥٠٫٤ و٥٦٫١ لا إلى ١٠٠ — فليسا «من الخسارة»."""

    for split in (SPLIT_BEFORE, SPLIT_AFTER):
        total = sum(split)
        assert total < Fraction("0.60")
        assert total > Fraction("0.50")


def test_the_only_consistent_reading_makes_them_shares_of_the_denominator() -> None:
    """١٠٠ − ٢٠٫٦ − ٣٥٫٥ = ٤٣٫٩٠ ≈ ٤٣٫٨٢ المُعلَنة — فهما من المقام."""

    implied = 1 - sum(SPLIT_AFTER)
    assert rounds_to(implied * 100, 2) == Fraction("43.90")
    assert abs(implied - REPORTED_ACCURACY) < Fraction("0.001")

    # وتمامُ القسمة حينئذٍ: دقّةٌ + تغطيةٌ مفقودةٌ + اختيارٌ خاطئ = المقام
    parts = (4_390, 2_060, 3_550)
    assert Partition(parts=parts, declared_total=10_000).residue == 0


def test_that_reading_implies_the_third_axis_lost_accuracy() -> None:
    """يلزم أنّ الدقّةَ كانت ٤٩٫٦٠٪ فصارت ٤٣٫٩٠٪ — انحدارٌ ٥٫٧٠ نقطة.

    ولا ينقض ذلك الخبرَ اللغويّ: «البابُ لا يُستنتَج من بقيّة خانات الجذر»
    مقيسٌ **بسقف التغطية** وهو ارتفع حقًّا. وإنّما يقلب حكمَ **المكسب**:
    المحورُ الثالثُ مبادلةٌ خسرت، لا مكسبٌ صافٍ.
    """

    before = 1 - sum(SPLIT_BEFORE)
    after = 1 - sum(SPLIT_AFTER)
    assert rounds_to(before * 100, 2) == Fraction("49.60")
    assert before > after
    assert rounds_to((before - after) * 100, 2) == Fraction("5.70")


def test_coverage_improved_less_than_selection_worsened() -> None:
    """التغطيةُ تحسّنت ١٨٫١ والاختيارُ ساء ٢٣٫٨ — والفرقُ هو الانحدارُ نفسُه."""

    coverage_gain = (SPLIT_BEFORE[0] - SPLIT_AFTER[0]) * 100
    selection_loss = (SPLIT_AFTER[1] - SPLIT_BEFORE[1]) * 100
    assert rounds_to(coverage_gain, 1) == Fraction("18.1")
    assert rounds_to(selection_loss, 1) == Fraction("23.8")
    assert rounds_to(selection_loss - coverage_gain, 1) == Fraction("5.7")


def test_the_measured_result_still_beats_its_null_by_a_factor() -> None:
    """٤٣٫٨٢٪ مقابل ١٧٫٨٦٪ = ٢٫٤٥ أضعاف — وذلك قائمٌ مهما كان تفسيرُ القسمة."""

    ratio = REPORTED_ACCURACY / REPORTED_BASELINE
    assert rounds_to(ratio, 2) == Fraction("2.45")
    assert REPORTED_ACCURACY > REPORTED_BASELINE * 2
