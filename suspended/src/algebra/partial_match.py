"""المطابقةُ بمجاهيلَ: للثقب مجالٌ مُعلَن، وإلّا طابق ما لا يجوز.

**ما تفعله هذه الوحدة**: تطابق نمطًا فيه **ثقوب** بمرشَّحين، فتشترط أن يكون
لكلّ ثقبٍ **مجالٌ مسرود** لا «أيُّ شيء». وتُخرِج الفرقَ بين المطابقات المشروعة
وما يضيفه ثقبٌ بلا مجال — عددًا لا تقديرًا. وهي لا تعرف موضوعًا: رموزٌ في
متتاليات.

`A_HOLE_WITHOUT_A_DOMAIN_MATCHES_TOO_MUCH`: «مجهولٌ يطابق أيَّ شيء» ليس حيادًا
بل **دعوى**: أنّ كلَّ قيمةٍ ممكنةٌ في ذلك الموضع. وهي كاذبةٌ متى كان الموضعُ
مقيَّدًا بنوعه — صامتٌ بلا حركةٍ لا يكون مدًّا أبدًا. فالمجالُ يُسرَد شرطَ
إنشاء.

`AN_ABSENCE_CLAIM_IS_ONLY_AS_SOUND_AS_ITS_HOLES`: «لا ملءَ يطابق» بيانٌ عن
اللغة **إن كان مجالُ الملء صحيحًا**. فثقبٌ أوسعُ من حقّه يجعل الغيابَ أندر،
وثقبٌ أضيقُ يجعله أكثر — وفي الحالين يقيس الثقبَ لا اللغة.

`THE_SPURIOUS_MATCHES_ARE_COUNTED_NOT_ESTIMATED`: أثرُ توسيع الثقب يُعَدّ
بالتفريق بين المجموعتين، لا يُقدَّر بنسبةٍ ولا يُهمَل بوصفه صغيرًا.

`A_LENGTH_MISMATCH_IS_NOT_A_NEAR_MISS`: اختلافُ الطول ردٌّ قاطعٌ لا درجةُ
تشابه؛ ولا يُقرَّب نمطٌ إلى مرشَّحٍ بإسقاط موضع.

`A_TOTAL_MAP_RAISES_ITS_OWN_ERROR_NOT_A_KEY_ERROR`: تحويلٌ يُدَّعى تمامُه
يرفع خطأَه المُسمّى على ما خرج عن مجاله، لا `KeyError` عارية. فالرسالةُ
تقول أيُّ رمزٍ خرج وأيُّ مجالٍ خالفه.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Final

__all__ = [
    "AN_ABSENCE_CLAIM_IS_ONLY_AS_SOUND_AS_ITS_HOLES_NOTE",
    "A_HOLE_WITHOUT_A_DOMAIN_MATCHES_TOO_MUCH_NOTE",
    "A_LENGTH_MISMATCH_IS_NOT_A_NEAR_MISS_NOTE",
    "A_TOTAL_MAP_RAISES_ITS_OWN_ERROR_NOT_A_KEY_ERROR_NOTE",
    "Hole",
    "PARTIAL_MATCH_NAMED_RESIDUALS",
    "PartialMatchError",
    "THE_SPURIOUS_MATCHES_ARE_COUNTED_NOT_ESTIMATED_NOTE",
    "matches",
    "spurious_matches",
    "total_map",
    "unify",
]

Pattern = Sequence["str | Hole"]


class PartialMatchError(ValueError):
    """رُفض ثقبٌ بلا مجالٍ أو تحويلٌ على رمزٍ خارجَ مجاله؛ ولا يُحمَل على أقرب."""


@dataclass(frozen=True, slots=True)
class Hole:
    """ثقبٌ في النمط: اسمُه ومجالُه المسرود — ولا ثقبَ مجالُه «كلُّ شيء»."""

    name: str
    domain: frozenset[str]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise PartialMatchError("ثقبٌ بلا اسمٍ لا يُحاسَب.")
        if not self.domain:
            raise PartialMatchError(
                f"ثقبُ «{self.name}» بلا مجالٍ مسرود؛ و«أيُّ شيء» دعوًى لا حياد "
                "(A_HOLE_WITHOUT_A_DOMAIN_MATCHES_TOO_MUCH)."
            )

    def admits(self, symbol: str) -> bool:
        """أيقبل هذا الثقبُ هذا الرمز؟"""

        return symbol in self.domain


def unify(pattern: Pattern, candidate: Sequence[str]) -> bool:
    """أيطابق النمطُ المرشَّحَ؟ الطولُ شرطٌ قاطع، والثقبُ يقبل مجالَه وحدَه."""

    if len(pattern) != len(candidate):
        return False
    for slot, symbol in zip(pattern, candidate, strict=True):
        if isinstance(slot, Hole):
            if not slot.admits(symbol):
                return False
        elif slot != symbol:
            return False
    return True


def matches(
    pattern: Pattern, candidates: Iterable[Sequence[str]]
) -> tuple[tuple[str, ...], ...]:
    """المرشَّحون الذين يطابقون، بترتيب ورودهم وبلا تكرارٍ للمتطابقين نصًّا."""

    found: list[tuple[str, ...]] = []
    for candidate in candidates:
        if unify(pattern, candidate) and tuple(candidate) not in found:
            found.append(tuple(candidate))
    return tuple(found)


def spurious_matches(
    pattern: Pattern, candidates: Iterable[Sequence[str]], universe: Iterable[str]
) -> tuple[tuple[str, ...], ...]:
    """ما يضيفه ثقبٌ **بلا مجال**: الفرقُ بين المطابقتين، معدودًا لا مقدَّرًا.

    و`universe` جردُ الرموز الممكنة كلِّها — وهو ما يصير إليه الثقبُ لو تُرِك
    بلا مجال. فالمُخرَجُ هو ما كان سيُقبَل ولا يجوز قبولُه.
    """

    everything = frozenset(universe)
    if not everything:
        raise PartialMatchError("جردٌ خالٍ للرموز لا يُقارَن به مجال.")
    wide: list[str | Hole] = [
        Hole(name=slot.name, domain=everything) if isinstance(slot, Hole) else slot
        for slot in pattern
    ]
    pool = [tuple(candidate) for candidate in candidates]
    strict = set(matches(pattern, pool))
    return tuple(
        candidate for candidate in matches(wide, pool) if candidate not in strict
    )


def total_map(
    table: Mapping[str, str], symbols: Sequence[str], what: str = "الرمز"
) -> tuple[str, ...]:
    """حوِّل متتاليةً بجدولٍ يُدَّعى تمامُه؛ وما خرج عنه يرفع خطأً **مُسمًّى**."""

    out: list[str] = []
    for symbol in symbols:
        if symbol not in table:
            raise PartialMatchError(
                f"{what} «{symbol}» خارجَ مجال التحويل "
                f"({'، '.join(sorted(table))}) — والتحويلُ مُدَّعًى تمامُه "
                "(A_TOTAL_MAP_RAISES_ITS_OWN_ERROR_NOT_A_KEY_ERROR)."
            )
        out.append(table[symbol])
    return tuple(out)


A_HOLE_WITHOUT_A_DOMAIN_MATCHES_TOO_MUCH_NOTE: Final[str] = (
    "AHoleWithoutADomainMatchesTooMuch: «مجهولٌ يطابق أيَّ شيء» دعوًى لا حياد، "
    "وهي كاذبةٌ متى كان الموضعُ مقيَّدًا بنوعه؛ فالمجالُ يُسرَد شرطَ إنشاء"
)

AN_ABSENCE_CLAIM_IS_ONLY_AS_SOUND_AS_ITS_HOLES_NOTE: Final[str] = (
    "AnAbsenceClaimIsOnlyAsSoundAsItsHoles: «لا ملءَ يطابق» بيانٌ عن اللغة إن "
    "صحّ مجالُ الملء؛ وثقبٌ أوسعُ من حقّه يقيس الثقبَ لا اللغة"
)

THE_SPURIOUS_MATCHES_ARE_COUNTED_NOT_ESTIMATED_NOTE: Final[str] = (
    "TheSpuriousMatchesAreCountedNotEstimated: أثرُ توسيع الثقب يُعَدّ بالتفريق "
    "بين المجموعتين، لا يُقدَّر بنسبةٍ ولا يُهمَل بوصفه صغيرًا"
)

A_LENGTH_MISMATCH_IS_NOT_A_NEAR_MISS_NOTE: Final[str] = (
    "ALengthMismatchIsNotANearMiss: اختلافُ الطول ردٌّ قاطعٌ لا درجةُ تشابه، "
    "ولا يُقرَّب نمطٌ إلى مرشَّحٍ بإسقاط موضع"
)

A_TOTAL_MAP_RAISES_ITS_OWN_ERROR_NOT_A_KEY_ERROR_NOTE: Final[str] = (
    "ATotalMapRaisesItsOwnErrorNotAKeyError: تحويلٌ يُدَّعى تمامُه يرفع خطأَه "
    "المُسمّى ويقول أيُّ رمزٍ خرج وأيُّ مجالٍ خالفه"
)

PARTIAL_MATCH_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_HOLE_WITHOUT_A_DOMAIN_MATCHES_TOO_MUCH_NOTE,
    AN_ABSENCE_CLAIM_IS_ONLY_AS_SOUND_AS_ITS_HOLES_NOTE,
    THE_SPURIOUS_MATCHES_ARE_COUNTED_NOT_ESTIMATED_NOTE,
    A_LENGTH_MISMATCH_IS_NOT_A_NEAR_MISS_NOTE,
    A_TOTAL_MAP_RAISES_ITS_OWN_ERROR_NOT_A_KEY_ERROR_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
