"""الشاهدُ المفرد: مفترَقٌ لا نسبة، وخروجُه من المجال يُسحَب معه أهلُه.

**ما تفعله هذه الوحدة**: تأخذ حالةً واحدةً تخالف قاعدةً، والاصطلاحَ الذي
جعلها مخالِفة، وما يحمله ذلك الاصطلاحُ من قياساتٍ أخرى — فتُخرِج **مفترقًا
مُسعَّرًا**، وتردّ ثلاثةَ مهارب. وهي لا تعرف موضوعًا: أسماءٌ وقوائم.

`THE_CONVENTION_THAT_MAKES_THE_RULE_MAKES_THE_EXCEPTION`: الحالةُ لا تخالف
إلّا تحت اصطلاحٍ في التمثيل. وذلك الاصطلاحُ نفسُه هو الذي أنتج القياساتِ
التي تُسند القاعدة. فلا يُنقَض به هنا ويُثبَت به هناك.

`A_CASE_IS_OUT_OF_SCOPE_ONLY_IF_ITS_CONVENTION_CARRIES_NOTHING_ELSE`: «خارجُ
المجال» حكمٌ **مشروطٌ** لا مَخرَج. ويصحّ إن كان اصطلاحُها لا يحمل سواها؛ فإن
حمل قياساتٍ حيّةً، فإخراجُها يُخرِجها معها. والوحدةُ تُعدِّد ما يسقط ولا
تدع الحكمَ مجّانيًّا.

`WITHDRAWING_A_CASE_WITHDRAWS_ITS_KIN`: سحبُ الحالة سحبٌ لكلّ ما وُلِد من
اصطلاحها. وقائمةُ ما يُسحَب تُطبَع مع الحكم، لا تُترَك للقارئ يستنبطها.

`A_SINGLE_WITNESS_IS_A_FORK_NOT_A_RATE`: شاهدٌ واحدٌ لا يُقسَم على مجتمعٍ
فيصير «٠٫٠٠١٪». المفردُ يُلزِم اختيارًا، والنسبةُ تُخفيه. فالقسمةُ **مردودةٌ
في المتن** لا منهيٌّ عنها في تعليق.

`A_PENDING_TEST_IS_NAMED_OR_THE_COST_IS_UNKNOWN`: ما يُظَنّ أنّه يقوم على
الاصطلاح ولمّا يُفحَص يُسمّى **مع فحصه الفاصل**، ولا يُخلَط بما ثبت. فالكلفةُ
المظنونةُ ليست كلفةً حتى يُجرى الفحصُ المُسمّى.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .decisions import Branch

__all__ = [
    "A_CASE_IS_OUT_OF_SCOPE_ONLY_IF_ITS_CONVENTION_CARRIES_NOTHING_ELSE_NOTE",
    "A_PENDING_TEST_IS_NAMED_OR_THE_COST_IS_UNKNOWN_NOTE",
    "A_SINGLE_WITNESS_IS_A_FORK_NOT_A_RATE_NOTE",
    "Case",
    "Convention",
    "Fork",
    "THE_CONVENTION_THAT_MAKES_THE_RULE_MAKES_THE_EXCEPTION_NOTE",
    "WITHDRAWING_A_CASE_WITHDRAWS_ITS_KIN_NOTE",
    "WITNESS_NAMED_RESIDUALS",
    "WitnessError",
]


class WitnessError(ValueError):
    """رُفض شاهدٌ أو مفترقٌ ناقصُ السعر؛ ولا يُحمَل على أقرب مقبول."""


@dataclass(frozen=True, slots=True)
class Convention:
    """اصطلاحٌ في التمثيل: ما يقرّره، وما ثبت أنّه يحمله، وما ينتظر فحصًا."""

    name: str
    decides: str
    carries: tuple[str, ...] = ()
    pending: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.decides.strip():
            raise WitnessError("اصطلاحٌ بلا اسمٍ أو بلا ما يقرّره ليس اصطلاحًا.")
        for item, test in self.pending:
            if not item.strip() or not test.strip():
                raise WitnessError(
                    "المظنونُ يُسمّى مع فحصه الفاصل "
                    "(A_PENDING_TEST_IS_NAMED_OR_THE_COST_IS_UNKNOWN)."
                )
        if set(self.carries) & {item for item, _ in self.pending}:
            raise WitnessError("لا يكون الشيءُ ثابتًا ومظنونًا معًا.")

    @property
    def carries_nothing_else(self) -> bool:
        """أيحمل هذا الاصطلاحُ شيئًا سوى الحالة؟ وعليه يدور حكمُ «خارجِ المجال»."""

        return not self.carries


@dataclass(frozen=True, slots=True)
class Case:
    """حالةٌ واحدةٌ تخالف قاعدةً — تحت اصطلاحٍ مُسمًّى، لا في الهواء."""

    name: str
    violates: str
    under: Convention
    occurrences: int = 1

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.violates.strip():
            raise WitnessError("حالةٌ بلا اسمٍ أو بلا قاعدةٍ تخالفها ليست حالة.")
        if self.occurrences < 1:
            raise WitnessError("حالةٌ بلا وقوعٍ واحدٍ ليست شاهدًا.")


@dataclass(frozen=True, slots=True)
class Fork:
    """مفترقٌ مُسعَّرٌ: إمّا القاعدةُ باطلةٌ وإمّا الاصطلاحُ، ولا ثالثَ مجّانيّ."""

    case: Case
    rule_is_false: Branch
    convention_is_wrong: Branch

    @property
    def cost_of_denying(self) -> tuple[str, ...]:
        """ما يسقط إن قيل «التمثيلُ خطأٌ» — وهو ما يحمله الاصطلاحُ نفسُه."""

        return self.case.under.carries

    @property
    def pending_costs(self) -> tuple[tuple[str, str], ...]:
        """ما يُظَنّ سقوطُه، مع الفحص الفاصل في كلٍّ منه."""

        return self.case.under.pending

    @property
    def may_be_called_out_of_scope(self) -> bool:
        """أيجوز إخراجُها من المجال مجّانًا؟ لا، إلّا إن كان اصطلاحُها عقيمًا."""

        return self.case.under.carries_nothing_else

    def out_of_scope_withdraws(self) -> tuple[str, ...]:
        """عدِّد ما يُسحَب مع إخراجها؛ ويُرَدّ الإخراجُ إن كان ثمنُه غيرَ صفر."""

        if self.may_be_called_out_of_scope:
            return ()
        raise WitnessError(
            "«خارجُ المجال» غيرُ مجّانيّ: اصطلاحُها يحمل "
            + "، ".join(self.cost_of_denying)
            + " — فإخراجُها يُخرِجها معها "
            "(A_CASE_IS_OUT_OF_SCOPE_ONLY_IF_ITS_CONVENTION_CARRIES_NOTHING_ELSE)."
        )

    def as_rate(self, population: int) -> float:
        """مردودٌ دائمًا: المفردُ يُلزِم اختيارًا، والنسبةُ تُخفيه."""

        raise WitnessError(
            f"لا تُقسَم حالةٌ واحدةٌ على {population}: "
            "شاهدٌ مفردٌ مفترقٌ لا نسبة "
            "(A_SINGLE_WITNESS_IS_A_FORK_NOT_A_RATE)."
        )


THE_CONVENTION_THAT_MAKES_THE_RULE_MAKES_THE_EXCEPTION_NOTE: Final[str] = (
    "TheConventionThatMakesTheRuleMakesTheException: الحالةُ لا تخالف إلّا تحت "
    "اصطلاحٍ في التمثيل، وذلك الاصطلاحُ نفسُه أنتج ما يُسنِد القاعدة؛ فلا "
    "يُنقَض به هنا ويُثبَت به هناك"
)

A_CASE_IS_OUT_OF_SCOPE_ONLY_IF_ITS_CONVENTION_CARRIES_NOTHING_ELSE_NOTE: Final[str] = (
    "ACaseIsOutOfScopeOnlyIfItsConventionCarriesNothingElse: «خارجُ المجال» "
    "حكمٌ مشروطٌ لا مَخرَج؛ فإن حمل اصطلاحُها قياساتٍ حيّةً أخرجها معها"
)

WITHDRAWING_A_CASE_WITHDRAWS_ITS_KIN_NOTE: Final[str] = (
    "WithdrawingACaseWithdrawsItsKin: سحبُ الحالة سحبٌ لكلّ ما وُلِد من "
    "اصطلاحها، وقائمةُ ما يُسحَب تُطبَع مع الحكم"
)

A_SINGLE_WITNESS_IS_A_FORK_NOT_A_RATE_NOTE: Final[str] = (
    "ASingleWitnessIsAForkNotARate: شاهدٌ واحدٌ لا يُقسَم على مجتمعٍ فيصير "
    "كسرًا من الألف؛ المفردُ يُلزِم اختيارًا والنسبةُ تُخفيه"
)

A_PENDING_TEST_IS_NAMED_OR_THE_COST_IS_UNKNOWN_NOTE: Final[str] = (
    "APendingTestIsNamedOrTheCostIsUnknown: المظنونُ قيامُه على الاصطلاح "
    "يُسمّى مع فحصه الفاصل ولا يُخلَط بما ثبت؛ فالكلفةُ المظنونةُ ليست كلفة"
)

WITNESS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_CONVENTION_THAT_MAKES_THE_RULE_MAKES_THE_EXCEPTION_NOTE,
    A_CASE_IS_OUT_OF_SCOPE_ONLY_IF_ITS_CONVENTION_CARRIES_NOTHING_ELSE_NOTE,
    WITHDRAWING_A_CASE_WITHDRAWS_ITS_KIN_NOTE,
    A_SINGLE_WITNESS_IS_A_FORK_NOT_A_RATE_NOTE,
    A_PENDING_TEST_IS_NAMED_OR_THE_COST_IS_UNKNOWN_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
