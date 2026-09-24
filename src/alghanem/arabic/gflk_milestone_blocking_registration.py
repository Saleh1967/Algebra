"""ما لم يُنفَّذ من خطّة GFLK ولماذا، مُسمًّى بشرط رفعه لا مطويًّا في صمت.

`AN_UNBUILT_MILESTONE_IS_NAMED_NOT_OMITTED`: أربعُ مراحلَ من الخطّة لم تُبنَ
في هذه الجلسة — جداولُ الصفة والمخرج، واختبارُ OCP، وترميزُ الشجرة، وسُلَّمُ
الضغط. وغيابُها ليس تأجيلًا مزاجيًّا ولا نقصَ وقت: كلُّ واحدةٍ منها تستهلك
مُدخَلًا ليس في الشجرة. فتُسجَّل هنا باسمها، وبمُدخَلها الغائب، وبالشيء الذي
لو وصل لرُفِع الحجب — ولا يُكتَب لواحدةٍ منها حقلُ نتيجة.

`A_BLOCKING_INPUT_IS_NOT_A_MISSING_EFFORT`: الفرقُ مقصود. «لم يُقَس بعد» شيءٌ،
و«لا يُقاس من هنا» شيءٌ آخر. المراحلُ الأربعُ من الصنف الثاني: مصدرٌ مُسمًّى
للجدول ثلاثةَ عشرَ مخرجًا غيرُ موجود، وبايتاتُ جدول الصفة غيرُ موجودة، وسُلَّمُ
الضغط يستهلك قرارَ نطاقٍ لم يُتَّخذ. فلا يُغلَق شيءٌ منها بالاجتهاد.

`NO_FIGURE_CROSSES_A_STANDING_BLOCK`: لا يُنقَل رقمٌ من المواصفة إلى الشجرة
لأنّ مرحلتَه متعذّرة — لا ٨٨٫٣٤٪، ولا ١٨٫٧٥٪–٢٣٫٢٪، ولا p≈٠٫٠٢٧. هذه مُودَعةٌ
حيث أُودِعت، ولا تُصبح مقيسةً بأن تُذكَر في وحدةٍ برمجيّة.

`THE_BARRIERS_STAY_OPEN`: حواجزُ الاستيراد في
`gflk_feature_table_import_barrier` تبقى `OPEN`. ورفعُ حاجزٍ يكون في الالتزام
نفسِه الذي يُضيف بصمةَ مصدرِه وفحصَها، لا في وحدةِ تسجيلٍ كهذه.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`،
ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)

__all__ = [
    "AN_UNBUILT_MILESTONE_IS_NAMED_NOT_OMITTED",
    "A_BLOCKING_INPUT_IS_NOT_A_MISSING_EFFORT",
    "BLOCKED_MILESTONES",
    "MILESTONE_BLOCKING_NAMED_RESIDUALS",
    "NO_FIGURE_CROSSES_A_STANDING_BLOCK",
    "OPEN_QUESTIONS",
    "REGISTRATION_DIGEST",
    "THE_BARRIERS_STAY_OPEN",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY",
    "BlockKind",
    "BlockedMilestone",
    "MilestoneBlockingError",
    "OpenQuestion",
    "milestone_named",
    "question_named",
    "registration_digest",
]


class MilestoneBlockingError(ValueError):
    """رفضٌ بنيويّ: مرحلةٌ بلا مُدخَلٍ غائبٍ مُسمًّى، أو بحقلِ نتيجة."""


class BlockKind(Enum):
    """صنفُ المانع. ثلاثةٌ مغلقة، وليس فيها `ينقصه وقت`."""

    NO_DIGESTABLE_SOURCE_EXISTS = "لا مصدرَ قابلًا للبصم في الشجرة"
    DEPENDS_ON_A_BLOCKED_MILESTONE = "يستهلك مخرَجَ مرحلةٍ محجوبة"
    SCOPE_DECISION_NOT_TAKEN = "قرارُ نطاقٍ لم يُتَّخَذ بعد"


@dataclass(frozen=True, slots=True)
class OpenQuestion:
    """سؤالٌ مفتوحٌ يَحجُب مرحلةً؛ ويُسجَّل بنصّه لا بتخمين جوابه."""

    identifier: str
    question: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.identifier, "مُعرِّفُ السؤال"),
            (self.question, "نصُّ السؤال"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MilestoneBlockingError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى السؤال للبصمة."""

        return {"identifier": self.identifier, "question": self.question}


