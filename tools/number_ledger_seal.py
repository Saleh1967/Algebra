"""تجميدُ فصلٍ من أنبوبٍ **غيرِ هذه الشجرة** — العددُ والمعدود.

**ما هذا السجلّ**: أُودِع في `deposits/number_rule_note.md` فصلٌ نُقِل عن
تشغيلٍ أُجري **خارجَ** هذا المستودع على **تشجيرٍ ليس فيه**. **ولستُ أنا مَن
أجراه ولا مَن يوقّعه.**

`I_CANNOT_REMEASURE_WHAT_I_DO_NOT_HOLD`: لا تشجيرَ ولا حوافَّ في هذه
الشجرة، **فلا يُعاد القياس**. وإنّما **يُعاد الحساب** من الأعداد المعروضة:
الإنتروبياتُ من العدّ، والكسبُ، ومجالاتُ ويلسن، **والتصعيدُ بتّةً بتّة**.

`THE_READING_OF_THE_OUTCOMES_IS_MINE_AND_ITS_WHOLE_WARRANT_IS_ONE_NUMBER`:
والأنبوبُ **لم ينشر توزيعَ مخرج المعدود**، وإنّما نشر المواضعَ والمطابق.
**فقراءتي** أنّ المخرجَ زوجُ (حالةٍ وعدد)، وأنّ المخالفاتِ الثلاثَ
`مجرور-مفرد` بنصّ الإيداع. **وسندُها الوحيدُ أنّها تُعيد `H` المنشورةَ
(١٫٤٧١٧) بلا بقيّة** — وهذا سندٌ يُذكَر بحدّه، **ولا يُسمّى نصَّ الأنبوب**.

`THE_SHAPE_OF_THE_FINDING_IS_ENFORCED_BY_THE_TYPE`: ولا يُقفَل سجلٌّ لا
تُعيد أعدادُه إنتروبياتِه، ولا يبلغ تصعيدُه الشرطَ التامّ، ولا يتجاوز عددُ
بتّاته سقفَه الخام، ولا يكون أوّلُ سؤالٍ أغنى ما بعده، ولا يخلو من دَينه.

`AND_WHAT_IS_NOT_MINE_TO_SIGN_IS_CARRIED_AS_A_DEBT`: والقاعدةُ المنقولة،
وتعليلُ المخالفات الثلاث، وكفايةُ خمسةٍ وثلاثين موضعًا — **كلُّها محمولةٌ
دَينًا بنصّها**، ولا يُقرأ السجلُّ يومًا كأنّه وقّعها.

**ولا يدخل هذا السجلَّ اسمٌ لم يُودَع**: أسماءُ الأصناف والمخرجات **منقولةٌ
عن الإيداع** لا مُخترَعة.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
NOTE: Final[str] = "number_rule_note.md"
LADDER_LOG: Final[str] = "number_ladder_run.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_TOLERANCE: Final[float] = 5e-5


class NumberLedgerError(ValueError):
    """رُدَّ سجلٌّ لا تُعيد أعدادُه حسابَه، أو خلا من دَينه."""


def entropy(counts: tuple[int, ...]) -> float:
    total = sum(counts)
    if total == 0:
        return 0.0
    found = -math.fsum((one / total) * math.log2(one / total) for one in counts if one)
    return 0.0 if found == 0.0 else found


def wilson(hits: int, tries: int) -> tuple[float, float]:
    """مجالُ ويلسن ٩٥٪ — يُشتَقّ ولا يُنقَل."""

    z = 1.959963984540054
    share = hits / tries
    middle = share + z * z / (2 * tries)
    spread = z * math.sqrt(share * (1 - share) / tries + z * z / (4 * tries * tries))
    weight = 1 + z * z / tries
    return (middle - spread) / weight, (middle + spread) / weight


@dataclass(frozen=True, slots=True)
class ForeignNumberLedger:
    """فصلُ العدد والمعدود مُقفَلًا — وكلُّ عددٍ فيه معروضٌ في الإيداع."""

    classes: tuple[str, ...]
    places: tuple[int, ...]
    conforming: tuple[int, ...]
    outcomes: tuple[tuple[str, int], ...]
    flat: str
    given: str
    gain: str
    share: str
    steps: tuple[str, ...]
    step_gains: tuple[str, ...]
    bits: int
    ceiling: int
    held_out: tuple[tuple[str, int, int], ...]
    debts: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if len(self.classes) != 4:
            raise NumberLedgerError("أصنافُ العدد أربعةٌ كما عُرِضت.")
        for name in ("places", "conforming"):
            if len(getattr(self, name)) != 4:
                raise NumberLedgerError(f"{name}: أربعةُ حقولٍ لا غير.")
        if any(one > two for one, two in zip(self.conforming, self.places)):
            raise NumberLedgerError("مطابقٌ يفوق مواضعَه.")
        whole = sum(self.places)
        if whole != sum(two for _, two in self.outcomes):
            raise NumberLedgerError("مخرجاتُ المعدود لا تجمع إلى المواضع.")
        mine = entropy(tuple(two for _, two in self.outcomes))
        if abs(mine - float(self.flat)) > _TOLERANCE:
            raise NumberLedgerError(
                f"H المعروضةُ {self.flat} والمُشتَقّةُ من المخرجات {mine:.4f}"
            )
        conditional = math.fsum(
            self.places[index]
            / whole
            * entropy(
                (self.conforming[index], self.places[index] - self.conforming[index])
            )
            for index in range(4)
        )
        if abs(conditional - float(self.given)) > _TOLERANCE:
            raise NumberLedgerError(
                f"H المشروطةُ المعروضةُ {self.given} والمُشتَقّةُ {conditional:.4f}"
            )
        if abs((float(self.flat) - float(self.given)) - float(self.gain)) > _TOLERANCE:
            raise NumberLedgerError("الكسبُ لا يساوي فرقَ الإنتروبيتين.")
        if abs(float(self.gain) / float(self.flat) - float(self.share)) > _TOLERANCE:
            raise NumberLedgerError("نصيبُ الكسب لا يُشتَقّ من الكسب والحيرة.")
        if len(self.steps) != len(self.step_gains) or len(self.steps) != self.bits:
            raise NumberLedgerError("لكلّ درجةٍ سؤالُها وربحُها، ولا درجةَ بلا واحد.")
        gains = [float(one) for one in self.step_gains]
        if any(one <= 0 for one in gains):
            raise NumberLedgerError("درجةٌ لا تربح — فالتصعيدُ وقف ولم يُسجَّل.")
        if gains[0] != max(gains):
            raise NumberLedgerError("أوّلُ سؤالٍ ليس أغنى — تصعيدٌ آخر.")
        if abs(math.fsum(gains) - float(self.gain)) > _TOLERANCE:
            raise NumberLedgerError("مجموعُ أرباح الدرجات لا يبلغ الكسبَ التامّ.")
        if self.bits > self.ceiling:
            raise NumberLedgerError("بتّاتٌ فوق السقف الخام — تصعيدٌ مُسرِف.")
        if self.ceiling != (len(self.classes) - 1).bit_length():
            raise NumberLedgerError("السقفُ الخامُ لا يُشتَقّ من عدد الأصناف.")
        spans = [wilson(hits, tries) for _, hits, tries in self.held_out]
        if len(spans) != 2:
            raise NumberLedgerError("المحجوزُ ذراعان: القاعدةُ والأغلبُ الأعمى.")
        if not spans[0][0] <= spans[1][1]:
            raise NumberLedgerError("المجالان لا يتداخلان — والسجلُّ يحمل خلافَ ذلك بنصّه.")
        if not self.debts:
            raise NumberLedgerError("سجلٌّ بلا دَينٍ مُسمًّى دعوى توقيعٍ لا تُقفَل.")
        for name, why in self.debts:
            if not name.strip() or len(why) <= 25:
                raise NumberLedgerError(f"دَينٌ بلا بيانٍ مكتوب: {name}")


FROZEN_NUMBERS: Final[ForeignNumberLedger] = ForeignNumberLedger(
    classes=("٣–١٠", "١١–١٩", "عقود", "مئة/ألف"),
    places=(20, 6, 6, 3),
    conforming=(17, 6, 6, 3),
    outcomes=(("مجرور-جمع", 17), ("منصوب-مفرد", 12), ("مجرور-مفرد", 6)),
    flat="1.4717",
    given="0.3485",
    gain="1.1232",
    share="0.7632",
    steps=("مئة/ألف و٣–١٠", "٣–١٠"),
    step_gains=("0.927527", "0.195671"),
    bits=2,
    ceiling=2,
    held_out=(("القاعدة", 12, 15), ("الأغلبُ الأعمى", 8, 15)),
    debts=(
        (
            "القاعدةُ المنقولة",
            "نُقِلت عن مصادرَ خارجيّةٍ ولم تُشتَقّ من بايتات المجمَّد، "
            "فهي مُدخَلٌ يُختبَر لا حكمٌ يُبنى عليه، وتوقيعُها ليس فعلي",
        ),
        (
            "تعليلُ المخالفات الثلاث",
            "قولُ الأنبوب إنّها جموعُ تكسيرٍ وُسِمت مفردًا؛ وفضُّه يحتاج "
            "التشجيرَ وليس مُودَعًا في هذه الشجرة، فلا يُوقَّع ولا يُردّ",
        ),
        (
            "كفايةُ خمسةٍ وثلاثين موضعًا",
            "تعدادٌ تامٌّ على مقامه لا حكمٌ على العربيّة؛ ومقامُه ليس مقامَ "
            "هذه الشجرة، فلا يُنقَل رقمٌ من أحدهما إلى الآخر",
        ),
        (
            "توزيعُ مخرج المعدود",
            "لم ينشره الأنبوب، وقراءتي له سندُها الوحيدُ أنّها تُعيد H "
            "المنشورةَ بلا بقيّة — وهذا سندٌ يُذكَر بحدّه لا نصُّ الأنبوب",
        ),
        (
            "غيابُ التسجيل المسبق",
            "الفصلُ بلا تسجيلٍ مسبقٍ بإقرار الأنبوب نفسِه، وترويسةُ برنامجه "
            "تحيل إلى ملفٍّ لم يُكتَب — وهو إقرارُه لا استنتاجي",
        ),
    ),
)


def record_bytes(record: ForeignNumberLedger = FROZEN_NUMBERS) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: ForeignNumberLedger = FROZEN_NUMBERS) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ العدد والمعدود؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: ForeignNumberLedger = FROZEN_NUMBERS) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من الإيداع والسجلّ؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name in (NOTE, LADDER_LOG):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"مُودَعٌ غائب: {name}")
    if complaints:
        return complaints
    note = (DEPOSITS / NOTE).read_text(encoding="utf-8")
    text = (DEPOSITS / LADDER_LOG).read_text(encoding="utf-8")
    eastern = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    for index, name in enumerate(record.classes):
        places = str(record.places[index]).translate(eastern)
        right = str(record.conforming[index]).translate(eastern)
        if f"| {name} | {places} | {right} |" not in note:
            complaints.append(f"{name}: لا شاهدَ في الإيداع لصفّه")
        row = (
            f"    {name:8s} مواضعُ {record.places[index]:2d} "
            f"| مطابقٌ {record.conforming[index]:2d}"
        )
        if row not in text:
            complaints.append(f"{name}: لا شاهدَ في السجلّ لسطره")
    whole = sum(record.places)
    if f"— المواضعُ ذاتُ الحافّة: {whole} " not in text:
        complaints.append("المقامُ لا يطابق السجلّ")
    for key, count in record.outcomes:
        if f"    {key:12s} {count:2d} " not in text:
            complaints.append(f"مخرجُ {key}: لا شاهدَ في السجلّ")
    for value, label in (
        (f"H(المعدود) بلا شرط = {record.flat}", "الحيرةُ بلا شرط"),
        (f"H(المعدود | صنفِ العدد) = {record.given}", "الحيرةُ مشروطةً"),
        (f"الكسب = +{record.gain} ", "الكسب"),
        (f"عددُ البتّات المصروفة: {record.bits}", "البتّاتُ المصروفة"),
        (f"⌈log₂{len(record.classes)}⌉ = {record.ceiling}", "السقفُ الخام"),
        ("بلغ التصعيدُ الشرطَ التامَّ: True", "بلوغُ الشرط التامّ"),
    ):
        if value not in text:
            complaints.append(f"{label}: لا شاهدَ في السجلّ")
    for index, step in enumerate(record.steps):
        if f"«أمن {step}؟»" not in text:
            complaints.append(f"د{index + 1}: لا شاهدَ في السجلّ لسؤاله")
        if f"ربحٌ +{record.step_gains[index]}" not in text:
            complaints.append(f"د{index + 1}: لا شاهدَ في السجلّ لربحه")
    for label, hits, tries in record.held_out:
        low, high = wilson(hits, tries)
        row = (
            f"{label:14s} {hits}/{tries} = {hits / tries:.4%}"
            f" | ويلسن ٩٥٪ [{low:.4%} , {high:.4%}]"
        )
        if row not in text:
            complaints.append(f"{label}: لا شاهدَ في السجلّ لمجاله")
    if "أيتداخل المجالان؟ True" not in text:
        complaints.append("تداخلُ المجالين لا شاهدَ له")
    return complaints
