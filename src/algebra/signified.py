"""المدلولُ يُقاس بأوراكل، والأوراكلُ يُفحَص قبل أن يُصدَّق.

**ما تفعله هذه الوحدة**: تحسب على إسنادٍ من **صورةٍ** إلى **مدلول** — كلاهما
معطًى من خارج — ثلاثةَ أشياء: الإنتروبيا والمعلومةَ المتبادلةَ بكسورٍ صحيحةٍ
في الاحتمالات، وصفريًّا تبديليًّا مُعلَنَ البذرة، و**نصيبَ التلوّث**: كم من
أزواج (صورة، مدلول) مدلولُها مقروءٌ من صورتها. وهي لا تعرف لغةً ولا معجمًا.

`A_MEANING_READ_OFF_THE_FORM_IS_NOT_EVIDENCE_FOR_THE_FORM`: إن كان المعجميُّ
يشرح الجذرَ بمشتقٍّ منه، فالمدلولُ **صورةٌ متنكّرة**، وكلُّ ارتباطٍ يُقاس بينهما
مضمونٌ بالإنشاء لا مكتشَف. فيُقاس نصيبُ ذلك ويُعلَن قبل أيّ حكم؛ ولا يُقال
«ضئيلٌ فيُهمَل» بل يُقال مقداره.

`AN_ORACLE_IS_DECLARED_AND_THE_CLAIM_IS_BOUND_TO_IT`: لا مدلولَ يُستخرَج من
الركيزة. فكلُّ رقمٍ ههنا مقيَّدٌ باسم الأوراكل وتاريخه وطريقةِ استخراجه،
ويسقط بسقوطه. والأوراكلُ حجّةٌ على قائله لا على اللغة.

`ARBITRARINESS_IS_THE_NULL_NOT_THE_FINDING`: اعتباطيّةُ العلامة هي **الصفريُّ**
لا النتيجة. فمن قاس ارتباطًا وجب أن يعرضه على تبديلٍ يحفظ الهامشين؛ ومن عرض
رقمًا خامًّا بلا صفريٍّ لم يقل شيئًا.

`A_SPARSE_MUTUAL_INFORMATION_IS_BIASED_UPWARD`: المعلومةُ المتبادلةُ على فئاتٍ
كثيرةٍ قليلةِ الشواهد **موجبةٌ حتى على بياناتٍ مستقلّةٍ تمامًا**. فالخامُ لا
يُقرَأ وحدَه البتّة: يُطرَح منه متوسّطُ الصفريّ، ويُعلَن انحرافُه.

`A_FIELD_THAT_CONTRADICTS_ITS_OWN_COUNT_VOIDS_WHAT_RESTS_ON_IT`: حقلٌ يُعلِن
عددًا ثمّ يسرد غيرَه لا يُصلَح بالأكثر ولا بالأقلّ؛ يُقاس تناقضُه أوّلًا، فإن
تجاوز حدًّا مُعلَنًا سقط كلُّ ما بُني عليه.
"""

from __future__ import annotations

import hashlib
import math
import random
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

__all__ = [
    "AN_ORACLE_IS_DECLARED_AND_THE_CLAIM_IS_BOUND_TO_IT_NOTE",
    "ARBITRARINESS_IS_THE_NULL_NOT_THE_FINDING_NOTE",
    "A_FIELD_THAT_CONTRADICTS_ITS_OWN_COUNT_VOIDS_WHAT_RESTS_ON_IT_NOTE",
    "A_MEANING_READ_OFF_THE_FORM_IS_NOT_EVIDENCE_FOR_THE_FORM_NOTE",
    "A_SPARSE_MUTUAL_INFORMATION_IS_BIASED_UPWARD_NOTE",
    "BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE",
    "CONDITIONING_SIDES",
    "Direction",
    "NullReading",
    "Oracle",
    "Prediction",
    "SIGNIFIED_NAMED_RESIDUALS",
    "SignifiedError",
    "Verdict",
    "conditional_entropy",
    "contamination_share",
    "entropy",
    "mutual_information",
    "permutation_null",
    "seal",
]

Pair = tuple[str, str]


class SignifiedError(ValueError):
    """رُفض إسنادٌ أو شرطٌ لا يقبل الحساب؛ ولا يُحمَل على أقرب مقبول."""


