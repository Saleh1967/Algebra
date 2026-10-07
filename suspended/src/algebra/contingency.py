"""جدولُ الاقتران ٢×٢: نسبٌ بكسورٍ صحيحة، وG، والبتّاتُ بمتطابقةٍ تُفحَص.

**ما تفعله هذه الوحدة**: تحسب من جدولٍ ٢×٢ الاحتمالاتِ الشرطيّةَ ونسبةَ
الأرجحيّة **بكسورٍ صحيحةٍ لا بعائم**، وإحصاءةَ `G` بالتوقّعات المُشتَقّة، وكُلفةَ
النموذجين بالبتّات: المتعدّدِ الحرِّ والمستقلّ.

`THE_BITS_AND_THE_G_ARE_THE_SAME_NUMBER_TWICE`: الفرقُ بين كُلفة النموذج
المستقلّ وكُلفة المتعدّد الحرّ هو `KL`، و`G = 2·N·KL` بالنبرات. فالمتطابقةُ
`فرقُ البتّات = G / (2·N·ln2)` **تُفحَص** ههنا: إن لم تصدق فأحدُ الرقمَين محسوبٌ
على عيّنةٍ غير الآخر، أو بمقدِّرٍ آخر — وذلك خبرٌ لا يظهر بالنظر إلى الرقمين.

`AN_EXPECTED_COUNT_IS_DERIVED_NOT_TYPED`: توقّعاتُ الاستقلال تُشتَقّ من هوامش
الجدول، فلا يُكتَب توقّعٌ بيد ولا يُقرَّب قبل الجمع.

`A_ZERO_CELL_HAS_NO_LOGARITHM`: خليّةٌ صفرٌ لا تُسهِم في `G` (حدُّها نهايةً صفر)،
ولكنّها تُبطِل نسبةَ الأرجحيّة قسمةً على صفر؛ فالحالتان مفصولتان ومُعلَنتان.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_DOMAIN`: ما هنا حسابٌ على أربعة أعداد.
وأيُّ قراءةٍ سببيّةٍ لها تُكتَب عند مَن يقرأ، لا ههنا.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Final

__all__ = [
    "AN_EXPECTED_COUNT_IS_DERIVED_NOT_TYPED_NOTE",
    "A_ZERO_CELL_HAS_NO_LOGARITHM_NOTE",
    "CONTINGENCY_NAMED_RESIDUALS",
    "THE_BITS_AND_THE_G_ARE_THE_SAME_NUMBER_TWICE_NOTE",
    "ContingencyError",
    "ModelCost",
    "Table2x2",
]


class ContingencyError(ValueError):
    """رُفض جدولٌ لا يقبل الحساب؛ ولا يُحمَل على أقرب مقبول."""


@dataclass(frozen=True, slots=True)
class ModelCost:
    """كُلفةُ نموذجين بالبتّات، والفرقُ، ومتطابقتُه مع `G`."""

    free_multinomial_bits: float
    independent_bits: float
    excess_bits: float
    g_over_two_n_ln2: float

    @property
    def identity_holds(self) -> bool:
        """أيطابق فرقُ البتّات `G/(2N ln2)`؟ متطابقةٌ تُفحَص لا تُذكَر."""

        return math.isclose(self.excess_bits, self.g_over_two_n_ln2, rel_tol=1e-12)

    @property
    def independent_model_is_worse(self) -> bool:
        """أيُكلِّف النموذجُ المستقلُّ أكثرَ مع معالمَ أقلّ؟"""

        return self.independent_bits > self.free_multinomial_bits


@dataclass(frozen=True, slots=True)
class Table2x2:
    """جدولُ اقترانٍ ٢×٢ بأعداده الصحيحة؛ والصفُّ هو الشرط والعمودُ هو الأثر."""

    no_row_no_column: int
    no_row_column: int
    row_no_column: int
    row_column: int

    def __post_init__(self) -> None:
        for value in self.cells:
            if value < 0:
                raise ContingencyError("خليّةٌ سالبةٌ ليست عددَ مشاهدات.")
        if self.total == 0:
            raise ContingencyError("جدولٌ خالٍ لا يُحسَب عليه شيء.")
        if 0 in (
            self.first_row,
            self.second_row,
            self.first_column,
            self.second_column,
        ):
            raise ContingencyError(
                "هامشٌ صفرٌ: الشرطُ أو الأثرُ غيرُ مشاهَدٍ أصلًا، فلا اقترانَ "
                "يُقاس ولا توقّعٌ يُشتَقّ."
            )

    @property
    def cells(self) -> tuple[int, int, int, int]:
        """الخلايا الأربعُ بترتيبٍ ثابت."""

        return (
            self.no_row_no_column,
            self.no_row_column,
            self.row_no_column,
            self.row_column,
        )

    @property
    def total(self) -> int:
        """مجموعُ المشاهدات."""

        return sum(self.cells)

    @property
    def first_row(self) -> int:
        return self.no_row_no_column + self.no_row_column

    @property
    def second_row(self) -> int:
        return self.row_no_column + self.row_column

    @property
    def first_column(self) -> int:
        return self.no_row_no_column + self.row_no_column

    @property
    def second_column(self) -> int:
        return self.no_row_column + self.row_column

    def column_given_no_row(self) -> Fraction:
        """`P(الأثر | لا شرط)` كسرًا صحيحًا."""

        return Fraction(self.no_row_column, self.first_row)

    def column_given_row(self) -> Fraction:
        """`P(الأثر | الشرط)` كسرًا صحيحًا."""

        return Fraction(self.row_column, self.second_row)

    def risk_ratio(self) -> Fraction:
        """نسبةُ الاحتمالين الشرطيّين؛ وتُرفَض عند صفرٍ في المقام."""

        lower = self.column_given_row()
        if lower == 0:
            raise ContingencyError(
                "الاحتمالُ الشرطيُّ صفرٌ، فالنسبةُ غيرُ معرَّفة؛ ولا تُقرَّب " "إلى عددٍ كبير."
            )
        return self.column_given_no_row() / lower

    def odds_ratio(self) -> Fraction:
        """نسبةُ الأرجحيّة `ad/bc`؛ وتُرفَض عند خليّةٍ صفرٍ في المقام."""

        denominator = self.no_row_column * self.row_no_column
        if denominator == 0:
            raise ContingencyError(
                "خليّةٌ صفرٌ في مقام نسبة الأرجحيّة، فهي غيرُ معرَّفة "
                "(A_ZERO_CELL_HAS_NO_LOGARITHM)."
            )
        return Fraction(self.no_row_no_column * self.row_column, denominator)

    def expected(self) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        """توقّعاتُ الاستقلال مُشتَقّةً من الهوامش، بكسورٍ صحيحة."""

        rows = (self.first_row, self.first_row, self.second_row, self.second_row)
        columns = (
            self.first_column,
            self.second_column,
            self.first_column,
            self.second_column,
        )
        return tuple(  # type: ignore[return-value]
            Fraction(row * column, self.total)
            for row, column in zip(rows, columns, strict=True)
        )

    def g_statistic(self) -> float:
        """`G = 2 Σ O ln(O/E)`؛ والخليّةُ الصفرُ لا تُسهِم (نهايتُها صفر)."""

        return sum(
            2 * observed * math.log(observed / float(expected))
            for observed, expected in zip(self.cells, self.expected(), strict=True)
            if observed
        )

    def z_equivalent(self) -> float:
        """`√G` تقريبًا لدرجةِ حرّيّةٍ واحدة؛ وهو تحويلٌ لا اختبارٌ آخر."""

        return math.sqrt(self.g_statistic())

    def model_cost(self) -> ModelCost:
        """كُلفةُ النموذجين بالبتّات، ومتطابقتُهما مع `G` مفحوصة."""

        total = self.total
        observed = [Fraction(cell, total) for cell in self.cells]
        free = -sum(float(p) * math.log2(float(p)) for p in observed if p)
        row = Fraction(self.second_row, total)
        column = Fraction(self.second_column, total)
        modelled = (
            (1 - row) * (1 - column),
            (1 - row) * column,
            row * (1 - column),
            row * column,
        )
        independent = -sum(
            float(p) * math.log2(float(q))
            for p, q in zip(observed, modelled, strict=True)
            if p
        )
        return ModelCost(
            free_multinomial_bits=free,
            independent_bits=independent,
            excess_bits=independent - free,
            g_over_two_n_ln2=self.g_statistic() / (2 * total * math.log(2)),
        )


THE_BITS_AND_THE_G_ARE_THE_SAME_NUMBER_TWICE_NOTE: Final[str] = (
    "TheBitsAndTheGAreTheSameNumberTwice: فرقُ كُلفة النموذجين بالبتّات يساوي "
    "G/(2N ln2) بالمتطابقة؛ فإن لم يصدق فأحدُ الرقمين على عيّنةٍ غير الآخر أو "
    "بمقدِّرٍ آخر، وذلك خبرٌ لا يظهر بالنظر إلى الرقمين"
)

AN_EXPECTED_COUNT_IS_DERIVED_NOT_TYPED_NOTE: Final[str] = (
    "AnExpectedCountIsDerivedNotTyped: التوقّعاتُ من الهوامش بكسورٍ صحيحة، فلا "
    "يُكتَب توقّعٌ بيد ولا يُقرَّب قبل الجمع"
)

A_ZERO_CELL_HAS_NO_LOGARITHM_NOTE: Final[str] = (
    "AZeroCellHasNoLogarithm: الخليّةُ الصفرُ لا تُسهِم في G ولكنّها تُبطِل نسبةَ "
    "الأرجحيّة؛ والحالتان مفصولتان ومُعلَنتان لا مجموعتان في «صفر»"
)

CONTINGENCY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_BITS_AND_THE_G_ARE_THE_SAME_NUMBER_TWICE_NOTE,
    AN_EXPECTED_COUNT_IS_DERIVED_NOT_TYPED_NOTE,
    A_ZERO_CELL_HAS_NO_LOGARITHM_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
