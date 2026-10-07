"""الختمُ الخامس: صفريٌّ مطابقٌ في التردّد — أشيوعٌ هو أم مخرج؟

**تسجيلٌ محض: لا رقمَ مقيسٌ فيه.** وأوراكلُه يستشهد بالسجلّ `30c7e393…`.

`THE_SIZE_MATCHED_NULL_LEFT_ONE_EXPLANATION_STANDING`: قِيس تماسكُ مجموعات
المرشَّح بصفريٍّ **مطابقٍ في الحجم**، فخرجت G1 في أدنى المئينات وG5 في
أعلاها. وبقي تفسيرٌ واحدٌ لم يُردّ: أنّ المقيسَ **شيوعُ الحروف** لا مخارجُها
— فG1 فيها الألفُ الحاملةُ للهمزة، وهي من أشيع الرموز وأشذِّها توزيعًا.

`THE_MATCHED_NULL_HOLDS_THE_FREQUENCY_LAYER_FIXED`: فيُبنى صفريٌّ يحفظ
**طبقةَ الشيوع**: تُرتَّب الحروفُ الثمانيةُ والعشرون بتردّدها لاحقًا،
وتُقسَم أربعَ طبقاتٍ متساويةٍ سبعًا سبعًا، وتُسحَب المجموعاتُ **بحفظ عدد
الحروف من كلّ طبقة**. فما بقي من الفرق بعد ذلك ليس شيوعًا.

`A_MATCHED_NULL_THAT_IS_NOT_MATCHED_IS_WORSE_THAN_NONE`: ويُفحَص أنّ
المطابقةَ وقعت فعلًا: متوسّطُ رتبة التردّد في السحبات يقارب متوسّطَها في
المجموعة. فصفريٌّ يُسمّى مطابقًا ولا يُطابق **يُخفي العطلَ باسم إصلاحه**.

`THE_TWO_DIRECTIONS_ARE_BOTH_WRITTEN_BEFORE_THE_LOOK`: ويُسجَّل الاتّجاهان
معًا: أن تبقى G1 في الأدنى، وأن تبقى G5 في الأعلى. فإن ارتفعت الأولى أو
هبطت الثانية فالمقيسُ شيوعٌ — ويُقال كما يخرج، لا كما يُشتهى.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"

DRAWS = 2_000
SEED = 20_260_924
FAMILY = 4
STRATA = 4

FREQUENCY_MATCHED = Oracle(
    name="تماسكُ مجموعات المرشَّح تحت صفريٍّ مطابقٍ في طبقة الشيوع",
    source=(
        f"السجلُّ البايتيُّ {CORPUS_RECORD[:16]}… وحدَه؛ ومجموعاتُ المرشَّح "
        "كما وردت، ولا تُعدَّل حروفُها ههنا بحالٍ"
    ),
    extraction=(
        "تُرتَّب الحروفُ الثمانيةُ والعشرون بتردّدها لاحقًا في المدوّنة، "
        "وتُقسَم **أربعَ طبقاتٍ سبعًا سبعًا**. ولكلّ مجموعةٍ يُحسَب متوسّطُ "
        "تشابه صفوفها، ويُقارَن بسحباتٍ تحفظ **عددَ حروفها من كلّ طبقة**. "
        "والصفوفُ على الجوار العابر لحدّ الكلمة، والسياسةُ مُسمّاةٌ في المخرَج"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="و١ الحلقُ يبقى في الأدنى",
        statistic="مئينُ G1 بين السحبات المطابقة في طبقة الشيوع",
        threshold=Fraction(5, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ تباعدَ حروف الحلق خبرٌ عن المخرج؛ فارتفاعُ مئينها تحت "
            "الصفريّ المطابق يعني أنّ المقيسَ شيوعٌ لا مخرج"
        ),
    ),
    Prediction(
        identifier="و٢ الباقي يبقى في الأعلى",
        statistic="مئينُ G5 بين السحبات المطابقة في طبقة الشيوع",
        threshold=Fraction(95, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ تماسكَ مجموعة الباقي خبرٌ عنها؛ فهبوطُه تحت الصفريّ "
            "المطابق يعني أنّه خبرٌ عن طبقة شيوعها"
        ),
    ),
    Prediction(
        identifier="و٣ المطابقةُ وقعت فعلًا",
        statistic=(
            "أكبرُ فرقٍ مطلقٍ بين متوسّط رتبة التردّد في مجموعةٍ ومتوسّطها " "في سحباتها"
        ),
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "قابليّةَ قراءة و١ وو٢؛ فصفريٌّ يُسمّى مطابقًا ولا يُطابق يُخفي " "العطلَ باسم إصلاحه"
        ),
    ),
    Prediction(
        identifier="و٤ مقامُ السحب منشور",
        statistic="عددُ السحبات لكلّ مجموعة",
        threshold=Fraction(DRAWS),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ قراءة المئين؛ فدونه تكون خطوتُه أخشنَ ممّا يُدَّعى",
    ),
)

MATCHED_SEAL = seal(FREQUENCY_MATCHED, PREDICTIONS)

SEALED_DIGEST = "5e3656d53a1dceed7a151d1067813087e5b6f14faed6635c51729f8d1e5c4e27"


def test_the_seal_is_stable_and_forbids_touching_the_candidate() -> None:
    """بصمةٌ ثابتة، ومنصوصٌ ألّا تُعدَّل حروفُ المرشَّح ههنا بحال."""

    assert MATCHED_SEAL == SEALED_DIGEST
    assert len(MATCHED_SEAL) == 64
    assert "ولا تُعدَّل حروفُها ههنا بحال" in FREQUENCY_MATCHED.source
    assert CORPUS_RECORD[:16] in FREQUENCY_MATCHED.source


def test_the_two_directions_run_opposite_ways() -> None:
    """و١ «لا يجاوز» وو٢ «يبلغ» — فلا يمرّان معًا إلّا ببقاء الطرفين."""

    assert PREDICTIONS[0].direction is Direction.AT_MOST
    assert PREDICTIONS[1].direction is Direction.AT_LEAST
    assert PREDICTIONS[0].verdict(Fraction(4, 100)) is Verdict.MET
    assert PREDICTIONS[0].verdict(Fraction(40, 100)) is Verdict.FALSIFIED
    assert PREDICTIONS[1].verdict(Fraction(96, 100)) is Verdict.MET
    assert PREDICTIONS[1].verdict(Fraction(60, 100)) is Verdict.FALSIFIED


def test_the_matching_is_itself_a_condition() -> None:
    """و٣ يفحص الصفريَّ نفسَه: مطابقةٌ لا تقع تُبطِل قراءةَ ما بُني عليها."""

    third = PREDICTIONS[2]
    assert third.direction is Direction.AT_MOST
    assert third.verdict(Fraction(1, 2)) is Verdict.MET
    assert third.verdict(Fraction(3)) is Verdict.FALSIFIED
    assert "يُخفي العطلَ باسم إصلاحه" in third.falsifies


def test_the_strata_and_family_are_declared() -> None:
    """أربعُ طبقاتٍ سبعًا سبعًا، وأربعةُ شروطٍ، وألفا سحبة."""

    assert STRATA == 4 and 28 % STRATA == 0
    assert FAMILY == len(PREDICTIONS) == 4
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert DRAWS == 2_000 and SEED == 20_260_924
