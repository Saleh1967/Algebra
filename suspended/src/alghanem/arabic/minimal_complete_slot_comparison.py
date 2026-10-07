"""الخانةُ الدنيا المكتملة: مقابلةُ (C,H,B) المقترَحة بـ(a,g,p,r) القائمة.

**ما تفعله هذه الوحدة**: تقابل صياغةَ «الحدّ الأدنى المكتمل» الواردةَ من خارج
الشجرة — `MCU = (C, H, B)` — بالصياغة المُودَعة سلفًا في
`minimal_complete_fiber` — `u = (a, g, p, r)` — ثمّ تفحص بالحساب ما يُفحَص من
فضاء (C,H) اليوم، وتقول أيُّ شروط المقترَح قابلٌ للقياس وأيُّها ليس كذلك.

`TWO_OBJECTS_UNDER_ONE_NAME_IS_NOT_A_MEETING`: الاسمان واحدٌ والمُسمّيان
مختلفان. فالقائمةُ تمثيلٌ **إسناديّ**: مرساةٌ وجنسٌ ومحمولٌ ووجهُ ربط،
ومعيارُها `MCM(T) ⟺ Sufficient(T) ∧ ⋀ Necessary(i)` يُجرى بقارئٍ مستقلّ.
والمقترَحةُ خانةٌ **صوتيّةٌ مقطعيّة**: صامتٌ وحركةٌ وإغلاقٌ حدّيّ. فلا يُقال
إنّ أحدهما يؤكّد الآخر، ولا إنّ المقترَح «يلتقي مباشرةً» بالقائم — وهذا
تصحيحٌ لِما قلتُه أنا قبل القراءة.

`TWELVE_OCCURRENCES_ARE_ELEVEN_CELLS`: تقول ٥د «الخلايا غير المولودة الـ12»،
وهي **اثنتا عشرةَ وقوعةً في قناتين** لا اثنتي عشرةَ خليّةً متمايزة: القائمتان
تشتركان في `خْ`، فالاتّحادُ أحدَ عشرَ. والعددُ يُشتَقّ هنا بالاتّحاد لا
بالجمع.

`THE_DOCUMENT_USES_TWO_INVENTORIES_FOR_ONE_AXIS`: محورُ الصامت في ٥د
**ثمانيةٌ وعشرون** (26 ومعها الواو والياء في موقع الصامت)، وشاهدُه أنّ `وْ`
في قائمة غير المولودة النحويّة. وهو في ٥ي و٥ك **ستّةٌ وعشرون** بإسقاط الواو
والياء. فالمحورُ واحدٌ والمفردتان اثنتان داخل الوثيقة نفسِها.

`A_CONDITION_THAT_NEVER_REFUSES_IS_NOT_A_CONDITION`: شرطُ `Compatible(C,H)` في
المقترَح **لا يرفض شيئًا** في القناتين الجذعيّة والصوتيّة، إذ وُلدت فيهما
الخلايا المئةُ والاثنتا عشرةَ كلُّها بنصّ ٥د. فهو هناك تحصيلُ حاصلٍ، ولا يعمل
إلّا في القناتين الوظيفيّة والنحويّة. وشرطٌ لا يُرَدُّ به مدخلٌ واحدٌ لا
يُحتسَب بوّابة.

`WHAT_IS_MEASURABLE_TODAY_IS_TWO_OF_FOUR`: من شروط المقترَح الأربعة يُقاس
اليومَ اثنان من بايتات هذه الشجرة — `Identity(C)` و`H ∈ {F,D,K,S}` — أمّا
`Compatible` فمنقولٌ عن ٥د بلا مدوّنةٍ مُودَعةٍ تُعيد اشتقاقه، و`Closure`
يحتاج طبقةَ المقطع ولم يُبنَ لها مسارٌ هنا.

`THIS_IS_A_COMPARISON_NOT_A_MERGER`: لا تُعدَّل الصياغةُ القائمة، ولا تُنسَخ
المقترَحةُ إليها؛ وما هنا مقابلةٌ تُسجَّل.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .classical_makharij_table import CLASSICAL_ORDINAL
from .slgae_deposit import SlgaeDepositError
from .written_haraka_mark import THE_IMPORTED_HARAKAT

__all__ = [
    "A_CONDITION_THAT_NEVER_REFUSES_NOTE",
    "BASIC_STATES",
    "CHANNELS",
    "MCU_CONDITIONS",
    "MINIMAL_COMPLETE_NAMED_RESIDUALS",
    "PROPOSED_FIELDS",
    "SLOT_COMPARISON_NOTE",
    "STANDING_FIELDS",
    "THE_DOCUMENT_USES_TWO_INVENTORIES_NOTE",
    "TWELVE_OCCURRENCES_ARE_ELEVEN_CELLS_NOTE",
    "TWO_OBJECTS_UNDER_ONE_NAME_NOTE",
    "WHAT_IS_MEASURABLE_TODAY_NOTE",
    "ChannelRow",
    "Formulation",
    "InventoryConflictInsideTheDocument",
    "McuCondition",
    "Measurability",
    "UnbornCellCount",
    "derive_channel_arithmetic",
    "derive_inventory_conflict_inside_the_document",
    "derive_measurable_today",
    "derive_unborn_cell_count",
    "slot_space_size",
]

BASIC_STATES: Final[tuple[str, ...]] = (
    "َ",  # فتحة
    "ِ",  # كسرة
    "ُ",  # ضمّة
    "ْ",  # سكون
)
"""الحالاتُ الأربعُ في فضاء ٥د: {F, D, K, S}، وكلُّها من المُودَع السبع."""


class Formulation(Enum):
    """الصياغتان، كلٌّ باسم موضعها لا بوصفٍ عامّ."""

    STANDING = "القائمة في minimal_complete_fiber: u = (a, g, p, r)"
    PROPOSED = "المقترَحة من خارج الشجرة: MCU = (C, H, B)"


STANDING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("a", "مرساةُ هويّة"),
    ("g", "الجنسُ المرخَّص"),
    ("p", "المحمولُ من فضاء P(g)"),
    ("r", "تعيينُ نوع الربط: إخبارٌ أو تقييدٌ أو علاقةٌ حدثيّة"),
)
"""حقولُ الصياغة القائمة، وهي إسناديّةٌ لا صوتيّة."""

PROPOSED_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("C", "هويّةُ الصامت"),
    ("H", "رخصةُ الحركة من {F, D, K, S}"),
    ("B", "إغلاقٌ حدّيّ"),
)
"""حقولُ الصياغة المقترَحة، وهي مقطعيّةٌ لا إسناديّة."""

SLOT_COMPARISON_NOTE: Final[str] = (
    "معيارُ القائمة `MCM(T) ⟺ Sufficient(T) ∧ ⋀ Necessary(i)` يُجرى بقارئٍ "
    "مستقلٍّ على تمثيلٍ محجوب؛ ومعيارُ المقترَحة اقترانُ أربعةِ شروطٍ على "
    "زوجٍ (C,H). فالمعياران مختلفان مجالًا وإجراءً، لا درجةً"
)


class Measurability(Enum):
    """منزلةُ شرطٍ من حيث إمكانُ قياسه ببايتات هذه الشجرة اليوم."""

    MEASURABLE_HERE = "يُقاس من بايتات هذه الشجرة"
    TRANSCRIBED_ONLY = "منقولٌ عن الوثيقة بلا مدوّنةٍ مُودَعةٍ تُعيد اشتقاقه"
    NEEDS_A_LAYER_NOT_BUILT = "يحتاج طبقةً لم تُبنَ هنا"


@dataclass(frozen=True, slots=True)
class McuCondition:
    """شرطٌ من شروط المقترَح، بمنزلته ومصدرِ ما يُقاس به."""

    expression: str
    standing: Measurability
    what_it_rests_on: str

    def __post_init__(self) -> None:
        if not self.what_it_rests_on.strip():
            raise SlgaeDepositError("شرطٌ بلا ما يقوم عليه لا تُعرَف منزلتُه.")


MCU_CONDITIONS: Final[tuple[McuCondition, ...]] = (
    McuCondition(
        expression="Identity(C)",
        standing=Measurability.MEASURABLE_HERE,
        what_it_rests_on="الحروفُ المرقَّمةُ في CLASSICAL_MAKHARIJ المُبصَّم",
    ),
    McuCondition(
        expression="H ∈ {F, D, K, S}",
        standing=Measurability.MEASURABLE_HERE,
        what_it_rests_on="أربعٌ من THE_IMPORTED_HARAKAT السبع المُودَعة",
    ),
    McuCondition(
        expression="Compatible(C, H)",
        standing=Measurability.TRANSCRIBED_ONLY,
        what_it_rests_on=(
            "دعوى ٥د أنّ الخلايا 112 وُلدت كلُّها جذعيًّا وصوتيًّا؛ "
            "وبايتاتُ QAC ليست في مسار هذا الملفّ"
        ),
    ),
    McuCondition(
        expression="Closure(C, H)",
        standing=Measurability.NEEDS_A_LAYER_NOT_BUILT,
        what_it_rests_on="طبقةُ المقطع وحدُّ إغلاقه، ولم يُبنَ لها مسارٌ هنا",
    ),
)
"""شروطُ المقترَح الأربعة، كلٌّ بمنزلته."""


def slot_space_size() -> int:
    """حجمُ فضاء (C,H)، مُشتَقًّا من الجدول المُبصَّم لا مكتوبًا رقمًا."""

    return len(CLASSICAL_ORDINAL) * len(BASIC_STATES)


@dataclass(frozen=True, slots=True)
class ChannelRow:
    """قناةٌ من قنوات ٥د: ما وُلد فيها، وما لم يولد مُسمًّى خليّةً خليّة."""

    name: str
    born: int
    unborn_cells: tuple[str, ...]

    @property
    def total(self) -> int:
        """المجموعُ بالجمع، ويُقابَل بحجم الفضاء لا يُكتَب."""

        return self.born + len(self.unborn_cells)


CHANNELS: Final[tuple[ChannelRow, ...]] = (
    ChannelRow(name="جذعيّة", born=112, unborn_cells=()),
    ChannelRow(name="صوتيّة", born=112, unborn_cells=()),
    ChannelRow(
        name="وظيفيّة",
        born=106,
        unborn_cells=("ثِ", "خْ", "ظِ", "ظُ", "غِ", "غْ"),
    ),
    ChannelRow(
        name="نحويّة",
        born=106,
        unborn_cells=("خِ", "خْ", "زْ", "شْ", "ظْ", "وْ"),
    ),
)
"""قنواتُ ٥د الأربع كما نُشرت، والخلايا غيرُ المولودة مُسمّاة."""


def derive_channel_arithmetic() -> tuple[tuple[str, int, bool], ...]:
    """اجمع كلَّ قناةٍ وقابِلْها بحجم الفضاء؛ ولا رقمَ في النتيجة مكتوب."""

    size = slot_space_size()
    return tuple(
        (channel.name, channel.total, channel.total == size) for channel in CHANNELS
    )


@dataclass(frozen=True, slots=True)
class UnbornCellCount:
    """عدُّ غير المولود: وقوعاتٍ واتّحادًا، والفرقُ مُسمًّى لا مطويّ."""

    occurrences: int
    distinct_cells: int
    shared_cells: tuple[str, ...]
    document_says: int

    def __post_init__(self) -> None:
        if self.occurrences - self.distinct_cells != len(self.shared_cells):
            raise SlgaeDepositError(
                "فرقُ الوقوعات عن الخلايا لا يطابق عددَ المشترَك؛ "
                "وفرقٌ بلا مشترَكٍ يُسمّيه فرقٌ لا يُفحَص."
            )

    @property
    def document_counts_occurrences(self) -> bool:
        """أعدّت الوثيقةُ الوقوعاتِ لا الخلايا؟ مُشتَقٌّ بالمقارنة."""

        return self.document_says == self.occurrences != self.distinct_cells


def derive_unborn_cell_count() -> UnbornCellCount:
    """عُدَّ غيرَ المولود بالاتّحاد لا بالجمع، وقابِلْه بما قالته الوثيقة."""

    lists = [set(channel.unborn_cells) for channel in CHANNELS]
    occurrences = sum(len(channel.unborn_cells) for channel in CHANNELS)
    union: set[str] = set().union(*lists)
    shared = sorted(
        cell for cell in union if sum(1 for group in lists if cell in group) > 1
    )
    return UnbornCellCount(
        occurrences=occurrences,
        distinct_cells=len(union),
        shared_cells=tuple(shared),
        document_says=12,
    )


@dataclass(frozen=True, slots=True)
class InventoryConflictInsideTheDocument:
    """مفردتان لمحورٍ واحدٍ داخل الوثيقة نفسِها، وشاهدُ كلٍّ منهما."""

    in_cv112: int
    in_markov_and_vowel_first: int
    witness: str

    def __post_init__(self) -> None:
        if self.in_cv112 == self.in_markov_and_vowel_first:
            raise SlgaeDepositError("لا يُسجَّل تعارضٌ حيث لا تعارض.")


def derive_inventory_conflict_inside_the_document() -> (
    InventoryConflictInsideTheDocument
):
    """اقرأ المفردتين من شاهدهما: حرفُ الواو في قائمة غير المولودة النحويّة."""

    syntactic = next(channel for channel in CHANNELS if channel.name == "نحويّة")
    waw_present = any(cell.startswith("و") for cell in syntactic.unborn_cells)
    if not waw_present:  # pragma: no cover - حارس
        raise SlgaeDepositError(
            "لم تُوجَد الواوُ في القائمة النحويّة؛ والشاهدُ الذي يُبنى عليه " "التعارضُ غائب."
        )
    return InventoryConflictInsideTheDocument(
        in_cv112=len(CLASSICAL_ORDINAL),
        in_markov_and_vowel_first=len(CLASSICAL_ORDINAL) - 2,
        witness=(
            "وقوعُ `وْ` في قائمة غير المولودة النحويّة في ٥د، والواوُ مُسقَطةٌ "
            "من أبجديّة ٥ي و٥ك"
        ),
    )


def derive_measurable_today() -> tuple[int, int]:
    """كم شرطًا يُقاس هنا من كم؟ مُشتَقٌّ بالعدّ لا مكتوبًا."""

    measurable = sum(
        1
        for condition in MCU_CONDITIONS
        if condition.standing is Measurability.MEASURABLE_HERE
    )
    return measurable, len(MCU_CONDITIONS)


TWO_OBJECTS_UNDER_ONE_NAME_NOTE: Final[str] = (
    "TwoObjectsUnderOneNameIsNotAMeeting: القائمةُ تمثيلٌ إسناديٌّ "
    "(a,g,p,r) معيارُه قارئٌ مستقلّ، والمقترَحةُ خانةٌ مقطعيّةٌ (C,H,B) "
    "معيارُه اقترانُ شروط؛ فلا يؤكّد أحدُهما الآخرَ ولا يلتقيان بالاسم"
)

TWELVE_OCCURRENCES_ARE_ELEVEN_CELLS_NOTE: Final[str] = (
    "TwelveOccurrencesAreElevenCells: «الخلايا غير المولودة الـ12» اثنتا "
    "عشرةَ وقوعةً في قناتين، والخلايا المتمايزةُ إحدى عشرة؛ فالقائمتان "
    "تشتركان في خْ، والعددُ يُشتَقّ بالاتّحاد لا بالجمع"
)

THE_DOCUMENT_USES_TWO_INVENTORIES_NOTE: Final[str] = (
    "TheDocumentUsesTwoInventoriesForOneAxis: محورُ الصامت ثمانيةٌ وعشرون في "
    "٥د وستّةٌ وعشرون في ٥ي و٥ك، وشاهدُ الأولى وقوعُ وْ في قائمتها؛ "
    "فالمحورُ واحدٌ والمفردتان اثنتان داخل الوثيقة نفسِها"
)

A_CONDITION_THAT_NEVER_REFUSES_NOTE: Final[str] = (
    "AConditionThatNeverRefusesIsNotACondition: Compatible(C,H) لا يرفض مدخلًا "
    "واحدًا في القناتين الجذعيّة والصوتيّة إذ وُلدت الخلايا كلُّها؛ فهو هناك "
    "تحصيلُ حاصلٍ لا بوّابة"
)

WHAT_IS_MEASURABLE_TODAY_NOTE: Final[str] = (
    "WhatIsMeasurableTodayIsTwoOfFour: يُقاس من بايتات هذه الشجرة Identity(C) "
    "و H ∈ {F,D,K,S}؛ و Compatible منقولٌ بلا مدوّنةٍ تُعيد اشتقاقه، و Closure "
    "يحتاج طبقةَ مقطعٍ لم تُبنَ"
)

MINIMAL_COMPLETE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    TWO_OBJECTS_UNDER_ONE_NAME_NOTE,
    TWELVE_OCCURRENCES_ARE_ELEVEN_CELLS_NOTE,
    THE_DOCUMENT_USES_TWO_INVENTORIES_NOTE,
    A_CONDITION_THAT_NEVER_REFUSES_NOTE,
    WHAT_IS_MEASURABLE_TODAY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if not set(BASIC_STATES) <= set(THE_IMPORTED_HARAKAT):  # pragma: no cover - حارس
    raise RuntimeError(
        "حالةٌ من الأربع ليست في العلامات المُودَعة؛ وحالةٌ من خارج المُودَع "
        "تُدخِل في الفضاء ما لم يُودَع."
    )
