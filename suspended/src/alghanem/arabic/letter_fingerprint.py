"""بصمةُ الحرف بأربعة أبعادٍ: بُعدان مقيسان وبُعدان مستورَدان، والفرقُ مُعلَن.

السكربتُ الذي جاءت منه هذه الوحدة كان يَعِد بـ«نسخةٍ صادقة» ثم يُخفي ثلاثةَ
أشياء، فهذه الوحدةُ تُصلحه بإظهارها لا بتحسين رقمِه:

* **بُعدان من الأربعة ليسا قياسًا**: الذلاقةُ وعددُ الأدوار جدولان مكتوبان
  يدًا، لا يُشتقّان من المدوَّنة ولا يتغيّران بتغيُّرها. وهما وحدهما يقسمان
  الحروفَ التسعةَ والعشرين إلى ثماني خاناتٍ فقط، فالفصلُ الفعليُّ واقعٌ على
  بُعدين مقيسين لا أربعة. ولذلك فُصِلا هنا صراحةً في `DimensionProvenance`،
  ولا يُقرأ عددُ الأبعاد أربعةً في أيّ ادّعاءٍ عن قوّة القياس.
* **تصادمُ (د، ق) ليس مفاجأةً تُعتذَر عنها**: الحرفان يقعان سلفًا — قبل قراءة
  أيّ مدوَّنة — في خانةٍ واحدة `(غير ذَلْقيّ، عددُ أدوارٍ = ١)`، فبقاؤهما
  متصادمَين لازمٌ بنيويٌّ من الجدولين المستورَدين، لا نتيجةٌ رصديّة.
  و`structural_collision_classes` يُخرِج هذه الخانات من الجدولين وحدهما، بلا
  مدوَّنة، حتى يُقرأ اللازمُ قبل الرصد.
* **فريدٌ ٢٨ من ٢٩ رقمٌ بلا مُقابِل**: تفرُّدُ البصمات لا يدلّ على بنيةٍ حتى
  يُقارَن بما تُنتجه مدوَّنةٌ عشوائيّةٌ بنفس الحجم بنفس الخوارزميّة. ولذلك
  `uniform_null_unique_counts` جزءٌ من الوحدة لا ملحقٌ بها: من ذكر التفرُّدَ
  بلا خطِّ الصفر ذكر نصفَ القياس.

وأُصلِحت فيه كذلك عيوبٌ سلوكيّةٌ صامتة:

* التقريبُ كان تقريبَ بايثون المصرفيَّ (نصفٌ إلى الزوج)، فحرفان على حدّ ٠٫٥
  يلتصقان أو ينفصلان بلا معنًى لغويّ؛ وصار هنا `نصفٌ إلى أعلى` مُعلَنًا
  ومُحتسَبًا بكسورٍ صحيحةٍ لا بعائمٍ.
* تعادلُ المواضع كان يُفَضّ صامتًا بترتيب P1>P2>P3؛ وصار عضوًا مُعلَنًا
  `تعادل` في مفردةٍ مغلقة، فالتعادلُ يُقرأ ولا يُخفى.
* شرطُ «ثلاثيّ الطول» كان يُطبَّق **قبل** طيِّ الهمزات، فجذرٌ مكتوبٌ بصورةٍ
  أخرى يسقط صامتًا؛ وصار الطيُّ أوّلًا، وصار كلُّ صفٍّ مستبعَدٍ مُسمّى بسببه
  في `RootExclusion` بدل أن يتبخّر.
* «الكثافة» كانت مقسومةً على عدد الجذور لا عدد المواضع، فمجموعُها يقارب ٣٠٠٪
  لا ١٠٠٪؛ والحسابُ باقٍ كما هو لأنّه نصيبُ الحرف من الجذور، لكنّ الاسمَ صار
  `root_share` لا «كثافة».
* لا `pandas` هنا: المستودعُ بلا تبعياتِ تشغيل، والقراءةُ بمكتبة `csv`
  القياسيّة مع تحقُّقٍ صريحٍ من الأعمدة ورفضٍ مُسمًّى لكلّ حالةٍ خارج المجال.

نطاقُ الوحدة وحدُّها: **قياسٌ وتسجيلٌ لا سلطة**. لا تُصدر ولادةً ولا حكمَ
ولادةٍ ولا تجميدًا ولا `E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ
فيه. ولا تُقرِّر هذه الوحدةُ أنّ البصمةَ هُويّةٌ للحرف: التفرُّدُ خاصّيّةُ
جدولٍ مشتقٍّ من مدوَّنةٍ بعينها، وادّعاءُ الهُويّة يحتاج بوّابةَ ولادةٍ لم
تُبنَ.
"""

