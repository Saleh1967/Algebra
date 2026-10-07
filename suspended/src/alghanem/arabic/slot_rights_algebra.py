"""جبرُ حقوق الخانة على ثلاث طبقات، وسياسةُ الإدراج تُعلَن قبل العدّ.

**ما تفعله هذه الوحدة**: تبني الطبقاتَ الثلاثَ — حقوقُ الخانة، وهندسةُ
التركيب، والقيودُ المصنَّفةُ بنوع العلاقة — بأنواعٍ مغلقةٍ لمنازل الحكم، ثمّ
تُشغّلها على جذور المقاييس المُودَعة ببصمتها. والمصدرُ الثاني (QAC) **ليست
بايتاتُه في هذه الشجرة**، فلا وسمَ «مصدَّق» يصدر هنا بحال.

`THERE_IS_NO_FORBIDDEN_VALUE`: منازلُ الحقّ ثلاثٌ — مشهودٌ، ومرشَّحٌ للمنع،
وغيرُ محسوم — ولا رابعَ اسمُه «ممنوع». فالغيابُ وحدَه لا يُثبِت منعًا، وحارسٌ
يرفض أيَّ عضوٍ يُضاف بهذا المعنى.

`ATTESTATION_IS_MONOTONE` (مبرهنة ح١): ما شُهد يبقى مشهودًا مهما زادت
البيانات، لأنّ الشهادةَ وجوديّةٌ فتُحفَظ تحت التوسيع. وتُفحَص آليًّا: تشغيلٌ
على نصف الجذور ثمّ على كلّها، والمشهودُ في الأوّل يجب أن يبقى مشهودًا في
الثاني.

`THE_LEFT_AND_RIGHT_COMPOSITIONS_ARE_IDENTICAL` (مبرهنة ت١): التركيبُ الأيسر
`P(C₁,C₂)·P(C₃|C₂)` والأيمن `P(C₁|C₂)·P(C₂,C₃)` **متساويان تطابقًا**، إذ
كلاهما `P(C₂)·P(C₁|C₂)·P(C₃|C₂)`. فسؤالُ التجميعيّة ليس «أيتساوى الطرفان؟»
— وهو محقَّقٌ دائمًا — بل «أيساوي الطرفُ التوزيعَ الثلاثيَّ `P₁₂₃`؟»، وجوابُه
نعم **إذا وفقط إذا** انعدمت `I(C₁;C₃|C₂)`. وهذا مفحوصٌ عدديًّا على توزيعاتٍ
مولَّدةٍ لا على واحدٍ مختار.

`A_TYPES_LEXICON_CANNOT_TEST_CONDITIONAL_INDEPENDENCE` (مبرهنة ت٢، مُودَعةٌ
عن صاحب الجبر): في معجم أنواعٍ لا يتكرّر فيه جذر، المعلومةُ الشرطيّةُ
المحسوبةُ بالتكرار تتحدّد بالهوامش الثنائيّة، فلا تختبر الاستقلالَ الشرطيّ.
والمفحوصُ هنا شطرُها القابلُ للفحص: **نموذجٌ صفريٌّ يبدّل الأعمدةَ مستقلّةً
يولّد جذورًا مكرَّرةً**، أي لا يحفظ وحدةَ التحليل — ويُعَدُّ المكرَّرُ عددًا.

`AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL`: خليّةُ التماثل (`c₁ = c₂`) تُفرَد عن
خليّة التجانس (كتلةٌ واحدةٌ وحرفان مختلفان). وخلطُهما يجعل تخمةَ المضعَّف
تُقرأ خبرًا عن الكتلة. والاسمُ مأخوذٌ عمّا سمّاه صاحبُ الجبر.

`THE_INCLUSION_POLICY_IS_DECLARED_BEFORE_THE_COUNT`: وهذا **أهمُّ ما تُخرِجه
هذه الوحدة**. ملفُّ المقاييس يُصنّف الجذورَ أربعةَ أنواع، ومنها «مضاعف». وحكمُ
خليّة التماثل `C₂=C₃` **ينقلب بإدراجها**: كبتٌ عند الاقتصار على الثلاثيّ،
وتخمةٌ عند إدراج المضاعف. فسياسةُ الإدراج ليست تفصيلًا إجرائيًّا، بل هي التي
تُعيّن إشارةَ الحكم؛ ولذلك تحمل كلُّ قراءةٍ ههنا سياستَها في بنيتها، ولا تُقرأ
قراءةٌ بلا سياستها.

`ONE_SOURCE_YIELDS_UNDETERMINED_NOT_CERTIFIED`: قاعدةُ التصديق أن يتّفق
مصدران، وبايتاتُ QAC ليست في هذه الشجرة؛ فكلُّ حكمٍ هنا **غيرُ محسوم** بنصّ
القاعدة، لا تواضعًا. وحارسٌ يرفض وسمَ التصديق عن مصدرٍ واحد.

`THE_PERMUTATION_FLOOR_IS_A_FLOOR_NOT_A_VALUE`: أدنى قيمةٍ تُرصَد بـ`B` تبديلًا
هي `1/(B+1)`؛ فما بلغها يُكتَب حدًّا أدنى لا قيمةً مقيسة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import csv
import random
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .classical_makharij_table import CLASSICAL_ORDINAL
from .letter_fingerprint import fold_root
from .maqayis_root_table_deposit import root_table_digest, root_table_path
from .slgae_deposit import BORN_BLOCKS

__all__ = [
    "ATTESTATION_IS_MONOTONE_NOTE",
    "AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL_NOTE",
    "A_TYPES_LEXICON_CANNOT_TEST_CMI_NOTE",
    "ONE_SOURCE_YIELDS_UNDETERMINED_NOTE",
    "PERMUTATIONS",
    "RANKED_LETTERS",
    "SLOTS",
    "SLOT_RIGHTS_NAMED_RESIDUALS",
    "THERE_IS_NO_FORBIDDEN_VALUE_NOTE",
    "THE_COMPOSITIONS_ARE_IDENTICAL_NOTE",
    "THE_INCLUSION_POLICY_IS_DECLARED_NOTE",
    "THE_PERMUTATION_FLOOR_NOTE",
    "CellReading",
    "Certification",
    "InclusionPolicy",
    "PolicySensitivity",
    "RelationType",
    "RightStanding",
    "RightsCensus",
    "SlotAlgebraError",
    "compositions_are_identical",
    "derive_class_cells",
    "derive_identity_cells",
    "derive_policy_sensitivity",
    "derive_rights_census",
    "duplicates_under_column_permutation",
    "monotonicity_holds",
    "permutation_floor",
    "read_roots",
    "triple_equals_composition_iff_cmi_vanishes",
]

RANKED_LETTERS: Final[tuple[str, ...]] = tuple(sorted(CLASSICAL_ORDINAL))
"""الحروفُ المرقَّمةُ في الجدول المُبصَّم، وهي محورُ الحرف."""

SLOTS: Final[tuple[int, ...]] = (0, 1, 2)
"""خاناتُ الجذر الثلاثيّ، صفريّةَ الترقيم."""

PERMUTATIONS: Final[int] = 2_000
"""عددُ التباديل في الاختبارات؛ ومنه يُشتَقّ الحدُّ الأدنى للقيمة المرصودة."""


class SlotAlgebraError(ValueError):
    """رُفض مدخلٌ أو حكمٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class RightStanding(Enum):
    """منازلُ حقّ الحرف في الخانة. **ولا عضوَ اسمُه «ممنوع»**."""

    ATTESTED = "مشهود"
    PREVENTION_CANDIDATE = "مرشَّحٌ للمنع"
    UNDETERMINED = "غيرُ محسوم"


