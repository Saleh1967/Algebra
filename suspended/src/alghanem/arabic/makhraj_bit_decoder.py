"""من البتّات إلى يونيكود العربيّة: فكُّ متّجهِ بتّاتٍ إلى حروفِ مخرجِه.

هذه الوحدةُ أوّلُ خطٍّ يُنفَّذ في الاتّجاه المطلوب: **بتّاتٌ داخلة، ونقاطُ
يونيكود عربيّةٌ خارجة**. ولا تُودِع جدولًا جديدًا ولا تستورد واحدًا: كلُّ ما
تقرؤه هو `CLASSICAL_MAKHARIJ` المُودَعُ سلفًا في هذه الشجرة ببصمةٍ تُعاد
اشتقاقًا، وكلُّ عددٍ هنا مشتقٌّ منه لا مكتوبٌ بيد.

`THE_BIT_ORDER_IS_A_DECLARED_CONVENTION_NOT_A_FINDING`: عرضُ المتّجه أربعةُ
بتّاتٍ لأنّ `2**4` يساوي عددَ المخارج المُودَعة بالضبط، وقراءتُه من الأثقل إلى
الأخفّ على `الرتبة − 1` **اصطلاحٌ معلَنٌ منّا**. والمصدرُ يرتّب المخارجَ ولا
يقول إنّ رتبتَها عددٌ ثنائيّ، على منوال `ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP`.

`EVERY_PATTERN_IS_A_MAKHRAJ`: ستّةَ عشرَ مخرجًا تملأ `2**4` بلا فضلة، فلا نمطَ
بتّاتٍ بعرضِ أربعةٍ يُرَدُّ لخروجه عن المجال. وهذا خبرٌ مشتقٌّ من حجم الجدول
المُودَع، وينقلب متى تحرّك الجدولُ — ولذلك يُعاد اشتقاقُه عند كلّ استيراد ولا
يُكتَب رقمًا.

`FOUR_BITS_DO_NOT_NAME_A_LETTER`: المخارجُ ستّةَ عشرَ والحروفُ ثمانيةٌ
وعشرون، فالمتّجهُ الواحدُ يصف **خانةً** لا حرفًا. ولذلك يُخرِج الفكُّ مجموعةَ
الحروف كاملةً ويُسمّي حالَه `UNDERDETERMINED`، ولا يختار منها واحدًا بحال:
اختيارُ الأوّلِ ترتيبًا يُخرِج حرفًا صحيحَ الشكل من مدخلٍ لا يُحدّده، فيُقرأ
المخرجُ تحديدًا وليس به تحديد.

`THE_CLOSURE_IS_BARRED_NOT_MISSING`: ما يفصل بين حروف الخانة الواحدة هو جدولُ
الصفة، واستيرادُه **ممنوعٌ الآن** بحاجزٍ قائمٍ مسجَّلٍ في
`gflk_feature_table_import_barrier` (جدولٌ بلا مصدرٍ مسمًّى ولا بصمةِ بايتات).
فالنقصُ هنا ليس ثغرةً تُسدّ بجدولٍ يُكتَب في هذه الجلسة؛ وسدُّه بذلك يكسر
الحاجزَ من داخله. و`sifat_barrier_standing` يقرأ منزلةَ الحاجز من موضعه عند كلّ
نداءٍ بدل أن تُنسَخ هنا كلمةٌ تَقادم صدقُها.

`THE_JAWF_AND_THE_KHAYSHUM_ARE_OUTSIDE_THE_RANGE`: الألفُ وأختاها من حروف
المدّ لا رتبةَ لها في الجدول المُودَع قصدًا، فليست في مدى هذا الفكّ ولا تخرج
منه؛ وإدخالُها برتبةٍ مخترعةٍ يُقوِّل الجدولَ ما لم يقل.

`THIS_IS_A_READOUT_NOT_A_BIRTH`: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ ولا
`E0`، ولا تستورد هذه الوحدةُ من `kernel/` شيئًا.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final

from .classical_makharij_table import (
    CLASSICAL_MAKHARIJ,
    CLASSICAL_ORDINAL,
    CLASSICAL_TABLE_DIGEST,
)
from .gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)

__all__ = [
    "EVERY_PATTERN_IS_A_MAKHRAJ_NOTE",
    "FOUR_BITS_DO_NOT_NAME_A_LETTER_NOTE",
    "MAKHRAJ_BIT_WIDTH",
    "MAKHRAJ_LETTERS",
    "MAKHRAJ_NAMES",
    "SIFAT_BARRIER_TABLE",
    "THE_BIT_ORDER_IS_A_DECLARED_CONVENTION_NOTE",
    "THE_CLOSURE_IS_BARRED_NOT_MISSING_NOTE",
    "THE_JAWF_AND_THE_KHAYSHUM_ARE_OUTSIDE_THE_RANGE_NOTE",
    "DecodeCensus",
    "DecodeOutcome",
    "MakhrajBitError",
    "MakhrajReadout",
    "bits_of_value",
    "census",
    "codepoint_of",
    "decode_bits",
    "decode_value",
    "encode_letter",
    "sifat_barrier_standing",
    "value_of_bits",
]


class MakhrajBitError(ValueError):
    """رُفض مدخلٌ خارج شرطه؛ ولا يُحمَل على أقربِ نمطٍ مقبول."""


class DecodeOutcome(Enum):
    """حالُ الفكّ: هل عيّن المتّجهُ حرفًا واحدًا أم خانةً فيها أكثرُ من حرف."""

    DETERMINED = "معيَّنٌ: حرفٌ واحدٌ في الخانة"
    UNDERDETERMINED = "غيرُ معيَّنٍ: أكثرُ من حرفٍ في الخانة"


def _build_letters() -> MappingProxyType[int, tuple[str, ...]]:
    letters: dict[int, tuple[str, ...]] = {}
    for rank, _name, chars in CLASSICAL_MAKHARIJ:
        letters[rank] = tuple(chars)
    return MappingProxyType(letters)


def _build_names() -> MappingProxyType[int, str]:
    return MappingProxyType({rank: name for rank, name, _chars in CLASSICAL_MAKHARIJ})


MAKHRAJ_LETTERS: Final[MappingProxyType[int, tuple[str, ...]]] = _build_letters()

MAKHRAJ_NAMES: Final[MappingProxyType[int, str]] = _build_names()

MAKHRAJ_BIT_WIDTH: Final[int] = (len(CLASSICAL_MAKHARIJ) - 1).bit_length()

SIFAT_BARRIER_TABLE: Final[str] = "جدولُ الصفة"


THE_BIT_ORDER_IS_A_DECLARED_CONVENTION_NOTE: Final[str] = (
    "TheBitOrderIsADeclaredConventionNotAFinding: عرضُ المتّجه مشتقٌّ من عدد "
    "المخارج المُودَعة، وقراءتُه من الأثقل إلى الأخفّ على «الرتبة − 1» اصطلاحُنا "
    "نحن؛ والمصدرُ يرتّب المخارجَ ولا يجعل رتبتَها عددًا ثنائيًّا"
)

EVERY_PATTERN_IS_A_MAKHRAJ_NOTE: Final[str] = (
    "EveryPatternIsAMakhraj: المخارجُ المُودَعةُ تملأ فضاءَ البتّات بلا فضلة، "
    "فلا نمطَ بعرضِ الجدول يُرَدُّ لخروجه عن المجال؛ وهذا خبرٌ عن حجم الجدول "
    "ينقلب متى تحرّك، فيُعاد اشتقاقُه ولا يُكتَب رقمًا"
)

FOUR_BITS_DO_NOT_NAME_A_LETTER_NOTE: Final[str] = (
    "FourBitsDoNotNameALetter: المتّجهُ يصف خانةً لا حرفًا؛ فيُخرَج ما في "
    "الخانة كاملًا وتُسمّى الحالُ UNDERDETERMINED، ولا يُختار منها واحدٌ — "
    "فاختيارُ الأوّلِ ترتيبًا يُخرِج حرفًا صحيحَ الشكل من مدخلٍ لا يُحدّده"
)

THE_CLOSURE_IS_BARRED_NOT_MISSING_NOTE: Final[str] = (
    "TheClosureIsBarredNotMissing: الفاصلُ بين حروف الخانة هو جدولُ الصفة، "
    "وحاجزُ استيراده قائمٌ في gflk_feature_table_import_barrier؛ فالنقصُ ممنوعُ "
    "السدِّ اليومَ لا مُهمَلٌ، وسدُّه بجدولٍ يُكتَب هنا يكسر الحاجزَ من داخله"
)

THE_JAWF_AND_THE_KHAYSHUM_ARE_OUTSIDE_THE_RANGE_NOTE: Final[str] = (
    "TheJawfAndTheKhayshumAreOutsideTheRange: حروفُ المدّ الجوفيّةُ والخيشومُ "
    "خارجَ ترقيم الجدول المُودَع قصدًا، فليست في مدى هذا الفكّ؛ وإدخالُها "
    "برتبةٍ مخترعةٍ يُقوِّل الجدولَ ما لم يقل"
)


def codepoint_of(letter: str) -> str:
    """أعطِ نقطةَ اليونيكود بصيغة `U+XXXX`؛ وحرفٌ من أكثرَ من نقطةٍ يُرَدّ.

    التطبيعُ مفحوصٌ لا مفترَض: حرفٌ لا يستقرّ على نقطةٍ واحدةٍ تحت `NFC` يخرج
    من هنا نصًّا لا نقطة، فيُرَدُّ صريحًا بدل أن يُكتَب أوّلُ مقاطعه.
    """

    if unicodedata.normalize("NFC", letter) != letter:
        raise MakhrajBitError(
            f"حرفٌ غيرُ مستقرٍّ تحت NFC: {letter!r}؛ وبصمتُه بعد التطبيع غيرُها قبله."
        )
    if len(letter) != 1:
        raise MakhrajBitError(
            f"حرفٌ من {len(letter)} نقطةٍ لا نقطةَ واحدةَ له: {letter!r}."
        )
    return f"U+{ord(letter):04X}"


def bits_of_value(value: int) -> str:
    """رتبةُ مخرجٍ ← متّجهُ بتّاتٍ بعرضِ الجدول، من الأثقل إلى الأخفّ."""

    if value not in MAKHRAJ_LETTERS:
        raise MakhrajBitError(
            f"رتبةٌ خارجَ الجدول المُودَع: {value}؛ والرتبُ "
            f"{min(MAKHRAJ_LETTERS)}..{max(MAKHRAJ_LETTERS)}."
        )
    return format(value - 1, f"0{MAKHRAJ_BIT_WIDTH}b")


def value_of_bits(bits: str) -> int:
    """متّجهُ بتّاتٍ ← رتبةُ مخرجٍ؛ وعرضٌ أو رمزٌ خارجَ الشرط يُرَدّ."""

    if len(bits) != MAKHRAJ_BIT_WIDTH:
        raise MakhrajBitError(
            f"عرضُ المتّجه {len(bits)} والمطلوبُ {MAKHRAJ_BIT_WIDTH}؛ "
            "وتصفيرُ الناقصِ صمتًا يُغيّر الخانةَ بلا أثرٍ ظاهر."
        )
    if set(bits) - {"0", "1"}:
        raise MakhrajBitError(f"متّجهٌ فيه غيرُ الصفر والواحد: {bits!r}.")
    return int(bits, 2) + 1


@dataclass(frozen=True, slots=True)
class MakhrajReadout:
    """قراءةُ متّجهٍ واحد: خانتُه، وحروفُها، ونقاطُها، وما بقي غيرَ معيَّن."""

    bits: str
    value: int
    makhraj_name: str
    letters: tuple[str, ...]
    codepoints: tuple[str, ...]
    outcome: DecodeOutcome
    unresolved_letters: int

    def __post_init__(self) -> None:
        if not self.letters:
            raise MakhrajBitError("خانةٌ بلا حرفٍ واحدٍ لا تُقرأ فكًّا.")
        if len(self.letters) != len(self.codepoints):
            raise MakhrajBitError("عددُ النقاط يخالف عددَ الحروف في قراءةٍ واحدة.")


def decode_value(value: int) -> MakhrajReadout:
    """فُكَّ رتبةَ مخرجٍ إلى حروفها ونقاطِ يونيكودها."""

    letters = MAKHRAJ_LETTERS[value] if value in MAKHRAJ_LETTERS else ()
    if not letters:
        raise MakhrajBitError(
            f"رتبةٌ خارجَ الجدول المُودَع: {value}؛ والرتبُ "
            f"{min(MAKHRAJ_LETTERS)}..{max(MAKHRAJ_LETTERS)}."
        )
    outcome = (
        DecodeOutcome.DETERMINED if len(letters) == 1 else DecodeOutcome.UNDERDETERMINED
    )
    return MakhrajReadout(
        bits=bits_of_value(value),
        value=value,
        makhraj_name=MAKHRAJ_NAMES[value],
        letters=letters,
        codepoints=tuple(codepoint_of(letter) for letter in letters),
        outcome=outcome,
        unresolved_letters=len(letters) - 1,
    )


def decode_bits(bits: str) -> MakhrajReadout:
    """فُكَّ متّجهَ بتّاتٍ إلى حروفِ خانته ونقاطِ يونيكودها."""

    return decode_value(value_of_bits(bits))


def encode_letter(letter: str) -> str:
    """حرفٌ مرقَّمٌ ← متّجهُ بتّاتِ مخرجه؛ وحرفٌ بلا رتبةٍ يُرَدُّ صريحًا.

    وليس هذا عكسًا للفكّ: الفكُّ يُخرِج خانةً، فمن رمّز ثمّ فكّ رجع بالخانة
    كلِّها لا بحرفه، وذلك فقدٌ مقيسٌ في `census` لا عيبٌ يُداوى بالاختيار.
    """

    if letter not in CLASSICAL_ORDINAL:
        raise MakhrajBitError(
            f"حرفٌ لا رتبةَ له في الجدول المُودَع: {letter!r}؛ "
            "وحروفُ المدّ والخيشومُ خارجَ الترقيم قصدًا."
        )
    return bits_of_value(CLASSICAL_ORDINAL[letter])


def sifat_barrier_standing() -> ImportBarrierStanding:
    """اقرأ منزلةَ حاجزِ جدول الصفة من موضعه الآن، لا من كلمةٍ منسوخةٍ هنا."""

    for barrier in FEATURE_TABLE_IMPORT_BARRIERS:
        if barrier.table == SIFAT_BARRIER_TABLE:
            return barrier.standing
    raise MakhrajBitError(
        f"لم يُوجَد حاجزٌ باسم {SIFAT_BARRIER_TABLE!r}؛ " "وغيابُ الحاجزِ ليس رفعًا له."
    )


@dataclass(frozen=True, slots=True)
class DecodeCensus:
    """إحصاءُ الفكّ على فضاء البتّات كلِّه، مشتقًّا لا مكتوبًا."""

    bit_width: int
    patterns: int
    makharij: int
    letters_total: int
    determined_patterns: int
    underdetermined_patterns: int
    letters_in_determined_patterns: int
    letters_in_underdetermined_patterns: int
    largest_class_size: int
    table_digest: str
    sifat_barrier: ImportBarrierStanding

    def __post_init__(self) -> None:
        covered = (
            self.letters_in_determined_patterns
            + self.letters_in_underdetermined_patterns
        )
        if covered != self.letters_total:
            raise MakhrajBitError(
                f"مجموعُ الحروف في الخانات {covered} وحروفُ الجدول "
                f"{self.letters_total}؛ وفرقٌ بينهما يعني حرفًا يُعَدّ مرّتين "
                "أو لا يُعَدّ."
            )


def census() -> DecodeCensus:
    """شغِّل الفكَّ على كلِّ نمطٍ ممكنٍ وأخرِج إحصاءَه؛ ولا رقمَ هنا مكتوبٌ بيد."""

    readouts = [decode_value(value) for value in sorted(MAKHRAJ_LETTERS)]
    determined = [r for r in readouts if r.outcome is DecodeOutcome.DETERMINED]
    underdetermined = [
        r for r in readouts if r.outcome is DecodeOutcome.UNDERDETERMINED
    ]
    return DecodeCensus(
        bit_width=MAKHRAJ_BIT_WIDTH,
        patterns=2**MAKHRAJ_BIT_WIDTH,
        makharij=len(MAKHRAJ_LETTERS),
        letters_total=len(CLASSICAL_ORDINAL),
        determined_patterns=len(determined),
        underdetermined_patterns=len(underdetermined),
        letters_in_determined_patterns=sum(len(r.letters) for r in determined),
        letters_in_underdetermined_patterns=sum(
            len(r.letters) for r in underdetermined
        ),
        largest_class_size=max(len(r.letters) for r in readouts),
        table_digest=CLASSICAL_TABLE_DIGEST,
        sifat_barrier=sifat_barrier_standing(),
    )


if 2**MAKHRAJ_BIT_WIDTH != len(CLASSICAL_MAKHARIJ):  # pragma: no cover - حارس
    raise RuntimeError(
        "فضاءُ البتّات لا يطابق عددَ المخارج المُودَعة؛ وفضلةُ نمطٍ بلا مخرجٍ "
        "تجعل مدخلًا صحيحَ العرضِ بلا مخرَج، فيُقرأ الصمتُ فكًّا."
    )
if sum(len(letters) for letters in MAKHRAJ_LETTERS.values()) != len(CLASSICAL_ORDINAL):
    raise RuntimeError(  # pragma: no cover - حارس
        "حروفُ الخانات تخالف حروفَ الجدول المرقَّمة؛ وحرفٌ يُعَدُّ مرّتين "
        "أو لا يُعَدُّ يُفسِد كلَّ إحصاءٍ مبنيٍّ عليها."
    )


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويٌّ للفحص
    reading = census()
    print(f"عرضُ المتّجه = {reading.bit_width} بتّات، والأنماطُ {reading.patterns}")
    print(f"المخارجُ {reading.makharij}، والحروفُ {reading.letters_total}")
    print(
        f"الأنماطُ المعيَّنة: {reading.determined_patterns}، "
        f"وغيرُ المعيَّنة: {reading.underdetermined_patterns}"
    )
    print(f"حاجزُ جدول الصفة: {reading.sifat_barrier.value}")
