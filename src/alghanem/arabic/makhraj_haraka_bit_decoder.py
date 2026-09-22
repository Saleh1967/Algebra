"""محورٌ ثانٍ على المتّجه: الحركةُ مع المخرج، ووسعٌ في المخرَج لا فصلٌ في الخانة.

تمدّ هذه الوحدةُ متّجهَ `makhraj_bit_decoder` بمحورٍ ثانٍ مأخوذٍ ممّا هو
مُودَعٌ في الشجرة سلفًا — الحركاتُ السبعُ في `THE_IMPORTED_HARAKAT` بوزن
استيرادها المُعلَن — فلا تستورد جدولًا ولا تمسّ حاجزَ جدول الصفة القائم. وصار
المخرَجُ وحدةً مشكولةً من نقطتَي يونيكود بدل نقطةٍ واحدة.

`A_HARAKA_AXIS_WIDENS_THE_OUTPUT_AND_DOES_NOT_NARROW_THE_CLASS`: وهذا أهمُّ ما
تُخرِجه الوحدة، وهو **مقيسٌ لا موصوف**: `separation_gain` في الإحصاء يطرح
الحروفَ غيرَ المعيَّنة بعد المحور الثاني من عددها قبله، فيخرج **صفرًا**.
الحركةُ لا تفصل الطاءَ عن الدال عن التاء، إذ الفاصلُ بينهنّ صفةٌ لا حركة؛
فالمحورُ يضاعف الأنماطَ ولا يحسم منها واحدًا. ومن قرأ الوسعَ فصلًا عدَّ
الضربَ قسمةً.

`THE_ABSENCE_IS_A_MEMBER_NOT_A_SUKUN`: مفردةُ المحور ثمانيةُ أعضاء: سبعُ
علاماتٍ مُودَعة، والثامنُ **غيابُ العلامة**. والغيابُ عضوٌ قائمٌ بذاته لا
سكونٌ مُضمَر، على ما قرّره `THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN`؛ ومن
سمّى الغيابَ سكونًا أعاد استيرادَ النظريّة الصوتيّة كلِّها من باب خلفيّ.

`EIGHT_MEMBERS_FILL_THREE_BITS`: ثمانيةُ أعضاءٍ تملأ `2**3` بلا فضلة، كما ملأت
المخارجُ الستّةَ عشرَ `2**4`. فالمتّجهُ سبعةُ بتّاتٍ كلُّ نمطٍ منها مقروء،
وليس في الفضاء نمطٌ مرفوضٌ لخروجه عن المجال. والعرضان مشتقّان من حجمَي
المفردتَين، فينقلبان متى تحرّكتا.

`THE_EIGHTH_MEMBER_IS_A_STIPULATION_NOT_A_MEASUREMENT` — **تصحيحٌ لاحق**:
وامتلاءُ `2**3` أعلاه ليس خبرًا، بل **أثرُ اصطلاحٍ منّا**. فالعلاماتُ
المُودَعةُ سبعٌ، والثامنُ «غيابُ العلامة» **مُلحَقٌ من خارج الجدول**: ليس في
البتّات نقطةُ ترميزٍ اسمُها الغياب. وقد سبق أن سُمّي هذا الإلحاقُ بعينه في
`haraka_fiber_structure`:
`ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT` —
إلحاقُ الغياب يُسوّي الأليافَ ثمانيةً فيُعيد الحزمةَ تافهةً، وهو اصطلاحٌ لا
قياس. فالامتلاءُ ههنا يدور على الاصطلاح، ولا يُقرأ بعد جلساتٍ خاصّيّةً
للعربيّة. ولم تُحذَف العبارةُ الأولى لأنّ التصحيحَ يُسجَّل ولا يُمحى موضعُه.

`THE_AXIS_IS_A_MARK_SLOT_NOT_A_MEASURED_DURATION`: قراءةُ هذا المحور «زمنًا»
قراءةٌ مقبولةٌ في الاصطلاح، لكنّ المُودَعَ هنا **خانةُ علامةٍ مكتوبة** لا مقدارُ
زمنٍ مقيس. ولا مقدارَ في هذه الشجرة يُسند إلى فتحةٍ أو سكون؛ فمن قرأ الخانةَ
مدّةً نسب إلى الجدول ما ليس فيه.

`THE_ORDER_WITHIN_THE_UNIT_CARRIES_NO_BIT`: يُكتَب الحاملُ ثمّ علامتُه في
المخرَج اصطلاحًا، وقد بُرهن في `linearization_artifact` أنّ الترتيبَ بين
الحامل وحركته لا يحمل بتًّا. فترتيبُ العرض اصطلاحٌ، ولا يُقرأ خبرًا.

`THIS_IS_A_READOUT_NOT_A_BIRTH`: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`،
ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from .makhraj_bit_decoder import (
    MAKHRAJ_BIT_WIDTH,
    MAKHRAJ_LETTERS,
    DecodeOutcome,
    MakhrajBitError,
    MakhrajReadout,
    bits_of_value,
    codepoint_of,
    decode_bits,
    encode_letter,
)
from .makhraj_bit_decoder import census as makhraj_census
from .written_haraka_mark import THE_IMPORTED_HARAKAT

__all__ = [
    "A_HARAKA_AXIS_WIDENS_THE_OUTPUT_NOTE",
    "EIGHT_MEMBERS_FILL_THREE_BITS_NOTE",
    "HARAKA_ABSENT",
    "HARAKA_ALPHABET",
    "HARAKA_BIT_WIDTH",
    "HARAKA_NAMES",
    "THE_ABSENCE_IS_A_MEMBER_NOT_A_SUKUN_NOTE",
    "THE_EIGHTH_MEMBER_IS_A_STIPULATION_NOT_A_MEASUREMENT_NOTE",
    "THE_ABSENCE_NAME",
    "THE_AXIS_IS_A_MARK_SLOT_NOT_A_MEASURED_DURATION_NOTE",
    "THE_ORDER_WITHIN_THE_UNIT_CARRIES_NO_BIT_NOTE",
    "VECTOR_BIT_WIDTH",
    "VocalizedCensus",
    "VocalizedReadout",
    "bits_of_haraka",
    "census",
    "decode_vector",
    "encode_unit",
    "haraka_of_bits",
    "render_unit",
    "split_vector",
]

HARAKA_ABSENT: Final[str] = ""

THE_ABSENCE_NAME: Final[str] = "غيابُ العلامة"


def _build_alphabet() -> tuple[str, ...]:
    """مفردةُ المحور: الغيابُ أوّلًا، ثمّ العلاماتُ المُودَعةُ بترتيب نقاطها.

    والترتيبُ اصطلاحٌ مُعلَن: نقطةُ اليونيكود تُرتِّب، والغيابُ لا نقطةَ له
    فوُضِع في الصفر. والمصدرُ لا يرتّب العلاماتِ عددًا ثنائيًّا.
    """

    return (HARAKA_ABSENT, *sorted(THE_IMPORTED_HARAKAT))


def _build_names() -> MappingProxyType[str, str]:
    names: dict[str, str] = {HARAKA_ABSENT: THE_ABSENCE_NAME}
    for mark in sorted(THE_IMPORTED_HARAKAT):
        names[mark] = unicodedata.name(mark)
    return MappingProxyType(names)


HARAKA_ALPHABET: Final[tuple[str, ...]] = _build_alphabet()

HARAKA_NAMES: Final[MappingProxyType[str, str]] = _build_names()

HARAKA_BIT_WIDTH: Final[int] = (len(HARAKA_ALPHABET) - 1).bit_length()

VECTOR_BIT_WIDTH: Final[int] = MAKHRAJ_BIT_WIDTH + HARAKA_BIT_WIDTH


A_HARAKA_AXIS_WIDENS_THE_OUTPUT_NOTE: Final[str] = (
    "AHarakaAxisWidensTheOutputAndDoesNotNarrowTheClass: الحركةُ لا تفصل حروفَ "
    "الخانة، إذ الفاصلُ بينهنّ صفةٌ لا حركة؛ فالمحورُ يضاعف الأنماطَ ولا يحسم "
    "حرفًا واحدًا، وكسبُ الفصل مطروحٌ في الإحصاء فيخرج صفرًا"
)

THE_ABSENCE_IS_A_MEMBER_NOT_A_SUKUN_NOTE: Final[str] = (
    "TheAbsenceIsAMemberNotASukun: ثامنُ أعضاء المحور غيابُ العلامة، وهو عضوٌ "
    "قائمٌ بذاته لا سكونٌ مُضمَر؛ وتسميتُه سكونًا تُعيد استيرادَ النظريّة "
    "الصوتيّة من بابٍ خلفيّ"
)

THE_EIGHTH_MEMBER_IS_A_STIPULATION_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "TheEighthMemberIsAStipulationNotAMeasurement: العلاماتُ المُودَعةُ سبعٌ، "
    "والثامنُ «غيابُ العلامة» مُلحَقٌ من خارج الجدول إذ ليس في البتّات نقطةُ "
    "ترميزٍ اسمُها الغياب؛ فامتلاءُ 2**3 أثرُ اصطلاحٍ لا خاصّيّةٌ مقيسة، على "
    "منوال ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT"
)

EIGHT_MEMBERS_FILL_THREE_BITS_NOTE: Final[str] = (
    "EightMembersFillThreeBits: أعضاءُ المحور تملأ فضاءَ بتّاته بلا فضلة كما "
    "ملأت المخارجُ فضاءَها؛ والعرضان مشتقّان من حجمَي المفردتَين فينقلبان متى "
    "تحرّكتا، ولا يُكتَبان رقمًا"
)

THE_AXIS_IS_A_MARK_SLOT_NOT_A_MEASURED_DURATION_NOTE: Final[str] = (
    "TheAxisIsAMarkSlotNotAMeasuredDuration: المُودَعُ خانةُ علامةٍ مكتوبةٍ لا "
    "مقدارُ زمنٍ مقيس؛ ولا مقدارَ في هذه الشجرة يُسنَد إلى فتحةٍ أو سكون، فمن "
    "قرأ الخانةَ مدّةً نسب إلى الجدول ما ليس فيه"
)

THE_ORDER_WITHIN_THE_UNIT_CARRIES_NO_BIT_NOTE: Final[str] = (
    "TheOrderWithinTheUnitCarriesNoBit: كتابةُ الحامل قبل علامته اصطلاحُ عرضٍ، "
    "وقد بُرهن أنّ الترتيبَ بين الحامل وحركته لا يحمل بتًّا؛ فلا يُقرأ خبرًا"
)


def bits_of_haraka(mark: str) -> str:
    """علامةٌ (أو غيابُها) ← متّجهُ بتّاتِ محورها."""

    if mark not in HARAKA_NAMES:
        raise MakhrajBitError(
            f"علامةٌ خارجَ المفردة المُودَعة: {mark!r}؛ "
            f"وأعضاءُ المحور {len(HARAKA_ALPHABET)}."
        )
    return format(HARAKA_ALPHABET.index(mark), f"0{HARAKA_BIT_WIDTH}b")


def haraka_of_bits(bits: str) -> str:
    """متّجهُ بتّاتٍ ← علامةُ المحور؛ وعرضٌ أو رمزٌ خارجَ الشرط يُرَدّ."""

    if len(bits) != HARAKA_BIT_WIDTH:
        raise MakhrajBitError(
            f"عرضُ محور الحركة {len(bits)} والمطلوبُ {HARAKA_BIT_WIDTH}؛ "
            "وتصفيرُ الناقصِ صمتًا يُبدّل العلامة."
        )
    if set(bits) - {"0", "1"}:
        raise MakhrajBitError(f"متّجهٌ فيه غيرُ الصفر والواحد: {bits!r}.")
    return HARAKA_ALPHABET[int(bits, 2)]


def split_vector(bits: str) -> tuple[str, str]:
    """اقسِم المتّجهَ إلى شقَّي المخرج والحركة بعرضَيهما المشتقَّين."""

    if len(bits) != VECTOR_BIT_WIDTH:
        raise MakhrajBitError(
            f"عرضُ المتّجه {len(bits)} والمطلوبُ {VECTOR_BIT_WIDTH} "
            f"({MAKHRAJ_BIT_WIDTH} للمخرج و{HARAKA_BIT_WIDTH} للحركة)."
        )
    return bits[:MAKHRAJ_BIT_WIDTH], bits[MAKHRAJ_BIT_WIDTH:]


def render_unit(letter: str, mark: str) -> str:
    """اكتب الوحدةَ المشكولة؛ وما لا يستقرّ تحت NFC يُرَدُّ لا يُصحَّح.

    والاستقرارُ مفحوصٌ عند كلّ بناءٍ لا مفترَضٌ مرّةً: وحدةٌ يُبدّلها التطبيعُ
    تخرج من هنا نصًّا غيرَ الذي رُكّب، فيُقرأ المركَّبُ على غير ما رُمِّز.
    """

    unit = f"{letter}{mark}"
    if unicodedata.normalize("NFC", unit) != unit:
        raise MakhrajBitError(
            f"وحدةٌ غيرُ مستقرّةٍ تحت NFC: {unit!r}؛ وتطبيعُها يُبدّل ما رُكّب."
        )
    return unit


@dataclass(frozen=True, slots=True)
class VocalizedReadout:
    """قراءةُ متّجهٍ بمحورَيه: خانةُ المخرج، وعلامتُها، والوحداتُ المكتوبة."""

    bits: str
    makhraj: MakhrajReadout
    haraka: str
    haraka_name: str
    units: tuple[str, ...]
    codepoints: tuple[tuple[str, ...], ...]
    outcome: DecodeOutcome
    unresolved_letters: int

    def __post_init__(self) -> None:
        if len(self.units) != len(self.makhraj.letters):
            raise MakhrajBitError("عددُ الوحدات يخالف عددَ حروفِ الخانة.")
        if len(self.units) != len(self.codepoints):
            raise MakhrajBitError("عددُ قوائم النقاط يخالف عددَ الوحدات.")


def decode_vector(bits: str) -> VocalizedReadout:
    """فُكَّ متّجهًا بمحورَيه إلى وحداتٍ عربيّةٍ مشكولةٍ ونقاطِ يونيكودها."""

    makhraj_bits, haraka_bits = split_vector(bits)
    readout = decode_bits(makhraj_bits)
    mark = haraka_of_bits(haraka_bits)
    units = tuple(render_unit(letter, mark) for letter in readout.letters)
    codepoints = tuple(tuple(codepoint_of(point) for point in unit) for unit in units)
    return VocalizedReadout(
        bits=bits,
        makhraj=readout,
        haraka=mark,
        haraka_name=HARAKA_NAMES[mark],
        units=units,
        codepoints=codepoints,
        outcome=readout.outcome,
        unresolved_letters=readout.unresolved_letters,
    )


def encode_unit(letter: str, mark: str) -> str:
    """حرفٌ مرقَّمٌ وعلامةٌ ← متّجهُ المحورَين؛ وخارجُ المفردتَين يُرَدّ.

    وليس هذا عكسًا للفكّ على المحور الأوّل: الفكُّ يُرجِع خانةَ الحرف مشكولةً
    بعلامتها، فتعود العلامةُ وحدَها ويبقى الحرفُ في خانته.
    """

    return f"{encode_letter(letter)}{bits_of_haraka(mark)}"


@dataclass(frozen=True, slots=True)
class VocalizedCensus:
    """إحصاءُ المحورَين على فضائهما كلِّه، وكسبُ الفصل مطروحًا لا موصوفًا."""

    vector_bit_width: int
    patterns: int
    makhraj_patterns: int
    haraka_members: int
    units_total: int
    determined_patterns: int
    underdetermined_patterns: int
    unresolved_letters_before_axis: int
    unresolved_letters_after_axis: int
    separation_gain: int

    def __post_init__(self) -> None:
        if self.determined_patterns + self.underdetermined_patterns != self.patterns:
            raise MakhrajBitError(
                "مجموعُ الأنماط المعيَّنة وغيرِ المعيَّنة يخالف فضاءَ البتّات؛ "
                "ونمطٌ بلا حالٍ يُقرأ صمتُه تعيينًا."
            )
        expected_gain = (
            self.unresolved_letters_before_axis - self.unresolved_letters_after_axis
        )
        if self.separation_gain != expected_gain:
            raise MakhrajBitError(
                "كسبُ الفصل لا يطابق الفرقَ بين العددين؛ وكسبٌ يُكتَب ولا "
                "يُطرَح دعوى لا قياس."
            )


def _all_vectors() -> tuple[str, ...]:
    return tuple(
        f"{bits_of_value(value)}{format(index, f'0{HARAKA_BIT_WIDTH}b')}"
        for value in sorted(MAKHRAJ_LETTERS)
        for index in range(len(HARAKA_ALPHABET))
    )


def census() -> VocalizedCensus:
    """شغِّل الفكَّ على كلِّ نمطٍ بمحورَيه؛ ولا رقمَ هنا مكتوبٌ بيد."""

    readouts = [decode_vector(bits) for bits in _all_vectors()]
    determined = [r for r in readouts if r.outcome is DecodeOutcome.DETERMINED]
    before = makhraj_census().letters_in_underdetermined_patterns
    after = len(
        {
            letter
            for readout in readouts
            if readout.outcome is DecodeOutcome.UNDERDETERMINED
            for letter in readout.makhraj.letters
        }
    )
    return VocalizedCensus(
        vector_bit_width=VECTOR_BIT_WIDTH,
        patterns=2**VECTOR_BIT_WIDTH,
        makhraj_patterns=2**MAKHRAJ_BIT_WIDTH,
        haraka_members=len(HARAKA_ALPHABET),
        units_total=sum(len(r.units) for r in readouts),
        determined_patterns=len(determined),
        underdetermined_patterns=len(readouts) - len(determined),
        unresolved_letters_before_axis=before,
        unresolved_letters_after_axis=after,
        separation_gain=before - after,
    )


if 2**HARAKA_BIT_WIDTH != len(HARAKA_ALPHABET):  # pragma: no cover - حارس
    raise RuntimeError(
        "فضاءُ بتّات الحركة لا يطابق أعضاءَ مفردتها؛ وفضلةُ نمطٍ بلا عضوٍ "
        "تجعل مدخلًا صحيحَ العرضِ بلا علامة."
    )
if HARAKA_ABSENT in THE_IMPORTED_HARAKAT:  # pragma: no cover - حارس
    raise RuntimeError(
        "الغيابُ وُجِد عضوًا في العلامات المُودَعة؛ وخلطُه بها يجعل الغيابَ " "علامةً تُكتَب."
    )
