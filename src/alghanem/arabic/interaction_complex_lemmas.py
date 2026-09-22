"""مركّبُ التفاعل: ل١ و ل٢ و ل٣ مفحوصةً عند كلّ استيراد، وحدُّها مُؤشَّر.

**ما تفعله هذه الوحدة**: تُودِع المركّباتَ البسيطةَ الثلاثةَ فوق السلسلة —
`Δ_chain` و`Δ_pair` و`Δ_full` — وتفحص القضايا الثلاثَ الواردةَ من خارج الشجرة
**بالتعداد والحساب**، لا بالنثر. والفحوصُ تُعاد عند كلّ استيراد، فقضيّةٌ تسقط
تمنع تحميلَ الوحدة.

`A_GRAPH_CANNOT_SEPARATE_THE_HOLLOW_FROM_THE_FILLED` (ل٢): للمثلّث الزوجيّ
والتفاعل الثلاثيّ **الهيكلُ الأوّلُ نفسُه** — ثلاثةُ رؤوسٍ وثلاثةُ أضلاع.
فالرسمُ وحدَه لا يفصل بينهما، والأداةُ الصحيحةُ المركّبُ البسيط. وهذا تصحيحٌ
وارد، وقد فُحِص هنا لا صُدِّق.

`NINE_COMPLEXES_AND_THREE_ABOVE_THE_CHAIN` (ل١): المركّباتُ على ثلاثة رؤوسٍ
**تسعة** بالتعداد الشامل، وما يحتوي السلسلةَ منها **ثلاثة**. والوجهُ الثلاثيُّ
لا يدخل إلّا بأضلاعه الثلاثة، فإضافةُ `123` تقتضي `13`.

`BETTI_IS_COMPUTED_WITH_A_SIGNED_BOUNDARY` (ل٣): الأعدادُ `(1,0)` و`(1,1)` و
`(1,0,0)`. والمثلّثُ الزوجيُّ أوّلُ مركّبٍ فيه دورةٌ — `β₁ = 1` — والوجهُ
الثلاثيُّ يملؤها فتعود صفرًا.

`AN_UNSIGNED_INCIDENCE_MATRIX_IS_NOT_A_BOUNDARY_MAP` — **تصحيحٌ لحسابي**:
حسبتُ ل٣ مرّتين بمصفوفةِ تجاورٍ غيرِ مؤشَّرة، فخرجت `β₀ = 0` لمركّبٍ متّصلٍ
ثمّ `β₁ = −1`. وكلتاهما **مستحيلةٌ بنيويًّا**، لا «نتيجةٌ مخالفة»: عددُ بيتي لا
يكون سالبًا، و`β₀` لمركّبٍ غيرِ فارغٍ لا يكون صفرًا. فالحدُّ مؤشَّرٌ
`∂(v₀…v_d) = Σ (−1)ⁱ (الوجهُ بلا vᵢ)`، ولو نُشرت قراءتي الأولى لقيل إنّ ل٣
ساقطةٌ وهي صحيحة. ولذلك أُضيف حارسان يرفضان المستحيلَ قبل أن يُقرأ نتيجةً
(`IMPOSSIBLE_BETTI_VALUES_ARE_REFUSED`).

`THE_UNIFORMITY_RESTS_ON_ROOT_DISTINCTNESS` (سندُ ت٣): انتظامُ التوزيع الشرطيّ
يقوم على أنّ خلايا الجدول صفرٌ أو واحد، فيكون `∏ n! = 1`. وذلك **أثرُ تمايز
الجذور** بعينه: داخل طبقة `C₂` الواحدة يجعل التمايزُ أزواجَ `(C₁,C₃)`
متمايزة. فشرطُ التمايز ليس تدقيقًا إجرائيًّا بل **هو** ما يجعل الصفريَّ
منتظمًا؛ ويُفحَص ههنا على الجذور المُودَعة لا يُفترَض.

`THIS_IS_A_CHECK_NOT_A_CERTIFICATION`: ما هنا فحصُ قضايا رياضيّةٍ، لا حكمٌ على
العربيّة ولا تصديقٌ لنتيجةٍ لغويّة. وقضيّةٌ رياضيّةٌ تُفحَص بالتعداد لا تحتاج
مصدرَين، بخلاف الدعاوى المقيسة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Final

from .slot_rights_algebra import InclusionPolicy, read_roots

__all__ = [
    "A_GRAPH_CANNOT_SEPARATE_THE_HOLLOW_FROM_THE_FILLED_NOTE",
    "AN_UNSIGNED_INCIDENCE_IS_NOT_A_BOUNDARY_NOTE",
    "BETTI_IS_COMPUTED_WITH_A_SIGNED_BOUNDARY_NOTE",
    "CHAIN",
    "CHAIN_EDGES",
    "COMPLEX_LEMMAS_NAMED_RESIDUALS",
    "FULL",
    "IMPOSSIBLE_BETTI_VALUES_ARE_REFUSED_NOTE",
    "NINE_COMPLEXES_AND_THREE_ABOVE_THE_CHAIN_NOTE",
    "PAIR",
    "THE_UNIFORMITY_RESTS_ON_ROOT_DISTINCTNESS_NOTE",
    "THIS_IS_A_CHECK_NOT_A_CERTIFICATION_NOTE",
    "VERTICES",
    "ComplexLemmaError",
    "Face",
    "InteractionComplex",
    "betti_numbers",
    "boundary_matrix",
    "complexes_above_the_chain",
    "enumerate_complexes",
    "first_skeleton",
    "matrix_rank",
    "strata_cells_are_binary",
]

VERTICES: Final[tuple[int, ...]] = (1, 2, 3)
"""رؤوسُ المركّب: خاناتُ الجذر الثلاثيّ."""

Face = tuple[int, ...]
"""وجهٌ مرتَّبٌ تصاعديًّا؛ والترتيبُ شرطُ إشارةِ الحدّ."""


class ComplexLemmaError(ValueError):
    """رُفض مدخلٌ أو ناتجٌ مستحيل؛ ولا يُحمَل على أقرب قيمةٍ مقبولة."""


def _face(items: tuple[int, ...]) -> Face:
    return tuple(sorted(items))


@dataclass(frozen=True, slots=True)
class InteractionComplex:
    """مركّبٌ بسيطٌ باسمه وأوجهه؛ والانغلاقُ على الأوجه الأدنى شرطُ إنشاء."""

    name: str
    faces: frozenset[Face]

    def __post_init__(self) -> None:
        if not self.faces:
            raise ComplexLemmaError("مركّبٌ بلا وجهٍ واحدٍ ليس مركّبًا.")
        for face in self.faces:
            if tuple(sorted(face)) != face:
                raise ComplexLemmaError(f"وجهٌ غيرُ مرتَّب: {face}؛ والترتيبُ شرطُ الإشارة.")
            for size in range(1, len(face)):
                for sub in combinations(face, size):
                    if _face(sub) not in self.faces:
                        raise ComplexLemmaError(
                            f"وجهٌ {face} بلا وجهه الأدنى {sub}؛ "
                            "ومركّبٌ غيرُ منغلقٍ على أوجهه الأدنى ليس مركّبًا."
                        )

    def faces_of_dimension(self, dimension: int) -> tuple[Face, ...]:
        """أوجهُ بعدٍ ما، مرتّبةً ترتيبًا ثابتًا يُثبِّت أعمدةَ المصفوفة."""

        return tuple(sorted(face for face in self.faces if len(face) == dimension + 1))

    @property
    def top_dimension(self) -> int:
        """أعلى بعدٍ فيه وجه، مُشتَقًّا لا مكتوبًا."""

        return max(len(face) for face in self.faces) - 1


CHAIN_EDGES: Final[tuple[Face, ...]] = ((1, 2), (2, 3))
"""أضلاعُ السلسلةِ المُودَعة بعينها: `12` و`23`، لا كلُّ مسارٍ ذي ضلعَين."""


def _name_for(edges: tuple[Face, ...], with_triangle: bool) -> str:
    """اسمٌ مُشتَقٌّ من الأوجه لا مُعلَّقٌ بعددها؛ والمُودَعُ يُسمّى باسمه.

    والمساراتُ ذواتُ الضلعَين ثلاثةٌ متماثلةٌ رسمًا، وواحدٌ منها **هو** سلسلةُ
    مركوف المُودَعة (`12` ثمّ `23`)؛ فلا يُسمّى الآخَران `Δ_chain` وإن شابهاها،
    إذ ترتيبُ الخانات معطًى لا اصطلاح.
    """

    if with_triangle:
        return "Δ_full"
    if len(edges) == 3:
        return "Δ_pair"
    if tuple(sorted(edges)) == CHAIN_EDGES:
        return "Δ_chain"
    listed = "، ".join("".join(str(vertex) for vertex in edge) for edge in edges)
    return f"Δ⟨{listed}⟩" if listed else "Δ⟨⟩"


def _closure(edges: tuple[Face, ...], with_triangle: bool) -> InteractionComplex:
    faces: set[Face] = {(vertex,) for vertex in VERTICES}
    faces |= set(edges)
    if with_triangle:
        faces.add(_face(VERTICES))
    if with_triangle and len(edges) != 3:
        raise ComplexLemmaError("الوجهُ الثلاثيُّ لا يدخل إلّا بأضلاعه الثلاثة.")
    return InteractionComplex(
        name=_name_for(edges, with_triangle), faces=frozenset(faces)
    )


_ALL_EDGES: Final[tuple[Face, ...]] = tuple(
    _face(pair) for pair in combinations(VERTICES, 2)
)

CHAIN: Final[InteractionComplex] = InteractionComplex(
    name="Δ_chain", faces=frozenset({(1,), (2,), (3,), (1, 2), (2, 3)})
)
"""السلسلة ⟨12, 23⟩: `C₁` مستقلّةٌ عن `C₃` إذا عُرفت `C₂`."""

PAIR: Final[InteractionComplex] = InteractionComplex(
    name="Δ_pair", faces=frozenset({(1,), (2,), (3,), *_ALL_EDGES})
)
"""المثلّثُ الزوجيّ ⟨12, 13, 23⟩: ثلاثُ روابطَ زوجيّة، والمثلّثُ أجوف."""

FULL: Final[InteractionComplex] = InteractionComplex(
    name="Δ_full",
    faces=frozenset({(1,), (2,), (3,), *_ALL_EDGES, _face(VERTICES)}),
)
"""التفاعلُ الثلاثيّ ⟨123⟩: المثلّثُ مصمت."""


def enumerate_complexes() -> tuple[InteractionComplex, ...]:
    """عدِّد كلَّ المركّبات على الرؤوس الثلاثة تعدادًا شاملًا (ل١)."""

    found: dict[frozenset[Face], InteractionComplex] = {}
    for size in range(len(_ALL_EDGES) + 1):
        for edges in combinations(_ALL_EDGES, size):
            for with_triangle in (False, True):
                if with_triangle and size != 3:
                    continue
                complex_ = _closure(edges, with_triangle)
                found[complex_.faces] = complex_
    return tuple(
        found[key]
        for key in sorted(found, key=lambda faces: (len(faces), sorted(faces)))
    )


def complexes_above_the_chain() -> tuple[InteractionComplex, ...]:
    """ما يحتوي السلسلةَ من المركّبات، مُشتَقًّا بالاحتواء لا مكتوبًا (ل١)."""

    return tuple(
        complex_ for complex_ in enumerate_complexes() if CHAIN.faces <= complex_.faces
    )


def first_skeleton(complex_: InteractionComplex) -> frozenset[Face]:
    """الهيكلُ الأوّل: الرؤوسُ والأضلاعُ وحدَها، وهو ما يراه الرسم (ل٢)."""

    return frozenset(face for face in complex_.faces if len(face) <= 2)


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    """رتبةُ مصفوفةٍ بكسورٍ صحيحة؛ ولا عائمَ في الطريق."""

    if not matrix:
        return 0
    rows = [row[:] for row in matrix]
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ComplexLemmaError("مصفوفةٌ غيرُ مستوية الصفوف.")
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


def boundary_matrix(
    complex_: InteractionComplex, dimension: int
) -> list[list[Fraction]]:
    """مصفوفةُ الحدّ `∂_d` **مؤشَّرةً**: العنصرُ `(−1)ⁱ` لا `+1`.

    والإشارةُ هي ما سهوتُ عنه مرّتين، فأخرج الحسابُ أعدادًا مستحيلة. ومصفوفةُ
    التجاور غيرِ المؤشَّرة ليست حدًّا، وإن تشابه شكلُها.
    """

    if dimension < 1:
        raise ComplexLemmaError("الحدُّ يُحسَب من البعد الأوّل صعودًا.")
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


def betti_numbers(complex_: InteractionComplex) -> tuple[int, ...]:
    """أعدادُ بيتي بحدٍّ مؤشَّرٍ وكسورٍ صحيحة (ل٣)؛ والمستحيلُ يُرَدُّ لا يُخرَج."""

    ranks: dict[int, int] = {0: 0}
    for dimension in range(1, complex_.top_dimension + 1):
        ranks[dimension] = matrix_rank(boundary_matrix(complex_, dimension))
    numbers: list[int] = []
    for dimension in range(complex_.top_dimension + 1):
        count = len(complex_.faces_of_dimension(dimension))
        numbers.append(count - ranks.get(dimension, 0) - ranks.get(dimension + 1, 0))
    if any(value < 0 for value in numbers):
        raise ComplexLemmaError(
            f"عددُ بيتي سالب: {tuple(numbers)}؛ وهو مستحيلٌ بنيويًّا، "
            "وأمارةُ حدٍّ غيرِ مؤشَّر."
        )
    if numbers[0] < 1:
        raise ComplexLemmaError(
            f"β₀ = {numbers[0]} لمركّبٍ غيرِ فارغ؛ وهو مستحيلٌ، وأمارةُ حدٍّ غيرِ مؤشَّر."
        )
    return tuple(numbers)


def strata_cells_are_binary(
    policy: InclusionPolicy = InclusionPolicy.WITH_DOUBLED,
    root: Path | None = None,
) -> bool:
    """سندُ ت٣ على الجذور المُودَعة: خلايا `(C₁,C₃)` داخل طبقة `C₂` صفرٌ أو واحد.

    وهذا **ما يجعل** التوزيعَ الشرطيَّ منتظمًا، إذ `∏ n! = 1`؛ فيُفحَص ولا
    يُفترَض.
    """

    roots, _dropped = read_roots(policy, root)
    if not roots:
        raise ComplexLemmaError("لا جذورَ في هذه السياسة.")
    strata: dict[str, set[tuple[str, str]]] = defaultdict(set)
    counts: dict[str, int] = defaultdict(int)
    for item in roots:
        strata[item[1]].add((item[0], item[2]))
        counts[item[1]] += 1
    return all(len(strata[middle]) == counts[middle] for middle in counts)


A_GRAPH_CANNOT_SEPARATE_THE_HOLLOW_FROM_THE_FILLED_NOTE: Final[str] = (
    "AGraphCannotSeparateTheHollowFromTheFilled: للمثلّث الزوجيّ والتفاعل "
    "الثلاثيّ الهيكلُ الأوّلُ نفسُه، فالرسمُ لا يفصل بينهما والأداةُ المركّبُ "
    "البسيط"
)

NINE_COMPLEXES_AND_THREE_ABOVE_THE_CHAIN_NOTE: Final[str] = (
    "NineComplexesAndThreeAboveTheChain: المركّباتُ على ثلاثة رؤوسٍ تسعةٌ "
    "بالتعداد الشامل، وما يحتوي السلسلةَ ثلاثةٌ؛ والوجهُ الثلاثيُّ لا يدخل "
    "إلّا بأضلاعه الثلاثة"
)

BETTI_IS_COMPUTED_WITH_A_SIGNED_BOUNDARY_NOTE: Final[str] = (
    "BettiIsComputedWithASignedBoundary: (1,0) و(1,1) و(1,0,0)؛ والمثلّثُ "
    "الزوجيُّ أوّلُ مركّبٍ فيه دورةٌ، والوجهُ الثلاثيُّ يملؤها"
)

AN_UNSIGNED_INCIDENCE_IS_NOT_A_BOUNDARY_NOTE: Final[str] = (
    "AnUnsignedIncidenceMatrixIsNotABoundaryMap: حُسِبت ل٣ مرّتين بتجاورٍ غيرِ "
    "مؤشَّرٍ فخرجت β₀ = 0 ثمّ β₁ = −1، وكلتاهما مستحيلةٌ بنيويًّا لا نتيجةٌ "
    "مخالفة؛ ولو نُشرت الأولى لقيل إنّ ل٣ ساقطةٌ وهي صحيحة"
)

IMPOSSIBLE_BETTI_VALUES_ARE_REFUSED_NOTE: Final[str] = (
    "ImpossibleBettiValuesAreRefused: عددٌ سالبٌ أو β₀ دون الواحد لمركّبٍ غيرِ "
    "فارغٍ يُرَدُّ عند الحساب لا يُخرَج؛ والحارسان يمنعان أن يُقرأ عطبُ الأداة "
    "نتيجةً"
)

THE_UNIFORMITY_RESTS_ON_ROOT_DISTINCTNESS_NOTE: Final[str] = (
    "TheUniformityRestsOnRootDistinctness: انتظامُ التوزيع الشرطيّ يقوم على "
    "خلايا صفرٍ أو واحدٍ فيكون ∏n! = 1، وذلك أثرُ تمايز الجذور بعينه؛ "
    "فالتمايزُ هو ما يجعل الصفريَّ منتظمًا لا تدقيقٌ إجرائيّ"
)

THIS_IS_A_CHECK_NOT_A_CERTIFICATION_NOTE: Final[str] = (
    "ThisIsACheckNotACertification: قضيّةٌ رياضيّةٌ تُفحَص بالتعداد لا تحتاج "
    "مصدرَين، بخلاف الدعاوى المقيسة؛ ولا حكمَ هنا على العربيّة"
)

COMPLEX_LEMMAS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_GRAPH_CANNOT_SEPARATE_THE_HOLLOW_FROM_THE_FILLED_NOTE,
    NINE_COMPLEXES_AND_THREE_ABOVE_THE_CHAIN_NOTE,
    BETTI_IS_COMPUTED_WITH_A_SIGNED_BOUNDARY_NOTE,
    AN_UNSIGNED_INCIDENCE_IS_NOT_A_BOUNDARY_NOTE,
    IMPOSSIBLE_BETTI_VALUES_ARE_REFUSED_NOTE,
    THE_UNIFORMITY_RESTS_ON_ROOT_DISTINCTNESS_NOTE,
    THIS_IS_A_CHECK_NOT_A_CERTIFICATION_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


# ل١ و ل٢ و ل٣ تُفحَص عند كلّ استيراد: قضيّةٌ تسقط تمنع تحميلَ الوحدة.
if len(enumerate_complexes()) != 9:  # pragma: no cover - حارس
    raise RuntimeError("ل١ سقطت: المركّباتُ على ثلاثة رؤوسٍ تسعة.")
if len(complexes_above_the_chain()) != 3:  # pragma: no cover - حارس
    raise RuntimeError("ل١ سقطت: ما فوق السلسلة ثلاثةُ مركّبات.")
if [c.name for c in enumerate_complexes()].count("Δ_chain") != 1:  # pragma: no cover
    raise RuntimeError("السلسلةُ المُودَعةُ واحدةٌ في التعداد، لا صفرٌ ولا اثنتان.")
if first_skeleton(PAIR) != first_skeleton(FULL):  # pragma: no cover - حارس
    raise RuntimeError("ل٢ سقطت: الهيكلُ الأوّلُ يجب أن يتطابق في الزوجيّ والثلاثيّ.")
if betti_numbers(CHAIN) != (1, 0):  # pragma: no cover - حارس
    raise RuntimeError("ل٣ سقطت عند السلسلة.")
if betti_numbers(PAIR) != (1, 1):  # pragma: no cover - حارس
    raise RuntimeError("ل٣ سقطت عند المثلّث الزوجيّ.")
if betti_numbers(FULL) != (1, 0, 0):  # pragma: no cover - حارس
    raise RuntimeError("ل٣ سقطت عند التفاعل الثلاثيّ.")
