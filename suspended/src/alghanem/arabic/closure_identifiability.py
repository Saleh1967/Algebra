"""تنفيذُ شرط الإبطال الرابع: القيدُ يقسم، والعددُ لا يتعيّن — والمانعُ بنيويّ.

**ما تفعله هذه الوحدة**: تُنفّذ الشرطَ الرابعَ من
`WHAT_WOULD_FALSIFY_THE_REDUCTION` في `closure_window_reduction` — «قيدٌ آخرُ
يقسم القوالبَ القسمةَ نفسها بلا عدّ سواكن، فيسقط تخصيصُ العدد» — بتعديد
مرشّحاتٍ آليًّا على فضاء الوصف، لا بالبحث في الذاكرة.

`THE_FOURTH_FALSIFIER_FIRES`: وقد **فَعَل**. أربعةُ مرشّحاتٍ تُعطي القسمةَ
نفسَها بلا خطأٍ في قالبٍ واحد: عدُّ سواكن النافذة `s ≤ 1`، والوزنُ المُوريُّ
`μ ≤ 2`، وطولُ القافية `≤ 2`، وطولُ المقطع `≤ 3`. فالقسمةُ **لا تُعيّن** أيَّ
المقاييس هو العامل.

`S_AND_MU_ARE_ONE_FUNCTION_IN_TWO_DRESSES`: وأشدُّ من ذلك: `μ = s + 1` على
فضاء الوصف كلِّه، لا على القوالب الستّة وحدها. فهما **إعادةُ معايرةٍ تآلفيّة**
لدالّةٍ واحدة، لا قيدان متنافسان. ومن قابل بينهما على القوالب قابل بين
تسميتين.

`THE_IDENTIFIABILITY_BARRIER_IS_STRUCTURAL_NOT_EMPIRICAL`: والموضعُ الوحيدُ
الذي يفترق فيه المقياسان هو **عنقودٌ في بداية ما يلي**: `s` ترى بدايةَ ما يلي
لأنّ `k = إغلاقٌ + بداية`، و`μ` لا تراها. فعند بدايتين يفترقان في كلّ قالب،
وعند بدايةٍ واحدةٍ لا يفترقان في واحد. **والعربيّةُ لا تُرخّص العنقودَ في
البداية** — بقانون الحواف نفسِه: «بدايةٌ واحدة». فالمانعُ من التعيين ليس قلّةَ
بيانٍ تُسَدُّ بمدوّنةٍ أوسع، بل **بنيةُ اللغة تمنع الموضعَ الفاصل**.

`WHAT_FALLS_IS_THE_SPECIALIZATION_NOT_THE_PARTITION`: فالساقطُ **تخصيصُ
العدد** — أي أنّ عدَّ السواكن بعينه هو العامل. والباقي قائمٌ: القسمةُ نفسُها،
وأنّ العاملَ دالّةٌ على الزوج (إغلاق، طول) بحدٍّ واحد. وأربعةُ مرشّحاتٍ تقع في
صنفٍ واحدٍ من التكافؤ، فلا يُنتقى منها واحدٌ بهذه البيانات.

`THIS_WEAKENS_A_PHRASE_IN_THE_DOCUMENT`: وعبارةُ ٥م «العدد فراكتالي، والنوع
معجمي» تحمل من التخصيص ما لا يقوم عليه دليلٌ ههنا: «العدد» فيها قد يكون
«الوزن» بلا فرقٍ مرصود. والعبارةُ لا تُبطَل — يُضيَّق مدلولُها.

`A_FIRED_FALSIFIER_IS_A_SUCCESS_OF_THE_METHOD`: ولم يُكتَب شرطُ الإبطال ليُزيَّن
به، فإطلاقُه وإسقاطُه دعوًى منّا هو ما كان يُرجى منه. ولو أُخفي لبقي الاختزالُ
يُقرأ أقوى ممّا هو.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from .closure_window_reduction import (
    CLOSURE_THRESHOLD,
    TEMPLATES,
    WHAT_WOULD_FALSIFY_THE_REDUCTION,
    derive_closure_readouts,
    window_saturation,
)
from .slgae_deposit import SlgaeDepositError

__all__ = [
    "A_FIRED_FALSIFIER_IS_A_SUCCESS_NOTE",
    "CANDIDATES",
    "FALSIFIER_INDEX",
    "IDENTIFIABILITY_NAMED_RESIDUALS",
    "SEPARATING_ONSET",
    "THE_BARRIER_IS_STRUCTURAL_NOTE",
    "THE_FOURTH_FALSIFIER_FIRES_NOTE",
    "THIS_WEAKENS_A_PHRASE_NOTE",
    "WHAT_FALLS_IS_THE_SPECIALIZATION_NOTE",
    "CandidateConstraint",
    "CandidateVerdict",
    "IdentifiabilityReading",
    "SeparatingConfiguration",
    "derive_candidate_verdicts",
    "derive_identifiability",
    "derive_separating_configuration",
    "feature_space",
    "s_and_mu_agree_everywhere",
    "target_partition",
]

FALSIFIER_INDEX: Final[int] = 3
"""موضعُ الشرط المُنفَّذ في `WHAT_WOULD_FALSIFY_THE_REDUCTION` (الرابع، صفريًّا)."""

SEPARATING_ONSET: Final[int] = 2
"""أدنى عددِ بداياتٍ يفرّق بين `s` و`μ`؛ والعربيّةُ لا تُرخّصه."""


def feature_space() -> tuple[tuple[int, int], ...]:
    """فضاءُ الوصف (إغلاق، طول) مُشتَقًّا من القوالب المُودَعة لا مكتوبًا."""

    return tuple(sorted({(row.coda, row.long_nucleus) for row in TEMPLATES}))


def target_partition() -> dict[str, bool]:
    """القسمةُ الهدفُ مقروءةً من تشغيل الاختزال، لا مكتوبةً هنا."""

    return {item.name: item.closes for item in derive_closure_readouts()}


@dataclass(frozen=True, slots=True)
class CandidateConstraint:
    """قيدٌ مرشَّحٌ: اسمُه، وصيغتُه، وأيقوم على عدّ السواكن أم لا."""

    name: str
    formula: str
    counts_consonants: bool
    predicate: Callable[[int, int], bool]

    def __post_init__(self) -> None:
        if not self.formula.strip():
            raise SlgaeDepositError("قيدٌ بلا صيغةٍ مكتوبةٍ لا يُفحَص.")


CANDIDATES: Final[tuple[CandidateConstraint, ...]] = (
    CandidateConstraint(
        name="عدُّ سواكن النافذة",
        formula="s = إغلاق + طول ≤ 1",
        counts_consonants=True,
        predicate=lambda coda, long: coda + long <= CLOSURE_THRESHOLD,
    ),
    CandidateConstraint(
        name="الوزنُ المُوريّ",
        formula="μ = 1 + طول + إغلاق ≤ 2",
        counts_consonants=False,
        predicate=lambda coda, long: 1 + long + coda <= 2,
    ),
    CandidateConstraint(
        name="طولُ القافية",
        formula="نواةٌ + إغلاقٌ ≤ 2",
        counts_consonants=False,
        predicate=lambda coda, long: 1 + long + coda <= 2,
    ),
    CandidateConstraint(
        name="طولُ المقطع بالمقاطع الصوتيّة",
        formula="بدايةٌ + نواةٌ + إغلاقٌ ≤ 3",
        counts_consonants=False,
        predicate=lambda coda, long: 2 + long + coda <= 3,
    ),
    CandidateConstraint(
        name="حدُّ الإغلاق وحدَه",
        formula="إغلاق ≤ 1",
        counts_consonants=True,
        predicate=lambda coda, _long: coda <= 1,
    ),
    CandidateConstraint(
        name="قِصَرُ النواة وحدَه",
        formula="طول = 0",
        counts_consonants=False,
        predicate=lambda _coda, long: long == 0,
    ),
    CandidateConstraint(
        name="وزنٌ يُثقِل الطولَ ضِعفين",
        formula="إغلاق + 2×طول ≤ 2",
        counts_consonants=True,
        predicate=lambda coda, long: coda + 2 * long <= 2,
    ),
    CandidateConstraint(
        name="أكبرُ الحدّين",
        formula="max(إغلاق، طول) ≤ 1",
        counts_consonants=True,
        predicate=lambda coda, long: max(coda, long) <= 1,
    ),
)
"""المرشّحاتُ المُعدَّدة، بعضُها يعدّ السواكنَ وبعضُها لا."""


@dataclass(frozen=True, slots=True)
class CandidateVerdict:
    """حكمُ مرشَّحٍ: أيُعيد القسمةَ، وأين يختلف إن اختلف."""

    name: str
    counts_consonants: bool
    reproduces_partition: bool
    divergences: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.reproduces_partition != (not self.divergences):
            raise SlgaeDepositError(
                "حكمٌ يخالف مواضعَ اختلافه؛ ومرشَّحٌ «يُعيد القسمة» مع "
                "اختلافٍ مسجَّلٍ حكمٌ لا يُشتَقّ."
            )


def derive_candidate_verdicts() -> tuple[CandidateVerdict, ...]:
    """شغِّل كلَّ مرشَّحٍ على القوالب وقابِلْه بالقسمة الهدف."""

    target = target_partition()
    verdicts: list[CandidateVerdict] = []
    for candidate in CANDIDATES:
        divergences = tuple(
            row.name
            for row in TEMPLATES
            if candidate.predicate(row.coda, row.long_nucleus) != target[row.name]
        )
        verdicts.append(
            CandidateVerdict(
                name=candidate.name,
                counts_consonants=candidate.counts_consonants,
                reproduces_partition=not divergences,
                divergences=divergences,
            )
        )
    return tuple(verdicts)


def s_and_mu_agree_everywhere(max_coda: int = 8) -> bool:
    """أتتّفق `s ≤ 1` و`μ ≤ 2` على فضاءٍ أوسعَ من القوالب الستّة؟

    والفحصُ يُجرى على مدًى أوسعَ عمدًا: اتّفاقٌ على ستّة قوالبَ اتّفاقُ عيّنة،
    واتّفاقٌ على المدى كلِّه يجعلهما دالّةً واحدةً لا قيدين.
    """

    if max_coda < 2:
        raise SlgaeDepositError("المدى يتجاوز القوالبَ المُودَعة، فلا يقلّ عن اثنين.")
    return all(
        (coda + long <= CLOSURE_THRESHOLD) == (1 + long + coda <= 2)
        for coda in range(max_coda + 1)
        for long in (0, 1)
    )


@dataclass(frozen=True, slots=True)
class IdentifiabilityReading:
    """حصادُ التعديد: كم مرشَّحًا أعاد القسمة، وكم منها لا يعدّ السواكن."""

    candidates: int
    reproducing: tuple[str, ...]
    reproducing_without_counting: tuple[str, ...]
    falsifier_text: str

    @property
    def falsifier_fires(self) -> bool:
        """أفَعَل الشرطُ الرابع؟ مُشتَقٌّ من وجود مرشَّحٍ لا يعدّ السواكن."""

        return bool(self.reproducing_without_counting)

    @property
    def specialization_is_identifiable(self) -> bool:
        """أيتعيّن العاملُ بهذه البيانات؟ لا، إن أعاد القسمةَ أكثرُ من واحد."""

        return len(self.reproducing) == 1


def derive_identifiability() -> IdentifiabilityReading:
    """أخرِج الحصادَ، ونصَّ الشرط المُنفَّذ معه لا مفصولًا عنه."""

    verdicts = derive_candidate_verdicts()
    reproducing = tuple(item.name for item in verdicts if item.reproduces_partition)
    without = tuple(
        item.name
        for item in verdicts
        if item.reproduces_partition and not item.counts_consonants
    )
    return IdentifiabilityReading(
        candidates=len(verdicts),
        reproducing=reproducing,
        reproducing_without_counting=without,
        falsifier_text=WHAT_WOULD_FALSIFY_THE_REDUCTION[FALSIFIER_INDEX],
    )


@dataclass(frozen=True, slots=True)
class SeparatingConfiguration:
    """الموضعُ الذي يفصل المقياسَين، وسببُ تعذّره في العربيّة."""

    onset_count: int
    separates: bool
    why_unavailable: str
    licensed_onset_count: int

    def __post_init__(self) -> None:
        if self.onset_count <= self.licensed_onset_count:
            raise SlgaeDepositError(
                "الموضعُ الفاصلُ يتجاوز ما تُرخّصه اللغة؛ وموضعٌ مرخَّصٌ " "لا يكون متعذّرًا."
            )


def derive_separating_configuration() -> SeparatingConfiguration:
    """اقرأ الموضعَ الفاصلَ بالتشغيل: بدايتان تُغيّران `s` ولا تُغيّران `μ`."""

    at_one = [
        window_saturation(row.coda, row.long_nucleus, following_onset=1)
        for row in TEMPLATES
    ]
    at_two = [
        window_saturation(row.coda, row.long_nucleus, following_onset=SEPARATING_ONSET)
        for row in TEMPLATES
    ]
    return SeparatingConfiguration(
        onset_count=SEPARATING_ONSET,
        separates=at_one != at_two,
        why_unavailable=(
            "قانونُ الحواف يُرخّص بدايةً واحدةً للمقطع؛ فالعنقودُ في البداية "
            "غيرُ واقعٍ في العربيّة، والموضعُ الفاصلُ غيرُ متاحٍ فيها"
        ),
        licensed_onset_count=1,
    )


THE_FOURTH_FALSIFIER_FIRES_NOTE: Final[str] = (
    "TheFourthFalsifierFires: أربعةُ مرشّحاتٍ تُعطي القسمةَ نفسَها بلا خطأٍ "
    "في قالبٍ واحد، وفيها ثلاثةٌ لا تعدّ السواكن؛ فالقسمةُ لا تُعيّن العامل"
)

THE_BARRIER_IS_STRUCTURAL_NOTE: Final[str] = (
    "TheIdentifiabilityBarrierIsStructuralNotEmpirical: الموضعُ الوحيدُ الفاصلُ "
    "عنقودٌ في البداية، وقانونُ الحواف يمنعه؛ فالمانعُ بنيةُ اللغة لا قلّةُ "
    "بيانٍ تُسَدُّ بمدوّنةٍ أوسع"
)

WHAT_FALLS_IS_THE_SPECIALIZATION_NOTE: Final[str] = (
    "WhatFallsIsTheSpecializationNotThePartition: الساقطُ أنّ عدَّ السواكن "
    "بعينه هو العامل؛ والباقي القسمةُ نفسُها، وأنّ العاملَ دالّةٌ على "
    "(إغلاق، طول) بحدٍّ واحدٍ في صنفِ تكافؤٍ من أربعة"
)

THIS_WEAKENS_A_PHRASE_NOTE: Final[str] = (
    "ThisWeakensAPhraseInTheDocument: «العدد فراكتالي، والنوع معجمي» تحمل من "
    "التخصيص ما لا يقوم عليه دليلٌ ههنا، إذ «العدد» قد يكون «الوزن» بلا فرقٍ "
    "مرصود؛ فيُضيَّق مدلولُها ولا تُبطَل"
)

A_FIRED_FALSIFIER_IS_A_SUCCESS_NOTE: Final[str] = (
    "AFiredFalsifierIsASuccessOfTheMethod: شرطُ الإبطال لم يُكتَب ليُزيَّن به، "
    "فإطلاقُه وإسقاطُه دعوًى منّا هو ما كان يُرجى منه؛ ولو أُخفي لبقي "
    "الاختزالُ يُقرأ أقوى ممّا هو"
)

IDENTIFIABILITY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_FOURTH_FALSIFIER_FIRES_NOTE,
    THE_BARRIER_IS_STRUCTURAL_NOTE,
    WHAT_FALLS_IS_THE_SPECIALIZATION_NOTE,
    THIS_WEAKENS_A_PHRASE_NOTE,
    A_FIRED_FALSIFIER_IS_A_SUCCESS_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(WHAT_WOULD_FALSIFY_THE_REDUCTION) <= FALSIFIER_INDEX:  # pragma: no cover
    raise RuntimeError(
        "موضعُ الشرط المُنفَّذ خارجَ قائمة شروط الإبطال؛ وتنفيذُ شرطٍ لا "
        "يُشار إليه تنفيذٌ لغير المكتوب."
    )