class Direction(Enum):
    """اتّجاهُ الشرط، مغلقًا اثنين: ولا اتّجاهَ اسمُه «قريبٌ بما يكفي»."""

    AT_LEAST = "يتحقّق إن بلغ المقيسُ الحدَّ أو جاوزه"
    AT_MOST = "يتحقّق إن لم يجاوز المقيسُ الحدَّ"


class Verdict(Enum):
    """أحكامُ الشرط، مغلقةً ثلاثًا: ولا حكمَ اسمُه «مُبشِّر»."""

    MET = "تحقّق الشرطُ المُسجَّلُ قبل النظر"
    FALSIFIED = "لم يتحقّق، والقولُ المعلَّقُ عليه ساقط"
    VOID = "سقط الشرطُ لأنّ ما يقوم عليه انتقض قبله"


def entropy(counts: Iterable[int]) -> float:
    """إنتروبيا توزيعٍ بالبتّات؛ والاحتمالاتُ كسورٌ صحيحةٌ لا عائمات."""

    tallies = [count for count in counts if count]
    if any(count < 0 for count in tallies):
        raise SignifiedError("عددٌ سالبٌ ليس تكرارًا.")
    total = sum(tallies)
    if total == 0:
        raise SignifiedError("توزيعٌ خالٍ لا إنتروبيا له.")
    return -sum(
        float(Fraction(count, total)) * math.log2(float(Fraction(count, total)))
        for count in tallies
    )


CONDITIONING_SIDES: Final[tuple[str, ...]] = ("صورة", "مدلول")
"""جانبا الشرط؛ والجانبُ يُسمّى لأنّ الاتّجاهين رقمان لا رقم."""


def conditional_entropy(pairs: Sequence[Pair], *, given: str) -> float:
    """`H(الآخر | given)` بالبتّات؛ والجانبُ **يُسمّى** ولا يُستنتَج.

    فالاتّجاهان مقداران مختلفان لا صيغتان لمقدارٍ واحد: `H(مدلول | صورة)`
    اشتراكٌ، و`H(صورة | مدلول)` ترادف. ودالّةٌ تختار أحدَهما ضمنًا تُسلِّم
    الاتّجاهَ إلى ترتيب الحقول.
    """

    if given not in CONDITIONING_SIDES:
        raise SignifiedError(
            f"جانبُ الشرط يُسمّى من {CONDITIONING_SIDES}؛ و«{given}» ليس منها."
        )
    if not pairs:
        raise SignifiedError("لا إنتروبيا شرطيّةَ على إسنادٍ خالٍ.")
    index = CONDITIONING_SIDES.index(given)
    grouped: dict[str, Counter[str]] = {}
    for pair in pairs:
        grouped.setdefault(pair[index], Counter())[pair[1 - index]] += 1
    total = len(pairs)
    return sum(
        float(Fraction(sum(inner.values()), total)) * entropy(inner.values())
        for inner in grouped.values()
    )


def mutual_information(pairs: Sequence[Pair]) -> float:
    """`I(صورة ؛ مدلول) = H(ص) + H(م) − H(ص، م)` بالبتّات، خامًّا لا مصحَّحًا.

    و**الخامُ لا يُقرَأ وحدَه**: انظر `permutation_null`.
    """

    if not pairs:
        raise SignifiedError("لا معلومةَ متبادلةَ على إسنادٍ خالٍ.")
    forms = Counter(form for form, _ in pairs)
    senses = Counter(sense for _, sense in pairs)
    joint = Counter(pairs)
    return entropy(forms.values()) + entropy(senses.values()) - entropy(joint.values())


@dataclass(frozen=True, slots=True)
class NullReading:
    """قراءةُ الصفريّ التبديليّ: متوسّطُه وانحرافُه والمقيسُ فوقه."""

    observed: float
    null_mean: float
    null_deviation: float
    replicates: int
    seed: int

    def __post_init__(self) -> None:
        if self.replicates < 2:
            raise SignifiedError("الصفريُّ تبديلان فأكثر.")
        if self.null_deviation < 0:
            raise SignifiedError("انحرافٌ سالبٌ ليس انحرافًا.")

    @property
    def excess(self) -> float:
        """المقيسُ ناقصَ متوسّطِ الصفريّ — وهذا ما يُقرَأ، لا الخام."""

        return self.observed - self.null_mean

    @property
    def deviations(self) -> float:
        """كم انحرافًا فوق الصفريّ؛ ويُرَدّ عند انحرافٍ صفر."""

        if self.null_deviation == 0:
            raise SignifiedError("انحرافُ الصفريِّ صفرٌ، فلا تُقسَم عليه؛ ويُعلَن الفائضُ وحدَه.")
        return self.excess / self.null_deviation


