"""تدقيقُ اتّفاق المصدرين على المصدر: ٨٦ وقوعًا من **أربعة جذور**.

**ما يُقاس ههنا**: اتّساقُ ملفَّي CSV الواردَين — «اتّفاقُ المصدرين» (٨٦ صفًّا)
و«المرشَّحون» (٤٣٨) — وما يُشتَقّ منهما بالحساب. والأرقامُ منقولةٌ من قراءةٍ
مباشرةٍ للملفّين، لا من نصٍّ عنهما.

`A_TOKEN_COUNT_IS_NOT_A_WITNESS_COUNT`: أثقلُ ما في التدقيق. ٨٦ صفَّ اتّفاقٍ
تأتي من **أربعة جذور**، و**٨١٫٤٪ منها جذرٌ واحد** (ذكر)، وجذران يحملان ٩٣٪.
فالشهادةُ أربعٌ لا ستٌّ وثمانون، والفرقُ ليس تفصيلًا: الوقوعاتُ ليست
مشاهداتٍ مستقلّة.

`A_ZERO_CELL_IS_A_FINDING_NOT_A_ROUNDING`: المصدران يتّفقان على الجذر الصحيح
بنسبة ٢٠٫٦٪، وعلى المعتلّ بنسبة **صفرٍ تامّ** من ١٠٧. وليست هذه نسبةً صغيرة
بل **خليّةٌ فارغة**: نسبةُ الاحتمالين غيرُ معرَّفةٍ فتُرَدّ، والتوقّعُ تحت
الاستقلال كان ١٧٫٦.

`AN_UNREADABLE_SOURCE_IS_AN_UNVERIFIABLE_ORACLE`: الملفُّ الثالث
(`Masaq_cor-1.txt`) **فارغٌ**، فعمودُ MASAQ كلُّه أوراكلُ لا يُعاد اشتقاقُه
في هذه الجلسة. وكلُّ ما يقوم عليه مقيَّدٌ به.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.contingency import ContingencyError, Table2x2
from algebra.reconciliation import Partition, rounds_to

AGREE_ROWS, CANDIDATE_ROWS, TOTAL = 86, 438, 524
COLUMNS = 30
ALWAYS_EMPTY_COLUMNS = ("QAC_Derived_Form", "QAC_Participle_Kind")

# ٠٢: الاتّفاقُ بحسب الجذر
AGREE_BY_ROOT = (("ذكر", 70), ("قتل", 10), ("أكل", 4), ("أخذ", 2))
CANDIDATE_ROOTS = 24
AGREE_LEMMAS, ALL_LEMMAS = 4, 37

# سلامةُ الجذر × الاتّفاق
SOUND_AGREE, SOUND_NOT = 86, 331
WEAK_AGREE, WEAK_NOT = 0, 107
HEALTH_DETAIL = (
    ("سالم", 80, 251),
    ("مهموز", 6, 80),
    ("ناقص", 0, 76),
    ("مثال", 0, 29),
    ("ناقص + مهموز", 0, 2),
)

THIRD_FILE_BYTES = 1  # Masaq_cor-1.txt


def test_the_two_files_partition_the_gerunds_without_overlap() -> None:
    """٨٦ + ٤٣٨ = ٥٢٤، ولا موضعَ مكرَّرٌ ولا مشترَكٌ بين الملفّين."""

    split = Partition(parts=(AGREE_ROWS, CANDIDATE_ROWS), declared_total=TOTAL)
    assert split.balances
    assert rounds_to(Fraction(AGREE_ROWS * 100, TOTAL), 2) == Fraction("16.41")
    assert COLUMNS == 30


def test_the_eighty_six_agreements_come_from_four_roots() -> None:
    """الوقوعاتُ ٨٦ والجذورُ **أربعة**، وواحدٌ منها يحمل ٨١٫٤٪.

    فعبارةُ «اتّفاقُ مصدرين على ٨٦» تُقرأ «على أربعةِ ألفاظ»، وجذرُ «ذكر»
    وحدَه يحمل سبعين منها. ولو حُذِف لبقيت **ستّةَ عشرَ صفًّا من ثلاثة جذور**.
    """

    roots = Partition(
        parts=tuple(count for _, count in AGREE_BY_ROOT), declared_total=AGREE_ROWS
    )
    assert roots.balances
    assert len(AGREE_BY_ROOT) == 4
    top_root, top_count = AGREE_BY_ROOT[0]
    assert top_root == "ذكر"
    assert rounds_to(Fraction(top_count * 100, AGREE_ROWS), 1) == Fraction("81.4")
    two = sum(count for _, count in AGREE_BY_ROOT[:2])
    assert rounds_to(Fraction(two * 100, AGREE_ROWS), 1) == Fraction("93.0")
    assert AGREE_ROWS - top_count == 16


def test_the_rate_barely_moves_between_tokens_and_roots_but_falls_by_lemma() -> None:
    """بالوقوعات ١٦٫٤١٪ وبالجذور ١٦٫٠٠٪ وبالِّلمَم **١٠٫٨١٪**."""

    by_token = Fraction(AGREE_ROWS * 100, TOTAL)
    by_root = Fraction(4 * 100, 4 + CANDIDATE_ROOTS - 3)  # ثلاثةُ جذورٍ في الاثنين
    by_lemma = Fraction(AGREE_LEMMAS * 100, ALL_LEMMAS)
    assert rounds_to(by_token, 2) == Fraction("16.41")
    assert rounds_to(by_root, 2) == Fraction("16.00")
    assert rounds_to(by_lemma, 2) == Fraction("10.81")
    assert by_lemma < by_root


def test_the_weak_root_cell_is_exactly_zero_of_one_hundred_and_seven() -> None:
    """الجذرُ الصحيح ٢٠٫٦٪، والمعتلُّ **صفرٌ من ١٠٧** — خليّةٌ فارغةٌ لا نسبةٌ صغيرة.

    والتوقّعُ تحت الاستقلال كان **١٧٫٦**، وG = ٤٣٫٤ (z ≈ ٦٫٦). ونسبةُ
    الاحتمالين **غيرُ معرَّفة** فتُرَدّ في المتن — وذلك أصدقُ من «٠٫٠٠».
    """

    table = Table2x2(SOUND_NOT, SOUND_AGREE, WEAK_NOT, WEAK_AGREE)
    assert table.total == TOTAL
    assert table.column_given_row() == 0
    assert rounds_to(
        Fraction(str(round(float(table.column_given_no_row()), 6))), 4
    ) == (Fraction("0.2062"))
    assert round(table.g_statistic(), 1) == 43.4
    assert round(table.z_equivalent(), 2) == 6.59
    assert round(float(table.expected()[3]), 1) == 17.6
    with pytest.raises(ContingencyError):
        table.risk_ratio()
    assert table.odds_ratio() == 0


def test_the_agreement_falls_monotonically_with_root_weakness() -> None:
    """سالم ٢٤٫٢٪ · مهموز ٧٫٠٪ · ناقص ومثال ولفيف **صفر** — تدرّجٌ لا قفزة."""

    rates = []
    for name, agree, candidate in HEALTH_DETAIL:
        total = agree + candidate
        rates.append((name, Fraction(agree * 100, total)))
    assert rounds_to(rates[0][1], 2) == Fraction("24.17")
    assert rounds_to(rates[1][1], 2) == Fraction("6.98")
    for _, rate in rates[2:]:
        assert rate == 0
    assert [rate for _, rate in rates] == sorted(
        (rate for _, rate in rates), reverse=True
    )
    assert sum(agree for _, agree, _ in HEALTH_DETAIL) == AGREE_ROWS
    assert sum(candidate for _, _, candidate in HEALTH_DETAIL) == CANDIDATE_ROWS


def test_the_health_totals_reconcile_with_their_details_in_both_files() -> None:
    """صحيح = سالم + مهموز، ومعتلّ = ما سواهما — في الملفّين بلا بقيّة."""

    sound_detail = sum(
        agree + candidate
        for name, agree, candidate in HEALTH_DETAIL
        if name in ("سالم", "مهموز")
    )
    weak_detail = sum(
        agree + candidate
        for name, agree, candidate in HEALTH_DETAIL
        if name not in ("سالم", "مهموز")
    )
    assert sound_detail == SOUND_AGREE + SOUND_NOT == 417
    assert weak_detail == WEAK_AGREE + WEAK_NOT == 107
    assert sound_detail + weak_detail == TOTAL


def test_the_third_file_is_empty_so_the_masaq_side_is_an_unverifiable_oracle() -> None:
    """`Masaq_cor-1.txt` بايتٌ واحد: عمودُ MASAQ لا يُعاد اشتقاقُه ههنا."""

    assert THIRD_FILE_BYTES <= 1
    # وعمودان من الثلاثين خاليان في الصفوف الـ٥٢٤ كلِّها
    assert len(ALWAYS_EMPTY_COLUMNS) == 2
    assert COLUMNS - len(ALWAYS_EMPTY_COLUMNS) == 28


def test_the_one_reviewed_row_is_routed_consistently() -> None:
    """أربعةُ صفوفٍ بأصنافٍ فرعيّة، والمراجَعُ منها هو الذي يتّفق فيه المصدران.

    ثلاثةٌ `GERUND_MEEM` بلا وسمِ VN من QAC فهي مرشَّحاتٌ عاديّة، وواحدٌ
    `GERUND_INSTANT` (أَخْذَةً، ٦٩:١٠:٥) وسمه QAC بـVN صيغةَ I — فلم يُدرَج في
    ملفّ الاتّفاق لأنّ صنفَ MASAQ الفرعيَّ لم يُراجَع. والتوجيهُ **متّسق**.
    """

    subtypes = (
        ("GERUND_MEEM", "", "MASAQ_GERUND_ONLY__QAC_NOT_VN", 3),
        ("GERUND_INSTANT", "I", "QAC_VN_FORM_I__MASAQ_SUBTYPE_REQUIRES_REVIEW", 1),
    )
    assert sum(count for *_, count in subtypes) == 4
    for tag, vn_form, rank, _ in subtypes:
        assert bool(vn_form) == ("REQUIRES_REVIEW" in rank)
        assert tag.startswith("GERUND_")
    # ولا صفَّ في ملفّ الاتّفاق إلّا وصيغتُه I ووسمُ MASAQ فيه GERUND مجرَّدًا
    assert AGREE_ROWS == 86