class RelationType(Enum):
    """أنواعُ العلاقة الثلاثةُ بين خانتين؛ وOCP فرعٌ في هذا الفضاء لا أصلُه."""

    C1C2 = (0, 1)
    C2C3 = (1, 2)
    C1C3 = (0, 2)


class InclusionPolicy(Enum):
    """سياسةُ إدراج أنواع الجذور، تُعلَن قبل العدّ لا بعده."""

    TRILATERAL_ONLY = ("ثلاثي",)
    WITH_DOUBLED = ("ثلاثي", "مضاعف")
    WITH_DOUBLED_AND_WEAK = ("ثلاثي", "مضاعف", "ثلاثي معتل")


class Certification(Enum):
    """منزلةُ التصديق؛ ولا تبلغ `CERTIFIED` إلّا باتّفاق مصدرين."""

    CERTIFIED = "مصدَّق: اتّفق المصدران"
    UNDETERMINED = "غيرُ محسوم: مصدرٌ واحد"


def permutation_floor(permutations: int = PERMUTATIONS) -> float:
    """أدنى قيمةٍ تُرصَد: `1/(B+1)`؛ وما بلغها حدٌّ أدنى لا قيمةٌ مقيسة."""

    if permutations < 1:
        raise SlotAlgebraError("عددُ التباديل موجب.")
    return 1.0 / (permutations + 1)


