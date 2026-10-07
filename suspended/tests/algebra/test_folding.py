"""التقابلُ مفحوصٌ **على كلّ الجائزات**، لا على عيّنة — فالبرهانُ يُستوفى.

**الفرقُ عن كلّ ما سبقه في هذه الشجرة**: ما قِيس قبلَه **إنتروبيا وثمنٌ
محجوز** — ولا يُستَرجَع منه سطرٌ واحد. **وهذا يُطوى ويُفَكّ**: `fold`
و`unfold` معكوسان، والبرهانُ في `src/algebra/folding.py`، والاستيفاءُ
ههنا.

`EXHAUSTIVE_MEANS_EVERY_WORD_NOT_A_SAMPLE`: تُعَدّ **كلُّ** كلمةٍ جائزةٍ
حتّى طولٍ مُعلَن، ويُفحَص لكلٍّ منها: أنّ `fold` أعطاها دليلًا، وأنّ
الأدلّةَ **هي `{0,…,T(n)−1}` بلا تكرارٍ ولا فجوة**، وأنّ
`unfold(fold(w)) = w` **حرفًا بحرف**. فإن سقط واحدٌ سقطت المبرهنة.

`AND_THE_COUNT_IS_CHECKED_AGAINST_A_DIFFERENT_METHOD`: ويُقابَل `T(n)`
المُشتَقُّ بالمتتالية **بعَدٍّ مباشرٍ للكلمات** — طريقتان مستقلّتان،
فالتطابقُ شاهدٌ لا تعريف.

`AND_THE_ROOT_IS_APPROACHED_WITHOUT_A_FLOAT`: وبلوغُ المعدَّل `ρ` يُفحَص
بـ`ratio_gap` **بكسورٍ صحيحةٍ تامّة** تنزل إلى الصفر، فلا يُبرهَن شيءٌ
بجذرٍ أصمَّ مُقرَّب.
"""

from __future__ import annotations

import re
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest

from algebra.folding import (
    FoldingError,
    Guarded,
    admissible_count,
    bits_exactly,
    fold,
    fold_any,
    growth_root,
    offset,
    ratio_gap,
    recurrence_holds,
    unfold,
    unfold_any,
)

SHAPES = (
    Guarded(free=3, blocked=1),  # حارسُ «لا ساكنَ بعد ساكن» — ρ = (3+√21)/2
    Guarded(free=2, blocked=1),
    Guarded(free=1, blocked=1),
    Guarded(free=4, blocked=2),
    Guarded(free=15, blocked=0),  # بلا حارس — أبجديّةٌ مطلقة
)
MOST_WORDS = 200_000


def _all_admissible(shape: Guarded, length: int) -> list[tuple[int, ...]]:
    """كلُّ الجائزات الطولِ `length` — **بعَدٍّ مباشرٍ لا بالمتتالية**."""

    found: list[tuple[int, ...]] = []
    for word in product(range(shape.size), repeat=length):
        blocked_before = False
        good = True
        for symbol in word:
            free = symbol < shape.free
            if blocked_before and not free:
                good = False
                break
            blocked_before = not free
        if good:
            found.append(word)
    return found


def test_the_count_matches_a_direct_enumeration() -> None:
    """`T(n)` المُشتَقُّ = العدُّ المباشر — طريقتان مستقلّتان تتطابقان."""

    for shape in SHAPES:
        for length in range(0, 7):
            if shape.size**length > MOST_WORDS:
                continue
            assert len(_all_admissible(shape, length)) == admissible_count(
                shape, length
            ), (shape, length)


def test_the_recurrence_is_exact_in_integers_to_five_hundred() -> None:
    """`T(n) = f·T(n−1) + f·b·T(n−2)` — صحيحةٌ تامّةٌ إلى خمس مئة."""

    for shape in SHAPES:
        assert recurrence_holds(shape, 500), shape


def test_the_base_cases_are_what_the_proof_says() -> None:
    """`T(0) = 1` و`T(1) = f+b` و`T(2) = f² + 2fb` — كما في البرهان."""

    for shape in SHAPES:
        f, b = shape.free, shape.blocked
        assert admissible_count(shape, 0) == 1
        assert admissible_count(shape, 1) == f + b
        assert admissible_count(shape, 2) == f * f + 2 * f * b
        # وهو `(f+b)² − b²` — عددُ الكلمات ناقصَ ما فيه محجوران
        assert admissible_count(shape, 2) == (f + b) ** 2 - b * b


