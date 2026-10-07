"""فحصُ أرقامِ مصنَّفِ الحركة: ما يُعاد اشتقاقُه، وما يُعارِض الشجرة، وما لا يُفحَص.

**الوارد**: تقريرُ تحقّقٍ من محادثةٍ أخرى على مصنَّفٍ لم يصل إلى هذه الشجرة، فيه
أربعُ «بطّاريّات» ثلاثٌ منها ✅ ورابعةٌ غيرُ حاسمة، ودعوى `Root_Slots` بأربعة
آلافٍ وخمسِ مئةٍ واثنين وستّين صفًّا، واثنين وثلاثين حاملًا، ومئةٍ وثمانٍ
وعشرين حالة.

`A_GREEN_BATTERY_OVER_DERIVED_COLUMNS_IS_NOT_EVIDENCE`: أكثرُ فحوص البطّاريّة
الأولى **لا يمكن أن تسقط**: إن كان `Total_Carrier_Count` محسوبًا مجموعَ
`C1+C2+C3` فمساواتُه إيّاه تعريفٌ لا خبر، وكذلك «صفوفُ الحركات الأربعُ تتشارك
عددَ الخانات» إن كانت مضمومةً بالحامل، و«غيرُ المشاهَد صفرٌ في كلّ الأعمدة» إن
كان الصفرُ هو تعريفَ غيرِ المشاهَد. فخضرةُ هذه الفحوص تُخبِر عن صيغِ المصنَّف
لا عن العربيّة. والقابلُ للسقوط منها ما كان **متفاوتةً** لا مساواة.

`FOUR_THOUSAND_FIVE_HUNDRED_SIXTY_TWO_IS_A_POLICY_NOT_A_FACT`: العددُ يُعاد
اشتقاقُه من البايتات المُودَعة بالضبط، لكنّه **يضمّ ثلاثةَ أنواعٍ تفصلها قاعدةُ
العدّ المُودَعة**: ثلاثيٌّ (4,087) ومضاعفٌ (419) وثلاثيٌّ معتلٌّ (56). وعددُ
الشجرة المُجمَّد للثلاثيّ **4,087**. وليس هذا تدقيقًا لفظيًّا: قِيس في هذه
الشجرة أنّ ضمَّ المضاعف **يقلب حكمًا** في خليّة `C2C3` من كبتٍ (0.170) إلى
تخمةٍ (2.354). فسلسلةُ مركوف المدرَّبةُ على 4,562 مدرَّبةٌ على مجتمعٍ مخلوطٍ لم
تُعلَن سياستُه.

`THIRTY_TWO_CARRIERS_ARE_SEATS_NOT_LETTERS`: الحواملُ الاثنان والثلاثون يُعادان
اشتقاقًا، لكنّ الطيَّ المُودَع (`fold_root`) يردّها **تسعةً وعشرين**: فـ`أ` و`ئ`
و`ء` مقاعدُ همزةٍ لا حروفٌ متمايزة، و`ى` صورةُ `ي`. فالفضاءُ 128 = 32×4 يصير
116 = 29×4، وما سمّاه التقريرُ «أثرَ هُويّةٍ» في `أ-K` هو هذا بعينه — مقيسًا
لا موصوفًا.

`THE_DENOMINATOR_GAP_IS_THE_FINDING_THAT_COULD_HAVE_FAILED`: فجوةُ المقامات
(77,783 مقابل 77,411 و77,403) خبرٌ حقيقيّ: 372 و380. وهي الشيءُ الوحيدُ في
التقرير الذي **كان يمكن أن يخرج سليمًا فخرج معطوبًا**.

`A_PARSER_DEFECT_IS_NOT_A_NULL_RESULT`: إعلانُ البطّاريّة الرابعة عطبًا في
أداتها لا نتيجةً في المصنَّف **صوابٌ يُحسَب لها**؛ والستّةُ والثمانون «اختلافًا»
لا تُقيَّد شيئًا: لا شاهدًا ولا نفيًا.

`THE_WORKBOOK_DID_NOT_ARRIVE`: كلُّ ما ههنا مُعادٌ من بايتات الشجرة. ودعاوى
المصنَّف الداخليّة (تطابقُ كلّ حاملٍ مع المصفوفة، ومجاميعُ `Function_Evidence`)
**غيرُ مفحوصةٍ** — لا مؤكَّدةٌ ولا مردودة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Final

from .letter_fingerprint import fold_root
from .maqayis_root_table_deposit import (
    REDERIVED_DISTINCT_TRILATERAL_ROOTS,
    read_root_table_bytes,
)

__all__ = [
    "A_GREEN_BATTERY_OVER_DERIVED_COLUMNS_IS_NOT_EVIDENCE_NOTE",
    "A_PARSER_DEFECT_IS_NOT_A_NULL_RESULT_NOTE",
    "CarrierCensus",
    "CheckKind",
    "ClaimVerdict",
    "FOUR_THOUSAND_FIVE_HUNDRED_SIXTY_TWO_IS_A_POLICY_NOT_A_FACT_NOTE",
    "REPORTED_BATTERY_ONE_CHECKS",
    "REPORTED_FIGURES",
    "THE_DENOMINATOR_GAP_IS_THE_FINDING_THAT_COULD_HAVE_FAILED_NOTE",
    "THE_WORKBOOK_DID_NOT_ARRIVE_NOTE",
    "THIRTY_TWO_CARRIERS_ARE_SEATS_NOT_LETTERS_NOTE",
    "WORKBOOK_CROSSCHECK_NAMED_RESIDUALS",
    "WorkbookCrosscheckError",
    "carrier_census",
    "check_reported_arithmetic",
    "derive_denominator_gap",
    "falsifiable_check_share",
    "population_decomposition",
    "read_claim_verdicts",
]


class WorkbookCrosscheckError(ValueError):
    """رُفض مدخلٌ أو قراءةٌ ناقصة؛ ولا يُحمَل على أقرب مقبول."""


class ClaimVerdict(Enum):
    """منازلُ الدعوى الواردة، مغلقةً: ولا منزلةَ اسمُها «على الأرجح صحيح»."""

    REPRODUCED = "أُعيد اشتقاقُه"
    CONFLICTS_WITH_THE_TREE = "يعارض عدَّ الشجرة"
    NOT_VERIFIABLE_HERE = "لا يُفحَص ههنا"


class CheckKind(Enum):
    """نوعُ الفحص: ما يمكن أن يسقط، وما هو تعريفٌ لا يسقط."""

    FALSIFIABLE = "قابلٌ للسقوط"
    DEFINITIONAL = "تعريفيٌّ لا يسقط"


@dataclass(frozen=True, slots=True)
class ReportedFigures:
    """أرقامُ التقرير بنصّها، مُقيَّدةً كي تُقارَن لا كي تُصدَّق."""

    root_slot_rows: int = 4_562
    carriers: int = 32
    states: int = 128
    movement_f: int = 127_430
    movement_d: int = 39_123
    movement_k: int = 42_594
    movement_s: int = 43_599
    explicit_total: int = 252_746
    unmarked: int = 68_320
    grand_total: int = 321_066
    inferred_not_written: int = 17_957
    segment_aligned: int = 75_365
    segment_denominator: int = 77_783
    surface_tokens: int = 77_411
    lexical_aligned: int = 77_403
    unobserved_states: int = 8

    def __post_init__(self) -> None:
        if self.carriers * 4 != self.states:
            raise WorkbookCrosscheckError(
                "الحالاتُ حاصلُ ضربِ الحواملِ في الحركات الأربع؛ فإن لم تكن "
                "كذلك فالعددان ليسا من فضاءٍ واحد."
            )


REPORTED_FIGURES: Final[ReportedFigures] = ReportedFigures()
"""ما ورد، محفوظًا بنصّه؛ فالمقارنةُ تحتاج الأصلَ لا إعادةَ صياغته."""


@dataclass(frozen=True, slots=True)
class PopulationDecomposition:
    """تفكيكُ 4,562 إلى أنواعِ الجذر التي تفصلها قاعدةُ العدّ المُودَعة."""

    total_distinct_length_three: int
    sound_trilateral: int
    doubled: int
    weak_trilateral: int
    tree_frozen_trilateral: int

    def __post_init__(self) -> None:
        parts = self.sound_trilateral + self.doubled + self.weak_trilateral
        if parts != self.total_distinct_length_three:
            raise WorkbookCrosscheckError(
                f"التفكيكُ لا يجمع إلى الكلّ: {parts} ≠ "
                f"{self.total_distinct_length_three}؛ ولا يُقرَّب."
            )

    @property
    def merged_beyond_the_frozen_rule(self) -> int:
        """كم جذرًا يزيده عدُّ التقرير على عدّ الشجرة المُجمَّد، مُشتَقًّا."""

        return self.total_distinct_length_three - self.tree_frozen_trilateral

    @property
    def verdict(self) -> ClaimVerdict:
        """العددُ يُعاد اشتقاقُه، لكنّه يعارض قاعدةَ العدّ المُجمَّدة."""

        return (
            ClaimVerdict.CONFLICTS_WITH_THE_TREE
            if self.merged_beyond_the_frozen_rule
            else ClaimVerdict.REPRODUCED
        )


@dataclass(frozen=True, slots=True)
class CarrierCensus:
    """الحواملُ خامًا وبعد الطيّ المُودَع، والحالاتُ المشتقّةُ منهما."""

    raw_carriers: int
    folded_carriers: int
    seats_folded_away: tuple[str, ...]

    @property
    def raw_states(self) -> int:
        """فضاءُ الحالات كما في التقرير: حاملٌ × أربعُ حركات."""

        return self.raw_carriers * 4

    @property
    def folded_states(self) -> int:
        """الفضاءُ بعد ردّ مقاعد الهمزة وصورة الياء."""

        return self.folded_carriers * 4


@lru_cache(maxsize=1)
def _length_three_rows() -> tuple[tuple[str, str], ...]:
    text = read_root_table_bytes().decode("utf-8")
    return tuple(
        (row["root_full"], row["root_type"])
        for row in csv.DictReader(text.splitlines())
        if len(row["root_full"]) == 3
    )


def population_decomposition() -> PopulationDecomposition:
    """فكِّك 4,562 من البايتات المُودَعة، وقابِله بعدّ الشجرة المُجمَّد."""

    rows = _length_three_rows()
    distinct = {root for root, _type in rows}
    by_type: dict[str, set[str]] = {}
    for root, root_type in rows:
        by_type.setdefault(root_type, set()).add(root)
    return PopulationDecomposition(
        total_distinct_length_three=len(distinct),
        sound_trilateral=len(by_type.get("ثلاثي", set())),
        doubled=len(by_type.get("مضاعف", set())),
        weak_trilateral=len(by_type.get("ثلاثي معتل", set())),
        tree_frozen_trilateral=REDERIVED_DISTINCT_TRILATERAL_ROOTS,
    )


def carrier_census() -> CarrierCensus:
    """احصِ الحواملَ خامًا وبعد الطيّ المُودَع، وسمِّ المقاعدَ المطويّة."""

    rows = _length_three_rows()
    raw = {letter for root, _type in rows for letter in root}
    folded = {letter for root, _type in rows for letter in fold_root(root)}
    return CarrierCensus(
        raw_carriers=len(raw),
        folded_carriers=len(folded),
        seats_folded_away=tuple(sorted(raw - folded)),
    )


def check_reported_arithmetic() -> dict[str, bool]:
    """افحص ما يُفحَص من حسابِ التقرير بالأعداد وحدَها."""

    figures = REPORTED_FIGURES
    movements = (
        figures.movement_f
        + figures.movement_d
        + figures.movement_k
        + figures.movement_s
    )
    return {
        "F+D+K+S = الصريح": movements == figures.explicit_total,
        "الصريح + غير المعلَّم = الكلّ": (
            figures.explicit_total + figures.unmarked == figures.grand_total
        ),
        "المستنتَج ≤ غير المعلَّم": figures.inferred_not_written <= figures.unmarked,
        "المحاذى ≤ مقامه": figures.segment_aligned <= figures.segment_denominator,
        "مقامُ المقاطع ≤ فضاء الرموز": (
            figures.segment_denominator <= figures.surface_tokens
        ),
    }


def derive_denominator_gap() -> tuple[int, int]:
    """فجوةُ المقامات: ما يزيده مقامُ المقاطع على الرموز وعلى المحاذى معجميًّا."""

    figures = REPORTED_FIGURES
    return (
        figures.segment_denominator - figures.surface_tokens,
        figures.segment_denominator - figures.lexical_aligned,
    )


REPORTED_BATTERY_ONE_CHECKS: Final[tuple[tuple[str, CheckKind], ...]] = (
    ("C1+C2+C3 = مجموعُ الحامل", CheckKind.DEFINITIONAL),
    ("سابقة+جذع+لاحقة = المحاذى", CheckKind.DEFINITIONAL),
    ("غيرُ طرفيٍّ + طرفيّ = المحاذى", CheckKind.DEFINITIONAL),
    ("مطابقاتُ النحو/البناء/الإعراب ≤ المحاذى", CheckKind.FALSIFIABLE),
    ("المحاذى ≤ الصريح", CheckKind.FALSIFIABLE),
    ("غيرُ المشاهَد صفرٌ في الأعمدة الثلاثةَ عشرَ", CheckKind.DEFINITIONAL),
    ("صفوفُ الحركات الأربعُ تتشارك عددَ الخانات", CheckKind.DEFINITIONAL),
)
"""تصنيفُ فحوص البطّاريّة الأولى: أيُّها كان يمكن أن يسقط، وأيُّها تعريف."""


def falsifiable_check_share() -> tuple[int, int]:
    """كم من فحوص البطّاريّة الأولى كان يمكن أن يسقط، من كم."""

    falsifiable = sum(
        1
        for _name, kind in REPORTED_BATTERY_ONE_CHECKS
        if kind is CheckKind.FALSIFIABLE
    )
    return falsifiable, len(REPORTED_BATTERY_ONE_CHECKS)


def read_claim_verdicts() -> dict[str, ClaimVerdict]:
    """أحكامُ الدعاوى الواردة، كلٌّ بما يقابله في الشجرة."""

    census = carrier_census()
    figures = REPORTED_FIGURES
    return {
        "Root_Slots = 4,562": population_decomposition().verdict,
        "الحواملُ 32": (
            ClaimVerdict.REPRODUCED
            if census.raw_carriers == figures.carriers
            else ClaimVerdict.CONFLICTS_WITH_THE_TREE
        ),
        "الفضاءُ 128 حالةً": (
            ClaimVerdict.REPRODUCED
            if census.raw_states == figures.states
            else ClaimVerdict.CONFLICTS_WITH_THE_TREE
        ),
        "مجاميعُ Function_Evidence": ClaimVerdict.NOT_VERIFIABLE_HERE,
        "تطابقُ كلّ حاملٍ مع المصفوفة": ClaimVerdict.NOT_VERIFIABLE_HERE,
        "البطّاريّةُ الرابعة": ClaimVerdict.NOT_VERIFIABLE_HERE,
    }


A_GREEN_BATTERY_OVER_DERIVED_COLUMNS_IS_NOT_EVIDENCE_NOTE: Final[str] = (
    "AGreenBatteryOverDerivedColumnsIsNotEvidence: مساواةُ عمودٍ لمجموع أعمدةٍ "
    "حُسِب منها تعريفٌ لا يسقط؛ فخمسةٌ من سبعةِ فحوصٍ في البطّاريّة الأولى تخبر "
    "عن صيغِ المصنَّف لا عن العربيّة، والقابلُ للسقوط متفاوتتان"
)

FOUR_THOUSAND_FIVE_HUNDRED_SIXTY_TWO_IS_A_POLICY_NOT_A_FACT_NOTE: Final[str] = (
    "FourThousandFiveHundredSixtyTwoIsAPolicyNotAFact: العددُ يُعاد اشتقاقُه "
    "بالضبط، لكنّه يضمّ ثلاثيًّا (4,087) ومضاعفًا (419) ومعتلًّا (56) تفصلها "
    "قاعدةُ العدّ المُودَعة؛ وضمُّ المضاعف قُلِب به حكمُ C2C3 في هذه الشجرة من "
    "0.170 كبتًا إلى 2.354 تخمةً، فالمجتمعُ المخلوطُ ليس تفصيلًا"
)

THIRTY_TWO_CARRIERS_ARE_SEATS_NOT_LETTERS_NOTE: Final[str] = (
    "ThirtyTwoCarriersAreSeatsNotLetters: الطيُّ المُودَع يردّ 32 حاملًا إلى 29، "
    "فيصير الفضاءُ 116 لا 128؛ وما سمّاه التقريرُ «أثرَ هُويّة» في أ-K هو هذا "
    "مقيسًا"
)

THE_DENOMINATOR_GAP_IS_THE_FINDING_THAT_COULD_HAVE_FAILED_NOTE: Final[str] = (
    "TheDenominatorGapIsTheFindingThatCouldHaveFailed: 77,783 يتجاوز فضاءَ "
    "الرموز 77,411 بـ372 والمحاذى معجميًّا 77,403 بـ380؛ وهو الشيءُ الوحيدُ "
    "الذي كان يمكن أن يخرج سليمًا فخرج معطوبًا"
)

A_PARSER_DEFECT_IS_NOT_A_NULL_RESULT_NOTE: Final[str] = (
    "AParserDefectIsNotANullResult: إعلانُ البطّاريّة الرابعة عطبَ أداتها لا "
    "نتيجةً في المصنَّف صوابٌ يُحسَب لها؛ والستّةُ والثمانون «اختلافًا» لا تُقيَّد "
    "شاهدًا ولا نفيًا"
)

THE_WORKBOOK_DID_NOT_ARRIVE_NOTE: Final[str] = (
    "TheWorkbookDidNotArrive: كلُّ ما ههنا مُعادٌ من بايتات الشجرة، ودعاوى "
    "المصنَّف الداخليّةُ غيرُ مفحوصةٍ — لا مؤكَّدةٌ ولا مردودة"
)

WORKBOOK_CROSSCHECK_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_GREEN_BATTERY_OVER_DERIVED_COLUMNS_IS_NOT_EVIDENCE_NOTE,
    FOUR_THOUSAND_FIVE_HUNDRED_SIXTY_TWO_IS_A_POLICY_NOT_A_FACT_NOTE,
    THIRTY_TWO_CARRIERS_ARE_SEATS_NOT_LETTERS_NOTE,
    THE_DENOMINATOR_GAP_IS_THE_FINDING_THAT_COULD_HAVE_FAILED_NOTE,
    A_PARSER_DEFECT_IS_NOT_A_NULL_RESULT_NOTE,
    THE_WORKBOOK_DID_NOT_ARRIVE_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


# يُفحَص عند كلّ استيراد: منازلُ الحكم مغلقةٌ، والتفكيكُ يجمع إلى كلّه.
if len(ClaimVerdict) != 3:  # pragma: no cover - حارس
    raise RuntimeError("منازلُ الدعوى ثلاثٌ مغلقةٌ؛ ولا «على الأرجح صحيح» فيها.")
if len(CheckKind) != 2:  # pragma: no cover - حارس
    raise RuntimeError("الفحصُ إمّا قابلٌ للسقوط وإمّا تعريفٌ؛ ولا ثالثَ.")
if len(REPORTED_BATTERY_ONE_CHECKS) != 7:  # pragma: no cover - حارس
    raise RuntimeError("فحوصُ البطّاريّة الأولى سبعةٌ كما وردت.")
