"""إسنادٌ تامٌّ على حاصل ضربِ عاملين مغلقين: لا خليّةَ فارغةٌ ولا مزدوجة.

**ما تفعله هذه الوحدة**: تأخذ صفوفًا وأعمدةً مغلقةً، وخلايا، وقائمةَ خلايا
**ممتنعةٍ مُعلَنة** — فتفحص أنّ الإسنادَ **تامٌّ ودالّيّ** على ما ليس ممتنعًا،
ثمّ تُخرِج ما لا يُرى بالنظر: أيُّ صفوفٍ **لا يفرّق بينها الإسنادُ أصلًا**،
وأيُّ عمودٍ يفرّق بين صفّين. وهي لا تعرف موضوعًا: أسماءٌ في شبكة.

`AN_EMPTY_CELL_IS_A_HOLE_NOT_A_DEFAULT`: خليّةٌ غيرُ مذكورةٍ ليست «الشائع»
ولا «كالأصل»؛ هي ثغرةٌ تُرَدّ عند الإنشاء. فإن كانت الخليّةُ لا تقع في اللغة
فهي **ممتنعةٌ تُعلَن**، والفرقُ بين «ممتنعٍ» و«منسيٍّ» هو مدارُ الصحّة.

`A_FORBIDDEN_CELL_IS_A_CLAIM_NOT_A_GAP`: إعلانُ الامتناع دعوًى قابلةٌ للنقض
(«لا جرَّ في الأفعال»)، لا إعفاءٌ من الملء. فتُسمّى وتُفحَص كسائر الدعاوى.

`A_TABLE_THAT_CANNOT_SEPARATE_TWO_ROWS_DOES_NOT_DISTINGUISH_THEM`: صفّان
بتوقيعٍ واحدٍ **لا يميّزهما الإسنادُ**، مهما اختلف اسماهما. وذلك خبرٌ عن
النظام لا عيبٌ في الجدول، ويُخرَج صريحًا كيلا يُظَنّ التمييزُ حاصلًا.

`THE_SEPARATING_COLUMN_IS_NAMED`: حين يفترق صفّان في عمودٍ واحدٍ فقط، يُسمّى
ذلك العمود. فهو الموضعُ الذي يقوم عليه الفرقُ كلُّه، وسقوطُه يُلغيه.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "ASSIGNMENT_NAMED_RESIDUALS",
    "AN_EMPTY_CELL_IS_A_HOLE_NOT_A_DEFAULT_NOTE",
    "A_FORBIDDEN_CELL_IS_A_CLAIM_NOT_A_GAP_NOTE",
    "A_TABLE_THAT_CANNOT_SEPARATE_TWO_ROWS_DOES_NOT_DISTINGUISH_THEM_NOTE",
    "Assignment",
    "AssignmentError",
    "THE_SEPARATING_COLUMN_IS_NAMED_NOTE",
]


class AssignmentError(ValueError):
    """رُفض إسنادٌ ناقصٌ أو مزدوجٌ أو على خليّةٍ ممتنعة؛ ولا يُكمَّل صمتًا."""


@dataclass(frozen=True, slots=True)
class Assignment:
    """جدولُ إسنادٍ تامٌّ: صفوفٌ وأعمدةٌ مغلقةٌ، وخلايا، وممتنعاتٌ مُعلَنة."""

    rows: tuple[str, ...]
    columns: tuple[str, ...]
    cells: tuple[tuple[str, str, str], ...]
    forbidden: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        for axis, name in ((self.rows, "الصفوف"), (self.columns, "الأعمدة")):
            if not axis:
                raise AssignmentError(f"{name} لا تكون خاليةً.")
            if len(set(axis)) != len(axis):
                raise AssignmentError(f"{name} تُسمّى أسماءً مميَّزة.")
        for row, column in self.forbidden:
            self._check_coordinate(row, column)
        forbidden = set(self.forbidden)
        if len(forbidden) != len(self.forbidden):
            raise AssignmentError("الممتنعاتُ لا تتكرّر.")
        seen: set[tuple[str, str]] = set()
        for row, column, value in self.cells:
            self._check_coordinate(row, column)
            if not value.strip():
                raise AssignmentError(f"خليّةُ ({row}، {column}) بلا قيمة.")
            if (row, column) in forbidden:
                raise AssignmentError(
                    f"({row}، {column}) مُعلَنةٌ ممتنعةً فلا تُملأ "
                    "(A_FORBIDDEN_CELL_IS_A_CLAIM_NOT_A_GAP)."
                )
            if (row, column) in seen:
                raise AssignmentError(f"({row}، {column}) مُسنَدةٌ مرّتين.")
            seen.add((row, column))
        holes = [
            (row, column)
            for row in self.rows
            for column in self.columns
            if (row, column) not in forbidden and (row, column) not in seen
        ]
        if holes:
            shown = "، ".join(f"({row}، {column})" for row, column in holes[:4])
            raise AssignmentError(
                f"ثغراتٌ غيرُ مُعلَنةٍ ({len(holes)}): {shown}… — والخليّةُ "
                "الفارغةُ ليست شائعًا ولا أصلًا "
                "(AN_EMPTY_CELL_IS_A_HOLE_NOT_A_DEFAULT)."
            )

    def _check_coordinate(self, row: str, column: str) -> None:
        if row not in self.rows:
            raise AssignmentError(f"«{row}» ليس صفًّا في هذا الجدول.")
        if column not in self.columns:
            raise AssignmentError(f"«{column}» ليس عمودًا في هذا الجدول.")

    @property
    def table(self) -> dict[tuple[str, str], str]:
        """الخلايا مفهرسةً بإحداثيّها."""

        return {(row, column): value for row, column, value in self.cells}

    def value_at(self, row: str, column: str) -> str:
        """قيمةُ خليّةٍ؛ ويُرَدّ سؤالُ الممتنع بتسميته ممتنعًا لا بإرجاع فراغ."""

        self._check_coordinate(row, column)
        if (row, column) in set(self.forbidden):
            raise AssignmentError(f"({row}، {column}) ممتنعةٌ مُعلَنة، فلا قيمةَ لها.")
        return self.table[(row, column)]

    def signature_of(self, row: str) -> tuple[str | None, ...]:
        """توقيعُ صفٍّ عبر الأعمدة؛ والممتنعُ `None` لا فراغ."""

        if row not in self.rows:
            raise AssignmentError(f"«{row}» ليس صفًّا في هذا الجدول.")
        forbidden = set(self.forbidden)
        return tuple(
            None if (row, column) in forbidden else self.table[(row, column)]
            for column in self.columns
        )

    def indistinguishable_rows(self) -> tuple[tuple[str, ...], ...]:
        """زمرُ الصفوف التي لا يفرّق بينها الإسنادُ — خبرٌ عن النظام لا عيب."""

        groups: dict[tuple[str | None, ...], list[str]] = {}
        for row in self.rows:
            groups.setdefault(self.signature_of(row), []).append(row)
        return tuple(tuple(members) for members in groups.values() if len(members) > 1)

    def separating_columns(self, first: str, second: str) -> tuple[str, ...]:
        """الأعمدةُ التي يفترق فيها صفّان؛ وواحدٌ منها يعني أنّ الفرقَ عليه وحدَه."""

        left, right = self.signature_of(first), self.signature_of(second)
        return tuple(
            column
            for column, one, other in zip(self.columns, left, right, strict=True)
            if one != other
        )

    @property
    def distinct_values(self) -> tuple[str, ...]:
        """القيمُ المتمايزةُ في الجدول، مرتّبةً ترتيبًا ثابتًا."""

        return tuple(sorted({value for _, _, value in self.cells}))

    @property
    def filled(self) -> int:
        """عددُ الخلايا المملوءة."""

        return len(self.cells)

    @property
    def forbidden_count(self) -> int:
        """عددُ الخلايا الممتنعة المُعلَنة."""

        return len(self.forbidden)

    def covers_the_grid(self) -> bool:
        """المملوءُ زائدَ الممتنعِ يساوي الشبكةَ كلَّها — وهو شرطُ الإنشاء."""

        return self.filled + self.forbidden_count == len(self.rows) * len(self.columns)


AN_EMPTY_CELL_IS_A_HOLE_NOT_A_DEFAULT_NOTE: Final[str] = (
    "AnEmptyCellIsAHoleNotADefault: خليّةٌ غيرُ مذكورةٍ ليست «الشائع» ولا "
    "«كالأصل»، بل ثغرةٌ تُرَدّ؛ وما لا يقع يُعلَن ممتنعًا"
)

A_FORBIDDEN_CELL_IS_A_CLAIM_NOT_A_GAP_NOTE: Final[str] = (
    "AForbiddenCellIsAClaimNotAGap: إعلانُ الامتناع دعوًى قابلةٌ للنقض لا "
    "إعفاءٌ من الملء، فتُسمّى وتُفحَص كسائر الدعاوى"
)

A_TABLE_THAT_CANNOT_SEPARATE_TWO_ROWS_DOES_NOT_DISTINGUISH_THEM_NOTE: Final[str] = (
    "ATableThatCannotSeparateTwoRowsDoesNotDistinguishThem: صفّان بتوقيعٍ "
    "واحدٍ لا يميّزهما الإسنادُ مهما اختلف اسماهما، ويُخرَج ذلك صريحًا"
)

THE_SEPARATING_COLUMN_IS_NAMED_NOTE: Final[str] = (
    "TheSeparatingColumnIsNamed: حين يفترق صفّان في عمودٍ واحدٍ يُسمّى، فهو "
    "الموضعُ الذي يقوم عليه الفرقُ كلُّه وسقوطُه يُلغيه"
)

ASSIGNMENT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_EMPTY_CELL_IS_A_HOLE_NOT_A_DEFAULT_NOTE,
    A_FORBIDDEN_CELL_IS_A_CLAIM_NOT_A_GAP_NOTE,
    A_TABLE_THAT_CANNOT_SEPARATE_TWO_ROWS_DOES_NOT_DISTINGUISH_THEM_NOTE,
    THE_SEPARATING_COLUMN_IS_NAMED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