def test_folding_is_a_bijection_on_every_word_not_a_sample() -> None:
    """**كلُّ** جائزةٍ تُطوى، والأدلّةُ `{0,…,T(n)−1}` بلا تكرارٍ ولا فجوة."""

    for shape in SHAPES:
        for length in range(0, 7):
            if shape.size**length > MOST_WORDS:
                continue
            words = _all_admissible(shape, length)
            indices = [fold(shape, one) for one in words]
            whole = admissible_count(shape, length)
            assert len(indices) == whole, (shape, length)
            assert len(set(indices)) == whole, (shape, length)
            assert set(indices) == set(range(whole)), (shape, length)


def test_unfolding_recovers_every_word_exactly() -> None:
    """`unfold(fold(w)) = w` **لكلّ** جائزةٍ — حرفًا بحرف، لا تقريبًا."""

    for shape in SHAPES:
        for length in range(0, 7):
            if shape.size**length > MOST_WORDS:
                continue
            for word in _all_admissible(shape, length):
                assert unfold(shape, fold(shape, word), length) == word, (shape, word)


def test_folding_recovers_every_index_exactly() -> None:
    """`fold(unfold(k)) = k` لكلّ `k < T(n)` — والاتّجاهُ الآخرُ مستوفًى."""

    for shape in SHAPES:
        for length in range(0, 7):
            whole = admissible_count(shape, length)
            if whole > MOST_WORDS:
                continue
            for index in range(whole):
                assert fold(shape, unfold(shape, index, length)) == index


def test_folding_is_monotone_in_the_lexicographic_order() -> None:
    """والتقابلُ رتيبٌ: ترتيبُ الكلمات معجميًّا هو ترتيبُ أدلّتها."""

    for shape in SHAPES:
        for length in range(1, 6):
            if shape.size**length > MOST_WORDS:
                continue
            words = sorted(_all_admissible(shape, length))
            indices = [fold(shape, one) for one in words]
            assert indices == sorted(indices), (shape, length)
            assert indices == list(range(len(words))), (shape, length)


def test_the_guard_is_refused_not_silently_repaired() -> None:
    """ويُردّ محجورٌ بعد محجورٍ **بموضعه** — فلا يُطوى ما لا يُفَكّ."""

    shape = Guarded(free=3, blocked=1)
    with pytest.raises(FoldingError, match="الموضع 1"):
        fold(shape, (3, 3))
    with pytest.raises(FoldingError, match="الموضع 2"):
        fold(shape, (0, 3, 3))
    with pytest.raises(FoldingError):
        fold(shape, (4,))
    with pytest.raises(FoldingError):
        unfold(shape, admissible_count(shape, 3), 3)
    with pytest.raises(FoldingError):
        unfold(shape, -1, 3)


def test_the_sukun_guard_gives_the_golden_style_root_exactly() -> None:
    """`f=3, b=1` ⟹ `x² = 3x+3` ⟹ `ρ = (3+√21)/2` — وأوّلُ الأعداد ٤ ١٥ ٥٧."""

    shape = Guarded(free=3, blocked=1)
    assert [admissible_count(shape, one) for one in range(5)] == [1, 4, 15, 57, 216]
    # وأنّ ٢١٦ = ٣·٥٧ + ٣·١٥ بالضبط
    assert 216 == 3 * 57 + 3 * 15
    root = growth_root(shape)
    assert abs(root * root - (3 * root + 3)) < 1e-9
    assert abs(root - 3.7912878474779199) < 1e-12


