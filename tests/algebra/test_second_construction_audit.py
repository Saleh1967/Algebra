"""تدقيقُ «البناء الثاني» داخليًّا: أرقامُه تُصدِّق بعضَها أو تتناقض.

**ما يُقاس ههنا وما لا يُقاس**: لا يُفحَص في هذا الملفّ صدقُ رقمٍ على مصحفٍ ولا
على مدوَّنة — لا بايتَ نصٍّ يُقرَأ. يُفحَص شيءٌ واحدٌ فقط: أنّ أرقام الوثيقة
**متّسقةٌ فيما بينها**. فإن جمع جدولٌ إلى مجموعٍ مُعلَنٍ في موضعٍ آخر، فتلك
شهادةٌ على أنّ الرقمَين من عدٍّ واحد؛ وإن تخالفا فالخبرُ في التخالف.

`A_DOCUMENT_IS_ITS_OWN_FIRST_WITNESS`: أقوى ما ههنا ليس رقمًا بل **التقاءُ
مجموعين مستقلَّين**: توزيعُ الأطوال يجمع إلى ٧٧٬٤٢٩ كلمةً و٣٤١٬٢٤٩ ذرّةً معًا،
ولا يفعل ذلك جدولٌ مُجمَّعٌ من مصادر.

`A_CONFLICT_IS_ADJUDICATED_NOT_SPLIT`: حيث تناقض النصُّ جدولًا، لا يُؤخَذ
المتوسّطُ ولا يُسكَت: يُسأل أيُّ الرقمين يُبقي المجاميعَ منطبقة، فيُحسَم.

`A_PRECISION_DISPUTE_IS_NOT_AN_ARITHMETIC_DISPUTE`: رقمان مختلفان لقياسٍ واحد
قد يكونان **كلاهما** متّسقَين مع ما نُشِر، إن كان المقامُ مطبوعًا أخشنَ من
الحاصل. وذلك عيبُ إعلانٍ لا عيبُ حساب، ويُسمّى باسمه.

والمصدرُ المُدقَّق: «البناء الثاني — الأطوار ٢–٥»، الأبواب ٥–٢٣. وكلُّ رقمٍ
أدناه منقولٌ من متنها لا مُشتَقٌّ منه.
"""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from algebra.contingency import Table2x2
from algebra.reconciliation import (
    Difference,
    Partition,
    PrintedFigure,
    Quotient,
    ReconciliationError,
    rounds_alike,
    rounds_to,
)

# تحويلُ الأرقام الهنديّة إلى لاتينيّةٍ ليُقرأ المطبوعُ رقمًا
INDIC_TO_ASCII = str.maketrans("٠١٢٣٤٥٦٧٨٩٫", "0123456789.")

