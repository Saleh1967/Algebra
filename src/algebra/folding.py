"""الطيُّ والفكُّ — **تقابلٌ مبرهَن**، لا إنتروبيا ولا تقدير.

**ما ليس ههنا**: لا `H` ولا ثمنٌ محجوزٌ ولا نصيبٌ مقيس. **فتلك قياساتٌ لا
تُطوى**: لا يُستَرجَع سطرٌ واحدٌ من `H = 2.6283`.

**وما ههنا**: دالّتان `fold` و`unfold` بينهما **تقابلٌ مبرهَنٌ**، وعدٌّ
صحيحٌ تامٌّ، وبرهانٌ بالاستقراء. والعائمُ **لا يدخل شيئًا منه**.

════════════════════════════════════════════════════════════════════

## المسألة

أبجديّةٌ `Σ = F ⊎ B` فيها `f = |F|` رمزًا **حرًّا** و`b = |B|` رمزًا
**محجورًا**. وكلمةٌ `w ∈ Σⁿ` تُسمّى **جائزةً** إن لم يقع محجوران
متجاوران. (وعند `f = 3, b = 1` هذا حارسُ «لا ساكنَ بعد ساكن».)

## المبرهنة ١ — العدُّ

ليكن `A(n)` عددَ الجائزات الطولِ `n` المنتهيةِ بحرٍّ، و`B(n)` المنتهيةِ
بمحجور، و`T(n) = A(n) + B(n)`. فـ:

    A(1) = f ،  B(1) = b
    A(n) = f·(A(n−1) + B(n−1))          [الحرُّ يتبع أيَّ شيء]
    B(n) = b·A(n−1)                      [المحجورُ يتبع الحرَّ وحدَه]

**فيلزم**: `T(n) = f·T(n−1) + f·b·T(n−2)` لكلّ `n ≥ 2`، مع
`T(0) = 1` و`T(1) = f + b`.

**البرهان.** `T(n) = A(n) + B(n) = f·(A(n−1)+B(n−1)) + b·A(n−1)
= f·T(n−1) + b·A(n−1)`. وبالتعريف `A(n−1) = f·(A(n−2)+B(n−2))
= f·T(n−2)`. فبالتعويض `T(n) = f·T(n−1) + f·b·T(n−2)`. ∎

**والتحقّقُ عند `n = 2`**: `T(2) = f(f+b) + fb = f² + 2fb`، وهو عددُ
`Σ²` ناقصَ ما فيه محجوران: `(f+b)² − b² = f² + 2fb`. ✓

## المبرهنة ٢ — معدَّلُ النموّ

جذرُ `x² = f·x + f·b` الأكبرُ `ρ = (f + √(f² + 4fb)) / 2`، و
`T(n) / T(n−1) → ρ`. **وعند `f = 3, b = 1` يكون `ρ = (3 + √21)/2`**،
و`log₂ ρ = 1.9227…`.

**فما كان يُسمّى «سعةَ الطبقة» صار مبرهنةً عن تقابلٍ**، لا مقدارًا
مُشتَقًّا من نموٍّ مزعوم. والفرقُ أنّ الطولَ `⌈log₂ T(n)⌉` **بتّةً
يُطوى بها ويُفَكّ**، لا حدًّا أعلى يُقارَب.

## المبرهنة ٣ — التقابل (وهو المقصود)

رتِّب `Σ` ترتيبًا ثابتًا. وليكن `S(m, True)` عددَ الجائزات الطولِ `m`
التي **يجوز أن يبدأها محجور**، و`S(m, False)` التي **لا يجوز**:

    S(0, ·)     = 1
    S(m, True)  = f·S(m−1, True) + b·S(m−1, False)
    S(m, False) = f·S(m−1, True)

فـ`T(n) = S(n, True)`. وتُعرَّف

    fold(w) = Σᵢ  Σ_{c < wᵢ ، c جائزٌ في الموضع i}  S(n−i−1, بعدَ c)

**فـ`fold` تقابلٌ من الجائزات الطولِ `n` إلى `{0, …, T(n)−1}`، ورتيبةٌ
بالترتيب المُعجَميّ.**

**البرهان** بالاستقراء على `n`. عند `n = 0` الجائزةُ واحدةٌ وصورتُها
`0 = T(0)−1`. وليَصحّ عند كلّ ما دون `n`. الرموزُ الجائزةُ في الموضع
الأوّل تقسم الجائزاتِ الطولِ `n` أقسامًا متباينةً، وحجمُ قسمِ `c` هو
`S(n−1, بعدَ c)`، **ومجموعُها `S(n, True) = T(n)` بالتعريف**. وتُرتَّب
الأقسامُ بترتيب `c`، فبادئةُ `fold` تُعيِّن القسمَ، وبقيّتُها — بفرض
الاستقراء — تقابلٌ داخلَ القسم. فالمجموعُ تقابلٌ على `{0,…,T(n)−1}`
ورتيبٌ. ∎

**ويلزم عنه أنّ `unfold` معرَّفةٌ ووحيدة**: تُطرَح أحجامُ الأقسام
بترتيبها حتّى يصغر الباقي عن حجمِ القسم، فيُعيَّن `c` ثمّ يُنزَل. ولأنّ
`fold` تقابلٌ فـ`unfold(fold(w)) = w` لكلّ `w` جائزة،
و`fold(unfold(k)) = k` لكلّ `k < T(n)`. ∎

## المبرهنة ٤ — الطيُّ بلا طولٍ يُمرَّر من خارج

**وعطلٌ في المبرهنة ٣ يُقال**: `fold` تقابلٌ **على الجائزات الطولِ `n`
وحدَه**، و`unfold` **تطلب `n`**. فمن طوى كلمةً ثمّ فكَّها **بطولٍ يعرفه
من خارج** فقد استرجع **بدليلٍ وطول**، لا بدليلٍ وحدَه. **وذلك ليس طيًّا
تامًّا للكلمة** — والطولُ معلومةٌ لم تُحسَب في الثمن.

**والإصلاحُ مبرهَن**. ليكن `off(n) = Σ_{m<n} T(m)`. فالمُعرَّف

    foldany(w) = off(|w|) + fold(w)

**تقابلٌ من الجائزات على كلّ الأطوال إلى `ℕ` كلِّها.**

**البرهان.** الفتراتُ `[off(n), off(n+1))` لكلّ `n ≥ 0` **تقسم `ℕ`**:
متتاليةٌ متلاصقةٌ متباينةٌ، وسعةُ كلٍّ `T(n)`، ومجموعُها يتباعد لأنّ
`T(n) ≥ 1`. وبالمبرهنة ٣ فـ`fold` تقابلٌ من جائزات الطولِ `n` على
`{0,…,T(n)−1}`، فـ`off(n) + fold(·)` تقابلٌ عليها على الفترةِ `n`. فاجتماعُ
تقابلاتٍ على أقسامٍ تقسم `ℕ` تقابلٌ على `ℕ`. ∎

**ويلزم أنّ `unfoldany` معرَّفةٌ بلا طول**: يُبحَث `n` الذي
`off(n) ≤ k < off(n+1)` — وهو وحيدٌ لأنّ الفتراتَ تقسم — ثمّ
`unfold(k − off(n), n)`. ∎

**فهذا هو الطيُّ الذي لا يستعير شيئًا من خارجه.**

## المبرهنة ٥ — الصعودُ يتركّب

وإذ صار كلُّ لفظٍ **عددًا واحدًا** في `{0,…,A(L)−1}` حيث
`A(L) = Σ_{n≤L} T(n)` و`L` أطولُ لفظ، **فمتتاليةُ الألفاظ كلمةٌ على
أبجديّةٍ سعتُها `A(L)` بلا حارس**. فتُطوى بالمبرهنة ٤ نفسِها عند
`f = A(L)` و`b = 0`. **فالتقابلُ يتركّب على نفسه**، والسطرُ يصير عددًا
واحدًا، **ويُفَكّ فيرجع ألفاظًا ثمّ حالاتٍ**. ∎

**ولا يُستعار طولٌ في مستوًى من المستويات** — وذلك المقصود.

════════════════════════════════════════════════════════════════════

`NO_FLOAT_ENTERS_THE_FOLD`: كلُّ ما في الطيّ والفكّ **أعدادٌ صحيحةٌ
تامّة**. والعائمُ لا يدخل إلّا في `growth_root` — وهو **وصفٌ للمعدَّل لا
جزءٌ من التقابل** — ويُستغنى عنه بـ`ratio_gap` بالكسور الصحيحة.

`AND_THE_VERIFICATION_IS_EXHAUSTIVE_NOT_SAMPLED`: ويُفحَص التقابلُ
**على كلّ الجائزات** حتّى طولٍ مُعلَن، لا على عيّنة — فما بُرهِن يُرى
مُستوفًى. وذلك في `tests/algebra/test_folding.py`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from typing import Final

__all__ = [
    "FoldingError",
    "Guarded",
    "admissible_count",
    "completions",
    "fold",
    "fold_any",
    "growth_root",
    "offset",
    "ratio_gap",
    "unfold",
    "unfold_any",
]

THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE: Final[str] = (
    "الحرُّ والمحجورُ صنفان في أبجديّةٍ مجرَّدة، ولا يُسمّى أحدُهما حركةً "
    "ولا سكونًا ههنا. والحارسُ قيدٌ على المتجاورات، لا حكمٌ على لغة."
)


class FoldingError(ValueError):
    """رُدَّ طيٌّ أو فكٌّ خارجَ مجاله — والخروجُ يُسمّى ولا يُصحَّح صمتًا."""


@dataclass(frozen=True, slots=True)
class Guarded:
    """أبجديّةٌ محروسة: `f` حرًّا و`b` محجورًا، ولا محجوران متجاوران.

    والترتيبُ المُعتمَد: الأحرارُ `0 … f−1` ثمّ المحجورون `f … f+b−1`.
    """

    free: int
    blocked: int

    def __post_init__(self) -> None:
        if self.free < 1:
            raise FoldingError("أبجديّةٌ بلا حرٍّ واحد — فلا كلمةَ جائزة.")
        if self.blocked < 0:
            raise FoldingError("عددُ المحجورين سالب.")

    @property
    def size(self) -> int:
        return self.free + self.blocked

    def is_free(self, symbol: int) -> bool:
        if not 0 <= symbol < self.size:
            raise FoldingError(f"رمزٌ خارجَ الأبجديّة: {symbol}")
        return symbol < self.free

    def admits(self, symbol: int, after_blocked: bool) -> bool:
        """أيجوز `symbol` بعد موضعٍ محجورٍ أو حرّ؟"""

        return self.is_free(symbol) if after_blocked else True


@cache
def completions(shape: Guarded, length: int, open_start: bool) -> int:
    """`S(m, …)` — عددُ الجائزات الطولِ `length`، صحيحًا تامًّا.

    و`open_start` أنّ الموضعَ الأوّلَ **يجوز أن يكون محجورًا** (أي أنّ ما
    قبله حرٌّ أو أنّه البدء).
    """

    if length < 0:
        raise FoldingError(f"طولٌ سالب: {length}")
    if length == 0:
        return 1
    free = shape.free * completions(shape, length - 1, True)
    if not open_start:
        return free
    return free + shape.blocked * completions(shape, length - 1, False)


def admissible_count(shape: Guarded, length: int) -> int:
    """`T(n)` — عددُ الجائزات الطولِ `n`، صحيحًا تامًّا."""

    return completions(shape, length, True)


def fold(shape: Guarded, word: tuple[int, ...]) -> int:
    """الطيُّ: كلمةٌ جائزةٌ ← دليلٌ في `{0, …, T(n)−1}`.

    ويُردّ ما ليس جائزًا **بموضعه**، فلا يُطوى ما لا يُفَكّ.
    """

    length = len(word)
    index = 0
    after_blocked = False
    for place, symbol in enumerate(word):
        if not shape.admits(symbol, after_blocked):
            raise FoldingError(f"محجورٌ بعد محجورٍ في الموضع {place}")
        rest = length - place - 1
        # **والمجموعُ مُغلَقٌ لا حلقة**: الأحرارُ دون `symbol` عددُهم
        # `min(symbol, f)` ولكلٍّ `S(rest, True)`؛ والمحجورون دونه
        # `max(symbol − f, 0)` ولكلٍّ `S(rest, False)` — **وإن جاز**.
        # وذلك مطابقٌ للحلقة حرفًا، ومفحوصٌ بالعدّ المباشر في
        # `tests/algebra/test_folding.py`؛ **ولولاه لكان الطيُّ
        # `O(حجم الأبجديّة)`** فيتعذّر على أبجديّةٍ كبيرة.
        index += min(symbol, shape.free) * completions(shape, rest, True)
        if not after_blocked and symbol > shape.free:
            index += (symbol - shape.free) * completions(shape, rest, False)
        after_blocked = not shape.is_free(symbol)
    return index


def unfold(shape: Guarded, index: int, length: int) -> tuple[int, ...]:
    """الفكُّ: دليلٌ ← الكلمةُ الجائزةُ بعينها. وهو معكوسُ `fold` تمامًا."""

    if length < 0:
        raise FoldingError(f"طولٌ سالب: {length}")
    whole = admissible_count(shape, length)
    if not 0 <= index < whole:
        raise FoldingError(f"دليلٌ خارجَ المدى: {index} من {whole}")
    left = index
    after_blocked = False
    built: list[int] = []
    for _place in range(length):
        rest = length - len(built) - 1
        free_each = completions(shape, rest, True)
        free_block = shape.free * free_each
        if left < free_block:
            symbol = left // free_each
            left -= symbol * free_each
        else:
            if after_blocked:  # pragma: no cover - يمنعه التقابل المبرهَن
                raise FoldingError("باقٍ فوق كتلةِ الأحرار بعد محجور")
            left -= free_block
            blocked_each = completions(shape, rest, False)
            symbol = shape.free + left // blocked_each
            left -= (symbol - shape.free) * blocked_each
        built.append(symbol)
        after_blocked = not shape.is_free(symbol)
    return tuple(built)


@cache
def offset(shape: Guarded, length: int) -> int:
    """`off(n) = Σ_{m<n} T(m)` — بدايةُ فترةِ الطولِ `n` في `ℕ`."""

    if length < 0:
        raise FoldingError(f"طولٌ سالب: {length}")
    if length == 0:
        return 0
    return offset(shape, length - 1) + admissible_count(shape, length - 1)


def fold_any(shape: Guarded, word: tuple[int, ...]) -> int:
    """الطيُّ بلا طول: كلمةٌ جائزةٌ **أيَّ طولٍ كانت** ← عددٌ في `ℕ`.

    وهو تقابلٌ على `ℕ` كلِّها (المبرهنة ٤)، **فلا يُمرَّر طولٌ في الفكّ**.
    """

    return offset(shape, len(word)) + fold(shape, word)


def unfold_any(shape: Guarded, index: int) -> tuple[int, ...]:
    """الفكُّ بلا طول: عددٌ ← الكلمةُ بعينها، **وطولُها من العدد نفسِه**."""

    if index < 0:
        raise FoldingError(f"دليلٌ سالب: {index}")
    length = 0
    left = index
    while True:
        here = admissible_count(shape, length)
        if left < here:
            return unfold(shape, left, length)
        left -= here
        length += 1


def bits_exactly(shape: Guarded, length: int) -> int:
    """`⌈log₂ T(n)⌉` بالأعداد الصحيحة وحدَها — لا لوغاريتمَ عائمًا."""

    whole = admissible_count(shape, length)
    if whole <= 1:
        return 0
    return (whole - 1).bit_length()


def ratio_gap(shape: Guarded, length: int) -> Fraction:
    """`r² − f·r − f·b` عند `r = T(n)/T(n−1)` — بكسورٍ صحيحةٍ تامّة.

    وهو **صفرٌ في الحدّ**، وقربُه من الصفر يُقاس بلا عائم. فبهذا يُقال
    «المعدَّلُ يبلغ `ρ`» **دون أن يُستعمَل جذرٌ أصمّ في برهان**.
    """

    if length < 1:
        raise FoldingError("النسبةُ تحتاج طولًا لا يقلّ عن واحد.")
    ratio = Fraction(
        admissible_count(shape, length), admissible_count(shape, length - 1)
    )
    return ratio * ratio - shape.free * ratio - shape.free * shape.blocked


def growth_root(shape: Guarded) -> float:
    """`ρ = (f + √(f² + 4fb)) / 2` — **وصفٌ للمعدَّل لا جزءٌ من التقابل**.

    ولا يدخل هذا العائمُ طيًّا ولا فكًّا؛ ومن أراد بلا عائمٍ فـ`ratio_gap`.
    """

    discriminant = shape.free * shape.free + 4 * shape.free * shape.blocked
    return (shape.free + math.sqrt(discriminant)) / 2


def recurrence_holds(shape: Guarded, upto: int) -> bool:
    """`T(n) = f·T(n−1) + f·b·T(n−2)` مفحوصةً بالأعداد الصحيحة إلى `upto`."""

    for length in range(2, upto + 1):
        expected = shape.free * admissible_count(shape, length - 1) + (
            shape.free * shape.blocked * admissible_count(shape, length - 2)
        )
        if admissible_count(shape, length) != expected:
            return False
    return True
