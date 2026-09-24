"""موضعُ التعريب في الشجرة، وشرطٌ أُعلِن غيرَ قابلٍ للتكذيب قبل القياس.

**ما يُقاس ههنا**: بنيةُ الوضع وحسابُها، لا العربيّة. وكان الفصلُ السابقُ
يُعيد الأرقامَ ويردّ على المقدار؛ وبقي منه شيئان لم يُودَعا — **الموضعُ**
و**الشرطُ المُعلَنُ عقيمًا** — فهما ههنا.

`THE_TWO_CONDITIONS_ARE_NOT_TWO_MEASUREMENTS`: الكتابُ يعطي شرطين — صياغةٌ
على وزنٍ عربيّ، وموافقةُ الحروف — ولا يُقاس منهما إلّا **الأوّل**. والثاني
مُعلَنٌ **غيرَ قابلٍ للتكذيب على هذه الركيزة**: كلُّ ما في المصحف مكتوبٌ
بحروفه بالضرورة، فلا وقوعَ يُتصوَّر يُسقِطه. **وإعلانُه قبل النظر هو ما يجعله
حدًّا لا عذرًا** — إذ لو قيل بعد الرقم لكان اختيارًا للشرط الذي وافق.

`AN_UNFALSIFIABLE_CONDITION_IS_STILL_REFUTABLE_ELSEWHERE`: وليس عقمُه دائمًا:
ركيزةٌ فيها لفظٌ بحرفٍ غيرِ عربيٍّ تُسقِطه في الحال. فالخانةُ **ممتنعةٌ ههنا
بناقضٍ مُسمًّى**، لا ممتنعةٌ في نفسها — وذلك فرقٌ تحمله المكتبةُ بالبناء.

`THE_NODE_SITS_UNDER_THE_SIGNIFIER_BECAUSE_BOTH_CONDITIONS_ARE_FORMAL`:
وشرطاه صوريّان بحتان — وزنٌ وحروف — فلا يمسّ أحدُهما المدلول. فموضعُ العقدة
**تحت الدالّ وحدَه**، والخانتان الأخريان (المدلول، ومعًا) ممتنعتان بعلّةٍ
واحدةٍ وناقضٍ واحد: شرطٌ في التعريب يستلزم معنًى مُعيَّنًا يُسقِط الامتناع.

`IT_IS_THE_FIRST_NODE_ADDED_BY_MEASUREMENT_NOT_BY_TRANSMISSION`: وسائرُ عقد
الشجرة منقولةٌ من كتبٍ ثمّ فُحِصت. وهذه **قِيست أوّلًا**: الترتيبُ (أصيلٌ <
مصوغٌ < غيرُ مصوغ) خرج من العدّ، والكتابُ صدّقه. فتُوسَم بذلك ههنا كي لا
تُقرَأ يومًا نقلًا.
"""

from __future__ import annotations

import pytest

from algebra.results import Axis, Placement, Product, ResultsError, Vacancy
from algebra.selection import Locus, partition_of_loci

FORMAL_CONDITIONS = ("الصياغةُ على وزنٍ عربيّ", "موافقةُ الحروف")


def test_the_book_gives_two_conditions_and_only_one_is_measurable_here() -> None:
    """شرطان، ومقيسٌ واحدٌ — والثاني يُعلَن عقيمًا **قبل** الرقم لا بعدَه."""

    assert len(FORMAL_CONDITIONS) == 2
    assert len(set(FORMAL_CONDITIONS)) == 2

    measurable = Placement(
        coordinate=("التعريب", "الصياغةُ على وزنٍ عربيّ"),
        open_test=(
            "تُقاس مفاجأةُ السلسلة على المعرَّبات ذاتِ الجذر وغيرِها، ويُنظَر "
            "أتفترقان بمقدارٍ فوق صفريٍّ مُسمّى الأساس"
        ),
    )
    barren = Placement(
        coordinate=("التعريب", "موافقةُ الحروف"),
        forbidden_because=(
            "كلُّ ما في هذه الركيزة مكتوبٌ بحروفها بالضرورة، فلا وقوعَ " "يُتصوَّر يُسقِط الشرط"
        ),
        refuted_by="ركيزةٌ فيها لفظٌ بحرفٍ غيرِ عربيّ",
    )

    assert measurable.vacancy is Vacancy.UNRUN
    assert barren.vacancy is Vacancy.IMPOSSIBLE
    assert measurable.vacancy is not barren.vacancy