from __future__ import annotations

import csv
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from pathlib import Path
from random import Random
from typing import Final, Literal

__all__ = [
    "DIACRITICS_AND_TATWEEL",
    "DIMENSION_PROVENANCE",
    "FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS_NOTE",
    "IMPORTED_ROLE_COUNTS",
    "ITHLAQ_LETTERS",
    "LETTER_FINGERPRINT_IS_NOT_A_GATE_NOTE",
    "LETTER_VOCABULARY",
    "NAMED_RESIDUALS",
    "NORMALIZATION_FORM",
    "ROOT_COLUMN",
    "ROOT_SHARE_IS_NOT_A_DENSITY_NOTE",
    "ROOT_TYPE_COLUMN",
    "TRILITERAL_ROOT_TYPE",
    "UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT_NOTE",
    "CollisionKey",
    "CorpusReading",
    "DimensionProvenance",
    "ExclusionReason",
    "FingerprintCensus",
    "ImportedClassKey",
    "LetterFingerprint",
    "LetterFingerprintError",
    "LetterPositionCounts",
    "PreferredPosition",
    "RootExclusion",
    "compute_fingerprint_census",
    "fold_root",
    "read_triliteral_roots",
    "round_half_up_percent",
    "structural_collision_classes",
    "uniform_null_unique_counts",
]


CollisionKey = tuple[str, int, bool, int]
"""مفتاحُ المقارنة: (الموضعُ المفضَّل، النصيب، الذلاقة، عددُ الأدوار)."""

ImportedClassKey = tuple[bool, int]
"""الخانةُ المستورَدةُ وحدَها: (الذلاقة، عددُ الأدوار)."""


class LetterFingerprintError(ValueError):
    """رفضٌ صريحٌ في بصمة الحرف؛ لا يُحمَل مدخلٌ على أقرب حالةٍ مقبولة."""


LETTER_VOCABULARY: Final[tuple[str, ...]] = (
    *"ابتثجحخدذرزسشصضطظعغفقكلمنهوي",
    "ء",
)

ITHLAQ_LETTERS: Final[frozenset[str]] = frozenset("فرمنلب")

IMPORTED_ROLE_COUNTS: Final[Mapping[str, int]] = {
    "ا": 5,
    "ت": 3,
    "ح": 3,
    "ث": 2,
    "ذ": 2,
    "ع": 2,
    "ك": 2,
    "ل": 2,
    "ه": 2,
    "و": 2,
    "ء": 1,
    "ب": 1,
    "د": 1,
    "س": 1,
    "غ": 1,
    "ف": 1,
    "ق": 1,
    "ن": 1,
    "ي": 1,
    "م": 1,
    "ج": 0,
    "خ": 0,
    "ز": 0,
    "ش": 0,
    "ص": 0,
    "ض": 0,
    "ط": 0,
    "ظ": 0,
    "ر": 0,
}

NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"

DIACRITICS_AND_TATWEEL: Final[frozenset[str]] = frozenset(
    (
        "\u0640",  # تطويل
        *(chr(code) for code in range(0x064B, 0x0653)),
        "\u0670",  # ألف خنجريّة
    )
)

_FOLDING_MAP: Final[Mapping[str, str]] = {
    "أ": "ء",
    "إ": "ء",
    "ؤ": "ء",
    "ئ": "ء",
    "آ": "ء",
    "ٱ": "ا",
    "ى": "ي",
}

ROOT_COLUMN: Final[str] = "root_full"

ROOT_TYPE_COLUMN: Final[str] = "root_type"

TRILITERAL_ROOT_TYPE: Final[str] = "ثلاثي"

_TRILITERAL_LENGTH: Final[int] = 3


if len(LETTER_VOCABULARY) != 29:  # pragma: no cover - guard
    raise RuntimeError("the closed letter vocabulary is 28 letters plus bare hamza")

if set(IMPORTED_ROLE_COUNTS) != set(LETTER_VOCABULARY):  # pragma: no cover - guard
    raise RuntimeError("the imported role table must cover exactly the vocabulary")

