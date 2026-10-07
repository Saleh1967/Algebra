"""أبوابُ المعنى الثلاثة، مشتقّةً من بتّتين لا مسرودةً قائمةً.

**الجملةُ المُثبَتةُ في الدفتر**: المعنى في هذا المشروع ثلاثةٌ لا واحد —
**ظلالٌ مشهودةٌ تُقاس، وذوقٌ عربيٌّ يُروى، وماهيةٌ تُحجَب**. وكلُّ ما تعدّى
الثلاثةَ فهو **بابٌ رابعٌ مردود**: خبرٌ عن غير محسوسٍ شُبِك بالشاهد.

`THE_THREE_DOORS_ARE_A_PRODUCT_NOT_A_LIST`: والثلاثةُ لا تُحفَظ عددًا، بل
تُشتَقّ من **بتّتين مُعلَنتين** وعمودَي حكم: أتقع المادّةُ تحت الحسّ؟ وأسندُها
شاهدٌ عن شاهدٍ أم غائبٌ مقيسٌ عليه؟ ثمّ: أتُعَدّ بمقامٍ أم تُروى بسند؟ فالجدولُ
ثمانِ خاناتٍ تامّةٍ، ستٌّ مملوءةٌ واثنتان ممتنعتان بالتركيب — إذ لا يُعَدّ
بمقامٍ ما لا يقع تحت الحسّ. والقائمةُ تُنسى، والجداءُ يُفحَص.

`ONLY_ONE_CELL_IS_THE_COLUMN_OF_ATOMS_AND_IT_NEEDS_BOTH_BITS`: وخانةٌ واحدةٌ
من الثمان هي عمودُ الذرات: **مشهودٌ** و**شاهدٌ عن شاهد** و**يُعَدّ بمقام**.
فسقوطُ بتّةٍ واحدةٍ يُخرِج المصدرَ منها، ولا يُعوَّض بجودة صنعته.

`THE_OBJECTION_IS_OVER_A_DENOMINATOR_COUNTED_IN_ANOTHER_TONGUE`: وموضعُ
الاعتراض على شبكات المعاني المستوردة يُحرَّر ههنا تحريرًا لا يزيد على ما
يَثبُت: العيبُ أنّ **جردَ المعاني نفسَه** — الخاناتُ التي تُوزَّع عليها
الألفاظ — مأخوذٌ من لسانٍ آخرَ ثمّ أُنزِلت عليه العربيّة. فهو المجالُ
المُعدَّدُ في غير لسانه، لا حكمٌ على من صنعه ولا على جنسيّته. وذلك أقوى
للاعتراض وأصدق: عيبُ مقامٍ لا عيبُ صانع.

`A_REFUTABLE_TAG_AND_AN_UNREFUTABLE_ONE_ARE_NOT_TWO_GRADES_OF_ONE_THING`:
وبه يفترق الوسمُ الصرفيُّ عن جرد المعاني. وسمُ الجذر والعدد والجنس **خبرٌ
عن النصّ يُكذِّبه النصُّ** إن أخطأ، فيُرَدّ درايةً ويُعَدّ في الميزان. وخانةُ
المعنى المستوردةُ لا يكذّبها النصُّ العربيُّ ولا يصدّقها — فليست في مادّة
الميزان أصلًا. والفرقُ فرقُ **قابليّة الردّ**، لا فرقُ درجةٍ في الثقة.

`THREE_OF_THE_FOUR_SHADOWS_ARE_CARRIED_NOT_REPRODUCED_HERE`: وظلالُ
الاستعمال الأربعةُ تُسمّى بمنازلها: واحدٌ منها له قياسٌ أوّلُ في هذا
المستودع، وثلاثةٌ **منقولةٌ عن تقارير** لم تُعَد ههنا. وخلطُ المنقول
بالمُعاد هو النقلُ الصامتُ الذي بُنِي `provenance` لردّه.
"""

from __future__ import annotations

import pytest

from algebra.assignment import Assignment, AssignmentError
from algebra.results import Vacancy

