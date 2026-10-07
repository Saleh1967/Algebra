"""آيةٌ عربيّةٌ ثانيةٌ مُودَعةٌ بحروفها، ومعه جنسُ تحقُّقها لا دعوى إسنادها.

قامت هذه الوحدةُ على ما قرّرته `fatiha_source_text`: لا رقمَ يُشتقّ من نصٍّ
غيرِ مُودَع، فما لم تكن حروفُه في الشجرة فلا يُعاد اشتقاقُ رقمه. وأُريد قياسٌ
على مادّةٍ غيرِ الفاتحة، فأُودعت هنا الآيةُ التاسعةُ والعشرون من سورة الفتح
لتكون **موضوعَ قياسٍ ثانيًا معلومًا** تُجرى عليه تجربةُ الطبقة المرجعيّة في
`reference_articulation_layer`::

    DepositedText     != CollatedText
    PublicDomainMatn  != AttributedEdition
    SimplifiedRasm    != AnyPrintedRasm

**والمُودَعُ نقلٌ مُبسَّطٌ لم يُقابَل.** كُتبت الحروفُ في هذه الشجرة بالرسم
الإملائيّ المُشكَّل، وأُسقطت منها علاماتُ الوقف المصحفيّة كلُّها، فهي ليست
رسمَ طبعةٍ ولا رسمَ مصحف. ولم تُبلَغ الشبكةُ من هذه البيئة، فلا يُنسَب هذا
النقلُ إلى مشروع تنزيل ولا إلى غيره
(`REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH`).

**وبصمةُ تقريرٍ خارجيٍّ ليست بصمةَ هذا المُودَع.** سُجِّل في تقرير جلسةٍ
خارجَ الشجرة معرّفُ مصدرٍ وبصمةُ محتوًى لنقلٍ «مُبسَّطٍ مُشكَّل» للآية نفسِها؛
ولم تُنقَل بايتاتُ ذلك النقل إلى هنا، فلا تُقارَن بصمةُ هذه الحروف به ولا
يُدَّعى توافقُهما. وما يُشتقّ من هذه الوحدة يُنسَب إليها وحدَها
(`AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا تقرؤها
بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

import hashlib
import unicodedata
from enum import Enum
from typing import Final, Literal

__all__ = [
    "AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST",
    "A_SIMPLIFIED_RASM_IS_NOT_AN_EDITION",
    "FATH_AYAH_NAMED_RESIDUALS",
    "FATH_AYAH_SOURCE_ID",
    "FATH_AYAH_SOURCE_TEXT",
    "NORMALIZATION_FORM",
    "REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH",
    "THE_WAQF_MARKS_ARE_DROPPED_SO_NO_PAUSE_IS_READABLE",
    "TRANSCRIPTION_STANDING",
    "TranscriptionStanding",
    "source_byte_length",
    "source_sha256",
    "written_word_count",
]


FATH_AYAH_SOURCE_ID: Final[str] = "fath-48-29-simplified-transcription-in-tree"
"""اسمُ هذا المُودَع؛ ويُسمّي نفسَه نقلًا مُبسَّطًا في الشجرة لا طبعةً مُسمّاة."""


FATH_AYAH_SOURCE_TEXT: Final[str] = (
    "مُحَمَّدٌ رَسُولُ اللَّهِ وَالَّذِينَ مَعَهُ أَشِدَّاءُ عَلَى الْكُفَّارِ "
    "رُحَمَاءُ بَيْنَهُمْ تَرَاهُمْ رُكَّعًا سُجَّدًا يَبْتَغُونَ فَضْلًا مِنَ "
    "اللَّهِ وَرِضْوَانًا سِيمَاهُمْ فِي وُجُوهِهِمْ مِنْ أَثَرِ السُّجُودِ "
    "ذَلِكَ مَثَلُهُمْ فِي التَّوْرَاةِ وَمَثَلُهُمْ فِي الْإِنْجِيلِ كَزَرْعٍ "
    "أَخْرَجَ شَطْأَهُ فَآزَرَهُ فَاسْتَغْلَظَ فَاسْتَوَى عَلَى سُوقِهِ "
    "يُعْجِبُ الزُّرَّاعَ لِيَغِيظَ بِهِمُ الْكُفَّارَ وَعَدَ اللَّهُ الَّذِينَ "
    "آمَنُوا وَعَمِلُوا الصَّالِحَاتِ مِنْهُمْ مَغْفِرَةً وَأَجْرًا عَظِيمًا"
)
"""الحروفُ مُجمَّعةً كما تُقاس: كلماتٌ مفصولةٌ بفراغٍ واحدٍ لا أكثر."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"
"""صورةُ التطبيع المُصرَّح بها، ويُتحقَّق منها عند الاستيراد لا تُدَّعى."""


def source_sha256() -> str:
    """بصمةُ الحروف المُودَعة، مُشتقّةً منها الآن لا مكتوبةً في ثابت."""

    return hashlib.sha256(FATH_AYAH_SOURCE_TEXT.encode("utf-8")).hexdigest()


