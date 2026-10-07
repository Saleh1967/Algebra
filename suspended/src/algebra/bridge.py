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

`A_BINARY_STANDING_HAS_NO_CELL_FOR_A_TAUGHT_CROSSING`: كان «مبنيّ» ثنائيًّا:
مبنيٌّ إن لم يكن له أوراكل، وإلّا فلا. ولا خانةَ للحال التي تقع فعلًا — **جسرٌ
يحتاج الأوراكلَ مرّةً ليُدرَّب، ثمّ يعبُر المحجوبَ بدونه بنسبةٍ مُعلَنة**. فليس
مبنيًّا (احتاج معطًى من خارج) ولا غيرَ مبنيٍّ (يعبُر على ما لم يرَ). فصارت
المواقفُ أربعةً: مبنيٌّ، ومتعلَّمٌ بنسبة، ومنتظِرٌ، **ومردودٌ بسببٍ مقيس**.

`A_REFUSAL_IS_A_RESULT_NOT_A_WAIT`: جسرٌ أوراكلُه المُسمّى **اختُبِر فسقط** ليس
منتظِرًا؛ فوسمُه انتظارًا يُخفي قياسًا جرى. وهو موقفٌ رابعٌ يُسمّى بمن أسقطه.

`A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT`: نسبةُ عبورٍ بلا صفريٍّ **مُسمّى
الأساس** رقمٌ لا يُقارَن. ومستوًى مفتوحُ الجرد لا يُشتَقّ منه انتظامٌ، فجسرٌ
غايتُه مفتوحةٌ لا يُودَع متعلَّمًا حتّى يُعلَن صفريُّه من خارج الجرد.

`BUILT_IS_NOT_CROSSED`: و«مبنيّ» ههنا تعني «لا ينتظر معطًى»، ولا تعني «جرى
عبورُه». فجسرٌ لا أوراكلَ له ولا عبورَ مسجَّلًا يُعَدّ مبنيًّا وهو **فارغ**؛
فيُفرَد عدُّه ولا يُخلَط بمن عبَر.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

