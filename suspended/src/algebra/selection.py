"""عيّنةٌ مشروطةٌ بمصدر: نصفُ جدولٍ لا يُقاس عليه اقتران، والصفرُ فيه ليس صفرًا.

**ما تفعله هذه الوحدة**: تصف عيّنةً **انتُقيت بقيمةِ أحد المحورين** — كلُّ
صفوفها تحمل `الشرط` — فتردّ قياسَ الاقتران عليها، وتُعدِّد الخلايا الغائبة،
وتُوطِّن عددًا من خارجٍ في الصفّ الغائب. وهي لا تعرف موضوعًا: أربعةُ أعداد
أحدُها مجهول.

`A_SAMPLE_SELECTED_ON_ONE_SOURCE_CANNOT_MEASURE_AGREEMENT`: إن كانت العيّنةُ
كلُّها «المصدرُ الأوّلُ قال نعم»، فالصفُّ «قال لا» **غيرُ مرصودٍ بالبناء**.
والاتّفاقُ دالّةٌ في الصفّين معًا، فلا يُقاس من أحدهما. وهذا ردٌّ في المتن لا
تحفّظٌ في هامش.

`A_ZERO_IN_A_CONDITIONED_CELL_IS_NOT_A_ZERO_IN_THE_TABLE`: «صفرُ اتّفاقٍ» في
عيّنةٍ مشروطةٍ يعني: لم يجتمع الوسمان **فيما انتُقي**. وقد يكون العمودُ
الموجبُ مأهولًا بالمئات خارجَها. فالصفرُ خبرٌ عن **الانتقاء** حتى يُفحَص
الصفُّ الآخر.

`AN_OUTSIDE_COUNT_LOCATES_THE_MISSING_ROW`: عددٌ يُعرَف من خارج العيّنة
للعمود الموجب يُحدِّد حدًّا أدنى للخليّة الغائبة: `خارجٌ − مرصودٌ`. فالمجهولُ
يصير **محدودًا من أسفل** بلا تشغيلٍ جديد.

`A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS`: «العلّةُ في أ **أو** ب» ليست خانةً في
قسمةٍ بل امتناعٌ عن القسمة. والقسمةُ الديكارتيّةُ لا «أو» فيها: تُفكَّك حتى
يصير لكلّ موضعٍ فحصٌ يفصله عن جاره.

`THE_COMPLETION_IS_ONE_PASS_NOT_A_NEW_STUDY`: إكمالُ الصفّ الغائب مرورٌ واحدٌ
على المجتمع الموجب، لا دراسةٌ ثانية. وتأجيلُه بحجّة الكلفة تأجيلٌ بلا ثمن.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Final

__all__ = [
    "AN_OUTSIDE_COUNT_LOCATES_THE_MISSING_ROW_NOTE",
    "A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS_NOTE",
    "A_SAMPLE_SELECTED_ON_ONE_SOURCE_CANNOT_MEASURE_AGREEMENT_NOTE",
    "A_ZERO_IN_A_CONDITIONED_CELL_IS_NOT_A_ZERO_IN_THE_TABLE_NOTE",
    "ConditionedTable",
    "Locus",
    "SELECTION_NAMED_RESIDUALS",
    "SelectionError",
    "THE_COMPLETION_IS_ONE_PASS_NOT_A_NEW_STUDY_NOTE",
    "partition_of_loci",
]


class SelectionError(ValueError):
    """رُفض قياسٌ على نصف جدول، أو موضعٌ فيه «أو»؛ ولا يُحمَل على أقرب."""


@dataclass(frozen=True, slots=True)
class ConditionedTable:
    """جدولٌ نصفُه مرصود: صفُّ الشرط معدودٌ، وصفُّ نقيضه غائبٌ بالبناء."""

    condition: str
    absent_row: str
    positive: int
    negative: int
    outside_positive_total: int | None = None

    def __post_init__(self) -> None:
        if not self.condition.strip() or not self.absent_row.strip():
            raise SelectionError("الشرطُ والصفُّ الغائبُ يُسمّيان كلاهما.")
        if self.positive < 0 or self.negative < 0:
            raise SelectionError("عددٌ سالبٌ ليس خليّة.")
        if self.positive + self.negative == 0:
            raise SelectionError("صفٌّ خالٍ لا يُقرَأ.")
        if (
            self.outside_positive_total is not None
            and self.outside_positive_total < self.positive
        ):
            raise SelectionError(
                "العددُ الخارجيُّ للعمود الموجب دون المرصود داخلَه، "
                "فأحدُ العدَّين على مجتمعٍ غير الآخر."
            )

    @property
    def observed_total(self) -> int:
        """ما رُصِد فعلًا: صفُّ الشرط وحدَه."""

        return self.positive + self.negative

    @property
    def missing_cells(self) -> int:
        """الخلايا الغائبةُ من الجدء ٢×٢ — اثنتان دائمًا."""

        return 2

    @property
    def association_is_measurable(self) -> bool:
        """أيُقاس اقترانٌ من هذا؟ لا — والجوابُ ثابتٌ لا مشروط."""

        return False

    def assert_measurable(self) -> None:
        """ردُّ قياس الاقتران على نصف جدولٍ، بتسمية الصفّ الغائب."""

        raise SelectionError(
            f"العيّنةُ كلُّها «{self.condition}»، والصفُّ «{self.absent_row}» "
            "غيرُ مرصودٍ بالبناء؛ فلا يُقاس اقترانٌ من نصف جدول "
            "(A_SAMPLE_SELECTED_ON_ONE_SOURCE_CANNOT_MEASURE_AGREEMENT)."
        )

    def missing_positive_at_least(self) -> int:
        """حدٌّ أدنى للخليّة الغائبة الموجبة من عددٍ خارجيّ؛ ويُرَدّ بلا عدد."""

        if self.outside_positive_total is None:
            raise SelectionError(
                "لا عددَ خارجيًّا للعمود الموجب، فلا يُحَدّ المجهولُ من أسفل."
            )
        return self.outside_positive_total - self.positive

    def zero_is_about_selection_not_the_column(self) -> bool:
        """أيكون الصفرُ المرصودُ خبرًا عن الانتقاء لا عن العمود؟

        نعم متى كان العمودُ الموجبُ مأهولًا خارجَ العيّنة والمرصودُ فيه صفرًا.
        """

        return self.positive == 0 and bool(self.outside_positive_total)

    def share_of_the_column_that_escaped(self) -> Fraction:
        """كم من العمود الموجب وقع **خارجَ** العيّنة، كسرًا صحيحًا."""

        if not self.outside_positive_total:
            raise SelectionError("لا عددَ خارجيًّا يُنسَب إليه الهارب.")
        return Fraction(
            self.outside_positive_total - self.positive, self.outside_positive_total
        )


@dataclass(frozen=True, slots=True)
class Locus:
    """موضعٌ محتمَلٌ للعلّة: اسمُه وحالُه والفحصُ الذي يفصله عن جاره."""

    name: str
    settled: bool
    deciding_test: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SelectionError("موضعٌ بلا اسمٍ لا يُحاسَب.")
        if " أو " in self.name or "/" in self.name:
            raise SelectionError(
                f"«{self.name}» موضعان في خانةٍ واحدة؛ والقسمةُ لا «أو» فيها "
                "(A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS)."
            )
        if not self.deciding_test.strip():
            raise SelectionError(
                f"«{self.name}» بلا فحصٍ فاصلٍ، فلا يُفصَل عن جاره "
                "(A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS)."
            )


def partition_of_loci(loci: tuple[Locus, ...]) -> tuple[Locus, ...]:
    """قسمةُ المواضع: أسماءٌ مميَّزةٌ، ولكلٍّ فحصٌ، وواحدٌ على الأقلّ لم يُحسَم."""

    if not loci:
        raise SelectionError("قسمةٌ بلا مواضعَ ليست قسمة.")
    names = [locus.name for locus in loci]
    if len(set(names)) != len(names):
        raise SelectionError("المواضعُ تُسمّى أسماءً مميَّزة.")
    tests = [locus.deciding_test for locus in loci]
    if len(set(tests)) != len(tests):
        raise SelectionError(
            "موضعان بفحصٍ واحدٍ لا يُفصَل أحدُهما عن الآخر، فهما موضعٌ واحد."
        )
    if all(locus.settled for locus in loci):
        raise SelectionError("حُسِمت المواضعُ كلُّها والأثرُ قائم؛ فالقسمةُ ناقصةٌ لا تامّة.")
    return loci


A_SAMPLE_SELECTED_ON_ONE_SOURCE_CANNOT_MEASURE_AGREEMENT_NOTE: Final[str] = (
    "ASampleSelectedOnOneSourceCannotMeasureAgreement: عيّنةٌ كلُّها «المصدرُ "
    "الأوّلُ قال نعم» صفُّها المقابلُ غيرُ مرصودٍ بالبناء، والاتّفاقُ دالّةٌ "
    "في الصفّين معًا"
)

A_ZERO_IN_A_CONDITIONED_CELL_IS_NOT_A_ZERO_IN_THE_TABLE_NOTE: Final[str] = (
    "AZeroInAConditionedCellIsNotAZeroInTheTable: «صفرُ اتّفاقٍ» في عيّنةٍ "
    "مشروطةٍ خبرٌ عن الانتقاء حتى يُفحَص الصفُّ الآخر"
)

AN_OUTSIDE_COUNT_LOCATES_THE_MISSING_ROW_NOTE: Final[str] = (
    "AnOutsideCountLocatesTheMissingRow: عددٌ خارجيٌّ للعمود الموجب يُحدّ "
    "المجهولَ من أسفل بـ«خارجٌ − مرصود» بلا تشغيلٍ جديد"
)

A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS_NOTE: Final[str] = (
    "ADisjunctiveLocusIsNotALocus: «العلّةُ في أ أو ب» امتناعٌ عن القسمة لا "
    "خانةٌ فيها؛ وتُفكَّك حتى يصير لكلّ موضعٍ فحصٌ يفصله عن جاره"
)

THE_COMPLETION_IS_ONE_PASS_NOT_A_NEW_STUDY_NOTE: Final[str] = (
    "TheCompletionIsOnePassNotANewStudy: إكمالُ الصفّ الغائب مرورٌ واحدٌ على "
    "المجتمع الموجب، وتأجيلُه بحجّة الكلفة تأجيلٌ بلا ثمن"
)

SELECTION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_SAMPLE_SELECTED_ON_ONE_SOURCE_CANNOT_MEASURE_AGREEMENT_NOTE,
    A_ZERO_IN_A_CONDITIONED_CELL_IS_NOT_A_ZERO_IN_THE_TABLE_NOTE,
    AN_OUTSIDE_COUNT_LOCATES_THE_MISSING_ROW_NOTE,
    A_DISJUNCTIVE_LOCUS_IS_NOT_A_LOCUS_NOTE,
    THE_COMPLETION_IS_ONE_PASS_NOT_A_NEW_STUDY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
