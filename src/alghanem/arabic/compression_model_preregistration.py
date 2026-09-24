"""تجميدُ قياسِ الضغط قبل إجرائه: بايتاتٌ مُبصَّمة، ونموذجان، وقاعدةُ تعادلٍ كليّة.

**السؤالُ الذي وقفت عنده هذه الوحدة**: رقمُ ضغطٍ يُذكَر مجرَّدًا — «78.78%» —
لا يُعاد اشتقاقُه من أحد، لأنّ ثلاثةَ أشياء تبقى خارجه: **أيُّ بايتاتٍ قِيست**،
و**ماذا يُحسَب في الحجم**، و**أيُّ شجرةٍ من أشجار هفمان المثلى بُنيت**. وقد أخرج
إغفالُ الأوّل رقمًا سابقًا مقيسًا على تمثيلٍ أسقط الحركات، وأخرج إغفالُ الثاني
رقمًا للحمولة وحدها قُدِّم كأنّه حجمُ الملفّ القابل لفكّ الترميز. فهذه الوحدة
تُجمِّد الثلاثةَ قبل أن تُكتَب دالّةُ قياسٍ واحدة.

`MEASUREMENT_IS_BOUND_TO_BYTES_NOT_TO_A_REPRESENTATION`: مدخلُ القياس بايتاتٌ
خام يُتحقَّق من طولها وبصمتها قبل فكّ ترميزها، لا قائمةُ وحداتٍ ولا تمثيلٌ وسيط.
فتمثيلٌ وسيطٌ قد يُسقط حركةً أو مسافةً، ورقمٌ صحيحُ الحساب على نصف المعلومة
رقمٌ خاطئٌ عن الكلّ. والأبجديّةُ تُشتَقّ من البايتات نفسها عدًّا، فعددُها
نتيجةٌ تُتحقَّق لا ثابتٌ يُعلَن.

`TWO_SIZES_OR_NONE`: لا يُصدَر رقمُ حجمٍ واحد. يُصدَر معًا دائمًا **طولُ الحمولة
المرمَّزة** و**الحجمُ الكلّيُّ القابل لفكّ الترميز من الصفر** شاملًا جداولَ
الشفرة. فمن ذكر الحمولةَ وحدها ذكر حجمًا لا يُفَكّ إلا بمعرفةٍ مسبقةٍ لم
يحسبها.

`ROUND_TRIP_IS_A_PRECONDITION_OF_ISSUANCE`: المطابقةُ بايتًا-ببايت شرطُ إصدارٍ
لا بندُ تقرير. فإن لم يُطابق فكُّ الشيفرة الأصلَ رُفِع استثناءٌ ولم يُصدَر رقمُ
ضغطٍ أصلًا؛ ورقمٌ بلا مطابقةٍ هو عينُ الخطأ الذي أُريدَ سدُّه.

`THE_TIE_BREAK_IS_DECLARED_BECAUSE_THE_TABLE_IS_NOT_INVARIANT`: كلفةُ هفمان
(الحمولة) وحيدةٌ عدديًّا مهما تعدّدت الأشجارُ المثلى — فالأمثل لا يتعدّد.
أمّا **مجموعُ أطوال الشفرات** فيختلف بين أشجارٍ مثلى متساوية الكلفة، وعليه
يتوقّف حجمُ الجدول. لذلك تُعلَن هنا قاعدةُ حسمِ تعادلٍ **كليّة** لا جزئية،
ويُصرَّح أنّ رقمَ الحجم الكلّيّ **نسبةٌ إلى قاعدته** لا مطلق.

`A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM`: أقصى ما تبلغه هذه الطبقةُ
رقمٌ قابلٌ لإعادة الاشتقاق من بايتاتٍ مُبصَّمة. أمّا أن يكون الرقمُ شاهدًا على
بنيةٍ في العربية، فحكمٌ يُكتَب في موضع الأحكام ولا يخرج من أداةِ قياسٍ تلقائيًّا.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا تستورد هذه الوحدةُ من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM_NOTE",
    "FIRST_SYMBOL_CONTEXT",
    "FROZEN_CORPUS",
    "MEASUREMENT_IS_BOUND_TO_BYTES_NOTE",
    "NAMED_RESIDUALS",
    "PREREGISTRATION_DIGEST",
    "PRE_REGISTERED_EXPECTATION",
    "ROUND_TRIP_IS_A_PRECONDITION_NOTE",
    "TABLE_ENTRY_CODEPOINT_BITS",
    "TABLE_ENTRY_LENGTH_FIELD_BITS",
    "THE_TIE_BREAK_IS_DECLARED_NOTE",
    "TWO_SIZES_OR_NONE_NOTE",
    "CompressionCorpusReference",
    "CompressionPreregistrationError",
    "TieBreakRule",
    "preregistration_digest",
]


class CompressionPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: مرجعٌ ناقصٌ أو بايتاتٌ لا تطابق المُجمَّد."""