def read_roots(
    policy: InclusionPolicy, root: Path | None = None
) -> tuple[tuple[str, ...], int]:
    """اقرأ الجذورَ الثلاثيّةَ بسياسةٍ مُعلَنة، وأعِد معها عددَ المُسقَط.

    والطيُّ هو `fold_root` المُودَع في الشجرة لا خريطةً تُكتَب هنا: صورُ الهمزة
    تُطوى إلى `ء`، و`ى` إلى `ي`. ثمّ يُسقَط كلُّ جذرٍ فيه حرفٌ لا رتبةَ له في
    الجدول — والألفُ من هؤلاء بإعلان الجدول نفسِه — ويُعَدُّ المُسقَطُ ولا
    يُطوى صمتًا.
    """

    path = root_table_path(root)
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    folded = {
        fold_root(row["root_full"]) for row in rows if row["root_type"] in policy.value
    }
    triples = sorted(item for item in folded if len(item) == 3)
    kept = tuple(
        item for item in triples if all(char in CLASSICAL_ORDINAL for char in item)
    )
    return kept, len(triples) - len(kept)


@dataclass(frozen=True, slots=True)
class RightsCensus:
    """الطبقةُ الأولى: منازلُ الخلايا الأربعِ والثمانين بسياستها ومصدرها."""

    policy: InclusionPolicy
    roots: int
    dropped_for_unranked: int
    cells: int
    attested: int
    prevention_candidates: tuple[tuple[str, int], ...]
    undetermined: tuple[tuple[str, int], ...]
    source_digest: str
    certification: Certification

    def __post_init__(self) -> None:
        counted = (
            self.attested + len(self.prevention_candidates) + len(self.undetermined)
        )
        if counted != self.cells:
            raise SlotAlgebraError(
                f"مجموعُ المنازل {counted} والخلايا {self.cells}؛ "
                "وخليّةٌ بلا منزلةٍ تُقرأ صمتُها شهادة."
            )
        if self.certification is Certification.CERTIFIED:
            raise SlotAlgebraError(
                "لا يصدر وسمُ التصديق عن مصدرٍ واحد؛ وبايتاتُ المصدر الثاني "
                "ليست في هذه الشجرة."
            )


def derive_rights_census(
    policy: InclusionPolicy, root: Path | None = None
) -> RightsCensus:
    """شغِّل الطبقةَ الأولى: أيُّ الخلايا مشهودٌ وأيُّها لا."""

    roots, dropped = read_roots(policy, root)
    if not roots:
        raise SlotAlgebraError("لا جذورَ في هذه السياسة، فلا حقوقَ تُقرأ.")
    seen = {(char, index) for item in roots for index, char in enumerate(item)}
    absent = tuple(
        (letter, slot)
        for letter in RANKED_LETTERS
        for slot in SLOTS
        if (letter, slot) not in seen
    )
    return RightsCensus(
        policy=policy,
        roots=len(roots),
        dropped_for_unranked=dropped,
        cells=len(RANKED_LETTERS) * len(SLOTS),
        attested=len(seen),
        prevention_candidates=absent,
        undetermined=(),
        source_digest=root_table_digest(root),
        certification=Certification.UNDETERMINED,
    )


