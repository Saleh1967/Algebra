"""تجميدُ فصل الحصر والاستثناء من أنبوبٍ **غيرِ هذه الشجرة**.

`I_CANNOT_REMEASURE_WHAT_I_DO_NOT_HOLD`: لا تشجيرَ في هذه الشجرة، **فلا
يُعاد القياس**. وإنّما **يُعاد الحساب** من الأعداد المعروضة.

`THE_ESTIMATOR_IS_DERIVED_NOT_ASSUMED`: والمنشورُ من المعلومات **لا يوافق
التقديرَ الخام**. **ولم أُسمِّه خطأً**: جرّبتُ التصحيحَ من الرتبة الأولى
(ميلر–مادو) **فأعاد الرقمين معًا إلى أربع منازل**. **فالمقدارُ مُشتَقٌّ لا
مظنون**، والسجلُّ يردُّ نفسَه إن لم يُعِده.

`AND_A_NUMBER_THAT_DOES_NOT_CLOSE_IS_NAMED`: والعرضُ يحمل **عددين
للاستثناء** — ١٠٥ و١٠٢ — **ولا يجتمعان**. وخانتا «النفي السابق» تحملان
**١٠٥** على **٦٦٢** موضعًا، **فيُغلِق ١٠٥ وحدَه**. **والعددُ الآخرُ
يُسمّى ولا يُخمَّن سببُه.**

`AND_THE_GREEDY_SPENT_A_BIT_IT_DID_NOT_NEED`: والتصعيدُ الجشعُ على أربع
خاناتٍ صرف **ثلاثَ بتّاتٍ** والسقفُ الخام **بتّتان**. **فهذا شاهدٌ مقيسٌ
على أنّ الجشعَ غيرُ مبرهَن**، لا في النصّ بل في السلّم نفسِه.

`AND_WHAT_IS_NOT_PUBLISHED_IS_NOT_REBUILT`: وثلاثةُ ملامحَ بلا تفصيل،
وجداءُ الملامح غيرُ منشور. **فلا تُعاد ولا تُصدَّق ولا تُكذَّب**، ولا
يُبنى سلّمٌ عبر ملمحين.

**ولا يوقَّع ههنا تأويل**: لا قراءةُ الكتاب في «إنّما»، ولا حكمُ
المُشجِّر في «إلّا».
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
NOTE: Final[str] = "hasr_rule_note.md"
AUDIT_LOG: Final[str] = "hasr_audit_run.log"
BUNUD_LOG: Final[str] = "foreign_bunud_out.txt"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_PLACES: Final[float] = 5e-5


class HasrLedgerError(ValueError):
    """رُدَّ سجلٌّ لا تُعيد أعدادُه حسابَه، أو ادّعى إعادةَ ما لم يُنشَر."""


def binary(share: float) -> float:
    if share <= 0.0 or share >= 1.0:
        return 0.0
    found = -(share * math.log2(share) + (1 - share) * math.log2(1 - share))
    return 0.0 if found == 0.0 else found


def conditional(cells: tuple[tuple[int, int], ...]) -> float:
    total = sum(one for one, _ in cells)
    return math.fsum(one / total * binary(two / one) for one, two in cells if one)


def miller_madow(cells: int, total: int) -> float:
    """تصحيحُ الانحياز من الرتبة الأولى — يُشتَقّ ولا يُنقَل."""

    return (cells - 1) / (2 * total * math.log(2))


@dataclass(frozen=True, slots=True)
class HasrLedger:
    """فصلُ الحصر والاستثناء مُقفَلًا — وكلُّ عددٍ فيه معروضٌ في الإيداع."""

    total: int
    restriction: int
    exception: int
    rejected_count: int
    sign_cells: tuple[tuple[int, int], ...]
    case_cells: tuple[tuple[int, int], ...]
    published: tuple[tuple[str, str], ...]
    ladder_gains: tuple[str, ...]
    bits_spent: int
    bits_needed: int
    held_out: tuple[tuple[str, int, int], ...]
    confusion: tuple[int, int, int, int]
    shared_row: tuple[str, str, str]
    unbuilt: tuple[str, ...]
    debts: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.restriction + self.exception != self.total:
            raise HasrLedgerError("الحصرُ والاستثناءُ لا يجمعان إلى المقام.")
        if self.rejected_count == self.exception:
            raise HasrLedgerError("العددُ المردودُ يطابق المقبول — فلا خلافَ يُسمّى.")
        if sum(two for _, two in self.sign_cells) != self.exception:
            raise HasrLedgerError("خانتا «النفي» لا تحملان عددَ الاستثناء المقبول.")
        if sum(one for one, _ in self.sign_cells) != self.total:
            raise HasrLedgerError("خانتا «النفي» لا تغطّيان المقام.")
        flat = binary(self.exception / self.total)
        shown = dict(self.published)
        for name, cells in (("م١", self.sign_cells), ("م٢", self.case_cells)):
            rows = list(cells)
            seen = sum(one for one, _ in rows)
            if seen < self.total:
                rows.append(
                    (self.total - seen, self.exception - sum(two for _, two in rows))
                )
            raw = flat - conditional(tuple(rows))
            fixed = raw - miller_madow(len(rows), self.total)
            if abs(fixed - float(shown[name])) > _PLACES:
                raise HasrLedgerError(
                    f"{name}: المنشورُ {shown[name]} والمُصحَّحُ {fixed:.4f}"
                )
            if raw < float(shown[name]):
                raise HasrLedgerError(f"{name}: الخامُ دون المنشور — تصحيحٌ معكوس.")
        gains = [float(one) for one in self.ladder_gains]
        if any(one <= 0 for one in gains):
            raise HasrLedgerError("درجةٌ لا تربح — فالتصعيدُ وقف ولم يُسجَّل.")
        if gains[0] != max(gains):
            raise HasrLedgerError("أوّلُ سؤالٍ ليس أغنى — تصعيدٌ آخر.")
        if self.bits_spent != len(gains):
            raise HasrLedgerError("البتّاتُ المصروفةُ لا توافق عددَ الدرجات.")
        if self.bits_spent <= self.bits_needed:
            raise HasrLedgerError("السجلُّ يحمل دعوى إسرافٍ ولا إسرافَ فيه — فلا يُقفَل.")
        if self.bits_needed != (len(self.case_cells) + 1 - 1).bit_length():
            raise HasrLedgerError("السقفُ الخامُ لا يُشتَقّ من عدد الخانات.")
        right, wrong, missed, caught = self.confusion
        if right + wrong + missed + caught != self.held_out[0][2]:
            raise HasrLedgerError("مصفوفةُ اللبس لا تجمع إلى المحجوز.")
        if right + caught != self.held_out[0][1]:
            raise HasrLedgerError("المصيبُ في المصفوفة لا يوافق المعلَن.")
        if right != self.held_out[1][1]:
            raise HasrLedgerError("الأغلبُ الأعمى لا يوافق صفَّ الحصر.")
        if caught >= missed:
            raise HasrLedgerError(
                "المصنِّفُ أصاب من الاستثناء أكثرَ ممّا أخطأ — والسجلُّ خلافُه."
            )
        if len(self.unbuilt) < 2:
            raise HasrLedgerError("ما لم يُنشَر يُسمّى، ولا سجلَّ يدّعي إعادةَ الكلّ.")
        if not self.debts:
            raise HasrLedgerError("سجلٌّ بلا دَينٍ مُسمًّى دعوى توقيعٍ لا تُقفَل.")
        for name, why in self.debts:
            if not name.strip() or len(why) <= 25:
                raise HasrLedgerError(f"دَينٌ بلا بيانٍ مكتوب: {name}")


FROZEN_HASR: Final[HasrLedger] = HasrLedger(
    total=662,
    restriction=557,
    exception=105,
    rejected_count=102,
    sign_cells=((547, 76), (115, 29)),
    case_cells=((200, 34), (123, 2), (42, 4)),
    published=(("م١", "0.0079"), ("م٢", "0.0378")),
    ladder_gains=("0.035701", "0.003638", "0.001770"),
    bits_spent=3,
    bits_needed=2,
    held_out=(("بايز", 270, 341), ("الأغلبُ الأعمى", 269, 341)),
    confusion=(269, 0, 71, 1),
    shared_row=("شرط", "0.1391", "0.0331"),
    unbuilt=(
        "م٣ وسمُ التالي — بلا تفصيلٍ منشور",
        "م٤ حالةُ السابق — بلا تفصيلٍ منشور",
        "م٥ تعريفُ التالي — بلا تفصيلٍ منشور",
        "جداءُ الملامح — غيرُ منشور، فلا سلّمَ عبر ملمحين",
    ),
    debts=(
        (
            "وسمُ RES/EXP حكمُ مُشجِّرٍ بشر",
            "وهو إقرارُ الأنبوب نفسِه: إن كان تفريقُه غيرَ منضبطٍ فالقياسُ "
            "يقيس اضطرابَه لا اضطرابَ اللغة، ولا يُوقَّع ولا يُردّ",
        ),
        (
            "دعوى الكتاب في «إنّما» غيرُ قابلةٍ للاختبار",
            "التشجيرُ يعطيها وسمًا واحدًا لا يتغيّر في ١٣٢ موضعًا، فلا "
            "تُثبَت ولا تُبطَل بهذه الأداة — وهو إعلانُ الأنبوب لا استنتاجي",
        ),
        (
            "عددان للاستثناء لا يجتمعان",
            "العرضُ يحمل ١٠٥ و١٠٢؛ وخانتا «النفي» تُغلِقان على ١٠٥ وحدَه، "
            "وسببُ الآخر لا يُخمَّن — وقد ورد ١٠٢ في إيداعٍ سابقٍ أيضًا",
        ),
        (
            "ستُّ مئةٍ واثنان وستّون موضعًا",
            "تعدادٌ على مقامه لا حكمٌ على العربيّة؛ ومقامُه ليس مقامَ هذه "
            "الشجرة، فلا يُنقَل رقمٌ من أحدهما إلى الآخر",
        ),
        (
            "موضعُ الفارق بين الحصر والاستثناء",
            "الملامحُ السطحيّةُ لا تُخرِجه؛ وحدُّ الاستثناء يقتضي مستثنًى "
            "منه سابقًا، وهي علاقةٌ تركيبيّةٌ لم تُقَس — دَينٌ لا نتيجة",
        ),
    ),
)


def record_bytes(record: HasrLedger = FROZEN_HASR) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: HasrLedger = FROZEN_HASR) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ الحصر والاستثناء؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: HasrLedger = FROZEN_HASR) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من الإيداع والسجلّات؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name in (NOTE, AUDIT_LOG, BUNUD_LOG):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"مُودَعٌ غائب: {name}")
    if complaints:
        return complaints
    text = (DEPOSITS / AUDIT_LOG).read_text(encoding="utf-8")
    if f"— المقام: {record.total} موضعًا" not in text:
        complaints.append("المقامُ لا يطابق السجلّ")
    if f"⇒ العددُ الذي يُغلِق وحدَه: {record.exception}" not in text:
        complaints.append("العددُ المُغلِقُ لا شاهدَ له")
    if f"استثناء={record.rejected_count}" not in text:
        complaints.append("العددُ المردودُ لا شاهدَ له")
    for name, value in record.published:
        if f"| المنشور {value}" not in text:
            complaints.append(f"{name}: لا شاهدَ في السجلّ لقيمته المنشورة")
    for gain in record.ladder_gains:
        if f"ربحٌ +{gain}" not in text:
            complaints.append(f"درجةٌ بربحٍ {gain}: لا شاهدَ في السجلّ")
    if (
        f"عددُ البتّات المصروفة: {record.bits_spent}"
        f" | والسقفُ الخام ⌈log₂{len(record.case_cells) + 1}⌉"
        f" = {record.bits_needed}"
    ) not in text:
        complaints.append("البتّاتُ والسقفُ لا شاهدَ لهما")
    if f"صرف {record.bits_spent} حيث تكفي {record.bits_needed}" not in text:
        complaints.append("إسرافُ الجشع لا شاهدَ له")
    for label, hits, tries in record.held_out:
        if f"{label:14s} {hits}/{tries} = " not in text:
            complaints.append(f"{label}: لا شاهدَ في السجلّ لذراعه")
    if "أيتداخل المجالان؟ True" not in text:
        complaints.append("تداخلُ المجالين لا شاهدَ له")
    note = (DEPOSITS / NOTE).read_text(encoding="utf-8")
    eastern = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    for number in (record.total, record.restriction, record.exception):
        if str(number).translate(eastern) not in note:
            complaints.append(f"{number}: لا شاهدَ في الإيداع")
    name, height, gain = record.shared_row
    bunud = (DEPOSITS / BUNUD_LOG).read_text(encoding="utf-8")
    if f"{name}            {height}" not in bunud.replace(" ", " "):
        if f"{name}" not in bunud or height not in bunud:
            complaints.append("صفُّ «شرط» لا يُقابَل بالإيداع الأسبق")
    if f"+{gain}" not in bunud:
        complaints.append("كسبُ «شرط» لا يُقابَل بالإيداع الأسبق")
    return complaints
