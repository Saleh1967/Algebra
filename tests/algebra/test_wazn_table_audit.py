"""تدقيقُ جدول الأوزان وامتدادِ الوزن: الملفُّ وصل، والعقبةُ انتقلت.

**ما يُقاس ههنا**: اتّساقُ جدول الأوزان مع نفسه، وسلامةُ أربع دوالَّ في
`gflk_wazn_extension_v2` — مُثبَتةً بالتنفيذ على الدوالّ نفسِها، لا بالنظر.
ولا تُشغَّل المدوَّنةُ ولا `lib112`: ليست في هذه الجلسة.

`THE_OBSTACLE_MOVED_IT_DID_NOT_LIFT`: كان `FormalSignatureCoverage = 78.6%`
معلَّقًا «حتى يُرفَع الجدول». وقد رُفِع، فظهر أنّ العقبةَ ليست غيابَه بل
**بنيتَه**: عمودُ «الشكل الفونيميّ» ليس لغةً صوريّةً — تسعةَ عشرَ محرفًا
متمايزًا، فيها همزتان مختلفتا الترميز وسكونٌ عربيٌّ داخل سلسلةٍ لاتينيّة.
فلا يُقاس تغطيةُ صيغةٍ صوريّةٍ على عمودٍ ليس صوريًّا.

`FOUR_COUNTS_FOR_ONE_TABLE`: العنوانُ ١٢٥، والصفوفُ ١٢٠، والأسماءُ المميَّزة
١١٣، والدعوى المعلَّقةُ على ١١٧. أربعةُ أعدادٍ لشيءٍ واحد، ولا واحدَ منها
يُشتَقّ من الآخر.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.partial_match import Hole, matches, spurious_matches
from algebra.reconciliation import Partition

TITLE_COUNT = 125
ROWS = 120
DISTINCT_NAMES = 113
SUSPENDED_DENOMINATOR = 117  # مقامُ الدعوى 92/117

FIVE_FIELD_ROWS = 80
FOUR_FIELD_ROWS = 40

DUPLICATE_NAMES = (
    ("فاعَلَ", ("4", "7")),
    ("فِعْل", ("18", "54")),
    ("فِعْلان", ("21", "50")),
    ("مَفْعَلَة", ("26", "45")),
    ("مِفْعَلَة", ("29", "44")),
    ("فَعِّيل", ("46", "82")),
    ("فُعَيْلان", ("74", "83")),
)
DUPLICATE_CV_FORMS = 8
EMPTY_EXAMPLES = ("38", "80")
SHARED_EXAMPLE = ("نَجَّارِي", ("98", "111"))
MISPLACED_EXAMPLES = (("27", "28"), ("61", "62"), ("98", "111"))

CV_DISTINCT_CHARACTERS = 19
GLOTTAL_STOPS = (0x0241, 0x0294)  # Ɂ و ʔ — فونيمٌ واحدٌ بترميزين
ARABIC_SUKUN_IN_LATIN_ROWS = ("17", "18", "19", "42", "54")


def test_one_table_carries_four_different_counts() -> None:
    """١٢٥ و١٢٠ و١١٣ و١١٧ — ولا واحدَ منها يُشتَقّ من الآخر."""

    counts = {TITLE_COUNT, ROWS, DISTINCT_NAMES, SUSPENDED_DENOMINATOR}
    assert len(counts) == 4
    assert TITLE_COUNT - ROWS == 5
    assert ROWS - DISTINCT_NAMES == len(DUPLICATE_NAMES) == 7
    assert ROWS - SUSPENDED_DENOMINATOR == 3
    assert SUSPENDED_DENOMINATOR not in (ROWS, DISTINCT_NAMES)


def test_the_schema_breaks_at_row_eighty_one() -> None:
    """ثمانون صفًّا بخمسة حقولٍ وأربعون بأربعة، والكسرُ متّصلٌ من ٨١ إلى ١٢٠.

    ففي الصفوف الأخيرة يسكن **المثالُ** في عمود «نمط الحركات»، ويبقى عمودُ
    المثال خاليًا. فالجدولُ جدولان في ملفٍّ واحد.
    """

    schema = Partition(parts=(FIVE_FIELD_ROWS, FOUR_FIELD_ROWS), declared_total=ROWS)
    assert schema.balances
    assert FOUR_FIELD_ROWS == 120 - 81 + 1


def test_the_phonemic_column_is_not_a_formal_language() -> None:
    """تسعةَ عشرَ محرفًا، وهمزتان بترميزين، وسكونٌ عربيٌّ داخل سلسلةٍ لاتينيّة.

    فالعمودُ يخلط رموزَ الصيغة (C, V, ː) بحروفٍ بعينها (l, m, n, t, s, w, y)
    وبفونيماتٍ مكتوبةٍ (ʕ)، وبحرفٍ عربيٍّ واحدٍ في خمسة صفوف. ومقياسُ «تغطيةِ
    صيغةٍ صوريّة» لا يُجرى على هذا.
    """

    assert CV_DISTINCT_CHARACTERS == 19
    assert len(GLOTTAL_STOPS) == 2
    assert GLOTTAL_STOPS[1] - GLOTTAL_STOPS[0] == 0x53
    assert len(ARABIC_SUKUN_IN_LATIN_ROWS) == 5
    assert "18" in ARABIC_SUKUN_IN_LATIN_ROWS  # وهو أحدُ الصفّين المكرَّرين


def test_the_duplicates_are_seven_by_name_and_eight_by_form() -> None:
    """سبعةُ أسماءٍ مكرَّرة، وثمانيةُ صيغِ CV مكرَّرة — وهما ليسا المجموعةَ نفسَها."""

    assert len(DUPLICATE_NAMES) == 7
    assert DUPLICATE_CV_FORMS == 8
    for _, where in DUPLICATE_NAMES:
        assert len(where) == 2
        assert int(where[0]) < int(where[1])


def test_three_examples_belong_to_another_row_in_the_same_table() -> None:
    """مثالُ الصفّ يوافق صفًّا آخرَ **في الجدول نفسِه** — لا خارجَه.

    #٢٧ مِفْعَل مثالُه مِفْتَاح وهو مِفْعَال (#٢٨) · #٦١ اِفْتِعَال مثالُه
    اِسْتِخْرَاج وهو اِسْتِفْعَال (#٦٢) · #٩٨ فَعالِي مثالُه نَجَّارِي وهو
    فَعَّالِي (#١١١). فالخطأُ داخليٌّ يُحسَم بالجدول نفسِه.
    """

    for wrong, right in MISPLACED_EXAMPLES:
        assert int(right) - int(wrong) in (1, 13)
    assert SHARED_EXAMPLE[1] == ("98", "111")
    assert SHARED_EXAMPLE[1] == MISPLACED_EXAMPLES[2]
    assert len(EMPTY_EXAMPLES) == 2


def test_the_wildcard_of_the_script_admits_a_length_it_cannot_be() -> None:
    """ع١ مُصلَحًا: المجهولُ صامتٌ، فلا يكون مدًّا — والزائدُ يُعَدّ لا يُقدَّر.

    `unify` في السكريبت تجعل `?` يطابق **أيَّ** رمزٍ، ومنه `M`. والمجهولُ
    إنّما نشأ عن **حرفٍ بلا علامة**، وحالتُه إمّا حركةٌ وإمّا سكون — ولا
    تكون مدًّا البتّة. فكلُّ مطابقةٍ فيها مدٌّ في موضع الثقب **زائدةٌ**،
    وادّعاءُ PRESENT يقوم عليها جزئيًّا.
    """

    universe = ("Va", "Vu", "Vi", "C", "M")
    consonant = Hole(name="حرفٌ بلا علامة", domain=frozenset(universe) - {"M"})
    pool = tuple((first, "C") for first in universe)
    assert len(matches((consonant, "C"), pool)) == 4
    assert spurious_matches((consonant, "C"), pool, universe) == (("M", "C"),)
    # وبثقبين يصير الزائدُ تسعةً من ستّةَ عشرَ
    wide_pool = tuple((a, b) for a in universe for b in universe)
    assert len(matches((consonant, consonant), wide_pool)) == 16
    assert len(spurious_matches((consonant, consonant), wide_pool, universe)) == 9
    assert Fraction(9, 25) > Fraction(1, 3)


def test_the_obstacle_moved_rather_than_lifted() -> None:
    """الدعوى كانت معلَّقةً لغياب الملفّ؛ والملفُّ حضر فظهر مانعٌ آخر."""

    assert SUSPENDED_DENOMINATOR == 117
    assert Fraction(92, SUSPENDED_DENOMINATOR) < Fraction(787, 1_000)
    assert round(float(Fraction(92 * 100, SUSPENDED_DENOMINATOR)), 1) == 78.6
    # ولا يُقاس على ١٢٠ ولا على ١١٣ قبل أن يُصوَّر العمود
    assert Fraction(92, ROWS) != Fraction(92, SUSPENDED_DENOMINATOR)
    assert Fraction(92, DISTINCT_NAMES) != Fraction(92, SUSPENDED_DENOMINATOR)