SENSED = "مشهودٌ يقع تحت الحسّ"
UNSENSED = "غيرُ مشهودٍ لا يقع تحته"
NATIVE_WITNESS = "شاهدٌ عن شاهد"
TRANSFERRED = "غائبٌ مقيسٌ على شاهد"

ROWS: tuple[str, ...] = (
    f"{SENSED} · {NATIVE_WITNESS}",
    f"{SENSED} · {TRANSFERRED}",
    f"{UNSENSED} · {NATIVE_WITNESS}",
    f"{UNSENSED} · {TRANSFERRED}",
)

COUNTED = "يُعَدّ بمقامٍ مُعلَن"
NARRATED = "يُروى بسندٍ مُسمًّى"
COLUMNS: tuple[str, ...] = (COUNTED, NARRATED)

ATOMS = "عمودُ الذرات — ظلالُ الاستعمال والوسمُ القابلُ للردّ"
TRADITION = "العمودُ الثاني — الذوقُ العربيّ مرويًّا بسنده"
REJECTED_GRID = "مردودٌ — العددُ يخرج خبرًا عن الشبكة المستوردة لا عن العربيّة"
REJECTED_NARRATOR = "مردودٌ — راوٍ من غير أهل اللسان المرويِّ عنه"
VEILED_QUIDDITY = "محجوبٌ — بابُ الماهيات: ما وراء الطبيعة"
VEILED_OTHERS = "محجوبٌ — بابُ نفوس الغير"

IMPOSSIBLE_CELLS: tuple[tuple[str, str], ...] = (
    (ROWS[2], COUNTED),
    (ROWS[3], COUNTED),
)
"""لا يُعَدّ بمقامٍ ما لا يقع تحت الحسّ؛ وهي استحالةٌ مُعلَنةٌ قابلةٌ للنقض."""

DOORS = Assignment(
    rows=ROWS,
    columns=COLUMNS,
    cells=(
        (ROWS[0], COUNTED, ATOMS),
        (ROWS[0], NARRATED, TRADITION),
        (ROWS[1], COUNTED, REJECTED_GRID),
        (ROWS[1], NARRATED, REJECTED_NARRATOR),
        (ROWS[2], NARRATED, VEILED_QUIDDITY),
        (ROWS[3], NARRATED, VEILED_OTHERS),
    ),
    forbidden=IMPOSSIBLE_CELLS,
)

# ظلالُ الاستعمال الأربعةُ ومنازلُها ههنا: أمُعادةٌ في هذا المستودع أم منقولة؟
SHADOWS: tuple[tuple[str, str, bool], ...] = (
    ("حمولةُ الجذر", "z = ٩٫١", False),
    ("ثباتُ الوضع", "ρ = ٠٫٦٢", False),
    ("آيةُ النظم", "٤٠٫٧٪", False),
    ("نقضُ الكفاية الصرفيّة", "٤٣٫٨٢٪ مقابل ١٧٫٨٦٪", True),
)


def test_the_grid_of_meaning_is_total_over_its_declared_bits() -> None:
    """ثمانِ خاناتٍ: ستٌّ مملوءةٌ واثنتان ممتنعتان — ولا خانةَ منسيّة."""

    assert len(ROWS) * len(COLUMNS) == 8
    assert DOORS.covers_the_grid()
    assert DOORS.filled == 6
    assert DOORS.forbidden_count == 2

    # والممتنعُ دعوًى تُعلَن لا فراغٌ يُسكَت عنه
    assert Vacancy.IMPOSSIBLE.value == "استحالةٌ مُعلَنةٌ قابلةٌ للنقض"
    # وسؤالُ الممتنع يُرَدّ بتسميته، لا بإرجاع فراغ
    for row, column in IMPOSSIBLE_CELLS:
        with pytest.raises(AssignmentError):
            DOORS.value_at(row, column)
        assert column == COUNTED and row.startswith(UNSENSED)