# الباب ٥ — توزيع الطول بالذرّات، كما وردت سلسلتُه
ATOM_LENGTH_HISTOGRAM: dict[int, int] = {
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
DECLARED_WORDS = 77_429
PROSE_TWO_ATOM_OCCURRENCES = 8_078  # «أقصر كلمةٍ منطوقة: ذرّتان — ٨٬٠٧٨ وقوعاً»

# الباب ٦ — أشكال المقاطع على الأساس المُصلَح
SHAPE_COUNTS = (103_682, 71_794, 50_328, 106)  # CV · CVC · CVV · CVVC
SHAPE_SHARES = ("45.895", "31.780", "22.278", "0.047")
DECLARED_SYLLABLES = 225_911


def test_the_length_histogram_lands_on_two_independent_totals() -> None:
    """يجمع التوزيعُ إلى ٧٧٬٤٢٩ كلمةً و٣٤١٬٢٤٩ ذرّةً معًا، بلا فضلةٍ في أيّهما.

    وهذا أقوى ما في الوثيقة: مجموعان مستقلّان — عددُ الصفوف وثقلُها — يصيبان
    رقمَين مُعلَنَين في مواضعَ أخرى. ولا يفعل ذلك جدولٌ مُجمَّعٌ من مصادر.
    """

    words = Partition(
        parts=tuple(ATOM_LENGTH_HISTOGRAM.values()), declared_total=DECLARED_WORDS
    )
    assert words.balances
    atoms = sum(length * count for length, count in ATOM_LENGTH_HISTOGRAM.items())
    assert atoms == 341_249
    assert rounds_to(Fraction(atoms, 1_000), 0) == 341  # «من ٣٤١ ألف وقوعٍ»


def test_the_prose_two_atom_count_is_the_one_the_sums_reject() -> None:
    """يقول المتنُ ٨٬٠٧٨ ويقول الجدولُ ٨٬٠٩٨، والمجموعان يحسمان للجدول.

    ووضعُ ٨٬٠٧٨ مكانَ ٨٬٠٩٨ يُخرِج المجموعَين معًا عن المُعلَن (٧٧٬٤٠٩ و
    ٣٤١٬٢٠٩). وطرفا التوزيع يشهدان للجدول أيضًا: «أربعُ كلماتٍ» بذرّةٍ واحدة،
    و«١٢ وقوعًا» بإحدى عشرة — وكلاهما مطابقٌ لصفّه. فالتناقضُ محسومٌ لا معلَّق.
    """

    assert ATOM_LENGTH_HISTOGRAM[2] != PROSE_TWO_ATOM_OCCURRENCES
    assert ATOM_LENGTH_HISTOGRAM[2] - PROSE_TWO_ATOM_OCCURRENCES == 20
    amended = dict(ATOM_LENGTH_HISTOGRAM) | {2: PROSE_TWO_ATOM_OCCURRENCES}
    assert sum(amended.values()) != DECLARED_WORDS
    assert sum(length * count for length, count in amended.items()) != 341_249
    assert ATOM_LENGTH_HISTOGRAM[1] == 4  # «أربع كلمات فقط — يسٓ، صٓ، قٓ، نٓ»
    assert ATOM_LENGTH_HISTOGRAM[11] == 12  # «١٢ وقوعاً في ١١ صورةً»


def test_the_syllable_shapes_leave_exactly_one_residue_and_the_text_names_it() -> None:
    """الأشكالُ الأربعةُ ٢٢٥٬٩١٠ والمجموعُ ٢٢٥٬٩١١: بقيّةٌ واحدةٌ مُسمّاةٌ في المتن."""

    shapes = Partition(parts=SHAPE_COUNTS, declared_total=DECLARED_SYLLABLES)
    assert shapes.measured_total == 225_910
    assert shapes.residue == 1  # CVCCV ×١ — مَجْر۪ىٰهَا، ثغرةُ ترميزٍ مُعلَنة


def test_the_shape_shares_reproduce_but_cannot_see_the_residue() -> None:
    """النسبُ الأربعُ تُعاد بالضبط، ولا تفرّق بين ٢٢٥٬٩١٠ و٢٢٥٬٩١١."""

    for count, share in zip(SHAPE_COUNTS, SHAPE_SHARES, strict=True):
        printed = PrintedFigure(share)
        assert rounds_to(Fraction(count * 100, DECLARED_SYLLABLES), 3) == printed.value
        assert rounds_alike(
            Fraction(count * 100, DECLARED_SYLLABLES),
            Fraction(count * 100, 225_910),
            3,
        )


def test_the_shape_counts_are_the_cells_of_the_deposited_contingency_table() -> None:
    """الأشكالُ الأربعةُ هي خلايا جدول المدّ×العَجُز المودَع، لا عدٌّ آخر.

    CVC مدٌّ معدومٌ وعَجُزٌ حاضر، وCVV عكسُه؛ فالتقاطعان يطابقان الشكلين عددًا.
    وهذا يربط تدقيقَ الوثيقة بما أُودِع من قبل بدل أن يكون رقمًا يتيمًا.
    """

    table = Table2x2(103_682, 71_794, 50_328, 106)
    assert table.cells == SHAPE_COUNTS
    assert table.total == 225_910


def test_two_bases_with_one_total_move_only_between_cv_and_cvc() -> None:
    """أساسان مجموعُهما واحدٌ ونسبُهما مختلفة، ومجموعُ CV+CVC فيهما متطابقٌ حرفًا.

    «U بلا ردّ» و«UR بلا ردّ» يعطيان ٢١٥٬١٣١ كليهما، وCVV وCVVC فيهما سواء؛
    فالفرقُ محصورٌ في توزيعٍ بين CV وCVC، ومجموعُهما ٧٦٫٥٥٦٪ في الأساسين معًا.
    وهذا اتّساقٌ لا يقع مصادفةً بين جدولين مستقلّين.
    """

    first = Fraction("48.195") + Fraction("28.361")
    second = Fraction("48.527") + Fraction("28.029")
    assert first == second == Fraction("76.556")


def test_the_entropy_ledger_of_chapter_eleven_closes_on_itself() -> None:
    """أرقامُ الباب ١١ تُشتَقّ بعضُها من بعض: السقفُ والباقي والمعلومةُ والسعة."""

    assert round(math.log2(28), 4) == 4.8074  # سقفُ العَجُز
    assert round(math.log2(84), 4) == 6.3923  # سقفُ الصدر
    assert round(math.log2(2_352), 4) == 11.1997  # ٢٣٥٢ = ٨٤ × ٢٨
    assert 84 * 28 == 2_352
    assert Fraction("6.3923") + Fraction("4.8074") == Fraction("11.1997")
    # MI = H(العَجُز) − H(العَجُز | الصدر)
    assert Fraction("3.6150") - Fraction("2.8286") == rounds_to(Fraction("0.786405"), 4)
    assert round(2**2.8286, 1) == 7.1  # الأبجديةُ الفعّالة
    assert round(84 * 2**2.8286) == 597  # السعةُ الفعّالة


def test_the_mutual_information_z_is_announced_far_past_its_denominator() -> None:
    """z واحدٌ يُنشَر مرّتين برقمين، وكلاهما متّسقٌ مع مقامه المطبوع.

    الباب ١١: صفريٌّ ٠٫٠٠٧٥٧±٠٫٠٠٠٤ ← z = +١٩٦٥٫٦.
    الباب ٢٢: صفريٌّ ٠٫٠٠٧٥٧٥±٠٫٠٠٠٣٩٦ ← z = +١٩٦٩٫٢.
    والمقامُ في الأوّل بخانةٍ معنويّةٍ واحدة، فلا يحدّد من الحاصل خانةً واحدة؛
    ومع ذلك يُعلَن الحاصلُ بخمس. والمقامُ المُستلزَمُ من كلِّ رقمٍ يُطبَع بصورة
    مقامه المُعلَن بعينها — فالخلافُ في دقّة النشر لا في الحساب.
    """

    measured = PrintedFigure("0.786405")
    for null, deviation, reported, determined in (
        ("0.00757", "0.0004", "1965.6", 0),
        ("0.007575", "0.000396", "1969.2", 2),
    ):
        quotient = Quotient(
            Difference(measured, PrintedFigure(null)), PrintedFigure(deviation)
        )
        claim = quotient.claim(reported)
        assert claim.lies_in_interval
        assert claim.digits_determined == determined
        assert claim.digits_announced == 5
        assert claim.is_over_announced
        assert claim.implied_denominator_prints_as_declared


def test_the_template_measurement_differs_in_its_null_count_as_well() -> None:
    """القوالبُ: z مرّتين (−١٤٧٣٫٩ و−١٥٤٨٫٧) وصفريٌّ مرّتين (٦٧٧٫٣ و٦٧٧٫٦).

    وz العددان متّسقان كلاهما مع «±٠٫٠٠٠٣» كما في سابقه. أمّا عددُ القوالب
    الصفريّ فليس أثرَ تقريب: ٦٧٧٫٣ و٦٧٧٫٦ لا يُطبَعان بصورةٍ واحدةٍ لا بمنزلةٍ
    عشريّةٍ ولا بصحيحٍ، فهما قيمتان مختلفتان لقياسٍ واحدٍ مُعلَن.
    """

    quotient = Quotient(
        Difference(PrintedFigure("5.8916"), PrintedFigure("6.3403")),
        PrintedFigure("0.0003"),
    )
    assert quotient.determined_significant_digits == 0
    for reported in ("-1473.9", "-1548.7"):
        claim = quotient.claim(reported)
        assert claim.lies_in_interval
        assert claim.is_over_announced
        assert claim.implied_denominator_prints_as_declared
    assert not rounds_alike(Fraction("677.3"), Fraction("677.6"), 1)
    assert not rounds_alike(Fraction("677.3"), Fraction("677.6"), 0)


def test_three_reported_differences_are_consistent_but_not_reproducible() -> None:
    """ثلاثةُ فروقٍ لا تُعاد بالطرح المباشر، وكلُّها داخلَ ما يحتمله المطبوع.

    الخارجُ عن المعجم ١٨٫٠٨٪ وGT ١٧٫٠٠٪، والفرقُ المُعلَن ١٫٠٧ نقطةً والطرحُ
    يعطي ١٫٠٨. والربحُ ٤٧٫٦ ← ٢٢٫٧ مُعلَنٌ ٥٢٫٢٪ والقسمةُ تعطي ٥٢٫٣٪. وβ فرقُه
    ٩٫٩ انحرافاتٍ مُعلَنًا و٩٫٨ محسوبًا. وكلُّ واحدٍ منها يقع في مجاله، فلا
    يُنقَض — ولكنّه يُعلَن بخاناتٍ أكثرَ ممّا يحدّده ما نُشِر معه.
    """

    gap = Difference(PrintedFigure("18.08"), PrintedFigure("17.00"))
    low, high = gap.interval()
    assert gap.value == Fraction("1.08")
    assert low <= Fraction("1.07") <= high

    gain = Quotient(
        Difference(PrintedFigure("47.6"), PrintedFigure("22.7")), PrintedFigure("47.6")
    )
    gain_claim = gain.claim("0.522")
    assert rounds_to(gain.nominal() * 100, 1) == Fraction("52.3")
    assert gain_claim.lies_in_interval and gain_claim.is_over_announced

    beta = Quotient(
        Difference(PrintedFigure("0.7744"), PrintedFigure("0.7390")),
        PrintedFigure("0.0036"),
    )
    beta_claim = beta.claim("9.9")
    assert rounds_to(beta.nominal(), 1) == Fraction("9.8")
    assert beta_claim.lies_in_interval and beta_claim.is_over_announced


def test_the_rotation_line_of_chapter_seventeen_cannot_be_a_zero_difference() -> None:
    """«٥٥٫٣٣٦٨ ← ١٥٥٫٣٣٦٨ (صفر)» فرقُه مئةٌ تامّة، والباب ١٩ يحمل الصورةَ الصحيحة."""

    printed = Difference(PrintedFigure("155.3368"), PrintedFigure("55.3368"))
    assert printed.value == 100
    low, high = printed.interval()
    assert not low <= 0 <= high
    settled = Difference(PrintedFigure("155.336783"), PrintedFigure("155.336783"))
    assert settled.value == 0


def test_the_summary_chapter_prints_a_corrupted_digit_inside_a_figure() -> None:
    """الباب ٢٢ يطبع المعلومةَ بمحرف U+0868 مكانَ الرقم ٨ (U+0668).

    والباب ١١ يطبعها سليمةً ٠٫٧٨٦٤٠٥. فالرقمُ واحدٌ والعطبُ في محرفٍ واحدٍ
    يفترق عن الصحيح بخانةٍ ستّ عشريّةٍ واحدة. وأثرُه أنّ الرقمَ لم يعد يُقرأ
    عددًا: تحويلُ الأرقام الهنديّة إلى لاتينيّةٍ يُخرِج نصًّا تردّه الوحدة.
    """

    sound = "٠٫٧٨٦٤٠٥"
    corrupted = sound.replace("٨", "\u0868")
    assert corrupted != sound
    assert ord("\u0868") - ord("٨") == 0x200
    assert PrintedFigure(sound.translate(INDIC_TO_ASCII)).value == Fraction("0.786405")
    with pytest.raises(ReconciliationError):
        PrintedFigure(corrupted.translate(INDIC_TO_ASCII))


def test_the_smaller_ledgers_of_the_document_close_exactly() -> None:
    """حساباتٌ صغيرةٌ متفرّقةٌ تُعاد بالضبط، فتشهد أنّ العدّ واحدٌ لا مُجمَّع."""

    assert 3_717 + 30 == 3_747  # الباب ٦: الكلماتُ بلا صدرٍ محرّك
    assert rounds_to(Fraction(12_004 * 100, DECLARED_WORDS), 2) == Fraction("15.50")
    assert Fraction("18.98") - Fraction("15.50") == Fraction("3.48")
