"""طبقاتُ ماركوف: الطبقةُ **إسقاطٌ**، والسؤالُ أهي مستوًى أم ظلّ؟

**العطلُ الذي تعالجه هذه الوحدة**: يُقال «طبقةٌ صوتيّة» و«طبقةٌ صرفيّة»
و«طبقةٌ دلاليّة» كأنّها مستوياتُ وصفٍ قائمةٌ بذاتها. وبناءُ سلسلةِ ماركوف
على طبقةٍ **يدّعي ضمنًا** أنّ الطبقةَ تكفي نفسَها: أنّ المستقبلَ مستقلٌّ عن
التفاصيل التي طُوِيت. وهذه دعوى **تُفحَص ولا تُفترَض**، ولها شرطٌ جبريٌّ
حاسم.

`A_LAYER_IS_A_PROJECTION_AND_NOTHING_MORE`: فالطبقةُ ههنا `π: Σ → Λ` تامّةُ
الصورة، وتمتدّ إلى التيارات **بالاستقراء على الطول**: `π(ε) = ε`
و`π(a·w) = π(a)·π(w)`. ولا طبقةَ بلا إسقاطٍ مُودَع — والتسميةُ وحدَها
ليست طبقة.

`THE_LAYERS_FORM_A_POSET_BY_REFINEMENT`: و`ℓ ⊑ ℓ'` متى وُجد `φ` بحيث
`π_ℓ = φ ∘ π_ℓ'`. وهذا ترتيبٌ جزئيّ، والتخشينُ نزولٌ فيه.

`COARSENING_CANNOT_ADD_INFORMATION`: ومنه مبرهنةُ معالجة المعطيات: إن
`ℓ ⊑ ℓ'` فالمعلوماتُ المتبادلةُ بين المتجاورين في `ℓ` **لا تفوق** نظيرتَها
في `ℓ'`. فارتفاعُها بالتخشين **مستحيلٌ بالبناء**، ووقوعُه في مقياسٍ عطلٌ
في المقياس لا خبرٌ عن اللغة.

`A_LAYER_WITHOUT_LUMPABILITY_IS_A_SHADOW_NOT_A_LEVEL`: والشرطُ الحاسم
(كيمني وسنل): الإسقاطُ **قابلٌ للتكتيل الشديد** متى استوى، لكلّ كتلتين
`A` و`B`، نصيبُ كلِّ عضوٍ من `A` إلى `B` كلِّها. فإن استوى كانت الطبقةُ
سلسلةَ ماركوف **بذاتها لأيّ بداية**؛ وإن اختلّ فهي **ظلُّ** سلسلةٍ أدقَّ
لا مستوًى قائم، وكلُّ رقمٍ يُقرَأ عليها مشروطٌ بالبداية. والخللُ يُقاس
`δ(π) ∈ [0,1]`، و`δ = 0` هو الشرط.

`AN_EMPIRICAL_ENTROPY_FALLS_BY_SPARSITY_NOT_ONLY_BY_STRUCTURE`: و`h_k`
المقيسةُ من عيّنةٍ تنزل برتبةِ السياق **حتمًا**، إذ عددُ السياقات ينمو
أسّيًّا ونصيبُ كلٍّ منها يضؤل حتّى يصير الرقمُ صفرًا بالحفظ لا بالبنية.
فلا يُقرَأ `h_k` إلّا مع **عدد سياقاته ومتوسّط نصيبها**، ويُوقَف عند أرضيّةٍ
مُعلَنة.

`FLOW_CONSERVATION_IS_AN_IDENTITY_NOT_A_FINDING`: ولكلّ تيارٍ متّصلٍ هُويّةٌ
تُبرهَن بالاستقراء على الطول: صادرُ الرمز ناقصَ وارده يساوي `[a = الأوّل] −
[a = الأخير]`. وهي **محفوظةٌ تحت كلّ إسقاط**، فتصلح حارسًا لكلّ تعدادِ
جوارٍ: خرقُها عطلُ آلةٍ لا خبرُ مادّة.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Final

__all__ = [
    "A_LAYER_IS_A_PROJECTION_AND_NOTHING_MORE_NOTE",
    "A_LAYER_WITHOUT_LUMPABILITY_IS_A_SHADOW_NOT_A_LEVEL_NOTE",
    "AN_EMPIRICAL_ENTROPY_FALLS_BY_SPARSITY_NOT_ONLY_BY_STRUCTURE_NOTE",
    "COARSENING_CANNOT_ADD_INFORMATION_NOTE",
    "ContextReading",
    "FLOW_CONSERVATION_IS_AN_IDENTITY_NOT_A_FINDING_NOTE",
    "Layer",
    "LayerError",
    "LumpabilityReading",
    "MARKOV_LAYER_NAMED_RESIDUALS",
    "bigram_census",
    "conditional_entropy",
    "context_reading",
    "flow_defect",
    "identity_layer",
    "induced_map",
    "lumpability",
    "mutual_information",
    "project_census",
    "refines",
]


class LayerError(ValueError):
    """رُدَّت طبقةٌ أو قياسٌ عليها: إسقاطٌ ناقص، أو رمزٌ خارجَ مجاله."""


@dataclass(frozen=True, slots=True)
class Layer:
    """طبقةٌ مُودَعة: اسمٌ وإسقاطٌ من الأبجديّة الأساس إلى أبجديّتها."""

    name: str
    projection: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise LayerError("طبقةٌ بلا اسمٍ لا تُنسَب إليها قراءة.")
        if not self.projection:
            raise LayerError(f"طبقةُ «{self.name}» بلا إسقاطٍ مُودَع؛ والتسميةُ ليست طبقة.")
        for source, target in self.projection.items():
            if not source or not target:
                raise LayerError(
                    f"طبقةُ «{self.name}»: رمزٌ خاوٍ في الإسقاط — "
                    "والخاوي ليس رمزًا ولا حدًّا."
                )

    @property
    def source_alphabet(self) -> tuple[str, ...]:
        """مجالُ الإسقاط مرتَّبًا؛ وما خرج عنه يُرَدّ ولا يُطوى."""

        return tuple(sorted(self.projection))

    @property
    def alphabet(self) -> tuple[str, ...]:
        """صورةُ الإسقاط مرتَّبةً — أبجديّةُ الطبقة."""

        return tuple(sorted(set(self.projection.values())))

    @property
    def blocks(self) -> Mapping[str, tuple[str, ...]]:
        """كتلُ التقسيم: لكلّ رمزٍ في الطبقة أصولُه في الأساس."""

        out: dict[str, list[str]] = {}
        for source in self.source_alphabet:
            out.setdefault(self.projection[source], []).append(source)
        return {one: tuple(members) for one, members in out.items()}

    def of(self, symbol: str) -> str:
        """صورةُ رمزٍ واحد؛ والرمزُ المجهول يُرَدّ ولا يُخمَّن له موضع."""

        try:
            return self.projection[symbol]
        except KeyError as error:
            raise LayerError(
                f"رمزٌ «{symbol}» خارجَ مجال طبقة «{self.name}»؛ "
                "ولا يُخمَّن له موضعٌ ولا يُطوى صامتًا."
            ) from error

    def stream(self, base: Sequence[str]) -> tuple[str, ...]:
        """امتدادُ الإسقاط إلى التيار بالاستقراء على الطول."""

        return tuple(self.of(one) for one in base)


def identity_layer(alphabet: Sequence[str], name: str = "الأساس") -> Layer:
    """الطبقةُ الذرّيّة: كلُّ رمزٍ كتلةٌ بذاته — وهي رأسُ ترتيب التخشين."""

    if not alphabet:
        raise LayerError("أبجديّةٌ خاليةٌ لا تُصنَع منها طبقة.")
    return Layer(name=name, projection={one: one for one in alphabet})


def refines(finer: Layer, coarser: Layer) -> bool:
    """أتخشينٌ هو؟ أي: أتقع كلُّ كتلةٍ من الأدقّ داخلَ كتلةٍ من الأخشن؟"""

    if set(finer.source_alphabet) != set(coarser.source_alphabet):
        raise LayerError(
            "طبقتان على أبجديّتين مختلفتين لا تُرتَّبان؛ " "والترتيبُ يقتضي مجالًا واحدًا."
        )
    seen: dict[str, str] = {}
    for source in finer.source_alphabet:
        image = finer.of(source)
        target = coarser.of(source)
        if seen.setdefault(image, target) != target:
            return False
    return True


def induced_map(finer: Layer, coarser: Layer) -> Mapping[str, str]:
    """`φ` بحيث `π_coarser = φ ∘ π_finer`؛ ويُرَدّ متى لم يكن تخشينًا."""

    if not refines(finer, coarser):
        raise LayerError(
            f"«{coarser.name}» ليست تخشينًا لـ«{finer.name}»؛ "
            "فلا دالّةَ بينهما، ولا يُقارَن الرقمان بمبرهنة المعالجة."
        )
    return {finer.of(one): coarser.of(one) for one in finer.source_alphabet}


def bigram_census(stream: Sequence[str]) -> Mapping[tuple[str, str], int]:
    """تعدادُ الجوار على تيارٍ واحدٍ متّصل؛ ولا يُقفَز على حدٍّ ههنا."""

    if len(stream) < 2:
        raise LayerError("تيارٌ دون رمزين لا جوارَ فيه يُعَدّ.")
    return Counter(zip(stream, stream[1:], strict=False))


def project_census(
    census: Mapping[tuple[str, str], int], layer: Layer
) -> Mapping[tuple[str, str], int]:
    """إسقاطُ تعدادٍ قائمٍ بدل إعادة المسح — وهو يكافئه بالبناء."""

    out: Counter[tuple[str, str]] = Counter()
    for (first, second), number in census.items():
        out[(layer.of(first), layer.of(second))] += number
    return out


def flow_defect(stream: Sequence[str]) -> Mapping[str, int]:
    """خللُ الحفظ لكلّ رمز؛ والهُويّةُ توجب أن يكون صفرًا في كلّ رمز.

    `Σ_b N(a,b) − Σ_b N(b,a) = [a = الأوّل] − [a = الأخير]`

    **بالاستقراء على الطول**: تيارٌ من رمزين يعطي `N(x₁,x₂) = 1` فيصدق
    الطرفان. وزيادةُ رمزٍ في الذيل تزيد صادرَ الأخير السابق وواردَ الجديد
    بواحد، فينتقل الطرفُ الأيمن معها — فتبقى الهُويّة.
    """

    census = bigram_census(stream)
    out_degree: Counter[str] = Counter()
    in_degree: Counter[str] = Counter()
    for (first, second), number in census.items():
        out_degree[first] += number
        in_degree[second] += number
    defect: dict[str, int] = {}
    for one in set(out_degree) | set(in_degree):
        expected = int(one == stream[0]) - int(one == stream[-1])
        defect[one] = out_degree[one] - in_degree[one] - expected
    return defect


def _probabilities(
    census: Mapping[tuple[str, str], int],
) -> tuple[Mapping[tuple[str, str], Fraction], int]:
    total = sum(census.values())
    if total <= 0:
        raise LayerError("تعدادٌ خالٍ لا تُقسَم عليه نسبة.")
    return {pair: Fraction(number, total) for pair, number in census.items()}, total


def mutual_information(census: Mapping[tuple[str, str], int]) -> float:
    """`I(X_t ; X_{t+1})` بالبتّات؛ الكسورُ مضبوطةٌ واللوغاريتمُ وحدَه عائم."""

    joint, _ = _probabilities(census)
    left: dict[str, Fraction] = {}
    right: dict[str, Fraction] = {}
    for (first, second), share in joint.items():
        left[first] = left.get(first, Fraction(0)) + share
        right[second] = right.get(second, Fraction(0)) + share
    return math.fsum(
        float(share) * math.log2(float(share / (left[first] * right[second])))
        for (first, second), share in joint.items()
        if share
    )


def conditional_entropy(census: Mapping[tuple[str, str], int]) -> float:
    """`H(X_{t+1} | X_t)` بالبتّات — رتبةُ السياق واحدة."""

    joint, _ = _probabilities(census)
    left: dict[str, Fraction] = {}
    for (first, _), share in joint.items():
        left[first] = left.get(first, Fraction(0)) + share
    return -math.fsum(
        float(share) * math.log2(float(share / left[first]))
        for (first, _), share in joint.items()
        if share
    )


@dataclass(frozen=True, slots=True)
class ContextReading:
    """قراءةُ رتبةٍ واحدة: قيمتُها، وعددُ سياقاتها، ومتوسّطُ نصيب السياق."""

    order: int
    entropy: float
    contexts: int
    mean_count: Fraction

    def __post_init__(self) -> None:
        if self.order < 1:
            raise LayerError("رتبةُ السياق واحدةٌ فأكثر.")
        if self.contexts < 1:
            raise LayerError("قراءةٌ بلا سياقٍ واحدٍ لا مقامَ لها.")
        if self.entropy < 0:
            raise LayerError("إنتروبيا سالبةٌ لا تُقرَأ؛ والعطلُ في العادّ.")
        if self.mean_count <= 0:
            raise LayerError("متوسّطُ نصيب السياق موجبٌ، وإلّا فلا سياق.")

    @property
    def is_readable(self) -> bool:
        """لا تُقرَأ رتبةٌ متوسّطُ نصيب سياقها دون عشرة — أرضيّةٌ مُعلَنة."""

        return self.mean_count >= 10


def context_reading(stream: Sequence[str], order: int) -> ContextReading:
    """`H(X_{t+1} | السياقُ السابقُ بطول order)` مع مقامه المنشور."""

    if order < 1:
        raise LayerError("رتبةُ السياق واحدةٌ فأكثر.")
    if len(stream) <= order:
        raise LayerError("تيارٌ أقصرُ من رتبته لا يُقاس.")
    contexts: dict[tuple[str, ...], Counter[str]] = {}
    for index in range(len(stream) - order):
        history = tuple(stream[index : index + order])
        contexts.setdefault(history, Counter())[stream[index + order]] += 1
    total = sum(sum(one.values()) for one in contexts.values())
    cells = [
        (number, sum(followers.values()))
        for followers in contexts.values()
        for number in followers.values()
    ]
    entropy = -math.fsum(
        (number / total) * math.log2(number / mass) for number, mass in cells
    )
    return ContextReading(
        order=order,
        entropy=entropy,
        contexts=len(contexts),
        mean_count=Fraction(total, len(contexts)),
    )


@dataclass(frozen=True, slots=True)
class LumpabilityReading:
    """قراءةُ التكتيل: خللُه، وأين بلغ أقصاه، وكم حالةٍ خرجت دون الأرضيّة.

    و`weighted` خللٌ موزونٌ بنصيب الكتل من المواضع: فخللٌ في كتلةٍ نادرةٍ
    ليس كخللٍ في كتلةٍ تحمل عُشرَ المادّة، والأقصى وحدَه لا يفرّق بينهما.
    """

    defect: Fraction
    weighted: Fraction
    worst_block: str
    worst_target: str
    floor: int
    compared_states: int
    excluded_states: int

    def __post_init__(self) -> None:
        for value, label in ((self.defect, "الخلل"), (self.weighted, "الموزون")):
            if not 0 <= value <= 1:
                raise LayerError(f"{label} فرقُ نسبتين، فمداه من صفرٍ إلى واحد.")
        if self.floor < 1:
            raise LayerError("أرضيّةُ الصادر واحدٌ فأكثر.")
        if self.compared_states < 0 or self.excluded_states < 0:
            raise LayerError("عددُ الحالات غيرُ سالبٍ بحال.")
        if self.defect == 0 and self.worst_block:
            raise LayerError("خللٌ صفرٌ لا كتلةَ أسوأَ له؛ والتسميةُ ادّعاء.")

    @property
    def is_strong(self) -> bool:
        """التكتيلُ الشديدُ صفرُ خلل — ولا يُقارَب، إمّا صفرٌ أو ظلّ."""

        return self.defect == 0


def lumpability(
    census: Mapping[tuple[str, str], int], layer: Layer, floor: int = 1
) -> LumpabilityReading:
    """شرطُ كيمني وسنل مقيسًا: أقصى فرقٍ في نصيب عضوين من كتلةٍ إلى كتلة.

    و**الأرضيّةُ شرطُ قراءةٍ لا تجميل**: حالةٌ صادرُها وقوعٌ واحدٌ صفُّها
    كتلةٌ نقطيّة، فتعطي فرقًا يساوي الواحدَ **بالندرة لا بالبنية**. فتُستبعَد
    الحالاتُ دون الأرضيّة و**تُعَدّ**، ويُنشَر العددُ مع الخلل. وأرضيّةُ
    الواحد تعني «لا استبعاد»، وهي الحالُ الخام.
    """

    if floor < 1:
        raise LayerError("أرضيّةُ الصادر واحدٌ فأكثر.")
    rows: dict[str, Counter[str]] = {}
    for (first, second), number in census.items():
        rows.setdefault(first, Counter())[layer.of(second)] += number
    masses = {one: sum(counts.values()) for one, counts in rows.items()}
    whole = sum(masses.values())

    targets = layer.alphabet
    defect = Fraction(0)
    weighted = Fraction(0)
    worst_block, worst_target = "", ""
    compared = 0
    excluded = 0
    for block, members in layer.blocks.items():
        present = [one for one in members if masses.get(one, 0) >= floor]
        excluded += len(members) - len(present)
        if len(present) < 2:
            continue
        compared += len(present)
        block_worst = Fraction(0)
        for target in targets:
            shares = [Fraction(rows[one][target], masses[one]) for one in present]
            spread = max(shares) - min(shares)
            block_worst = max(block_worst, spread)
            if spread > defect:
                defect, worst_block, worst_target = spread, block, target
        if whole:
            share = Fraction(sum(masses[one] for one in present), whole)
            weighted += share * block_worst
    return LumpabilityReading(
        defect=defect,
        weighted=weighted,
        worst_block=worst_block,
        worst_target=worst_target,
        floor=floor,
        compared_states=compared,
        excluded_states=excluded,
    )


A_LAYER_IS_A_PROJECTION_AND_NOTHING_MORE_NOTE: Final[str] = (
    "ALayerIsAProjectionAndNothingMore: لا طبقةَ بلا إسقاطٍ مُودَعٍ تامِّ "
    "الصورة؛ والاسمُ وحدَه ليس مستوى وصف"
)

COARSENING_CANNOT_ADD_INFORMATION_NOTE: Final[str] = (
    "CoarseningCannotAddInformation: التخشينُ لا يرفع المعلوماتِ المتبادلةَ "
    "بحال؛ فارتفاعُها عطلُ مقياسٍ لا خبرُ لغة"
)

A_LAYER_WITHOUT_LUMPABILITY_IS_A_SHADOW_NOT_A_LEVEL_NOTE: Final[str] = (
    "ALayerWithoutLumpabilityIsAShadowNotALevel: خللُ التكتيل صفرٌ أو ليس "
    "بمستوًى؛ والظلُّ يُقرَأ مشروطًا بالبداية لا مطلقًا"
)

AN_EMPIRICAL_ENTROPY_FALLS_BY_SPARSITY_NOT_ONLY_BY_STRUCTURE_NOTE: Final[str] = (
    "AnEmpiricalEntropyFallsBySparsityNotOnlyByStructure: تُقرَأ `h_k` مع "
    "عدد سياقاتها ومتوسّط نصيبها، وتُوقَف عند أرضيّةٍ مُعلَنة"
)

FLOW_CONSERVATION_IS_AN_IDENTITY_NOT_A_FINDING_NOTE: Final[str] = (
    "FlowConservationIsAnIdentityNotAFinding: صادرُ الرمز ناقصَ وارده حدٌّ "
    "طرفيّ؛ وخرقُها عطلُ آلةٍ يُوقِف التشغيل"
)

MARKOV_LAYER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_LAYER_IS_A_PROJECTION_AND_NOTHING_MORE_NOTE,
    COARSENING_CANNOT_ADD_INFORMATION_NOTE,
    A_LAYER_WITHOUT_LUMPABILITY_IS_A_SHADOW_NOT_A_LEVEL_NOTE,
    AN_EMPIRICAL_ENTROPY_FALLS_BY_SPARSITY_NOT_ONLY_BY_STRUCTURE_NOTE,
    FLOW_CONSERVATION_IS_AN_IDENTITY_NOT_A_FINDING_NOTE,
)
