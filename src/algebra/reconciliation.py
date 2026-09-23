"""مطابقةُ الأرقام المنشورة: الرقمُ المطبوعُ مَجالٌ لا نقطة، والحاصلُ لا يسبق مقامَه.

**ما تفعله هذه الوحدة**: تأخذ أرقامًا **كما طُبِعت** — نصًّا لا عائمًا — فتشتقّ
منها ثلاثةَ أشياء: المجالَ الذي يحتمله الرقمُ عند دقّةِ طباعته، والمجالَ الذي
يحتمله حاصلُ قسمةِ رقمَين مطبوعَين، وبقيّةَ تجزئةٍ بين أجزائها ومجموعها
المُعلَن. وهي لا تعرف موضوعًا ولا مدوَّنةً ولا لغة: أربعةُ أرقامٍ وسلسلةُ محارف.

`A_PRINTED_FIGURE_IS_AN_INTERVAL_NOT_A_POINT`: «٠٫٠٠٠٤» ليست العددَ ٠٫٠٠٠٤ بل
كلَّ عددٍ يُطبَع هكذا، أي `[٠٫٠٠٠٣٥، ٠٫٠٠٠٤٥)`. ومَن يعامل المطبوعَ نقطةً يحسب
بدقّةٍ لا يملكها.

`A_QUOTIENT_MAY_NOT_OUTRUN_ITS_DENOMINATOR`: إن كان المقامُ مطبوعًا بخانةٍ
معنويّةٍ واحدة، فحاصلُ القسمة **غيرُ محدَّدٍ** بخمسِ خانات مهما بلغت دقّةُ
البسط. وإعلانُ الحاصلِ بخاناتٍ أكثرَ ممّا يحدّده مقامُه ليس خطأً في الجمع، بل
دعوى دقّةٍ لا سند لها — ورقمان مختلفان عن قياسٍ واحدٍ قد يكونان **كلاهما
متّسقَين** مع المطبوع، فيُحسَم الخلافُ بأنّه في الإعلان لا في القياس.

`A_ROUNDING_CONVENTION_IS_DECLARED_NOT_ASSUMED`: المجالُ ههنا نصفُ مفتوح
`[v−h، v+h)`، أي التقريبُ إلى أعلى عند المنتصف. وهذا **اختيارٌ مُعلَن**؛ ولو
اختير غيرُه لانتقل طرفٌ واحد. ولا يُترَك مضمرًا.

`A_DIGIT_COUNT_IS_A_CONVENTION_NOT_A_THEOREM`: «كم خانةً يحدّدها المجال» حسابٌ
باصطلاحٍ (`⌊log₁₀(القَدْر/العرض)⌋`)، لا برهان. والفحصُ الحاملُ ههنا هو
**انتماءُ المُعلَن إلى المجال**، وهو قاطعٌ لا اصطلاحيّ؛ وعدُّ الخانات تلخيصٌ
يُقرأ بعده.

`A_RESIDUE_IS_NAMED_NOT_ABSORBED`: بقيّةُ التجزئة تُعلَن عددًا، ولا تُوزَّع على
الأجزاء ولا تُسمّى «تقريبًا». وبقيّةُ الصفر خبرٌ كبقيّة الواحد.

`THIS_MODULE_READS_FIGURES_NOT_CLAIMS`: ما هنا حسابٌ على محارفَ وأعداد. وأنّ
الرقمَ صادقٌ على شيءٍ في العالم مسألةٌ أخرى لا تُقاس ههنا.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Final, Protocol

__all__ = [
    "A_DIGIT_COUNT_IS_A_CONVENTION_NOT_A_THEOREM_NOTE",
    "A_PRINTED_FIGURE_IS_AN_INTERVAL_NOT_A_POINT_NOTE",
    "A_QUOTIENT_MAY_NOT_OUTRUN_ITS_DENOMINATOR_NOTE",
    "A_RESIDUE_IS_NAMED_NOT_ABSORBED_NOTE",
    "A_ROUNDING_CONVENTION_IS_DECLARED_NOT_ASSUMED_NOTE",
    "RECONCILIATION_NAMED_RESIDUALS",
    "Difference",
    "Partition",
    "PrintedFigure",
    "Quotient",
    "QuotientClaim",
    "Reading",
    "ReconciliationError",
    "rounds_alike",
    "rounds_to",
]

_PRINTED: Final[re.Pattern[str]] = re.compile(r"^[+-]?(\d+)(?:\.(\d+))?$")


class ReconciliationError(ValueError):
    """رُفض رقمٌ أو تجزئةٌ لا تقبل الحساب؛ ولا يُحمَل على أقرب مقبول."""


class Reading(Protocol):
    """قراءةٌ لها قيمةٌ ومجال: رقمٌ مطبوعٌ، أو فرقُ رقمَين مطبوعَين."""

    @property
    def value(self) -> Fraction:
        """القيمةُ الاسميّة."""

    def interval(self) -> tuple[Fraction, Fraction]:
        """المجالُ الذي يحتمله المطبوع."""


def rounds_to(value: Fraction, places: int) -> Fraction:
    """تقريبُ `value` إلى `places` منزلةً بالاصطلاح المُعلَن (المنتصفُ لأعلى).

    و`places` سالبةٌ جائزة: `-2` تقريبٌ إلى المئات.
    """

    quantum = Fraction(10) ** places
    return Fraction(math.floor(value * quantum + Fraction(1, 2))) / quantum


def rounds_alike(first: Fraction, second: Fraction, places: int) -> bool:
    """أيُطبَع العددان **بالصورة نفسها** عند هذه الدقّة؟ فالفرقُ مستورٌ إذن."""

    return rounds_to(first, places) == rounds_to(second, places)


@dataclass(frozen=True, slots=True)
class PrintedFigure:
    """رقمٌ كما طُبِع: نصُّه هو المعطى، ودقّتُه تُقرأ منه لا تُخمَّن.

    والنصُّ هو المعطى لأنّ «٠٫٠٠٠٤» و«٠٫٠٠٠٤٠٠» عددٌ واحدٌ وإعلانان مختلفان،
    والعائمُ يمحو الفرقَ بينهما وهو بيتُ القصيد.
    """

    text: str

    def __post_init__(self) -> None:
        if not _PRINTED.match(self.text):
            raise ReconciliationError(
                f"«{self.text}» ليس رقمًا عشريًّا مطبوعًا؛ ولا يُنظَّف ليصير كذلك."
            )

    @property
    def value(self) -> Fraction:
        """قيمتُه المطبوعةُ كسرًا صحيحًا، لا عائمًا."""

        return Fraction(Decimal(self.text))

    @property
    def places(self) -> int:
        """عددُ المنازل العشريّة المطبوعة."""

        match = _PRINTED.match(self.text)
        assert match is not None
        return len(match.group(2) or "")

    @property
    def significant_digits(self) -> int:
        """عددُ الخانات المعنويّة المطبوعة؛ والأصفارُ اللاحقةُ معنويّةٌ ههنا."""

        match = _PRINTED.match(self.text)
        assert match is not None
        return len((match.group(1) + (match.group(2) or "")).lstrip("0"))

    @property
    def half_width(self) -> Fraction:
        """نصفُ عرض المجال الذي يُطبَع بهذه الصورة."""

        return Fraction(1, 2 * 10**self.places)

    def interval(self) -> tuple[Fraction, Fraction]:
        """`[v−h، v+h)` — نصفُ مفتوحٍ بالاصطلاح المُعلَن."""

        return (self.value - self.half_width, self.value + self.half_width)

    @property
    def relative_half_width(self) -> Fraction:
        """نصفُ العرض منسوبًا إلى القَدْر؛ ويُرفَض عند الصفر."""

        if self.value == 0:
            raise ReconciliationError("الصفرُ المطبوعُ لا نسبةَ لعرضه.")
        return self.half_width / abs(self.value)

    def prints(self, value: Fraction) -> bool:
        """أيُطبَع هذا العددُ بهذه الصورة بعينها؟"""

        low, high = self.interval()
        return low <= value < high


@dataclass(frozen=True, slots=True)
class Difference:
    """فرقُ رقمَين مطبوعَين؛ ومجالُه يجمع عدمَ اليقين لا يُلغيه.

    وهذا شكلُ بسطِ `z` بعينه: مقيسٌ ناقصَ متوسّطِ الصفريّ. وكتابةُ الفرق
    رقمًا مطبوعًا واحدًا تُخفي أنّ عرضَه مجموعُ عرضَين.
    """

    minuend: PrintedFigure
    subtrahend: PrintedFigure

    @property
    def value(self) -> Fraction:
        """الفرقُ الاسميّ بين القيمتين المطبوعتين."""

        return self.minuend.value - self.subtrahend.value

    def interval(self) -> tuple[Fraction, Fraction]:
        """`[أدنى − أقصى، أقصى − أدنى]` — العرضان مجموعان."""

        low, high = self.minuend.interval()
        other_low, other_high = self.subtrahend.interval()
        return (low - other_high, high - other_low)


@dataclass(frozen=True, slots=True)
class Partition:
    """أجزاءٌ ومجموعٌ مُعلَن؛ والبقيّةُ تُعلَن عددًا ولا تُوزَّع."""

    parts: tuple[int, ...]
    declared_total: int

    def __post_init__(self) -> None:
        if not self.parts:
            raise ReconciliationError("تجزئةٌ بلا أجزاءٍ لا مجموعَ لها يُطابَق.")

    @property
    def measured_total(self) -> int:
        """مجموعُ الأجزاء مُشتَقًّا."""

        return sum(self.parts)

    @property
    def residue(self) -> int:
        """المُعلَنُ ناقصَ المقيس؛ موجبًا كان أو سالبًا أو صفرًا."""

        return self.declared_total - self.measured_total

    @property
    def balances(self) -> bool:
        """أتنطبق التجزئةُ على مجموعها المُعلَن بلا بقيّة؟"""

        return self.residue == 0

    def residue_is_hidden_in_share(self, base: int, places: int) -> bool:
        """أتُطبَع حصّةُ المُعلَن وحصّةُ المقيس من `base` بالصورة نفسها؟

        فإن كانت كذلك فالبقيّةُ **مستورةٌ بالتقريب**: قارئُ النسبة وحدَها لا
        يستطيع أن يرى الفرق.
        """

        if base == 0:
            raise ReconciliationError("لا حصّةَ من أساسٍ صفر.")
        return rounds_alike(
            Fraction(self.declared_total, base),
            Fraction(self.measured_total, base),
            places,
        )


@dataclass(frozen=True, slots=True)
class Quotient:
    """حاصلُ قسمةِ رقمَين مطبوعَين؛ وهو مجالٌ لأنّ طرفَيه مجالان."""

    numerator: Reading
    denominator: PrintedFigure

    def __post_init__(self) -> None:
        low, high = self.denominator.interval()
        if low <= 0 <= high:
            raise ReconciliationError(
                "مجالُ المقام يعبر الصفرَ، فحاصلُ القسمة غيرُ محدودٍ أصلًا."
            )

    def nominal(self) -> Fraction:
        """القسمةُ على القيمتين المطبوعتين كما هما — نقطةٌ داخل المجال."""

        return self.numerator.value / self.denominator.value

    def interval(self) -> tuple[Fraction, Fraction]:
        """أصغرُ وأكبرُ حاصلٍ يحتمله المطبوعُ، بأخذ أطراف المجالين الأربعة."""

        numerators = self.numerator.interval()
        denominators = self.denominator.interval()
        corners = [top / bottom for top in numerators for bottom in denominators]
        return (min(corners), max(corners))

    @property
    def determined_significant_digits(self) -> int:
        """كم خانةً معنويّةً يحدّدها المجال، بالاصطلاح المُعلَن في رأس الوحدة."""

        low, high = self.interval()
        width = high - low
        if width == 0:
            raise ReconciliationError("عرضٌ صفرٌ: لا مجالَ ههنا أصلًا.")
        magnitude = max(abs(low), abs(high))
        return math.floor(math.log10(float(magnitude / width)))

    def claim(self, reported: str) -> QuotientClaim:
        """دعوى رقمٍ مُعلَنٍ على هذا الحاصل."""

        return QuotientClaim(quotient=self, reported=PrintedFigure(reported))


@dataclass(frozen=True, slots=True)
class QuotientClaim:
    """رقمٌ أُعلِن حاصلًا، مقروءًا في مجال ما يحتمله مقامُه وبسطُه."""

    quotient: Quotient
    reported: PrintedFigure

    @property
    def lies_in_interval(self) -> bool:
        """أيقع المُعلَنُ في مجال ما يحتمله المطبوع؟ وهذا الفحصُ القاطع."""

        low, high = self.quotient.interval()
        return low <= self.reported.value <= high

    @property
    def digits_announced(self) -> int:
        """كم خانةً معنويّةً أُعلِنت."""

        return self.reported.significant_digits

    @property
    def digits_determined(self) -> int:
        """كم خانةً معنويّةً يحدّدها المطبوع."""

        return self.quotient.determined_significant_digits

    @property
    def is_over_announced(self) -> bool:
        """أأُعلِن الحاصلُ بدقّةٍ أعلى ممّا يحدّده مقامُه؟"""

        return self.digits_announced > self.digits_determined

    def implied_denominator(self) -> Fraction:
        """المقامُ الذي يُخرِج المُعلَنَ بالضبط من البسط المطبوع.

        وهو الطريقُ إلى الحكم: إن كان هذا المقامُ المُستلزَمُ **يُطبَع كما طُبِع
        المقامُ المُعلَن**، فالرقمُ المُعلَنُ صادرٌ عن مقامٍ أدقَّ ممّا نُشِر —
        فالخلافُ في النشر لا في الحساب.
        """

        if self.reported.value == 0:
            raise ReconciliationError("حاصلٌ صفرٌ لا يستلزم مقامًا.")
        return self.numerator_value / self.reported.value

    @property
    def numerator_value(self) -> Fraction:
        """قيمةُ البسط المطبوعة."""

        return self.quotient.numerator.value

    @property
    def implied_denominator_prints_as_declared(self) -> bool:
        """أيُطبَع المقامُ المُستلزَمُ بصورة المقام المُعلَن بعينها؟"""

        return self.quotient.denominator.prints(self.implied_denominator())


A_PRINTED_FIGURE_IS_AN_INTERVAL_NOT_A_POINT_NOTE: Final[str] = (
    "APrintedFigureIsAnIntervalNotAPoint: «٠٫٠٠٠٤» ليست عددًا بل كلَّ عددٍ "
    "يُطبَع هكذا؛ ومَن عاملها نقطةً حسب بدقّةٍ لا يملكها"
)

A_QUOTIENT_MAY_NOT_OUTRUN_ITS_DENOMINATOR_NOTE: Final[str] = (
    "AQuotientMayNotOutrunItsDenominator: مقامٌ بخانةٍ معنويّةٍ واحدةٍ لا يحدّد "
    "حاصلًا بخمسِ خانات؛ ورقمان مختلفان عن قياسٍ واحدٍ قد يتّسقان كلاهما مع "
    "المطبوع، فالخلافُ في الإعلان لا في القياس"
)

A_ROUNDING_CONVENTION_IS_DECLARED_NOT_ASSUMED_NOTE: Final[str] = (
    "ARoundingConventionIsDeclaredNotAssumed: المجالُ نصفُ مفتوحٍ [v−h، v+h) "
    "والمنتصفُ لأعلى؛ اختيارٌ مُعلَنٌ لا مضمَر"
)

A_DIGIT_COUNT_IS_A_CONVENTION_NOT_A_THEOREM_NOTE: Final[str] = (
    "ADigitCountIsAConventionNotATheorem: عدُّ الخانات المحدَّدة اصطلاحٌ "
    "⌊log₁₀(القَدْر/العرض)⌋؛ والفحصُ الحاملُ هو انتماءُ المُعلَن إلى المجال"
)

A_RESIDUE_IS_NAMED_NOT_ABSORBED_NOTE: Final[str] = (
    "AResidueIsNamedNotAbsorbed: بقيّةُ التجزئة تُعلَن عددًا ولا تُوزَّع على "
    "الأجزاء ولا تُسمّى تقريبًا؛ وبقيّةُ الصفر خبرٌ كبقيّة الواحد"
)

RECONCILIATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_PRINTED_FIGURE_IS_AN_INTERVAL_NOT_A_POINT_NOTE,
    A_QUOTIENT_MAY_NOT_OUTRUN_ITS_DENOMINATOR_NOTE,
    A_ROUNDING_CONVENTION_IS_DECLARED_NOT_ASSUMED_NOTE,
    A_DIGIT_COUNT_IS_A_CONVENTION_NOT_A_THEOREM_NOTE,
    A_RESIDUE_IS_NAMED_NOT_ABSORBED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