def source_byte_length() -> int:
    """طولُ الحروف المُودَعة بالبايت في ترميز UTF-8، مُشتقًّا لا مُعلَنًا."""

    return len(FATH_AYAH_SOURCE_TEXT.encode("utf-8"))


def written_word_count() -> int:
    """عددُ الكلمات المكتوبة، مُشتقًّا من الفواصل لا مكتوبًا في حقل.

    وهو عدُّ **كلماتٍ مرسومةٍ مفصولةٍ بفراغ**، لا عدُّ كلماتٍ نحويّة: فـ«بِهِمُ»
    كلمةٌ واحدةٌ هنا وهي حرفٌ وضميرٌ، و«اللَّهِ» بعد «رَسُولُ» كلمةٌ مستقلّةٌ
    وإن كانت مضافًا إليه. فالفاصلُ رسمٌ لا تحليل.
    """

    return len(FATH_AYAH_SOURCE_TEXT.split())


class TranscriptionStanding(Enum):
    """رتبةُ تحقُّق النقل؛ ثلاثةٌ مغلقة، والأدنى وحدَه ذو مدخلٍ اليوم."""

    TRANSCRIBED_IN_TREE_NOT_COLLATED = "transcribed_in_tree_not_collated"
    COLLATED_AGAINST_A_NAMED_DIGITAL_EDITION = (
        "collated_against_a_named_digital_edition"
    )
    COLLATED_AGAINST_A_PRINTED_MUSHAF = "collated_against_a_printed_mushaf"


TRANSCRIPTION_STANDING: Final[TranscriptionStanding] = (
    TranscriptionStanding.TRANSCRIBED_IN_TREE_NOT_COLLATED
)
"""رتبةُ هذا المُودَع: نقلٌ في الشجرة لم يُقابَل بشاهدٍ رقميٍّ ولا مطبوع."""


if not unicodedata.is_normalized(  # pragma: no cover - حارس استيراد
    NORMALIZATION_FORM, FATH_AYAH_SOURCE_TEXT
):
    raise RuntimeError("the deposited ayah is not in its declared normal form")

if "\n" in FATH_AYAH_SOURCE_TEXT:  # pragma: no cover - حارس استيراد
    raise RuntimeError("the deposit is a single ayah on a single line")

if "  " in FATH_AYAH_SOURCE_TEXT:  # pragma: no cover - حارس استيراد
    raise RuntimeError("words are separated by a single space, not more")


# --- ما لا يحسمه هذا الإيداع، مُسمًّى ----------------------------------------


A_SIMPLIFIED_RASM_IS_NOT_AN_EDITION: Final[str] = (
    "A_SIMPLIFIED_RASM_IS_NOT_AN_EDITION: الحروفُ هنا نقلٌ مُبسَّطٌ كُتب في هذه "
    "الشجرة ولم يُقابَل بشاهدٍ رقميٍّ ولا بمصحفٍ مطبوع؛ فكلُّ رقمٍ يُشتقّ منها "
    "رقمٌ عن هذا النقل، ولا يُقرأ رقمًا عن مصحفٍ ولا عن طبعةٍ مُسمّاة"
)

REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH: Final[str] = (
    "REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH: لم تُبلَغ الشبكةُ من هذه "
    "البيئة، فلم تُنقَل بايتاتُ طبعةٍ رقميةٍ مُسمّاة؛ وكتابةُ إسنادٍ إلى طبعةٍ "
    "لم تُنقَل تصديقٌ لا نقل"
)

AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST: Final[str] = (
    "AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST: بصمةُ النقل المُبسَّط "
    "المذكورةُ في تقرير جلسةٍ خارجَ الشجرة لا تُقارَن ببصمة هذه الحروف، إذ لم "
    "تُنقَل بايتاتُ ذلك النقل هنا؛ وملاءمةُ البايتات لتوافق بصمةً منقولةً "
    "هندسةٌ للمُخرَج لا نقلٌ له"
)

THE_WAQF_MARKS_ARE_DROPPED_SO_NO_PAUSE_IS_READABLE: Final[str] = (
    "THE_WAQF_MARKS_ARE_DROPPED_SO_NO_PAUSE_IS_READABLE: أُسقطت علاماتُ الوقف "
    "المصحفيّة من هذا النقل، فلا يُقرأ منه موضعُ وقفٍ ولا وصلٍ ولا يُحتجّ "
    "بخلوّه منها على شيء"
)

FATH_AYAH_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_SIMPLIFIED_RASM_IS_NOT_AN_EDITION": A_SIMPLIFIED_RASM_IS_NOT_AN_EDITION,
    "REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH": (
        REQUESTED_EDITION_WAS_NOT_REACHED_FOR_THIS_AYAH
    ),
    "AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST": (
        AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST
    ),
    "THE_WAQF_MARKS_ARE_DROPPED_SO_NO_PAUSE_IS_READABLE": (
        THE_WAQF_MARKS_ARE_DROPPED_SO_NO_PAUSE_IS_READABLE
    ),
}
"""ما لا يحسمه هذا الإيداع، مُسمًّى هنا لا متروكًا ليُفترَض."""
