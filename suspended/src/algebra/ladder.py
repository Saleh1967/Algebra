"""السُّلَّمُ مُشتَقٌّ لا مُختار: ارتفاعُه يُعدّ من الأبجديّة، واتّجاهُه من ذروتها.

**ما تفعله هذه الوحدة**: تأخذ **تجريدًا** — أصنافَ ذرّاتٍ لكلٍّ منها صورةٌ على
أبجديّةٍ صغرى، وصنفًا واحدًا مُعلَنًا حاملًا للذروة — فتشتقّ منه ثلاثةَ أشياء:
**ارتفاعَ السُّلَّم** (كم صنفًا صورتُه رمزٌ واحد)، و**اتّجاهَه** (أيُّ الرموز
أعلى)، و**الجردَ** الذي يلزم عنهما. وهي لا تعرف موضوعًا: أسماءٌ وصورٌ وأعداد.

`THE_HEIGHT_OF_A_LADDER_IS_COUNTED_NOT_CHOSEN`: `n` ليس معلَمًا يُضبَط. هو عددُ
الأصناف التي صورتُها **رمزٌ واحد**، أي التي تستطيع أن تقع في الذيل فتزيده رمزًا.
فيُقرَأ من الأبجديّة قراءةً، ويلزم منه الجردُ `2**n` لزومًا لا استقراءً.

`THE_DIRECTION_IS_THE_PEAKS_OWN_SYMBOL`: أعلى درجةٍ هي **الرمزُ الذي ينتهي
إليه الصنفُ الحامل**، أي رمزُ الذروة نفسِه. فالبروزُ = القربُ من الذروة، ولا
يُنفَق في الاتّجاه بتٌّ زائد. وهذا يصدق على درجتين، ولا يصدق على ثلاث.

`A_LADDER_OF_MORE_THAN_TWO_RUNGS_IS_NOT_ORDERED_BY_ITSELF`: بدرجتين يكفي
«رمزُ الذروة أوّلًا» لتعيين الترتيب تعيينًا تامًّا. وبثلاثٍ فأكثر تبقى
ترتيباتٌ كثيرة، فالترتيبُ **مصادرةٌ حقيقيّةٌ تُعلَن** أو يُرَدّ الحساب. ولا
يُخترَع ترتيبٌ صمتًا.

`A_CLASS_WITHOUT_AN_IMAGE_ADDS_NO_RUNG`: صنفٌ صورتُه خاليةٌ لا يرفع السُّلَّم
ولا يدخل الجرد. ووجودُه في الأبجديّة ليس وجودًا في البناء.

`ADDING_A_RUNG_DOUBLES_THE_INVENTORY`: وهذا هو الناقض. إن أُدخِل صنفٌ جديدٌ
صورتُه رمزٌ واحدٌ جديد، **وجب** أن يتضاعف الجرد. فمن قال بسُلَّمٍ ثمّ رأى
الجردَ ثابتًا مع درجةٍ زائدةٍ فقد نُقِض قولُه، لا قُيِّد.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Final

from .stipulation import chain_words

__all__ = [
    "ADDING_A_RUNG_DOUBLES_THE_INVENTORY_NOTE",
    "A_CLASS_WITHOUT_AN_IMAGE_ADDS_NO_RUNG_NOTE",
    "A_LADDER_OF_MORE_THAN_TWO_RUNGS_IS_NOT_ORDERED_BY_ITSELF_NOTE",
    "THE_DIRECTION_IS_THE_PEAKS_OWN_SYMBOL_NOTE",
    "THE_HEIGHT_OF_A_LADDER_IS_COUNTED_NOT_CHOSEN_NOTE",
    "Abstraction",
    "AtomClass",
    "LadderError",
    "LADDER_NAMED_RESIDUALS",
]


class LadderError(ValueError):
    """رُفض تجريدٌ لا يُشتَقّ منه سُلَّم؛ ولا يُكمَّل بترتيبٍ مُخترَع."""


@dataclass(frozen=True, slots=True)
class AtomClass:
    """صنفُ ذرّاتٍ: اسمُه، وصورتُه على الأبجديّة الصغرى، وكم ذرّةً يضمّ."""

    name: str
    image: str
    size: int = 1

    def __post_init__(self) -> None:
        if not self.name:
            raise LadderError("صنفٌ بلا اسمٍ لا يُحاسَب.")
        if self.size < 1:
            raise LadderError(f"صنف «{self.name}» يضمّ ذرّةً فأكثر.")


@dataclass(frozen=True, slots=True)
class Abstraction:
    """تجريدٌ كاملٌ: أصنافُ الذرّات، والصنفُ الحاملُ للذروة، وترتيبٌ إن لزم."""

    classes: tuple[AtomClass, ...]
    head: str
    declared_order: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.classes:
            raise LadderError("تجريدٌ بلا أصنافٍ ليس تجريدًا.")
        names = [atom.name for atom in self.classes]
        if len(set(names)) != len(names):
            raise LadderError("أصنافُ الذرّات تُسمّى أسماءً مميَّزة.")
        if self.head not in names:
            raise LadderError(f"الصنفُ الحاملُ «{self.head}» ليس في الأصناف.")
        if len(self.head_image) < 2:
            raise LadderError(
                "الصنفُ الحاملُ صورتُه رمزان فأكثر: صدرٌ ثمّ ذروة؛ "
                "وصنفٌ برمزٍ واحدٍ درجةٌ لا ذروة."
            )
        rung_symbols = [atom.image for atom in self.rungs]
        if len(set(rung_symbols)) != len(rung_symbols):
            raise LadderError("درجتان بصورةٍ واحدةٍ ليستا درجتين.")
        if self.declared_order and set(self.declared_order) != set(rung_symbols):
            raise LadderError("الترتيبُ المُعلَنُ يذكر درجاتِ السُّلَّم كلَّها ولا يزيد.")

    @property
    def atom_count(self) -> int:
        """عددُ الذرّات كلِّها، مجموعَ أحجام الأصناف."""

        return sum(atom.size for atom in self.classes)

    def class_named(self, name: str) -> AtomClass:
        """صنفٌ باسمه؛ ويُرَدّ ما ليس فيها."""

        for atom in self.classes:
            if atom.name == name:
                return atom
        raise LadderError(f"لا صنفَ باسم «{name}».")

    @property
    def head_image(self) -> str:
        """صورةُ الصنف الحامل: صدرٌ ثمّ ذروة."""

        return self.class_named(self.head).image

    @property
    def peak_symbol(self) -> str:
        """رمزُ الذروة: آخِرُ ما ينتهي إليه الصنفُ الحامل."""

        return self.head_image[-1]

    @property
    def rungs(self) -> tuple[AtomClass, ...]:
        """درجاتُ السُّلَّم: الأصنافُ التي صورتُها رمزٌ واحد، لا غير."""

        return tuple(atom for atom in self.classes if len(atom.image) == 1)

    @property
    def height(self) -> int:
        """ارتفاعُ السُّلَّم، معدودًا لا مختارًا."""

        return len(self.rungs)

    @property
    def imageless(self) -> tuple[AtomClass, ...]:
        """أصنافٌ صورتُها خالية: في الأبجديّة ولا أثرَ لها في البناء."""

        return tuple(atom for atom in self.classes if not atom.image)

    def ladder(self) -> tuple[str, ...]:
        """رموزُ الدرجات من الأعلى إلى الأدنى؛ وتُشتَقّ عند درجتين لا أكثر."""

        symbols = tuple(atom.image for atom in self.rungs)
        if self.declared_order:
            return self.declared_order
        if self.height > 2:
            raise LadderError(
                f"سُلَّمٌ بـ{self.height} درجاتٍ لا يرتّب نفسَه؛ "
                "فالترتيبُ مصادرةٌ تُعلَن (A_LADDER_OF_MORE_THAN_TWO_RUNGS)."
            )
        if self.peak_symbol not in symbols:
            raise LadderError(
                "رمزُ الذروة ليس درجةً، فلا يُشتَقّ الاتّجاهُ من القرب منها؛ "
                "ويُعلَن الترتيبُ صراحةً."
            )
        return (
            self.peak_symbol,
            *(s for s in sorted(symbols) if s != self.peak_symbol),
        )

    def tails(self) -> frozenset[str]:
        """ذيولُ المقطع: المتتالياتُ الهابطةُ تمامًا على السُّلَّم."""

        return chain_words(self.ladder())

    def inventory(self) -> frozenset[str]:
        """الجردُ: صورةُ الصنف الحامل موصولةً بكلّ ذيل."""

        return frozenset(self.head_image + tail for tail in self.tails())

    @property
    def predicted_size(self) -> int:
        """`2**n` — ما يلزم عن الارتفاع وحدَه، قبل النظر في الجرد."""

        return int(2**self.height)

    def with_extra_rung(
        self, name: str, symbol: str, size: int = 1, position: int | None = None
    ) -> Abstraction:
        """أضِف درجةً جديدةً، ليُرى أيتضاعف الجردُ كما يلزم — أم يُنقَض القول.

        و`position` موضعُها في السُّلَّم، وهو **مُعلَنٌ لا مُشتَقّ**: سُلَّمٌ
        بثلاث درجاتٍ لا يرتّب نفسَه، فلا يُخترَع له موضعٌ صمتًا. وتخلّفُه
        يضعها في الأسفل، وذلك اصطلاحٌ مذكورٌ لا استنباط. والمُدَّعى لا يتعلّق
        بالموضع أصلًا: العددُ `2**n` في المواضع كلِّها.
        """

        if len(symbol) != 1:
            raise LadderError("الدرجةُ صورتُها رمزٌ واحد.")
        if symbol in {atom.image for atom in self.rungs}:
            raise LadderError(f"الرمزُ «{symbol}» درجةٌ قائمةٌ فليس جديدًا.")
        current = list(self.ladder()) if self.height >= 2 else []
        where = len(current) if position is None else position
        if not 0 <= where <= len(current):
            raise LadderError("موضعُ الدرجة داخلَ السُّلَّم أو عند أحد طرفيه.")
        current.insert(where, symbol)
        return replace(
            self,
            classes=(*self.classes, AtomClass(name=name, image=symbol, size=size)),
            declared_order=tuple(current),
        )


THE_HEIGHT_OF_A_LADDER_IS_COUNTED_NOT_CHOSEN_NOTE: Final[str] = (
    "TheHeightOfALadderIsCountedNotChosen: n عددُ الأصناف التي صورتُها رمزٌ "
    "واحد، يُقرَأ من الأبجديّة لا يُضبَط؛ ويلزم عنه الجردُ 2**n لزومًا"
)

THE_DIRECTION_IS_THE_PEAKS_OWN_SYMBOL_NOTE: Final[str] = (
    "TheDirectionIsThePeaksOwnSymbol: أعلى درجةٍ هي رمزُ الذروة نفسِه، فالبروزُ "
    "قربٌ منها ولا يُنفَق في الاتّجاه بتٌّ زائد — بدرجتين لا بثلاث"
)

A_LADDER_OF_MORE_THAN_TWO_RUNGS_IS_NOT_ORDERED_BY_ITSELF_NOTE: Final[str] = (
    "ALadderOfMoreThanTwoRungsIsNotOrderedByItself: بثلاث درجاتٍ فأكثر يبقى "
    "الترتيبُ مصادرةً تُعلَن، ولا يُخترَع صمتًا"
)

A_CLASS_WITHOUT_AN_IMAGE_ADDS_NO_RUNG_NOTE: Final[str] = (
    "AClassWithoutAnImageAddsNoRung: صنفٌ صورتُه خاليةٌ لا يرفع السُّلَّم ولا "
    "يدخل الجرد؛ ووجودُه في الأبجديّة ليس وجودًا في البناء"
)

ADDING_A_RUNG_DOUBLES_THE_INVENTORY_NOTE: Final[str] = (
    "AddingARungDoublesTheInventory: درجةٌ زائدةٌ توجب جردًا مضاعفًا؛ فمن رأى "
    "الجردَ ثابتًا معها فقد نُقِض قولُه لا قُيِّد"
)

LADDER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_HEIGHT_OF_A_LADDER_IS_COUNTED_NOT_CHOSEN_NOTE,
    THE_DIRECTION_IS_THE_PEAKS_OWN_SYMBOL_NOTE,
    A_LADDER_OF_MORE_THAN_TWO_RUNGS_IS_NOT_ORDERED_BY_ITSELF_NOTE,
    A_CLASS_WITHOUT_AN_IMAGE_ADDS_NO_RUNG_NOTE,
    ADDING_A_RUNG_DOUBLES_THE_INVENTORY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
