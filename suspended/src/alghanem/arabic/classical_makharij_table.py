"""جدولُ المخارج التقليديّ المُودَع، بديلًا عن جدولِ الجلسة المُبتكَر.

سجّلت `phonetic_economy_candidate` سببَ فشلِ الإغلاق المستقلّ بلا تلطيف: جدولُ
`PLACE_NUM` في `phonetic_economy_tool.py` **من ابتكار الجلسة، لم يُقابَل بمصدر
صوتيّاتٍ مستقلّ** — وذاك، لا فارقُ التقريب العدديّ، هو العطب. وهذه الوحدةُ
تُودِع البديلَ المطلوب: ترتيبَ المخارج السبعةَ عشرَ المعروفَ في التراث، من
أقصى الحلق إلى الشفتين.

**والترتيبُ مُثبَتٌ لا مُبتكَر**: هو ترتيبُ سيبويه في «الكتاب» (بابُ عددِ
حروفِ العربية ومخارجِها) كما استقرّ في تقسيمِ التجويد المشهور إلى سبعةَ عشرَ
مخرجًا: الحلقُ ثلاثةُ مخارج، ثمّ اللسانُ عشرة، ثمّ الشفتان اثنان، ثمّ
الخيشومُ للغنّة، ثمّ الجوفُ لحروف المدّ. وهو **خارجَ جلسةِ GFLK بالكلّية**،
مُتواترٌ في مصادر العربية والتجويد، فلا يُقال فيه ما قيل في جدولِ الجلسة.

**وحدودُ الإيداع مُسمّاةٌ لا مطويّة**، وثلاثةٌ منها تُسجَّل بقايا في وحدة
`phonetic_economy_classical_line`:

* **الترتيبُ مأخوذٌ عن التقليد لا عن طبعةٍ مُعيَّنةٍ مُودَعةٍ بصفحتها**: هذه
  الوحدةُ تُودِع بايتاتِ الجدول وتُعيد اشتقاقَ بصمتها، فيُفحَص ما هو مُودَعٌ
  فعلًا؛ ولا تدّعي مطابقةَ نصٍّ مطبوعٍ لم يُنسَخ هنا.
* **الترتيبُ تسلسلٌ، وجعلُه مسافةً خطوتُنا نحن**: التراثُ يرتّب المخارجَ من
  الحلق إلى الشفة، ولا يقول إنّ الفرقَ بين رتبتَين مقدارُ تباعدٍ صوتيّ. فرقمُ
  الرتبة مأخوذٌ عن المصدر، وطرحُ رتبةٍ من رتبةٍ ليس عنه.
* **الخيشومُ والجوفُ خارجَ الترقيم قصدًا**: الغنّةُ ليست مخرجَ حرفٍ مستقلٍّ
  بذاته في هذا القياس، وحروفُ المدّ الجوفيّةُ لا رتبةَ لها على مسارِ الفم؛
  وإقحامُهما برقمٍ يخترع ما لم يقله المصدر.

**ولا يُبدَّل جدولُ الجلسة هنا ولا يُمحى**: `phonetic_economy_tool.py` يبقى
كما سُجِّل بأرقامه ٣٫٤٣ و٩٫٩٦، فهو شاهدُ النتيجة السلبية. وهذه الوحدةُ حسابٌ
ثانٍ مستقلُّ المصدر يُقرأ إلى جانبه، لا تصحيحٌ يُزيله.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ ولا تجميدَ ولا `E0`، ولا يقرؤها
`IndependentClosureGate` ولا `BirthVerdictGate`.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from alghanem.canonical_content import canonical_digest

__all__ = [
    "CLASSICAL_MAKHARIJ",
    "CLASSICAL_METRIC_DEFINITION",
    "CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE",
    "CLASSICAL_ORDINAL",
    "CLASSICAL_SOURCE_ATTESTATION",
    "CLASSICAL_TABLE_DIGEST",
    "CLASSICAL_TABLE_MODULE_PATH",
    "JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE",
    "ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE",
    "ClassicalMakhrajError",
    "average_ordinal_distance",
    "classical_lam_f",
    "classical_nun_f",
    "classical_table_bytes",
    "rederive_classical_table_digest",
]

CLASSICAL_TABLE_MODULE_PATH: Final[str] = (
    "src/alghanem/arabic/classical_makharij_table.py"
)

CLASSICAL_SOURCE_ATTESTATION: Final[str] = (
    "ترتيبُ المخارج السبعةَ عشرَ كما في «الكتاب» لسيبويه (بابُ عددِ حروفِ "
    "العربية ومخارجِها) واستقرّ عليه تقسيمُ التجويد المشهور: الحلقُ ثلاثة، "
    "ثمّ اللسانُ عشرة، ثمّ الشفتان اثنان، ثمّ الخيشومُ للغنّة والجوفُ "
    "لحروف المدّ؛ مصدرٌ متواترٌ خارجَ جلسة GFLK بالكلّية"
)

CLASSICAL_METRIC_DEFINITION: Final[str] = (
    "فرقُ الرتبة على تسلسلِ المخارج السبعةَ عشرَ التقليديّ من أقصى الحلق "
    "إلى الشفتين، ثمّ نسبةُ متوسّطِ المجموعة البعيدة إلى متوسّطِ المجموعة "
    "القريبة؛ والتسلسلُ مأخوذٌ عن المصدر، وجعلُه مسافةً خطوةُ نمذجةٍ منّا"
)

CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE: Final[str] = (
    "CLASSICAL_ORDERING_NOT_EDITION_CITED: المُودَعُ هنا بايتاتُ الجدول "
    "وبصمتُها مُعادةُ الاشتقاق، لا نسخةٌ من طبعةٍ مُعيَّنةٍ بصفحتها؛ "
    "فالترتيبُ متواترٌ مُثبَتٌ عن التقليد، ولا يُقرأ هذا الإيداعُ مطابقةً "
    "لنصٍّ مطبوعٍ لم يُنسَخ في المستودع"
)

ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE: Final[str] = (
    "ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP: المصدرُ يرتّب المخارجَ ولا "
    "يقول إنّ الفرقَ بين رتبتَين مقدارُ تباعدٍ صوتيّ؛ فرقمُ الرتبة عن "
    "المصدر، وطرحُ رتبةٍ من رتبةٍ خطوتُنا نحن، ولا تُنسَب إليه"
)

JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE: Final[str] = (
    "JAWF_AND_KHAYSHUM_UNRANKED: الخيشومُ مخرجُ غنّةٍ لا مخرجُ حرفٍ مستقلٍّ "
    "في هذا القياس، وحروفُ المدّ الجوفيّةُ لا رتبةَ لها على مسارِ الفم؛ "
    "فتُركا خارجَ الترقيم قصدًا، وإقحامُهما برقمٍ يخترع ما لم يقله المصدر"
)


class ClassicalMakhrajError(ValueError):
    """رُفض مدخلٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


