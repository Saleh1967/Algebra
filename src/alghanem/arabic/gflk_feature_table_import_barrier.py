"""حاجزُ استيرادِ جداول المخرج/الصفة، وتوقّعُ اختبار OCP مكتوبًا قبل قياسه.

جداولُ المخرج والصفة **مستوردةٌ لا مولودةٌ هنا**. فدخولُها يقع على منوال
`imported_feature_vocabulary`: بمصدرٍ مسمًّى، وببصمةٍ، وبتصريحٍ أنّها ليست
دعوى هذه الشجرة. وهذه الوحدةُ تسجّل ما يمنع دخولَها الآن، وما يرفع المنع.

`AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE`: الجدولُ المستورَدُ يُنسَب إلى
مصدره ويبقى منسوبًا إليه؛ فما إن يُستعمَل بلا نسبةٍ حتّى يصير — بعد جلساتٍ —
كأنّه ممّا اشتُقَّ هنا، فيُستشهَد به على نفسه.

`THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOT_AFTER`: المواصفةُ تقول
ثلاثَ عشرةَ فئةَ مخرجٍ، والشجرةُ تحمل جدولًا مُبصَّمًا بستّةَ عشرَ مخرجًا
وثمانيةٍ وعشرين صامتًا، وفيه حارسٌ يرفض غيرَ ١٦. فإن استُورِد الجدولُ ثمّ
نُظِر في التعارض، صار في الشجرة رقمان لشيءٍ واحدٍ وصار الاختيارُ بينهما
اختيارًا لما يوافق نتيجةً مرغوبة. والحسمُ قبل الاستيراد يمنع ذلك بنيويًّا.

`AN_ANALYTIC_TRUTH_IS_NOT_A_DISCOVERY`: علاقةُ `إطباق ⊆ استعلاء` — إن كان
الإطباقُ مُعرَّفًا بما يستلزم الاستعلاء — تحصيلُ حاصلٍ من التعريف، لا خبرٌ عن
العربية. وتوفيرُ الترميز الشجريّ المبنيّ عليها يُنسَب إلى **بنيةِ التعريف** لا
إلى بنية اللغة. وهذا لا يُبطل التوفير؛ يُبطل قراءتَه اكتشافًا.

`THE_EXPECTATION_IS_WRITTEN_BEFORE_THE_MEASUREMENT`: توقّعُ اختبار OCP يُكتَب
هنا قبل إجرائه: **DEFER لا PASS**. فالمرشّحُ الأقوى سقط عند الإغلاق المستقلّ
لا عند الرقم (`phonetic_economy_candidate`, `DEFER_IN_SCOPE`)، وسببُ سقوطه
قائمٌ بعينه: كوربصٌ واحدٌ، وأداةٌ واحدة، وتعريفُ مقياسٍ واحد. فما لم يُضَفّ خطٌّ
ثانٍ مستقلٌّ حقًّا، فالمتوقَّعُ ما سبق. ومن كتب توقّعَه بعد رؤية الرقم لم يتوقّع.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .classical_makharij_table import CLASSICAL_MAKHARIJ

__all__ = [
    "AN_ANALYTIC_TRUTH_IS_NOT_A_DISCOVERY_NOTE",
    "AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE_NOTE",
    "ANALYTIC_REGISTRATIONS",
    "FEATURE_TABLE_IMPORT_BARRIERS",
    "OCP_PREREGISTERED_EXPECTATION",
    "THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOT_AFTER_NOTE",
    "THE_EXPECTATION_IS_WRITTEN_BEFORE_THE_MEASUREMENT_NOTE",
    "AnalyticRegistration",
    "FeatureTableImportBarrier",
    "FeatureTableImportError",
    "ImportBarrierStanding",
    "PreregisteredExpectation",
    "frozen_makhraj_count",
]


class FeatureTableImportError(ValueError):
    """رفضٌ عند الإنشاء: حاجزٌ بلا شرطِ رفع، أو توقّعٌ بلا مُبرِّرٍ سابقٍ للقياس."""


class ImportBarrierStanding(Enum):
    """منزلةُ الحاجز. `OPEN` تعني أنّ الاستيراد ممنوعٌ حتّى يُرفَع."""

    OPEN = "قائمٌ: الاستيرادُ ممنوع"
    LIFTED = "مرفوعٌ: شرطُه استُوفي"


@dataclass(frozen=True, slots=True)
class FeatureTableImportBarrier:
    """مانعٌ يحول دون استيراد جدولٍ، وشرطُ رفعه مكتوبًا."""

    table: str
    barrier: str
    what_lifts_it: str
    standing: ImportBarrierStanding

    def __post_init__(self) -> None:
        if not self.barrier.strip() or not self.what_lifts_it.strip():
            raise FeatureTableImportError(
                "حاجزٌ بلا شرطِ رفعٍ مكتوبٍ حاجزٌ يُرفَع متى شاء رافعُه"
            )


@dataclass(frozen=True, slots=True)
class AnalyticRegistration:
    """قضيّةٌ تحليليّةٌ مُسجَّلةٌ بنصّ تعريفها، فلا تُحتسَب اكتشافًا."""

    proposition: str
    definition_text: str
    what_follows_from_the_definition: str
    what_would_make_it_empirical: str

    def __post_init__(self) -> None:
        if not self.definition_text.strip():
            raise FeatureTableImportError(
                "قضيّةٌ تحليليّةٌ بلا نصِّ تعريفها لا يُتحقَّق من تحليليّتها"
            )


@dataclass(frozen=True, slots=True)
class PreregisteredExpectation:
    """توقّعٌ مكتوبٌ قبل القياس: ما يُتوقَّع، ولمَ، وما يُبطل التوقّع."""

    test_name: str
    expected_outcome: str
    grounds_known_before_measuring: str
    what_would_overturn_the_expectation: str


def frozen_makhraj_count() -> int:
    """عددُ المخارج في الجدول المُبصَّم، مقروءًا منه لا مكتوبًا هنا."""

    return len(CLASSICAL_MAKHARIJ)


FEATURE_TABLE_IMPORT_BARRIERS: Final[tuple[FeatureTableImportBarrier, ...]] = (
    FeatureTableImportBarrier(
        table="جدولُ المخرج (المواصفة: ١٣ فئة)",
        barrier=(
            "الشجرةُ تحمل جدولًا مُبصَّمًا بستّةَ عشرَ مخرجًا لثمانيةٍ وعشرين "
            "صامتًا، وفيه حارسٌ يرفض غيرَ ١٦؛ والمواصفةُ تقول ثلاثَ عشرةَ فئةً "
            "بلا مصدرٍ مسمًّى. ولو استُورِد الجدولان معًا لصار في الشجرة رقمان "
            "لشيءٍ واحدٍ، والاختيارُ بينهما يتبع النتيجةَ المرغوبة"
        ),
        what_lifts_it=(
            "إمّا مصدرٌ مسمًّى للثلاثة عشر يُبيّن أنّه تصنيفٌ آخرُ مقصودٌ لا "
            "خطأ — فيُستورَد جدولًا ثانيًا منسوبًا لا بديلًا — وإمّا إعادةُ "
            "صياغة المواصفة على الستّة عشر المُبصَّمة. ولا يُدمَج الرقمان بحال"
        ),
        standing=ImportBarrierStanding.OPEN,
    ),
    FeatureTableImportBarrier(
        table="جدولُ الصفة",
        barrier=(
            "لم يُذكَر للجدول مصدرٌ مسمًّى ولا بصمةٌ لبايتاته؛ وجدولٌ بلا بصمةٍ "
            "يتحرّك بين الجلسات ويُستشهَد به بعد تحرّكه كأنّه لم يتحرّك"
        ),
        what_lifts_it=(
            "مصدرٌ مسمًّى وبصمةُ بايتاتٍ وتصريحٌ بأنّه ليس دعوى هذه الشجرة، على "
            "منوال `imported_feature_vocabulary`"
        ),
        standing=ImportBarrierStanding.OPEN,
    ),
)


ANALYTIC_REGISTRATIONS: Final[tuple[AnalyticRegistration, ...]] = (
    AnalyticRegistration(
        proposition="إطباق ⊆ استعلاء",
        definition_text=(
            "الإطباقُ — بنصّ التعريف المستعمَل — انطباقُ اللسان على الحنك الأعلى "
            "**مع** ارتفاعه إليه؛ والاستعلاءُ ارتفاعُ اللسان إلى الحنك الأعلى. "
            "فالارتفاعُ داخلٌ في تعريف الإطباق"
        ),
        what_follows_from_the_definition=(
            "الاحتواءُ يلزم من التعريف لزومًا، ولا يحتاج إلى مدوَّنةٍ ولا إلى "
            "إحصاء؛ وتوفيرُ الترميز الشجريّ المبنيُّ عليه يُنسَب إلى بنية "
            "التعريف لا إلى بنية العربية. والتوفيرُ قائمٌ، وقراءتُه اكتشافًا "
            "هي الباطلة"
        ),
        what_would_make_it_empirical=(
            "تعريفٌ للإطباق لا يذكر الارتفاع، ثمّ رصدُ الاحتواء على مدوَّنةٍ "
            "مُبصَّمة. وعندها وحدها يصير الاحتواءُ خبرًا عن العربية"
        ),
    ),
)


OCP_PREREGISTERED_EXPECTATION: Final[PreregisteredExpectation] = (
    PreregisteredExpectation(
        test_name="اختبارُ OCP (تنافرُ المخرج/الصفة في الجذر)",
        expected_outcome="DEFER لا PASS",
        grounds_known_before_measuring=(
            "شرطُ الإغلاق المستقلّ هو ما سقط عنده المرشّحُ الأقوى سابقًا "
            "(`phonetic_economy_candidate`, `DEFER_IN_SCOPE`): خطّا الشاهد "
            "يشتركان في كوربصٍ واحدٍ وأداةٍ واحدةٍ وتعريفِ مقياسٍ واحد، فلا "
            "يُغلقان. وهذا السببُ قائمٌ بعينه في OCP: الجذورُ والتصنيفُ "
            "والمقياسُ من أصلٍ واحد، فتكرارُ الحساب تكرارُ الأداة لا شاهدٌ ثانٍ"
        ),
        what_would_overturn_the_expectation=(
            "خطٌّ ثانٍ مستقلٌّ حقًّا: مدوَّنةٌ أخرى مُبصَّمة، وتصنيفُ مخرجٍ من "
            "مصدرٍ آخرَ مسمًّى، وتعريفُ مقياسٍ لا يشتقّ من الأوّل. وما دون ذلك "
            "تكثيرٌ للأرقام لا للشواهد"
        ),
    )
)


AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE_NOTE: Final[str] = (
    "AnImportedTableIsNotAClaimOfThisTree: الجدولُ المستورَد يبقى منسوبًا إلى "
    "مصدره؛ فما استُعمِل بلا نسبةٍ صار بعد جلساتٍ كأنّه ممّا اشتُقَّ هنا "
    "فاستُشهِد به على نفسه"
)

THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOT_AFTER_NOTE: Final[str] = (
    "TheConflictIsResolvedBeforeTheImportNotAfter: تعارضُ ١٣/١٦ يُحسَم قبل "
    "الاستيراد؛ فبعده يصير في الشجرة رقمان لشيءٍ واحدٍ والاختيارُ بينهما يتبع "
    "النتيجةَ المرغوبة"
)

AN_ANALYTIC_TRUTH_IS_NOT_A_DISCOVERY_NOTE: Final[str] = (
    "AnAnalyticTruthIsNotADiscovery: ما لزم من التعريف يُسجَّل بنصّ تعريفه ولا "
    "يُحتسَب خبرًا عن اللغة؛ والتوفيرُ المبنيُّ عليه يُنسَب إلى بنية التعريف"
)

THE_EXPECTATION_IS_WRITTEN_BEFORE_THE_MEASUREMENT_NOTE: Final[str] = (
    "TheExpectationIsWrittenBeforeTheMeasurement: توقّعُ OCP مكتوبٌ DEFER قبل "
    "إجرائه؛ ومن كتب توقّعَه بعد رؤية الرقم لم يتوقّع بل وصف"
)
