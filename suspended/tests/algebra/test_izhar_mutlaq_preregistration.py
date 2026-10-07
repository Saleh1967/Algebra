"""تسجيلُ الإظهار المطلق قبل عدّه: أربعةُ ألفاظٍ، وتنبّؤٌ باتّجاهٍ واحد.

**البقيّةُ التي فتحت هذا الباب**: خرج بعد نونٍ موسومةٍ بالسكون **١٢٢** على
الياء و**٣** على الواو — وهما من حروف الإدغام، فالقاعدةُ تقتضي ألّا يقعا.
ومرشَّحُ التفسير **الإظهارُ المطلق**: نونٌ ساكنةٌ يليها واوٌ أو ياءٌ **في
الكلمة نفسِها** تُظهَر ولا تُدغَم.

`THE_PREDICTION_IS_WRITTEN_BEFORE_THE_COUNT_AND_IT_IS_SHARP`: والتنبّؤُ
حادٌّ يقبل التكذيب بسهولة: إن كان الإظهارُ المطلقُ هو العلّة، فالغالبيّةُ
العظمى من تلك المواضع **داخلَ الكلمة**. وإن خرجت أكثرُها عابرةً حدَّ
الكلمة، فالعلّةُ غيرُها ولا يُلتمَس لها عذر.

`A_NAMED_LIST_IS_NOT_A_FILTER_ADDED_AFTER_SIGHT`: والألفاظُ الأربعةُ
المذكورةُ في كتب التجويد — دنيا، بنيان، قنوان، صنوان — **تُسمّى ههنا قبل
العدّ**. فإن غطّت أكثرَ المواضع فذلك خبر، وإن لم تُغطِّها فالباقي يُعَدّ
ويُنشَر ولا يُطوى.

`WHAT_THIS_CANNOT_SHOW`: ولا يُثبِت هذا العدُّ أنّ «الإظهارَ المطلق» حكمٌ
في العربيّة: يُثبِت أنّ **وسمَ هذا المصدر** يسلك مسلكَه. والفرقُ بين
الأمرين هو الفرقُ نفسُه المكتوبُ في كلّ رقمٍ من هذا الباب.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

RESIDUE_YAA, RESIDUE_WAW = 122, 3
NAMED_WORDS: tuple[str, ...] = ("دنيا", "بنيان", "قنوان", "صنوان")

FAMILY = 3
SEED = 20_260_924

IZHAR_MUTLAQ = Oracle(
    name="بقيّةُ الواو والياء بعد النون الساكنة في المصحف",
    source="المدوّنةُ المُجمَّدةُ ببصمتها، ومصدرُ ضبطها مُسمًّى",
    extraction=(
        "يُعَدّ كلُّ موضعٍ فيه نونٌ موسومةٌ بالسكون يليها واوٌ أو ياء، "
        "ويُقسَم قسمين: ما كان الحرفان فيه **في كلمةٍ واحدة**، وما عبر "
        "الحرفُ الثاني فيه إلى كلمةٍ تالية. والقسمةُ بالفراغ في الرسم"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ط١ الأكثرُ داخلَ الكلمة",
        statistic="نصيبُ المواضع التي يقع فيها الحرفان في كلمةٍ واحدة",
        threshold=Fraction(90, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الإظهارَ المطلق يفسّر البقيّة؛ فدونه تكون العلّةُ غيرَه "
            "ولا يُلتمَس لها عذرٌ بعد العدّ"
        ),
    ),
    Prediction(
        identifier="ط٢ الألفاظُ الأربعةُ مُسمّاةٌ قبل العدّ",
        statistic="عددُ الألفاظ المُسمّاةِ في هذا التسجيل قبل التشغيل",
        threshold=Fraction(4),
        direction=Direction.AT_LEAST,
        falsifies=("لا شيء؛ وهو بندُ إعلانٍ يمنع أن تُضاف مصفاةٌ بعد رؤية الرقم"),
    ),
    Prediction(
        identifier="ط٣ مقامُ البقيّة منشور",
        statistic="عددُ مواضع الواو والياء بعد النون الموسومة بالسكون",
        threshold=Fraction(50),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ القراءة؛ فدونه يُعلَن العددُ ضعيفَ الشهادة",
    ),
)

IZHAR_SEAL = seal(IZHAR_MUTLAQ, PREDICTIONS)

SEALED_DIGEST = "57ac0f3852debdaff5164c78add3e623f982025b2ee6239d046f41e723ecc499"


def test_the_seal_is_stable_and_the_prediction_is_falsifiable() -> None:
    """بصمةٌ ثابتة، وحدٌّ يقبل التكذيب: نصفُ المواضع يُسقِط ط١."""

    assert IZHAR_SEAL == SEALED_DIGEST
    assert len(IZHAR_SEAL) == 64

    first = PREDICTIONS[0]
    assert first.verdict(Fraction(95, 100)) is Verdict.MET
    assert first.verdict(Fraction(50, 100)) is Verdict.FALSIFIED


def test_the_residue_that_opened_the_door_is_recorded() -> None:
    """١٢٢ على الياء و٣ على الواو — والمقامُ مئةٌ وخمسةٌ وعشرون موضعًا."""

    assert RESIDUE_YAA == 122 and RESIDUE_WAW == 3
    assert RESIDUE_YAA + RESIDUE_WAW == 125
    assert PREDICTIONS[2].verdict(Fraction(125)) is Verdict.MET


def test_the_four_words_are_named_before_the_count() -> None:
    """أربعةُ ألفاظٍ مُسمّاةٌ، ولا خامسَ يُضاف بعد رؤية الرقم."""

    assert len(NAMED_WORDS) == FAMILY + 1 == 4
    assert len(set(NAMED_WORDS)) == 4
    assert PREDICTIONS[1].verdict(Fraction(len(NAMED_WORDS))) is Verdict.MET


def test_what_the_count_cannot_show_is_written_in_the_seal() -> None:
    """يُثبِت مسلكَ الوسم لا حكمًا في العربيّة، والفرقُ مكتوبٌ لا مطويّ."""

    assert "مصدرُ ضبطها مُسمًّى" in IZHAR_MUTLAQ.source
    assert FAMILY == len(PREDICTIONS) == 3
    assert SEED == 20_260_924