def test_only_one_cell_is_the_column_of_atoms_and_it_needs_both_bits() -> None:
    """عمودُ الذرات خانةٌ واحدة، وشرطُها بتّتان لا واحدة."""

    atoms = [
        (row, column)
        for row, column, value in DOORS.cells
        if value.startswith("عمودُ الذرات")
    ]
    assert len(atoms) == 1
    row, column = atoms[0]
    assert row == f"{SENSED} · {NATIVE_WITNESS}"
    assert column == COUNTED

    # وسقوطُ أيّ البتّتين يُخرِج من الخانة: الجارتان ليستا ذرّات
    assert not DOORS.value_at(ROWS[1], COUNTED).startswith("عمودُ الذرات")
    assert not DOORS.value_at(ROWS[0], NARRATED).startswith("عمودُ الذرات")


def test_three_doors_stand_and_a_fourth_is_refused() -> None:
    """ثلاثةٌ مقبولةُ الحكم — تُقاس وتُروى وتُحجَب — ورابعٌ مردود."""

    standings = {value.split(" — ")[0] for _, _, value in DOORS.cells}
    assert standings == {"عمودُ الذرات", "العمودُ الثاني", "مردودٌ", "محجوبٌ"}

    admitted = {one for one in standings if one != "مردودٌ"}
    assert len(admitted) == 3

    veiled = [value for _, _, value in DOORS.cells if value.startswith("محجوبٌ")]
    assert len(veiled) == 2  # الماهيّاتُ ونفوسُ الغير، وكلتاهما تُروى ولا تُعَدّ


def test_an_imported_sense_grid_misses_the_atoms_cell_under_every_reading() -> None:
    """ثلاثُ قراءاتٍ لشبكة المعاني المستوردة، ولا واحدةَ تبلغ خانةَ الذرات."""

    readings = {
        "خبرٌ عن معنًى في النفس": ROWS[3],
        "خبرٌ عن ذوقِ غيرِ أهل اللسان": ROWS[1],
        "وزنُ مواضعَ مشهودةٍ بوسمٍ مستورد": ROWS[1],
    }
    assert len(set(readings.values())) == 2

    for row in readings.values():
        assert row != f"{SENSED} · {NATIVE_WITNESS}"

    # وأضعفُ تسليمٍ — المواضعُ مشهودةٌ — يبقى مردودًا بالبتّة الثانية وحدَها
    weakest = DOORS.value_at(ROWS[1], COUNTED)
    assert weakest.startswith("مردودٌ")
    assert "الشبكة المستوردة" in weakest


def test_the_difference_from_a_morphological_tag_is_refutability() -> None:
    """الوسمُ يُكذِّبه النصُّ فيُعَدّ، والخانةُ المستوردةُ لا يكذّبها فتخرج."""

    refutable_by_the_text = ("الجذر", "العدد", "الجنس")
    assert len(refutable_by_the_text) == 3

    # والعيبُ في المستورد مقامٌ عُدِّد في لسانٍ آخر، لا صانعٌ يُطعَن فيه
    defect = "جردُ المعاني مأخوذٌ من لسانٍ آخرَ ثمّ أُنزِلت عليه العربيّة"
    assert "صانع" not in defect and "جنسيّة" not in defect
    assert "جردُ المعاني" in defect

    # فالفرقُ فرقُ قابليّة ردٍّ لا درجةُ ثقة
    assert Vacancy.REFUSED.value == "رُدَّت بقياسٍ جرى"
    assert Vacancy.REFUSED is not Vacancy.IMPOSSIBLE


def test_three_of_the_four_shadows_are_carried_not_reproduced_here() -> None:
    """أربعةُ ظلالٍ: واحدٌ له قياسٌ أوّلُ ههنا، وثلاثةٌ منقولةٌ عن تقارير."""

    assert len(SHADOWS) == 4
    reproduced = [name for name, _, here in SHADOWS if here]
    carried = [name for name, _, here in SHADOWS if not here]
    assert len(reproduced) == 1 and len(carried) == 3
    assert reproduced == ["نقضُ الكفاية الصرفيّة"]

    # والمنقولُ يُنشَر منقولًا: منزلتُه «فحصُه مُعيَّنٌ ولم يُجرَ» ههنا
    assert Vacancy.UNRUN.value == "فحصُها مُعيَّنٌ ولم يُجرَ"
    assert len({figure for _, figure, _ in SHADOWS}) == 4
