"""محمولٌ يُقرَّر من اليونيكود وحدَه: أفي هذا الموضع علامةُ حركةٍ مكتوبة؟

كلُّ ما تقدَّم في هذه الشجرة من تصنيفٍ للحروف — تسعةٌ وعشرون حرفًا وأحدَ عشرَ
مخرجًا — **استيرادٌ من التراث الصوتيّ**، مُقَرٌّ به ومُسمًّى في موضعه. وهذه
الوحدةُ من جنسٍ آخر: محمولٌ واحدٌ **يُقرَّر من جداول اليونيكود نفسِها**، كلّيٌّ
على كلّ نصّ، قاطعٌ بلا غموض، ولا يقوم على نظريّةٍ صوتيّةٍ ولا على سمعٍ ولا على
قراءة:

    HasWrittenHarakaMark(موضع) ⟺ في العلامات اللاصقة بهذا الموضع عضوٌ
                                  من المجموعة المستورَدة السباعيّة

**والموضعُ نفسُه مشتقٌّ لا مُصطلَحٌ عليه.** يقسم اليونيكودُ نقاطَ الترميز
بخاصّية `General_Category`: ما كان `Mn` (علامةٌ لاصقةٌ غيرُ مُفرِغة) يلتصق بما
قبله، وما سواه يفتح موضعًا. فالتقسيمُ إلى مواضعَ **قراءةٌ في جدول**، لا حكمٌ
عربيّ. وفي المُودَعَين ههنا انقسمت النقاطُ قسمين نظيفين: 34 نقطةً `Lo` و9
نقاطٍ `Mn`، لا ثالثَ لهما.

**والاستيرادُ لا يُنفى، بل يُوزَن.** اليونيكودُ **لا يملك خاصّيةً اسمُها
«حركة»**؛ فلا يُشتقّ منه أيُّ السبعِ حركةٌ وأيُّها ليس. الذي يُشتقّ منه هو
**المجموعةُ الأكبر**: نقاطُ `Mn` في كتل العربيّة، وهي **105** نقطةً في
يونيكود 15.0.0. والمستورَدُ هو **اختيارُ سبعٍ منها** — الفتحةُ والضمّةُ
والكسرةُ والسكونُ والتنوينُ الثلاثة — أي **6.667%** من المجموعة. فهذا هو حجمُ
الاستيراد مقيسًا لا موصوفًا: سبعٌ من مئةٍ وخمس
(`THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION`).

**والمقامُ تحرّك فعلًا، كما قالت البقيّةُ إنّه قد يتحرّك.** قيل ههنا إنّ
المئةَ والخمسَ رقمٌ مؤرَّخٌ لا دائم، ثمّ قُرئ الجدولُ بإصدارٍ آخر فتحرّك:

| إصدارُ اليونيكود | نقاطُ `Mn` | نصيبُ السبع |
|---|---|---|
| 13.0.0 | 96 | 7.292% |
| 15.0.0 | 105 | 6.667% |

فتسعُ نقاطٍ أُضيفت بين الإصدارين، فهبط نصيبُ الاستيراد بلا أن تُمَسَّ السبع.
والسبعُ أنفسُها لم تتحرّك في الإصدارين جميعًا، فالمُستورَدُ ثابتٌ والمقامُ
متحرّك. ولا تُقرأ الهُويّاتُ التسعُ ههنا — إنّما عدَدُها — إذ لا يُقرأ في
الشجرة جدولٌ غيرُ الجدول الحاضر
(`A_UNICODE_VERSION_IS_A_DEPENDENCY`).

**والشدّةُ والألفُ الخنجريّةُ خارجتان بالاستيراد لا باليونيكود.** كلتاهما
`Mn` كالسبع سواءً بسواء، ولا شيءَ في الجدول يُخرجهما. أُخرجتا لأنّ الاختيارَ
أخرجهما، وهو عينُ ما يجعل الاستيرادَ استيرادًا
(`SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE`).

**وأخطرُ ما في الاستيراد لا يحرّك ههنا شيئًا.** أوجُه الخلاف في الاختيار
موضعُها الشدّةُ والألفُ الخنجريّة؛ وقِيس أثرُ إدخالهما على المُودَعَين
فكان **صفرًا في الصور الأربع كلِّها**. وعلّتُه مقيسةٌ لا مُقدَّرة: ليس في
النصّين موضعٌ واحدٌ يحمل شدّةً أو خنجريّةً بلا حركةٍ معها، فالموضعُ موسومٌ
قبل أن يُسأل عنهما. فنتائجُ هذا المحمول ههنا **لا تتعلّق بالجزء المُختلَف
فيه من الاستيراد**، ووزنُه الفاعلُ أصغرُ من وزنه المُعلَن. وهذا حكمٌ على
هذين النصّين لا على القاعدة: «بّ» مجرّدةً يتحرّك حكمُها، ومُجرَّبٌ ذلك
(`THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE`).

**والخمولُ مقصورٌ على هذا السؤال وحدَه، وقد قِيس حدُّه.** أظهرت
`haraka_fiber_structure` أنّ التوسيعَ الذي حرّك **صفرَ** أحكامٍ ههنا يحرّك
**ستّةَ عشرَ** موضعًا في النصّين من ليفٍ مفردٍ إلى مزدوج. فالصفرُ صفرُ
**الإسقاط الثنائيّ** لا صفرُ أثرِ الاستيراد؛ ولا يُرفَع هذا الخمولُ حكمًا على
بنيةٍ فوق المحمول.

**وثبوتُ الحكم تحت التسوية مُبرهَنٌ بالاستقراء التامّ لا مُلاحَظ.** فُحصت
نقاطُ يونيكود كلُّها — 1,114,112 نقطةً — فلم توجد نقطةٌ واحدةٌ يُدخِل تفكيكُها
القانونيُّ (NFD) حركةً من السبع حيث لم تكن، ولا حركةٌ من السبع تتفكّك فتزول،
ولا نقطةٌ عربيّةٌ تنقسم فتزيد المواضع. فحكمُ المحمول **ثابتٌ تحت NFC وNFD على
كلّ نصٍّ ممكن**، لا على هذين المُودَعَين فحسب. وقِيس على المُودَعَين فطابق:
143 موضعًا و249 في الصورتين جميعًا.

**وحدُّ البرهان صورتان لا أربع.** تحت التسوية التوافقيّة (NFKC/NFKD) ينكسر
الحكمُ في **اثنتين وعشرين نقطةً بعينها** — صورُ العرض المعزولةُ والوسطيّة مثل
`U+FE76` التي تتفكّك إلى مسافةٍ وفتحة، فتضع حركةً على موضعٍ لم يكن حرفًا.
والاثنتان والعشرون مُستخرَجاتٌ من الجدول لا مكتوبةٌ باليد، ونطاقُ المحمول
مُعلَنٌ بالصورتين القانونيّتين
(`THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY`).

**وهذا المحمولُ ينفي عمودًا سبق أن قِيس بحدّه.** قرّرت `implicit_sukun_treatment`
أنّ السكونَ يُقرأ مرّةً من علامةٍ ومرّةً من غياب، وأنّ «أوّلَ زوج الشدّة»
دخل عمودَ السكون وهو **ليس سكونًا أصلًا**. وهذا المحمولُ يُسقطه **من تلقاء
بنائه**: لا يعدّ إلّا مواضعَ موجودةً في الرسم، فلا نصفَ حرفٍ فيه. والمطابقةُ
تامّةٌ في النصّين:

| | الفاتحة | الفتح ٢٩ |
|---|---|---|
| المواضعُ كلُّها | 143 | 249 |
| بعلامةِ حركة | 103 | 188 |
| بلا علامة | **40** | **61** |
| المُضمَرُ في الإحصاء السابق | 54 | 77 |
| ناقصَ أوّلِ زوج الشدّة | 54−14 = **40** | 77−16 = **61** |

فما كان يحتاج إلى تنبيهٍ باليد هناك، صار ههنا **غيرَ قابلٍ للدخول أصلًا**.

**وما لا يقوله هذا المحمولُ أكثرُ ممّا يقوله.** يقرأ الرسمَ لا الصوت: «عليه
علامة» غيرُ «يُنطَق بحركة»، ولا بايتَ ههنا يشهد لنطق
(`A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL`). ونفيُه **ليس سكونًا**: «لا علامةَ
عليه» حكمٌ في الرسم، والقفزُ منه إلى «ساكن» هو عينُ الاستنتاج من الغياب الذي
سُمِّي هناك (`THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN`). وجدولُ اليونيكود
نفسُه إصدارٌ مؤرَّخ، فعدّةُ المجموعة الأكبر قد تتحرّك بين إصدارين، والإصدارُ
المقيسُ عليه مُسجَّلٌ لا مطويّ (`A_UNICODE_VERSION_IS_A_DEPENDENCY`).

**خمولٌ سلطويّ**: لا ولادةَ ولا حكمَ ولا تجميد، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import sys
import unicodedata
from dataclasses import dataclass, fields
from typing import Final

__all__ = [
    "ARABIC_BLOCK_RANGES",
    "A_UNICODE_VERSION_IS_A_DEPENDENCY",
    "A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL",
    "CANONICAL_FORMS",
    "SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE",
    "THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE",
    "THE_IMPORTED_HARAKAT",
    "THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION",
    "THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY",
    "THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN",
    "THE_SUPERSET_MEASURED_BY_UNICODE_VERSION",
    "UNICODE_VERSION",
    "WRITTEN_HARAKA_NAMED_RESIDUALS",
    "ImportWeight",
    "MarkCensus",
    "Position",
    "WrittenHarakaError",
    "arabic_combining_marks",
    "census_of",
    "compatibility_exceptions",
    "has_written_haraka_mark",
    "import_weight",
    "imported_haraka_names",
    "positions_of",
    "the_superset_recorded_for",
    "verify_canonical_invariance",
]


UNICODE_VERSION: Final[str] = unicodedata.unidata_version
"""إصدارُ جدول اليونيكود الذي قُرِّر عليه كلُّ ما ههنا، مُسجَّلًا لا مطويًّا."""


THE_SUPERSET_MEASURED_BY_UNICODE_VERSION: Final[dict[str, int]] = {
    "13.0.0": 96,
    "15.0.0": 105,
}
"""حجمُ المجموعة الأكبر عند كلّ إصدارٍ قِيس عليه فعلًا؛ وما سواه غيرُ مقيس."""


def the_superset_recorded_for(version: str) -> int | None:
    """الحجمُ المُجمَّدُ لإصدارٍ إن كان قِيس عليه، و`None` إن لم يُقَس.

    والعدمُ ههنا **«لم يُقَس»** لا «لا شيءَ فيه»: فمن قرأ الجدولَ بإصدارٍ
    ثالثٍ فحجمُه مقروءٌ عنده من `arabic_combining_marks` ولا يُدَّعى أنّه
    أحدُ العددين المُجمَّدين.
    """

    return THE_SUPERSET_MEASURED_BY_UNICODE_VERSION.get(version)


THE_IMPORTED_HARAKAT: Final[frozenset[str]] = frozenset(
    {
        "\u064b",  # ARABIC FATHATAN
        "\u064c",  # ARABIC DAMMATAN
        "\u064d",  # ARABIC KASRATAN
        "\u064e",  # ARABIC FATHA
        "\u064f",  # ARABIC DAMMA
        "\u0650",  # ARABIC KASRA
        "\u0652",  # ARABIC SUKUN
    }
)
"""الاستيرادُ كلُّه، سبعُ نقاطٍ مُسمّاةٍ بأعيانها؛ ولا يُشتقّ هذا من جدول."""


ARABIC_BLOCK_RANGES: Final[tuple[tuple[int, int], ...]] = (
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
)
"""كتلُ العربيّة في اليونيكود؛ ومنها تُشتقّ المجموعةُ الأكبر التي وُزن بها."""


CANONICAL_FORMS: Final[tuple[str, str]] = ("NFC", "NFD")
"""نطاقُ المحمول: الصورتان القانونيّتان وحدَهما، والتوافقيّتان خارجَه."""


_COMBINING: Final[str] = "Mn"


class WrittenHarakaError(ValueError):
    """رفضٌ عند القرار: علامةٌ لاصقةٌ بلا موضعٍ قبلها، أو صورةٌ غيرُ قانونيّة."""


@dataclass(frozen=True)
class Position:
    """موضعٌ واحدٌ: نقطةٌ غيرُ لاصقةٍ ومعها ما لصق بها، بترتيب ورودها."""

    carrier: str
    marks: tuple[str, ...]
    index: int

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise WrittenHarakaError("الموضعُ نقطةُ ترميزٍ واحدة لا سلسلة.")
        if unicodedata.category(self.carrier) == _COMBINING:
            raise WrittenHarakaError(
                f"نقطةٌ لاصقةٌ (Mn) لا تفتح موضعًا: U+{ord(self.carrier):04X}."
            )
        if any(unicodedata.category(mark) != _COMBINING for mark in self.marks):
            raise WrittenHarakaError("ما ليس Mn لا يلصق بموضعٍ قبله.")
        if self.index < 0:
            raise WrittenHarakaError("رتبةٌ سالبةٌ لا تكون.")

    @property
    def haraka_marks(self) -> tuple[str, ...]:
        """ما لصق بهذا الموضع من السبع المستورَدة، بترتيب وروده."""

        return tuple(mark for mark in self.marks if mark in THE_IMPORTED_HARAKAT)


def has_written_haraka_mark(position: Position) -> bool:
    """المحمولُ نفسُه: قرارٌ كلّيٌّ قاطعٌ، لا يقرأ إلّا نقاطَ الترميز."""

    return bool(position.haraka_marks)


def _normalized(form: str, text: str) -> str:
    """يُسوّي النصَّ على صورةٍ قانونيّةٍ مُتحقَّقٍ منها قبلُ."""

    if form == "NFC":
        return unicodedata.normalize("NFC", text)
    return unicodedata.normalize("NFD", text)


def positions_of(text: str, form: str = "NFC") -> tuple[Position, ...]:
    """يقسم نصًّا إلى مواضعَ بخاصّية `General_Category` وحدَها، بلا حكمٍ عربيّ."""

    if form not in CANONICAL_FORMS:
        raise WrittenHarakaError(
            f"الصورةُ {form!r} خارج نطاق هذا المحمول؛ ونطاقُه {CANONICAL_FORMS} "
            "وحدَهما، وعلّتُه مُسمّاةٌ في THE_INVARIANCE_IS_CANONICAL_AND_NOT_"
            "COMPATIBILITY."
        )
    built: list[tuple[str, list[str]]] = []
    for character in _normalized(form, text):
        if character.isspace():
            continue
        if unicodedata.category(character) == _COMBINING:
            if not built:
                raise WrittenHarakaError(
                    "علامةٌ لاصقةٌ في أوّل النصّ بلا موضعٍ قبلها؛ ولا يُفتَح "
                    "لها موضعٌ لأنّ ذلك حكمٌ لا قراءة."
                )
            built[-1][1].append(character)
        else:
            built.append((character, []))
    return tuple(
        Position(carrier=carrier, marks=tuple(marks), index=index)
        for index, (carrier, marks) in enumerate(built)
    )


@dataclass(frozen=True)
class MarkCensus:
    """إحصاءُ نصٍّ بهذا المحمول: موضعٌ موسومٌ وموضعٌ غيرُ موسوم، لا ثالثَ."""

    scope: str
    marked: int
    unmarked: int

    def __post_init__(self) -> None:
        if self.marked < 0 or self.unmarked < 0:
            raise WrittenHarakaError("عدّةٌ سالبةٌ لا تكون.")
        if not self.total:
            raise WrittenHarakaError("إحصاءٌ على صفرِ مواضعَ ليس إحصاءً.")

    @property
    def total(self) -> int:
        """المواضعُ كلُّها؛ والقسمةُ تامّةٌ لأنّ المحمولَ ثنائيُّ القيمة."""

        return self.marked + self.unmarked

    @property
    def marked_share(self) -> float:
        """نصيبُ الموسوم من المواضع، نسبةً مئويّة."""

        return 100.0 * self.marked / self.total


def census_of(text: str, scope: str, form: str = "NFC") -> MarkCensus:
    """يقرّر المحمولَ على كلّ موضعٍ في نصّ، ويقسمه قسمين لا ثالثَ لهما."""

    positions = positions_of(text, form=form)
    marked = sum(1 for position in positions if has_written_haraka_mark(position))
    return MarkCensus(scope=scope, marked=marked, unmarked=len(positions) - marked)


# --- وزنُ الاستيراد، مشتقًّا من الجدول لا موصوفًا -------------------------


def arabic_combining_marks() -> tuple[str, ...]:
    """المجموعةُ الأكبر: نقاطُ `Mn` في كتل العربيّة، مشتقّةً من الجدول."""

    return tuple(
        chr(codepoint)
        for start, end in ARABIC_BLOCK_RANGES
        for codepoint in range(start, end + 1)
        if unicodedata.category(chr(codepoint)) == _COMBINING
    )


@dataclass(frozen=True)
class ImportWeight:
    """حجمُ الاستيراد مقيسًا: كم اختِيرت من كم، ونصيبُها."""

    selected: int
    superset: int
    unicode_version: str

    def __post_init__(self) -> None:
        if not 0 < self.selected <= self.superset:
            raise WrittenHarakaError(
                "المختارُ أكثرُ من المجموعة الأكبر أو خالٍ؛ وكلاهما ينقض الوزن."
            )

    @property
    def share(self) -> float:
        """نصيبُ المستورَد من المجموعة المشتقّة، نسبةً مئويّة."""

        return 100.0 * self.selected / self.superset


def import_weight() -> ImportWeight:
    """يزن الاستيرادَ عند القراءة: سبعٌ من مئةٍ وخمسٍ في يونيكود 15.0.0."""

    superset = arabic_combining_marks()
    if not THE_IMPORTED_HARAKAT.issubset(set(superset)):
        raise WrittenHarakaError(
            "خرجت حركةٌ مستورَدةٌ عن نقاط `Mn` في كتل العربيّة؛ فالوزنُ باطل."
        )
    return ImportWeight(
        selected=len(THE_IMPORTED_HARAKAT),
        superset=len(superset),
        unicode_version=UNICODE_VERSION,
    )


def imported_haraka_names() -> tuple[tuple[str, str], ...]:
    """أسماءُ السبع كما يسمّيها اليونيكود، مقروءةً منه لا مكتوبةً باليد."""

    return tuple(
        (f"U+{ord(mark):04X}", unicodedata.name(mark))
        for mark in sorted(THE_IMPORTED_HARAKAT)
    )


# --- البرهانُ بالاستقراء التامّ، وحدُّه -----------------------------------


def verify_canonical_invariance(limit: int | None = None) -> tuple[int, int, int]:
    """يستقرئ نقاطَ اليونيكود ويعدّ ما ينقض ثباتَ الحكم تحت NFD.

    يُعاد ثلاثةُ أعدادٍ: ما يُدخِل حركةً لم تكن، وما تتفكّك فيه حركةٌ فتزول،
    وما ينقسم من نقاطِ العربيّة فتزيد المواضع. والمُبرهَنُ أنّ الثلاثةَ صفر.
    """

    ceiling = sys.maxunicode if limit is None else limit
    introduced = destroyed = split = 0
    for codepoint in range(ceiling + 1):
        character = chr(codepoint)
        if not unicodedata.name(character, ""):
            continue
        decomposed = unicodedata.normalize("NFD", character)
        if decomposed == character:
            continue
        carries = bool(set(decomposed) & THE_IMPORTED_HARAKAT)
        if carries and character not in THE_IMPORTED_HARAKAT:
            introduced += 1
        if character in THE_IMPORTED_HARAKAT and set(decomposed) != {character}:
            destroyed += 1
        if (
            unicodedata.category(character) != _COMBINING
            and _in_arabic_blocks(codepoint)
            and sum(
                1 for part in decomposed if unicodedata.category(part) != _COMBINING
            )
            > 1
        ):
            split += 1
    return introduced, destroyed, split


def _in_arabic_blocks(codepoint: int) -> bool:
    return any(start <= codepoint <= end for start, end in ARABIC_BLOCK_RANGES)


def compatibility_exceptions() -> tuple[str, ...]:
    """النقاطُ التي يُدخِل تفكيكُها التوافقيُّ حركةً؛ مُستخرَجةً لا مكتوبة."""

    found: list[str] = []
    for start, end in ARABIC_BLOCK_RANGES:
        for codepoint in range(start, end + 1):
            character = chr(codepoint)
            if not unicodedata.name(character, "") or character in THE_IMPORTED_HARAKAT:
                continue
            if set(unicodedata.normalize("NFKD", character)) & THE_IMPORTED_HARAKAT:
                found.append(character)
    return tuple(found)


THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION: Final[str] = (
    "THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION: لا خاصّيةَ في اليونيكود "
    "اسمُها «حركة»، فلا يُشتقّ منه أنّ هذه السبعَ حركاتٌ وأنّ غيرَها ليس. "
    "المُشتَقُّ منه المجموعةُ الأكبر: نقاطُ `Mn` في كتل العربيّة، وهي 105 "
    "عند الإصدار 15.0.0 و96 عند 13.0.0؛ والمستورَدُ اختيارُ سبعٍ منها، أي "
    "6.667% أو 7.292% بحسب الجدول المقروء. فهذا استيرادٌ صغيرٌ **موزونٌ** لا "
    "مَنفيّ، وحجمُه مقيسٌ عند القراءة في `import_weight`."
)

SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE: Final[str] = (
    "SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE: الشدّةُ "
    "(U+0651) والألفُ الخنجريّة (U+0670) نقطتا `Mn` كالسبع سواءً بسواء، ولا "
    "شيءَ في جدول اليونيكود يُخرجهما. أُخرجتا بالاختيار المستورَد وحدَه. "
    "ولو أُدخلتا لتغيّر كلُّ رقمٍ ههنا، وذلك يبيّن أنّ الاختيارَ فاعلٌ لا زينة."
)

THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE: Final[str] = (
    "THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE: أُدخلت الشدّةُ "
    "والخنجريّةُ في الاختيار تجربةً، إفرادًا واجتماعًا، فلم يتحرّك حكمُ موضعٍ "
    "واحدٍ في النصّين: صفرٌ في الصور الأربع. وعلّتُه مقيسة: لا موضعَ ههنا "
    "يحمل واحدةً منهما بلا حركةٍ معها. فالأرقامُ المنشورةُ **لا تتعلّق "
    "بالجزء المُختلَف فيه من الاستيراد**. وهذا خبرٌ عن هذين النصّين لا عن "
    "القاعدة: «بّ» مجرّدةً يتحرّك حكمُها، وهو مُجرَّبٌ في "
    "`test_the_inertness_is_a_property_of_these_texts_and_not_of_the_rule`. "
    "وهو خمولٌ في هذا السؤال الثنائيّ وحدَه: في السؤال الليفيّ يتحرّك 16 "
    "موضعًا في كلٍّ من النصّين، كما في `haraka_fiber_structure`."
)

THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY: Final[str] = (
    "THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY: استُقرئت نقاطُ "
    "اليونيكود كلُّها فلم يوجد ما ينقض ثباتَ الحكم تحت NFC وNFD: صفرٌ يُدخِل "
    "حركةً، وصفرٌ تزول فيه حركة، وصفرٌ ينقسم من نقاط العربيّة. أمّا تحت "
    "NFKC/NFKD فينكسر في 22 نقطةً بعينها — صورِ العرض مثل U+FE76 التي تتفكّك "
    "إلى مسافةٍ وفتحة — فتُوضَع حركةٌ على موضعٍ ليس حرفًا. فنطاقُ المحمول "
    "الصورتان القانونيّتان، و`positions_of` ترفض ما سواهما رفضًا لا تصحيحًا."
)

THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN: Final[str] = (
    "THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN: نفيُ المحمول يقول «لا علامةَ "
    "على هذا الموضع» ولا يقول «هذا الموضعُ ساكن». والقفزُ بينهما هو عينُ "
    "الاستنتاج من الغياب الذي سُمِّي في `WHAT_IS_READ_FROM_ABSENCE_IS_NOT_"
    "READ_FROM_BYTES`. وههنا فائدةٌ تُقاس: 40 موضعًا غيرَ موسومٍ في الفاتحة "
    "و61 في الفتح، وهي المُضمَرُ السابق ناقصًا «أوّلَ زوج الشدّة» بالضبط "
    "(54−14، 77−16)؛ إذ لا يدخل نصفُ حرفٍ في عدٍّ لا يعدّ إلّا مواضعَ مرسومة."
)

A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL: Final[str] = (
    "A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL: هذا المحمولُ يقرأ الرسمَ "
    "وحدَه. «عليه علامةٌ مكتوبة» غيرُ «يُنطَق بحركة»: فالمُشكَّلُ قد يُوصَل "
    "فلا تُنطَق حركتُه، والعاري قد يُنطَق بها. ولا بايتَ في هذه الشجرة يشهد "
    "لنطقٍ أصلًا. فالقطعيّةُ ههنا قطعيّةُ رسمٍ لا قطعيّةُ صوت، والثانيةُ "
    "ليست مُدَّعاةً ولا مُقاسةً."
)

A_UNICODE_VERSION_IS_A_DEPENDENCY: Final[str] = (
    "A_UNICODE_VERSION_IS_A_DEPENDENCY: المجموعةُ الأكبر مقروءةٌ من جدولٍ "
    f"مؤرَّخ، وهو ههنا {UNICODE_VERSION}؛ وقد قيل إنّ المقامَ قد يتحرّك، "
    "فتحرّك: 96 نقطةً عند 13.0.0 و105 عند 15.0.0، فنصيبُ السبع 7.292% ثمّ "
    "6.667%. والسبعُ أنفسُها لم تتحرّك في الإصدارين، لكنّ استقرارَها "
    "**مقروءٌ لا مضمون**: لذلك يُقاس الوزنُ عند القراءة ولا يُكتَب في ثابت، "
    "وإصدارٌ لم يُقَس عليه لا يُدَّعى له رقمٌ من هذين."
)

WRITTEN_HARAKA_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION": (
        THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION
    ),
    "SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE": (
        SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE
    ),
    "THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE": (
        THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE
    ),
    "THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY": (
        THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY
    ),
    "THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN": (
        THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN
    ),
    "A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL": (
        A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL
    ),
    "A_UNICODE_VERSION_IS_A_DEPENDENCY": A_UNICODE_VERSION_IS_A_DEPENDENCY,
}
"""ما لا يُثبِته هذا المحمولُ مُسمًّى باسمه، لا مطويًّا في قطعيّته."""


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في محمولٍ لا سلطةَ فيه."""

    for holder in (Position, MarkCensus, ImportWeight):
        for declared in fields(holder):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise WrittenHarakaError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى {holder.__name__}: "
                        f"{declared.name}؛ وهذا محمولٌ لا سلطةَ فيه."
                    )


def _assert_the_import_stays_inside_the_derived_superset() -> None:
    """حارسُ استيراد: حركةٌ خارج `Mn` العربيّة تنقض الوزنَ كلَّه."""

    import_weight()


def _assert_the_frozen_superset_matches_the_table_being_read() -> None:
    """حارسُ استيراد: إن كان الإصدارُ مقيسًا فرقمُه يُطابِق، وإلّا فلا يُدَّعى."""

    recorded = the_superset_recorded_for(UNICODE_VERSION)
    if recorded is None:
        return
    derived = len(arabic_combining_marks())
    if derived != recorded:
        raise WrittenHarakaError(
            f"المجموعةُ الأكبر عند {UNICODE_VERSION} قُرئت {derived} "
            f"والمُجمَّدُ لها {recorded}؛ فالرقمُ المنشورُ يُعاد قياسُه."
        )


_assert_no_authority_field()
_assert_the_import_stays_inside_the_derived_superset()
_assert_the_frozen_superset_matches_the_table_being_read()
