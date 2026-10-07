"""تجميدُ السلّم: سجلٌّ واحدٌ يحمل المستوياتِ الأربعةَ وما فوقها، ببصمةٍ تُعاد.

**العطلُ الذي يعالجه**: صار السلّمُ يُذكَر **نثرًا** — «ينقلب عند اللفظ»،
«السطرُ أسوأُ الأربعة». والنثرُ يتبدّل ولا يُعرَف تبدّلُه. وأخطرُ منه أنّ
**أسماءَ المستويات** تُنقَل: فقد سمّيتُ اللفظَ كلمةً مرّةً (العطل ١٩)،
والاسمُ يُنقَل ولا يُراجَع.

`THE_RECORD_IS_REDERIVED_NOT_TRANSCRIBED`: وبصمةُ السجلّ **تُشتَقّ من
حقوله**؛ وتبديلُ حقلٍ يُغيّرها ويُسقِط الفحص.

`EVERY_FIELD_IS_CHECKED_AGAINST_THE_DEPOSITED_LOG`: وحقولُه كلُّها
**مقيسة**، ويُعاد التحقّقُ منها في `verify_against_logs` بمطابقة نصّ
`deposits/markov_ladder_run.log` حرفًا بحرف.

`THE_SHAPE_OF_THE_FINDING_IS_ENFORCED_BY_THE_TYPE`: والسلّمُ نفسُه
**شرطُ بناء**: لا يُقفَل سجلٌّ يرتفع فيه الملحَقُ صعودًا، ولا يقع أرخصُ
محجوزٍ في غير الدرجة الثانية، ولا يكون السطرُ أرخصَ من الوحدة، ولا تخرج
`L − H` عن `[٠، ١)`. **فمن بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه.**

`AND_WHAT_THE_BYTES_DO_NOT_LICENSE_IS_CARRIED_AS_VACANT`: وأربعةُ
مستوياتٍ فوق البايتات **محمولةٌ في السجلّ بأسبابها** لا مطويّة: فلا
يُقرأ السلّمُ يومًا كأنّه بلغ الجملة.

**ولا اسمٌ لصنفٍ يدخل**: وحداتٌ وألفاظٌ وأسطرٌ وبتّات.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
LADDER_LOG: Final[str] = "markov_ladder_run.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"


class LadderSealError(ValueError):
    """رُدَّ سجلٌّ لا يحمل شكلَ السلّم، أو خالف السجلَّ في حقلٍ مقيس."""


@dataclass(frozen=True, slots=True)
class SealedLadder:
    """سجلُّ السلّم مُقفَلًا: أربعُ درجاتٍ بأثمانها، وأربعٌ فوقها بأسبابها."""

    names: tuple[str, ...]
    counts: tuple[int, ...]
    alphabets: tuple[int, ...]
    entropies: tuple[str, ...]
    inside_symbol: tuple[str, ...]
    outside_symbol: tuple[str, ...]
    missing: tuple[str, ...]
    flow: tuple[str, ...]
    inside_unit: tuple[str, ...]
    outside_unit: tuple[str, ...]
    gaps: tuple[str, ...]
    stirling: tuple[str, ...]
    vacant: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        widths = {
            one.name: len(getattr(self, one.name))
            for one in fields(self)
            if one.name != "vacant"
        }
        if set(widths.values()) != {4}:
            raise LadderSealError(f"درجاتُ السلّم أربعٌ في كلّ حقل: {widths}.")
        inside = [float(one) for one in self.inside_unit]
        outside = [float(one) for one in self.outside_unit]
        if inside != sorted(inside, reverse=True) or len(set(inside)) != 4:
            raise LadderSealError(
                "الملحَقُ للوحدة ينزل بلا انقطاع صعودًا — وارتفاعُه نقضُ السلّم."
            )
        if outside.index(min(outside)) != 1:
            raise LadderSealError(
                "أرخصُ محجوزٍ في الدرجة الثانية؛ ووقوعُه في غيرها سلّمٌ آخر "
                "يُسجَّل بسجلٍّ آخر."
            )
        if not outside[0] < outside[3]:
            raise LadderSealError("السطرُ أغلى من الوحدة محجوزًا، أو فالسلّمُ غيرُه.")
        if not outside[1] < outside[2] < outside[0]:
            raise LadderSealError(
                "اللفظُ بين الرمزِ المُرخَّص والوحدة محجوزًا — وثَمَّ الانقلاب."
            )
        escapes = [float(one) for one in self.missing]
        if escapes != sorted(escapes):
            raise LadderSealError("نصيبُ المرتدّ لا ينقص صعودًا.")
        for one in self.gaps:
            if not 0 < float(one) < 1:
                raise LadderSealError(f"`L − H` خارجَ [٠، ١): {one}.")
        for one in self.stirling:
            if float(one) <= 0:
                raise LadderSealError(f"`N·H − تباديل` غيرُ موجب: {one}.")
        counts = list(self.counts)
        if counts != sorted(counts, reverse=True) or len(set(counts)) != 4:
            raise LadderSealError("المجرى ينكمش صعودًا في الدرجات الأربع.")
        if len(self.vacant) != 4:
            raise LadderSealError("أربعةُ مستوياتٍ فوق البايتات، لا تُزاد ولا تُنقَص.")
        for name, why in self.vacant:
            if not name.strip() or len(why) <= 25:
                raise LadderSealError(f"مستوًى محمولٌ بلا سببٍ مكتوب: {name}.")


FROZEN_LADDER: Final[SealedLadder] = SealedLadder(
    names=("م٠ الوحدة", "م١ الرمزُ المُرخَّص", "م٢ اللفظُ المفرد", "م٣ السطر"),
    counts=(364_747, 135_603, 78_245, 6_236),
    alphabets=(112, 2_952, 17_909, 6_057),
    entropies=("5.5818", "9.6963", "11.5923", "12.5214"),
    inside_symbol=("5.6048", "9.7250", "11.6195", "12.6005"),
    outside_symbol=("5.6059", "9.8311", "19.6339", "405.7416"),
    missing=("0.0000", "0.0020", "0.1972", "0.9699"),
    flow=("1.2874", "4.3798", "8.1255", "12.4475"),
    inside_unit=("5.6048", "3.6155", "2.4926", "0.2154"),
    outside_unit=("5.6059", "3.6549", "4.2118", "6.9369"),
    gaps=("0.0230", "0.0287", "0.0272", "0.0791"),
    stirling=("718.3", "9997.1", "32137.3", "8785.2"),
    vacant=(
        (
            "الكلمةُ المفردة",
            "حدُّها فصلُ ملتصقٍ عن أصلٍ — قاعدةٌ لا تُشتَقّ من البايتات",
        ),
        (
            "التركيبُ الإسناديّ",
            "يحتاج إسنادًا موقَّعًا بين لفظين، ولا أثرَ له في الرسم",
        ),
        ("التركيبُ المزجيّ", "يحتاج جردًا مُودَعًا لما مُزِج، ولا يميّزه فاصل"),
        ("الجملة", "حدُّها ليس السطرَ ولا الفاصلَ، ويحتاج وقفًا مُودَعًا"),
    ),
)


def record_bytes(record: SealedLadder = FROZEN_LADDER) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedLadder = FROZEN_LADDER) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ السلّم؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedLadder = FROZEN_LADDER) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من السجلّ المُودَع؛ وما خالف يُسمّى."""

    path = DEPOSITS / LADDER_LOG
    if not path.is_file():
        return [f"سجلٌّ مُودَعٌ غائب: {LADDER_LOG}"]
    text = path.read_text(encoding="utf-8")
    complaints: list[str] = []
    for index, name in enumerate(record.names):
        row = (
            f"  {name} | {record.counts[index]} | {record.alphabets[index]} "
            f"| {record.entropies[index]} | {record.inside_symbol[index]} "
            f"| {record.outside_symbol[index]} | {record.missing[index]} "
            f"| {record.flow[index]} | {record.inside_unit[index]} "
            f"| {record.outside_unit[index]} | +{record.gaps[index]} "
            f"| +{record.stirling[index]}"
        )
        if row not in text:
            complaints.append(f"{name}: لا شاهدَ في السجلّ لسطره")
    for name, why in record.vacant:
        if f"  {name}: UNCLASSIFIED — {why}" not in text:
            complaints.append(f"{name}: لا شاهدَ في السجلّ لتصنيفه")
    if f"جملتُها: {len(record.vacant)}" not in text:
        complaints.append("عددُ المستويات المحمولة لا يطابق السجلّ")
    return complaints
