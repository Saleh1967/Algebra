"""المركّباتُ البسيطة: حدٌّ مؤشَّر، وأعدادُ بيتي بكسورٍ صحيحة، ومَعيارُ أويلر.

**ما تفعله هذه الوحدة**: تبني المركّبَ البسيطَ على أيّ مجموعةِ رؤوسٍ منتهية،
وتحسب أعدادَ بيتي بحدٍّ **مؤشَّر** وكسورٍ صحيحة، وتفحص النتيجةَ بمَعيار أويلر
**اشتقاقًا مستقلًّا** لا إعادةَ للحساب نفسِه.

`AN_UNSIGNED_INCIDENCE_MATRIX_IS_NOT_A_BOUNDARY_MAP`: مصفوفةُ التجاور غيرِ
المؤشَّرة ليست حدًّا وإن تشابه شكلُها. وحسابٌ بها يُخرِج أعدادًا **مستحيلةً
بنيويًّا** — عددًا سالبًا، أو `β₀ = 0` لمركّبٍ غيرِ فارغ — لا «نتيجةً مخالفة».
ولذلك حارسان يرُدّانها عند الحساب قبل أن تُقرأ نتيجة.

`EULER_IS_AN_INDEPENDENT_WITNESS_NOT_A_RESTATEMENT`: مَعيارُ أويلر يُحسَب من
**عدد الأوجه** لا من الرتب، ومساواتُه مجموعَ أعداد بيتي بالتناوب فحصٌ يمكن أن
يسقط إن أخطأت الرتبةُ أو الإشارة. فهو شاهدٌ ثانٍ لا صياغةٌ أخرى للأوّل.

`A_COMPLEX_IS_CLOSED_OR_IT_IS_NOT_A_COMPLEX`: الانغلاقُ على الأوجه الأدنى شرطُ
إنشاءٍ يُرَدُّ خلافُه، ولا يُكمَّل المركّبُ صمتًا بأوجهٍ لم تُذكَر.

`THIS_MODULE_CLAIMS_NOTHING_ABOUT_ANY_LANGUAGE`: ما هنا رياضيّاتٌ تُفحَص
بالتعداد. وإن استُعمِلت في قراءةِ ظاهرةٍ ما، فشرطُ تلك القراءة يُكتَب هناك لا
ههنا.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb
from typing import Final

__all__ = [
    "A_COMPLEX_IS_CLOSED_OR_IT_IS_NOT_A_COMPLEX_NOTE",
    "AN_UNSIGNED_INCIDENCE_MATRIX_IS_NOT_A_BOUNDARY_MAP_NOTE",
    "EULER_IS_AN_INDEPENDENT_WITNESS_NOT_A_RESTATEMENT_NOTE",
    "SIMPLICIAL_NAMED_RESIDUALS",
    "Complex",
    "Face",
    "SimplicialError",
    "betti_numbers",
    "boundary_matrix",
    "closure_of",
    "enumerate_complexes",
    "enumeration_passes",
    "euler_characteristic",
    "euler_witness_holds",
    "matrix_rank",
    "skeleton",
]

Face = tuple[int, ...]
"""وجهٌ مرتَّبٌ تصاعديًّا؛ والترتيبُ شرطُ إشارةِ الحدّ لا زينةَ عرض."""


class SimplicialError(ValueError):
    """رُفض مدخلٌ أو ناتجٌ مستحيل؛ ولا يُحمَل على أقرب قيمةٍ مقبولة."""


def _face(items: tuple[int, ...]) -> Face:
    return tuple(sorted(items))


@dataclass(frozen=True, slots=True)
class Complex:
    """مركّبٌ بسيطٌ منغلقٌ على أوجهه الأدنى؛ والانغلاقُ شرطُ إنشاء."""

    faces: frozenset[Face]
    name: str = ""

    def __post_init__(self) -> None:
        if not self.faces:
            raise SimplicialError("مركّبٌ بلا وجهٍ واحدٍ ليس مركّبًا.")
        for face in self.faces:
            if not face:
                raise SimplicialError("الوجهُ الخالي لا يُقيَّد وجهًا ههنا.")
            if tuple(sorted(face)) != face:
                raise SimplicialError(f"وجهٌ غيرُ مرتَّب: {face}؛ والترتيبُ شرطُ الإشارة.")
            if len(set(face)) != len(face):
                raise SimplicialError(f"وجهٌ برأسٍ مكرَّر: {face}.")
            for size in range(1, len(face)):
                for sub in combinations(face, size):
                    if _face(sub) not in self.faces:
                        raise SimplicialError(
                            f"وجهٌ {face} بلا وجهه الأدنى {sub}؛ "
                            "ومركّبٌ غيرُ منغلقٍ ليس مركّبًا."
                        )

    @property
    def vertices(self) -> tuple[int, ...]:
        """رؤوسُ المركّب مُشتَقّةً من أوجهه، لا مكتوبةً إلى جانبها."""

        return tuple(sorted(face[0] for face in self.faces if len(face) == 1))

    @property
    def top_dimension(self) -> int:
        """أعلى بعدٍ فيه وجه، مُشتَقًّا لا مكتوبًا."""

        return max(len(face) for face in self.faces) - 1

    def faces_of_dimension(self, dimension: int) -> tuple[Face, ...]:
        """أوجهُ بعدٍ ما مرتّبةً ترتيبًا ثابتًا يُثبِّت أعمدةَ المصفوفة."""

        return tuple(sorted(face for face in self.faces if len(face) == dimension + 1))


def closure_of(generators: tuple[Face, ...], name: str = "") -> Complex:
    """أغلِق مجموعةَ أوجهٍ على أوجهها الأدنى، فيصير المركّبُ منها لا معها."""

    if not generators:
        raise SimplicialError("لا مركّبَ من مجموعةٍ خالية.")
    faces: set[Face] = set()
    for generator in generators:
        ordered = _face(generator)
        for size in range(1, len(ordered) + 1):
            for sub in combinations(ordered, size):
                faces.add(_face(sub))
    return Complex(faces=frozenset(faces), name=name)


def enumeration_passes(vertices: int) -> int:
    """كم دورةً يقتضي التعدادُ الشامل على `n` رأسًا: `2 ** (2**n − n − 1)`.

    ويُحسَب **قبل** التعداد لا بعده، لأنّ الرقمَ هو القرار: ١ و٢ و١٦ و٢٬٠٤٨
    للأربعة الأولى، ثمّ ٦٧ مليونًا للخامس، ثمّ ١٫٤ × ١٠¹⁷ للسادس.
    """

    if vertices < 1:
        raise SimplicialError("الرؤوسُ واحدٌ فأكثر.")
    higher = sum(comb(vertices, size) for size in range(2, vertices + 1))
    return 1 << higher


def enumerate_complexes(
    vertices: int, passes_at_most: int = 4_096
) -> tuple[Complex, ...]:
    """عدِّد المركّباتِ على `n` رأسًا التي تحوي كلَّ رؤوسها، تعدادًا شاملًا.

    ويُعدُّ الوجهُ الأعلى بأوجهه كلِّها: إضافةُ وجهٍ تقتضي أوجهَه الأدنى، فلا
    يدخل مثلّثٌ بلا أضلاعه الثلاثة.

    و`passes_at_most` سقفُ الدورات **المُعلَن**: ما تجاوزه يُرَدّ بعدده لا
    بصمتٍ ولا بانتظار. فالوحدةُ التي تزن بلوغَ اختبارٍ حدَّه لا يليق بها أن
    تحاول ما لا يُبلَغ؛ ورفعُ السقف يكون صريحًا ليُدفَع الثمنُ عن علم.
    """

    passes = enumeration_passes(vertices)
    if passes > passes_at_most:
        raise SimplicialError(
            f"تعدادُ {vertices} رؤوسٍ يقتضي {passes:,} دورةً، والسقفُ المُعلَن "
            f"{passes_at_most:,}. فارفعْه صراحةً إن أردتَ دفعَ الثمن."
        )
    points = tuple(range(1, vertices + 1))
    higher = [
        _face(subset)
        for size in range(2, vertices + 1)
        for subset in combinations(points, size)
    ]
    found: dict[frozenset[Face], Complex] = {}
    for chosen in range(1 << len(higher)):
        generators = tuple(
            face for index, face in enumerate(higher) if chosen >> index & 1
        )
        complex_ = closure_of((*generators, *((point,) for point in points)))
        found[complex_.faces] = complex_
    return tuple(
        found[key]
        for key in sorted(found, key=lambda faces: (len(faces), sorted(faces)))
    )


def skeleton(complex_: Complex, dimension: int) -> frozenset[Face]:
    """هيكلٌ من بعدٍ ما فما دون؛ والهيكلُ الأوّلُ هو ما يراه الرسمُ وحدَه."""

    if dimension < 0:
        raise SimplicialError("بعدُ الهيكل صفرٌ فأكثر.")
    return frozenset(face for face in complex_.faces if len(face) <= dimension + 1)


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    """رتبةُ مصفوفةٍ بكسورٍ صحيحة؛ ولا عائمَ في الطريق."""

    if not matrix:
        return 0
    rows = [row[:] for row in matrix]
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise SimplicialError("مصفوفةٌ غيرُ مستوية الصفوف.")
    pivot = 0
    for column in range(width):
        target = next(
            (index for index in range(pivot, len(rows)) if rows[index][column] != 0),
            None,
        )
        if target is None:
            continue
        rows[pivot], rows[target] = rows[target], rows[pivot]
        scale = Fraction(1) / rows[pivot][column]
        rows[pivot] = [value * scale for value in rows[pivot]]
        for index in range(len(rows)):
            if index != pivot and rows[index][column] != 0:
                factor = rows[index][column]
                rows[index] = [
                    value - factor * base
                    for value, base in zip(rows[index], rows[pivot], strict=True)
                ]
        pivot += 1
    return pivot


def boundary_matrix(complex_: Complex, dimension: int) -> list[list[Fraction]]:
    """مصفوفةُ الحدّ `∂_d` **مؤشَّرةً**: العنصرُ `(−1)ⁱ` لا `+1`."""

    if dimension < 1:
        raise SimplicialError("الحدُّ يُحسَب من البعد الأوّل صعودًا.")
    rows = complex_.faces_of_dimension(dimension - 1)
    columns = complex_.faces_of_dimension(dimension)
    if not rows or not columns:
        return []
    index_of = {face: position for position, face in enumerate(rows)}
    matrix = [[Fraction(0)] * len(columns) for _ in rows]
    for column, face in enumerate(columns):
        for position in range(len(face)):
            lower = face[:position] + face[position + 1 :]
            matrix[index_of[lower]][column] = Fraction((-1) ** position)
    return matrix


def betti_numbers(complex_: Complex) -> tuple[int, ...]:
    """أعدادُ بيتي بحدٍّ مؤشَّرٍ وكسورٍ صحيحة؛ والمستحيلُ يُرَدُّ لا يُخرَج."""

    ranks: dict[int, int] = {0: 0}
    for dimension in range(1, complex_.top_dimension + 1):
        ranks[dimension] = matrix_rank(boundary_matrix(complex_, dimension))
    numbers: list[int] = []
    for dimension in range(complex_.top_dimension + 1):
        count = len(complex_.faces_of_dimension(dimension))
        numbers.append(count - ranks.get(dimension, 0) - ranks.get(dimension + 1, 0))
    if any(value < 0 for value in numbers):
        raise SimplicialError(
            f"عددُ بيتي سالب: {tuple(numbers)}؛ وهو مستحيلٌ بنيويًّا، "
            "وأمارةُ حدٍّ غيرِ مؤشَّر."
        )
    if numbers[0] < 1:
        raise SimplicialError(
            f"β₀ = {numbers[0]} لمركّبٍ غيرِ فارغ؛ وهو مستحيلٌ، " "وأمارةُ حدٍّ غيرِ مؤشَّر."
        )
    return tuple(numbers)


def euler_characteristic(complex_: Complex) -> int:
    """مَعيارُ أويلر من **عدد الأوجه** بالتناوب، لا من الرتب."""

    return sum(
        (-1) ** dimension * len(complex_.faces_of_dimension(dimension))
        for dimension in range(complex_.top_dimension + 1)
    )


def euler_witness_holds(complex_: Complex) -> bool:
    """أيوافق مجموعُ أعداد بيتي بالتناوب مَعيارَ أويلر؟ شاهدٌ ثانٍ يمكن أن يسقط."""

    numbers = betti_numbers(complex_)
    alternating = sum((-1) ** index * value for index, value in enumerate(numbers))
    return bool(alternating == euler_characteristic(complex_))


AN_UNSIGNED_INCIDENCE_MATRIX_IS_NOT_A_BOUNDARY_MAP_NOTE: Final[str] = (
    "AnUnsignedIncidenceMatrixIsNotABoundaryMap: التجاورُ غيرُ المؤشَّر ليس حدًّا، "
    "وحسابٌ به يُخرِج مستحيلًا بنيويًّا لا نتيجةً مخالفة؛ فالحارسان يرُدّانه عند "
    "الحساب"
)

EULER_IS_AN_INDEPENDENT_WITNESS_NOT_A_RESTATEMENT_NOTE: Final[str] = (
    "EulerIsAnIndependentWitnessNotARestatement: المَعيارُ يُحسَب من عدد الأوجه لا "
    "من الرتب، فمساواتُه مجموعَ بيتي بالتناوب فحصٌ يمكن أن يسقط"
)

A_COMPLEX_IS_CLOSED_OR_IT_IS_NOT_A_COMPLEX_NOTE: Final[str] = (
    "AComplexIsClosedOrItIsNotAComplex: الانغلاقُ على الأوجه الأدنى شرطُ إنشاءٍ "
    "يُرَدُّ خلافُه، ولا يُكمَّل المركّبُ صمتًا"
)

SIMPLICIAL_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_UNSIGNED_INCIDENCE_MATRIX_IS_NOT_A_BOUNDARY_MAP_NOTE,
    EULER_IS_AN_INDEPENDENT_WITNESS_NOT_A_RESTATEMENT_NOTE,
    A_COMPLEX_IS_CLOSED_OR_IT_IS_NOT_A_COMPLEX_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
