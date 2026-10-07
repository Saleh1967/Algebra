"""مِرمازٌ ثنائيٌّ تامٌّ للوحدة المشكولة: ثمانيةُ بتّاتٍ تُعيّن حرفًا وعلامتَه.

**لمَ هذه الوحدة وقد سبقتها وحدتان**: محورُ المخرج يحمل معنًى ولا يُعيّن —
أربعةُ بتّاتٍ تُخرِج خانةً فيها إلى ثلاثة حروف، وحسمُها يحتاج جدولَ صفةٍ
حاجزُه قائم. وهذه الوحدةُ تقلب المقايضة: محورُ **هُويّة** يُعيّن ولا يحمل
معنًى، فيغلق الطريقَ إلى يونيكود بلا مصدرٍ خارجيٍّ ألبتّة.

`THE_IDENTITY_AXIS_DETERMINES_AND_MEANS_NOTHING`: رقمُ الحرف في المفردة ليس
خبرًا عنه: لا مخرجَ فيه ولا صفة، ولا يقرب حرفًا من حرفٍ لقربِ رقمَيهما. فمن
قرأ فرقَ رقمين تباعدًا نسب إلى المفردة ما ليس فيها، على منوال
`ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP`. وثمنُ التعيين هو المعنى، وهو ثمنٌ
مُعلَنٌ لا مطويّ.

`THE_CLASS_REMAINS_OPEN_AND_THIS_DOES_NOT_CLOSE_IT`: العشرون حرفًا المعلَّقة في
`makhraj_bit_decoder` **باقيةٌ معلَّقةً**. هذه الوحدةُ تتجاوز السؤالَ ولا
تجيبه: سؤالُ الفصل الصوتيّ سؤالُ صفةٍ، وحاجزُه قائمٌ في موضعه، ولا يرفعه
مِرمازٌ يُرقّم الحروف. ومن عدَّ هذا الإغلاقَ حسمًا خلط مِرمازًا بخبر.

`FOUR_PATTERNS_ARE_UNASSIGNED_AND_ARE_REFUSED_NOT_WRAPPED`: الحروفُ ثمانيةٌ
وعشرون وفضاءُ خمسةِ بتّاتٍ اثنان وثلاثون، فأربعةُ أنماطٍ بلا حرف. وهي
**تُرَدُّ صريحًا** ولا تُلَفّ على أوّل المفردة ولا تُقرَّب إلى أقربها: لفُّ
النمط يُخرِج حرفًا صحيحَ الشكل من مدخلٍ لا يقابله حرف. وهذا خلافُ محورَي
المخرج والحركة، إذ ملأ كلٌّ منهما فضاءَه بلا فضلة.

`THE_ALPHABET_ORDER_IS_THE_DEPOSITED_TABLE_TRAVERSAL_NOT_A_CLAIM`: ترتيبُ
المفردة هو ترتيبُ المرورِ على `CLASSICAL_MAKHARIJ` — رتبةً برتبة، وحروفَ كلِّ
رتبةٍ بترتيب ورودها. وهو اصطلاحُ ترقيمٍ مُشتَقٌّ من بايتات الجدول لا دعوى
ترتيبٍ أبجديٍّ ولا صوتيّ؛ ومتى تحرّك الجدولُ تحرّكت الأرقام، فالبصمةُ تُقرأ
معها.

`THE_UNIT_IS_A_LETTER_AND_A_MARK_AND_NOT_A_TEXT`: مدى هذا المِرماز الوحدةُ
المشكولةُ من حرفٍ مرقَّمٍ وعلامةٍ مُودَعة. وما خرج عنه — الألفُ وحروفُ المدّ،
والفراغُ، والترقيمُ، وكلُّ رمزٍ آخر — يُرَدُّ باسمه ولا يُمرَّر. ونصٌّ كاملٌ
يحتاج مجموعةَ حواملَ أوسع، وموضعُها `CarrierStateCodec` لا هنا.

`THIS_IS_A_CODEC_NOT_A_BIRTH`: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .classical_makharij_table import CLASSICAL_MAKHARIJ, CLASSICAL_TABLE_DIGEST
from .makhraj_bit_decoder import MakhrajBitError, codepoint_of
from .makhraj_haraka_bit_decoder import (
    HARAKA_ALPHABET,
    HARAKA_BIT_WIDTH,
    HARAKA_NAMES,
    bits_of_haraka,
    haraka_of_bits,
    render_unit,
)

__all__ = [
    "FOUR_PATTERNS_ARE_UNASSIGNED_NOTE",
    "IDENTITY_ALPHABET",
    "IDENTITY_BIT_WIDTH",
    "THE_ALPHABET_ORDER_IS_A_TRAVERSAL_NOTE",
    "THE_CLASS_REMAINS_OPEN_NOTE",
    "THE_IDENTITY_AXIS_DETERMINES_AND_MEANS_NOTHING_NOTE",
    "THE_UNIT_IS_A_LETTER_AND_A_MARK_NOTE",
    "UNASSIGNED_PATTERNS",
    "UNIT_BIT_WIDTH",
    "CodecCensus",
    "DecodedUnit",
    "codec_census",
    "decode_stream",
    "decode_unit",
    "encode_stream",
    "encode_unit",
    "is_assigned",
]


def _build_alphabet() -> tuple[str, ...]:
    """مفردةُ الهُويّة بترتيب المرورِ على الجدول المُودَع، لا بترتيبٍ نكتبه."""

    letters: list[str] = []
    for _rank, _name, chars in CLASSICAL_MAKHARIJ:
        letters.extend(chars)
    return tuple(letters)


IDENTITY_ALPHABET: Final[tuple[str, ...]] = _build_alphabet()

IDENTITY_BIT_WIDTH: Final[int] = (len(IDENTITY_ALPHABET) - 1).bit_length()

UNIT_BIT_WIDTH: Final[int] = IDENTITY_BIT_WIDTH + HARAKA_BIT_WIDTH

UNASSIGNED_PATTERNS: Final[int] = 2**IDENTITY_BIT_WIDTH - len(IDENTITY_ALPHABET)


THE_IDENTITY_AXIS_DETERMINES_AND_MEANS_NOTHING_NOTE: Final[str] = (
    "TheIdentityAxisDeterminesAndMeansNothing: رقمُ الحرف لا مخرجَ فيه ولا "
    "صفة، ولا يقرب حرفًا من حرفٍ لقربِ رقمَيهما؛ وثمنُ التعيين هو المعنى، "
    "وهو مُعلَنٌ لا مطويّ"
)

THE_CLASS_REMAINS_OPEN_NOTE: Final[str] = (
    "TheClassRemainsOpenAndThisDoesNotCloseIt: العشرون المعلَّقةُ باقيةٌ "
    "معلَّقة؛ سؤالُ الفصل سؤالُ صفةٍ وحاجزُه قائم، ولا يرفعه مِرمازٌ يُرقّم "
    "الحروف — ومن عدَّ هذا حسمًا خلط مِرمازًا بخبر"
)

FOUR_PATTERNS_ARE_UNASSIGNED_NOTE: Final[str] = (
    "PatternsAreUnassignedAndAreRefusedNotWrapped: فضاءُ بتّات الهُويّة أوسعُ "
    "من المفردة، فأنماطٌ بلا حرف؛ وتُرَدُّ صريحًا ولا تُلَفّ ولا تُقرَّب، إذ "
    "اللفُّ يُخرِج حرفًا صحيحَ الشكل من مدخلٍ لا يقابله حرف"
)

THE_ALPHABET_ORDER_IS_A_TRAVERSAL_NOTE: Final[str] = (
    "TheAlphabetOrderIsTheDepositedTableTraversalNotAClaim: الترتيبُ مرورٌ على "
    "الجدول المُودَع رتبةً برتبة، اصطلاحُ ترقيمٍ لا دعوى ترتيبٍ أبجديٍّ ولا "
    "صوتيّ؛ ومتى تحرّك الجدولُ تحرّكت الأرقام"
)

THE_UNIT_IS_A_LETTER_AND_A_MARK_NOTE: Final[str] = (
    "TheUnitIsALetterAndAMarkAndNotAText: المدى وحدةٌ مشكولةٌ من حرفٍ مرقَّمٍ "
    "وعلامةٍ مُودَعة؛ وما خرج عنه يُرَدُّ باسمه، ونصٌّ كامل موضعُه "
    "CarrierStateCodec لا هنا"
)


def is_assigned(bits: str) -> bool:
    """أيقابل هذا النمطُ حرفًا في المفردة؟ مُشتَقٌّ من طولها لا مكتوبٌ رقمًا."""

    if len(bits) != IDENTITY_BIT_WIDTH:
        raise MakhrajBitError(
            f"عرضُ محور الهُويّة {len(bits)} والمطلوبُ {IDENTITY_BIT_WIDTH}."
        )
    if set(bits) - {"0", "1"}:
        raise MakhrajBitError(f"متّجهٌ فيه غيرُ الصفر والواحد: {bits!r}.")
    return int(bits, 2) < len(IDENTITY_ALPHABET)


def encode_unit(letter: str, mark: str) -> str:
    """حرفٌ وعلامةٌ ← ثمانيةُ بتّات؛ وخارجُ المفردتَين يُرَدُّ باسمه."""

    if letter not in IDENTITY_ALPHABET:
        raise MakhrajBitError(
            f"حرفٌ خارجَ مفردة الهُويّة: {letter!r}؛ وحروفُ المدّ والفراغُ "
            "والترقيمُ خارجَ مدى هذا المِرماز."
        )
    index = IDENTITY_ALPHABET.index(letter)
    return f"{format(index, f'0{IDENTITY_BIT_WIDTH}b')}{bits_of_haraka(mark)}"


@dataclass(frozen=True, slots=True)
class DecodedUnit:
    """وحدةٌ مفكوكةٌ: حرفُها وعلامتُها ونصُّها ونقاطُها، لا مجموعةَ احتمالات."""

    bits: str
    letter: str
    haraka: str
    haraka_name: str
    unit: str
    codepoints: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.unit != f"{self.letter}{self.haraka}":
            raise MakhrajBitError("نصُّ الوحدة يخالف حرفَها وعلامتَها.")


def decode_unit(bits: str) -> DecodedUnit:
    """ثمانيةُ بتّاتٍ ← وحدةٌ عربيّةٌ واحدةٌ معيَّنة؛ ونمطٌ بلا حرفٍ يُرَدّ."""

    if len(bits) != UNIT_BIT_WIDTH:
        raise MakhrajBitError(
            f"عرضُ الوحدة {len(bits)} والمطلوبُ {UNIT_BIT_WIDTH} "
            f"({IDENTITY_BIT_WIDTH} للهُويّة و{HARAKA_BIT_WIDTH} للحركة)."
        )
    identity_bits, haraka_bits = bits[:IDENTITY_BIT_WIDTH], bits[IDENTITY_BIT_WIDTH:]
    if not is_assigned(identity_bits):
        raise MakhrajBitError(
            f"نمطُ هُويّةٍ بلا حرفٍ في المفردة: {identity_bits}؛ "
            f"والأنماطُ غيرُ المُسنَدة {UNASSIGNED_PATTERNS}، وتُرَدُّ ولا تُلَفّ."
        )
    letter = IDENTITY_ALPHABET[int(identity_bits, 2)]
    mark = haraka_of_bits(haraka_bits)
    unit = render_unit(letter, mark)
    return DecodedUnit(
        bits=bits,
        letter=letter,
        haraka=mark,
        haraka_name=HARAKA_NAMES[mark],
        unit=unit,
        codepoints=tuple(codepoint_of(point) for point in unit),
    )


def encode_stream(units: tuple[tuple[str, str], ...]) -> str:
    """سلسلةُ وحداتٍ ← سلسلةُ بتّاتٍ بطولٍ من مضاعفات عرض الوحدة."""

    return "".join(encode_unit(letter, mark) for letter, mark in units)


def decode_stream(bits: str) -> tuple[DecodedUnit, ...]:
    """سلسلةُ بتّاتٍ ← وحداتُها؛ وطولٌ ليس من مضاعفات عرض الوحدة يُرَدّ.

    ولا تُكمَّل البقيّةُ بأصفارٍ ولا تُهمَل: بقيّةٌ مُهمَلةٌ تُخرِج نصًّا
    أقصرَ من مدخله بلا خطأٍ يُقرأ.
    """

    if len(bits) % UNIT_BIT_WIDTH:
        raise MakhrajBitError(
            f"طولُ السلسلة {len(bits)} ليس من مضاعفات {UNIT_BIT_WIDTH}؛ "
            "وإكمالُ البقيّة بأصفارٍ يُخرِج وحدةً لم تُرمَّز."
        )
    return tuple(
        decode_unit(bits[start : start + UNIT_BIT_WIDTH])
        for start in range(0, len(bits), UNIT_BIT_WIDTH)
    )


@dataclass(frozen=True, slots=True)
class CodecCensus:
    """إحصاءُ المِرماز على فضائه كلِّه، مشتقًّا لا مكتوبًا."""

    unit_bit_width: int
    patterns: int
    assigned_patterns: int
    refused_patterns: int
    letters: int
    haraka_members: int
    table_digest: str

    def __post_init__(self) -> None:
        if self.assigned_patterns + self.refused_patterns != self.patterns:
            raise MakhrajBitError(
                "مجموعُ المُسنَد والمردودِ يخالف فضاءَ البتّات؛ ونمطٌ بلا "
                "حالٍ يُقرأ صمتُه إسنادًا."
            )
        if self.assigned_patterns != self.letters * self.haraka_members:
            raise MakhrajBitError(
                "المُسنَدُ يخالف حاصلَ ضرب المفردتين؛ وفرقٌ بينهما يعني "
                "وحدةً بلا نمطٍ أو نمطًا بوحدتين."
            )


def codec_census() -> CodecCensus:
    """شغِّل المِرمازَ على كلِّ نمطٍ وأحصِ المُسنَدَ والمردود."""

    assigned = 0
    refused = 0
    for value in range(2**UNIT_BIT_WIDTH):
        bits = format(value, f"0{UNIT_BIT_WIDTH}b")
        try:
            decode_unit(bits)
        except MakhrajBitError:
            refused += 1
        else:
            assigned += 1
    return CodecCensus(
        unit_bit_width=UNIT_BIT_WIDTH,
        patterns=2**UNIT_BIT_WIDTH,
        assigned_patterns=assigned,
        refused_patterns=refused,
        letters=len(IDENTITY_ALPHABET),
        haraka_members=len(HARAKA_ALPHABET),
        table_digest=CLASSICAL_TABLE_DIGEST,
    )


if len(set(IDENTITY_ALPHABET)) != len(IDENTITY_ALPHABET):  # pragma: no cover - حارس
    raise RuntimeError("حرفٌ مكرّرٌ في مفردة الهُويّة؛ ورقمان لحرفٍ واحدٍ يكسران التعيين.")
if UNASSIGNED_PATTERNS < 0:  # pragma: no cover - حارس
    raise RuntimeError("المفردةُ أوسعُ من فضاء بتّاتها؛ وحرفٌ بلا نمطٍ لا يُرمَّز.")