__all__ = [
    "AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE_NOTE",
    "A_BINARY_STANDING_HAS_NO_CELL_FOR_A_TAUGHT_CROSSING_NOTE",
    "A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE_NOTE",
    "A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN_NOTE",
    "A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER_NOTE",
    "A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT_NOTE",
    "A_REFUSAL_IS_A_RESULT_NOT_A_WAIT_NOTE",
    "A_REFUSAL_IS_NAMED_NOT_COUNTED_NOTE",
    "BRIDGE_NAMED_RESIDUALS",
    "BUILT_IS_NOT_CROSSED_NOTE",
    "Bridge",
    "BridgeError",
    "BridgeStanding",
    "Crossing",
    "Ladder",
    "Level",
    "Segment",
    "Taught",
    "uniform_null",
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


def uniform_null(level: Level) -> Fraction:
    """الانتظامُ على جردٍ **مغلق**؛ ومستوًى مفتوحٌ لا يُشتَقّ منه صفريّ.

    فهذا هو الصفريُّ الوحيدُ الذي يلزم من السُّلَّم نفسِه بلا قياسٍ خارجه. وما
    عداه يُجلَب ويُسمّى أساسُه، ولا يُقدَّر ههنا.
    """

    if level.inventory is None:
        raise BridgeError(
            f"«{level.name}» مفتوحُ الجرد، فلا انتظامَ يُشتَقّ منه؛ والصفريُّ "
            "يُجلَب ويُسمّى أساسُه (A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT)."
        )
    return Fraction(1, level.size)


class BridgeStanding(Enum):
    """مواقفُ الجسر الأربعة؛ مفردةٌ مغلقةٌ لا يُقرَأ خارجُها انتظارًا."""

    BUILT = "مبنيّ"
    LEARNED = "متعلَّمٌ بنسبةٍ مقيسة"
    AWAITING = "ينتظر أوراكلًا مُسمًّى"
    REFUTED = "أوراكلُه مُختبَرٌ وساقط"


@dataclass(frozen=True, slots=True)
class Taught:
    """عبورٌ متعلَّم: مُعلِّمٌ يُسمّى، ومحجوبٌ يُعَدّ، وصفريٌّ يُسمّى أساسُه.

    والأوراكلُ ههنا **دخل مرّةً** في التدريب ولم يدخل في المحجوب؛ فالنسبةُ
    نسبةُ عبورٍ على ما لم يُرَ، لا نسبةُ مطابقةٍ لجدولٍ حُفِظ.
    """

    teacher: str
    held_out: int
    matched: int
    null: Fraction
    null_basis: str

    def __post_init__(self) -> None:
        if not self.teacher.strip():
            raise BridgeError("العبورُ المتعلَّمُ يُسمّي مُعلِّمَه؛ وبلا اسمٍ لا يُراجَع.")
        if self.held_out <= 0:
            raise BridgeError("مقامٌ خالٍ ليس محجوبًا؛ والنسبةُ بلا مقامٍ ليست نسبة.")
        if not 0 <= self.matched <= self.held_out:
            raise BridgeError(
                f"المطابقُ {self.matched} والمحجوبُ {self.held_out}؛ "
                "ولا يعبُر أكثرُ ممّا حُجِب."
            )
        if not Fraction(0) < self.null < Fraction(1):
            raise BridgeError("صفريٌّ خارجَ الوحدة المفتوحة ليس صفريًّا.")
        if not self.null_basis.strip():
            raise BridgeError(
                "الصفريُّ يُسمّى أساسُه — «انتظامٌ على جردٍ مغلق» أو غيرُه — "
                "وإلّا فالنسبةُ لا تُقارَن "
                "(A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT)."
            )

    @property
    def rate(self) -> Fraction:
        """نسبةُ العبور على المحجوب، كسرًا مضبوطًا."""

        return Fraction(self.matched, self.held_out)

    @property
    def lift(self) -> Fraction:
        """النسبةُ إلى صفريِّها؛ وهي ما يُقرَأ لا النسبةُ وحدَها."""

        return self.rate / self.null


@dataclass(frozen=True, slots=True)
class Bridge:
    """جسرٌ بين مستويين: مبنيٌّ، أو متعلَّمٌ بنسبة، أو منتظِرٌ، أو مردودٌ بقياس."""

    name: str
    source: Level
    target: Level
    oracle: str | None = None
    refusal_kinds: tuple[str, ...] = ()
    taught: Taught | None = None
    refuted_by: str | None = None
    verification: Crossing | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise BridgeError("جسرٌ بلا اسمٍ لا يُحاسَب.")
        if self.oracle is not None and not self.oracle.strip():
            raise BridgeError(
                "جسرٌ غيرُ مبنيٍّ يُسمّي أوراكلَه (AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE)."
            )
        if len(set(self.refusal_kinds)) != len(self.refusal_kinds):
            raise BridgeError("أصنافُ الردّ تُسمّى أسماءً مميَّزة.")
        if self.taught is not None and self.refuted_by is not None:
            raise BridgeError(
                f"«{self.name}» متعلَّمٌ ومردودٌ معًا؛ وأوراكلٌ أسقطه اختبارٌ "
                "لا يُدرَّب عليه بعدَه."
            )
        if self.taught is not None and self.oracle is None:
            raise BridgeError(
                f"«{self.name}» متعلَّمٌ بلا أوراكلَ مُسمًّى؛ والذي دُرِّب عليه "
                "مرّةً يُسمّى ولا يُطوى بدعوى أنّه لم يُستعمَل في المحجوب."
            )
        if self.refuted_by is not None:
            if self.oracle is None:
                raise BridgeError(
                    f"«{self.name}» مردودٌ بلا أوراكلَ مُسمًّى؛ ولا يسقط ما لم يُسَمَّ."
                )
            if not self.refuted_by.strip():
                raise BridgeError("الردُّ يُسمّى مُسقِطَه (A_REFUSAL_IS_A_RESULT_NOT_A_WAIT).")
        if self.verification is not None and self.verification.bridge != self.name:
            raise BridgeError(
                f"عبورٌ باسم «{self.verification.bridge}» مُودَعٌ في «{self.name}»؛ "
                "وشاهدُ جسرٍ لا يُحتسَب لغيره."
            )

    @property
    def is_built(self) -> bool:
        """أمبنيٌّ هو؟ والمبنيُّ ما لا ينتظر معطًى من خارج — ولا يعني أنّه عُبِر."""

        return self.oracle is None

    @property
    def standing(self) -> BridgeStanding:
        """موقفُ الجسر، مُشتَقًّا من مكوّناته لا مكتوبًا إلى جانبها."""

        if self.refuted_by is not None:
            return BridgeStanding.REFUTED
        if self.taught is not None:
            return BridgeStanding.LEARNED
        if self.oracle is None:
            return BridgeStanding.BUILT
        return BridgeStanding.AWAITING

    @property
    def crossing_rate(self) -> Fraction:
        """احتمالُ العبور: واحدٌ للمبنيّ، والنسبةُ للمتعلَّم، وصفرٌ لما سواهما."""

        if self.standing is BridgeStanding.BUILT:
            return Fraction(1)
        if self.taught is not None:
            return self.taught.rate
        return Fraction(0)

    @property
    def is_crossable(self) -> bool:
        """أيُعبَر من الأسفل باحتمالٍ موجب؟"""

        return self.crossing_rate > 0


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
        """الأوراكلاتُ **المطلوبةُ** مُسمّاةً، بلا تكرار.

        ولا يُعَدّ منها ما سقط: أوراكلٌ اختُبِر فردَّه القياسُ ليس مطلوبًا بل
        **مُنفَقًا** (A_REFUSAL_IS_A_RESULT_NOT_A_WAIT). وكذلك ما دُرِّب عليه
        مرّةً ثمّ عبَر المحجوبَ بدونه؛ فطلبُه انقضى وبقي أثرُه في النسبة.
        """

        seen: list[str] = []
        for bridge in self.bridges:
            if bridge.standing is not BridgeStanding.AWAITING:
                continue
            assert bridge.oracle is not None
            if bridge.oracle not in seen:
                seen.append(bridge.oracle)
        return tuple(seen)

    def oracles_spent(self) -> tuple[tuple[str, str], ...]:
        """الأوراكلاتُ التي اختُبِرت فسقطت، ومُسقِطُ كلٍّ منها."""

        return tuple(
            (bridge.oracle, bridge.refuted_by)
            for bridge in self.bridges
            if bridge.standing is BridgeStanding.REFUTED
            and bridge.oracle is not None
            and bridge.refuted_by is not None
        )

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

    def built_but_never_crossed(self) -> tuple[Bridge, ...]:
        """مبنيٌّ ولا عبورَ مسجَّلًا له — فارغٌ يُعَدّ وحدَه (BUILT_IS_NOT_CROSSED)."""

        return tuple(
            bridge
            for bridge in self.bridges
            if bridge.standing is BridgeStanding.BUILT and bridge.verification is None
        )

    def standings(self) -> dict[BridgeStanding, int]:
        """عددُ الجسور بكلّ موقف؛ والأربعةُ تُعَدّ كلُّها ولو كان بعضُها صفرًا."""

        counts = {standing: 0 for standing in BridgeStanding}
        for bridge in self.bridges:
            counts[bridge.standing] += 1
        return counts

    def reach_profile(self) -> tuple[tuple[Level, Fraction], ...]:
        """البلوغُ **باحتمالٍ متراكم** من الأسفل، لا بلوغًا ثنائيًّا.

        فالمبنيُّ يضرب في واحد، والمتعلَّمُ في نسبته، والسيرُ يقف عند أوّل جسرٍ
        لا يُعبَر. وهو الوصفُ الصادق لما في اليد: طريقٌ موصولٌ **باحتمال**، لا
        ممهَّدٌ ولا مقطوع.
        """

        profile = [(self.bridges[0].source, Fraction(1))]
        running = Fraction(1)
        for bridge in self.bridges:
            if not bridge.is_crossable:
                break
            running *= bridge.crossing_rate
            profile.append((bridge.target, running))
        return tuple(profile)

    def segments(self) -> tuple[Segment, ...]:
        """قطعُ السُّلَّم المتّصلة، ولكلِّ قطعةٍ احتمالُ عبورها ومن قطعها بعدها.

        فالسُّلَّمُ لا يُقال «مقطوع» ولا «ممهَّد»، بل **مقطوعٌ بنسبة**: قطعٌ
        تُعبَر باحتمالٍ مقيس، يفصل بينها جسورٌ تُسمّى.
        """

        found: list[Segment] = []
        run: list[Bridge] = []
        for bridge in self.bridges:
            if bridge.is_crossable:
                run.append(bridge)
                continue
            if run:
                found.append(Segment(bridges=tuple(run), severed_by=bridge.name))
                run = []
            else:
                found.append(Segment(bridges=(), severed_by=bridge.name))
        if run:
            found.append(Segment(bridges=tuple(run), severed_by=None))
        return tuple(found)


@dataclass(frozen=True, slots=True)
class Segment:
    """قطعةٌ متّصلةٌ من السُّلَّم: جسورُها، واحتمالُ عبورها، ومن قطعها بعدها."""

    bridges: tuple[Bridge, ...]
    severed_by: str | None

    def __post_init__(self) -> None:
        for bridge in self.bridges:
            if not bridge.is_crossable:
                raise BridgeError(
                    f"«{bridge.name}» غيرُ مقطوعِ العبورِ فلا يدخل قطعةً متّصلة."
                )

    @property
    def rate(self) -> Fraction:
        """حاصلُ ضربِ احتمالات جسورها؛ وقطعةٌ خاليةٌ احتمالُها واحدٌ لا صفر."""

        running = Fraction(1)
        for bridge in self.bridges:
            running *= bridge.crossing_rate
        return running

    @property
    def is_empty(self) -> bool:
        """أقطعةٌ بلا جسر؟ وهي ما يقع بين قاطعَين متجاورَين."""

        return not self.bridges


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

A_BINARY_STANDING_HAS_NO_CELL_FOR_A_TAUGHT_CROSSING_NOTE: Final[str] = (
    "ABinaryStandingHasNoCellForATaughtCrossing: جسرٌ يحتاج الأوراكلَ مرّةً "
    "ليُدرَّب ثمّ يعبُر المحجوبَ بدونه ليس مبنيًّا ولا غيرَ مبنيّ؛ فالمواقفُ "
    "أربعةٌ لا اثنان"
)

A_REFUSAL_IS_A_RESULT_NOT_A_WAIT_NOTE: Final[str] = (
    "ARefusalIsAResultNotAWait: أوراكلٌ مُسمًّى اختُبِر فسقط يُوسَم مردودًا "
    "بمن أسقطه؛ ووسمُه انتظارًا يُخفي قياسًا جرى"
)

A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT_NOTE: Final[str] = (
    "ARateWithoutANamedNullIsNotAResult: نسبةُ عبورٍ بلا صفريٍّ مُسمّى الأساس "
    "رقمٌ لا يُقارَن؛ ومستوًى مفتوحُ الجرد لا يُشتَقّ منه انتظام"
)

BUILT_IS_NOT_CROSSED_NOTE: Final[str] = (
    "BuiltIsNotCrossed: «مبنيّ» تعني لا ينتظر معطًى، ولا تعني جرى عبورُه؛ "
    "فجسرٌ بلا أوراكلَ ولا عبورٍ مسجَّلٍ مبنيٌّ وفارغٌ معًا"
)

BRIDGE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_BRIDGE_THAT_DROPS_SILENTLY_IS_A_LIE_NOTE,
    A_REFUSAL_IS_NAMED_NOT_COUNTED_NOTE,
    AN_UNBUILT_BRIDGE_NAMES_ITS_ORACLE_NOTE,
    A_LADDER_WITH_A_GAP_IS_NOT_A_LADDER_NOTE,
    A_CLOSED_INVENTORY_IS_STATED_OR_THE_LEVEL_IS_OPEN_NOTE,
    A_BINARY_STANDING_HAS_NO_CELL_FOR_A_TAUGHT_CROSSING_NOTE,
    A_REFUSAL_IS_A_RESULT_NOT_A_WAIT_NOTE,
    A_RATE_WITHOUT_A_NAMED_NULL_IS_NOT_A_RESULT_NOTE,
    BUILT_IS_NOT_CROSSED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
