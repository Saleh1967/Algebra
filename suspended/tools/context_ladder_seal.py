"""تجميدُ سلّم السياق: سجلٌّ واحدٌ يحمل درجاته الاثنتي عشرةَ، ببصمةٍ تُعاد.

**العطلُ الذي يعالجه**: صار السلّمُ يُذكَر **نثرًا** — «أوّلُ بتّةٍ بتّةُ
الموضع»، «التصعيدُ يتجاوز الجار». والنثرُ يتبدّل ولا يُعرَف تبدّلُه.

`THE_RECORD_IS_REDERIVED_NOT_TRANSCRIBED`: وبصمةُ السجلّ **تُشتَقّ من
حقوله**؛ وتبديلُ حقلٍ يُغيّرها ويُسقِط الفحص.

`NO_GLYPH_OF_THE_CORPUS_IS_TYPED_HERE`: **ولا محرفَ من المجمَّد مكتوبٌ في
هذا السجلّ**: الأسئلةُ محفوظةٌ **بصنفها ونقطةِ ترميزها** لا بصورتها، وصورتُها
تُقرَأ من السجلّ المُودَع عند التحقّق. **فلا تُكتَب شريحةٌ بيد** — وهو
العطلُ الثاني، ممنوعًا بالبناء.

`THE_SHAPE_OF_THE_FINDING_IS_ENFORCED_BY_THE_TYPE`: وشكلُ النتيجة **شرطُ
بناء**: لا يُقفَل سجلٌّ ترتفع فيه الملحَقةُ درجةً، ولا يقع أكبرُ ربحٍ في غير
الدرجة الأولى، ولا يكون سؤالُ الأولى غيرَ سؤالِ الموضع، ولا تنزل محجوزةٌ
تحت ملحَقتها، ولا تزيد الكتلُ على الضعف بسؤالٍ واحد، ولا يقلّ مجموعُ الكسب
عن كسب الجار كلِّه. **فمن بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه.**

`AND_THE_MEETING_OF_TWO_SEALS_IS_A_CONSTRUCTION_RULE`: وربحُ الدرجة الأولى
**يُقابَل بما قِيس في `26ae5b5b…`** — `I(الحال ؛ الموضع)` — ويُردّ السجلُّ
إن تباعدا. **فالتلاقي محروسٌ لا مرويّ.**

`AND_WHAT_WAS_NOT_REACHED_IS_CARRIED_AS_A_DEBT`: **والسلّمُ لم يقف**: بلغ
السقفَ المُعلَنَ وكلُّ درجةٍ ربحت محجوزًا. **فالدَّينُ محمولٌ في السجلّ**
بنصّه، ولا يُقرأ السلّمُ يومًا كأنّه بلغ حدَّ المادّة.

**ولا اسمَ بابٍ ولا علامةٍ يدخل**: أصنافُ أسئلةٍ ونقاطُ ترميزٍ وبتّات.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
LADDER_LOG: Final[str] = "context_ladder_run.log"
VERSE_LOG: Final[str] = "verse_ending_run.log"
NEIGHBOUR_LOG: Final[str] = "arabic_token_run.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_MEETING: Final[float] = 5e-4
"""أبعدُ ما يُقبَل بين ربح الدرجة الأولى وما قِيس في ختم خاتمة الآية."""

POSITIONAL: Final[str] = "آخرُ السطر"
HEAD: Final[str] = "أوّلُ السطر"


class ContextLadderError(ValueError):
    """رُدَّ سجلٌّ لا يحمل شكلَ السلّم، أو خالف السجلَّ المُودَع في حقل."""


@dataclass(frozen=True, slots=True)
class SealedContextLadder:
    """سجلُّ سلّم السياق مُقفَلًا: اثنتا عشرةَ درجةً، وما لم يُبلَغ بنصّه."""

    tokens: int
    lines: int
    boxes: int
    field: str
    questions: int
    kinds: tuple[str, ...]
    points: tuple[str, ...]
    inside: tuple[str, ...]
    outside: tuple[str, ...]
    gains_in: tuple[str, ...]
    gains_out: tuple[str, ...]
    blocks: tuple[int, ...]
    whole_in: str
    whole_out: str
    first_share: str
    neighbour: str
    positional: str
    tally: tuple[tuple[str, int], ...]
    unreached: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        rows = (
            "kinds",
            "points",
            "inside",
            "outside",
            "gains_in",
            "gains_out",
            "blocks",
        )
        widths = {one: len(getattr(self, one)) for one in rows}
        if set(widths.values()) != {12}:
            raise ContextLadderError(f"درجاتُ السلّم اثنتا عشرةَ في كلّ حقل: {widths}")
        inside = [float(one) for one in self.inside]
        outside = [float(one) for one in self.outside]
        if inside != sorted(inside, reverse=True) or len(set(inside)) != 12:
            raise ContextLadderError(
                "الملحَقةُ تنزل بلا انقطاع — وارتفاعُها نقضُ مبرهنة التنقيح."
            )
        if any(two < one for one, two in zip(inside, outside)):
            raise ContextLadderError("محجوزةٌ دون ملحَقتها — ونقضُ اتّجاه الانتحال.")
        gains_out = [float(one) for one in self.gains_out]
        if any(one <= 0 for one in gains_out):
            raise ContextLadderError("درجةٌ لا تربح محجوزًا — فالسلّمُ وقف ولم يُسجَّل.")
        if gains_out.index(max(gains_out)) != 0:
            raise ContextLadderError("أكبرُ ربحٍ في غير الدرجة الأولى — سلّمٌ آخر.")
        if self.kinds[0] != POSITIONAL:
            raise ContextLadderError(
                f"سؤالُ الدرجة الأولى «{self.kinds[0]}» لا سؤالُ الموضع — وهو الخبر."
            )
        if any(float(one) <= 0 for one in self.gains_in):
            raise ContextLadderError("درجةٌ لا تربح ملحَقةً — نقضُ مبرهنة التنقيح.")
        blocks = list(self.blocks)
        if blocks != sorted(blocks) or blocks[0] != 2:
            raise ContextLadderError("الكتلُ لا تنمو، أو أولاها ليست كتلتين.")
        if any(two > 2 * one for one, two in zip(blocks, blocks[1:])):
            raise ContextLadderError("سؤالٌ واحدٌ زاد الكتلَ على الضعف.")
        if not float(self.whole_out) > float(self.neighbour):
            raise ContextLadderError(
                "مجموعُ الكسب لا يتجاوز كسبَ الجار كلِّه — فلا فضلَ للتصعيد."
            )
        if not float(self.whole_in) > float(self.whole_out):
            raise ContextLadderError("الملحَقُ لا يعلو المحجوز — ونقضُ الانتحال.")
        if abs(gains_out[0] - float(self.positional)) > _MEETING:
            raise ContextLadderError(
                f"ربحُ الأولى {gains_out[0]} وما قِيس في ختم الخاتمة "
                f"{self.positional} — والتلاقي محروس."
            )
        if abs(gains_out[0] / sum(gains_out) - float(self.first_share)) > 5e-4:
            raise ContextLadderError("نصيبُ الأولى لا يُشتَقّ من الكسب المنشور.")
        if sum(two for _, two in self.tally) != 12:
            raise ContextLadderError("جملةُ الأسئلة المختارة ليست اثنتي عشرة.")
        if any(one == HEAD for one, _ in self.tally):
            raise ContextLadderError("سؤالُ صدر السطر لم يُختَر — فلا يُذكَر مختارًا.")
        if not self.unreached:
            raise ContextLadderError("سجلٌّ بلا دَينٍ مُسمًّى دعوى بلوغٍ لا تُقفَل.")
        for name, why in self.unreached:
            if not name.strip() or len(why) <= 25:
                raise ContextLadderError(f"دَينٌ بلا بيانٍ مكتوب: {name}")
        for one in self.points:
            if one and not (one.startswith("U+") or len(one) <= 1):
                raise ContextLadderError(f"نقطةُ ترميزٍ ليست نقطة: {one}")


FROZEN_CONTEXT: Final[SealedContextLadder] = SealedContextLadder(
    tokens=78_245,
    lines=6_236,
    boxes=8,
    field="2.6106",
    questions=57,
    kinds=(
        "آخرُ السطر",
        "حالُ السابق",
        "حرفُ خاتمةِ السابق",
        "حالُ السابق",
        "حرفُ خاتمةِ السابق",
        "حالُ السابق",
        "حالُ السابق",
        "حالُ ما قبله",
        "حالُ السابق",
        "حرفُ خاتمةِ السابق",
        "حرفُ خاتمةِ السابق",
        "حرفُ خاتمةِ السابق",
    ),
    points=(
        "",
        "U+064C",
        "U+0627",
        "·",
        "U+0646",
        "U+0652",
        "U+064D",
        "⊢",
        "U+0650",
        "U+0647",
        "U+0645",
        "U+0648",
    ),
    inside=(
        "2.5536",
        "2.5348",
        "2.5183",
        "2.4927",
        "2.4790",
        "2.4610",
        "2.4481",
        "2.4326",
        "2.4189",
        "2.4053",
        "2.3912",
        "2.3831",
    ),
    outside=(
        "2.5540",
        "2.5355",
        "2.5192",
        "2.4945",
        "2.4818",
        "2.4644",
        "2.4521",
        "2.4397",
        "2.4271",
        "2.4155",
        "2.4050",
        "2.3989",
    ),
    gains_in=(
        "0.0570",
        "0.0188",
        "0.0165",
        "0.0256",
        "0.0137",
        "0.0180",
        "0.0130",
        "0.0155",
        "0.0137",
        "0.0136",
        "0.0142",
        "0.0081",
    ),
    gains_out=(
        "0.0569",
        "0.0185",
        "0.0162",
        "0.0248",
        "0.0126",
        "0.0174",
        "0.0123",
        "0.0125",
        "0.0125",
        "0.0117",
        "0.0105",
        "0.0061",
    ),
    blocks=(2, 4, 6, 10, 16, 20, 24, 44, 52, 65, 88, 105),
    whole_in="0.227508",
    whole_out="0.211963",
    first_share="0.2684",
    neighbour="0.0653",
    positional="0.056529",
    tally=(
        ("آخرُ السطر", 1),
        ("حالُ السابق", 5),
        ("حالُ ما قبله", 1),
        ("حرفُ خاتمةِ السابق", 5),
    ),
    unreached=(
        (
            "وقوفُ السلّم",
            "بلغ السقفَ المُعلَنَ (اثنتا عشرةَ درجة) وكلُّ درجةٍ ربحت "
            "محجوزًا، فالوقوفُ لم يقع وحدُّ ما تحمله المادّةُ لم يُبلَغ",
        ),
        (
            "أمثليّةُ السلّم",
            "الجشعُ غيرُ مبرهَن: أفضلُ سؤالٍ عند درجةٍ ليس أفضلَ سلّمٍ في "
            "النهاية، فما بُلِغ حدٌّ أدنى لِما يبلغه بحثٌ أوسع",
        ),
        (
            "ما فوق السياق الماضي",
            "لم يُسأل عن شيءٍ من بايتات الموضع نفسِه، وحرفُ خاتمته يحمل "
            "عنه ١٫٠٣١٠ بتًّا — وإدخالُه جوابٌ لا سؤال، فبقي خارجَ السلّم",
        ),
    ),
)


def record_bytes(record: SealedContextLadder = FROZEN_CONTEXT) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedContextLadder = FROZEN_CONTEXT) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ سلّم السياق؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedContextLadder = FROZEN_CONTEXT) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من السجلّات المُودَعة؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name in (LADDER_LOG, VERSE_LOG, NEIGHBOUR_LOG):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"سجلٌّ مُودَعٌ غائب: {name}")
    if complaints:
        return complaints
    text = (DEPOSITS / LADDER_LOG).read_text(encoding="utf-8")
    if f"— الأسطر: {record.lines}" not in text:
        complaints.append("عددُ الأسطر لا يطابق السجلّ")
    if f"— الألفاظ: {record.tokens} | وعبرَ العدّادات {record.tokens}" not in text:
        complaints.append("عددُ الألفاظ لا يطابق السجلّ")
    if f"— خاناتُ الحال: {record.boxes} | H = {record.field}" not in text:
        complaints.append("حقلُ الحال لا يطابق السجلّ")
    if f"— الأسئلةُ المتاحة: {record.questions} " not in text:
        complaints.append("عددُ الأسئلة المتاحة لا يطابق السجلّ")
    for index in range(12):
        point = record.points[index]
        shape = (
            ""
            if not point
            else (
                r"= \S+ " + re.escape(point)
                if point.startswith("U+")
                else "= " + re.escape(point)
            )
        )
        pattern = (
            rf"— د{index + 1} «{re.escape(record.kinds[index])}\s*{shape}»: "
            rf"ملحَقة {re.escape(record.inside[index])} \| "
            rf"محجوزة {re.escape(record.outside[index])} \| "
            rf"ربحٌ ملحَقٌ \+{re.escape(record.gains_in[index])} \| "
            rf"ربحٌ محجوزٌ \+{re.escape(record.gains_out[index])} \| "
            rf"كتلٌ {record.blocks[index]}$"
        )
        if not re.search(pattern, text, re.MULTILINE):
            complaints.append(f"د{index + 1}: لا شاهدَ في السجلّ لسطره")
    for value, label in (
        (f"مجموعُ الكسب المحجوز: +{record.whole_out}", "مجموعُ المحجوز"),
        (f"مجموعُ الكسب الملحَق: +{record.whole_in}", "مجموعُ الملحَق"),
        (
            f"نصيبُ الدرجة الأولى من الكسب المحجوز: {record.first_share}",
            "نصيبُ الأولى",
        ),
        (f"كتلُ آخر درجة: {record.blocks[-1]}", "كتلُ الآخرة"),
        (f"— الدرجاتُ المبلوغة: {len(record.kinds)}", "الدرجاتُ المبلوغة"),
    ):
        if value not in text:
            complaints.append(f"{label}: لا شاهدَ في السجلّ")
    for name, count in record.tally:
        if f"  أسئلةُ «{name}»: {count}" not in text:
            complaints.append(f"جردُ «{name}»: لا شاهدَ في السجلّ")
    if "الوقوف:" in text:
        complaints.append("السجلُّ يذكر وقوفًا، والسجلُّ المُقفَل يحمل خلافه")
    verse = (DEPOSITS / VERSE_LOG).read_text(encoding="utf-8")
    if f"I(الحال ; الموضع) = {record.positional} " not in verse:
        complaints.append("ما قِيس في ختم الخاتمة لا شاهدَ له")
    near = (DEPOSITS / NEIGHBOUR_LOG).read_text(encoding="utf-8")
    if f"\n  I = {record.neighbour}\n" not in near:
        complaints.append("كسبُ الجار لا شاهدَ له")
    return complaints