def test_an_unfalsifiable_condition_still_names_what_would_refute_it() -> None:
    """العقمُ ههنا لا عقمٌ في نفسه؛ وامتناعٌ بلا ناقضٍ يُرَدّ عند الإنشاء."""

    with pytest.raises(ResultsError, match="بلا ناقضٍ"):
        Placement(
            coordinate=("التعريب", "موافقةُ الحروف"),
            forbidden_because="لا وقوعَ يُسقِطه على هذه الركيزة",
        )


def test_the_node_sits_under_the_signifier_and_two_cells_are_forbidden() -> None:
    """ثلاثُ خانٍ: واحدةٌ تُسكَن، واثنتان ممتنعتان بعلّةٍ واحدةٍ وناقضٍ واحد."""

    where = Product(
        axes=(Axis(name="موضعُ العقدة", values=("الدالّ", "المدلول", "معًا")),)
    )
    assert where.size == 3

    reason = "شرطا التعريب صوريّان بحتان — وزنٌ وحروف — فلا يمسّ أحدُهما المدلول"
    refuter = "شرطٌ في التعريب يستلزم معنًى مُعيَّنًا لا صورةً"

    placements = (
        Placement(
            coordinate=("الدالّ",),
            open_test=(
                "يُقاس الفرقُ بين المصوغ وغيرِ المصوغ داخلَ المعرَّبات وحدَها، "
                "بمقامٍ مُعلَنٍ وصفريٍّ مُسمّى الأساس"
            ),
        ),
        Placement(
            coordinate=("المدلول",), forbidden_because=reason, refuted_by=refuter
        ),
        Placement(coordinate=("معًا",), forbidden_because=reason, refuted_by=refuter),
    )
    kinds = [one.vacancy for one in placements]
    assert kinds.count(Vacancy.IMPOSSIBLE) == 2
    assert kinds.count(Vacancy.UNRUN) == 1
    assert len(placements) == where.size  # والجداءُ مملوءٌ بلا خانةٍ منسيّة


def test_the_node_joins_two_siblings_already_under_the_signifier() -> None:
    """ثلاثُ قسماتٍ تحت الدالّ، والتعريبُ ثالثُها — **وكلٌّ محورٌ لا قيمة**.

    وقد كتبتُها أوّلًا قيمًا لمحورٍ واحد («مفرد/مركّب» و«اسم/فعل/حرف»)، فردَّها
    `Axis` بأنّ الشرطةَ في خانةٍ واحدةٍ امتناعٌ عن القسمة لا قسمة. وهو ردٌّ
    صحيح: هذه **أسماءُ قسماتٍ** لا أعضاءُ قسمةٍ واحدة، وجمعُها في محورٍ يخلط
    المستويين.
    """

    siblings = (
        Axis(name="الإفرادُ والتركيب", values=("مفرد", "مركّب")),
        Axis(name="القسمةُ الثلاثيّة", values=("اسم", "فعل", "حرف")),
        Axis(name="التعريب", values=("معرَّب", "أصيل")),
    )
    assert len(siblings) == 3
    assert len({one.name for one in siblings}) == 3
    assert siblings[-1].name == "التعريب"

    # وكلُّها تُقرَأ من الصورة وحدَها، وذلك ما يجمعها تحت الدالّ
    together = Product(axes=siblings)
    assert together.size == 2 * 3 * 2 == 12


def test_it_is_the_first_node_that_measurement_put_there() -> None:
    """عقدةٌ قِيست ثمّ صدّقها الكتاب، لا عقدةٌ نُقِلت ثمّ فُحِصت."""

    loci = partition_of_loci(
        (
            Locus(
                name="العقدةُ منقولةٌ من كتابٍ ثمّ فُحِصت",
                settled=False,
                deciding_test=(
                    "يُطلَب نصٌّ يجعل «معرَّب/أصيل» قسمةً في الدالّ قبل القياس؛ "
                    "فإن وُجد فهي منقولة"
                ),
            ),
            Locus(
                name="العقدةُ قِيست ثمّ صدّقها الكتاب",
                settled=False,
                deciding_test=(
                    "يُنظَر أيُّهما سبق في السجلّ: ترتيبُ المفاجأة الثلاثيُّ "
                    "أم نصُّ الشرطين؛ والسابقُ هو الأصل"
                ),
            ),
        )
    )
    assert len(loci) == 2
    assert all(not one.settled for one in loci)
    assert len({one.deciding_test for one in loci}) == 2

    # والفارقُ عمليّ: المنقولُ يُفحَص، والمقيسُ يحتاج تسجيلًا سابقًا لترتيبه
    assert all(" أو " not in one.name for one in loci)
