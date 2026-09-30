"""تحقيقُ نقلٍ عن حاويةٍ مختومةٍ خارجَ الشجرة — **يُعاد ولا يُصدَّق**.

**العطلُ الذي يعالجه**: بلغني تقريرٌ فيه «أربعةَ عشرَ اقتباسًا طابقت
الحاويةَ المختومةَ حرفيًّا». **وهذه دعوًى لا رقم**: من يقرؤها لا يملك
أن يعيدها، وأرقامُ الأسطرِ المرويّةُ لا تُطابق فهرسي لأنّ الاستخراجَ
غيرُ الاستخراج. **وفهرسٌ لا يُتَّفَق عليه ليس شاهدًا.**

فهذه الأداةُ تُبدِّل الدعوى بأمرين:

١. **مرساةٌ**: بصمةُ الحاويةِ نفسِها. فمن أراد الإعادةَ لزمه المِلفُّ
   بهذه البصمةِ بعينها، **ولا يُقاس على نسخةٍ أخرى بلا إعلان**.
٢. **مِسبارٌ مُعلَن**: نصوصٌ تُطلَب في المتنِ **بنصِّها لا برقمها**،
   فيُطبَع لكلٍّ أوُجِد وفي أيّ سطرٍ من استخراجٍ **مُعرَّفٍ ههنا**.

`THE_TEXT_IS_THE_WITNESS_NOT_THE_LINE_NUMBER`: فالمطابقةُ تُطلَب
بالنصّ، **والرقمُ ناتجٌ لا شرط**. ولهذا يَصْدُق التحقيقُ ولو اختلف
ترقيمُ الناقلِ عن ترقيمي — وهو ما وقع فعلًا.

`A_QUOTATION_THAT_MATCHES_PROVES_TRANSFER_NOT_INFERENCE`: **وحدُّه
مُعلَنٌ وهو أهمُّ ما فيه**: يُثبت أنّ المنقولَ في المصدر، **ولا يُثبت
أنّ ما بُنِي عليه لازمٌ عنه**. فمقابلةٌ بين عمودَين أحدُهما نصٌّ
والآخرُ قراءةٌ **سهمُها استدلالٌ يُبرهَن وحدَه**، ولا يكفيه صدقُ النقل.

**والحاويةُ لا تُودَع في هذه الشجرة**: هي متنٌ لغيرها. فيُودَع **سجلُّ
التحقيقِ وبصمةُ الحاوية** لا الحاوية، **وغيابُها يُصنَّف ولا يُصفَّر**.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata as ud
import zipfile
from pathlib import Path
from typing import Final, NamedTuple

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSIT: Final[Path] = REPOSITORY / "deposits" / "quotation_audit.log"

# الحاويةُ المُعلَنةُ ببصمتها — **والقياسُ على غيرها يُعلَن أو يُرَدّ**.
HOLDER: Final[Path] = Path(
    "/home/user/saleh1967/hamil-hala-zaman-program/"
    "الشخصية الاسلامية الجزء الثالث ورد (2).docx"
)
DIGEST: Final[str] = "360f7653df4e3396d18153d0"
"""أوّلُ ٢٤ محرفًا من بصمةِ الحاويةِ التي قِيست — والمرساةُ هي، لا المسار."""

PARAGRAPH: Final[str] = r"<w:p[ >].*?</w:p>"
RUN: Final[str] = r"<w:t[^>]*>(.*?)</w:t>"
TATWEEL: Final[str] = "\u0640"

# **المسبارُ**: ما يُطلَب في المتنِ بنصِّه. ولكلٍّ سببُ طلبه، فلا يُزاد
# نصٌّ بلا غرضٍ ولا يُحذَف بلا ذكر.
PROBE: Final[tuple[tuple[str, str], ...]] = (
    ("علم آدم الأسماء", "النصُّ المؤسِّسُ المزعوم"),
    ("الأسماء كلها", "تمامُ الاقتباس"),
    ("حقائق الأشياء وخواصها", "تفسيرُ المسمّيات"),
    ("معلومات سابقة", "طبقةُ المعلوماتِ قبلَ الحكم"),
    ("الإحساس بالواقع", "أنّ الإحساسَ وحدَه لا يكفي"),
    ("مسميات الأشياء لا اللغات", "**الفصلُ الذي ينقض المقابلة**"),
    ("عرف الأشياء ولم يعرف اللغات", "**الفصلُ نفسُه بعبارةٍ ثانية**"),
    ("الألفاظ ليست دلالة على الحقائق", "**نفيُ أنّ اللفظَ يدلُّ على الحقيقة**"),
    ("المعاني الذهنية دون الخارجية", "موضوعُ الوضعِ ذهنيٌّ لا خارجيّ"),
    ("تخصيص لفظ بمعنى", "تعريفُ الوضع"),
    ("النسب الإسنادية", "طبقةُ النِّسَبِ بنصِّها"),
    ("النسب والمعاني المركبة", "غرضُ المركَّب"),
    ("بعد علمه بأوضاع المفردات", "ترتيبُ الطبقتين"),
    ("دلالة المطابقة", "الدلالةُ الأولى"),
    ("دلالة التضمن", "الثانية"),
    ("دلالة الالتزام", "الثالثة"),
    ("مجموع الكلام من حيث هو", "تعريفُ المهمَل — **صنفُ الباقي**"),
    ("وإن دل كل جزء منه على معنى", "تمامُ تعريفِ المهمَل"),
    ("تابع لأصله وهو المصدر", "تبعيّةُ المشتقِّ للمصدر"),
    ("الأصل في الكلام هو الحقيقة", "قاعدةُ الأصلِ والفرع"),
    ("يفتقر إلى شيء يفسره", "وصفُ الضميرِ الذي ذُكِر شاهدًا"),
)

# أنواعُ العلاقةِ كما تُعَدُّ من النصّ — **العدُّ لا الرواية**.
KINDS: Final[str] = (
    r"النوع (الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)"
)
ELEVENTH: Final[str] = r"الحادي عشر: التعلق"


class Hit(NamedTuple):
    """نصٌّ مطلوبٌ وما وُجِد له."""

    text: str
    why: str
    lines: tuple[int, ...]


def bare(text: str) -> str:
    """تجريدٌ للمطابقةِ وحدَها: تُطرَح علاماتُ الدمجِ والتطويلُ والفراغ.

    **والأصلُ لا يُمَسّ**: يُقرَأ من الحاويةِ كما هو ويُجرَّد نسخةٌ منه
    للمقابلة. فحركةٌ في المصدرِ وغيابُها في النقلِ ليس اختلافَ نصّ.
    """

    # **والتطويلُ يُحذَف ولا يُبدَّل فراغًا**: كان يُبدَّل، فصارت
    # «الأســماء» تُجرَّد إلى «الأس ماء» فلا تُطابق «الأسماء» — ورَدَّه
    # `test_the_matching_strips_marks_but_never_touches_the_source` أوّلَ
    # نصبه. وكنتُ قد داريتُ العَرَضَ بحيلةِ `عشـ?ر` في نمطِ الحاديَ عشر
    # **فعالجتُ الأثرَ دونَ سببه**، فسقطت الحيلةُ مع السبب.
    #
    # والفراغُ يُطبَّق ولا يُحذَف: حذفُه يلصق كلمتين **فيُطابِق ما ليس
    # مطابقًا**، وذاك أسوأُ من إخفاقِ مطابقةٍ صحيحة.
    without = "".join(one for one in text if not ud.combining(one) and one != TATWEEL)
    return re.sub(r"\s+", " ", without)


def held() -> bool:
    return HOLDER.is_file()


def measured_digest() -> str:
    return hashlib.sha256(HOLDER.read_bytes()).hexdigest()[: len(DIGEST)]


def lines_of() -> list[str]:
    """استخراجٌ **مُعرَّفٌ ههنا**: سطرٌ لكلّ `<w:p>`، ونصُّه من `<w:t>`.

    فالترقيمُ ناتجُ هذا التعريفِ لا خاصّيّةً للحاوية. **ومن استخرج بغيره
    جاءه ترقيمٌ آخرُ بلا خطأٍ في واحدٍ منهما.**
    """

    with zipfile.ZipFile(HOLDER) as box:
        xml = box.read("word/document.xml").decode("utf-8")
    out: list[str] = []
    for one in re.findall(PARAGRAPH, xml, re.DOTALL):
        joined = "".join(re.findall(RUN, one, re.DOTALL))
        out.append(re.sub(r"<[^>]+>", "", joined).strip())
    return out


def probe(rows: list[str]) -> list[Hit]:
    found: list[Hit] = []
    for text, why in PROBE:
        key = bare(text).strip()
        at = tuple(i + 1 for i, one in enumerate(rows) if key in bare(one))
        found.append(Hit(text=text, why=why, lines=at))
    return found


def relations(rows: list[str]) -> tuple[int, bool]:
    """عددُ أنواعِ العلاقةِ المعدودةِ في المتنِ، وأوُجِد الحاديَ عشر."""

    whole = bare("\n".join(rows))
    numbered = len(set(re.findall(KINDS, whole)))
    return numbered, bool(re.search(ELEVENTH, whole))


def missing(hits: list[Hit]) -> tuple[str, ...]:
    return tuple(one.text for one in hits if not one.lines)


def report() -> str:
    rows = lines_of()
    hits = probe(rows)
    numbered, eleventh = relations(rows)
    gone = missing(hits)
    out: list[str] = [
        "تحقيقُ نقلٍ عن حاويةٍ مختومةٍ خارجَ الشجرة",
        "",
        f"المرساة (بصمةٌ مقصوصة): {measured_digest()}",
        f"فقرات: {len(rows)}   ·   غيرُ فارغة: {sum(1 for one in rows if one)}",
        "استخراج: سطرٌ لكلّ <w:p>، ونصُّه من <w:t> — والترقيمُ ناتجُ هذا",
        "",
        "المسبار — يُطلَب النصُّ لا الرقم:",
        "",
    ]
    for one in hits:
        mark = "وُجد" if one.lines else "**غيرُ موجود**"
        where = f"سطر {', '.join(str(i) for i in one.lines[:5])}" if one.lines else "—"
        out.append(f"  [{mark}] {one.text}")
        out.append(f"           {where}   ({one.why})")
    out += [
        "",
        f"أنواعُ العلاقةِ المرقَّمةُ في المتن: {numbered}",
        f"والحاديَ عشرَ (تعلّقُ المصدرِ واسمَي الفاعلِ والمفعول): "
        f"{'وُجد' if eleventh else 'غيرُ موجود'}",
        f"فالمجموعُ المعدود: {numbered + (1 if eleventh else 0)}",
        "",
        f"ما لم يوجد: {'، '.join(gone) if gone else 'لا شيء'}",
        "",
        "الحدّ: هذا يُثبت أنّ المنقولَ في المصدر. ولا يُثبت أنّ ما بُنِي",
        "عليه لازمٌ عنه — فسهمُ المقابلةِ استدلالٌ يُبرهَن وحدَه.",
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    if not held():
        print("الحاويةُ غائبة — والحالُ مُصنَّفةٌ لا مُصفَّرة:")
        print(f"  {HOLDER}")
        print(f"  والمرساةُ المطلوبة: {DIGEST}")
        return 0
    if measured_digest() != DIGEST:
        print(f"حاويةٌ أخرى: {measured_digest()} لا {DIGEST} — لا يُقاس عليها.")
        return 1
    DEPOSIT.write_text(report(), encoding="utf-8")
    print(f"أُودِع: {DEPOSIT.relative_to(REPOSITORY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