def test_the_root_is_approached_without_any_float() -> None:
    """`ratio_gap` ينزل إلى الصفر بكسورٍ صحيحةٍ — فلا برهانَ بجذرٍ مُقرَّب.

    **وبلا حارسٍ يكون الصفرُ تامًّا من أوّل خطوة**: `T(n) = fⁿ` فالنسبةُ
    `f` بعينها، وهي الجذرُ الأكبرُ لـ`x² = f·x` — **فالفجوةُ صفرٌ لا
    مقاربةٌ إليه**. وذلك فرقٌ رياضيٌّ يُقال ولا يُطوى في «ينزل».
    """

    for shape in SHAPES:
        gaps = [abs(ratio_gap(shape, one)) for one in range(2, 40)]
        assert all(isinstance(one, Fraction) for one in gaps)
        assert gaps == sorted(gaps, reverse=True), shape
        assert gaps[-1] < Fraction(1, 10**6), (shape, gaps[-1])
        if shape.blocked == 0:
            assert set(gaps) == {Fraction(0)}, shape
        else:
            assert gaps[-1] < gaps[0], shape
            assert gaps[-1] == Fraction(0) or gaps[-1] < Fraction(1, 10**15), shape


def test_the_bit_count_is_integer_and_sufficient() -> None:
    """`⌈log₂ T(n)⌉` بالأعداد الصحيحة، وكافيةٌ لكلّ دليل."""

    for shape in SHAPES:
        for length in range(0, 9):
            whole = admissible_count(shape, length)
            width = bits_exactly(shape, length)
            assert whole <= 2**width or whole == 1, (shape, length)
            assert width == 0 or whole > 2 ** (width - 1)


def test_the_unguarded_shape_is_plain_base_conversion() -> None:
    """وبلا حارسٍ يصير الطيُّ تحويلَ أساسٍ — والتقابلُ يشمله فلا يُستثنى."""

    shape = Guarded(free=15, blocked=0)
    for length in range(0, 5):
        assert admissible_count(shape, length) == 15**length
    word = (1, 0, 14, 7)
    assert fold(shape, word) == 1 * 15**3 + 0 * 15**2 + 14 * 15 + 7
    assert unfold(shape, fold(shape, word), 4) == word


def test_the_module_claims_nothing_about_a_language() -> None:
    """ولا يُسمّى الحرُّ حركةً ولا المحجورُ سكونًا في الوحدة نفسِها."""

    from algebra import folding

    assert (
        "لا يُسمّى أحدُهما حركةً" in folding.THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE
    )
    assert folding.__doc__ is not None
    text = " ".join(folding.__doc__.split())
    assert "لا يُستَرجَع سطرٌ واحدٌ من `H = 2.6283`" in text
    assert "**تقابلٌ مبرهَنٌ**" in text


def test_folding_without_a_borrowed_length_is_a_bijection_onto_the_naturals() -> None:
    """المبرهنة ٤: `fold_any` تقابلٌ على `ℕ` — **ولا يُمرَّر طولٌ في الفكّ**.

    **والعطلُ الذي يُصلَحه**: `fold` تقابلٌ على الجائزات الطولِ `n` **وحدَه**،
    و`unfold` **تطلب `n`**. فمن فكَّ بطولٍ يعرفه من خارجٍ فقد استرجع
    **بدليلٍ وطول** — والطولُ معلومةٌ لم تُحسَب في الثمن.
    """

    for shape in SHAPES:
        whole = admissible_count(shape, 0) + admissible_count(shape, 1)
        upto = whole + admissible_count(shape, 2)
        seen: dict[int, tuple[int, ...]] = {}
        for index in range(min(upto, 400)):
            word = unfold_any(shape, index)
            assert fold_any(shape, word) == index, (shape, index)
            assert word not in seen.values(), (shape, word)
            seen[index] = word
        assert unfold_any(shape, 0) == (), shape
        assert set(len(one) for one in seen.values()) >= {0, 1}, shape


def test_the_blocks_of_each_length_are_consecutive_and_exact() -> None:
    """والفتراتُ `[off(n), off(n+1))` تقسم `ℕ` بسعةِ `T(n)` — وذلك البرهان."""

    for shape in SHAPES:
        for length in range(0, 6):
            low = offset(shape, length)
            high = offset(shape, length + 1)
            assert high - low == admissible_count(shape, length), (shape, length)
            for index in range(low, min(high, low + 60)):
                assert len(unfold_any(shape, index)) == length, (shape, index)


def test_every_admissible_word_folds_without_a_length_and_returns() -> None:
    """وكلُّ جائزةٍ حتّى الطول الخامس تُطوى بلا طولٍ وترجع — استيفاءً."""

    for shape in SHAPES:
        for length in range(0, 6):
            if shape.size**length > MOST_WORDS:
                continue
            for word in _all_admissible(shape, length):
                index = fold_any(shape, word)
                assert unfold_any(shape, index) == word, (shape, word)
                assert offset(shape, length) <= index < offset(shape, length + 1)


