"""تجميدُ «ستيرلنغ مع الجشع»: سجلٌّ يحمل **سقوطَ دعوًى** لا صمودَها.

`A_RECORD_THAT_FREEZES_A_REFUTATION`: وأكثرُ ما جُمِّد في هذه الشجرة
نتائجُ صمدت. **وهذا يُجمِّد سقوطًا**: أنّ الحسابَ بعدد التباديل **وقت
الاختيار** لا يُعيد البتّةَ المفقودة، **ولا يُبدِّل اختيارَ الجشع ولا
مرّةً**. **فالسقوطُ أولى بالتجميد من الصمود**، لأنّه أسهلُ نسيانًا.

`THE_SHAPE_OF_THE_FINDING_IS_ENFORCED_BY_THE_TYPE`: ولا يُقفَل سجلٌّ
يختلف فيه المعياران على سؤال، ولا تنكسر فيه الهويّةُ، ولا يصرف الجشعُ فيه
ما يكفي، ولا يقلُّ فيه كسبُ التباديل عن كسب الإنتروبيا، ولا يكون فضاءُ
القسمات أصغرَ ممّا زاره.

`AND_THE_IDENTITY_IS_A_CONSTRUCTION_RULE_NOT_A_SENTENCE`: وفرقُ الكسبين
**يُشتَقّ من الفجوات ويُقابَل بالمنشور**؛ فإن تباعدا رُدَّ السجلّ.

**ولا رقمَ منقول**: الفجواتُ تُحسَب بـ`algebra.stirling`، والقسماتُ
بقاعدة النمط، **ولا جدولَ مُودَع**.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

from algebra.stirling import bell, gap_in_bits, subsets

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
RUN_LOG: Final[str] = "stirling_greedy_run.log"
WITNESS_LOG: Final[str] = "stirling_greedy_witness.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_CLOSES: Final[float] = 1e-9


class StirlingGreedyError(ValueError):
    """رُدَّ سجلٌّ لا يحمل شكلَ النتيجة، أو انكسرت فيه الهويّة."""


@dataclass(frozen=True, slots=True)
class SealedStirlingGreedy:
    """سقوطُ المقترَح مُقفَلًا: المعياران يتّفقان، والبتّةُ لم تعد."""

    stands: tuple[str, ...]
    bits_entropy: tuple[int, ...]
    bits_permutation: tuple[int, ...]
    needed: tuple[int, ...]
    smallest_first: tuple[int, ...]
    disagreements: int
    identity_drift: str
    spread: str
    trivial_edge: str
    honest_edge: str
    cells: int
    visited: int
    blocks: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        wide = {
            one: len(getattr(self, one))
            for one in (
                "stands",
                "bits_entropy",
                "bits_permutation",
                "needed",
                "smallest_first",
            )
        }
        if set(wide.values()) != {2}:
            raise StirlingGreedyError(f"مقامان في كلّ حقل: {wide}")
        if self.bits_entropy != self.bits_permutation:
            raise StirlingGreedyError(
                "المعياران اختلفا في البتّات — والسجلُّ يحمل اتّفاقَهما."
            )
        if self.disagreements != 0:
            raise StirlingGreedyError("سجلٌّ يدّعي الاتّفاق وفيه خلاف.")
        if float(self.identity_drift) > _CLOSES:
            raise StirlingGreedyError("الهويّةُ لم تُغلِق — والفرقُ ليس بالفجوات.")
        if float(self.spread) <= 0:
            raise StirlingGreedyError("كسبُ التباديل لم يفق كسبَ الإنتروبيا.")
        if float(self.trivial_edge) != 0:
            raise StirlingGreedyError("الطرفُ التافهُ ليس صفرًا — فلا تفاهةَ تُسمّى.")
        if not float(self.honest_edge) > float(self.trivial_edge):
            raise StirlingGreedyError("الطرفُ الصادقُ لا يفوق التافه.")
        wasted = [one > two for one, two in zip(self.bits_permutation, self.needed)]
        if wasted != [True, False]:
            raise StirlingGreedyError(
                "الإسرافُ في مقامٍ واحدٍ لا غير — والسجلُّ يحمل خلافَ ذلك."
            )
        if self.visited != bell(self.cells) - 1:
            raise StirlingGreedyError("فضاءُ القسمات لا يُطابِق عددَ بِلّ.")
        found = tuple(
            (one, subsets(self.cells, one)) for one in range(2, self.cells + 1)
        )
        if found != self.blocks:
            raise StirlingGreedyError("أرقامُ ستيرلنغ لا تُشتَقّ من قاعدة النمط.")
        if sum(two for _, two in self.blocks) != self.visited:
            raise StirlingGreedyError("مجموعُ القسمات لا يُطابِق المحسوب.")
        if not self.cells - 1 < self.visited:
            raise StirlingGreedyError("ما زاره الجشعُ ليس دون فضاء القسمات.")


FROZEN_STIRLING: Final[SealedStirlingGreedy] = SealedStirlingGreedy(
    stands=("الحصر", "العدد"),
    bits_entropy=(3, 2),
    bits_permutation=(3, 2),
    needed=(2, 2),
    smallest_first=(1, 2),
    disagreements=0,
    identity_drift="4.974e-14",
    spread="7.497413",
    trivial_edge="0.000000",
    honest_edge="1.873581",
    cells=4,
    visited=14,
    blocks=((2, 7), (3, 6), (4, 1)),
)


def record_bytes(record: SealedStirlingGreedy = FROZEN_STIRLING) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedStirlingGreedy = FROZEN_STIRLING) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ ستيرلنغ مع الجشع؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedStirlingGreedy = FROZEN_STIRLING) -> list[str]:
    """يُعاد اشتقاقُ كلِّ حقلٍ من السجلّين المُودَعين؛ وما خالف يُسمّى."""

    complaints: list[str] = []
    for name in (RUN_LOG, WITNESS_LOG):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"سجلٌّ مُودَعٌ غائب: {name}")
    if complaints:
        return complaints
    text = (DEPOSITS / RUN_LOG).read_text(encoding="utf-8")
    for index, stand in enumerate(record.stands):
        for how, bits in (
            ("إنتروبيا", record.bits_entropy[index]),
            ("تباديل", record.bits_permutation[index]),
        ):
            row = (
                f"  {stand} بمعيار {how}: بتّاتٌ {bits}"
                f" | أوّلُ سؤالٍ أصغرُ كتلةٍ فيه {record.smallest_first[index]}"
            )
            if row not in text:
                complaints.append(f"{stand}/{how}: لا شاهدَ في السجلّ")
    for value, label in (
        (f"درجاتٌ يفترق فيها السؤالُ الأوّل: {record.disagreements}", "الخلاف"),
        (f"أقصى انحرافٍ عن الهويّة: {record.identity_drift}", "الهويّة"),
        (f"فرقٌ +{record.spread}", "الفرق"),
        (f"أدنى فجوةِ ستيرلنغ على الكتل: +{record.trivial_edge}", "الطرفُ التافه"),
        (f"وأدناها على كتلةٍ غيرِ نقيّة: +{record.honest_edge}", "الطرفُ الصادق"),
        (
            f"قسماتُ {record.cells} خاناتٍ (بِلّ ناقصَ الواحدة): {record.visited}"
            f" | وزارها الجشعُ {record.cells - 1}",
            "فضاءُ القسمات",
        ),
    ):
        if value not in text:
            complaints.append(f"{label}: لا شاهدَ في السجلّ")
    for parts, count in record.blocks:
        if f"إلى {parts} كتلًا: S({record.cells},{parts}) = {count}" not in text:
            complaints.append(f"S({record.cells},{parts}): لا شاهدَ في السجلّ")
    proof = (DEPOSITS / WITNESS_LOG).read_text(encoding="utf-8")
    if "لا فرقَ ألبتّة — صفرُ أسطرٍ مختلفة." not in proof:
        complaints.append("شاهدُ عدمِ التبدّل غائب")
    made = gap_in_bits((34, 166))
    if not math.isfinite(made) or made <= 0:
        complaints.append("فجوةُ ستيرلنغ لا تُحسَب من الوحدة المُودَعة")
    return complaints