def monotonicity_holds(
    policy: InclusionPolicy = InclusionPolicy.WITH_DOUBLED,
    root: Path | None = None,
) -> bool:
    """مبرهنة ح١ بالتشغيل: المشهودُ على نصف الجذور مشهودٌ على كلّها."""

    roots, _dropped = read_roots(policy, root)
    half = roots[: len(roots) // 2]
    small = {(char, index) for item in half for index, char in enumerate(item)}
    whole = {(char, index) for item in roots for index, char in enumerate(item)}
    return small <= whole


def compositions_are_identical(trials: int = 200, seed: int = 20260922) -> bool:
    """مبرهنة ت١، شطرُها الأوّل: الطرفان متساويان تطابقًا على كلّ توزيع."""

    if trials < 1:
        raise SlotAlgebraError("عددُ المحاولات موجب.")
    rng = random.Random(seed)
    for _ in range(trials):
        p_b = [rng.random() for _ in range(3)]
        total = sum(p_b)
        p_b = [value / total for value in p_b]
        a_given_b = [_normalized([rng.random() for _ in range(3)]) for _ in range(3)]
        c_given_b = [_normalized([rng.random() for _ in range(3)]) for _ in range(3)]
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    left = (p_b[b] * a_given_b[b][a]) * c_given_b[b][c]
                    right = a_given_b[b][a] * (p_b[b] * c_given_b[b][c])
                    if abs(left - right) > 1e-12:
                        return False
    return True


def _normalized(values: list[float]) -> list[float]:
    total = sum(values)
    return [value / total for value in values]


def triple_equals_composition_iff_cmi_vanishes(
    trials: int = 60, seed: int = 20260922
) -> bool:
    """مبرهنة ت١، شطرُها الثاني: الطرفُ يساوي `P₁₂₃` متى انعدمت المعلومةُ الشرطيّة.

    ويُفحَص الاتّجاهان: توزيعٌ مبنيٌّ على الاستقلال الشرطيّ يُطابِق، وتوزيعٌ
    عامٌّ لا يُطابِق إلّا إذا انعدمت معلومتُه الشرطيّة.
    """

    rng = random.Random(seed)
    for _ in range(trials):
        p_b = _normalized([rng.random() for _ in range(3)])
        a_given_b = [_normalized([rng.random() for _ in range(3)]) for _ in range(3)]
        c_given_b = [_normalized([rng.random() for _ in range(3)]) for _ in range(3)]
        built = {
            (a, b, c): p_b[b] * a_given_b[b][a] * c_given_b[b][c]
            for a in range(3)
            for b in range(3)
            for c in range(3)
        }
        if _conditional_mutual_information(built) > 1e-12:
            return False
        general = {
            (a, b, c): rng.random()
            for a in range(3)
            for b in range(3)
            for c in range(3)
        }
        mass = sum(general.values())
        general = {key: value / mass for key, value in general.items()}
        cmi = _conditional_mutual_information(general)
        composed = _compose_from_margins(general)
        matches = all(abs(general[key] - composed[key]) <= 1e-12 for key in general)
        if matches != (cmi <= 1e-12):
            return False
    return True


def _conditional_mutual_information(
    joint: dict[tuple[int, int, int], float],
) -> float:
    from math import log

    total = 0.0
    for b in range(3):
        p_b = sum(joint[(a, b, c)] for a in range(3) for c in range(3))
        if p_b <= 0:
            continue
        for a in range(3):
            p_ab = sum(joint[(a, b, c)] for c in range(3))
            for c in range(3):
                p_abc = joint[(a, b, c)]
                p_cb = sum(joint[(x, b, c)] for x in range(3))
                if p_abc <= 0 or p_ab <= 0 or p_cb <= 0:
                    continue
                total += p_abc * log((p_abc * p_b) / (p_ab * p_cb))
    return total


def _compose_from_margins(
    joint: dict[tuple[int, int, int], float],
) -> dict[tuple[int, int, int], float]:
    composed: dict[tuple[int, int, int], float] = {}
    for b in range(3):
        p_b = sum(joint[(a, b, c)] for a in range(3) for c in range(3))
        for a in range(3):
            p_ab = sum(joint[(a, b, c)] for c in range(3))
            for c in range(3):
                p_cb = sum(joint[(x, b, c)] for x in range(3))
                composed[(a, b, c)] = 0.0 if p_b <= 0 else p_ab * p_cb / p_b
    return composed


def duplicates_under_column_permutation(
    policy: InclusionPolicy = InclusionPolicy.WITH_DOUBLED,
    seed: int = 20260922,
    root: Path | None = None,
) -> int:
    """شطرُ مبرهنة ت٢ القابلُ للفحص: تبديلُ الأعمدة مستقلًّا يولّد مكرَّرًا.

    والمكرَّرُ يُعَدّ: نموذجٌ يولّد جذرَين متماثلين لا يحفظ وحدةَ التحليل،
    فلا يصلح صفرًا لمعجمِ أنواع.
    """

    roots, _dropped = read_roots(policy, root)
    rng = random.Random(seed)
    columns = [list(item[index] for item in roots) for index in SLOTS]
    for column in columns:
        rng.shuffle(column)
        # ترتيبٌ عشوائيٌّ مستقلٌّ لكلّ عمود، وهو عينُ النموذج المُنتقَد
    generated = [
        "".join(columns[index][position] for index in SLOTS)
        for position in range(len(roots))
    ]
    return len(generated) - len(set(generated))


@dataclass(frozen=True, slots=True)
class CellReading:
    """خليّةٌ من الطبقة الثالثة: مرصودُها ومتوقّعُها بسياستها ونوع علاقتها."""

    label: str
    relation: RelationType
    policy: InclusionPolicy
    observed: int
    expected: float
    is_identity_cell: bool

    def __post_init__(self) -> None:
        if self.expected <= 0:
            raise SlotAlgebraError("المتوقَّعُ موجبٌ، وإلّا فلا نسبةَ تُحسَب.")
        if self.observed < 0:
            raise SlotAlgebraError("المرصودُ غيرُ سالب.")

    @property
    def ratio(self) -> float:
        """`O/E`، مُشتَقًّا لا مكتوبًا."""

        return self.observed / self.expected

    @property
    def is_suppressed(self) -> bool:
        """أمكبوتةٌ هي؟ مُشتَقٌّ من النسبة لا من حقلٍ بجانبها."""

        return self.ratio < 1.0


def _margins(roots: tuple[str, ...]) -> list[Counter[str]]:
    return [Counter(item[index] for item in roots) for index in SLOTS]


def derive_identity_cells(
    policy: InclusionPolicy, root: Path | None = None
) -> tuple[CellReading, ...]:
    """خلايا التماثل بحسب نوع العلاقة، مُفرَدةً عن خلايا الكتلة."""

    roots, _dropped = read_roots(policy, root)
    margins = _margins(roots)
    total = len(roots)
    readings: list[CellReading] = []
    for relation in RelationType:
        first, second = relation.value
        observed = sum(1 for item in roots if item[first] == item[second])
        expected = (
            sum(
                margins[first][letter] * margins[second][letter]
                for letter in RANKED_LETTERS
            )
            / total
        )
        readings.append(
            CellReading(
                label=f"تماثل {relation.name}",
                relation=relation,
                policy=policy,
                observed=observed,
                expected=expected,
                is_identity_cell=True,
            )
        )
    return tuple(readings)


def derive_class_cells(
    policy: InclusionPolicy, root: Path | None = None
) -> tuple[CellReading, ...]:
    """خلايا التجانس: كتلةٌ واحدةٌ وحرفان **مختلفان**، فلا تخمةَ تماثلٍ فيها."""

    roots, _dropped = read_roots(policy, root)
    margins = _margins(roots)
    total = len(roots)
    block_of = {char: name for name, chars in BORN_BLOCKS for char in chars}
    readings: list[CellReading] = []
    for relation in RelationType:
        first, second = relation.value
        observed = sum(
            1
            for item in roots
            if item[first] != item[second]
            and block_of.get(item[first]) is not None
            and block_of.get(item[first]) == block_of.get(item[second])
        )
        expected = sum(
            margins[first][one] * margins[second][two] / total
            for one in RANKED_LETTERS
            for two in RANKED_LETTERS
            if one != two
            and block_of.get(one) is not None
            and block_of.get(one) == block_of.get(two)
        )
        readings.append(
            CellReading(
                label=f"تجانس {relation.name}",
                relation=relation,
                policy=policy,
                observed=observed,
                expected=expected,
                is_identity_cell=False,
            )
        )
    return tuple(readings)


@dataclass(frozen=True, slots=True)
class PolicySensitivity:
    """أثرُ سياسة الإدراج على إشارة حكمِ خليّةٍ واحدة."""

    label: str
    relation: RelationType
    under_trilateral_only: float
    under_with_doubled: float
    sign_flips: bool

    def __post_init__(self) -> None:
        flips = (self.under_trilateral_only < 1.0) != (self.under_with_doubled < 1.0)
        if self.sign_flips != flips:
            raise SlotAlgebraError(
                "حقلُ الانقلاب لا يطابق النسبتين؛ وانقلابٌ يُكتَب ولا يُشتَقّ " "دعوى لا حساب."
            )


def derive_policy_sensitivity(
    root: Path | None = None,
) -> tuple[PolicySensitivity, ...]:
    """قابِلْ خلايا التماثل تحت سياستَي إدراج، وأخرِج ما تنقلب إشارتُه."""

    only = {
        item.relation: item.ratio
        for item in derive_identity_cells(InclusionPolicy.TRILATERAL_ONLY, root)
    }
    doubled = {
        item.relation: item.ratio
        for item in derive_identity_cells(InclusionPolicy.WITH_DOUBLED, root)
    }
    return tuple(
        PolicySensitivity(
            label=f"تماثل {relation.name}",
            relation=relation,
            under_trilateral_only=only[relation],
            under_with_doubled=doubled[relation],
            sign_flips=(only[relation] < 1.0) != (doubled[relation] < 1.0),
        )
        for relation in RelationType
    )


THERE_IS_NO_FORBIDDEN_VALUE_NOTE: Final[str] = (
    "ThereIsNoForbiddenValue: منازلُ الحقّ ثلاثٌ ولا رابعَ اسمُه «ممنوع»؛ "
    "فالغيابُ وحدَه لا يُثبِت منعًا، وحارسٌ يرفض عضوًا بهذا المعنى"
)

ATTESTATION_IS_MONOTONE_NOTE: Final[str] = (
    "AttestationIsMonotone: الشهادةُ وجوديّةٌ فتُحفَظ تحت التوسيع؛ ومبرهنةُ "
    "ح١ مفحوصةٌ بالتشغيل على نصفٍ ثمّ على الكلّ لا مُبرهَنةٌ بالنثر"
)

THE_COMPOSITIONS_ARE_IDENTICAL_NOTE: Final[str] = (
    "TheLeftAndRightCompositionsAreIdentical: الطرفان متساويان تطابقًا لأنّ "
    "كلًّا منهما P(C₂)·P(C₁|C₂)·P(C₃|C₂)؛ فالسؤالُ الحقيقيُّ أيساوي الطرفُ "
    "P₁₂₃، وجوابُه نعم إذا وفقط إذا انعدمت I(C₁;C₃|C₂)"
)

A_TYPES_LEXICON_CANNOT_TEST_CMI_NOTE: Final[str] = (
    "ATypesLexiconCannotTestConditionalIndependence: في معجم أنواعٍ لا يتكرّر "
    "فيه جذرٌ تتحدّد المعلومةُ الشرطيّةُ بالهوامش الثنائيّة؛ ونموذجٌ صفريٌّ "
    "يبدّل الأعمدةَ مستقلًّا يولّد مكرَّرًا فلا يحفظ وحدةَ التحليل"
)

AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL_NOTE: Final[str] = (
    "AnIdentityCellIsNotAClassCell: خليّةُ التماثل تُفرَد عن خليّة التجانس؛ "
    "وخلطُهما يجعل تخمةَ المضعَّف تُقرأ خبرًا عن الكتلة"
)

THE_INCLUSION_POLICY_IS_DECLARED_NOTE: Final[str] = (
    "TheInclusionPolicyIsDeclaredBeforeTheCount: حكمُ خليّة التماثل C2C3 "
    "ينقلب بإدراج المضاعف — كبتٌ بدونه وتخمةٌ معه؛ فالسياسةُ تُعيّن إشارةَ "
    "الحكم، وتحمل كلُّ قراءةٍ سياستَها في بنيتها"
)

ONE_SOURCE_YIELDS_UNDETERMINED_NOTE: Final[str] = (
    "OneSourceYieldsUndeterminedNotCertified: التصديقُ اتّفاقُ مصدرين، "
    "وبايتاتُ QAC ليست في هذه الشجرة؛ فكلُّ حكمٍ هنا غيرُ محسومٍ بنصّ القاعدة "
    "لا تواضعًا، وحارسٌ يرفض وسمَ التصديق عن مصدرٍ واحد"
)

THE_PERMUTATION_FLOOR_NOTE: Final[str] = (
    "ThePermutationFloorIsAFloorNotAValue: أدنى ما يُرصَد بـB تبديلًا "
    "1/(B+1)؛ فما بلغها حدٌّ أدنى لا قيمةٌ مقيسة"
)

SLOT_RIGHTS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THERE_IS_NO_FORBIDDEN_VALUE_NOTE,
    ATTESTATION_IS_MONOTONE_NOTE,
    THE_COMPOSITIONS_ARE_IDENTICAL_NOTE,
    A_TYPES_LEXICON_CANNOT_TEST_CMI_NOTE,
    AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL_NOTE,
    THE_INCLUSION_POLICY_IS_DECLARED_NOTE,
    ONE_SOURCE_YIELDS_UNDETERMINED_NOTE,
    THE_PERMUTATION_FLOOR_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if "FORBIDDEN" in RightStanding.__members__:  # pragma: no cover - حارس
    raise RuntimeError(
        "أُضيف عضوٌ اسمُه «ممنوع» إلى منازل الحقّ؛ والغيابُ وحدَه لا يُثبِت منعًا."
    )
if len(RelationType) != 3:  # pragma: no cover - حارس
    raise RuntimeError("أنواعُ العلاقة ثلاثةٌ؛ وزيادةٌ تُفسِد تصنيفَ القيود.")