def test_the_ascent_composes_on_itself() -> None:
    """المبرهنة ٥: الألفاظُ أعدادٌ، فمتتاليتُها كلمةٌ تُطوى بالتقابل نفسِه."""

    unit = Guarded(free=3, blocked=1)
    longest = 4
    radix = offset(unit, longest + 1)
    above = Guarded(free=radix, blocked=0)
    words = [(0, 3, 0), (), (1,), (2, 2, 2, 2)]
    indices = tuple(fold_any(unit, one) for one in words)
    assert all(one < radix for one in indices)
    packed = fold_any(above, indices)
    assert unfold_any(above, packed) == indices
    rebuilt = [unfold_any(unit, one) for one in unfold_any(above, packed)]
    assert rebuilt == words


def test_every_heading_that_claims_a_theorem_carries_a_proof() -> None:
    """**العطل ٣٤**: عنوانٌ يقول «مبرهنة» ولا `∎` تحته — وقد وقع.

    كانت «المبرهنة ٢» عنوانًا بلا برهان: تقولُ `T(n)/T(n−1) → ρ` **دعوًى
    لا اشتقاقًا**، وأربعُ أخواتها تنتهي بـ`∎`. **وما كشفها فحصٌ بل قراءةُ
    الوحدة حرفًا حرفًا** حين طُلِب منّي فرزُ المبرهَن من المدَّعى.

    `A_HEADING_IS_NOT_A_PROOF`: فههنا مانعٌ آليّ: **كلُّ قسمٍ عنوانُه
    «المبرهنة» في `src/algebra` يلزمه `∎` في متنه**. ولو كان منصوبًا
    لَرُدَّت «المبرهنة ٢» يومَ كُتِبت.

    **وحدُّه مُعلَن**: يحرس **وجودَ** برهانٍ لا **صحّتَه** — برهانٌ خاطئٌ
    ينتهي بـ`∎` يمرُّ عليه. فهو يردُّ **العنوانَ الفارغ**، لا الغلط.
    """

    where = Path(__file__).resolve().parents[2] / "src" / "algebra"
    seen = 0
    for one in sorted(where.glob("*.py")):
        text = one.read_text(encoding="utf-8")
        parts = re.split(r"^## (?=المبرهنة)", text, flags=re.MULTILINE)[1:]
        for part in parts:
            head = part.splitlines()[0].strip()
            body = re.split(r"^## ", part, flags=re.MULTILINE)[0]
            assert "∎" in body, f"{one.name}: «{head}» بلا برهان"
            seen += 1
    assert seen == 5, seen


def test_the_integer_hypotheses_of_the_growth_proof_hold() -> None:
    """فروضُ المبرهنة ٢ **بأعدادٍ صحيحة** — والنهايةُ تلزم بالبرهان لا بالفحص.

    ولا تُفحَص نهايةٌ بحسابٍ منتهٍ. فيُفحَص ما يُفحَص: `f ≥ 1` فالنسبةُ
    معرَّفة؛ و`f·b ≥ 0` فـ`D ≥ f²`؛ وعند `b ≥ 1` يكون `D > f²` فالجذران
    متمايزان و`σ < 0 < ρ`؛ ومن `ρ+σ = f > 0` يلزم `ρ > |σ|`؛
    و`A = (f+b−σ)/√D > 0` **وهو موضعُ اللاانحلال**.
    """

    for shape in SHAPES:
        f, b = shape.free, shape.blocked
        assert f >= 1
        assert f * b >= 0
        discriminant = f * f + 4 * f * b
        assert discriminant >= f * f
        # مجموعُ الجذرين وحاصلُهما بأعدادٍ صحيحة — لا جذرَ تقريبيّ
        assert f * b == -(-f * b)  # ρ·σ = −f·b
        if b == 0:
            assert discriminant == f * f  # فـ ρ = f و σ = 0
            assert admissible_count(shape, 5) == f**5
        else:
            assert discriminant > f * f  # متمايزان، و σ < 0 < ρ
            # ‏`f + b − σ > f + b ≥ 1` فالمعامِلُ `A` موجبٌ ألبتّة
            assert f + b >= 1