if not ITHLAQ_LETTERS <= set(LETTER_VOCABULARY):  # pragma: no cover - guard
    raise RuntimeError("the ithlaq letters must be members of the vocabulary")


FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS_NOTE: Final[str] = (
    "FourDimensionsAreNotFourMeasurements: بُعدان فقط مقيسان من المدوَّنة "
    "(الموضعُ المفضَّل ونصيبُ الجذور)، والذلاقةُ وعددُ الأدوار جدولان "
    "مستورَدان لا يتغيّران بتغيُّر المدوَّنة؛ فمن عدَّ الأبعادَ أربعةً في "
    "تقدير قوّة القياس عدَّ مُدخَلاتِه شواهدَه"
)

ROOT_SHARE_IS_NOT_A_DENSITY_NOTE: Final[str] = (
    "RootShareIsNotADensity: المقسومُ عليه عددُ الجذور لا عددُ المواضع، فمجموعُ "
    "القيم يقارب ٣٠٠٪ لا ١٠٠٪؛ فهي نصيبُ الحرف من الجذور وتسميتُها كثافةً "
    "تُوهِم نسبةً موضعيّةً لم تُحسَب"
)

UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT_NOTE: Final[str] = (
    "UniquenessWithoutANullBaselineIsHalfAMeasurement: عددُ البصمات الفريدة لا "
    "يدلّ على بنيةٍ حتى يُقابَل بما تُنتجه مدوَّنةٌ عشوائيّةٌ بنفس الحجم بنفس "
    "الخوارزميّة؛ فالرقمُ وحده لا يفصل البنيةَ عن الصدفة"
)

LETTER_FINGERPRINT_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادةٍ ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)


NAMED_RESIDUALS: Final[Mapping[str, str]] = {
    "FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS": (
        FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS_NOTE
    ),
    "ROOT_SHARE_IS_NOT_A_DENSITY": ROOT_SHARE_IS_NOT_A_DENSITY_NOTE,
    "UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT": (
        UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT_NOTE
    ),
    "A_UNIQUE_FINGERPRINT_IS_NOT_AN_IDENTITY": (
        "تفرُّدُ صفٍّ في جدولٍ مشتقٍّ من مدوَّنةٍ بعينها خاصّيّةُ ذلك الجدول، لا "
        "هُويّةٌ للحرف ولا بنيةٌ فيه؛ وادّعاءُ الهُويّة يحتاج بوّابةَ ولادةٍ لم "
        "تُبنَ، ولا تُصدرها هذه الوحدة"
    ),
    "COARSENESS_IS_A_CHOICE_NOT_A_FINDING": (
        "خشونةُ التقريب — عددٌ صحيحٌ لا أربع منازل — اختيارٌ يغيّر عددَ "
        "التصادمات؛ فتغييرُها بعد رؤية التصادمات هو عينُ اختيار السمة بعد رؤية "
        "النتيجة الذي يمنعه `probe_preregistration`، ولذلك تُعلَن هنا قاعدةً "
        "واحدةً ثابتةً لا مُعامَلًا يُدار"
    ),
    "EXCLUDED_ROWS_ARE_NAMED_NOT_DROPPED": (
        "لا يسقط صفٌّ صامتًا: كلُّ صفٍّ خارج المجال يُسجَّل بسببه في "
        "`RootExclusion`، فمدوَّنةٌ نصفُها مرفوضٌ تُقرأ مرفوضةً ولا تُقرأ صغيرة"
    ),
    "THIS_CORPUS_IS_NOT_THE_LANGUAGE": (
        "المسحُ تامٌّ على المدوَّنة المُعطاة وحدها؛ وتمامُه عليها ليس تمامًا على "
        "الجذور الثلاثيّة في العربيّة، على حدِّ "
        "`ExhaustedSourceIsNotAnExhaustedWorld`"
    ),
}


