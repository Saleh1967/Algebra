"""جبرُ التقويم: مجموعةُ قرارٍ لُمِست بالاختبار ليست مختبَرة، والامتناعُ ليس خطأً.

**ما تفعله هذه الوحدة**: تصف قسمةَ تدريبٍ واختبار، وما بُنِيت عليه مجموعةُ
القرار، وحصيلةَ التقويم — فترفض ثلاثةَ أشياء **في الإنشاء**: قسمةً غيرَ
منفصلة، ومجموعةَ قرارٍ لمست الاختبار ثمّ ادُّعي أنّها خارجه، ورقمًا واحدًا
يجمع الإصابةَ والخطأ والامتناع. وهي لا تعرف موضوعًا: مفاتيحُ وأعداد.

`A_DECISION_SET_BUILT_ON_THE_TEST_IS_NOT_TESTED`: قائمةٌ مغلقةٌ تُستخرَج من
المدوَّنة **كلِّها** ثمّ تُقوَّم على نصفها ليست تقويمًا خارج العيّنة. والتسرّبُ
لا يُقاس بمقداره بل يُمنَع: تُبنى من التدريب وحدَه أو يُسمّى الرقمُ داخليًّا.

`ABSTENTION_IS_NOT_ERROR_AND_NEITHER_IS_IT_SUCCESS`: قاعدةٌ لا تنطبق على
مدخلٍ **امتنعت**، ولم تُخطئ. وجمعُ الامتناع مع الخطأ في «الدقّة» يخلط سعةَ
القاعدة بصوابها، فيُخفي أيَّهما يُصلَح. فالثلاثةُ تُعلَن مفصولةً دائمًا.

`AN_IN_SAMPLE_NUMBER_SAYS_SO_IN_ITS_NAME`: رقمٌ بلا قسمةٍ رقمٌ **داخليّ**،
ويُسمّى كذلك. وسكوتُه عن ذلك يجعل قارئَه يحسبه تعميمًا.

`A_BASELINE_IS_COMPUTED_ON_THE_SET_IT_IS_COMPARED_TO`: خطُّ أساسٍ من التدريب
يُقارَن بدقّةٍ على الاختبار مقارنةٌ بين مجموعتين لا بين طريقتين. والفرقُ
الناتجُ يخلط انزياحَ التوزيع بقدرة النموذج.

`A_SPLIT_IS_DISJOINT_OR_IT_IS_NOT_A_SPLIT`: تقاطعُ التدريب والاختبار يُرَدّ
عددًا لا يُغتفَر صغيرُه؛ ومفتاحٌ في الجهتين يُبطِل الجهتين.

`A_TOKEN_COUNT_IS_NOT_A_SAMPLE_SIZE_WHEN_THE_TYPES_ARE_FEW`: ألفُ وقوعٍ من
أربعة أنواعٍ ليست ألفَ مشاهدةٍ مستقلّة بل **أربعًا**. فالوقوعاتُ المتشاركةُ
نوعًا تتشارك صورتَه كلَّها، فيتضخّم الخطأُ المعياريُّ بجذر (وقوعات ÷ أنواع).
والعددُ الكبيرُ ههنا **يطمئن ولا يخبر**.

`A_MEASURE_NEEDS_ITS_CONTEXT_AND_THE_SHORT_UNITS_CARRY_NONE`: مقياسٌ يحتاج
سياقًا برتبة `r` لا يقيس شيئًا على وحدةٍ طولُها `r` فأقلّ. فمتوسّطٌ على وحداتٍ
مختلفةِ الأطوال **خليطٌ لا متوسّط**؛ ونصيبُ الرموز ذاتِ السياق التامّ يُحسَب
ويُعلَن، وإلّا كان الطولُ متغيّرًا خفيًّا يُقارِن مجموعتين بمقياسين.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from typing import Final

__all__ = [
    "ABSTENTION_IS_NOT_ERROR_AND_NEITHER_IS_IT_SUCCESS_NOTE",
    "AN_IN_SAMPLE_NUMBER_SAYS_SO_IN_ITS_NAME_NOTE",
    "A_BASELINE_IS_COMPUTED_ON_THE_SET_IT_IS_COMPARED_TO_NOTE",
    "A_DECISION_SET_BUILT_ON_THE_TEST_IS_NOT_TESTED_NOTE",
    "A_MEASURE_NEEDS_ITS_CONTEXT_AND_THE_SHORT_UNITS_CARRY_NONE_NOTE",
    "A_SPLIT_IS_DISJOINT_OR_IT_IS_NOT_A_SPLIT_NOTE",
    "A_TOKEN_COUNT_IS_NOT_A_SAMPLE_SIZE_WHEN_THE_TYPES_ARE_FEW_NOTE",
    "ClusteredSample",
    "DecisionSet",
    "EVALUATION_NAMED_RESIDUALS",
    "EvaluationError",
    "Split",
    "Tally",
    "full_context_share",
    "units_that_carry_no_context",
]


class EvaluationError(ValueError):
    """رُفض قسمةٌ أو مجموعةُ قرارٍ أو حصيلةٌ لا تقبل القراءة؛ ولا تُقرَّب."""


@dataclass(frozen=True, slots=True)
class ClusteredSample:
    """عيّنةٌ عناقيدُها مُعلَنة: وقوعاتٌ، وأنواعٌ هي وحدةُ الاستقلال.

    فالوقوعُ ليس مشاهدةً مستقلّةً متى تشارك ونظيرُه نوعًا واحدًا: صورتُه
    نفسُها، فما يُقاس عليه يُقاس على النوع مرّةً مكرَّرة. والعددُ الكبيرُ
    **يطمئن ولا يخبر**.
    """

    observations: int
    clusters: int

    def __post_init__(self) -> None:
        if self.clusters < 1:
            raise EvaluationError("عنقودٌ واحدٌ فأكثر؛ وصفرُ عناقيدَ ليس عيّنة.")
        if self.observations < self.clusters:
            raise EvaluationError(
                f"{self.observations} وقوعًا في {self.clusters} عنقودًا: "
                "وقوعاتٌ أقلُّ من عناقيدها ليست عنقدة."
            )

    @property
    def per_cluster(self) -> Fraction:
        """متوسّطُ الوقوعات لكلّ عنقود."""

        return Fraction(self.observations, self.clusters)

    @property
    def effective(self) -> int:
        """المشاهداتُ المستقلّة: العناقيدُ لا الوقوعات."""

        return self.clusters

    @property
    def inflation(self) -> float:
        """كم يتّسع الخطأُ المعياريُّ إن حُسِب على العناقيد: جذرُ الوقوعِ للعنقود."""

        return math.sqrt(float(self.per_cluster))


def units_that_carry_no_context(lengths: Iterable[int], order: int) -> int:
    """عددُ الوحدات التي لا يحمل أيُّ رمزٍ فيها سياقًا تامًّا بهذه الرتبة."""

    if order < 1:
        raise EvaluationError("رتبةٌ دون الواحد ليست سياقًا.")
    return sum(1 for length in lengths if length <= order)


def full_context_share(lengths: Iterable[int], order: int) -> Fraction:
    """نصيبُ الرموز التي تحمل سياقًا تامًّا برتبة `order` من مجموع الرموز.

    فوحدةٌ طولُها `L` تُخرِج `max(0, L − order)` رمزًا ذا سياقٍ تامّ. ونصيبٌ
    دون الواحد يعني أنّ المتوسّطَ المُعلَن خليطُ مقياسين: مقيسٌ على ما حمل
    السياق، ومُرتَدٌّ إلى رتبةٍ أدنى على ما لم يحمله.
    """

    if order < 1:
        raise EvaluationError("رتبةٌ دون الواحد ليست سياقًا.")
    sizes = [length for length in lengths]
    if not sizes or any(length < 1 for length in sizes):
        raise EvaluationError("أطوالٌ خاليةٌ أو غيرُ موجبةٍ لا تُقاس.")
    total = sum(sizes)
    carried = sum(max(0, length - order) for length in sizes)
    return Fraction(carried, total)


@dataclass(frozen=True, slots=True)
class Split:
    """قسمةُ تدريبٍ واختبار، منفصلتين شرطَ إنشاء."""

    train: frozenset[str]
    test: frozenset[str]

    def __post_init__(self) -> None:
        if not self.train or not self.test:
            raise EvaluationError("قسمةٌ بجهةٍ خاليةٍ ليست قسمة.")
        overlap = self.train & self.test
        if overlap:
            shown = "، ".join(sorted(overlap)[:4])
            raise EvaluationError(
                f"تقاطعٌ بين الجهتين ({len(overlap)}): {shown}… "
                "(A_SPLIT_IS_DISJOINT_OR_IT_IS_NOT_A_SPLIT)."
            )

    @property
    def everything(self) -> frozenset[str]:
        """المدوَّنةُ كلُّها كما تراها هذه القسمة."""

        return self.train | self.test

    @property
    def test_share(self) -> Fraction:
        """نصيبُ الاختبار من المجموع — يُعلَن مع كلّ مقامٍ مشتقٍّ منه."""

        return Fraction(len(self.test), len(self.everything))


@dataclass(frozen=True, slots=True)
class DecisionSet:
    """مجموعةُ قرارٍ ومفاتيحُ ما بُنِيت عليه — والتسرّبُ يُرَدّ لا يُقاس."""

    name: str
    members: frozenset[str]
    built_from: frozenset[str]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise EvaluationError("مجموعةُ قرارٍ بلا اسمٍ لا تُحاسَب.")
        if not self.built_from:
            raise EvaluationError(
                "مجموعةٌ لا تقول ما بُنِيت عليه لا يُعرَف أخارجَ العيّنة هي أم داخلها."
            )

    def leaked_keys(self, split: Split) -> frozenset[str]:
        """مفاتيحُ الاختبار التي دخلت في بنائها."""

        return self.built_from & split.test

    def is_leaky(self, split: Split) -> bool:
        """أبُنِيت بشيءٍ من الاختبار؟"""

        return bool(self.leaked_keys(split))

    def assert_out_of_sample(self, split: Split) -> None:
        """ردُّ ادّعاءِ «خارجَ العيّنة» لمجموعةٍ لمست الاختبار."""

        leaked = self.leaked_keys(split)
        if leaked:
            raise EvaluationError(
                f"«{self.name}» بُنِيت على {len(leaked)} مفتاحًا من الاختبار، "
                "فتقويمُها عليه داخليٌّ لا خارجيّ "
                "(A_DECISION_SET_BUILT_ON_THE_TEST_IS_NOT_TESTED)."
            )


@dataclass(frozen=True, slots=True)
class Tally:
    """حصيلةٌ ثلاثيّة: أصابت، وأخطأت، وامتنعت — ولا تُجمَع في رقمٍ واحد."""

    correct: int
    wrong: int
    abstained: int

    def __post_init__(self) -> None:
        for value in (self.correct, self.wrong, self.abstained):
            if value < 0:
                raise EvaluationError("عددٌ سالبٌ ليس حصيلة.")
        if self.total == 0:
            raise EvaluationError("حصيلةٌ خاليةٌ لا تُقرَأ.")

    @property
    def total(self) -> int:
        """مجموعُ المقوَّم عليه."""

        return self.correct + self.wrong + self.abstained

    @property
    def fired(self) -> int:
        """ما انطبقت عليه القاعدةُ فعلًا."""

        return self.correct + self.wrong

    @property
    def coverage(self) -> Fraction:
        """سعةُ القاعدة: نصيبُ ما انطبقت عليه."""

        return Fraction(self.fired, self.total)

    @property
    def precision_where_it_fires(self) -> Fraction:
        """صوابُها حيث انطبقت؛ ويُرَدّ إن لم تنطبق قطّ."""

        if self.fired == 0:
            raise EvaluationError("لم تنطبق القاعدةُ قطّ، فلا صوابَ لها يُقاس.")
        return Fraction(self.correct, self.fired)

    @property
    def accuracy_charging_abstention(self) -> Fraction:
        """الدقّةُ إن حُسِب الامتناعُ خطأً — وهو اختيارٌ يُسمّى لا يُفترَض."""

        return Fraction(self.correct, self.total)

    @property
    def abstention_inflates_the_error_by(self) -> Fraction:
        """كم يهبط الرقمُ بسبب الامتناع وحدَه: الفرقُ بين القراءتين."""

        if self.fired == 0:
            return Fraction(0)
        return self.precision_where_it_fires - self.accuracy_charging_abstention


def majority_baseline(labels: Iterable[str]) -> Fraction:
    """خطُّ الأساس على **المجموعة التي يُقارَن بها**، لا على غيرها."""

    counts: dict[str, int] = {}
    total = 0
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
        total += 1
    if total == 0:
        raise EvaluationError("لا خطَّ أساسٍ على مجموعةٍ خالية.")
    return Fraction(max(counts.values()), total)


A_DECISION_SET_BUILT_ON_THE_TEST_IS_NOT_TESTED_NOTE: Final[str] = (
    "ADecisionSetBuiltOnTheTestIsNotTested: قائمةٌ مغلقةٌ تُستخرَج من المدوَّنة "
    "كلِّها ثمّ تُقوَّم على نصفها ليست خارج العيّنة؛ والتسرّبُ يُمنَع لا يُقاس"
)

ABSTENTION_IS_NOT_ERROR_AND_NEITHER_IS_IT_SUCCESS_NOTE: Final[str] = (
    "AbstentionIsNotErrorAndNeitherIsItSuccess: قاعدةٌ لا تنطبق امتنعت ولم "
    "تُخطئ؛ وجمعُهما في «الدقّة» يخلط سعةَ القاعدة بصوابها فيُخفي أيَّهما يُصلَح"
)

AN_IN_SAMPLE_NUMBER_SAYS_SO_IN_ITS_NAME_NOTE: Final[str] = (
    "AnInSampleNumberSaysSoInItsName: رقمٌ بلا قسمةٍ رقمٌ داخليٌّ ويُسمّى كذلك، "
    "وسكوتُه عن ذلك يجعل قارئَه يحسبه تعميمًا"
)

A_BASELINE_IS_COMPUTED_ON_THE_SET_IT_IS_COMPARED_TO_NOTE: Final[str] = (
    "ABaselineIsComputedOnTheSetItIsComparedTo: خطُّ أساسٍ من التدريب يُقارَن "
    "بدقّةٍ على الاختبار مقارنةٌ بين مجموعتين لا بين طريقتين"
)

A_SPLIT_IS_DISJOINT_OR_IT_IS_NOT_A_SPLIT_NOTE: Final[str] = (
    "ASplitIsDisjointOrItIsNotASplit: تقاطعُ الجهتين يُرَدّ عددًا لا يُغتفَر "
    "صغيرُه؛ ومفتاحٌ في الجهتين يُبطِل الجهتين"
)

A_TOKEN_COUNT_IS_NOT_A_SAMPLE_SIZE_WHEN_THE_TYPES_ARE_FEW_NOTE: Final[str] = (
    "ATokenCountIsNotASampleSizeWhenTheTypesAreFew: ألفُ وقوعٍ من أربعة أنواعٍ "
    "أربعُ مشاهداتٍ لا ألف؛ والخطأُ المعياريُّ يتّسع بجذر الوقوعِ للعنقود، "
    "والعددُ الكبيرُ يطمئن ولا يخبر"
)

A_MEASURE_NEEDS_ITS_CONTEXT_AND_THE_SHORT_UNITS_CARRY_NONE_NOTE: Final[str] = (
    "AMeasureNeedsItsContextAndTheShortUnitsCarryNone: مقياسٌ برتبة `r` لا "
    "يقيس شيئًا على وحدةٍ طولُها `r` فأقلّ؛ فمتوسّطٌ على أطوالٍ مختلفةٍ خليطُ "
    "مقياسين، والطولُ متغيّرٌ خفيٌّ يُقارِن مجموعتين بمقياسين"
)

EVALUATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_TOKEN_COUNT_IS_NOT_A_SAMPLE_SIZE_WHEN_THE_TYPES_ARE_FEW_NOTE,
    A_MEASURE_NEEDS_ITS_CONTEXT_AND_THE_SHORT_UNITS_CARRY_NONE_NOTE,
    A_DECISION_SET_BUILT_ON_THE_TEST_IS_NOT_TESTED_NOTE,
    ABSTENTION_IS_NOT_ERROR_AND_NEITHER_IS_IT_SUCCESS_NOTE,
    AN_IN_SAMPLE_NUMBER_SAYS_SO_IN_ITS_NAME_NOTE,
    A_BASELINE_IS_COMPUTED_ON_THE_SET_IT_IS_COMPARED_TO_NOTE,
    A_SPLIT_IS_DISJOINT_OR_IT_IS_NOT_A_SPLIT_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
