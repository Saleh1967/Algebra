"""نصٌّ عربيٌّ واحدٌ مُودَعٌ بحروفه، ومعه جنسُ تحقُّقه لا دعوى إسناده.

العدُّ الخامّ لا يقوم على نصٍّ غير مودَع: ما لم تكن حروفُه في الشجرة فلا يُعاد
اشتقاقُ رقمه، وهو عينُ ما سمّاه كاشفُ التلوّث في
`NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED`. فأُودعت هنا سورةُ
الفاتحة بآياتها السبع، سطرًا لكلّ آية، لتكون **موضوعَ قياسٍ واحدًا معلومًا**::

    DepositedText  != CollatedText
    PublicDomainMatn != AttributedEdition

**والمتنُ مِلكٌ عامٌّ، والمُودَعُ هنا نقلٌ لم يُقابَل.** طُلب أن يكون المصدرُ
نصَّ مشروع تنزيل (tanzil.net) برسم التنزيل العثمانيّ؛ ولم تُبلَغ الشبكةُ من
هذه البيئة، فلم تُنقَل بايتاتُ تلك الطبعة ولا تُنسَب إليها. والمُودَعُ نقلٌ
مُشكَّلٌ بالرسم الإملائيّ كُتب في هذه الشجرة ولم يُقابَل بشاهدٍ رقميٍّ ولا
بمصحفٍ مطبوع، وذلك مُصرَّحٌ به في `TRANSCRIPTION_STANDING` لا مطويّ
(`A_TRANSCRIPTION_IS_NOT_AN_EDITION`). وكلُّ رقمٍ يُشتقّ من هذه الحروف فهو
رقمٌ **عن هذا النقل**، لا عن مصحفٍ ولا عن طبعةٍ مُسمّاة.

**ورتبةُ التحقّق ثلاثيةٌ مغلقة، واثنتان منها بلا مدخلٍ اليوم**، على منوال بقاء
`مقابل_بنسخة_ورقية_محققة` عضوًا بلا مدخلٍ في `sentence_card_source_texts`؛
وبقاؤهما مُسمّاتَين هو ما يجعل المرتبةَ الدنيا مرتبةً لا سقفًا.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا تقرؤها
بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

import hashlib
import unicodedata
from enum import Enum
from typing import Final, Literal

__all__ = [
    "A_TRANSCRIPTION_IS_NOT_AN_EDITION",
    "FATIHA_LINES",
    "FATIHA_SOURCE_ID",
    "FATIHA_SOURCE_TEXT",
    "FATIHA_SOURCE_TEXT_NAMED_RESIDUALS",
    "NORMALIZATION_FORM",
    "REQUESTED_EDITION_WAS_NOT_REACHED",
    "RASM_IS_IMLAI_NOT_UTHMANI",
    "THE_MATN_IS_PUBLIC_DOMAIN_THE_EDITION_IS_NOT_CLAIMED",
    "TRANSCRIPTION_STANDING",
    "TranscriptionStanding",
    "source_byte_length",
    "source_sha256",
]


FATIHA_SOURCE_ID: Final[str] = "fatiha-transcription-in-tree"
"""اسمُ هذا المُودَع؛ ويُسمّي نفسَه نقلًا في الشجرة لا طبعةً مُسمّاة."""


FATIHA_LINES: Final[tuple[str, ...]] = (
    "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
    "الرَّحْمَٰنِ الرَّحِيمِ",
    "مَالِكِ يَوْمِ الدِّينِ",
    "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
    "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
    "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ " "وَلَا الضَّالِّينَ",
)
"""سبعةُ أسطر، سطرٌ لكلّ آيةٍ على عدّ الكوفيّين الذي يجعل البسملةَ آيةً."""


FATIHA_SOURCE_TEXT: Final[str] = "\n".join(FATIHA_LINES)
"""الحروفُ مجموعةً كما تُقاس: الأسطرُ مفصولةٌ بسطرٍ جديدٍ لا أكثر."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"
"""صورةُ التطبيع المُصرَّح بها، ويُتحقَّق منها عند الاستيراد لا تُدَّعى."""


