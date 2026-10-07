"""ضمُّ الدَّين: تجانسٌ مكانَ إسنادٍ حرّ، وسلسلةٌ واحدةٌ مكانَ رأسٍ وذيل.

**ما تفعله هذه الوحدة**: تأخذ ذرّةً ذاتَ **مكوّنات**، وإسنادًا من أصنافها إلى
سلاسلَ على أبجديّةٍ صغرى — فتفحص أنّ الإسنادَ **تجانسٌ** (صورةُ الصنف حاصلُ
وصلِ صور مكوّناته)، وتبني الجردَ **سلسلةً واحدةً** لا رأسًا مفروضًا وذيلًا
مشتقًّا. وهي لا تعرف موضوعًا: مكوّناتٌ وسلاسلُ محارف.

`A_HOMOMORPHISM_IS_CHECKED_ON_EVERY_CLASS_NOT_ASSERTED`: قولُ «الإسنادُ
تجانسٌ» دعوًى تُفحَص على **كلّ** صنفٍ بالوصل، لا صفةٌ تُمنَح. وصنفٌ واحدٌ
يخالف يُسقِط الدعوى كلَّها، فلا تُصلَح باستثناء.

`A_PRIMITIVE_CONTRIBUTES_AT_MOST_ONE_SEGMENT`: التجانسُ وحدَه **لا يوفّر
شيئًا**، بل قد يُوسِّع العائلة: مولِّداتٌ أربعةٌ بحرّيّةِ سلسلتين أوسعُ من
ثلاثة أصنافٍ حرّة. والذي يوفّر هو القيدُ: **المولِّدُ يُسهِم بمقطعٍ واحدٍ على
الأكثر**. فهو المصادرةُ الحاملةُ، ويُعلَن ولا يُدَسّ في كلمة «تجانس».

`THE_HEAD_IS_THE_MAXIMUM_NOT_A_SEPARATE_STIPULATION`: حين يُبنى المقطعُ
سلسلةً هابطةً **تحوي أعلاها**، لا يبقى «الرأسُ CV» مفروضًا: هو أعلى السلسلة.
فما كان مصادرتين — رأسٌ يُختار وذيلٌ يُرتَّب — صار واحدةً.

`THE_COUNT_IS_TWO_TO_THE_ARITY_OF_THE_ATOM`: الأصنافُ الناقصةُ بعددِ مكوّنات
الذرّة، فالجردُ `2**k`. والعددُ ٤ ليس لأنّ الدرجتين اثنتان، بل لأنّ **الذرّةَ
زوج**. وهذا تنبّؤٌ: ذرّةٌ بثلاثة مكوّناتٍ توجب جردًا من ثمانية.

`A_CONSOLIDATED_DEBT_IS_STILL_A_DEBT`: ضمُّ ثلاثِ مصادراتٍ في مبدأٍ واحدٍ
**ليس سدادًا**. ما يتغيّر أنّ الباقيَ صار عبارةً واحدةً من جنسٍ واحدٍ، قابلةً
لقياسٍ من خارج النصّ. والفرقُ بين «أقلّ» و«لا شيء» يُقال ولا يُطوى.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Final

__all__ = [
    "A_CONSOLIDATED_DEBT_IS_STILL_A_DEBT_NOTE",
    "A_HOMOMORPHISM_IS_CHECKED_ON_EVERY_CLASS_NOT_ASSERTED_NOTE",
    "A_PRIMITIVE_CONTRIBUTES_AT_MOST_ONE_SEGMENT_NOTE",
    "CONSOLIDATION_NAMED_RESIDUALS",
    "ConsolidationError",
    "Homomorphism",
    "THE_COUNT_IS_TWO_TO_THE_ARITY_OF_THE_ATOM_NOTE",
    "THE_HEAD_IS_THE_MAXIMUM_NOT_A_SEPARATE_STIPULATION_NOTE",
    "bits",
    "chains_with_maximum",
    "derive_order",
    "inventory_size_from_arity",
]


class ConsolidationError(ValueError):
    """رُفض إسنادٌ أو ترتيبٌ لا يُشتَقّ؛ ولا يُصلَح باستثناء."""


@dataclass(frozen=True, slots=True)
class Homomorphism:
    """إسنادٌ من مولِّداتٍ إلى سلاسل، يُمَدّ بالوصل ويُفحَص على كلّ صنف."""

    generators: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        names = [name for name, _ in self.generators]
        if not names:
            raise ConsolidationError("تجانسٌ بلا مولِّداتٍ ليس إسنادًا.")
        if len(set(names)) != len(names):
            raise ConsolidationError("المولِّداتُ تُسمّى أسماءً مميَّزة.")

    @property
    def table(self) -> dict[str, str]:
        """صورُ المولِّدات مفهرسةً باسمها."""

        return dict(self.generators)

    @property
    def is_segmental(self) -> bool:
        """أيُسهِم كلُّ مولِّدٍ بمقطعٍ واحدٍ على الأكثر؟ وهو القيدُ الحامل."""

        return all(len(image) <= 1 for _, image in self.generators)

    def image_of(self, parts: Sequence[str]) -> str:
        """صورةُ صنفٍ حاصلَ وصلِ صور مكوّناته؛ ويُرَدّ مكوّنٌ غيرُ مُسمًّى."""

        table = self.table
        for part in parts:
            if part not in table:
                raise ConsolidationError(f"«{part}» ليس مولِّدًا في هذا التجانس.")
        return "".join(table[part] for part in parts)

    def agrees_with(
        self,
        classes: Mapping[str, Sequence[str]],
        observed: Mapping[str, str],
    ) -> bool:
        """أيطابق الوصلُ المرصودَ في **كلّ** صنف؟ وصنفٌ يخالف يُسقِط الدعوى."""

        if set(classes) != set(observed):
            raise ConsolidationError(
                "الأصنافُ المرصودةُ والمُسنَدةُ ليست واحدةً، فلا مقابلةَ بينهما."
            )
        return all(
            self.image_of(parts) == observed[name] for name, parts in classes.items()
        )


def chains_with_maximum(order: tuple[str, ...]) -> frozenset[str]:
    """المتتالياتُ الهابطةُ تمامًا التي **تحوي أعلى** الترتيب، موصولةً.

    وعددُها `2**(n-1)`: مجموعاتٌ جزئيّةٌ تضمّ عنصرًا بعينه. فالرأسُ ليس
    مفروضًا — هو أعلى السلسلة.
    """

    if len(set(order)) != len(order):
        raise ConsolidationError("ترتيبٌ خطّيٌّ لا يكرّر عنصرًا.")
    if not order:
        raise ConsolidationError("لا سلسلةَ على ترتيبٍ خالٍ.")
    top = order[0]
    return frozenset(
        "".join(chosen)
        for size in range(1, len(order) + 1)
        for chosen in combinations(order, size)
        if chosen[0] == top
    )


def derive_order(
    levels: Sequence[str], arity: Mapping[str, int], peak: str
) -> tuple[str, ...]:
    """رتِّب الدرجاتِ **بعدد المكوّنات ثمّ بالقرب من الذروة** — بلا اختيار.

    والأتمُّ مكوّناتٍ أعلى؛ وعند التساوي يتقدّم حاملُ رمزِ الذروة. ويُرَدّ
    ترتيبٌ يبقى فيه تساوٍ بعد الشرطين، فلا يُخترَع كسرٌ للتعادل صمتًا.
    """

    if len(set(levels)) != len(levels):
        raise ConsolidationError("الدرجاتُ لا تتكرّر.")
    missing = [level for level in levels if level not in arity]
    if missing:
        raise ConsolidationError(f"لا عددَ مكوّناتٍ لـ{missing}.")
    keyed = sorted(levels, key=lambda name: (-arity[name], 0 if name == peak else 1))
    keys = [(-arity[name], 0 if name == peak else 1) for name in keyed]
    if len(set(keys)) != len(keys):
        raise ConsolidationError(
            "بقي تعادلٌ بعد المكوّنات والقرب من الذروة؛ فالكسرُ مصادرةٌ تُعلَن."
        )
    return tuple(keyed)


def inventory_size_from_arity(arity: int) -> int:
    """`2**k` حيث `k` عددُ مكوّنات الذرّة — وهو عددُ أصنافها الناقصة."""

    if arity < 1:
        raise ConsolidationError("ذرّةٌ بلا مكوّنٍ واحدٍ ليست ذرّة.")
    return int(2**arity)


def bits(family_size: int) -> float:
    """ثمنُ تمييز عضوٍ من عائلةٍ بهذا الحجم؛ ويُعاد لأنّ العائلةَ تُسمّى معه."""

    if family_size < 1:
        raise ConsolidationError("عائلةٌ خاليةٌ لا يُميَّز منها عضو.")
    return math.log2(family_size)


A_HOMOMORPHISM_IS_CHECKED_ON_EVERY_CLASS_NOT_ASSERTED_NOTE: Final[str] = (
    "AHomomorphismIsCheckedOnEveryClassNotAsserted: «الإسنادُ تجانسٌ» دعوًى "
    "تُفحَص بالوصل على كلّ صنف، وصنفٌ واحدٌ يخالف يُسقِطها ولا تُصلَح باستثناء"
)

A_PRIMITIVE_CONTRIBUTES_AT_MOST_ONE_SEGMENT_NOTE: Final[str] = (
    "APrimitiveContributesAtMostOneSegment: التجانسُ وحدَه قد يُوسِّع العائلةَ "
    "لا يضيّقها؛ والموفِّرُ هو قيدُ «المولِّدُ مقطعٌ واحدٌ على الأكثر»، فيُعلَن "
    "ولا يُدَسّ في كلمة تجانس"
)

THE_HEAD_IS_THE_MAXIMUM_NOT_A_SEPARATE_STIPULATION_NOTE: Final[str] = (
    "TheHeadIsTheMaximumNotASeparateStipulation: سلسلةٌ هابطةٌ تحوي أعلاها لا "
    "تحتاج رأسًا مفروضًا؛ فما كان مصادرتين صار واحدة"
)

THE_COUNT_IS_TWO_TO_THE_ARITY_OF_THE_ATOM_NOTE: Final[str] = (
    "TheCountIsTwoToTheArityOfTheAtom: الأصنافُ الناقصةُ بعدد مكوّنات الذرّة، "
    "فالجردُ 2**k؛ والأربعةُ لأنّ الذرّةَ زوجٌ لا لأنّ الدرجتين اثنتان"
)

A_CONSOLIDATED_DEBT_IS_STILL_A_DEBT_NOTE: Final[str] = (
    "AConsolidatedDebtIsStillADebt: ضمُّ ثلاثِ مصادراتٍ في مبدأٍ واحدٍ ليس "
    "سدادًا؛ والفرقُ بين «أقلّ» و«لا شيء» يُقال ولا يُطوى"
)

CONSOLIDATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_HOMOMORPHISM_IS_CHECKED_ON_EVERY_CLASS_NOT_ASSERTED_NOTE,
    A_PRIMITIVE_CONTRIBUTES_AT_MOST_ONE_SEGMENT_NOTE,
    THE_HEAD_IS_THE_MAXIMUM_NOT_A_SEPARATE_STIPULATION_NOTE,
    THE_COUNT_IS_TWO_TO_THE_ARITY_OF_THE_ATOM_NOTE,
    A_CONSOLIDATED_DEBT_IS_STILL_A_DEBT_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