class TieBreakRule(Enum):
    """قاعدةُ حسمِ التعادل عند تساوي التردّد في بناء شجرة هفمان.

    كلتاهما **كليّة**: لا يبقى تحتها عقدتان متساويتا المفتاح، لأنّ الشجيرات
    متباينةُ الرموز فأصغرُ رمزٍ فيها يفصل حتمًا. والحمولةُ واحدةٌ تحتهما معًا؛
    الفارقُ يقع في حجم الجدول وحده.
    """

    SMALLEST_CODEPOINT = "التردّد ثمّ أصغرُ نقطةِ كودٍ في الشجيرة"
    """قاعدةٌ بسيطةٌ مُعلَنة، وهي التي أُنتج بها الرقمُ المُجمَّد في هذه الشجرة."""

    MINIMAL_TABLE = "التردّد ثمّ أقلُّ عمقٍ ثمّ أقلُّ عددِ أوراقٍ ثمّ أصغرُ نقطةِ كود"
    """تفضيلُ الشجيرة الأقلّ عمقًا يُصغِّر مجموعَ أطوال الشفرات، فيُصغِّر الجدول."""


TABLE_ENTRY_CODEPOINT_BITS: Final[int] = 21
"""تمثيلٌ مُعلَنٌ لنقطة الكود في إدخال الجدول؛ اختيارٌ مُصرَّحٌ به لا حتميّة."""

TABLE_ENTRY_LENGTH_FIELD_BITS: Final[int] = 6
"""حقلُ طولِ الشفرة في إدخال الجدول، ويليه بتّاتُ الشفرة نفسها."""

FIRST_SYMBOL_CONTEXT: Final[str] = "\x00START\x00"
"""سياقُ أوّلِ رمزٍ في الرتبة الأولى: علامةٌ خارج الأبجدية لا رمزٌ منها."""


@dataclass(frozen=True, slots=True)
class CompressionCorpusReference:
    """مرجعُ البايتات المقيسة: اسمٌ وطولٌ وبصمةٌ وترميزٌ وسياسةُ تطبيق."""

    source_name: str
    byte_length: int
    sha256_hex: str
    encoding: str
    normalization_policy: str

    def __post_init__(self) -> None:
        if not self.source_name.strip():
            raise CompressionPreregistrationError("مرجعُ البايتات بلا اسمٍ مصدر")
        if self.byte_length <= 0:
            raise CompressionPreregistrationError("طولُ البايتات لا يكون غيرَ موجب")
        if len(self.sha256_hex) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256_hex
        ):
            raise CompressionPreregistrationError("البصمةُ ليست SHA-256 ستّ عشريّة")
        if not self.encoding.strip() or not self.normalization_policy.strip():
            raise CompressionPreregistrationError("الترميزُ وسياسةُ التطبيع مُصرَّحان")

    def as_canonical_content(self) -> dict[str, object]:
        return {
            "source_name": self.source_name,
            "byte_length": self.byte_length,
            "sha256_hex": self.sha256_hex,
            "encoding": self.encoding,
            "normalization_policy": self.normalization_policy,
        }


FROZEN_CORPUS: Final[CompressionCorpusReference] = CompressionCorpusReference(
    source_name="quran-simple-enhanced.txt",
    byte_length=1_319_901,
    sha256_hex="37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
    encoding="utf-8-without-bom",
    normalization_policy=(
        "لا تطبيع البتّة: كلُّ نقطةِ كودٍ تُعَدّ كما وردت — حرفًا أو حركةً أو "
        "مسافةً أو سطرًا أو محرفًا من محارف <sel> — ولا يُطوى شيءٌ في شيء"
    ),
)
"""البايتاتُ نفسُها غيرُ محشورةٍ في الشجرة؛ المُجمَّدُ بصمتُها وطولُها."""


MEASUREMENT_IS_BOUND_TO_BYTES_NOTE: Final[str] = (
    "MeasurementIsBoundToBytesNotToARepresentation: مدخلُ القياس بايتاتٌ خام "
    "يُتحقَّق من طولها وبصمتها قبل فكّ ترميزها، لا تمثيلٌ وسيطٌ قد يُسقط حركةً؛ "
    "والأبجديّةُ تُعَدّ من البايتات فعددُها نتيجةٌ تُتحقَّق لا ثابتٌ يُعلَن"
)

TWO_SIZES_OR_NONE_NOTE: Final[str] = (
    "TwoSizesOrNone: يُصدَر معًا دائمًا طولُ الحمولة المرمَّزة والحجمُ الكلّيُّ "
    "القابل لفكّ الترميز شاملًا الجداول؛ فمن ذكر الحمولةَ وحدها ذكر حجمًا لا "
    "يُفَكّ إلا بمعرفةٍ مسبقةٍ لم يحسبها"
)

ROUND_TRIP_IS_A_PRECONDITION_NOTE: Final[str] = (
    "RoundTripIsAPreconditionOfIssuance: المطابقةُ بايتًا-ببايت شرطُ إصدارٍ لا "
    "بندُ تقرير؛ فإن اختلف محرفٌ واحد رُفِع استثناءٌ ولم يُصدَر رقمُ ضغطٍ أصلًا"
)

