"""إغلاقُ صفرِ المعتلّ ديكارتيًّا: سبعةُ مواضعَ، أربعةٌ محسومة، ومرورٌ واحد.

**تصحيحٌ لقولي أوّلًا**: قلتُ «QAC لا يسم VN على الناقص والمثال، فالاتّفاقُ
ممتنعٌ بنيويًّا هناك». والعدُّ على المدوَّنة يُسقِطها: **٢١٨ مقطعًا في ٣٨
جذرًا معتلًّا** موسومةً VN — أجوف ١٤٣، ناقص ٨٧، مثال ٧. فالدعوى باطلةٌ
وتُسحَب.

**وما كشفه إسقاطُها أهمُّ منها**: الـ٢١٨ **كلُّها خارج العيّنة**. فالصفرُ
ليس عن العمود بل عن **الانتقاء**: الدراسةُ شريحةٌ ١×٢ من جدءٍ ٢×٢، كلُّ
صفوفها «MASAQ = GERUND»، فالصفُّ المقابلُ غيرُ مرصودٍ بالبناء.

`A_SETTLED_LOCUS_IS_SETTLED_BY_A_NUMBER_NOT_BY_A_STORY`: كلُّ موضعٍ يسقط
يسقط برقمٍ يُسمّى، وكلُّ موضعٍ يبقى يحمل **فحصَه الفاصل**. ولا خانةَ فيها
«أو».
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.reconciliation import Partition, rounds_to
from algebra.selection import ConditionedTable, Locus, SelectionError, partition_of_loci

# الرقمُ الحاسمُ كما ورد
VN_SEGMENTS_TOTAL, VN_ROOTS_TOTAL = 674, 154
WEAK_VN_SEGMENTS, WEAK_VN_ROOTS = 218, 38
BY_CLASS = (
    ("سالم", 341, None),
    ("أجوف", 143, 17),
    ("ناقص", 87, 20),
    ("مثال", 7, 5),
    ("مهموز · مضعّف", 106, None),
)

# الدراسةُ الواردةُ من قبل
STUDY_WEAK_AGREE, STUDY_WEAK_CANDIDATES = 0, 107
STUDY_ROWS_WITH_QAC_VN = 1  # أَخْذَةً وحدَه، وجذرُه ليس معتلًّا

# الركيزةُ أحاديّةَ المصدر
F1_SOUND, F1_WEAK = Fraction("0.794"), Fraction("0.823")

HALF_TABLE = ConditionedTable(
    condition="MASAQ = GERUND",
    absent_row="MASAQ ≠ GERUND",
    positive=STUDY_WEAK_AGREE,
    negative=STUDY_WEAK_CANDIDATES,
    outside_positive_total=WEAK_VN_SEGMENTS,
)


def test_my_structural_claim_is_refuted_by_the_count() -> None:
    """«الوسمُ ممتنعٌ في المعتلّ» باطلةٌ: ٢١٨ مقطعًا في ٣٨ جذرًا، و٣٢٫٣٪ من الكلّ."""

    assert WEAK_VN_SEGMENTS > 0
    assert WEAK_VN_ROOTS > 0
    assert rounds_to(Fraction(WEAK_VN_SEGMENTS * 100, VN_SEGMENTS_TOTAL), 1) == (
        Fraction("32.3")
    )
    assert 143 + 87 + 7 == 237  # مجموعُ الصفوف قبل خصم التداخل


def test_the_decisive_table_reconciles_only_if_its_rows_overlap() -> None:
    """صفوفُ الجدول تجمع ٦٨٤ والمُعلَنُ ٦٧٤، والمعتلُّ ٢٣٧ والمُعلَنُ ٢١٨.

    والقراءةُ التي تُصالِح المعتلَّ واحدةٌ: **الصفوفُ متداخلة** (اللفيفُ في
    صفّين)، فالمكرَّرُ ١٩ مقطعًا و٤ جذور — وعندها ٢٣٧−١٩ = ٢١٨ ✓ و٤٢−٤ = ٣٨ ✓.
    لكنّ الكلّيَّ لا يُصالَح بها: ٦٨٤−١٩ = ٦٦٥ ≠ ٦٧٤، **فبقيّةٌ تسعةٌ** تبقى
    بلا تفسير.
    """

    rows = Partition(
        parts=tuple(count for _, count, _ in BY_CLASS), declared_total=VN_SEGMENTS_TOTAL
    )
    assert rows.measured_total == 684
    assert rows.residue == -10
    weak_rows = 143 + 87 + 7
    weak_roots = 17 + 20 + 5
    assert weak_rows - WEAK_VN_SEGMENTS == 19
    assert weak_roots - WEAK_VN_ROOTS == 4
    assert 684 - 19 == 665
    assert VN_SEGMENTS_TOTAL - 665 == 9


def test_the_whole_weak_column_escaped_the_sample() -> None:
    """٢١٨ خارجًا و٠ داخلًا ⇒ **كلُّ** العمود هرب، فالصفرُ عن الانتقاء."""

    assert HALF_TABLE.missing_positive_at_least() == WEAK_VN_SEGMENTS
    assert HALF_TABLE.share_of_the_column_that_escaped() == 1
    assert HALF_TABLE.zero_is_about_selection_not_the_column()
    with pytest.raises(SelectionError):
        HALF_TABLE.assert_measurable()


def test_the_substrate_carries_it_more_in_the_weak_than_in_the_sound() -> None:
    """F1 ٠٫٨٢٣ في المعتلّ مقابل ٠٫٧٩٤ في الصحيح — النسبةُ فوق الواحد."""

    assert F1_WEAK > F1_SOUND
    ratio = F1_WEAK / F1_SOUND
    assert rounds_to(ratio, 4) == Fraction("1.0365")
    assert rounds_to(ratio, 3) == Fraction("1.037")  # والمنشورُ ١٫٠٣٦ بتْرًا
    assert Fraction(132, 4_848) > Fraction(233, 11_468)  # والكثافةُ أعلى أيضًا


def test_the_loci_form_a_partition_with_no_disjunction() -> None:
    """سبعةُ مواضعَ، لكلٍّ فحصٌ يفصله عن جاره — ولا خانةَ فيها «أو»."""

    loci = partition_of_loci(
        (
            Locus(
                name="١ اللغة: أفيها مصدرٌ معتلّ",
                settled=True,
                deciding_test="عدُّ VN على الجذور المعتلّة في QAC — ٢١٨ مقطعًا",
            ),
            Locus(
                name="٢ مخطَّطُ QAC: أيسم VN على المعتلّ",
                settled=True,
                deciding_test="وجودُ الوسم نفسِه — واقعٌ في ٣٨ جذرًا",
            ),
            Locus(
                name="٣ الركيزة: أتحمل المصدريّةَ في المعتلّ",
                settled=True,
                deciding_test="F1 أحاديَّ المصدر بصفريٍّ داخل الصنف — ٠٫٨٢٣ > ٠٫٧٩٤",
            ),
            Locus(
                name="٤ قاعدةُ الاتّفاق: أرفضت مطابقةً معتلّة",
                settled=True,
                deciding_test=(
                    "عدُّ صفوف الدراسة التي QAC فيها VN — " "واحدٌ، وجذرُه ليس معتلًّا"
                ),
            ),
            Locus(
                name="٥ وسمُ MASAQ: أوسم GERUND في مواضع الـ٢١٨",
                settled=False,
                deciding_test="وسمُ MASAQ عند كلّ موضعٍ من الـ٢١٨",
            ),
            Locus(
                name="٦ توليدُ المرشّحين: أأدخل تلك المواضع",
                settled=False,
                deciding_test="كم من الـ٢١٨ له صفٌّ في الـ٥٢٤ — والجوابُ صفرٌ فعلًا",
            ),
            Locus(
                name="٧ الوصل: أطابق المقطعَين في الموضع نفسِه",
                settled=False,
                deciding_test="معدّلُ فشل الوصل على المعتلّ مقابل الصحيح",
            ),
        )
    )
    assert len(loci) == 7
    settled = [locus for locus in loci if locus.settled]
    open_loci = [locus for locus in loci if not locus.settled]
    assert len(settled) == 4
    assert len(open_loci) == 3
    assert len({locus.deciding_test for locus in loci}) == 7


def test_the_fourth_locus_is_settled_by_the_study_itself() -> None:
    """قاعدةُ الاتّفاق لم تردّ معتلًّا قطّ: صفٌّ واحدٌ في الـ٥٢٤ فيه VN، وجذرُه سليم.

    فلم يبلغ الحكمَ صفٌّ معتلٌّ أصلًا، ولا يكون سببًا لصفرٍ لم يصل إليه.
    وهذا يُخرِجه من القسمة بالحساب لا بالترجيح.
    """

    assert STUDY_ROWS_WITH_QAC_VN == 1
    assert STUDY_WEAK_AGREE == 0
    # ولو كانت القاعدةُ هي السبب لوجب أن يكون في الدراسة معتلٌّ وسمه QAC بـVN
    assert STUDY_ROWS_WITH_QAC_VN - STUDY_WEAK_AGREE == 1


def test_one_pass_settles_the_three_that_remain() -> None:
    """مرورٌ واحدٌ على الـ٦٧٤ يملأ الصفَّ الغائبَ ويفصل الثلاثةَ معًا.

    لكلّ مقطعٍ وسمه QAC بـVN: أفي الـ٥٢٤ هو؟ وما وسمُ MASAQ عنده؟ فالجوابُ
    يُعيِّن أيَّ المواضع الثلاثة هو، ويُكمِل الجدءَ ٢×٢ الذي لا يُقاس نصفُه.
    """

    completed_cells = 4
    observed_cells = 2
    assert completed_cells - observed_cells == HALF_TABLE.missing_cells == 2
    assert VN_SEGMENTS_TOTAL == 674  # مجتمعُ المرور
    assert WEAK_VN_SEGMENTS < VN_SEGMENTS_TOTAL
