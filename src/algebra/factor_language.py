"""لغاتُ العوامل الممنوعة: الكلماتُ المسموحة، وانغلاقُ البادئة، والتراي.

**ما تفعله هذه الوحدة**: تأخذ أبجديّةً ومجموعةَ **عواملَ ممنوعة**، فتُخرِج
الكلماتِ التي تتجنّبها **بالتعداد**، وتفحص أهي منتهيةٌ ومنغلقةٌ على البادئة،
وتبني منها الشجرةَ (التراي) وتعدّ حوافَّها.

`A_TREE_IS_A_THEOREM_NOT_A_DRAWING`: كلُّ مجموعةٍ منتهيةٍ **منغلقةٍ على
البادئة** تقابل شجرةً مجذّرةً واحدةً: عُقَدُها الكلماتُ نفسُها، وأبو كلّ كلمةٍ
غيرِ خالية هو الكلمةُ بلا حرفها الأخير. فعددُ الحوافّ `|S| − 1` بالضرورة، ولا
اختيارَ في الشكل. وهذا يُفحَص ههنا بالبناء: يُطلَب أبو كلّ عقدةٍ فيوجد، وتُعَدّ
الحوافُّ فتوافق.

`FINITENESS_IS_PROVED_BY_A_BOUND_NOT_ASSUMED`: لغةُ العوامل الممنوعة قد تكون
لانهائيّة. وهي منتهيةٌ **إذا وفقط إذا** خلا مخطَّطُ الانتقالات المسموحة من دورة؛
وعندئذٍ طولُ أطول كلمةٍ محدودٌ بعدد الحروف. فالوحدةُ تفحص خلوَّ المخطَّط من
الدورات قبل التعداد، وترفض التعدادَ على لغةٍ لانهائيّة بدل أن تدور إلى ما لا
نهاية.

`PREFIX_CLOSURE_IS_CHECKED_NOT_ASSERTED`: انغلاقُ البادئة لازمٌ للشجرة، وهو
**نتيجةٌ** لكون المنعِ بالعوامل: حذفُ حرفٍ من الطرف لا يُنشِئ عاملًا لم يكن.
ومع ذلك يُفحَص بالتعداد، فالنتيجةُ المبرهَنةُ تُفحَص ولا تُؤخَذ.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE`: الحروفُ ههنا رموزٌ مجرّدة. وإن
سُمّيت `V` و`C` في استعمالٍ ما، فتلك تسميةُ المستعمِل وشرطُها يُكتَب عنده.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Final

__all__ = [
    "A_TREE_IS_A_THEOREM_NOT_A_DRAWING_NOTE",
    "FACTOR_LANGUAGE_NAMED_RESIDUALS",
    "FINITENESS_IS_PROVED_BY_A_BOUND_NOT_ASSUMED_NOTE",
    "PREFIX_CLOSURE_IS_CHECKED_NOT_ASSERTED_NOTE",
    "FactorLanguage",
    "FactorLanguageError",
    "Trie",
    "avoids",
    "is_prefix_closed",
]


class FactorLanguageError(ValueError):
    """رُفض مدخلٌ أو لغةٌ لانهائيّة؛ ولا يُقرَّب ولا يُدار إلى ما لا نهاية."""


def avoids(word: str, forbidden: frozenset[str]) -> bool:
    """أتتجنّب الكلمةُ كلَّ العوامل الممنوعة؟ والعاملُ متتاليةٌ متّصلة."""

    return not any(factor in word for factor in forbidden)


def is_prefix_closed(words: frozenset[str]) -> bool:
    """أكلُّ بادئةٍ لكلمةٍ في المجموعة داخلةٌ فيها؟ شرطُ وجود الشجرة."""

    return all(word[:length] in words for word in words for length in range(len(word)))


@dataclass(frozen=True, slots=True)
class Trie:
    """شجرةُ بادئاتٍ مبنيّةٌ من مجموعةٍ منغلقةٍ على البادئة، لا مرسومةٌ بيد."""

    words: frozenset[str]

    def __post_init__(self) -> None:
        if "" not in self.words:
            raise FactorLanguageError("لا شجرةَ بلا جذر: الكلمةُ الخاليةُ عقدتُه.")
        if not is_prefix_closed(self.words):
            raise FactorLanguageError(
                "المجموعةُ غيرُ منغلقةٍ على البادئة، فلا تقابل شجرةً؛ "
                "ولا تُكمَّل صمتًا ببادئاتٍ لم تُذكَر."
            )

    @property
    def nodes(self) -> int:
        """عُقَدُ الشجرة: الكلماتُ نفسُها."""

        return len(self.words)

    @property
    def edges(self) -> tuple[tuple[str, str], ...]:
        """حوافُّها مُشتَقّةً: لكلّ كلمةٍ غيرِ خاليةٍ حافّةٌ من أبيها إليها."""

        return tuple(sorted((word[:-1], word) for word in self.words if word))

    @property
    def depth(self) -> int:
        """أعمقُ عقدةٍ في الشجرة."""

        return max(len(word) for word in self.words)

    def children_of(self, word: str) -> tuple[str, ...]:
        """أولادُ عقدةٍ ما، مرتّبين ترتيبًا ثابتًا."""

        if word not in self.words:
            raise FactorLanguageError(f"«{word}» ليست عقدةً في هذه الشجرة.")
        return tuple(
            sorted(
                other
                for other in self.words
                if len(other) == len(word) + 1 and other.startswith(word)
            )
        )

    def edge_count_matches_node_count(self) -> bool:
        """`|E| = |V| − 1`: خاصّةُ الشجرة، مفحوصةً لا مفترَضة."""

        return len(self.edges) == self.nodes - 1


@dataclass(frozen=True, slots=True)
class FactorLanguage:
    """لغةُ عواملَ ممنوعة: أبجديّتُها، وممنوعاتُها، وما يُشتَقّ منهما."""

    alphabet: tuple[str, ...]
    forbidden: frozenset[str]

    def __post_init__(self) -> None:
        if not self.alphabet:
            raise FactorLanguageError("أبجديّةٌ خاليةٌ لا لغةَ لها.")
        if len(set(self.alphabet)) != len(self.alphabet):
            raise FactorLanguageError("حرفٌ مكرَّرٌ في الأبجديّة.")
        if any(not factor for factor in self.forbidden):
            raise FactorLanguageError("العاملُ الخالي ممنوعٌ منعَ كلِّ شيء.")
        for factor in self.forbidden:
            for letter in factor:
                if letter not in self.alphabet:
                    raise FactorLanguageError(
                        f"العاملُ «{factor}» فيه حرفٌ خارج الأبجديّة: «{letter}»."
                    )

    def allowed_transitions(self) -> tuple[tuple[str, str], ...]:
        """الانتقالاتُ المسموحةُ بين حرفين، مُشتَقّةً من الممنوعات."""

        return tuple(
            (first, second)
            for first, second in product(self.alphabet, repeat=2)
            if first + second not in self.forbidden
        )

    def transition_graph_is_acyclic(self) -> bool:
        """أخلا مخطَّطُ الانتقالات من دورة؟ وهو شرطُ انتهاء اللغة."""

        edges = {
            first: {
                second for start, second in self.allowed_transitions() if start == first
            }
            for first in self.alphabet
        }
        colour: dict[str, int] = {}

        def visit(node: str) -> bool:
            colour[node] = 1
            for nxt in sorted(edges[node]):
                if colour.get(nxt) == 1:
                    return False
                if colour.get(nxt) is None and not visit(nxt):
                    return False
            colour[node] = 2
            return True

        return all(
            colour.get(letter) is not None or visit(letter) for letter in self.alphabet
        )

    def words(self) -> frozenset[str]:
        """كلماتُ اللغة كلُّها بالتعداد؛ ويُرفَض التعدادُ على لغةٍ لانهائيّة.

        والحدُّ مُشتَقٌّ: إن خلا المخطَّطُ من الدورات فلا يتكرّر حرفٌ في مسارٍ
        موجَّه، فطولُ أطول كلمةٍ لا يتجاوز عددَ الحروف.
        """

        if not self.transition_graph_is_acyclic():
            raise FactorLanguageError(
                "مخطَّطُ الانتقالات فيه دورة، فاللغةُ لانهائيّة؛ ولا تُعَدّ " "بالتعداد الشامل."
            )
        bound = len(self.alphabet)
        found = {""}
        for length in range(1, bound + 1):
            for letters in product(self.alphabet, repeat=length):
                word = "".join(letters)
                if avoids(word, self.forbidden):
                    found.add(word)
        return frozenset(found)

    def trie(self) -> Trie:
        """شجرةُ البادئات المبنيّةُ من كلمات اللغة."""

        return Trie(words=self.words())


A_TREE_IS_A_THEOREM_NOT_A_DRAWING_NOTE: Final[str] = (
    "ATreeIsATheoremNotADrawing: مجموعةٌ منتهيةٌ منغلقةٌ على البادئة تقابل شجرةً "
    "واحدةً، عُقَدُها كلماتُها وأبوها حذفُ الحرف الأخير؛ فعددُ الحوافّ |S|−1 "
    "بالضرورة ولا اختيارَ في الشكل"
)

FINITENESS_IS_PROVED_BY_A_BOUND_NOT_ASSUMED_NOTE: Final[str] = (
    "FinitenessIsProvedByABoundNotAssumed: اللغةُ منتهيةٌ إذا خلا مخطَّطُ "
    "الانتقالات من دورة، وعندئذٍ الطولُ محدودٌ بعدد الحروف؛ فيُفحَص الخلوُّ قبل "
    "التعداد ويُرفَض التعدادُ على لانهائيّة"
)

PREFIX_CLOSURE_IS_CHECKED_NOT_ASSERTED_NOTE: Final[str] = (
    "PrefixClosureIsCheckedNotAsserted: انغلاقُ البادئة نتيجةٌ لكون المنع "
    "بالعوامل، إذ لا يُنشِئ الحذفُ من الطرف عاملًا جديدًا؛ ومع ذلك يُفحَص "
    "بالتعداد فلا يُؤخَذ مبرهَنًا بلا فحص"
)

FACTOR_LANGUAGE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_TREE_IS_A_THEOREM_NOT_A_DRAWING_NOTE,
    FINITENESS_IS_PROVED_BY_A_BOUND_NOT_ASSUMED_NOTE,
    PREFIX_CLOSURE_IS_CHECKED_NOT_ASSERTED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