THE_TIE_BREAK_IS_DECLARED_NOTE: Final[str] = (
    "TheTieBreakIsDeclaredBecauseTheTableIsNotInvariant: كلفةُ هفمان وحيدةٌ "
    "عدديًّا مهما تعدّدت الأشجارُ المثلى، أمّا مجموعُ أطوال الشفرات — وعليه حجمُ "
    "الجدول — فيختلف بينها؛ فحجمُ الجدول رقمٌ نسبةً إلى قاعدةِ تعادلٍ مُعلَنةٍ "
    "كليّة لا رقمٌ مطلق"
)

A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM_NOTE: Final[str] = (
    "ACompressionRatioIsNotALinguisticClaim: غايةُ هذه الطبقة رقمٌ قابلٌ لإعادة "
    "الاشتقاق من بايتاتٍ مُبصَّمة؛ وأن يكون الرقمُ شاهدًا على بنيةٍ في العربية "
    "حكمٌ يُكتَب في موضع الأحكام ولا يخرج من أداةِ قياسٍ تلقائيًّا"
)

PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: المُتوقَّعُ قبل القياس أن تبقى الحمولةُ ثابتةً "
    "تحت أيّ قاعدةِ تعادل، وأن يتحرّك حجمُ الجدولِ وحده بينها، وأن تكون قاعدةُ "
    "`MINIMAL_TABLE` أصغرَ جدولًا من `SMALLEST_CODEPOINT` أو مساويةً لها ولا "
    "تكون أكبرَ منها أبدًا. ومخالفةُ ذلك مفاجأةٌ تُوثَّق لا نتيجةٌ تُبتلَع"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من "
    "`kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه"
)

NAMED_RESIDUALS: Final[dict[str, str]] = {
    "MEASUREMENT_IS_BOUND_TO_BYTES_NOT_TO_A_REPRESENTATION": (
        MEASUREMENT_IS_BOUND_TO_BYTES_NOTE
    ),
    "TWO_SIZES_OR_NONE": TWO_SIZES_OR_NONE_NOTE,
    "ROUND_TRIP_IS_A_PRECONDITION_OF_ISSUANCE": ROUND_TRIP_IS_A_PRECONDITION_NOTE,
    "THE_TIE_BREAK_IS_DECLARED_BECAUSE_THE_TABLE_IS_NOT_INVARIANT": (
        THE_TIE_BREAK_IS_DECLARED_NOTE
    ),
    "A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM": (
        A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM_NOTE
    ),
    "THE_TABLE_REPRESENTATION_IS_DECLARED_NOT_NECESSARY": (
        "تمثيلُ الجدول (نقطةُ كودٍ ٢١ بت، ثمّ طولٌ ٦ بت، ثمّ الشفرة) اختيارٌ "
        "مُعلَنٌ لا حتميّة؛ وتمثيلٌ يُخزّن الأطوالَ وحدها ويشتقّ الشفرةَ "
        "القانونيّة منها أصغرُ منه، فرقمُ الحجم الكلّيّ رقمٌ نسبةً إلى تمثيله"
    ),
    "THE_CORPUS_BYTES_ARE_NOT_VENDORED": (
        "بايتاتُ النصّ غيرُ محشورةٍ في الشجرة؛ المُجمَّدُ بصمتُها وطولُها، "
        "ويرفض القياسُ أيَّ بايتاتٍ سواها. فبصمةٌ بلا بايتاتٍ تُعيد الاشتقاق "
        "لطرفٍ ثالث، وبايتاتٌ بلا بصمةٍ لا تُعيده لأحد"
    ),
    "ZLIB_IS_A_REFERENCE_CEILING_NOT_AN_OPPONENT": (
        "‏zlib مرجعٌ خارجيٌّ يُذكَر للمقارنة لا نموذجٌ من هذه الطبقة؛ وهو "
        "‏LZ77+هفمان يستثمر تكرارَ كلماتٍ وعباراتٍ كاملة، فمقارنتُه بنموذجِ "
        "سياقٍ بحرفٍ واحدٍ سابقٍ مقارنةُ سعةٍ لا مقارنةُ صحّة"
    ),
    "THIS_IS_REGISTRATION_NOT_AUTHORITY": THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
}


def preregistration_digest() -> str:
    """بصمةُ المُجمَّد: يتغيّر أيُّ بندٍ فيه فتتغيّر، فيسقط تحقّقُ وحدة القياس."""

    return canonical_digest(
        canonical_bytes(
            {
                "corpus": FROZEN_CORPUS.as_canonical_content(),
                "first_symbol_context": FIRST_SYMBOL_CONTEXT,
                "table_entry_codepoint_bits": TABLE_ENTRY_CODEPOINT_BITS,
                "table_entry_length_field_bits": TABLE_ENTRY_LENGTH_FIELD_BITS,
                "tie_break_rules": [rule.name for rule in TieBreakRule],
                "expectation": PRE_REGISTERED_EXPECTATION,
                "residuals": NAMED_RESIDUALS,
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
