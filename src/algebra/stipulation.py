"""حسابُ المصادرات: كم يحمل بناءٌ، وكم ترفع عنه إعادةُ صياغته — بالبتّات.

**ما تفعله هذه الوحدة**: تأخذ **هدفًا** (لغةً منتهيةً مقيسة) و**عائلةَ نظريّاتٍ
مُعلَنةً**، فتحسب: كم عضوًا في العائلة، وكم عضوًا منها يُنتِج هدفًا منتهيًا
أصلًا، وكم عضوًا يُصيب الهدفَ بعينه، وكم بتًّا يلزم لتمييز العضو المصيب. وهي
لا تعرف موضوعًا: أبجديّةٌ وسلاسلُ محارف.

`A_TRANSFER_IS_NOT_A_DISCHARGE`: نقلُ الثقل من «أربعِ وقائعَ تُحصى» إلى «ثلاثةِ
منوعٍ تُشتَقّ منها» ليس سدادًا بذاته. وإنّما يكون مكسبًا إن تحقّق شرطان
**يُحسَبان**: أن تكون العائلةُ الجديدةُ **أصغر** بالبتّات، وأن تبقى **مصيبةً**
للهدف. فإن كبرت العائلةُ أو أخطأت الهدفَ فالنقلُ خسارةٌ تتزيّا بصورة تفسير.

`A_SCHEMA_IS_PRICED_BY_WHAT_IT_FORBIDS`: ثمنُ الصيغة ليس في عدد كلماتها بل في
**كم هدفًا تستطيع أن تبلغه أصلًا**. صيغةٌ تبلغ اثنين من مئةٍ وثمانيةٍ وعشرين
قد حرّمت ستًّا وعشرين ومئةً **قبل النظر في البيانات** — وذلك هو مضمونُها.
وصيغةٌ تبلغ كلَّ شيءٍ لا تقول شيئًا.

`A_LAST_BIT_MAY_BE_PAID_BY_MEASUREMENT_NOT_STIPULATION`: ما بقي بعد الرفع
مصادرةٌ **ما دام لم يُقَس**. فإن قاسه عدٌّ مباشرٌ صار واقعةً، والبقيّةُ صفر.
وهذا الفرقُ — بين بتٍّ مُصادَرٍ وبتٍّ مدفوعٍ بالعدّ — لا يظهر في عدد البتّات
وحدَه، فيُعلَن إلى جانبه.

`AN_UNREACHED_TARGET_IS_A_REFUTED_SCHEMA`: صيغةٌ لا تبلغ الهدفَ بأيّ ثمنٍ
**منقوضةٌ لا رخيصة**. فالصفرُ في عمود «يُصيب» ليس ثمنًا أدنى.

`BITS_ARE_COUNTED_OVER_A_DECLARED_FAMILY`: عددُ البتّات بلا اسمِ العائلة التي
عُدَّ عليها لا معنى له؛ فالعائلةُ تُسمّى مع الرقم دائمًا.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations
from typing import Final

__all__ = [
    "AN_UNREACHED_TARGET_IS_A_REFUTED_SCHEMA_NOTE",
    "A_LAST_BIT_MAY_BE_PAID_BY_MEASUREMENT_NOT_STIPULATION_NOTE",
    "A_SCHEMA_IS_PRICED_BY_WHAT_IT_FORBIDS_NOTE",
    "A_TRANSFER_IS_NOT_A_DISCHARGE_NOTE",
    "BITS_ARE_COUNTED_OVER_A_DECLARED_FAMILY_NOTE",
    "STIPULATION_NAMED_RESIDUALS",
    "Schema",
    "StipulationError",
    "Weighing",
    "ban_schema",
    "bits_to_single_out",
    "chain_schema",
    "chain_words",
    "list_schema",
    "weigh",
]


class StipulationError(ValueError):
    """رُفض هدفٌ أو عائلةٌ لا تقبل الحساب؛ ولا تُحمَل على أقرب مقبول."""


def bits_to_single_out(family_size: int) -> float:
    """كم بتًّا يلزم لتمييز عضوٍ واحدٍ من عائلةٍ بهذا الحجم."""

    if family_size < 1:
        raise StipulationError("عائلةٌ خاليةٌ لا يُميَّز منها عضو.")
    return math.log2(family_size)


def chain_words(order: tuple[str, ...]) -> frozenset[str]:
    """المتتالياتُ الهابطةُ تمامًا على ترتيبٍ خطّيٍّ مُعلَنٍ من الأعلى إلى الأدنى.

    وهي بعينها **المجموعاتُ الجزئيّةُ** مكتوبةً بترتيب الهبوط، فعددُها `2**n`
    لزومًا. وهذا تنبّؤٌ لا وصف: تغيُّرُ عددِ المستويات يُغيّر الجردَ سلفًا.
    """

    if len(set(order)) != len(order):
        raise StipulationError("ترتيبٌ خطّيٌّ لا يكرّر رمزًا.")
    return frozenset(
        "".join(chosen)
        for size in range(len(order) + 1)
        for chosen in combinations(order, size)
    )


@dataclass(frozen=True, slots=True)
class Schema:
    """عائلةُ نظريّاتٍ مُسمّاة: لكلّ عضوٍ اسمٌ ولغةٌ، أو `None` إن كانت لانهائيّة."""

    name: str
    members: tuple[tuple[str, frozenset[str] | None], ...]

    def __post_init__(self) -> None:
        if not self.members:
            raise StipulationError("صيغةٌ بلا أعضاءٍ ليست عائلة.")
        labels = [label for label, _ in self.members]
        if len(set(labels)) != len(labels):
            raise StipulationError("أعضاءُ الصيغة تُسمّى أسماءً مميَّزة.")

    @property
    def size(self) -> int:
        """حجمُ العائلة."""

        return len(self.members)

    def finite_members(self) -> tuple[tuple[str, frozenset[str]], ...]:
        """الأعضاءُ التي تُنتِج لغةً منتهيةً فعلًا."""

        return tuple(
            (label, words) for label, words in self.members if words is not None
        )

    def distinct_languages(self) -> int:
        """كم لغةً منتهيةً **مختلفةً** تستطيع هذه الصيغةُ أن تبلغها أصلًا."""

        return len({words for _, words in self.finite_members()})


def ban_schema(alphabet: tuple[str, ...]) -> Schema:
    """عائلةُ «المنوع»: كلُّ مجموعةٍ جزئيّةٍ من العوامل الثنائيّة نظريّةٌ.

    واللغةُ تُشتَقّ بـ`factor_language`، فالعضوُ الدوريُّ لغتُه لانهائيّةٌ
    ويُعلَن `None` بدل أن يُسكَت عنه.
    """

    from .factor_language import FactorLanguage

    factors = tuple(first + second for first in alphabet for second in alphabet)
    members: list[tuple[str, frozenset[str] | None]] = []
    for size in range(len(factors) + 1):
        for banned in combinations(factors, size):
            language = FactorLanguage(alphabet=alphabet, forbidden=frozenset(banned))
            words = language.words() if language.transition_graph_is_acyclic() else None
            members.append(("منعُ {" + "، ".join(banned) + "}", words))
    return Schema(name="المنوع", members=tuple(members))


def chain_schema(alphabet: tuple[str, ...]) -> Schema:
    """عائلةُ «السلسلة»: كلُّ ترتيبٍ خطّيٍّ على الأبجديّة نظريّةٌ، ولا رابعَ لها.

    وهي أضيقُ العائلات: عددُها `n!` لا `2**(n**2)`، وكلُّ أعضائها منتهية.
    """

    return Schema(
        name="السلسلة",
        members=tuple(
            (" > ".join(order), chain_words(order)) for order in permutations(alphabet)
        ),
    )


def list_schema(pool: tuple[str, ...]) -> Schema:
    """عائلةُ «القائمة»: كلُّ مجموعةٍ جزئيّةٍ من الكلمات الممكنة جردٌ مقبول.

    وهي أوسعُ العائلات، إذ لا تقول شيئًا: تبلغ كلَّ جردٍ يُتصوَّر.
    """

    if len(set(pool)) != len(pool):
        raise StipulationError("مجتمعُ الكلمات لا يكرّر كلمة.")
    members: list[tuple[str, frozenset[str] | None]] = []
    for size in range(len(pool) + 1):
        for chosen in combinations(pool, size):
            shown = "، ".join(word or "ε" for word in chosen)
            members.append(("{" + shown + "}", frozenset(chosen)))
    return Schema(name="القائمة", members=tuple(members))


@dataclass(frozen=True, slots=True)
class Weighing:
    """وزنُ صيغةٍ أمام هدفٍ مقيس: حجمُها، وما تبلغه، وما يُصيب، وثمنُه."""

    schema_name: str
    family_size: int
    finite_count: int
    distinct_languages: int
    reaching: tuple[str, ...]

    @property
    def reaches_target(self) -> bool:
        """أتبلغ هذه الصيغةُ الهدفَ أصلًا؟ فإن لم تبلغه فهي منقوضةٌ لا رخيصة."""

        return bool(self.reaching)

    @property
    def identifies_target(self) -> bool:
        """أيُصيبه عضوٌ **واحدٌ** لا غير؟ فالنقلُ حينئذٍ بلا فقدِ خبر."""

        return len(self.reaching) == 1

    @property
    def bits(self) -> float:
        """ثمنُ تمييز العضو المصيب من العائلة كلِّها."""

        return bits_to_single_out(self.family_size)

    @property
    def bits_given_finiteness(self) -> float:
        """ثمنُه لو أُعطيَ التناهي مجّانًا؛ ويُعلَن مفصولًا لأنّه شرطٌ لا هبة."""

        return bits_to_single_out(self.finite_count)

    def forbidden_share(self, conceivable: int) -> Fraction:
        """كم من الأهداف المتصوَّرة تحرّمها هذه الصيغةُ قبل النظر في البيانات."""

        if conceivable < 1:
            raise StipulationError("عددُ الأهداف المتصوَّرة واحدٌ فأكثر.")
        if self.distinct_languages > conceivable:
            raise StipulationError(
                "الصيغةُ تبلغ أكثرَ ممّا يُتصوَّر؛ فالمجتمعان غيرُ متوافقين."
            )
        return Fraction(conceivable - self.distinct_languages, conceivable)


def weigh(schema: Schema, target: frozenset[str]) -> Weighing:
    """زِن صيغةً أمام هدفٍ مقيس، بلا حكمٍ على أيّهما أولى — الحكمُ يُقرأ بعدُ."""

    if not target:
        raise StipulationError("هدفٌ خالٍ لا يُصاب؛ ولا يُحمَل على «أيّ شيء».")
    finite = schema.finite_members()
    return Weighing(
        schema_name=schema.name,
        family_size=schema.size,
        finite_count=len(finite),
        distinct_languages=schema.distinct_languages(),
        reaching=tuple(label for label, words in finite if words == target),
    )


A_TRANSFER_IS_NOT_A_DISCHARGE_NOTE: Final[str] = (
    "ATransferIsNotADischarge: نقلُ الثقل من وقائعَ تُحصى إلى منوعٍ تُشتَقّ منها "
    "مكسبٌ بشرطين يُحسَبان — عائلةٌ أصغرُ بالبتّات، وإصابةٌ للهدف؛ وإلّا فهو "
    "خسارةٌ تتزيّا بصورة تفسير"
)

A_SCHEMA_IS_PRICED_BY_WHAT_IT_FORBIDS_NOTE: Final[str] = (
    "ASchemaIsPricedByWhatItForbids: مضمونُ الصيغة في عدد ما لا تستطيع بلوغَه، "
    "لا في عدد كلماتها؛ وصيغةٌ تبلغ كلَّ شيءٍ لا تقول شيئًا"
)

A_LAST_BIT_MAY_BE_PAID_BY_MEASUREMENT_NOT_STIPULATION_NOTE: Final[str] = (
    "ALastBitMayBePaidByMeasurementNotStipulation: البتُّ الباقي مصادرةٌ ما دام "
    "لم يُقَس، فإن قاسه عدٌّ مباشرٌ صار واقعةً؛ والفرقُ لا يظهر في عدد البتّات "
    "فيُعلَن إلى جانبه"
)

AN_UNREACHED_TARGET_IS_A_REFUTED_SCHEMA_NOTE: Final[str] = (
    "AnUnreachedTargetIsARefutedSchema: صيغةٌ لا تبلغ الهدفَ بأيّ ثمنٍ منقوضةٌ "
    "لا رخيصة؛ والصفرُ في عمود الإصابة ليس ثمنًا أدنى"
)

BITS_ARE_COUNTED_OVER_A_DECLARED_FAMILY_NOTE: Final[str] = (
    "BitsAreCountedOverADeclaredFamily: عددُ البتّات بلا اسمِ العائلة التي عُدَّ "
    "عليها لا معنى له؛ فالعائلةُ تُسمّى مع الرقم دائمًا"
)

STIPULATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_TRANSFER_IS_NOT_A_DISCHARGE_NOTE,
    A_SCHEMA_IS_PRICED_BY_WHAT_IT_FORBIDS_NOTE,
    A_LAST_BIT_MAY_BE_PAID_BY_MEASUREMENT_NOT_STIPULATION_NOTE,
    AN_UNREACHED_TARGET_IS_A_REFUTED_SCHEMA_NOTE,
    BITS_ARE_COUNTED_OVER_A_DECLARED_FAMILY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
