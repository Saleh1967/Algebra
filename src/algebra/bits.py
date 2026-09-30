"""نواةُ البتّات — **عددٌ يُقرَأ من بايتاته**، وعمليّةٌ تردّ جوابَها وثمنَها.

**ما ليس ههنا**: لا عائمٌ ولا `int.bit_length` ولا `bin(…)`. فدالّةٌ مبنيّةٌ
في المفسّر تُعطي الجوابَ ولا تُعطي **أثرَه**، ومن أخذ الجوابَ بلا أثرٍ أخذ
رقمًا لا يُعاد التحقّقُ منه.

**وما ههنا**: `Bits` بتّاتٌ صريحةٌ بترتيبٍ واحد (الأثقلُ أوّلًا، ولا بتّةَ
صفرٍ في الصدر)، وأربعُ عمليّاتٍ **مُعرَّفةٍ بتّةً بتّة**: الجمعُ بحمل،
والضربُ بإزاحةٍ وجمع، والقسمةُ بطرحٍ مُزاح، والمقارنةُ من الصدر. وكلُّ
عمليّةٍ تردّ `Work`: القيمةَ، و**أثرَ الخطوات**، و**ثمنَها بالبتّات**.

`A_COST_THAT_IS_NOT_COUNTED_IS_AN_ESTIMATE`: الثمنُ ههنا **معدودٌ في
الخطوات** لا مُقدَّرٌ بصيغة. فكلُّ خطوةٍ تُعلِن كم بتّةً نظرت فيها،
و`Work.cost` مجموعُها — ومن كتب الثمنَ بصيغةٍ مغلقةٍ كتب **دعوى ثانيةً**
تحتاج برهانَها.

`THE_TRACE_IS_THE_ANSWER_NOT_ITS_COMMENTARY`: الأثرُ **معطًى قابلٌ لإعادة
الفحص** من خارج هذه الوحدة، لا شرحًا لها. وما لا يُعاد فحصُه من أثره
**ليس مبرهَنًا ههنا**، وإن كان صحيحًا.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE`: بايتاتٌ وأعدادٌ صحيحةٌ
فقط؛ ولا دعوى ههنا على العربيّة ولا على غيرها.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "A_COST_THAT_IS_NOT_COUNTED_IS_AN_ESTIMATE_NOTE",
    "BYTE_WIDTH",
    "Bits",
    "BitsError",
    "Step",
    "THE_TRACE_IS_THE_ANSWER_NOT_ITS_COMMENTARY_NOTE",
    "THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE",
    "Work",
    "add",
    "compare",
    "divide",
    "multiply",
    "read_bytes",
]

BYTE_WIDTH: Final[int] = 8
"""عرضُ البايتة بتّاتٍ — مُعلَنٌ لأنّه يدخل عدَّ الثمن."""

THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE: Final[str] = (
    "بايتاتٌ وأعدادٌ صحيحة؛ ولا دعوى ههنا على لغةٍ ولا على معنى"
)


class BitsError(ValueError):
    """رُفض بتٌّ أو خطوةٌ أو عمليّةٌ لا تصحّ؛ ولا تُحمَل على أقرب مقبول."""


@dataclass(frozen=True, slots=True)
class Bits:
    """عددٌ بتّاتٍ صريحة: الأثقلُ أوّلًا، **ولا صفرَ في الصدر**.

    والصفرُ `Bits(())` — لا بتّةَ له، وذلك حكمٌ لا اصطلاح: عدَدٌ لا يحتاج
    بتّةً واحدةً ليُمَيَّز من نفسه.
    """

    digits: tuple[int, ...]

    def __post_init__(self) -> None:
        for one in self.digits:
            if one not in (0, 1):
                raise BitsError(f"ما ليس بتًّا لا يدخل: {one!r}")
        if self.digits and self.digits[0] == 0:
            raise BitsError("صفرٌ في الصدر — والصورةُ واحدةٌ لا صورتان.")

    @property
    def width(self) -> int:
        """كم بتّةً يكلّف هذا العدد — **معدودةً لا محسوبةً بصيغة**."""

        return len(self.digits)

    @property
    def written(self) -> str:
        """صورتُه المكتوبة؛ والصفرُ يُكتَب `-` لأنّه بلا بتّة."""

        return "".join(str(one) for one in self.digits) if self.digits else "-"

    @property
    def number(self) -> int:
        """قيمتُه عددًا صحيحًا — **مبنيّةً بتّةً بتّة** لا بدالّةٍ مبنيّة."""

        total = 0
        for one in self.digits:
            total = total + total + one
        return total

    @classmethod
    def of(cls, number: int) -> Bits:
        """بتّاتُ عددٍ صحيحٍ غيرِ سالب، **مشتقّةً بالقسمة على اثنين**."""

        if number < 0:
            raise BitsError("السالبُ لا بتّاتِ له ههنا؛ والإشارةُ تُمثَّل صراحةً.")
        found: list[int] = []
        left = number
        while left:
            left, one = divmod(left, 2)
            found.append(one)
        return cls(tuple(reversed(found)))


@dataclass(frozen=True, slots=True)
class Step:
    """خطوةٌ واحدةٌ من الأثر: اسمُها ومُدخَلاتُها ومخرَجُها وما نظرت فيه."""

    operation: str
    inputs: tuple[str, ...]
    output: str
    bits: int

    def __post_init__(self) -> None:
        if not self.operation.strip():
            raise BitsError("خطوةٌ بلا اسمٍ لا تُعاد.")
        if not self.inputs:
            raise BitsError("خطوةٌ بلا مُدخَلٍ لا تُفحَص.")
        if not self.output.strip():
            raise BitsError("خطوةٌ بلا مخرَجٍ لا تُقابَل.")
        if self.bits < 0:
            raise BitsError("ثمنٌ سالبٌ ليس ثمنًا.")

    @property
    def line(self) -> str:
        """سطرُ الخطوة كما يُكتَب في السجلّ ويُقرَأ منه؛ ولا يُعاد ترتيبُه."""

        return f"{self.operation}|{','.join(self.inputs)}|{self.output}|{self.bits}"


@dataclass(frozen=True, slots=True)
class Work:
    """عملٌ تَمّ: قيمُه، وإشارتُه إن كانت مقارنةً، وأثرُه، وثمنُه معدودًا."""

    values: tuple[Bits, ...]
    sign: int | None
    steps: tuple[Step, ...]

    def __post_init__(self) -> None:
        if not self.steps:
            raise BitsError("عملٌ بلا أثرٍ لا يُعاد التحقّقُ منه.")
        if self.sign is not None and self.sign not in (-1, 0, 1):
            raise BitsError(f"إشارةٌ ليست من (−١، ٠، +١): {self.sign!r}")
        if not self.values and self.sign is None:
            raise BitsError("عملٌ بلا قيمةٍ ولا إشارةٍ لم يُخبر بشيء.")

    @property
    def cost(self) -> int:
        """ثمنُه بالبتّات — **مجموعُ ما نظرت فيه خطواتُه**، لا صيغةٌ مغلقة."""

        return sum(one.bits for one in self.steps)


def _trimmed(digits: list[int]) -> tuple[int, ...]:
    """احذف أصفارَ الصدر — والصورةُ الواحدةُ شرطُ المقابلة بتًّا ببت."""

    first = 0
    while first < len(digits) and digits[first] == 0:
        first += 1
    return tuple(digits[first:])


def read_bytes(raw: bytes) -> Work:
    """اقرأ بايتاتٍ بتّةً بتّة — **والقراءةُ نفسُها تُعَدّ ثمنًا**.

    كلُّ بايتةٍ تُفَكّ إلى ثماني بتّاتٍ بالقسمة على اثنين، ثمّ تُحذَف أصفارُ
    الصدر في خطوةٍ **تُعلَن** لا تُطوى — فحذفُ صفرٍ قرارٌ يُراجَع.
    """

    if not raw:
        raise BitsError("لا بتّاتِ لبايتاتٍ خالية.")
    steps: list[Step] = []
    spread: list[int] = []
    for index, one in enumerate(raw):
        eight: list[int] = []
        left = one
        for _ in range(BYTE_WIDTH):
            left, bit = divmod(left, 2)
            eight.append(bit)
        eight.reverse()
        spread.extend(eight)
        steps.append(
            Step(
                operation="بايتة",
                inputs=(str(index), str(one)),
                output="".join(str(two) for two in eight),
                bits=BYTE_WIDTH,
            )
        )
    kept = _trimmed(spread)
    steps.append(
        Step(
            operation="حذفُ الصدر",
            inputs=("".join(str(one) for one in spread),),
            output="".join(str(one) for one in kept) if kept else "-",
            bits=len(spread),
        )
    )
    return Work(values=(Bits(kept),), sign=None, steps=tuple(steps))


def compare(first: Bits, second: Bits) -> Work:
    """قابِل عددين من الصدر: الأعرضُ أكبرُ، وعند التساوي أوّلُ اختلاف."""

    steps: list[Step] = []
    if first.width != second.width:
        sign = 1 if first.width > second.width else -1
        steps.append(
            Step(
                operation="عرضٌ",
                inputs=(first.written, second.written),
                output=str(sign),
                bits=first.width + second.width,
            )
        )
        return Work(values=(), sign=sign, steps=tuple(steps))
    looked = 0
    for one, two in zip(first.digits, second.digits, strict=True):
        looked += 2
        if one != two:
            sign = 1 if one > two else -1
            steps.append(
                Step(
                    operation="أوّلُ اختلاف",
                    inputs=(first.written, second.written),
                    output=str(sign),
                    bits=looked,
                )
            )
            return Work(values=(), sign=sign, steps=tuple(steps))
    steps.append(
        Step(
            operation="سواء",
            inputs=(first.written, second.written),
            output="0",
            bits=max(looked, 1),
        )
    )
    return Work(values=(), sign=0, steps=tuple(steps))


def add(first: Bits, second: Bits) -> Work:
    """اجمع بحملٍ من الذيل — خطوةٌ لكلّ منزلة، وثمنُها بتّتان وحملُها."""

    steps: list[Step] = []
    wide = max(first.width, second.width)
    left = list(reversed(first.digits))
    right = list(reversed(second.digits))
    carry = 0
    found: list[int] = []
    for place in range(wide):
        one = left[place] if place < len(left) else 0
        two = right[place] if place < len(right) else 0
        total = one + two + carry
        carry, digit = divmod(total, 2)
        found.append(digit)
        steps.append(
            Step(
                operation="منزلةٌ",
                inputs=(str(place), str(one), str(two)),
                output=f"{digit}{carry}",
                bits=3,
            )
        )
    if carry:
        found.append(carry)
        steps.append(
            Step(
                operation="حملٌ أخير",
                inputs=(str(wide),),
                output=str(carry),
                bits=1,
            )
        )
    found.reverse()
    return Work(values=(Bits(_trimmed(found)),), sign=None, steps=tuple(steps))


def multiply(first: Bits, second: Bits) -> Work:
    """اضرب بإزاحةٍ وجمع — بتّةُ الضارب الواحدةُ إمّا تُزيح وإمّا تُهمَل."""

    steps: list[Step] = []
    total = Bits(())
    for place, one in enumerate(reversed(second.digits)):
        if one == 0:
            steps.append(
                Step(
                    operation="إهمالٌ",
                    inputs=(str(place), "0"),
                    output=total.written,
                    bits=1,
                )
            )
            continue
        shifted = Bits(first.digits + (0,) * place) if first.digits else Bits(())
        done = add(total, shifted)
        total = done.values[0]
        steps.append(
            Step(
                operation="إزاحةٌ وجمع",
                inputs=(str(place), shifted.written),
                output=total.written,
                bits=1 + done.cost,
            )
        )
    if not steps:
        steps.append(
            Step(
                operation="ضاربٌ بلا بتّة",
                inputs=(first.written,),
                output="-",
                bits=1,
            )
        )
    return Work(values=(total,), sign=None, steps=tuple(steps))


def divide(first: Bits, second: Bits) -> Work:
    """اقسم بطرحٍ مُزاح — بتّةً بتّة من الصدر، والباقي يُردّ مع الخارج.

    والقسمةُ على صفرٍ **تُرَدّ** ولا تُعطى قيمةً تُقرَأ بعدُ خطأً.
    """

    if not second.digits:
        raise BitsError("القسمةُ على صفرٍ مردودةٌ، ولا يُخترَع لها خارج.")
    steps: list[Step] = []
    carried: list[int] = []
    found: list[int] = []
    for place, one in enumerate(first.digits):
        carried.append(one)
        rest = Bits(_trimmed(carried))
        seen = compare(rest, second)
        if seen.sign is not None and seen.sign >= 0:
            back = _subtract(rest, second)
            carried = list(back.digits)
            found.append(1)
        else:
            found.append(0)
        steps.append(
            Step(
                operation="طرحٌ مُزاح",
                inputs=(str(place), rest.written),
                output=f"{found[-1]}{Bits(_trimmed(carried)).written}",
                bits=1 + seen.cost,
            )
        )
    if not steps:
        steps.append(
            Step(
                operation="مقسومٌ بلا بتّة",
                inputs=(second.written,),
                output="-",
                bits=1,
            )
        )
    return Work(
        values=(Bits(_trimmed(found)), Bits(_trimmed(carried))),
        sign=None,
        steps=tuple(steps),
    )


def _subtract(first: Bits, second: Bits) -> Bits:
    """طرحٌ باستلافٍ، داخليٌّ للقسمة؛ ويُرَدّ إن كان المطروحُ أكبر."""

    seen = compare(first, second)
    if seen.sign is not None and seen.sign < 0:
        raise BitsError("الطرحُ ههنا لا ينزل تحت الصفر.")
    left = list(reversed(first.digits))
    right = list(reversed(second.digits))
    borrow = 0
    found: list[int] = []
    for place in range(len(left)):
        one = left[place]
        two = right[place] if place < len(right) else 0
        value = one - two - borrow
        borrow = 1 if value < 0 else 0
        found.append(value + 2 * borrow)
    found.reverse()
    return Bits(_trimmed(found))


A_COST_THAT_IS_NOT_COUNTED_IS_AN_ESTIMATE_NOTE: Final[str] = (
    "ACostThatIsNotCountedIsAnEstimate: الثمنُ معدودٌ في الخطوات لا مُقدَّرٌ "
    "بصيغة؛ ومن كتب الثمنَ بصيغةٍ مغلقةٍ كتب دعوى ثانيةً تحتاج برهانَها"
)

THE_TRACE_IS_THE_ANSWER_NOT_ITS_COMMENTARY_NOTE: Final[str] = (
    "TheTraceIsTheAnswerNotItsCommentary: الأثرُ معطًى يُعاد فحصُه من خارج "
    "هذه الوحدة لا شرحًا لها؛ وما لا يُعاد فحصُه من أثره ليس مبرهَنًا ههنا"
)