# المخارجُ بترتيبها التقليديّ: الرتبةُ، واسمُ المخرج، وحروفُه.
CLASSICAL_MAKHARIJ: Final[tuple[tuple[int, str, str], ...]] = (
    (1, "أقصى الحلق", "ءه"),
    (2, "وسط الحلق", "عح"),
    (3, "أدنى الحلق", "غخ"),
    (4, "أقصى اللسان مع الحنك اللحمي", "ق"),
    (5, "أقصى اللسان مع الحنك العظمي", "ك"),
    (6, "وسط اللسان", "جشي"),
    (7, "حافة اللسان مع الأضراس", "ض"),
    (8, "أدنى حافة اللسان مع اللثة", "ل"),
    (9, "طرف اللسان مع لثة الثنايا العليا", "ن"),
    (10, "ظهر طرف اللسان مع اللثة", "ر"),
    (11, "طرف اللسان مع أصول الثنايا العليا", "طدت"),
    (12, "طرف اللسان بين الثنايا العليا والسفلى", "صزس"),
    (13, "طرف اللسان مع أطراف الثنايا العليا", "ظذث"),
    (14, "باطن الشفة السفلى مع أطراف الثنايا العليا", "ف"),
    (15, "الشفتان بانطباق", "بم"),
    (16, "الشفتان بانفتاح", "و"),
)


def _build_ordinals() -> MappingProxyType[str, int]:
    ordinals: dict[str, int] = {}
    for rank, name, letters in CLASSICAL_MAKHARIJ:
        if not letters:
            raise ClassicalMakhrajError(f"مخرجٌ بلا حرفٍ واحد: {name}.")
        for letter in letters:
            if letter in ordinals:
                raise ClassicalMakhrajError(
                    f"حرفٌ في مخرجَين: {letter}؛ ورتبتان لحرفٍ واحدٍ تخلطان "
                    "هويّتَين تحت رقمٍ واحد."
                )
            ordinals[letter] = rank
    return MappingProxyType(ordinals)


