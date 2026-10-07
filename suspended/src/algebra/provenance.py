"""ختمُ النسبة: رقمٌ يحمل مدوّنتَه ومقياسَه ووحدتَه، فالنقلُ يُعلَن أو يُرَدّ.

**العطلُ الذي تعالجه هذه الوحدة**: ثوابتُ هذا المستودع كلُّها مقيسةٌ على
مدوّنةٍ بعينها، وأكثرُها على المصحف. ومن شحن أداةً منها على نصٍّ آخرَ **نقل
رقمَها لا خدمتَها**. والامتناعُ عن النقل ليس حلًّا — فالمنقولُ بنسبته مقبول.
والحلُّ أن يصير النقلُ **فعلًا مُعلَنًا**: رقمٌ يحمل ختمَه، فالنقلُ الخفيُّ
مستحيلٌ بالبناء والمُعلَنُ مفتوح.

`A_NUMBER_WITHOUT_ITS_CORPUS_IS_A_RUMOUR`: ولا تُقارَن قيمتان حتّى يُعلَم
أهما من مقياسٍ واحدٍ وبوحدةٍ واحدة. فمقياسان مختلفان لا يُطرَح أحدُهما من
الآخر **ولو كانت المدوّنةُ واحدة**؛ وهذا أكثرُ ما سقط في هذا العمل.

`A_DIFFERENT_CORPUS_IS_A_DECLARATION_NOT_A_REFUSAL`: وأمّا اختلافُ المدوّنة
فليس مانعًا: يُقارَن ويُكتَب أنّ المقارنةَ **عبر مدوّنتين**، فيصير الفرقُ
خبرًا عن المدوّنتين لا عن الظاهرة. والخطرُ في السكوت لا في النقل.

`THE_UNIT_IS_PART_OF_THE_STATISTIC_NOT_A_FOOTNOTE`: ونصيبُ الأنواع غيرُ
نصيب الوقوعات غيرُ نصيب اللِّمَم. فالوحدةُ حقلٌ شرطَ إنشاءٍ ههنا، لا حاشيةٌ
تُقرَأ عند الاختلاف.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Final

__all__ = [
    "A_DIFFERENT_CORPUS_IS_A_DECLARATION_NOT_A_REFUSAL_NOTE",
    "A_NUMBER_WITHOUT_ITS_CORPUS_IS_A_RUMOUR_NOTE",
    "Corpus",
    "PROVENANCE_NAMED_RESIDUALS",
    "ProvenanceError",
    "Reading",
    "THE_UNIT_IS_PART_OF_THE_STATISTIC_NOT_A_FOOTNOTE_NOTE",
]


class ProvenanceError(ValueError):
    """رُفضت مقارنةٌ بين مقياسين أو وحدتين، أو ختمٌ ناقص."""


@dataclass(frozen=True, slots=True)
class Corpus:
    """مدوّنةٌ مختومة: اسمُها وبصمةُ بايتاتها وحجمُها بوحدةٍ مُسمّاة."""

    name: str
    digest: str
    size: int
    size_unit: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ المدوّنة"),
            (self.digest, "بصمتُها"),
            (self.size_unit, "وحدةُ حجمها"),
        ):
            if not value.strip():
                raise ProvenanceError(f"{label} يُكتَب؛ ومدوّنةٌ بلا ختمٍ لا يُنسَب إليها.")
        if len(self.digest) != 64 or set(self.digest) - set("0123456789abcdef"):
            raise ProvenanceError(
                "البصمةُ أربعٌ وستّون خانةً ستّةَ عشريّة؛ " "واسمٌ بلا بصمةٍ ليس ختمًا."
            )
        if self.size <= 0:
            raise ProvenanceError("مدوّنةٌ بحجمٍ غيرِ موجبٍ لا تُقاس.")


@dataclass(frozen=True, slots=True)
class Reading:
    """قيمةٌ مختومة: مقياسُها، ووحدتُها، ومدوّنتُها — والثلاثةُ شرطُ إنشاء."""

    value: Fraction
    statistic: str
    unit: str
    corpus: Corpus

    def __post_init__(self) -> None:
        for value, label in ((self.statistic, "اسمُ المقياس"), (self.unit, "الوحدة")):
            if not value.strip():
                raise ProvenanceError(
                    f"{label} يُكتَب؛ فقيمةٌ بلا مقياسٍ ولا وحدةٍ إشاعةٌ لا رقم."
                )

    @property
    def stamp(self) -> str:
        """الختمُ مقروءًا سطرًا واحدًا؛ يُطبَع مع الرقم دائمًا."""

        return (
            f"{self.statistic} · وحدةً: {self.unit} · "
            f"مدوّنةً: {self.corpus.name} ({self.corpus.digest[:8]}…)"
        )

    def comparable_with(self, other: Reading) -> bool:
        """أيُقارَنان أصلًا؟ ولا يكون إلّا باتّحاد المقياس والوحدة."""

        return self.statistic == other.statistic and self.unit == other.unit

    def against(self, other: Reading) -> tuple[Fraction, str]:
        """(الفرقُ، بيانُه) — ويُرَدّ ما لم يتّحد المقياسُ والوحدة.

        واختلافُ المدوّنة **يُعلَن ولا يمنع**: الفرقُ حينئذٍ خبرٌ عن
        المدوّنتين، ويُكتَب ذلك في بيانه فلا يُقرَأ خبرًا عن الظاهرة.
        """

        if self.statistic != other.statistic:
            raise ProvenanceError(
                f"مقياسان لا مقياس: «{self.statistic}» و«{other.statistic}»؛ "
                "ولا يُطرَح أحدُهما من الآخر ولو اتّحدت المدوّنة."
            )
        if self.unit != other.unit:
            raise ProvenanceError(
                f"وحدتان لا وحدة: «{self.unit}» و«{other.unit}»؛ "
                "والوحدةُ جزءٌ من المقياس لا حاشيةٌ فيه."
            )
        gap = self.value - other.value
        if self.corpus.digest == other.corpus.digest:
            return gap, f"مدوّنةٌ واحدة ({self.corpus.name})"
        return gap, (
            f"**عبر مدوّنتين**: {self.corpus.name} و{other.corpus.name} — "
            "فالفرقُ خبرٌ عنهما معًا، لا عن الظاهرة وحدَها"
        )


A_NUMBER_WITHOUT_ITS_CORPUS_IS_A_RUMOUR_NOTE: Final[str] = (
    "ANumberWithoutItsCorpusIsARumour: قيمةٌ بلا مقياسٍ ووحدةٍ ومدوّنةٍ لا "
    "تُقارَن بشيء؛ والختمُ يُطبَع مع الرقم لا في حاشيته"
)

A_DIFFERENT_CORPUS_IS_A_DECLARATION_NOT_A_REFUSAL_NOTE: Final[str] = (
    "ADifferentCorpusIsADeclarationNotARefusal: النقلُ عبر مدوّنتين مقبولٌ "
    "بنسبته، ومردودٌ بسكوته؛ فالفرقُ حينئذٍ خبرٌ عن المدوّنتين معًا"
)

THE_UNIT_IS_PART_OF_THE_STATISTIC_NOT_A_FOOTNOTE_NOTE: Final[str] = (
    "TheUnitIsPartOfTheStatisticNotAFootnote: نصيبُ الأنواع غيرُ نصيب "
    "الوقوعات غيرُ نصيب اللِّمَم؛ والوحدةُ شرطُ إنشاءٍ لا حاشية"
)

PROVENANCE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_NUMBER_WITHOUT_ITS_CORPUS_IS_A_RUMOUR_NOTE,
    A_DIFFERENT_CORPUS_IS_A_DECLARATION_NOT_A_REFUSAL_NOTE,
    THE_UNIT_IS_PART_OF_THE_STATISTIC_NOT_A_FOOTNOTE_NOTE,
)
