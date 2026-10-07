"""اختزالُ `Closure(C,H)` إلى `s ≤ 1` على النافذة، وتقسيمٌ يتطابق بلا تدخّل.

**ما تفعله هذه الوحدة**: تردّ شرطَ إغلاق الخانة الدنيا — الشرطَ الرابعَ في
`MCU = (C, H, B)` الذي كان **يحتاج طبقةً لم تُبنَ** — إلى قيد العدد المُودَع
في ٥م: `s ≤ 1`. ثمّ تفحص الاختزالَ على القوالب الستّة في ٥هـ، فيخرج تطابقٌ
تامٌّ لم يُتدخَّل فيه.

**الاختزالُ شفّافٌ في صيغته**. بنصّ ٥م: النافذةُ بين صائتين `V C^k V`،
و`s = (k−1) + [الصائتُ السابقُ طويل]`. فإذا وُضع ما يلي القالبَ أدنى استمرارٍ
ممكنٍ — بدايةً واحدة — صار `k = إغلاقُ القالب + 1`، ومنه:

    s = إغلاقُ القالب + طولُ النواة

وهذا يجعل الحسابَ قابلًا للفحص بالعين، ولا يخفي خطوةً في تعريف.

`THE_REDUCTION_IS_A_MODELLING_STEP_NOT_A_MEASUREMENT`: ردُّ `Closure` إلى
`s ≤ 1` **خطوةُ نمذجةٍ منّا**، لا نتيجةٌ قِيست. فـ٥م يقيس القيدَ على النوافذ،
و٥هـ يحكم على القوالب بالولادة والتدوير، وليس في واحدٍ منهما أنّ إغلاقَ
الخانة الدنيا **هو** ذلك القيد. وشرطُ إبطال الاختزال مكتوبٌ في
`WHAT_WOULD_FALSIFY_THE_REDUCTION`.

`THE_PARTITIONS_COINCIDE_WITHOUT_INTERVENTION`: و`s ≤ 1` يقسم القوالبَ الستّةَ
إلى ثلاثةٍ تُغلِق — `CV` و`CVV` و`CVC` — وثلاثةٍ تسقط — `CVVC` و`CVCC`
و`CVVCC`. والقسمةُ الأولى هي **بعينها** ما حكم عليه ٥هـ بالولادة أو بالتدوير
بالزمن، والثانيةُ هي **بعينها** المُدوَّرةُ عند الحواف. وهذا تطابقٌ بين قسمين
مستقلَّين في الوثيقة، يُشتَقّ هنا بالمقارنة ولا يُكتَب.

`A_COINCIDENCE_OVER_SIX_IS_NOT_A_LAW`: والتطابقُ على **ستّة** قوالبَ عدُّ
أمثلةٍ معدودةٍ لا عدُّ مجتمع. فمنزلتُه منزلةُ
`AN_ENUMERATED_EXAMPLE_SWEEP_IS_NOT_A_UNIVERSAL`: يرفع الاختزالَ من دعوًى
مجرّدةٍ إلى دعوًى نجت من فحصٍ صغير، ولا يبلغ به قانونًا.

`THE_UPGRADE_IS_CAPPED_BY_THE_DOCUMENTS_OWN_LIMIT`: يصير المقيسُ ثلاثةً من
أربعة، لكنّ قوّةَ الثالث **محدودةٌ بحدٍّ أعلنته الوثيقةُ نفسُها** (٥م، الحدّ
الأوّل): العددُ في الرسم يكاد يكون مضمونًا، لأنّ المصحفَ المشكولَ يكتب كثيرًا
من حركات الإصلاح. فالترقيةُ في **الإمكان** لا في القوّة.

`THE_EARLIER_READING_IS_SUPERSEDED_NOT_ERASED`: قراءةُ «اثنان من أربعة» في
`minimal_complete_slot_comparison` تبقى كما هي في موضعها، ولا تُعدَّل؛ وهذه
الوحدةُ تُسجّل ما يخلفها، على منوال نسخ SLGAE.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .minimal_complete_slot_comparison import MCU_CONDITIONS, Measurability
from .slgae_deposit import SlgaeDepositError

__all__ = [
    "A_COINCIDENCE_OVER_SIX_IS_NOT_A_LAW_NOTE",
    "CLOSURE_REDUCTION_NAMED_RESIDUALS",
    "CLOSURE_THRESHOLD",
    "MINIMAL_FOLLOWING_ONSET",
    "TEMPLATES",
    "THE_PARTITIONS_COINCIDE_NOTE",
    "THE_REDUCTION_IS_A_MODELLING_STEP_NOTE",
    "THE_UPGRADE_IS_CAPPED_NOTE",
    "THE_EARLIER_READING_IS_SUPERSEDED_NOTE",
    "WHAT_WOULD_FALSIFY_THE_REDUCTION",
    "ClosureReadout",
    "PartitionCoincidence",
    "TemplateRow",
    "TemplateVerdict",
    "UpgradedStanding",
    "derive_closure_readouts",
    "derive_partition_coincidence",
    "derive_upgraded_standing",
    "window_saturation",
]

CLOSURE_THRESHOLD: Final[int] = 1
"""حدُّ القيد في ٥م: `s ≤ 1`، أي «لا يلتقي ساكنان»."""

MINIMAL_FOLLOWING_ONSET: Final[int] = 1
"""أدنى استمرارٍ ممكنٍ بعد القالب: بدايةٌ واحدة، وهو مقامُ فحص الإغلاق."""


class TemplateVerdict(Enum):
    """حكمُ ٥هـ على القالب، بأصنافه الثلاثة كما وردت."""

    BORN = "مولود"
    RECYCLED_BY_TIME = "مُدوَّر بالزمن"
    RECYCLED_AT_EDGE = "مُدوَّر عند الحافة"


@dataclass(frozen=True, slots=True)
class TemplateRow:
    """قالبٌ من الستّة: إغلاقُه، وطولُ نواته، وعددُه، وحكمُ ٥هـ عليه."""

    name: str
    coda: int
    long_nucleus: int
    syllables: int
    verdict: TemplateVerdict

    def __post_init__(self) -> None:
        if self.coda < 0 or self.long_nucleus not in (0, 1):
            raise SlgaeDepositError("الإغلاقُ غيرُ سالب، وطولُ النواة صفرٌ أو واحدٌ حصرًا.")
        if self.syllables <= 0:
            raise SlgaeDepositError("عددُ المقاطع موجب.")


TEMPLATES: Final[tuple[TemplateRow, ...]] = (
    TemplateRow("CV", 0, 0, 93_229, TemplateVerdict.BORN),
    TemplateRow("CVV", 0, 1, 40_475, TemplateVerdict.RECYCLED_BY_TIME),
    TemplateRow("CVC", 1, 0, 67_361, TemplateVerdict.BORN),
    TemplateRow("CVVC", 1, 1, 8_036, TemplateVerdict.RECYCLED_AT_EDGE),
    TemplateRow("CVCC", 2, 0, 755, TemplateVerdict.RECYCLED_AT_EDGE),
    TemplateRow("CVVCC", 2, 1, 5, TemplateVerdict.RECYCLED_AT_EDGE),
)
"""القوالبُ الستّةُ كما نُشرت في ٥هـ، بأعدادها وأحكامها."""


def window_saturation(
    coda: int, long_nucleus: int, following_onset: int = MINIMAL_FOLLOWING_ONSET
) -> int:
    """`s` على النافذة، محسوبًا بنصّ تعريف ٥م لا بصيغةٍ مختصرةٍ تُخفي خطوة.

    النافذةُ بين صائتين تحمل `k = إغلاقُ القالب + بدايةُ ما يليه` من السواكن،
    و`s = (k − 1) + طولُ النواة السابقة`.
    """

    if coda < 0 or following_onset < 1:
        raise SlgaeDepositError(
            "الإغلاقُ غيرُ سالب، وبدايةُ ما يلي واحدةٌ على الأقلّ؛ "
            "ونافذةٌ بلا بدايةٍ بعدها ليست نافذةً بين صائتين."
        )
    if long_nucleus not in (0, 1):
        raise SlgaeDepositError("طولُ النواة صفرٌ أو واحدٌ حصرًا.")
    consonants = coda + following_onset
    return (consonants - 1) + long_nucleus


@dataclass(frozen=True, slots=True)
class ClosureReadout:
    """قراءةُ قالبٍ واحد: `s` وحكمُ الإغلاق وحكمُ ٥هـ معه."""

    name: str
    saturation: int
    closes: bool
    verdict: TemplateVerdict
    syllables: int

    def __post_init__(self) -> None:
        if self.closes != (self.saturation <= CLOSURE_THRESHOLD):
            raise SlgaeDepositError(
                "حكمُ الإغلاق لا يطابق `s ≤ 1`؛ وحكمٌ يُكتَب ولا يُشتَقّ " "دعوى لا حساب."
            )


def derive_closure_readouts() -> tuple[ClosureReadout, ...]:
    """شغِّل الاختزالَ على القوالب الستّة؛ ولا حكمَ فيها مكتوبٌ بيد."""

    return tuple(
        ClosureReadout(
            name=row.name,
            saturation=window_saturation(row.coda, row.long_nucleus),
            closes=window_saturation(row.coda, row.long_nucleus) <= CLOSURE_THRESHOLD,
            verdict=row.verdict,
            syllables=row.syllables,
        )
        for row in TEMPLATES
    )


@dataclass(frozen=True, slots=True)
class PartitionCoincidence:
    """تطابقُ قسمةِ `s ≤ 1` بقسمةِ ٥هـ، مُشتَقًّا بالمقارنة لا مكتوبًا."""

    closing: tuple[str, ...]
    failing: tuple[str, ...]
    edge_recycled: tuple[str, ...]
    not_edge_recycled: tuple[str, ...]
    coincides: bool
    failing_syllables: int
    total_syllables: int

    @property
    def failing_share(self) -> float:
        """نصيبُ المقاطع الساقطةِ من مجموعِ ما عُدّ في ٥هـ."""

        return self.failing_syllables / self.total_syllables


def derive_partition_coincidence() -> PartitionCoincidence:
    """قابِلْ قسمةَ القيد بقسمةِ الأحكام، وأخرِج التطابقَ بالمقارنة."""

    readouts = derive_closure_readouts()
    closing = tuple(item.name for item in readouts if item.closes)
    failing = tuple(item.name for item in readouts if not item.closes)
    edge = tuple(
        item.name
        for item in readouts
        if item.verdict is TemplateVerdict.RECYCLED_AT_EDGE
    )
    not_edge = tuple(
        item.name
        for item in readouts
        if item.verdict is not TemplateVerdict.RECYCLED_AT_EDGE
    )
    return PartitionCoincidence(
        closing=closing,
        failing=failing,
        edge_recycled=edge,
        not_edge_recycled=not_edge,
        coincides=set(closing) == set(not_edge) and set(failing) == set(edge),
        failing_syllables=sum(item.syllables for item in readouts if not item.closes),
        total_syllables=sum(item.syllables for item in readouts),
    )


WHAT_WOULD_FALSIFY_THE_REDUCTION: Final[tuple[str, ...]] = (
    "قالبٌ `s ≤ 1` يحكم عليه ٥هـ بالتدوير عند الحافة",
    "قالبٌ `s > 1` يحكم عليه ٥هـ بالولادة أو بالتدوير بالزمن",
    "خانةٌ دنيا مقبولةٌ في القوالب المُودَعة يردّها `s ≤ 1`",
    "قيدٌ آخرُ يقسم القوالبَ القسمةَ نفسَها بلا عدّ سواكن، فيسقط تخصيصُ العدد",
)
"""شروطُ إبطال الاختزال، مكتوبةً قبل الفحص لا بعده."""


@dataclass(frozen=True, slots=True)
class UpgradedStanding:
    """منزلةُ شروط المقترَح بعد الاختزال، والقراءةُ السابقةُ مذكورةٌ معها."""

    measurable_before: int
    measurable_after: int
    total: int
    upgraded_condition: str
    capped_by: str

    def __post_init__(self) -> None:
        if self.measurable_after <= self.measurable_before:
            raise SlgaeDepositError("ترقيةٌ لا تزيد المقيسَ ليست ترقية؛ ولا تُسجَّل.")
        if self.measurable_after > self.total:
            raise SlgaeDepositError("المقيسُ لا يزيد على مجموع الشروط.")
        if not self.capped_by.strip():
            raise SlgaeDepositError("ترقيةٌ بلا حدٍّ مكتوبٍ تُقرأ رفعًا للقوّة لا للإمكان.")


def derive_upgraded_standing() -> UpgradedStanding:
    """أخرِج المنزلةَ الجديدة، مُشتَقّةً من منازل الشروط لا مكتوبةً رقمًا."""

    before = sum(
        1
        for condition in MCU_CONDITIONS
        if condition.standing is Measurability.MEASURABLE_HERE
    )
    needs_layer = tuple(
        condition
        for condition in MCU_CONDITIONS
        if condition.standing is Measurability.NEEDS_A_LAYER_NOT_BUILT
    )
    if len(needs_layer) != 1:  # pragma: no cover - حارس
        raise SlgaeDepositError(
            "الشرطُ المحتاجُ طبقةً ليس واحدًا؛ والترقيةُ مبنيّةٌ على أنّه واحد."
        )
    return UpgradedStanding(
        measurable_before=before,
        measurable_after=before + 1,
        total=len(MCU_CONDITIONS),
        upgraded_condition=needs_layer[0].expression,
        capped_by=(
            "٥م، الحدُّ الأوّل: العددُ في الرسم يكاد يكون مضمونًا لأنّ المصحفَ "
            "المشكولَ يكتب كثيرًا من حركات الإصلاح؛ فالترقيةُ في الإمكان لا "
            "في القوّة"
        ),
    )


THE_REDUCTION_IS_A_MODELLING_STEP_NOTE: Final[str] = (
    "TheReductionIsAModellingStepNotAMeasurement: ردُّ Closure إلى s ≤ 1 "
    "خطوةُ نمذجةٍ منّا؛ فـ٥م يقيس القيدَ على النوافذ و٥هـ يحكم على القوالب، "
    "وليس في واحدٍ منهما أنّ إغلاقَ الخانة هو ذلك القيد"
)

THE_PARTITIONS_COINCIDE_NOTE: Final[str] = (
    "ThePartitionsCoincideWithoutIntervention: s ≤ 1 يقسم القوالبَ إلى "
    "{CV, CVV, CVC} و{CVVC, CVCC, CVVCC}، وهما بعينهما قسمةُ ٥هـ بين "
    "المولودِ والمُدوَّرِ بالزمن من جهةٍ والمُدوَّرِ عند الحافة من أخرى"
)

A_COINCIDENCE_OVER_SIX_IS_NOT_A_LAW_NOTE: Final[str] = (
    "ACoincidenceOverSixIsNotALaw: التطابقُ على ستّة قوالبَ عدُّ أمثلةٍ "
    "معدودةٍ لا عدُّ مجتمع؛ فيرفع الاختزالَ إلى دعوًى نجت من فحصٍ صغير، "
    "ولا يبلغ به قانونًا"
)

THE_UPGRADE_IS_CAPPED_NOTE: Final[str] = (
    "TheUpgradeIsCappedByTheDocumentsOwnLimit: صار المقيسُ ثلاثةً من أربعة، "
    "وقوّةُ الثالث محدودةٌ بحدّ ٥م الأوّل — العددُ في الرسم يكاد يكون مضمونًا؛ "
    "فالترقيةُ في الإمكان لا في القوّة"
)

THE_EARLIER_READING_IS_SUPERSEDED_NOTE: Final[str] = (
    "TheEarlierReadingIsSupersededNotErased: قراءةُ «اثنان من أربعة» تبقى في "
    "موضعها ولا تُعدَّل، وهذه الوحدةُ تُسجّل ما يخلفها"
)

CLOSURE_REDUCTION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_REDUCTION_IS_A_MODELLING_STEP_NOTE,
    THE_PARTITIONS_COINCIDE_NOTE,
    A_COINCIDENCE_OVER_SIX_IS_NOT_A_LAW_NOTE,
    THE_UPGRADE_IS_CAPPED_NOTE,
    THE_EARLIER_READING_IS_SUPERSEDED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(TEMPLATES) != 6:  # pragma: no cover - حارس
    raise RuntimeError("القوالبُ ستّةٌ في ٥هـ؛ وزيادةٌ أو نقصٌ يُبطِل المقابلة.")
if not WHAT_WOULD_FALSIFY_THE_REDUCTION:  # pragma: no cover - حارس
    raise RuntimeError(
        "اختزالٌ بلا شرطِ إبطالٍ يُثبَّت مهما جاءت البيانات؛ وذلك دعوى لا اختبار."
    )