CLASSICAL_ORDINAL: Final[MappingProxyType[str, int]] = _build_ordinals()

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"


def classical_table_bytes() -> bytes:
    """رمِّز الجدولَ بدقّة البايت: «رتبة U+001F حروف»، مفصولةً بـU+001E.

    لا تطبيعَ هنا قصدًا: الجدولُ المُودَعُ هو بايتاتُه، وتطبيعُنا إيّاه يجعل
    البصمةَ بصمةَ نصٍّ آخرَ ثمّ يُسمّى الاختلافُ تطابقًا.
    """

    lines = [
        f"{rank}{_FIELD_SEPARATOR}{letters}"
        for rank, _name, letters in CLASSICAL_MAKHARIJ
    ]
    return _RECORD_SEPARATOR.join(lines).encode("utf-8")


def rederive_classical_table_digest() -> str:
    """أعِد اشتقاقَ بصمةِ الجدول من بايتاته الآن، لا من رقمٍ منسوخٍ في حقل."""

    return canonical_digest(classical_table_bytes())


CLASSICAL_TABLE_DIGEST: Final[str] = rederive_classical_table_digest()


def average_ordinal_distance(letters: frozenset[str], target_rank: int) -> float:
    """متوسّطُ |رتبة(c) − target_rank| عبر مجموعةِ حروف؛ وحرفٌ بلا رتبةٍ يُرَدّ.

    ولا يُتجاوَز حرفٌ صامتًا: الحرفُ الذي لا رتبةَ له في الجدول المُودَع
    إسقاطُه يُغيّر المتوسّطَ بلا أثرٍ ظاهر، فيُرَدُّ صريحًا.
    """

    if not letters:
        raise ClassicalMakhrajError("المتوسّطُ يُحسَب على مجموعةٍ غيرِ فارغة.")
    missing = sorted(letter for letter in letters if letter not in CLASSICAL_ORDINAL)
    if missing:
        raise ClassicalMakhrajError(
            "حروفٌ لا رتبةَ لها في الجدول المُودَع: "
            + "، ".join(missing)
            + "؛ وإسقاطُها صمتًا يُغيّر المتوسّطَ بلا أثرٍ ظاهر."
        )
    distances = [abs(CLASSICAL_ORDINAL[letter] - target_rank) for letter in letters]
    return sum(distances) / len(distances)


def _ratio(far: frozenset[str], near: frozenset[str], anchor: str) -> float:
    rank = CLASSICAL_ORDINAL[anchor]
    near_average = average_ordinal_distance(near, rank)
    if near_average == 0:
        raise ClassicalMakhrajError("نسبةٌ على متوسّطٍ صفرٍ لا تُحسَب.")
    return average_ordinal_distance(far, rank) / near_average


def classical_nun_f() -> float:
    """نسبةُ الإظهار إلى الإدغام عند النون الساكنة، بالجدول التقليديّ المُودَع."""

    from .phonetic_economy_tool import IDGHAM_NUN_LETTERS, IZHAR_NUN_LETTERS

    return _ratio(IZHAR_NUN_LETTERS, IDGHAM_NUN_LETTERS, "ن")


def classical_lam_f() -> float:
    """نسبةُ القمريّ إلى الشمسيّ عند لام التعريف، بالجدول التقليديّ المُودَع."""

    from .phonetic_economy_tool import MOON_LETTERS_REAL, SUN_LETTERS

    return _ratio(MOON_LETTERS_REAL, SUN_LETTERS, "ل")


if len(CLASSICAL_MAKHARIJ) != 16:  # pragma: no cover - حارس
    raise RuntimeError(
        "مخارجُ الحروف المرقَّمةُ ستّةَ عشرَ، والسابعَ عشرَ خيشومُ الغنّة "
        "وهو خارجَ الترقيم قصدًا."
    )
if len(CLASSICAL_ORDINAL) != 28:  # pragma: no cover - حارس
    raise RuntimeError(
        "الحروفُ المرقَّمةُ ثمانيةٌ وعشرون؛ ونقصُ حرفٍ يجعل متوسّطًا يُحسَب " "على غير مجموعته."
    )


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويٌّ للفحص
    print(f"F(نون) = {classical_nun_f():.2f}")
    print(f"F(لام) = {classical_lam_f():.2f}")
    print(f"بصمةُ الجدول = {CLASSICAL_TABLE_DIGEST}")
    print()
    print(CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE)
    print(ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE)
    print(JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE)
