"""الأداةُ الفعليةُ التي أنتجت رقمَي الاقتصاد الصوتيّ، مُرفَقةً لإعادة التشغيل.

هذا الملفُّ هو `tool_identity` المرجعيُّ لحقلَي الدليل في
`phonetic_economy_candidate.py`: النتيجةُ لا تُسجَّل وصفًا بلا وسيلةِ فحصها،
فمن أراد ردَّها أعاد تشغيلَ هذا الحساب بعينه.

**تنبيهُ أمانةٍ إلزاميّ، مُسجَّلٌ بقيّةً لا تعليقًا**: هذه **إعادةُ بناءٍ
مُبسَّطة** (متوسّطُ مسافةِ مخرجٍ مباشرٌ بين مجموعتَي حروف) لا نسخةٌ حرفيةٌ من
أداةِ الجلسة الأصلية (التي استخدمت تكرارَ تلازمٍ فعليّ في نصّ المصحف بمنطق
تباعد KL، لا متوسّطَ مسافةٍ مجرَّدًا عن مجموعةِ حروف). ولذلك يخرج هذا الملفُّ
٣٫٤٣ لا ٤٫٠، و٩٫٩٦ لا ٩٫٥؛ والفارقُ العدديُّ **دليلٌ مباشرٌ على اختلافٍ
منهجيّ**، لا خطأَ تقريبٍ يُسوَّى بتعديل الجدول. وقد سُجِّل هذا الفارقُ بقيّةً
باسم `TOOL_IS_APPROXIMATE_RECONSTRUCTION` في وحدة التسجيل، ولا يُستبدَل رقمُ
هذا الملفّ برقم الجلسة ولا العكس.

**وملاحظةٌ منهجيةٌ أهمّ**: جدولُ `PLACE_NUM` نفسُه من ابتكار الجلسة، لم يُقابَل
بمصدر صوتيّاتٍ فيزيائيٍّ مستقلّ — وهذا، لا فارقُ التقريب أعلاه، هو السببُ
الحقيقيُّ لفشل `IndependentClosureCheck`.

ولا سلطةَ لهذا الملفّ: لا يقرؤه `IndependentClosureGate` ولا `BirthVerdictGate`،
ولا يدخل في `BirthExperimentSpecification`، ولا يُصدر حكمًا.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

__all__ = [
    "IDGHAM_NUN_LETTERS",
    "IZHAR_NUN_LETTERS",
    "MOON_LETTERS_REAL",
    "PLACE_NUM",
    "SUN_LETTERS",
    "TOOL_IS_AN_APPROXIMATE_RECONSTRUCTION_NOTE",
    "TOOL_MODULE_PATH",
    "TOOL_TABLE_IS_SELF_INVENTED_NOTE",
    "average_place_distance",
    "compute_lam_f",
    "compute_nun_f",
]

TOOL_MODULE_PATH: Final[str] = "src/alghanem/arabic/phonetic_economy_tool.py"

TOOL_IS_AN_APPROXIMATE_RECONSTRUCTION_NOTE: Final[str] = (
    "TOOL_IS_APPROXIMATE_RECONSTRUCTION: هذا الملفُّ إعادةُ بناءٍ مُبسَّطة "
    "(متوسّطُ مسافةِ مخرجٍ بين مجموعتَي حروف) لأداةِ الجلسة الأصلية القائمة "
    "على تكرارِ التلازم في نصّ المصحف بمنطق تباعد KL؛ فمخرجاتُه ٣٫٤٣ و٩٫٩٦ "
    "لا تُطابق رقمَي الجلسة ٤٫٠ و٩٫٥، ولا يُستعمل رقمُه مكانَ رقمِ الجلسة، "
    "ولا يُعدَّل الجدولُ لإجبار التطابق"
)

TOOL_TABLE_IS_SELF_INVENTED_NOTE: Final[str] = (
    "TOOL_TABLE_IS_SELF_INVENTED: جدولُ المخارج وترقيمُه من ابتكار الجلسة، "
    "لم يُقابَل بمصدر صوتيّاتٍ فيزيائيٍّ مستقلّ؛ وهو سببُ فشلِ الإغلاق "
    "المستقلّ لا فارقُ التقريب العدديّ"
)

# جدولُ المخارج المُستخدَم فعليًّا (تسعةُ مخارجَ تقليدية، ترقيمٌ تقريبيٌّ
# للمسافة النسبية).
PLACE_NUM: Final[MappingProxyType[str, int]] = MappingProxyType(
    {
        "ب": 1,
        "م": 1,
        "و": 1,
        "ف": 2,
        "ث": 3,
        "ذ": 3,
        "ظ": 3,
        "ت": 4,
        "د": 4,
        "ط": 4,
        "س": 4,
        "ز": 4,
        "ص": 4,
        "ن": 4,
        "ل": 4,
        "ض": 4,
        "ر": 4,
        "ج": 5,
        "ش": 5,
        "ي": 5,
        "ك": 6,
        "ق": 7,
        "خ": 7,
        "غ": 7,
        "ح": 8,
        "ع": 8,
        "ء": 9,
        "ه": 9,
    }
)

IDGHAM_NUN_LETTERS: Final[frozenset[str]] = frozenset("يرملون")
IZHAR_NUN_LETTERS: Final[frozenset[str]] = frozenset("ءهعحغخ")
SUN_LETTERS: Final[frozenset[str]] = frozenset("تثدذرزسشصضطظلن")
# بلا الألف: لا تقبل «ال» أصلًا كحرفٍ تالٍ.
MOON_LETTERS_REAL: Final[frozenset[str]] = frozenset("بجحخعغفقكمهوي")


def average_place_distance(letters: frozenset[str], target_place: int) -> float:
    """متوسّطُ |مخرج(c) − target_place| عبر مجموعةِ حروف.

    هذا كلُّ ما يقف وراء الرقمَين، لا شيءَ أعمق؛ وهذا بعينه ما يجعله قابلًا
    لإعادة الفحص.
    """

    distances = [abs(PLACE_NUM[c] - target_place) for c in letters if c in PLACE_NUM]
    if not distances:
        return float("nan")
    return sum(distances) / len(distances)


def compute_nun_f() -> float:
    """نسبةُ متوسّطِ مسافةِ الإظهار إلى متوسّطِ مسافةِ الإدغام عند النون الساكنة."""

    nun_place = PLACE_NUM["ن"]
    idgham_avg = average_place_distance(IDGHAM_NUN_LETTERS, nun_place)
    izhar_avg = average_place_distance(IZHAR_NUN_LETTERS, nun_place)
    return izhar_avg / idgham_avg


def compute_lam_f() -> float:
    """نسبةُ متوسّطِ مسافةِ القمريّ إلى متوسّطِ مسافةِ الشمسيّ عند لام التعريف."""

    lam_place = PLACE_NUM["ل"]
    shamsi_avg = average_place_distance(SUN_LETTERS, lam_place)
    qamari_avg = average_place_distance(MOON_LETTERS_REAL, lam_place)
    return qamari_avg / shamsi_avg


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويٌّ للفحص
    print(f"F(نون) = {compute_nun_f():.2f}  (تقريب؛ الأصلُ الجلسيُّ كان 4.0)")
    print(f"F(لام) = {compute_lam_f():.2f}  (تقريب؛ الأصلُ الجلسيُّ كان 9.5)")
    print()
    print(TOOL_IS_AN_APPROXIMATE_RECONSTRUCTION_NOTE)
    print(TOOL_TABLE_IS_SELF_INVENTED_NOTE)
