"""لعبةُ الصقر والحمامة (Maynard Smith & Price, 1973): توازنٌ مُشتَقٌّ لا مكتوب.

**ما هذه الوحدة**: بناءٌ رياضيٌّ قائمٌ بذاته للعبة الصقر والحمامة ودينامِكا
المُماثلة عليها. كلُّ عددٍ فيها يخرج من `V` و`C` بالحساب، ولا رقمَ مكتوبٌ بيد.

`THIS_MODEL_CLAIMS_NOTHING_ABOUT_ARABIC`: هذه اللعبةُ لا تُقرأ نموذجًا لتجنُّب
الحروف في الجذور ولا لـ OCP ولا لشيءٍ في مشروع SLGAE. والتشابهُ الظاهريُّ —
«توزيعٌ مستقرٌّ بين سلوكين» — ليس شاهدًا: ما يجعلها نموذجًا لظاهرةٍ لغويّةٍ هو
**تعريفُ عائدٍ مقيس** لكلّ استراتيجيّة، ولا عائدَ مُعرَّفًا في تجنُّب الجذور.
وما يلزم لإجراء ذلك الاختبار مكتوبٌ في `WHAT_A_LINGUISTIC_READING_WOULD_NEED`،
ولم يُجرَ منه شيء.

`THE_EQUILIBRIUM_IS_DERIVED_NOT_ASSERTED`: نسبةُ الصقور عند التوازن تُشتَقّ من
شرط اللامبالاة — تساوي عائدَي الاستراتيجيّتين — بكسورٍ صحيحةٍ لا بعائم. ومن
كتب `V/C` رقمًا ثمّ عرضه نتيجةً وصف ما افترض.

`AN_ESS_IS_NOT_AN_OPTIMUM`: التوازنُ المستقرُّ تطوريًّا **أدنى** في متوسّط
العائد من مجتمع الحمائم الخالص — **في المجالين كليهما** لا في مجالٍ دون آخر،
إذ أعلى متوسّطٍ ممكنٍ هو `V/2` ولا يبلغه إلّا مجتمعٌ بلا صقرٍ واحد، والتوازنُ
لا يخلو من الصقور ما دامت القيمةُ موجبة. وهذا مُشتَقٌّ بالطرح لا مذكورٌ نثرًا:
`optimality_gap` يُخرِجه، وهو موجبٌ دائمًا. فالاستقرارُ ليس صلاحًا، و«البقاءُ
للأفضل» ليس بقاءً للأنفع للجماعة.

`A_PURE_HAWK_POPULATION_IS_STABLE_ONLY_WHEN_FIGHTING_IS_CHEAP`: إذا كانت
الكلفةُ دون القيمة فالصقرُ الخالصُ هو المستقرّ، ولا خليطَ. والحالتان تخرجان من
المقارنة نفسها، فلا تُكتَب إحداهما حالةً خاصّةً تُستثنى.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

__all__ = [
    "AN_ESS_IS_NOT_AN_OPTIMUM_NOTE",
    "A_PURE_HAWK_POPULATION_IS_STABLE_ONLY_WHEN_FIGHTING_IS_CHEAP_NOTE",
    "THE_EQUILIBRIUM_IS_DERIVED_NOT_ASSERTED_NOTE",
    "THIS_MODEL_CLAIMS_NOTHING_ABOUT_ARABIC_NOTE",
    "WHAT_A_LINGUISTIC_READING_WOULD_NEED",
    "EquilibriumKind",
    "HawkDoveError",
    "HawkDoveGame",
    "Strategy",
    "Equilibrium",
]


class HawkDoveError(ValueError):
    """رُفض مدخلٌ خارج شرطه؛ ولا يُحمَل على أقرب قيمةٍ مقبولة."""


class Strategy(Enum):
    """الاستراتيجيّتان النقيّتان، ولا ثالثَ لهما في هذا النموذج."""

    HAWK = "صقر: يتصعّد حتّى الإصابة أو انسحاب الخصم"
    DOVE = "حمامة: يستعرض ثمّ ينسحب إن تُصُعِّد عليه"


class EquilibriumKind(Enum):
    """جنسُ التوازن، مُشتَقًّا من مقارنة الكلفة بالقيمة لا مكتوبًا."""

    MIXED = "خليطٌ مستقرّ: نسبةُ الصقور بين الصفر والواحد"
    PURE_HAWK = "صقرٌ خالص: الكلفةُ لا تزيد على القيمة"


@dataclass(frozen=True, slots=True)
class Equilibrium:
    """توازنُ اللعبة: نسبتُه وجنسُه ومتوسّطُ عائده، وفرقُه عن الأمثل."""

    hawk_share: Fraction
    kind: EquilibriumKind
    mean_payoff: Fraction
    all_dove_payoff: Fraction
    optimality_gap: Fraction

    def __post_init__(self) -> None:
        if not 0 <= self.hawk_share <= 1:
            raise HawkDoveError("نسبةُ الصقور بين الصفر والواحد.")
        if self.optimality_gap != self.all_dove_payoff - self.mean_payoff:
            raise HawkDoveError(
                "فرقُ الأمثليّة لا يطابق الطرح؛ وفرقٌ يُكتَب ولا يُطرَح دعوى لا حساب."
            )


@dataclass(frozen=True, slots=True)
class HawkDoveGame:
    """اللعبةُ بقيمتها وكلفتها؛ وكلُّ ما بعدهما مُشتَقٌّ منهما.

    `value` قيمةُ المورد المتنازَع عليه، و`cost` كلفةُ الصراع بين صقرين.
    وكلاهما موجبٌ شرطَ إنشاء: قيمةٌ صفرٌ تُلغي التنازع، وكلفةٌ صفرٌ تجعل
    الصراعَ مجّانيًّا فيسقط ما بُنيت عليه اللعبة.
    """

    value: Fraction
    cost: Fraction

    def __post_init__(self) -> None:
        for field_name, label in (("value", "قيمةُ المورد"), ("cost", "كلفةُ الصراع")):
            amount = getattr(self, field_name)
            if not isinstance(amount, Fraction):
                raise HawkDoveError(f"{label} كسرٌ صحيحٌ لا عائم، كيلا يُقرَّب التوازن.")
            if amount <= 0:
                raise HawkDoveError(f"{label} موجبٌ شرطَ إنشاء.")

    def payoff(self, own: Strategy, other: Strategy) -> Fraction:
        """عائدُ استراتيجيّةٍ أمام أخرى، بالمصفوفة الكلاسيكيّة.

        صقرٌ أمام صقر يقتسمان القيمةَ والكلفة، وصقرٌ أمام حمامةٍ يأخذ القيمةَ
        كاملةً، وحمامةٌ أمام صقرٍ تنسحب بلا شيء، وحمامتان تقتسمان القيمة.
        """

        if own is Strategy.HAWK:
            if other is Strategy.HAWK:
                return (self.value - self.cost) / 2
            return self.value
        if other is Strategy.HAWK:
            return Fraction(0)
        return self.value / 2

    def expected_payoff(self, own: Strategy, hawk_share: Fraction) -> Fraction:
        """عائدُ استراتيجيّةٍ متوقَّعًا في مجتمعٍ نسبةُ صقوره معلومة."""

        if not 0 <= hawk_share <= 1:
            raise HawkDoveError("نسبةُ الصقور بين الصفر والواحد.")
        return hawk_share * self.payoff(own, Strategy.HAWK) + (
            1 - hawk_share
        ) * self.payoff(own, Strategy.DOVE)

    def mean_payoff(self, hawk_share: Fraction) -> Fraction:
        """متوسّطُ عائد المجتمع كلِّه عند نسبةٍ من الصقور."""

        return hawk_share * self.expected_payoff(Strategy.HAWK, hawk_share) + (
            1 - hawk_share
        ) * self.expected_payoff(Strategy.DOVE, hawk_share)

    def indifference_share(self) -> Fraction:
        """النسبةُ التي يتساوى عندها العائدان، مُشتَقّةً من شرط اللامبالاة.

        وحلُّها `V/C`، لكنّه يخرج هنا من حلّ المعادلة لا يُكتَب رقمًا؛ ويُقصَر
        على الواحد حين تكون الكلفةُ دون القيمة، إذ لا لامبالاةَ في المجال.
        """

        share = self.value / self.cost
        return min(share, Fraction(1))

    def equilibrium(self) -> Equilibrium:
        """أخرِج التوازنَ بجنسه ونسبته ومتوسّط عائده وفرقِه عن الأمثل."""

        share = self.indifference_share()
        kind = (
            EquilibriumKind.MIXED
            if self.cost > self.value
            else EquilibriumKind.PURE_HAWK
        )
        mean = self.mean_payoff(share)
        all_dove = self.mean_payoff(Fraction(0))
        return Equilibrium(
            hawk_share=share,
            kind=kind,
            mean_payoff=mean,
            all_dove_payoff=all_dove,
            optimality_gap=all_dove - mean,
        )

    def is_equilibrium(self, hawk_share: Fraction) -> bool:
        """أنسبةٌ ما توازنٌ؟ مُشتَقٌّ بالمقارنة لا مقروءٌ من حقل."""

        return hawk_share == self.equilibrium().hawk_share

    def replicator_step(self, hawk_share: float, step: float) -> float:
        """خطوةٌ واحدةٌ من دينامِكا المُماثلة: النموّ بفارق العائد عن المتوسّط.

        ولا تُقصَر النتيجةُ إلى المجال قسرًا: خطوةٌ تُخرِج النسبةَ عن المجال
        تُرَدُّ بخطوتها، إذ قصرُها صمتًا يُخفي أنّ الخطوةَ أكبرُ من أن تُحاكي.
        """

        if not 0 <= hawk_share <= 1:
            raise HawkDoveError("نسبةُ الصقور بين الصفر والواحد.")
        if step <= 0:
            raise HawkDoveError("طولُ الخطوة موجب.")
        share = Fraction(hawk_share).limit_denominator(10**9)
        advantage = float(
            self.expected_payoff(Strategy.HAWK, share)
            - self.expected_payoff(Strategy.DOVE, share)
        )
        moved = hawk_share + step * hawk_share * (1 - hawk_share) * advantage
        if not 0 <= moved <= 1:
            raise HawkDoveError(
                f"خطوةٌ أخرجت النسبةَ عن مجالها: {moved}؛ "
                "وقصرُها صمتًا يُخفي أنّ الخطوةَ أكبرُ من أن تُحاكي."
            )
        return moved

    def simulate(self, start: float, steps: int, step: float) -> tuple[float, ...]:
        """شغِّل الدينامِكا من نسبةٍ ابتدائيّةٍ وأخرِج مسارَها كاملًا."""

        if steps <= 0:
            raise HawkDoveError("عددُ الخطوات موجب.")
        path = [start]
        for _ in range(steps):
            path.append(self.replicator_step(path[-1], step))
        return tuple(path)


WHAT_A_LINGUISTIC_READING_WOULD_NEED: Final[tuple[str, ...]] = (
    "عائدٌ مُعرَّفٌ ومقيسٌ لكلّ استراتيجيّة، لا تشابهٌ في صورة التوزيع",
    "وحدةُ تنافسٍ مُسمّاةٌ: ما الذي يتنازع، وعلى أيّ مورد",
    "كلفةٌ مقيسةٌ للصراع بوحدةٍ واحدةٍ مع القيمة، لا بوحدتين",
    "مدوّنةٌ مُبصَّمةٌ وتوقّعٌ مكتوبٌ قبل القياس، لا بعد رؤية الرقم",
)
"""ما يلزم قبل قراءة هذه اللعبة نموذجًا لظاهرةٍ لغويّة؛ ولم يُجرَ منه شيء."""


THIS_MODEL_CLAIMS_NOTHING_ABOUT_ARABIC_NOTE: Final[str] = (
    "ThisModelClaimsNothingAboutArabic: التشابهُ في صورة التوزيع ليس شاهدًا؛ "
    "وما يجعل لعبةً نموذجًا لظاهرةٍ عائدٌ مُعرَّفٌ مقيس، ولا عائدَ مُعرَّفًا في "
    "تجنُّب الجذور"
)

THE_EQUILIBRIUM_IS_DERIVED_NOT_ASSERTED_NOTE: Final[str] = (
    "TheEquilibriumIsDerivedNotAsserted: النسبةُ تخرج من شرط اللامبالاة بكسورٍ "
    "صحيحة؛ ومن كتب V/C رقمًا ثمّ عرضه نتيجةً وصف ما افترض"
)

AN_ESS_IS_NOT_AN_OPTIMUM_NOTE: Final[str] = (
    "AnEssIsNotAnOptimum: متوسّطُ العائد عند التوازن أدنى منه في مجتمع "
    "الحمائم في المجالين كليهما، والفرقُ مطروحٌ لا موصوف؛ فالاستقرارُ ليس "
    "صلاحًا"
)

A_PURE_HAWK_POPULATION_IS_STABLE_ONLY_WHEN_FIGHTING_IS_CHEAP_NOTE: Final[str] = (
    "APureHawkPopulationIsStableOnlyWhenFightingIsCheap: إن كانت الكلفةُ دون "
    "القيمة فالصقرُ الخالصُ مستقرٌّ ولا خليط؛ والحالتان من مقارنةٍ واحدة، فلا "
    "تُكتَب إحداهما استثناءً"
)