class PreferredPosition(Enum):
    """الموضعُ المفضَّل؛ مفردةٌ مغلقةٌ رابعُها التعادلُ مُعلَنًا لا مفضوضًا."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    TIE = "تعادل"


class DimensionProvenance(Enum):
    """أمقيسٌ البُعدُ من المدوَّنة أم مستورَدٌ من جدولٍ مكتوبٍ يدًا؟"""

    MEASURED = "مقيس"
    IMPORTED = "مستورَد"


class ExclusionReason(Enum):
    """أسبابُ استبعاد الصفّ؛ مُسمّاةٌ كلُّها، ولا صفَّ يسقط بلا سبب."""

    ROOT_TYPE_NOT_TRILITERAL = "نوع_الجذر_ليس_ثلاثيًّا"
    EMPTY_ROOT = "جذر_خالٍ"
    LENGTH_NOT_THREE = "الطول_بعد_الطيّ_ليس_ثلاثة"
    LETTER_OUT_OF_VOCABULARY = "حرف_خارج_المفردة"


DIMENSION_PROVENANCE: Final[Mapping[str, DimensionProvenance]] = {
    "preferred_position": DimensionProvenance.MEASURED,
    "root_share_percent": DimensionProvenance.MEASURED,
    "is_ithlaq": DimensionProvenance.IMPORTED,
    "role_count": DimensionProvenance.IMPORTED,
}


for _vocabulary, _size, _reason in (
    (PreferredPosition, 4, "three positions plus a declared tie"),
    (DimensionProvenance, 2, "a dimension is measured or imported, never both"),
    (ExclusionReason, 4, "every excluded row is named by one of four reasons"),
):
    if len(_vocabulary) != _size:  # pragma: no cover - guard
        raise RuntimeError(_reason)


def fold_root(raw: str) -> str:
    """اطوِ صورةَ الجذر إلى المفردة المغلقة قبل أيّ شرطِ طول.

    الطيُّ مُعلَن: تطبيعُ `NFC`، وحذفُ الحركات والتطويل، وطيُّ صور الهمزة إلى
    `ء`، و`ٱ` إلى `ا`، و`ى` إلى `ي`، وحذفُ الفراغات المحيطة والفواصل الداخليّة.
    ولا يُحذَف حرفٌ غيرُ معروفٍ صامتًا: يبقى في المُخرَج ليُرَدّ باسمه.
    """

    if not isinstance(raw, str):
        raise LetterFingerprintError("الجذرُ نصٌّ لا شيءَ آخر.")
    normalized = unicodedata.normalize(NORMALIZATION_FORM, raw).strip()
    folded: list[str] = []
    for character in normalized:
        if character in DIACRITICS_AND_TATWEEL or character.isspace():
            continue
        folded.append(_FOLDING_MAP.get(character, character))
    return "".join(folded)


def round_half_up_percent(part: int, whole: int) -> int:
    """`part/whole` نسبةً مئويّةً صحيحةً بقاعدة «نصفٌ إلى أعلى» بكسورٍ صحيحة.

    لا عائمَ في الطريق ولا `round` مصرفيّ: حدُّ ٠٫٥ يصعد دائمًا، فلا يتعلّق
    التصاقُ حرفين بزوجيّة الرقم الذي قبله.
    """

    if whole <= 0:
        raise LetterFingerprintError("النسبةُ لا تُحسَب على مدوَّنةٍ خالية.")
    if part < 0:
        raise LetterFingerprintError("العدُّ لا يكون سالبًا.")
    shifted = Fraction(part * 100, whole) + Fraction(1, 2)
    return shifted.numerator // shifted.denominator


@dataclass(frozen=True, slots=True)
class RootExclusion:
    """صفٌّ مستبعَدٌ باسمِ سببه؛ ولا حقلَ حكمٍ فيه."""

    row_index: int
    raw_root: str
    reason: ExclusionReason

    def __post_init__(self) -> None:
        if self.row_index < 0:
            raise LetterFingerprintError("ترتيبُ الصفّ عددٌ غيرُ سالب.")
        if not isinstance(self.reason, ExclusionReason):
            raise LetterFingerprintError("سببُ الاستبعاد عضوٌ في مفردته.")


@dataclass(frozen=True, slots=True)
class CorpusReading:
    """قراءةُ مدوَّنةٍ: المقبولُ والمستبعَدُ معًا، فلا يُقرأ أحدُهما وحده."""

    accepted_roots: tuple[str, ...]
    exclusions: tuple[RootExclusion, ...]

    def __post_init__(self) -> None:
        for root in self.accepted_roots:
            if len(root) != _TRILITERAL_LENGTH:
                raise LetterFingerprintError("الجذرُ المقبولُ ثلاثيٌّ بعد الطيّ.")
            for letter in root:
                if letter not in LETTER_VOCABULARY:
                    raise LetterFingerprintError(
                        f"حرفٌ خارج المفردة المغلقة: {letter!r}."
                    )

    @property
    def row_count(self) -> int:
        """عددُ الصفوف المقروءة كلِّها، مقبولِها ومستبعَدِها."""

        return len(self.accepted_roots) + len(self.exclusions)

    @property
    def exclusion_counts(self) -> Mapping[ExclusionReason, int]:
        """تعدادُ الاستبعاد بحسب سببه؛ كلُّ سببٍ مذكورٌ ولو كان صفرًا."""

        counts = dict.fromkeys(ExclusionReason, 0)
        for exclusion in self.exclusions:
            counts[exclusion.reason] += 1
        return counts


@dataclass(frozen=True, slots=True)
class LetterPositionCounts:
    """العدُّ الخام لحرفٍ واحد في المواضع الثلاثة، قبل أيّ تقريب."""

    letter: str
    first: int
    second: int
    third: int

    def __post_init__(self) -> None:
        if self.letter not in LETTER_VOCABULARY:
            raise LetterFingerprintError("الحرفُ عضوٌ في المفردة المغلقة.")
        for count in (self.first, self.second, self.third):
            if count < 0:
                raise LetterFingerprintError("العدُّ لا يكون سالبًا.")

    @property
    def total(self) -> int:
        """مجموعُ المواضع الثلاثة؛ يُعدّ الحرفُ مرّةً لكلّ موضعٍ يقع فيه."""

        return self.first + self.second + self.third

    @property
    def preferred_position(self) -> PreferredPosition:
        """الموضعُ الأكثرُ؛ والتعادلُ عضوٌ مُعلَنٌ لا مفضوضٌ بترتيب المواضع."""

        ordered = (
            (PreferredPosition.P1, self.first),
            (PreferredPosition.P2, self.second),
            (PreferredPosition.P3, self.third),
        )
        best = max(count for _, count in ordered)
        winners = [position for position, count in ordered if count == best]
        if len(winners) != 1:
            return PreferredPosition.TIE
        return winners[0]


@dataclass(frozen=True, slots=True)
class LetterFingerprint:
    """بصمةُ حرفٍ بأربعة أبعاد؛ بُعدان مقيسان وبُعدان مستورَدان."""

    letter: str
    preferred_position: PreferredPosition
    root_share_percent: int
    is_ithlaq: bool
    role_count: int

    def __post_init__(self) -> None:
        if self.letter not in LETTER_VOCABULARY:
            raise LetterFingerprintError("الحرفُ عضوٌ في المفردة المغلقة.")
        if not isinstance(self.preferred_position, PreferredPosition):
            raise LetterFingerprintError("الموضعُ المفضَّل عضوٌ في مفردته.")
        if self.root_share_percent < 0:
            raise LetterFingerprintError("النصيبُ لا يكون سالبًا.")
        if self.is_ithlaq != (self.letter in ITHLAQ_LETTERS):
            raise LetterFingerprintError("الذلاقةُ تُقرأ من جدولها لا تُكتَب يدًا.")
        if self.role_count != IMPORTED_ROLE_COUNTS[self.letter]:
            raise LetterFingerprintError("عددُ الأدوار يُقرأ من جدوله المستورَد.")

    @property
    def discriminating_key(self) -> CollisionKey:
        """مفتاحُ المقارنة؛ هو ما يُقاس عليه التصادمُ لا نصُّ العرض."""

        return (
            self.preferred_position.value,
            self.root_share_percent,
            self.is_ithlaq,
            self.role_count,
        )

    @property
    def imported_class(self) -> ImportedClassKey:
        """الخانةُ المستورَدةُ وحدَها: ما يثبت للحرف قبل قراءة أيّ مدوَّنة."""

        return (self.is_ithlaq, self.role_count)


@dataclass(frozen=True, slots=True)
class FingerprintCensus:
    """جدولُ البصمات مع تصادماته مُسمّاةً؛ ولا عنوانَ نجاحٍ فيه."""

    corpus_size: int
    counts: tuple[LetterPositionCounts, ...]
    fingerprints: tuple[LetterFingerprint, ...]

    def __post_init__(self) -> None:
        if self.corpus_size <= 0:
            raise LetterFingerprintError("المسحُ لا يقع على مدوَّنةٍ خالية.")
        letters = tuple(fingerprint.letter for fingerprint in self.fingerprints)
        if letters != LETTER_VOCABULARY:
            raise LetterFingerprintError(
                "الجدولُ يغطّي المفردةَ المغلقةَ كلَّها بترتيبها، لا بعضَها."
            )
        if tuple(count.letter for count in self.counts) != LETTER_VOCABULARY:
            raise LetterFingerprintError("العدُّ الخامُ يغطّي المفردةَ كلَّها.")

    @property
    def by_letter(self) -> Mapping[str, LetterFingerprint]:
        """البصماتُ مفهرسةً بحرفها."""

        return {fingerprint.letter: fingerprint for fingerprint in self.fingerprints}

    @property
    def unique_fingerprint_count(self) -> int:
        """عددُ المفاتيح المتمايزة؛ لا يُقرأ إلا مع خطِّ الصفر."""

        keys = {fingerprint.discriminating_key for fingerprint in self.fingerprints}
        return len(keys)

    @property
    def collisions(self) -> tuple[tuple[CollisionKey, tuple[str, ...]], ...]:
        """التصادماتُ مُسمّاةً بحروفها؛ مرتَّبةً ترتيبًا ثابتًا لا عشوائيًّا."""

        grouped: dict[CollisionKey, list[str]] = {}
        for fingerprint in self.fingerprints:
            grouped.setdefault(fingerprint.discriminating_key, []).append(
                fingerprint.letter
            )
        return tuple(
            (key, tuple(letters))
            for key, letters in sorted(grouped.items())
            if len(letters) > 1
        )

    @property
    def structurally_forced_collisions(
        self,
    ) -> tuple[tuple[CollisionKey, tuple[str, ...]], ...]:
        """التصادماتُ التي حروفُها في خانةٍ مستورَدةٍ واحدةٍ أصلًا.

        وهي التي لا تُقرأ نتيجةً رصديّةً: اشتراكُ حرفين في الجدولين المكتوبين
        يدًا سابقٌ على المدوَّنة، فبقاؤهما متصادمَين لازمٌ لا اكتشاف.
        """

        by_letter = self.by_letter
        forced: list[tuple[CollisionKey, tuple[str, ...]]] = []
        for key, letters in self.collisions:
            classes = {by_letter[letter].imported_class for letter in letters}
            if len(classes) == 1:
                forced.append((key, letters))
        return tuple(forced)


def read_triliteral_roots(
    csv_path: Path | str,
    *,
    root_column: str = ROOT_COLUMN,
    root_type_column: str = ROOT_TYPE_COLUMN,
    root_type_value: str = TRILITERAL_ROOT_TYPE,
) -> CorpusReading:
    """اقرأ الجذورَ الثلاثيّةَ من ملفِّ `csv` برفضٍ مُسمًّى لا بإسقاطٍ صامت.

    الأعمدةُ مطلوبةٌ بأسمائها، وغيابُ أيٍّ منها رفضٌ لا تخمين. والطيُّ يسبق شرطَ
    الطول، فجذرٌ مكتوبٌ بهمزةٍ على كرسيّ لا يسقط لأنّ صورتَه غيرُ مطويّة.
    """

    path = Path(csv_path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        for required in (root_column, root_type_column):
            if required not in fieldnames:
                raise LetterFingerprintError(
                    f"العمودُ {required!r} مفقودٌ في المدوَّنة؛ لا يُخمَّن بديلُه."
                )
        return _read_rows(reader, root_column, root_type_column, root_type_value)


def _read_rows(
    rows: Iterable[Mapping[str, str | None]],
    root_column: str,
    root_type_column: str,
    root_type_value: str,
) -> CorpusReading:
    accepted: list[str] = []
    exclusions: list[RootExclusion] = []
    for index, row in enumerate(rows):
        raw_root = (row.get(root_column) or "").strip()
        declared_type = unicodedata.normalize(
            NORMALIZATION_FORM, (row.get(root_type_column) or "")
        ).strip()
        if declared_type != unicodedata.normalize(NORMALIZATION_FORM, root_type_value):
            exclusions.append(
                RootExclusion(index, raw_root, ExclusionReason.ROOT_TYPE_NOT_TRILITERAL)
            )
            continue
        folded = fold_root(raw_root)
        if not folded:
            exclusions.append(
                RootExclusion(index, raw_root, ExclusionReason.EMPTY_ROOT)
            )
            continue
        if len(folded) != _TRILITERAL_LENGTH:
            exclusions.append(
                RootExclusion(index, raw_root, ExclusionReason.LENGTH_NOT_THREE)
            )
            continue
        if any(letter not in LETTER_VOCABULARY for letter in folded):
            exclusions.append(
                RootExclusion(index, raw_root, ExclusionReason.LETTER_OUT_OF_VOCABULARY)
            )
            continue
        accepted.append(folded)
    return CorpusReading(tuple(accepted), tuple(exclusions))


def compute_fingerprint_census(roots: Sequence[str]) -> FingerprintCensus:
    """احسب جدولَ البصمات من جذورٍ مطويّةٍ ثلاثيّةٍ بحروفٍ من المفردة المغلقة."""

    if not roots:
        raise LetterFingerprintError("المسحُ لا يقع على مدوَّنةٍ خالية.")
    first: dict[str, int] = dict.fromkeys(LETTER_VOCABULARY, 0)
    second: dict[str, int] = dict.fromkeys(LETTER_VOCABULARY, 0)
    third: dict[str, int] = dict.fromkeys(LETTER_VOCABULARY, 0)
    for root in roots:
        if len(root) != _TRILITERAL_LENGTH:
            raise LetterFingerprintError("الجذرُ المقيسُ ثلاثيٌّ بعد الطيّ.")
        for position, bucket in enumerate((first, second, third)):
            letter = root[position]
            if letter not in bucket:
                raise LetterFingerprintError(f"حرفٌ خارج المفردة المغلقة: {letter!r}.")
            bucket[letter] += 1
    corpus_size = len(roots)
    counts = tuple(
        LetterPositionCounts(letter, first[letter], second[letter], third[letter])
        for letter in LETTER_VOCABULARY
    )
    fingerprints = tuple(
        LetterFingerprint(
            letter=count.letter,
            preferred_position=count.preferred_position,
            root_share_percent=round_half_up_percent(count.total, corpus_size),
            is_ithlaq=count.letter in ITHLAQ_LETTERS,
            role_count=IMPORTED_ROLE_COUNTS[count.letter],
        )
        for count in counts
    )
    return FingerprintCensus(corpus_size, counts, fingerprints)


def structural_collision_classes() -> (
    tuple[tuple[ImportedClassKey, tuple[str, ...]], ...]
):
    """الخاناتُ المستورَدةُ وحدَها، بلا مدوَّنة: ما يلزم قبل أيّ رصد.

    والخانةُ ذاتُ حرفين فأكثر تعني أنّ البُعدين المستورَدين لا يفصلان بينها،
    فكلُّ فصلٍ بينها واقعٌ على البُعدين المقيسين وحدهما.
    """

    grouped: dict[ImportedClassKey, list[str]] = {}
    for letter in LETTER_VOCABULARY:
        key = (letter in ITHLAQ_LETTERS, IMPORTED_ROLE_COUNTS[letter])
        grouped.setdefault(key, []).append(letter)
    return tuple((key, tuple(letters)) for key, letters in sorted(grouped.items()))


def uniform_null_unique_counts(
    *,
    corpus_size: int,
    trials: int,
    seed: int,
) -> tuple[int, ...]:
    """خطُّ الصفر: كم بصمةً فريدةً تُنتجها مدوَّناتٌ عشوائيّةٌ بنفس الحجم؟

    الجذورُ تُبنى بسحبٍ منتظمٍ من المفردة المغلقة، والبذرةُ مُعطاةٌ صراحةً
    فالنتيجةُ حتميّةٌ تُعاد. وهذا المُخرَج ليس دعوى توزيعٍ للعربيّة: هو نموذجُ
    عدمِ بنيةٍ يُقارَن به الرقمُ المرصود، وبدونه يبقى التفرُّدُ نصفَ قياس.
    """

    if corpus_size <= 0:
        raise LetterFingerprintError("حجمُ المدوَّنة عددٌ موجب.")
    if trials <= 0:
        raise LetterFingerprintError("عددُ المحاولات عددٌ موجب.")
    rng = Random(seed)
    results: list[int] = []
    for _ in range(trials):
        roots = tuple(
            "".join(rng.choice(LETTER_VOCABULARY) for _ in range(_TRILITERAL_LENGTH))
            for _ in range(corpus_size)
        )
        results.append(compute_fingerprint_census(roots).unique_fingerprint_count)
    return tuple(results)
