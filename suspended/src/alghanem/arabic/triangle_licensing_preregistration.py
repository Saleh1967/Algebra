"""تسجيلٌ مسبقٌ للمثلّث: B₁₃ عقدةً ثالثة — مُسجَّلٌ ولا يُختبَر في هذه الجلسة.

**ما تفعله هذه الوحدة**: تُسجّل — قبل أيّ عدّ — الفرضيّاتَ الثلاثَ لإدخال
`B₁₃` عقدةً ثالثةً في رسم الترخيص، فيصير التركيبُ **مثلّثًا لا سلسلة**. ومعها
شروطُ إبطال كلٍّ منها، ومقياسٌ مُعلَنٌ سابقٌ للنظر.

`A_PREREGISTRATION_TESTED_IN_ITS_OWN_SESSION_IS_NOT_A_PREREGISTRATION`: وهذا
شرطُ هذه الوحدة الأوّل، وهو **بنيويٌّ لا نصيحة**: ليس فيها دالّةُ قياسٍ واحدة،
ولا تقرأ جذرًا ولا بايتًا. فمن أراد الاختبارَ بناه في وحدةٍ أخرى وجلسةٍ أخرى،
وحارسٌ ههنا يرفض أن يُضاف إليها ما يقرأ بيانات.

`THE_TRIANGLE_IS_A_HYPOTHESIS_ABOUT_THE_GRAPH_NOT_ABOUT_ARABIC`: المقترَحُ
تغييرُ **رسم الترخيص**: أن تكون الرابطةُ بين الطرفين عقدةً قائمةً بذاتها لا
أثرًا لتركيب الرابطتين المتجاورتين. وهذا سؤالٌ عن بنية النموذج، ويصير سؤالًا
عن العربيّة متى قِيس على مصدرين.

`THE_MOTIVATION_IS_A_FALLEN_CLOSURE_NOT_A_CONFIRMED_TRIANGLE`: ودافعُه سقوطُ
إغلاق التركيب — وهو مُعادُ الإنتاج على المقاييس في
`composition_closure_replication`. وسقوطُ الإغلاق يقول إنّ السلسلةَ **لا
تكفي**، ولا يقول إنّ المثلّثَ **هو** البديل. فبين نفيِ السلسلة وإثباتِ المثلّث
اختبارٌ لم يُجرَ.

`EVERY_HYPOTHESIS_CARRIES_ITS_FALSIFIER`: كلُّ فرضيّةٍ هنا تحمل شرطَ إبطالها
نصًّا غيرَ فارغٍ شرطَ إنشاء، ويُرَدُّ ما طابق شرطُ إبطاله شرطَ تأكيده.

`THE_MEASURE_IS_DECLARED_BEFORE_THE_LOOK`: والمقياسُ مُعلَنٌ قبل النظر: أيُّ
نموذجٍ صفريٍّ، وأيُّ إحصاءةٍ، وأيُّ حدٍّ للقبول، وأيُّ تصحيحٍ للتعدّد. ومن
أعلن مقياسَه بعد رؤية الرقم وصف ما رأى.

`ONE_SOURCE_CANNOT_CERTIFY_THE_TRIANGLE`: وبايتاتُ المصدر الثاني ليست في هذه
الشجرة، فأقصى ما يبلغه اختبارٌ يُجرى هنا **غيرُ محسوم**؛ وذلك مكتوبٌ قبل
الاختبار لا بعده.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_PREREGISTRATION_TESTED_IN_ITS_OWN_SESSION_NOTE",
    "DECLARED_MEASURE",
    "EVERY_HYPOTHESIS_CARRIES_ITS_FALSIFIER_NOTE",
    "ONE_SOURCE_CANNOT_CERTIFY_NOTE",
    "REGISTERED_AT",
    "THE_MEASURE_IS_DECLARED_BEFORE_THE_LOOK_NOTE",
    "THE_MOTIVATION_IS_A_FALLEN_CLOSURE_NOTE",
    "THE_TRIANGLE_IS_A_HYPOTHESIS_ABOUT_THE_GRAPH_NOTE",
    "TRIANGLE_HYPOTHESES",
    "TRIANGLE_NAMED_RESIDUALS",
    "TRIANGLE_NODES",
    "DeclaredMeasure",
    "GraphShape",
    "TriangleHypothesis",
    "TrianglePreregistrationError",
    "hypothesis_named",
    "is_testable_in_this_module",
]

REGISTERED_AT: Final[str] = "2026-09-22"
"""تاريخُ التسجيل، ويسبق أيَّ اختبارٍ يُجرى على هذه الفرضيّات."""

TRIANGLE_NODES: Final[tuple[str, ...]] = ("B₁₂", "B₂₃", "B₁₃")
"""عُقَدُ الرسم المقترَح؛ والثالثةُ هي المضافة."""


class TrianglePreregistrationError(ValueError):
    """رُفض تسجيلٌ خارج شرطه؛ ولا يُحمَل على أقرب صيغةٍ مقبولة."""


class GraphShape(Enum):
    """شكلا الرسم المتنافسان، ولا ثالثَ مُسجَّلٌ هنا."""

    CHAIN = "سلسلة: B₁₂ ثمّ B₂₃، وB₁₃ أثرٌ لتركيبهما"
    TRIANGLE = "مثلّث: B₁₃ عقدةٌ قائمةٌ بذاتها إلى جانبهما"


@dataclass(frozen=True, slots=True)
class DeclaredMeasure:
    """المقياسُ مُعلَنًا قبل النظر: صفريُّه وإحصاءتُه وحدُّه وتصحيحُه."""

    null_model: str
    statistic: str
    acceptance_threshold: str
    multiplicity_correction: str
    replicates: int

    def __post_init__(self) -> None:
        if self.replicates < 1:
            raise TrianglePreregistrationError("عددُ التكرارات موجب.")
        for value, label in (
            (self.null_model, "النموذجُ الصفريّ"),
            (self.statistic, "الإحصاءة"),
            (self.acceptance_threshold, "حدُّ القبول"),
            (self.multiplicity_correction, "تصحيحُ التعدّد"),
        ):
            if not value.strip():
                raise TrianglePreregistrationError(
                    f"{label} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ ومقياسٌ ناقصٌ "
                    "يُكمَّل بعد رؤية الرقم"
                )


DECLARED_MEASURE: Final[DeclaredMeasure] = DeclaredMeasure(
    null_model=(
        "سلسلةُ تبادلٍ داخل طبقة C₂ تُثبِّت جدولَي (C₁,C₂) و(C₂,C₃) وترفض "
        "كلَّ تبديلٍ يولّد جذرًا مكرَّرًا؛ والحفظان يُفحَصان في كلّ تكرار"
    ),
    statistic=(
        "لكلّ زوج كتلتين ونوعِ علاقةٍ: الفرقُ بين المرصود ومتوسّطِ الصفريّ، "
        "مع إفراد خليّة التماثل عن خليّة التجانس"
    ),
    acceptance_threshold=(
        "يُقبَل أثرُ B₁₃ عقدةً مستقلّةً إن بقي فرقُه دالًّا بعد التصحيح في "
        "سياستَي الإدراج كلتيهما؛ وسياسةُ الإدراج تُعلَن مع كلّ قراءة"
    ),
    multiplicity_correction=(
        "بونفيروني على عدد خلايا (كتلة × كتلة × نوع علاقة) المُختبَرة، "
        "ويُعلَن العددُ قبل العدّ لا بعده"
    ),
    replicates=2_000,
)
"""المقياسُ المُعلَن؛ وتغييرُ عنصرٍ منه بعد النظر يُبطِل التسجيل."""


@dataclass(frozen=True, slots=True)
class TriangleHypothesis:
    """فرضيّةٌ مُسجَّلة: نصُّها، وما يؤكّدها، **وما يُبطلها**."""

    identifier: str
    claim: str
    what_would_confirm: str
    what_would_falsify: str

    def __post_init__(self) -> None:
        if not self.what_would_falsify.strip():
            raise TrianglePreregistrationError(
                "فرضيّةٌ بلا شرطِ إبطالٍ تُثبَّت مهما جاءت البيانات؛ " "وذلك سؤالٌ لا اختبار"
            )
        if self.what_would_confirm.strip() == self.what_would_falsify.strip():
            raise TrianglePreregistrationError(
                "شرطا التأكيد والإبطال واحدٌ؛ وشرطان متطابقان لا يفصلان"
            )


TRIANGLE_HYPOTHESES: Final[tuple[TriangleHypothesis, ...]] = (
    TriangleHypothesis(
        identifier="TRI-1",
        claim=(
            "B₁₃ عقدةٌ مستقلّة: بعد تثبيت الجدولين المتجاورين يبقى في "
            "اجتماع C₁ وC₃ أثرٌ لا يفسّره تركيبُ الرابطتين"
        ),
        what_would_confirm=(
            "فرقٌ دالٌّ بعد بونفيروني في سياستَي الإدراج كلتيهما، وفي المصدرين "
            "إن وصلت بايتاتُ الثاني"
        ),
        what_would_falsify=(
            "انعدامُ الفرق في إحدى السياستين، أو انقلابُ إشارته بينهما، أو "
            "زوالُه عند إفراد خليّة التماثل عن خليّة التجانس"
        ),
    ),
    TriangleHypothesis(
        identifier="TRI-2",
        claim=(
            "المثلّثُ يزيد على السلسلة زيادةً تُقاس: نموذجٌ بثلاث عُقَدٍ "
            "يُفضَّل على نموذج العقدتين بمعيار معلوماتيٍّ مُعلَن"
        ),
        what_would_confirm=(
            "تفضيلُ نموذج الثلاث بـBIC في نصفَي التقسيم كليهما، والفارقُ "
            "أكبرُ من حدٍّ يُعلَن قبل العدّ"
        ),
        what_would_falsify=(
            "تفضيلُ نموذج العقدتين، أو تفضيلُ الثلاث في نصفٍ وسقوطُه في "
            "الآخر، أو انقلابُ التفضيل بين الأنواع والرموز"
        ),
    ),
    TriangleHypothesis(
        identifier="TRI-3",
        claim=(
            "أثرُ B₁₃ ليس أثرَ التماثل وحدَه: يبقى في خلايا التجانس بعد "
            "استثناء الحرفين المتماثلين"
        ),
        what_would_confirm=(
            "بقاءُ فرقٍ دالٍّ في خلايا التجانس وحدَها، بعد إخراج التماثل " "من العدّ"
        ),
        what_would_falsify=(
            "زوالُ الفرق بعد إخراج التماثل، فيكون الأثرُ كلُّه أثرَ الجذور "
            "المضعَّفة وسياسةِ إدراجها"
        ),
    ),
)
"""الفرضيّاتُ الثلاثُ المُسجَّلة، كلٌّ بشرطَي تأكيدها وإبطالها."""


def hypothesis_named(identifier: str) -> TriangleHypothesis:
    """اقرأ فرضيّةً بمعرّفها؛ ومعرّفٌ غيرُ مُسجَّلٍ يُرَدُّ لا يُحمَل على أقربه."""

    for hypothesis in TRIANGLE_HYPOTHESES:
        if hypothesis.identifier == identifier:
            return hypothesis
    raise TrianglePreregistrationError(
        f"لا فرضيّةَ مُسجَّلةٌ بالمعرّف {identifier!r}؛ " "وغيابُ الفرضيّة ليس نفيًا لسؤالها."
    )


def is_testable_in_this_module() -> bool:
    """أيُختبَر شيءٌ هنا؟ **لا** — بالبناء؛ وهذا شرطُ التسجيل لا وصفُه."""

    return False


A_PREREGISTRATION_TESTED_IN_ITS_OWN_SESSION_NOTE: Final[str] = (
    "APreregistrationTestedInItsOwnSessionIsNotAPreregistration: ليس في هذه "
    "الوحدة دالّةُ قياسٍ واحدة ولا تقرأ بايتًا؛ ومن أراد الاختبارَ بناه في "
    "وحدةٍ أخرى وجلسةٍ أخرى"
)

THE_TRIANGLE_IS_A_HYPOTHESIS_ABOUT_THE_GRAPH_NOTE: Final[str] = (
    "TheTriangleIsAHypothesisAboutTheGraphNotAboutArabic: المقترَحُ تغييرُ "
    "رسم الترخيص؛ ويصير سؤالًا عن العربيّة متى قِيس على مصدرين"
)

THE_MOTIVATION_IS_A_FALLEN_CLOSURE_NOTE: Final[str] = (
    "TheMotivationIsAFallenClosureNotAConfirmedTriangle: سقوطُ الإغلاق يقول "
    "إنّ السلسلةَ لا تكفي، ولا يقول إنّ المثلّثَ هو البديل؛ وبين النفي "
    "والإثبات اختبارٌ لم يُجرَ"
)

EVERY_HYPOTHESIS_CARRIES_ITS_FALSIFIER_NOTE: Final[str] = (
    "EveryHypothesisCarriesItsFalsifier: شرطُ الإبطال شرطُ إنشاء، ويُرَدُّ ما "
    "طابق شرطُ إبطاله شرطَ تأكيده"
)

THE_MEASURE_IS_DECLARED_BEFORE_THE_LOOK_NOTE: Final[str] = (
    "TheMeasureIsDeclaredBeforeTheLook: الصفريُّ والإحصاءةُ وحدُّ القبول "
    "وتصحيحُ التعدّد مُعلَنةٌ قبل النظر؛ ومن أعلن مقياسَه بعد رؤية الرقم وصف "
    "ما رأى"
)

ONE_SOURCE_CANNOT_CERTIFY_NOTE: Final[str] = (
    "OneSourceCannotCertifyTheTriangle: بايتاتُ المصدر الثاني ليست في هذه "
    "الشجرة، فأقصى ما يبلغه اختبارٌ يُجرى هنا غيرُ محسوم؛ ومكتوبٌ قبله لا بعده"
)

TRIANGLE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_PREREGISTRATION_TESTED_IN_ITS_OWN_SESSION_NOTE,
    THE_TRIANGLE_IS_A_HYPOTHESIS_ABOUT_THE_GRAPH_NOTE,
    THE_MOTIVATION_IS_A_FALLEN_CLOSURE_NOTE,
    EVERY_HYPOTHESIS_CARRIES_ITS_FALSIFIER_NOTE,
    THE_MEASURE_IS_DECLARED_BEFORE_THE_LOOK_NOTE,
    ONE_SOURCE_CANNOT_CERTIFY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(TRIANGLE_NODES) != 3:  # pragma: no cover - حارس
    raise RuntimeError("عُقَدُ المثلّث ثلاثٌ؛ وعقدتان سلسلةٌ لا مثلّث.")
if len({item.identifier for item in TRIANGLE_HYPOTHESES}) != len(
    TRIANGLE_HYPOTHESES
):  # pragma: no cover - حارس
    raise RuntimeError("معرّفان لفرضيّةٍ واحدة؛ ومعرّفٌ يسمّي فرضيّتين يُستشهَد به على نفسه.")