def permutation_null(pairs: Sequence[Pair], replicates: int, seed: int) -> NullReading:
    """اعرض المقيسَ على تبديلٍ **يحفظ الهامشين**، ببذرةٍ مُعلَنة.

    ويُخلَط المدلولُ وحدَه، فيبقى توزيعُ الصور وتوزيعُ المدلولات كما هما ولا
    يبقى إلّا الاقتران. والبذرةُ معطًى لا سرّ، فالرقمُ يُعاد حرفًا.
    """

    if replicates < 2:
        raise SignifiedError("الصفريُّ تبديلان فأكثر.")
    observed = mutual_information(pairs)
    forms = [form for form, _ in pairs]
    senses = [sense for _, sense in pairs]
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(replicates):
        shuffled = senses[:]
        rng.shuffle(shuffled)
        draws.append(mutual_information(list(zip(forms, shuffled, strict=True))))
    mean = sum(draws) / len(draws)
    variance = sum((draw - mean) ** 2 for draw in draws) / (len(draws) - 1)
    return NullReading(
        observed=observed,
        null_mean=mean,
        null_deviation=math.sqrt(variance),
        replicates=replicates,
        seed=seed,
    )


def contamination_share(
    pairs: Sequence[Pair], reads_off_the_form: Callable[[str, str], bool]
) -> Fraction:
    """نصيبُ الأزواج التي مدلولُها مقروءٌ من صورتها — كسرًا صحيحًا لا نسبة."""

    if not pairs:
        raise SignifiedError("لا نصيبَ من إسنادٍ خالٍ.")
    tainted = sum(1 for form, sense in pairs if reads_off_the_form(form, sense))
    return Fraction(tainted, len(pairs))


@dataclass(frozen=True, slots=True)
class Oracle:
    """أوراكلُ مُعلَن: اسمُه ومصدرُه وطريقةُ استخراجه؛ والقولُ مقيَّدٌ به."""

    name: str
    source: str
    extraction: str

    def __post_init__(self) -> None:
        for field_name in ("name", "source", "extraction"):
            if not getattr(self, field_name).strip():
                raise SignifiedError(
                    "أوراكلُ بلا اسمٍ أو مصدرٍ أو طريقةِ استخراجٍ لا يُقيَّد به قول."
                )


@dataclass(frozen=True, slots=True)
class Prediction:
    """شرطٌ مُسجَّلٌ **قبل النظر**: مقياسُه وحدُّه واتّجاهُه وما يسقط بسقوطه."""

    identifier: str
    statistic: str
    threshold: Fraction
    direction: Direction
    falsifies: str

    def __post_init__(self) -> None:
        if not self.identifier.strip() or not self.statistic.strip():
            raise SignifiedError("شرطٌ بلا اسمٍ أو مقياسٍ ليس شرطًا.")
        if not self.falsifies.strip():
            raise SignifiedError(
                "شرطٌ لا يُسمّي ما يسقط بسقوطه غيرُ قابلٍ للنقض، فليس شرطًا."
            )

    def verdict(self, measured: Fraction, void: bool = False) -> Verdict:
        """احكم على المقيس بالحدّ المُسجَّل؛ و`void` لِما سقط أساسُه قبله."""

        if void:
            return Verdict.VOID
        met = (
            measured >= self.threshold
            if self.direction is Direction.AT_LEAST
            else measured <= self.threshold
        )
        return Verdict.MET if met else Verdict.FALSIFIED

    @property
    def line(self) -> str:
        """سطرُ الشرط كما يُختَم: لا يُعاد ترتيبُه ولا تُغيَّر صياغتُه."""

        sign = "≥" if self.direction is Direction.AT_LEAST else "≤"
        return (
            f"{self.identifier}|{self.statistic}|{sign}|"
            f"{self.threshold}|{self.falsifies}"
        )


