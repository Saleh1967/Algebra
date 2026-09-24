"""أثرُ التصميم: القسمةُ على الجذر حدٌّ محافظ، وعدمُ بلوغه ليس تكذيبًا.

**العطلُ الذي تعالجه هذه الوحدة**: يُصحَّح `z` لتعالق العناقيد بقسمته على
جذر «الوقوعات للعنقود». وتلك قسمةٌ **ليست محايدة**: أثرُ التصميم
`DEFF = 1 + (m̄ − 1)·ρ`، والقسمةُ على `√m̄` تكافئ `ρ = 1` بالضبط — أي أنّ
كلَّ وقوعات العنقود معلومةٌ واحدةٌ مكرَّرة. فهي **الطرفُ الأقصى** من مجالٍ،
لا نقطةً وسطى. و`ρ` يُقاس من البيانات؛ فإن لم يُقَس فالمقسومُ عليه مفروضٌ لا
مقيس.

`A_CONSERVATIVE_BOUND_CANNOT_REFUTE`: ولذلك لا تُرجِع هذه الوحدةُ حكمًا
اسمُه «مردود» من `z` وحدَه ألبتّة. فالحدُّ المحافظ يضخّم الخطأ عمدًا؛ فمن
بلغه فقد **ثبت** رغمَ التضخيم، ومن لم يبلغه فهو **غيرُ مُثبَتٍ** لا ساقط.
والفرقُ بينهما فرقُ القطع والظنّ، لا درجتان في الثقة. وأمّا الردُّ فله
بابُه: مجالٌ مقيسٌ يقع **كلُّه** دون هامشٍ مُعلَنٍ قبل النظر — وذلك اختبارٌ
آخرُ بشرطٍ آخر، و`refuted_against` وحدَها تفتحه.

`THE_MEAN_OVER_ALL_IS_NOT_THE_MEAN_OVER_THOSE_THAT_HAVE_ANY`: ومتوسّطُ حجم
العنقود محسوبًا على العناقيد كلِّها غيرُ محسوبٍ على **ما له فردٌ واحدٌ فأكثر**.
فإن كان نصفُ العقد معزولًا فمتوسّطُ ذوي الشاهد ضِعفُ المُعلَن. ولذلك يُرَدّ
سؤالُ حجم العنقود ما لم يُعلَن **نصيبُ المعزولات** — والعددُ المأخوذُ على
جمهورٍ نصفُه لا يُسهم بشيءٍ ليس متوسّطَ من يُسهم.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

__all__ = [
    "A_CONSERVATIVE_BOUND_CANNOT_REFUTE_NOTE",
    "ClusterProfile",
    "DESIGN_EFFECT_NAMED_RESIDUALS",
    "DesignEffectError",
    "EffectReading",
    "EffectStanding",
    "THE_MEAN_OVER_ALL_IS_NOT_THE_MEAN_OVER_THOSE_THAT_HAVE_ANY_NOTE",
    "THE_SQUARE_ROOT_RULE_FIXES_THE_CORRELATION_AT_ONE_NOTE",
    "conventional_threshold",
    "deflate",
    "design_effect",
    "read_effect",
    "refuted_against",
]


class DesignEffectError(ValueError):
    """رُفض مدخلٌ خارج المجال، أو سؤالٌ سبق إعلانَه."""


class EffectStanding(Enum):
    """منازلُ الأثر، مغلقةً ثلاثًا: ولا منزلةَ اسمُها «قريبٌ من الحدّ»."""

    ESTABLISHED = "بلغ الحدَّ رغم التضخيم"
    UNESTABLISHED = "لم يبلغه، ولم يُرَدّ"
    REFUTED = "مجالٌ مقيسٌ كلُّه دون هامشٍ مُعلَن"


def conventional_threshold() -> Fraction:
    """الحدُّ المتعارَف ١٫٩٦ كسرًا صحيحًا؛ ويُعلَن مع كلّ قراءةٍ ولا يُفترَض."""

    return Fraction(49, 25)


@dataclass(frozen=True, slots=True)
class ClusterProfile:
    """صورةُ العنقدة: وقوعاتٌ وعناقيدُ، **ونصيبُ المعزولات مُعلَن**."""

    observations: int
    clusters: int
    isolated: Fraction

    def __post_init__(self) -> None:
        if self.clusters < 1:
            raise DesignEffectError("عنقودٌ واحدٌ فأكثر؛ وصفرُ عناقيدَ ليس عيّنة.")
        if self.observations < 0:
            raise DesignEffectError("وقوعاتٌ سالبةٌ لا تُعَدّ.")
        if not 0 <= self.isolated < 1:
            raise DesignEffectError(
                "نصيبُ المعزولات في [٠، ١)؛ وواحدٌ صحيحٌ يعني ألّا عنقودَ يُسهم."
            )

    @property
    def mean_over_all(self) -> Fraction:
        """متوسّطُ الحجم على العناقيد كلِّها، بما فيها ما لا يُسهم بشيء."""

        return Fraction(self.observations, self.clusters)

    @property
    def mean_over_active(self) -> Fraction:
        """متوسّطُ الحجم على **ذوي الشاهد** وحدَهم؛ وهو الذي يدخل أثرَ التصميم."""

        return self.mean_over_all / (1 - self.isolated)


def design_effect(mean_size: Fraction, correlation: Fraction) -> Fraction:
    """`DEFF = 1 + (m̄ − 1)·ρ`؛ و`ρ` يُعلَن ولا يُفترَض."""

    if mean_size < 1:
        raise DesignEffectError("متوسّطُ الحجم واحدٌ فأكثر.")
    if not 0 <= correlation <= 1:
        raise DesignEffectError("ρ في [٠، ١]؛ وخارجَه ليس معامل تعالقٍ داخليّ.")
    return 1 + (mean_size - 1) * correlation


def deflate(statistic: float, effect: Fraction) -> float:
    """اقسم `z` على جذر أثر التصميم؛ وأثرٌ دون الواحد يُرَدّ لا يُقرَّب."""

    if effect < 1:
        raise DesignEffectError("أثرُ تصميمٍ دون الواحد يُصغّر الخطأ لا يكبّره.")
    return statistic / math.sqrt(float(effect))


@dataclass(frozen=True, slots=True)
class EffectReading:
    """قراءةُ أثرٍ كاملة: الخامُ، والمقسومُ، وأثرُ التصميم، و`ρ` إن قِيس."""

    raw: float
    deflated: float
    effect: Fraction
    correlation: Fraction | None
    threshold: Fraction
    standing: EffectStanding

    def __post_init__(self) -> None:
        if self.standing is EffectStanding.REFUTED:
            raise DesignEffectError(
                "لا يُبلَغ «مردود» من `z` وحدَه؛ وبابُه `refuted_against` "
                "بهامشٍ مُعلَنٍ ومجالٍ مقيس."
            )
        reached = self.deflated >= float(self.threshold)
        if reached is not (self.standing is EffectStanding.ESTABLISHED):
            raise DesignEffectError(
                "المنزلةُ تُشتَقّ من بلوغ الحدّ؛ وقراءةٌ تخالف اشتقاقَها دعوًى ثانية."
            )
        if self.correlation is not None and not 0 <= self.correlation <= 1:
            raise DesignEffectError("ρ في [٠، ١]؛ وقراءةٌ تحمل خارجَه لا تُبنى.")

    @property
    def is_a_bound_not_an_estimate(self) -> bool:
        """أهذه قراءةُ حدٍّ محافظٍ أم قراءةُ تقدير؟ و`ρ` غيرُ مقيسٍ يعني الأولى."""

        return self.correlation is None


def read_effect(
    statistic: float,
    profile: ClusterProfile,
    *,
    correlation: Fraction | None = None,
    threshold: Fraction | None = None,
) -> EffectReading:
    """اقرأ منزلةَ أثرٍ مقسومًا على أثر تصميمه؛ و`ρ` غيرُ المقيس يعني الطرفَ الأقصى.

    فإن لم يُعلَن `ρ` حُسِب أثرُ التصميم عند `ρ = 1` — وهو ما تفعله القسمةُ
    على `√m̄` ضمنًا — وسُمّيت القراءةُ **حدًّا محافظًا**. وعندها لا تكون
    المنزلةُ إلّا «بلغ» أو «لم يُثبَت»، ولا تكون «مردودًا» ألبتّة.
    """

    limit = conventional_threshold() if threshold is None else threshold
    if limit <= 0:
        raise DesignEffectError("الحدُّ موجبٌ.")
    mean = profile.mean_over_active
    effect = design_effect(mean, Fraction(1) if correlation is None else correlation)
    deflated = deflate(statistic, effect)
    standing = (
        EffectStanding.ESTABLISHED
        if deflated >= float(limit)
        else EffectStanding.UNESTABLISHED
    )
    return EffectReading(
        raw=statistic,
        deflated=deflated,
        effect=effect,
        correlation=correlation,
        threshold=limit,
        standing=standing,
    )


def refuted_against(
    interval: tuple[Fraction, Fraction], margin: Fraction
) -> EffectStanding:
    """البابُ الوحيدُ إلى «مردود»: مجالٌ مقيسٌ يقع كلُّه دون هامشٍ مُعلَن.

    والهامشُ يُكتَب **قبل** النظر: أصغرُ أثرٍ تُعَدّ الدعوى معه قائمة. فمجالٌ
    أعلاه دون الهامش يردُّ الدعوى ردًّا، ومجالٌ يشمل الهامشَ لا يردُّها ولا
    يُثبِتها.
    """

    low, high = interval
    if low > high:
        raise DesignEffectError("مجالٌ أدناه فوق أعلاه ليس مجالًا.")
    if margin <= 0:
        raise DesignEffectError("الهامشُ موجبٌ؛ وهامشُ صفرٍ لا يُرَدّ به شيء.")
    if high < margin:
        return EffectStanding.REFUTED
    return EffectStanding.UNESTABLISHED


THE_SQUARE_ROOT_RULE_FIXES_THE_CORRELATION_AT_ONE_NOTE: Final[str] = (
    "TheSquareRootRuleFixesTheCorrelationAtOne: القسمةُ على `√m̄` تكافئ "
    "`ρ = 1` في `DEFF = 1 + (m̄ − 1)ρ`؛ فهي طرفٌ أقصى لا تصحيحٌ محايد، "
    "و`ρ` يُقاس من البيانات ولا يُفترَض"
)

A_CONSERVATIVE_BOUND_CANNOT_REFUTE_NOTE: Final[str] = (
    "AConservativeBoundCannotRefute: من بلغ حدًّا محافظًا ثبت رغم التضخيم، "
    "ومن لم يبلغه فغيرُ مُثبَتٍ لا مردود؛ والردُّ بابُه مجالٌ مقيسٌ كلُّه دون "
    "هامشٍ مُعلَنٍ قبل النظر"
)

THE_MEAN_OVER_ALL_IS_NOT_THE_MEAN_OVER_THOSE_THAT_HAVE_ANY_NOTE: Final[str] = (
    "TheMeanOverAllIsNotTheMeanOverThoseThatHaveAny: متوسّطُ حجم العنقود على "
    "العناقيد كلِّها غيرُ متوسّطه على ذوي الشاهد؛ فيُعلَن نصيبُ المعزولات أو "
    "يُرَدّ السؤال"
)

DESIGN_EFFECT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_SQUARE_ROOT_RULE_FIXES_THE_CORRELATION_AT_ONE_NOTE,
    A_CONSERVATIVE_BOUND_CANNOT_REFUTE_NOTE,
    THE_MEAN_OVER_ALL_IS_NOT_THE_MEAN_OVER_THOSE_THAT_HAVE_ANY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
