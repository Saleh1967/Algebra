"""سجلُّ قرارات: ما ينتظر قرارًا يصير عينًا مُقيَّدةً، لا سطرًا في محادثة.

**ما تفعله هذه الوحدة**: تُقيِّد القرارَ بأنواعٍ مغلقةٍ وشروطِ إنشاء — سؤالُه،
وما يَحجُبه، وفروعُه **بأثمانها** — ثمّ تردُّ إعلانَ تمامِ ما يحجُبه قرارٌ
معلَّق. فما كان معلَّقًا في محادثةٍ يُنسى أو يُقرأ بعد حينٍ كأنّه حُسِم.

`A_PENDING_DECISION_IS_NOT_A_DEFAULT`: المعلَّقُ لا يصير فرعًا بالسكوت، وإعلانُ
التمام يُرَدُّ عند الاستدعاء لا يُوصَف في حاشية.

`A_BRANCH_WITHOUT_A_PRICE_IS_NOT_A_BRANCH`: فرعٌ بلا ثمنٍ يُختار مجّانًا ثمّ
يُدفع ثمنُه بعد النظر؛ فالثمنُ شرطُ إنشاءٍ لا وصفٌ اختياريّ.

`DELEGATION_IS_NOT_A_SIGNATURE`: «لا تفضيل» تفويضٌ لا اختيارُ فرع. فلا يُقيَّد
القرارُ متَّخَذًا باسم مالكه — إذ يُنسِب إليه ما لم يُسمِّه — ولا يبقى معلَّقًا —
إذ يُخفي أنّه فوَّض. ولذلك منزلةٌ رابعةٌ `DELEGATED` يُسمّى فيها **الوكيلُ في
حقلٍ غيرِ حقل السلطة**، فيبقى الفرقُ بين مَن يملك القرارَ ومَن اختار.

`THE_WRITER_OF_A_REGISTER_IS_NOT_ITS_AUTHORITY`: السلطاتُ المرفوضةُ **معطًى**
لكلّ سجلٍّ لا قائمةٌ مكتوبةٌ في متن الوحدة؛ فمن بنى سجلًّا أعلن فيه مَن لا
يُوقِّعه — وأوّلُهم كاتبُه.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_DOMAIN`: ما هنا مسكُ دفترٍ بأنواعٍ مغلقة،
لا حكمٌ في موضوعٍ بعينه.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Final

__all__ = [
    "A_BRANCH_WITHOUT_A_PRICE_IS_NOT_A_BRANCH_NOTE",
    "A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE",
    "DECISIONS_NAMED_RESIDUALS",
    "DELEGATION_IS_NOT_A_SIGNATURE_NOTE",
    "THE_WRITER_OF_A_REGISTER_IS_NOT_ITS_AUTHORITY_NOTE",
    "Branch",
    "Decision",
    "DecisionError",
    "Register",
    "Standing",
]


class DecisionError(ValueError):
    """رُفض قرارٌ ناقصٌ أو تمامٌ محجوب؛ ولا يُحمَل على أقرب مقبول."""


class Standing(Enum):
    """منازلُ القرار، مغلقةً أربعًا: ولا منزلةَ اسمُها «مفترَض»."""

    PENDING = "معلَّق"
    TAKEN = "متَّخَذ"
    DELEGATED = "مُفوَّض"
    DECLINED = "مردود"


@dataclass(frozen=True, slots=True)
class Branch:
    """فرعُ قرارٍ باسمه وأثرِه **وثمنِه**؛ وفرعٌ بلا ثمنٍ لا يُقيَّد."""

    label: str
    effect: str
    price: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.label, "اسمُ الفرع"),
            (self.effect, "ما يتغيّر"),
            (self.price, "الثمن"),
        ):
            if not value.strip():
                raise DecisionError(
                    f"{name} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ وفرعٌ بلا ثمنٍ "
                    "يُختار مجّانًا ثمّ يُدفع ثمنُه بعد النظر."
                )


@dataclass(frozen=True, slots=True)
class Decision:
    """قرارٌ مُقيَّد: سؤالُه، وما يحجُبه، وفروعُه، ومنزلتُه — ولا سلطةَ مُلفَّقة."""

    identifier: str
    question: str
    blocks: tuple[str, ...]
    branches: tuple[Branch, ...]
    standing: Standing = Standing.PENDING
    chosen_branch: str | None = None
    authority: str | None = None
    delegate: str | None = None
    decided_on: date | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise DecisionError("قرارٌ بلا معرِّفٍ لا يُحال إليه باسمه.")
        if not self.question.strip():
            raise DecisionError(f"{self.identifier}: قرارٌ بلا سؤال.")
        if not self.blocks:
            raise DecisionError(
                f"{self.identifier}: ما يحجُبه شرطُ إنشاء؛ وقرارٌ لا يحجُب شيئًا "
                "لا يُقيَّد سجلًّا."
            )
        if len(self.branches) < 2:
            raise DecisionError(
                f"{self.identifier}: القرارُ فرعان فأكثر؛ وفرعٌ واحدٌ إعلانٌ " "لا قرار."
            )
        labels = [branch.label for branch in self.branches]
        if len(set(labels)) != len(labels):
            raise DecisionError(f"{self.identifier}: فرعان بالاسم نفسِه.")
        if self.standing is Standing.DELEGATED:
            if self.delegate is None or not self.delegate.strip():
                raise DecisionError(
                    f"{self.identifier}: مُفوَّضٌ بلا وكيلٍ مُسمًّى؛ فيُقرأ "
                    "اختيارُ الوكيل كلامَ الموكِّل."
                )
            if self.chosen_branch is None:
                raise DecisionError(f"{self.identifier}: مُفوَّضٌ بلا فرعٍ مُسمًّى.")
        elif self.delegate is not None:
            raise DecisionError(
                f"{self.identifier}: وكيلٌ في قرارٍ غيرِ مُفوَّض؛ ومَن اختار "
                "بنفسه ليس وكيلًا عن نفسه."
            )
        if self.standing is Standing.PENDING:
            if self.chosen_branch is not None or self.authority is not None:
                raise DecisionError(
                    f"{self.identifier}: معلَّقٌ بفرعٍ مُختارٍ أو سلطةٍ مُوقِّعة؛ "
                    "والمعلَّقُ لا يصير فرعًا بالسكوت."
                )
            if self.decided_on is not None:
                raise DecisionError(f"{self.identifier}: معلَّقٌ بتاريخِ حسم.")
        else:
            if self.authority is None or not self.authority.strip():
                raise DecisionError(f"{self.identifier}: محسومٌ أو مُفوَّضٌ بلا سلطةٍ مسمّاة.")
            if self.decided_on is None:
                raise DecisionError(f"{self.identifier}: محسومٌ بلا تاريخ.")
        if self.standing is Standing.TAKEN and self.chosen_branch is None:
            raise DecisionError(f"{self.identifier}: متَّخَذٌ بلا فرعٍ مُسمًّى.")
        if self.standing is Standing.DECLINED and self.chosen_branch is not None:
            raise DecisionError(f"{self.identifier}: مردودٌ بفرعٍ مُختار.")
        if self.chosen_branch is not None and self.chosen_branch not in labels:
            raise DecisionError(
                f"{self.identifier}: الفرعُ «{self.chosen_branch}» ليس من فروعه."
            )
        if self.delegate is not None and self.delegate == self.authority:
            raise DecisionError(
                f"{self.identifier}: الوكيلُ هو الموكِّل؛ وذلك يُلغي الفرقَ."
            )


@dataclass(frozen=True, slots=True)
class Register:
    """سجلُّ قراراتٍ بسلطاتٍ مرفوضةٍ **مُعلَنةٍ فيه**، لا مكتوبةٍ في متن الوحدة."""

    decisions: tuple[Decision, ...]
    refused_authorities: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.decisions:
            raise DecisionError("سجلٌّ بلا قرارٍ واحدٍ لا يُقيَّد.")
        identifiers = [decision.identifier for decision in self.decisions]
        if len(set(identifiers)) != len(identifiers):
            raise DecisionError("معرِّفان متكرّران في السجلّ.")
        for decision in self.decisions:
            if (
                decision.authority is not None
                and decision.authority in self.refused_authorities
            ):
                raise DecisionError(
                    f"{decision.identifier}: السلطةُ «{decision.authority}» "
                    "مرفوضةٌ في هذا السجلّ؛ ولا يُوقِّعه مَن أُعلِن أنّه لا يُوقِّعه."
                )

    def pending(self) -> tuple[Decision, ...]:
        """ما لم يُحسَم، مُشتَقًّا بالمنزلة لا مكتوبًا."""

        return tuple(
            decision
            for decision in self.decisions
            if decision.standing is Standing.PENDING
        )

    def blocked_items(self) -> tuple[str, ...]:
        """كلُّ ما يحجُبه قرارٌ معلَّق، مرتَّبًا ترتيبًا ثابتًا."""

        return tuple(
            sorted({item for decision in self.pending() for item in decision.blocks})
        )

    def blockers_of(self, item: str) -> tuple[Decision, ...]:
        """القراراتُ المعلَّقةُ التي تحجُب شيئًا بعينه."""

        return tuple(decision for decision in self.pending() if item in decision.blocks)

    def assert_not_reportable_as_done(self, item: str) -> None:
        """ردُّ إعلانِ تمامٍ لمحجوب؛ والحجبُ يُقال ويُسمّى حاجبُه."""

        blockers = self.blockers_of(item)
        if blockers:
            named = "، ".join(decision.identifier for decision in blockers)
            raise DecisionError(
                f"«{item}» محجوبٌ بقرارٍ معلَّق ({named})؛ ولا يُعلَن تمامًا. "
                "والمحجوبُ ليس ساقطًا: هو غيرُ مُنجَزٍ بقرارٍ مُسمًّى."
            )

    def digest(self) -> str:
        """بصمةُ السجلّ: قرارٌ يُبدَّل لاحقًا يُعرَف بتغيُّرها."""

        parts: list[str] = []
        for decision in self.decisions:
            parts.extend(
                (
                    decision.identifier,
                    decision.question,
                    decision.standing.name,
                    decision.chosen_branch or "-",
                    decision.authority or "-",
                    decision.delegate or "-",
                    *decision.blocks,
                )
            )
            for branch in decision.branches:
                parts.extend((branch.label, branch.effect, branch.price))
            parts.append(decision.note)
        return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE: Final[str] = (
    "APendingDecisionIsNotADefault: المعلَّقُ لا يصير فرعًا بالسكوت، وإعلانُ تمامِ "
    "محجوبٍ مردودٌ عند الاستدعاء لا موصوفٌ في حاشية"
)

A_BRANCH_WITHOUT_A_PRICE_IS_NOT_A_BRANCH_NOTE: Final[str] = (
    "ABranchWithoutAPriceIsNotABranch: فرعٌ بلا ثمنٍ يُختار مجّانًا ثمّ يُدفع "
    "ثمنُه بعد النظر؛ فالثمنُ شرطُ إنشاء"
)

DELEGATION_IS_NOT_A_SIGNATURE_NOTE: Final[str] = (
    "DelegationIsNotASignature: «لا تفضيل» تفويضٌ لا اختيارُ فرع؛ فالفرعُ "
    "المُقيَّدُ قراءةُ الوكيل لا كلمةُ المالك، والمنزلةُ الرابعةُ تحفظ الفرقَ"
)

THE_WRITER_OF_A_REGISTER_IS_NOT_ITS_AUTHORITY_NOTE: Final[str] = (
    "TheWriterOfARegisterIsNotItsAuthority: السلطاتُ المرفوضةُ معطًى لكلّ سجلٍّ "
    "لا قائمةٌ في متن الوحدة؛ فمن بنى سجلًّا أعلن مَن لا يُوقِّعه، وأوّلُهم كاتبُه"
)

DECISIONS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE,
    A_BRANCH_WITHOUT_A_PRICE_IS_NOT_A_BRANCH_NOTE,
    DELEGATION_IS_NOT_A_SIGNATURE_NOTE,
    THE_WRITER_OF_A_REGISTER_IS_NOT_ITS_AUTHORITY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