def seal(oracle: Oracle, predictions: Sequence[Prediction]) -> str:
    """بصمةُ التسجيل: شرطٌ يُبدَّل بعد النظر يُعرَف بتغيُّرها."""

    if not predictions:
        raise SignifiedError("تسجيلٌ بلا شروطٍ لا يُختَم.")
    identifiers = [prediction.identifier for prediction in predictions]
    if len(set(identifiers)) != len(identifiers):
        raise SignifiedError("شروطُ التسجيل تُسمّى أسماءً مميَّزة.")
    body = "\n".join(
        [f"{oracle.name}|{oracle.source}|{oracle.extraction}"]
        + [prediction.line for prediction in predictions]
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


A_MEANING_READ_OFF_THE_FORM_IS_NOT_EVIDENCE_FOR_THE_FORM_NOTE: Final[str] = (
    "AMeaningReadOffTheFormIsNotEvidenceForTheForm: معجميٌّ يشرح الجذرَ بمشتقٍّ "
    "منه يجعل المدلولَ صورةً متنكّرة، فالارتباطُ مضمونٌ بالإنشاء لا مكتشَف؛ "
    "ويُقاس نصيبُ ذلك ويُعلَن قبل أيّ حكم"
)

AN_ORACLE_IS_DECLARED_AND_THE_CLAIM_IS_BOUND_TO_IT_NOTE: Final[str] = (
    "AnOracleIsDeclaredAndTheClaimIsBoundToIt: لا مدلولَ يُستخرَج من الركيزة، "
    "فكلُّ رقمٍ مقيَّدٌ باسم الأوراكل ومصدره وطريقة استخراجه ويسقط بسقوطه"
)

ARBITRARINESS_IS_THE_NULL_NOT_THE_FINDING_NOTE: Final[str] = (
    "ArbitrarinessIsTheNullNotTheFinding: اعتباطيّةُ العلامة صفريٌّ لا نتيجة؛ "
    "وكلُّ ارتباطٍ يُعرَض على تبديلٍ يحفظ الهامشين وإلّا لم يقل شيئًا"
)

A_SPARSE_MUTUAL_INFORMATION_IS_BIASED_UPWARD_NOTE: Final[str] = (
    "ASparseMutualInformationIsBiasedUpward: المعلومةُ المتبادلةُ على فئاتٍ "
    "كثيرةٍ موجبةٌ حتى على بياناتٍ مستقلّةٍ تمامًا، فالخامُ لا يُقرَأ وحدَه "
    "البتّة بل يُطرَح منه متوسّطُ الصفريّ ويُعلَن انحرافُه"
)

A_FIELD_THAT_CONTRADICTS_ITS_OWN_COUNT_VOIDS_WHAT_RESTS_ON_IT_NOTE: Final[str] = (
    "AFieldThatContradictsItsOwnCountVoidsWhatRestsOnIt: حقلٌ يُعلِن عددًا ثمّ "
    "يسرد غيرَه يُقاس تناقضُه أوّلًا، فإن جاوز حدًّا مُعلَنًا سقط ما بُني عليه"
)

BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE: Final[str] = (
    "BothMarginsDoNotFixAConditionalEntropy: صفريٌّ يحفظ هامشَي الجدول لا "
    "يُثبِّت `H(الآخر | given)`؛ فجدولان بهامشين متطابقين يختلفان فيها. "
    "والذي يُثبِّتها حفظُ **ملمحِ كلّ صفٍّ** — أي إعادةُ تسميةِ الأعمدة وحدَها، "
    "وذلك هُويّةٌ لا صفريّ"
)

SIGNIFIED_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE,
    A_MEANING_READ_OFF_THE_FORM_IS_NOT_EVIDENCE_FOR_THE_FORM_NOTE,
    AN_ORACLE_IS_DECLARED_AND_THE_CLAIM_IS_BOUND_TO_IT_NOTE,
    ARBITRARINESS_IS_THE_NULL_NOT_THE_FINDING_NOTE,
    A_SPARSE_MUTUAL_INFORMATION_IS_BIASED_UPWARD_NOTE,
    A_FIELD_THAT_CONTRADICTS_ITS_OWN_COUNT_VOIDS_WHAT_RESTS_ON_IT_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