@dataclass(frozen=True, slots=True)
class BlockedMilestone:
    """مرحلةٌ لم تُبنَ: اسمُها، وما تستهلكه، ومانعُها، وشرطُ رفعه."""

    identifier: str
    title: str
    blocking_input: str
    kind: BlockKind
    what_would_unblock_it: str
    open_question_identifiers: tuple[str, ...]
    figures_not_carried_across: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, label in (
            (self.identifier, "مُعرِّفُ المرحلة"),
            (self.title, "عنوانُ المرحلة"),
            (self.blocking_input, "المُدخَلُ الغائب"),
            (self.what_would_unblock_it, "شرطُ الرفع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MilestoneBlockingError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.kind, BlockKind):
            raise MilestoneBlockingError("صنفُ المانع عضوٌ في مفردته المغلقة")
        if not self.open_question_identifiers:
            raise MilestoneBlockingError(
                "مرحلةٌ محجوبةٌ بلا سؤالٍ مفتوحٍ مُسمًّى حجبٌ بلا سبيلِ رفع"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة؛ وليس فيه حقلُ نتيجةٍ لأنّها لم تُقَس."""

        return {
            "identifier": self.identifier,
            "title": self.title,
            "blocking_input": self.blocking_input,
            "kind": self.kind.name,
            "what_would_unblock_it": self.what_would_unblock_it,
            "open_question_identifiers": list(self.open_question_identifiers),
            "figures_not_carried_across": list(self.figures_not_carried_across),
        }


OPEN_QUESTIONS: Final[tuple[OpenQuestion, ...]] = (
    OpenQuestion(
        identifier="THIRTEEN_VERSUS_SIXTEEN_MAKHARIJ",
        question=(
            "أيُعاد بيانُ المواصفة على الستّةَ عشرَ المُجمَّدة، أم يُنتظَر مصدرٌ "
            "مُسمًّى قابلٌ للبصم لتقسيم الثلاثةَ عشر؟"
        ),
    ),
    OpenQuestion(
        identifier="SIFA_TABLE_BYTES",
        question=(
            "أتُسلَّم محاورُ الصفة الاثنا عشرَ ملفًّا بمصدرٍ منسوبٍ وبصمة، أم "
            "تبقى الطبقةُ محجوبةً بلا أجل؟"
        ),
    ),
    OpenQuestion(
        identifier="COMPRESSION_SCOPE",
        question=(
            "أيُعاد اشتقاقُ سُلَّم PILOT كاملًا داخل الشجرة، أم يُمَدُّ الخطُّ "
            "المقيسُ إلى الرتبة الثانية ويُسجَّل الباقي غيرَ مُصدَر؟"
        ),
    ),
)
"""الأسئلةُ المفتوحةُ التي تَحجُب المراحلَ الأربع، بنصّها لا بجوابٍ مُخمَّن."""


BLOCKED_MILESTONES: Final[tuple[BlockedMilestone, ...]] = (
    BlockedMilestone(
        identifier="C_FEATURE_TABLES",
        title="جداولُ المخرج والصفة (§٣)",
        blocking_input=(
            "مصدرٌ مُسمًّى قابلٌ للبصم لتقسيم الثلاثةَ عشرَ مخرجًا، وبايتاتُ "
            "جدول الصفة ذي المحاور الاثنَي عشرَ بنسبتها"
        ),
        kind=BlockKind.NO_DIGESTABLE_SOURCE_EXISTS,
        what_would_unblock_it=(
            "وصولُ ملفٍّ بمصدرٍ منسوبٍ وطولٍ وبصمةٍ يُودَع جدولًا ثانيًا منسوبًا "
            "إلى جانب `CLASSICAL_MAKHARIJ` لا بديلًا عنه؛ أو قرارٌ صريحٌ بإعادة "
            "بيان §٣ على الستّةَ عشرَ المُجمَّدة يُسجَّل تعديلًا في الإيداع"
        ),
        open_question_identifiers=(
            "THIRTEEN_VERSUS_SIXTEEN_MAKHARIJ",
            "SIFA_TABLE_BYTES",
        ),
    ),
    BlockedMilestone(
        identifier="F_OCP_TEST",
        title="اختبارُ تنافر التجاور (§٤)",
        blocking_input="مصدرُ التصنيف المخرجيّ الذي يُبنى عليه التبديل",
        kind=BlockKind.DEPENDS_ON_A_BLOCKED_MILESTONE,
        what_would_unblock_it=(
            "استقرارُ المرحلة C على جدولٍ واحدٍ مُسمًّى؛ وحتّى بعدها يبقى "
            "التوقّعُ المُسجَّلُ سلفًا `DEFER` في "
            "`gflk_feature_table_import_barrier.OCP_PREREGISTERED_EXPECTATION`، "
            "ولا يُصدَر `PASS` إلّا بفحص انغلاقٍ مستقلٍّ صريح"
        ),
        open_question_identifiers=("THIRTEEN_VERSUS_SIXTEEN_MAKHARIJ",),
        figures_not_carried_across=("p≈0.027",),
    ),
    BlockedMilestone(
        identifier="G_TREE_BIT_ENCODING",
        title="ترميزُ الشجرة بالبتّ المشروط (§٧)",
        blocking_input="جردُ البتّات، وهو مخرَجُ جدول الصفة",
        kind=BlockKind.DEPENDS_ON_A_BLOCKED_MILESTONE,
        what_would_unblock_it=(
            "وصولُ بايتات جدول الصفة؛ وعندها يُعاد اشتقاقُ التوفير لكلِّ طقم "
            "صفاتٍ على حدة ويُنشَر مدًى بعدد صفاته، منسوبًا إلى بنية التعريف "
            "لا إلى العربيّة"
        ),
        open_question_identifiers=("SIFA_TABLE_BYTES",),
        figures_not_carried_across=("18.75%", "23.2%"),
    ),
    BlockedMilestone(
        identifier="H_COMPRESSION_LADDER",
        title="سُلَّمُ الضغط (§٦)",
        blocking_input="قرارُ نطاقٍ: إعادةُ اشتقاق السُّلَّم كلِّه أم مدُّ الخطّ المقيس",
        kind=BlockKind.SCOPE_DECISION_NOT_TAKEN,
        what_would_unblock_it=(
            "اتّخاذُ قرار النطاق؛ ثمّ في الحالتين: دورةٌ كاملةٌ مطابقةٌ شرطًا "
            "قبل أيِّ نسبة، والحجمان معًا أو لا أحدَهما، وتجميدُ K ورتبِ المزج "
            "ومعامل التقريب داخل بصمة التسجيل القبْليّ"
        ),
        open_question_identifiers=("COMPRESSION_SCOPE",),
        figures_not_carried_across=("85.11%", "87.67%", "88.01%", "88.34%"),
    ),
)
"""المراحلُ الأربعُ المحجوبة؛ ولا حقلَ نتيجةٍ في واحدةٍ منها."""


def question_named(identifier: str) -> OpenQuestion:
    """سؤالٌ بعينه، مقروءًا من الجدول المُجمَّد لا مُنشأً عند النداء."""

    for question in OPEN_QUESTIONS:
        if question.identifier == identifier:
            return question
    raise MilestoneBlockingError(f"لا سؤالَ باسم {identifier!r}")


def milestone_named(identifier: str) -> BlockedMilestone:
    """مرحلةٌ محجوبةٌ بعينها، مقروءةً من الجدول المُجمَّد."""

    for milestone in BLOCKED_MILESTONES:
        if milestone.identifier == identifier:
            return milestone
    raise MilestoneBlockingError(f"لا مرحلةَ باسم {identifier!r}")


AN_UNBUILT_MILESTONE_IS_NAMED_NOT_OMITTED: Final[str] = (
    "AnUnbuiltMilestoneIsNamedNotOmitted: كلُّ مرحلةٍ لم تُبنَ تُسجَّل باسمها "
    "ومُدخَلِها الغائب وشرطِ رفع حجبها، ولا تُطوى في صمت"
)

A_BLOCKING_INPUT_IS_NOT_A_MISSING_EFFORT: Final[str] = (
    "ABlockingInputIsNotAMissingEffort: «لم يُقَس بعد» غيرُ «لا يُقاس من "
    "هنا»؛ والمراحلُ الأربعُ من الثاني، فلا تُغلَق بالاجتهاد"
)

NO_FIGURE_CROSSES_A_STANDING_BLOCK: Final[str] = (
    "NoFigureCrossesAStandingBlock: لا يُنقَل رقمٌ من المواصفة لأنّ مرحلتَه "
    "متعذّرة؛ وذكرُ الرقم في وحدةٍ برمجيّةٍ لا يجعله مقيسًا"
)

THE_BARRIERS_STAY_OPEN: Final[str] = (
    "TheBarriersStayOpen: حواجزُ الاستيراد تبقى `OPEN`، ورفعُ حاجزٍ يكون في "
    "الالتزام الذي يُضيف بصمةَ مصدره وفحصَها لا في وحدة تسجيل"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`، "
    "ولا استيرادَ من `kernel/`"
)

MILESTONE_BLOCKING_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_BLOCKING_INPUT_IS_NOT_A_MISSING_EFFORT,
    AN_UNBUILT_MILESTONE_IS_NAMED_NOT_OMITTED,
    NO_FIGURE_CROSSES_A_STANDING_BLOCK,
    THE_BARRIERS_STAY_OPEN,
    THIS_IS_REGISTRATION_NOT_AUTHORITY,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def registration_digest() -> str:
    """بصمةُ هذا التسجيل، محسوبةً عند الاستيراد لا مكتوبةً رقمًا ثابتًا."""

    return canonical_digest(
        canonical_bytes(
            {
                "open_questions": [
                    question.as_canonical_content() for question in OPEN_QUESTIONS
                ],
                "blocked_milestones": [
                    milestone.as_canonical_content() for milestone in BLOCKED_MILESTONES
                ],
                "named_residuals": list(MILESTONE_BLOCKING_NAMED_RESIDUALS),
            }
        )
    )


REGISTRATION_DIGEST: Final[str] = registration_digest()
"""البصمةُ المُجمَّدة؛ وأيُّ تغييرٍ في نصٍّ أعلاه يُغيّرها فيُكشَف."""


def _refuse_an_incomplete_registration() -> None:
    """احرس الوحدةَ عند الاستيراد: حواجزُ مفتوحة، ومراحلُ بلا حقل نتيجة."""

    if any(
        barrier.standing is not ImportBarrierStanding.OPEN
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS
    ):
        raise MilestoneBlockingError(
            "حاجزٌ مرفوعٌ يُبطِل تسجيلَ المرحلة C محجوبةً؛ ورفعُ الحاجز "
            "يُراجَع معه هذا التسجيل"
        )
    for milestone in BLOCKED_MILESTONES:
        for field_name in ("result", "outcome", "resolution", "verdict"):
            if field_name in milestone.__dataclass_fields__:
                raise MilestoneBlockingError(
                    f"حقلُ {field_name!r} لا يكون في مرحلةٍ لم تُبنَ"
                )
    if list(MILESTONE_BLOCKING_NAMED_RESIDUALS) != sorted(
        MILESTONE_BLOCKING_NAMED_RESIDUALS
    ):
        raise MilestoneBlockingError("البواقي المُسمّاةُ تُرتَّب ترتيبًا ثابتًا")


_refuse_an_incomplete_registration()