def source_sha256() -> str:
    """بصمةُ الحروف المُودَعة، مُشتقّةً منها الآن لا مكتوبةً في ثابت.

    وبصمةٌ مكتوبةٌ في نصّ الوحدة تُصدِّق نفسَها؛ فتُحسَب من `FATIHA_SOURCE_TEXT`
    عند الطلب، ويقارنها القارئُ بما يُخرجه من بايتات الملفّ إن شاء.
    """
    return hashlib.sha256(FATIHA_SOURCE_TEXT.encode("utf-8")).hexdigest()


def source_byte_length() -> int:
    """طولُ الحروف المُودَعة بالبايت في ترميز UTF-8، مُشتقًّا لا مُعلَنًا."""
    return len(FATIHA_SOURCE_TEXT.encode("utf-8"))


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
    NORMALIZATION_FORM, FATIHA_SOURCE_TEXT
):
    raise RuntimeError("the deposited text is not in its declared normal form")

if len(FATIHA_LINES) != 7:  # pragma: no cover - حارس استيراد
    raise RuntimeError("the deposited sura is seven verses, one line each")


# --- ما لا يحسمه هذا الإيداع، مُسمًّى ----------------------------------------


A_TRANSCRIPTION_IS_NOT_AN_EDITION: Final[str] = (
    "A_TRANSCRIPTION_IS_NOT_AN_EDITION: الحروفُ هنا نقلٌ كُتب في هذه الشجرة "
    "ولم يُقابَل بشاهدٍ رقميٍّ ولا بمصحفٍ مطبوع؛ فكلُّ رقمٍ يُشتقّ منها رقمٌ "
    "عن هذا النقل، ولا يُقرأ رقمًا عن مصحفٍ ولا عن طبعةٍ مُسمّاة"
)

REQUESTED_EDITION_WAS_NOT_REACHED: Final[str] = (
    "REQUESTED_EDITION_WAS_NOT_REACHED: طُلب رسمُ التنزيل من مشروع تنزيل "
    "(tanzil.net)، ولم تُبلَغ الشبكةُ من بيئة هذا العمل، فلم تُنقَل بايتاتُ "
    "تلك الطبعة؛ وكتابةُ إسنادٍ إليها دون نقلها تصديقٌ لا نقل"
)

THE_MATN_IS_PUBLIC_DOMAIN_THE_EDITION_IS_NOT_CLAIMED: Final[str] = (
    "THE_MATN_IS_PUBLIC_DOMAIN_THE_EDITION_IS_NOT_CLAIMED: المتنُ القرآنيُّ "
    "في نفسه مِلكٌ عامٌّ، والذي قد يحمل جهدًا محميًّا هو التوسيمُ والرسمُ في "
    "طبعةٍ رقميةٍ بعينها؛ ولا تُنسَب هذه الحروفُ إلى طبعةٍ من تلك"
)

RASM_IS_IMLAI_NOT_UTHMANI: Final[str] = (
    "RASM_IS_IMLAI_NOT_UTHMANI: النقلُ مُشكَّلٌ بالرسم الإملائيّ، لا برسم "
    "التنزيل العثمانيّ؛ والفرقُ بينهما يقع في حوامل الألف نفسِها (ألفُ الوصل، "
    "والألفُ الخنجرية، وحذفُ الألف) فيمسّ كلَّ عدٍّ يُبنى على الألف"
)

FATIHA_SOURCE_TEXT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_TRANSCRIPTION_IS_NOT_AN_EDITION": A_TRANSCRIPTION_IS_NOT_AN_EDITION,
    "REQUESTED_EDITION_WAS_NOT_REACHED": REQUESTED_EDITION_WAS_NOT_REACHED,
    "THE_MATN_IS_PUBLIC_DOMAIN_THE_EDITION_IS_NOT_CLAIMED": (
        THE_MATN_IS_PUBLIC_DOMAIN_THE_EDITION_IS_NOT_CLAIMED
    ),
    "RASM_IS_IMLAI_NOT_UTHMANI": RASM_IS_IMLAI_NOT_UTHMANI,
}
"""ما لا يحسمه هذا الإيداع، مُسمًّى هنا لا متروكًا ليُفترَض."""
