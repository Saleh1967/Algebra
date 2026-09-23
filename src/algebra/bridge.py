"""جبرُ الجسر: مستوًى يُعلَن مغلقًا أو مفتوحًا، وجسرٌ لا يُسقِط شيئًا صمتًا.

**ما تفعله هذه الوحدة**: تصف **سُلَّمَ مستويات** وجسورَها، فتفحص أنّ السلسلة
متّصلةٌ بلا فجوة، وأنّ كلَّ جسرٍ غيرِ مبنيٍّ **يُسمّي الأوراكلَ** الذي ينقصه،
وأنّ كلَّ عبورٍ **يوازن**: ما دخل = ما خرج + ما رُدَّ بسببٍ مُسمًّى. وهي لا
تعرف لغةً: أسماءٌ وأعداد.

`A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE`: جسرٌ يأخذ ١٣٦ ويعطي ما دونها بلا
بيانٍ ليس ناقصًا بل **كاذب**. فالموازنةُ شرطُ إنشاءٍ ههنا: `دخل = خرج + رُدّ`،
وإلّا رُفِض العبورُ كلُّه. وهذا بعينه ما وقع حين أسقط محلِّلٌ مدخلاتِ `آ`.

`A_REFUSAL_IS_NAMED_NOT_COUNTED`: المردودُ يُسمّى سببُه ويُعَدّ بسببه. وجمعُ
المردودات في رقمٍ واحدٍ يخفي أنّ بعضَها عيبُ أداةٍ وبعضَها خبرٌ عن اللغة.

`AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE`: مستوًى لا يُبلَغ بلا معطًى من خارج
يقول **أيَّ معطًى**. و«يحتاج معجمًا» بلا تسميةٍ ليس إعلانًا.

`A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER`: الجسورُ تتّصل طرفًا بطرف. وجسرٌ مبنيٌّ
فوق فجوةٍ **لا يُبلَغ من الأسفل** وإن صحّ في نفسه؛ فيُفصَل «مبنيٌّ» عن
«مبلوغ»، ولا يُخلَطان في كلمة «جاهز».

`A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN`: مستوًى يُدَّعى انغلاقُه
يسرد جردَه. وما لم يُسرَد فهو مفتوحٌ حكمًا، ولا يُقال «مغلقٌ عمليًّا».
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE_NOTE",
    "A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE_NOTE",
    "A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN_NOTE",
    "A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER_NOTE",
    "A_REFUSAL_IS_NAMED_NOT_COUNTED_NOTE",
    "BRIDGE_NAMED_RESIDUALS",
    "Bridge",
    "BridgeError",
    "Crossing",
    "Ladder",
    "Level",
]


class BridgeError(ValueError):
    """رُفض مستوًى أو جسرٌ أو عبورٌ لا يوازن؛ ولا يُحمَل على أقرب مقبول."""


@dataclass(frozen=True, slots=True)
class Level:
    """مستوًى في السُّلَّم: اسمُه، وجردُه إن كان مغلقًا، وإلّا فهو مفتوح."""

    name: str
    inventory: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise BridgeError("مستوًى بلا اسمٍ لا يُبنى عليه جسر.")
        if self.inventory is not None:
            if not self.inventory:
                raise BridgeError(
                    "جردٌ خالٍ ليس انغلاقًا؛ ومستوًى بلا جردٍ يُعلَن مفتوحًا "
                    "(A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN)."
                )
            if len(set(self.inventory)) != len(self.inventory):
                raise BridgeError("جردٌ يكرّر عنصرًا ليس جردًا.")

    @property
    def is_closed(self) -> bool:
        """أمغلقٌ هذا المستوى؟ ولا يكون كذلك إلّا بجردٍ مسرود."""

        return self.inventory is not None

    @property
    def size(self) -> int:
        """حجمُ الجرد؛ ويُرَدّ على مستوًى مفتوح."""

        if self.inventory is None:
            raise BridgeError(f"«{self.name}» مفتوحٌ فلا حجمَ لجرده.")
        return len(self.inventory)


@dataclass(frozen=True, slots=True)
class Bridge:
    """جسرٌ بين مستويين: مبنيٌّ، أو ينتظر أوراكلَ مُسمًّى."""

    name: str
    source: Level
    target: Level
    oracle: str | None = None
    refusal_kinds: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise BridgeError("جسرٌ بلا اسمٍ لا يُحاسَب.")
        if self.oracle is not None and not self.oracle.strip():
            raise BridgeError(
                "جسرٌ غيرُ مبنيٍّ يُسمّي أوراكلَه " "(AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE)."
            )
        if len(set(self.refusal_kinds)) != len(self.refusal_kinds):
            raise BridgeError("أصنافُ الردّ تُسمّى أسماءً مميَّزة.")

    @property
    def is_built(self) -> bool:
        """أمبنيٌّ هو؟ والمبنيُّ ما لا ينتظر معطًى من خارج."""

        return self.oracle is None


@dataclass(frozen=True, slots=True)
class Crossing:
    """عبورٌ موزون: ما دخل، وما خرج، وما رُدَّ بأصنافه المُسمّاة."""

    bridge: str
    given: int
    mapped: int
    refused: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        if self.given < 0 or self.mapped < 0:
            raise BridgeError("عددٌ سالبٌ ليس عبورًا.")
        for reason, count in self.refused:
            if not reason.strip():
                raise BridgeError("المردودُ يُسمّى سببُه (A_REFUSAL_IS_NAMED_NOT_COUNTED).")
            if count < 0:
                raise BridgeError("عددٌ سالبٌ ليس ردًّا.")
        reasons = [reason for reason, _ in self.refused]
        if len(set(reasons)) != len(reasons):
            raise BridgeError("أسبابُ الردّ لا تتكرّر في عبورٍ واحد.")
        if self.mapped + self.refused_total != self.given:
            raise BridgeError(
                f"عبورُ «{self.bridge}» لا يوازن: دخل {self.given}، وخرج "
                f"{self.mapped}، ورُدَّ {self.refused_total} — والفرقُ "
                f"{self.given - self.mapped - self.refused_total} ساقطٌ صمتًا "
                "(A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE)."
            )

    @property
    def refused_total(self) -> int:
        """مجموعُ المردود بأصنافه."""

        return sum(count for _, count in self.refused)

    @property
    def balances(self) -> bool:
        """أتوازن؟ وهي موازنةٌ دائمًا لأنّ عدمَها يُرَدّ في الإنشاء."""

        return self.mapped + self.refused_total == self.given


@dataclass(frozen=True, slots=True)
class Ladder:
    """سُلَّمٌ متّصلٌ من جسور: يُفحَص اتّصالُه، ويُفصَل المبنيُّ عن المبلوغ."""

    bridges: tuple[Bridge, ...]

    def __post_init__(self) -> None:
        if not self.bridges:
            raise BridgeError("سُلَّمٌ بلا جسورٍ ليس سُلَّمًا.")
        names = [bridge.name for bridge in self.bridges]
        if len(set(names)) != len(names):
            raise BridgeError("الجسورُ تُسمّى أسماءً مميَّزة.")
        for earlier, later in zip(self.bridges, self.bridges[1:], strict=False):
            if earlier.target != later.source:
                raise BridgeError(
                    f"فجوةٌ بين «{earlier.name}» و«{later.name}»: "
                    f"ينتهي عند «{earlier.target.name}» ويبدأ من "
                    f"«{later.source.name}» (A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER)."
                )

    @property
    def levels(self) -> tuple[Level, ...]:
        """المستوياتُ بترتيبها، مُشتَقّةً من الجسور لا مكتوبةً إلى جانبها."""

        return (self.bridges[0].source, *(bridge.target for bridge in self.bridges))

    @property
    def built(self) -> tuple[Bridge, ...]:
        """الجسورُ المبنيّة."""

        return tuple(bridge for bridge in self.bridges if bridge.is_built)

    @property
    def unbuilt(self) -> tuple[Bridge, ...]:
        """الجسورُ التي تنتظر أوراكلَ."""

        return tuple(bridge for bridge in self.bridges if not bridge.is_built)

    def oracles_required(self) -> tuple[str, ...]:
        """الأوراكلاتُ المطلوبةُ مُسمّاةً، بلا تكرار."""

        seen: list[str] = []
        for bridge in self.unbuilt:
            assert bridge.oracle is not None
            if bridge.oracle not in seen:
                seen.append(bridge.oracle)
        return tuple(seen)

    def reachable_levels(self) -> tuple[Level, ...]:
        """ما يُبلَغ من الأسفل فعلًا: يقف السيرُ عند أوّل جسرٍ غيرِ مبنيّ.

        فـ«مبنيٌّ» غيرُ «مبلوغ»: جسرٌ صحيحٌ فوق فجوةٍ لا يُوصَل إليه.
        """

        reached = [self.bridges[0].source]
        for bridge in self.bridges:
            if not bridge.is_built:
                break
            reached.append(bridge.target)
        return tuple(reached)

    @property
    def first_gap(self) -> Bridge | None:
        """أوّلُ جسرٍ غيرِ مبنيٍّ يقف عنده السيرُ من الأسفل."""

        for bridge in self.bridges:
            if not bridge.is_built:
                return bridge
        return None

    @property
    def is_traversable(self) -> bool:
        """أيُبلَغ أعلى السُّلَّم من أسفله بلا معطًى من خارج؟"""

        return self.first_gap is None

    def built_but_unreached(self) -> tuple[Bridge, ...]:
        """جسورٌ مبنيّةٌ لكنّها فوق الفجوة — والفرقُ يُعلَن ولا يُطوى."""

        reached = set(self.reachable_levels())
        return tuple(
            bridge
            for bridge in self.bridges
            if bridge.is_built and bridge.source not in reached
        )


A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE_NOTE: Final[str] = (
    "ABridgeThatDropsSilentlyIsALie: دخل = خرج + رُدّ شرطُ إنشاءٍ لا نصيحة؛ "
    "وجسرٌ يعطي أقلَّ ممّا أخذ بلا بيانٍ مردودٌ عبورُه كلُّه"
)

A_REFUSAL_IS_NAMED_NOT_COUNTED_NOTE: Final[str] = (
    "ARefusalIsNamedNotCounted: المردودُ يُسمّى سببُه ويُعَدّ به؛ وجمعُه في "
    "رقمٍ واحدٍ يخفي أنّ بعضَه عيبُ أداةٍ وبعضَه خبرٌ عن اللغة"
)

AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE_NOTE: Final[str] = (
    "AnUnbuiltBridgeNamesItsOracle: مستوًى لا يُبلَغ بلا معطًى من خارجٍ يقول "
    "أيَّ معطًى؛ و«يحتاج معجمًا» بلا تسميةٍ ليس إعلانًا"
)

A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER_NOTE: Final[str] = (
    "ALadderWithAGapIsNotALadder: الجسورُ تتّصل طرفًا بطرف، و«مبنيٌّ» غيرُ "
    "«مبلوغ»: جسرٌ صحيحٌ فوق فجوةٍ لا يُوصَل إليه من الأسفل"
)

A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN_NOTE: Final[str] = (
    "AClosedInventoryIsStatedOrTheLevelIsOpen: مستوًى يُدَّعى انغلاقُه يسرد "
    "جردَه، وما لم يُسرَد فهو مفتوحٌ حكمًا"
)

BRIDGE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE_NOTE,
    A_REFUSAL_IS_NAMED_NOT_COUNTED_NOTE,
    AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE_NOTE,
    A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER_NOTE,
    A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
