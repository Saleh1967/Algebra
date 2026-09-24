"""بلوغُ الحدّ: هل يستطيع اختبارٌ أن يبلغ عتبتَه بآلته أصلًا؟

**ما تفعله هذه الوحدة**: تحسب — قبل أيّ تشغيل — ما إذا كان حدُّ القبول المُعلَن
**قابلًا للبلوغ** بعدد التكرارات المُعلَن، وكم مخرجًا من مخارج الرفض متاحٌ فعلًا.

والسببُ أنّ أرضيّةَ قيمة `p` في اختبارٍ تبديليٍّ بـ`B` تكرارًا هي `1/(B+1)`،
وقيمُها المتاحةُ متقطّعةٌ `(k+1)/(B+1)`. فحدٌّ أصغرُ من الأرضيّة **لا يُبلَغ
أبدًا**، وحدٌّ يقع بين الأرضيّة وتاليها يجعل منطقةَ الرفض **نقطةً واحدة**:
تكرارٌ واحدٌ يبلغ المرصودَ يُسقِط الأثرَ مهما كان قويًّا. وفي كلتا الحالين
النتيجةُ يحكمها خشونةُ النموذج الصفريّ لا البيانات.

`A_THRESHOLD_ITS_OWN_MACHINE_CANNOT_REACH_IS_NOT_A_THRESHOLD`: تُجمَّد مقاييسُ
بحدودٍ لا يُفحَص أنّ آلتَها تبلغها، فيُقرأ «لم يظهر الفرقُ» خبرًا عن الظاهرة
وهو خبرٌ عن عددِ التكرار. وهذا يُحسَب **قبل** النظر، فيُصحَّح بلا أن يُمَسَّ حدٌّ
بعد رؤية رقم.

`RAISE_THE_REPLICATES_DO_NOT_LOWER_THE_THRESHOLD`: الحدُّ يُشتَقّ من تصميم
الاختبار وعائلته، والتكرارُ ميزانيّةُ حساب. فتخفيضُ الحدّ ليوافق ميزانيّةً هو
تفصيلُ المقياس على مقاس الآلة بعد أن عُرف ضيقُها؛ ورفعُ التكرار لا يمسّ دعوًى.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_DOMAIN`: ما هنا حسابٌ على `(α, B)` وعددِ
العائلة، لا حكمٌ على فرضيّةٍ بعينها.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

__all__ = [
    "ATTAINABILITY_NAMED_RESIDUALS",
    "A_THRESHOLD_ITS_OWN_MACHINE_CANNOT_REACH_IS_NOT_A_THRESHOLD_NOTE",
    "Attainability",
    "AttainabilityError",
    "AttainabilityReading",
    "RAISE_THE_REPLICATES_DO_NOT_LOWER_THE_THRESHOLD_NOTE",
    "attainable_rejection_outcomes",
    "bonferroni_threshold",
    "minimum_replicates_for",
    "permutation_floor",
    "read_attainability",
]


class AttainabilityError(ValueError):
    """رُفض مدخلٌ خارج المجال؛ ولا يُقرَّب إلى أقرب مقبول."""


class Attainability(Enum):
    """منازلُ البلوغ، مغلقةً ثلاثًا: ولا منزلةَ اسمُها «مقبولٌ على مضض»."""

    UNREACHABLE = "لا يُبلَغ"
    KNIFE_EDGE = "على حدِّ السكّين"
    ROOMY = "فيه سعة"


def permutation_floor(replicates: int) -> Fraction:
    """أدنى قيمةِ `p` ممكنةٍ باختبارٍ تبديليٍّ بـ`B` تكرارًا: `1/(B+1)`."""

    if replicates < 1:
        raise AttainabilityError("التكراراتُ واحدٌ فأكثر.")
    return Fraction(1, replicates + 1)


def bonferroni_threshold(alpha: Fraction, family_size: int) -> Fraction:
    """حدُّ بونفيروني `α/m`؛ وعددُ العائلة يُعلَن قبل العدّ لا بعده."""

    if not 0 < alpha <= 1:
        raise AttainabilityError("α بين الصفر والواحد، والطرفُ الأدنى مفتوح.")
    if family_size < 1:
        raise AttainabilityError("عددُ العائلة واحدٌ فأكثر.")
    return alpha / family_size


def attainable_rejection_outcomes(threshold: Fraction, replicates: int) -> int:
    """كم مخرجًا من مخارج الرفض يبلغ الحدَّ فعلًا: عددُ `k` بحيث `(k+1)/(B+1) ≤ α`.

    فإن كانت النتيجةُ صفرًا فالحدُّ **لا يُبلَغ**، وإن كانت واحدًا فمنطقةُ
    الرفض نقطةٌ واحدةٌ: تجاوزٌ واحدٌ يُسقِط الأثر.
    """

    if threshold <= 0:
        raise AttainabilityError("الحدُّ موجبٌ.")
    floor = permutation_floor(replicates)
    if floor > threshold:
        return 0
    return int(threshold * (replicates + 1))


def minimum_replicates_for(threshold: Fraction, outcomes: int) -> int:
    """أدنى عددِ تكرارٍ يجعل مخارجَ الرفض المتاحةَ `outcomes` فأكثر."""

    if outcomes < 1:
        raise AttainabilityError("المخارجُ المطلوبةُ واحدٌ فأكثر.")
    if threshold <= 0:
        raise AttainabilityError("الحدُّ موجبٌ.")
    needed = Fraction(outcomes) / threshold
    replicates = int(needed) - 1
    while attainable_rejection_outcomes(threshold, max(replicates, 1)) < outcomes:
        replicates += 1
    return max(replicates, 1)


@dataclass(frozen=True, slots=True)
class AttainabilityReading:
    """قراءةُ بلوغٍ كاملةٌ: الحدُّ، والأرضيّة، والمخارجُ، والمنزلة."""

    threshold: Fraction
    replicates: int
    floor: Fraction
    outcomes: int
    standing: Attainability

    def __post_init__(self) -> None:
        if self.outcomes == 0 and self.standing is not Attainability.UNREACHABLE:
            raise AttainabilityError("حدٌّ بلا مخرجٍ واحدٍ منزلتُه «لا يُبلَغ» لا غير.")
        if self.outcomes > 0 and self.standing is Attainability.UNREACHABLE:
            raise AttainabilityError("«لا يُبلَغ» مع مخارجَ مُعلَنةٍ تناقضٌ في القراءة.")
        derived_floor = permutation_floor(self.replicates)
        if self.floor != derived_floor:
            raise AttainabilityError(
                f"الأرضيّةُ المُعلَنةُ {self.floor} وتكرارُ {self.replicates} "
                f"يقتضي {derived_floor}؛ والقراءةُ لا تُخالف ما اشتُقّت منه."
            )
        derived_outcomes = attainable_rejection_outcomes(
            self.threshold, self.replicates
        )
        if self.outcomes != derived_outcomes:
            raise AttainabilityError(
                f"المخارجُ المُعلَنةُ {self.outcomes} والمشتقّةُ {derived_outcomes}؛ "
                "وحقلٌ مُشتَقٌّ يُخالف اشتقاقَه ليس قراءةً بل دعوًى ثانية."
            )

    @property
    def suggested_replicates(self) -> int:
        """أدنى تكرارٍ يُخرِج القراءةَ إلى السعة: عشرةُ مخارجَ فأكثر."""

        return minimum_replicates_for(self.threshold, 10)


def read_attainability(
    threshold: Fraction, replicates: int, roomy_at: int = 10
) -> AttainabilityReading:
    """اقرأ منزلةَ البلوغ: لا يُبلَغ، أم على حدِّ السكّين، أم فيه سعة.

    و`roomy_at` عددُ المخارج الذي تُسمّى عنده القراءةُ سعةً، ويُعلَن مع الحكم
    فلا يكون حدًّا مخفيًّا.
    """

    if roomy_at < 2:
        raise AttainabilityError("حدُّ السعة مخرجان فأكثر.")
    outcomes = attainable_rejection_outcomes(threshold, replicates)
    if outcomes == 0:
        standing = Attainability.UNREACHABLE
    elif outcomes < roomy_at:
        standing = Attainability.KNIFE_EDGE
    else:
        standing = Attainability.ROOMY
    return AttainabilityReading(
        threshold=threshold,
        replicates=replicates,
        floor=permutation_floor(replicates),
        outcomes=outcomes,
        standing=standing,
    )


A_THRESHOLD_ITS_OWN_MACHINE_CANNOT_REACH_IS_NOT_A_THRESHOLD_NOTE: Final[str] = (
    "AThresholdItsOwnMachineCannotReachIsNotAThreshold: حدٌّ دون أرضيّة التباديل "
    "لا يُبلَغ أبدًا، وحدٌّ يقع بين الأرضيّة وتاليها يجعل منطقةَ الرفض نقطةً "
    "واحدةً؛ وفي الحالين تحكم خشونةُ الصفريّ لا البيانات"
)

RAISE_THE_REPLICATES_DO_NOT_LOWER_THE_THRESHOLD_NOTE: Final[str] = (
    "RaiseTheReplicatesDoNotLowerTheThreshold: الحدُّ يُشتَقّ من التصميم "
    "والعائلة، والتكرارُ ميزانيّةُ حساب؛ فتخفيضُ الحدّ ليوافق الميزانيّةَ تفصيلٌ "
    "على مقاس الآلة، ورفعُ التكرار لا يمسّ دعوًى"
)

ATTAINABILITY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_THRESHOLD_ITS_OWN_MACHINE_CANNOT_REACH_IS_NOT_A_THRESHOLD_NOTE,
    RAISE_THE_REPLICATES_DO_NOT_LOWER_THE_THRESHOLD_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
