"""جداءُ الكتاب: أربعُ خانٍ وسبعةُ أقسام — والامتناعُ مُعلَنٌ بعلّةٍ تُنقَض.

**ما يُقاس ههنا**: بنيةُ التقسيم وحسابُها. ولا دعوى عن المصحف في هذا الملفّ
إلّا نِسَبَ الملء المنقولة، وهي تُعاد بالجمع لا تُصدَّق.

`A_TOTAL_PRODUCT_IS_NOT_A_COMPLETE_TAXONOMY`: الجداءُ (كثرةُ اللفظ × كثرةُ
المعنى) **تامٌّ**: أربعُ خانٍ كلُّها مملوءة، وصفرُ فراغ. ومع ذلك **لا يصنّف
السبعة**: المشتركُ والمنقولُ والحقيقةُ/المجاز تسكن خليّةً واحدةً بعينها، ولا
يفرّق بينها إحداثيّاها. فتمامُ الجداء غيرُ تمامِ التقسيم، والخلطُ بينهما هو
أن يُحسَب الجداءُ حاسمًا وهو **مُوقِعٌ** فقط.

`THE_SEPARATING_VARIABLE_IS_NOT_AN_AXIS_HERE`: والذي يفصل الثلاثةَ **الوضعُ
والاشتهار** — وهو ليس محورًا في هذا الجداء ولا يُشتَقّ من محورَيه. فإدخالُه
محورًا ثالثًا بثلاث قيمٍ يجعل الخانات **اثنتَي عشرةَ**، والمُسمّى سبعةٌ،
فيلزم **إعلانُ خمسِ خانٍ** — وذلك ثمنُ التمام لا عيبٌ فيه.

`THE_BOOK_FORBIDS_A_CELL_AND_NAMES_ITS_REASON`: وفي الجداء الثلاثيّ
(لفظ/معنى × مفرد/مركّب × مستعمل/مهمل) ثمانيَ خانات، يُعلِن الكتابُ امتناعَ
واحدةٍ بنصِّه: «وهذا القسمُ غيرُ موضوع… لأنّ الغرضَ من التركيب هو الإفادة».
**فالإفادةُ شرطٌ يمنع خليّةً، لا محتوى خليّة** — وذلك جوابٌ بنيويٌّ لا وصفيّ.
ودعواه **قابلةٌ للنقض** بمركّبٍ مهملٍ يُفيد، فهي في موضعها من المكتبة.

`FIVE_NAMED_AND_ONE_FORBIDDEN_LEAVE_TWO_UNSPOKEN`: وثمانيةٌ ناقصَ خمسةٍ
مُسمّاةٍ وواحدةٍ ممتنعةٍ = **اثنتان** لم يُقَل فيهما شيء. وهما موضعان لا
مجهولان — وذلك كلُّ ما يفعله الجداء، وهو كثير.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.reconciliation import Partition
from algebra.results import Axis, Placement, Product, ResultsError, Vacancy

# نِسَبُ الملء المنقولة، بالعُشر من المئة
FILL: dict[str, int] = {
    "متباين": 916,
    "مترادف": 68,
    "منفرد": 13,
    "مشترك": 3,
}

NAMED_DIVISIONS = 7
CELLS_TWO_WAY = 4
CELLS_THREE_WAY = 8
NAMED_IN_THE_THREE_WAY = 5
FORBIDDEN_IN_THE_THREE_WAY = 1


def test_the_two_by_two_is_total_and_its_cells_are_all_filled() -> None:
    """أربعُ خانٍ، وأربعُ نِسَبٍ تجمع إلى المئة تمامًا بلا بقيّة."""

    grid = Product(
        axes=(
            Axis(name="كثرةُ اللفظ", values=("واحد", "متعدّد")),
            Axis(name="كثرةُ المعنى", values=("واحد", "متعدّد")),
        )
    )
    assert grid.size == CELLS_TWO_WAY
    assert len(set(grid.points())) == CELLS_TWO_WAY

    assert Partition(parts=tuple(FILL.values()), declared_total=1_000).residue == 0
    assert sum(FILL.values()) == 1_000
    assert FILL["متباين"] > sum(
        count for name, count in FILL.items() if name != "متباين"
    )


def test_a_total_product_still_fails_to_separate_three_divisions() -> None:
    """ثلاثةٌ من السبعة في خليّةٍ واحدة، ولا يفرّق بينها إحداثيّاها."""

    sharing_one_cell = ("مشترك", "منقول", "حقيقةٌ ومجاز")
    assert len(sharing_one_cell) == 3
    assert len(set(sharing_one_cell)) == 3

    # أربعُ خانٍ لا تحمل سبعةَ أسماءٍ متمايزة
    assert CELLS_TWO_WAY < NAMED_DIVISIONS
    assert NAMED_DIVISIONS - CELLS_TWO_WAY == 3
    # وهو بعينه فائضُ الخليّة الواحدة: ثلاثةٌ في موضعِ واحد
    assert len(sharing_one_cell) == NAMED_DIVISIONS - CELLS_TWO_WAY


def test_a_third_axis_of_three_values_costs_five_declared_vacancies() -> None:
    """٤ × ٣ = ١٢ خانة، والمُسمّى سبعةٌ، فخمسٌ تُعلَن — وذلك ثمنُ التمام."""

    with_third = Product(
        axes=(
            Axis(name="كثرةُ اللفظ", values=("واحد", "متعدّد")),
            Axis(name="كثرةُ المعنى", values=("واحد", "متعدّد")),
            Axis(
                name="الوضعُ والاشتهار", values=("وضعٌ أوّل", "نقلٌ غالب", "اشتهارٌ بلا نقل")
            ),
        )
    )
    assert with_third.size == 12
    assert with_third.size - NAMED_DIVISIONS == 5

    # ومحورٌ بقيمتين لا يكفي: ثمانٍ دون سبعةٍ بواحدةٍ فقط، والفاصلُ ثلاثيّ
    assert 4 * 2 - NAMED_DIVISIONS == 1
    assert 4 * 2 < 4 * 3


def test_the_forbidden_cell_is_a_refutable_claim_not_an_exemption() -> None:
    """امتناعُ الخليّة الثامنة يُودَع بعلّته وبما ينقضه — فهو في موضعه."""

    cell = Placement(
        coordinate=("لفظ", "مركّب", "مهمل"),
        forbidden_because=("مركّبٌ مهملٌ غيرُ موضوع، لأنّ الغرضَ من التركيب هو الإفادة"),
        refuted_by="مركّبٌ مهملٌ يُفيد، أو تركيبٌ موضوعٌ لغير الإفادة",
    )
    assert cell.vacancy is Vacancy.IMPOSSIBLE
    assert "الإفادة" in cell.forbidden_because

    # والامتناعُ لا يُقبَل بلا ناقضٍ مُسمًّى، وإلّا كان إعفاءً من الملء
    with pytest.raises(ResultsError, match="بلا ناقضٍ"):
        Placement(
            coordinate=("لفظ", "مركّب", "مهمل"),
            forbidden_because="غيرُ موضوعٍ لأنّ الغرضَ الإفادة",
        )


def test_information_is_the_condition_that_forbids_not_the_content() -> None:
    """الإفادةُ تظهر **شرطَ امتناع** لا عقدةً في الشجرة؛ ولذلك لا تُقاس محتوًى."""

    forbidding = Placement(
        coordinate=("لفظ", "مركّب", "مهمل"),
        forbidden_because="الغرضُ من التركيب هو الإفادة",
        refuted_by="مركّبٌ مهملٌ يُفيد",
    )
    assert forbidding.vacancy is Vacancy.IMPOSSIBLE
    assert forbidding.finding is None  # فليست محتوًى يُملأ

    # ولو أُريدت محتوًى للزم لها مصدرٌ ووحدةٌ وصفريّ، وليس منها شيءٌ ههنا
    assert forbidding.state != "مُودَع"


def test_five_named_and_one_forbidden_leave_two_cells_unspoken() -> None:
    """٨ − ٥ − ١ = ٢ خانتان لم يُقَل فيهما شيء؛ وهما موضعان لا مجهولان."""

    unspoken = CELLS_THREE_WAY - NAMED_IN_THE_THREE_WAY - FORBIDDEN_IN_THE_THREE_WAY
    assert unspoken == 2
    assert (
        Partition(
            parts=(NAMED_IN_THE_THREE_WAY, FORBIDDEN_IN_THE_THREE_WAY, unspoken),
            declared_total=CELLS_THREE_WAY,
        ).residue
        == 0
    )
    # وجنسُ خلوّهما هو ما يعطيه الجداءُ وحدَه، لا أكثر
    assert Vacancy.UNCLASSIFIED in set(Vacancy)


def test_the_implication_is_refused_for_a_reason_that_is_itself_a_claim() -> None:
    """المفهومُ «في غير محلّ النطق»، فلا موضعَ له في المتتالية — ورفضٌ معلَّل.

    والدعوى قابلةٌ للنقض: مفهومٌ يُعيَّن له موضعٌ في المتتالية يُسقِطها. فليست
    عجزًا عن القياس بل **حكمًا على موضوعه**، وفرقُ الاثنين أنّ الأوّلَ يُرفَع
    بأداةٍ أقوى والثاني لا يُرفَع بها.
    """

    refusal = Placement(
        coordinate=("المفهوم", "ماركوف"),
        forbidden_because=(
            "المفهومُ ما دلّ عليه اللفظُ في غير محلّ النطق، والسلسلةُ تقيس "
            "ما له موضعٌ في المتتالية"
        ),
        refuted_by="مفهومٌ يُعيَّن له موضعٌ في المتتالية فيُقاس بها",
    )
    assert refusal.vacancy is Vacancy.IMPOSSIBLE
    assert "في غير محلّ النطق" in refusal.forbidden_because

    # والمنطوقُ في الركيزة بالتعريف، فخلوُّه لو وقع كان من جنسٍ آخرَ بالكلّيّة
    spoken = Placement(
        coordinate=("المنطوق", "ماركوف"),
        open_test="قياسُ سلسلةٍ على المنطوق وحدَه بمقامٍ مُعلَن",
    )
    assert spoken.vacancy is Vacancy.UNRUN
    assert spoken.vacancy is not refusal.vacancy


def test_the_measured_fill_orders_the_four_cells_by_a_factor_of_three_hundred() -> None:
    """٩١٫٦٪ إلى ٠٫٣٪ = ٣٠٥ أضعافًا؛ فالجداءُ مملوءٌ وميلُه شديد."""

    biggest = Fraction(FILL["متباين"], 1_000)
    smallest = Fraction(FILL["مشترك"], 1_000)
    assert round(float(biggest / smallest), 1) == 305.3
    assert biggest > Fraction(9, 10)
    assert smallest < Fraction(1, 100)

    # والمترادفُ فوق المنفرد، والمنفردُ فوق المشترك — ترتيبٌ يُعاد لا يُنقَل
    ordered = sorted(FILL.items(), key=lambda item: item[1], reverse=True)
    assert [name for name, _ in ordered] == ["متباين", "مترادف", "منفرد", "مشترك"]
