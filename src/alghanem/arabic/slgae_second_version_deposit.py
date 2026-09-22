"""النسخةُ الثانية من SLGAE: مراتبُ ادّعائها، ومواضعُ تقييدها، وتدقيقُ جدول ماركوف.

**ما تفعله هذه الوحدة**: تُودِع بايتاتِ النسخة الثانية مُبصَّمةً إلى جانب
الأولى — لا بدلًا منها — وتُسجّل ما قيّدته، ثمّ **تُدقّق جدولَ ماركوف في
القسم ٥ي داخليًّا**: أيُّ أعمدته يُعيد بناءَ أيّ، وأيُّها لا يُبنى من
المنشور.

`A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED`: النسختان تُودَعان معًا. وإيداعُ
الموسَّعة وحدها يُخفي أنّ دعوًى أُطلِقت ثمّ قُيِّدت، فتُقرأ الوثيقةُ بعد
جلساتٍ كأنّها لم تتغيّر — ويضيع أنفسُ ما فيها: **مواضعُ التقييد**.

`THE_AUTHORS_OWN_TIERING_IS_THE_STRONGEST_THING_IN_THE_SECOND_VERSION`: أنفسُ
ما جاءت به النسخةُ الثانية ليس قسمًا جديدًا، بل جدولُ مراتبِ الادّعاء الذي
يُنزِل بيدِ صاحبه ما كان مُطلَقًا في الأولى: أربعُ مراتبَ، ثلاثٌ منها ليست
«ثبت باختبار مستقلّ». وتُسجَّل هنا كما وردت، ولا تُرفَع مرتبةٌ ولا تُخفَض.

`THE_TWENTY_SIX_ARE_A_DECLARED_CHOICE_NOT_A_BIRTH`: قائمةُ الصوامت الستّةِ
والعشرين مُصنَّفةٌ في النسخة الثانية «اختيارٌ منّي». وهذا يمسّ ما قيس في
`slgae_deposit` مباشرةً: التعارضُ 26/28 لم يَعُد تعارضَ مولودٍ بمُجمَّد، بل
تعارضُ **اختيارٍ مُعلَنٍ** بمُجمَّدٍ مُبصَّم. والقياسُ لا يتغيّر بذلك، لكنّ
قراءتَه تتغيّر.

`AN_INTERNAL_AUDIT_IS_NOT_A_REDERIVATION`: ما يجري هنا على جدول ماركوف تدقيقُ
**اتّساقٍ داخليّ** بين أعمدةٍ منشورة، لا إعادةَ اشتقاقٍ من مدوّنة. فلا
بايتاتِ QAC في مسار هذا الملفّ، ولا يُقال هنا إنّ رقمًا صوابٌ أو خطأ: يُقال
ما يُبنى من المنشور وما لا يُبنى، وما يلزم ليُبنى.

`ROUNDING_IS_A_CANDIDATE_EXPLANATION_NAMED_BEFORE_THE_VERDICT`: الأعمدةُ
منشورةٌ بمنزلتين، فمجالُ التقريب يُحسَب أوّلًا ويُقارَن به الفرق. فمن أعلن
فرقًا قبل أن يحسب مجالَ تقريبه أعلن أثرَ التقريب خلافًا.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from itertools import pairwise
from pathlib import Path
from typing import Final

from alghanem.canonical_content import canonical_digest

from .slgae_deposit import SLGAE_RELATIVE_PATH, SlgaeDepositError, slgae_digest

__all__ = [
    "AN_INTERNAL_AUDIT_IS_NOT_A_REDERIVATION_NOTE",
    "A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE",
    "CLAIM_TIERS",
    "MARKOV_LEVELS",
    "PUBLISHED_DECIMALS",
    "REPORTED_GAMMA_OVER_BETA",
    "ROUNDING_IS_A_CANDIDATE_EXPLANATION_NOTE",
    "SECOND_VERSION_AMENDMENTS",
    "SLGAE_V2_RELATIVE_PATH",
    "SLGAE_V2_NAMED_RESIDUALS",
    "THE_AUTHORS_OWN_TIERING_IS_THE_STRONGEST_THING_NOTE",
    "THE_TWENTY_SIX_ARE_A_DECLARED_CHOICE_NOTE",
    "ClaimTier",
    "LambdaReconstruction",
    "MarkovAuditReading",
    "MarkovLevelRow",
    "RatioCheck",
    "TieredClaim",
    "VersionAmendment",
    "both_version_digests",
    "derive_lambda_reconstructions",
    "derive_ratio_checks",
    "markov_audit",
    "slgae_v2_digest",
    "slgae_v2_path",
]

SLGAE_V2_RELATIVE_PATH: Final[str] = "docs/reference/slgae_slot_licensing_algebra_v2.md"

PUBLISHED_DECIMALS: Final[int] = 2
"""عددُ المنازل التي نُشرت بها أعمدةُ الجدول؛ ومنه يُحسَب مجالُ التقريب."""

REPORTED_GAMMA_OVER_BETA: Final[float] = 1.55
"""النسبةُ المذكورة في ٥ي: «γ/β ≈ 1.55 ثابت»."""


class ClaimTier(Enum):
    """مراتبُ الادّعاء الأربعُ كما سمّاها صاحبُ الوثيقة، لا كما نُصنّفها."""

    INDEPENDENT_TEST = "ثبت باختبار مستقل"
    CIRCULAR = "دائري"
    NEAR_DEFINITIONAL = "قريب من التعريف"
    AUTHORS_CHOICE = "اختيار مني"


@dataclass(frozen=True, slots=True)
class TieredClaim:
    """ادّعاءٌ بمرتبته كما وردت، وبنصّ معنى المرتبة معه لا مفصولًا عنه."""

    tier: ClaimTier
    tier_meaning: str
    claim: str

    def __post_init__(self) -> None:
        if not self.claim.strip() or not self.tier_meaning.strip():
            raise SlgaeDepositError("ادّعاءٌ بلا نصٍّ أو مرتبةٌ بلا معناها لا يُسجَّل.")


CLAIM_TIERS: Final[tuple[TieredClaim, ...]] = (
    TieredClaim(
        tier=ClaimTier.INDEPENDENT_TEST,
        tier_meaning="تنبؤ مسجّل قبل العدّ، ومقياس لا يعتمد على القاعدة نفسها",
        claim=(
            "كتل المخارج وصفاتها من تجنُّب الجذور (مع تحفّظ: QAC متداخل مع "
            "المقاييس)؛ خط الشمسية لا يقطع كتلة؛ التركيبات الـ19 الممنوعة "
            "غائبة؛ المقاطع فائقة الثقل في الوصل محصورة؛ الفتح بعد إنّ على "
            "النص المشكول؛ الرباعي المكرّر والثلاثي المضعّف"
        ),
    ),
    TieredClaim(
        tier=ClaimTier.CIRCULAR,
        tier_meaning="المقياس وسم بشري وُضع بالقاعدة نفسها",
        claim=(
            "المبني للمجهول «نغمة»؛ حرف المضارعة؛ الإعراب من وسوم QAC؛ "
            "التعريف والتنوين"
        ),
    ),
    TieredClaim(
        tier=ClaimTier.NEAR_DEFINITIONAL,
        tier_meaning="النتيجة مضمونة بكيفية الكتابة أو بتعريف العامل",
        claim="CVV = CV + زمن؛ حياد الألف جزئيًا؛ غياب CVV عن المجرد",
    ),
    TieredClaim(
        tier=ClaimTier.AUTHORS_CHOICE,
        tier_meaning="النتيجة تتبع عوامل أو عتبات سمّاها صاحبُ الوثيقة",
        claim=(
            "«ما يولد وما يُدوَّر» في القوالب والأوزان؛ قائمة الصوامت الـ26؛ "
            "متنبئات نوع الحركة في الإعلال (لاحقة)"
        ),
    ),
)
"""مراتبُ الادّعاء الأربع كما وردت في النسخة الثانية، بلا رفعٍ ولا خفض."""


@dataclass(frozen=True, slots=True)
class VersionAmendment:
    """موضعٌ تغيّر بين النسختين: ما قالته الأولى، وما تقوله الثانية، وما يُقرأ."""

    locus: str
    first_version_said: str
    second_version_says: str
    what_the_tree_reads: str

    def __post_init__(self) -> None:
        if self.first_version_said == self.second_version_says:
            raise SlgaeDepositError(
                "لا يُسجَّل تغيّرٌ حيث لا تغيّر؛ وصفٌّ بلا فرقٍ يُضخّم جدولَ "
                "التغيّرات فيُقرأ تقييدٌ لم يقع."
            )


SECOND_VERSION_AMENDMENTS: Final[tuple[VersionAmendment, ...]] = (
    VersionAmendment(
        locus="مرتبةُ الادّعاء إجمالًا",
        first_version_said="تُعرَض النتائجُ مستويةً بلا تدرّجٍ مُعلَنٍ في قوّتها",
        second_version_says=(
            "أربعُ مراتب، وثلاثٌ منها ليست «ثبت باختبار مستقل»؛ و«العوامل» "
            "في أغلبها تصنيفُ الصرف التراثيّ بأسماءٍ جديدة"
        ),
        what_the_tree_reads=(
            "تقييدٌ صادرٌ عن صاحب الوثيقة نفسِه، وهو أقوى من تقييدٍ يأتي من "
            "خارجها؛ ويُسجَّل كما ورد"
        ),
    ),
    VersionAmendment(
        locus="قائمةُ الصوامت الستّةِ والعشرين",
        first_version_said="«ما لم يولد بعد: قائمة الصوامت الـ26 نفسها»",
        second_version_says="مُصنَّفةٌ صراحةً في مرتبة «اختيار مني»",
        what_the_tree_reads=(
            "التعارضُ 26/28 المقيسُ في `slgae_deposit` يبقى بعدده، وتتغيّر "
            "قراءتُه: طرفاه اختيارٌ مُعلَنٌ وجدولٌ مُبصَّم، لا مولودان"
        ),
    ),
    VersionAmendment(
        locus="٥ط المقولاتُ النحويّة",
        first_version_said="أكثرُ صفوف الجدول محكومٌ عليها بـ«مؤكد»",
        second_version_says=(
            "تصحيحٌ: أغلبُ «المؤكد» دائريٌّ لأنّ وسومَ QAC وضعها معربون "
            "بالقواعد نفسها؛ وأُعيد اختباران على النص المشكول بلا وسوم"
        ),
        what_the_tree_reads=(
            "سحبُ سندٍ عن صفوفٍ بقيت أحكامُها مكتوبةً في الجدول؛ فالجدولُ "
            "والتصحيحُ يُقرآن معًا لا منفصلَين"
        ),
    ),
    VersionAmendment(
        locus="٥ج الفراكتاليّة",
        first_version_said="«العامل واحد، والمدى يتغير» بلا إعلان فشل",
        second_version_says="«ادّعاء الفراكتالية فشل جزئيًا (المدى الهندسي لم يصمد)»",
        what_the_tree_reads="إعلانُ فشلٍ جزئيٍّ يُسجَّل بموضعه ولا يُحمَل على الكلّ",
    ),
    VersionAmendment(
        locus="٥ي ماركوف",
        first_version_said="لا وجودَ للقسم في النسخة الأولى",
        second_version_says=(
            "قسمٌ جديد: نواةُ ماركوف تفصل المنعَ عن التعيين، وP1 وP2 سقطا، "
            "وP2b يُفضَّل على الأنواع ويسقط على الرموز، وP3 تأكّد"
        ),
        what_the_tree_reads=(
            "إضافةٌ لا تقييد؛ وأرقامُها تُدقَّق هنا اتّساقًا داخليًّا لا " "إعادةَ اشتقاق"
        ),
    ),
)
"""مواضعُ التغيّر بين النسختين، كلُّ موضعٍ بما قالته كلُّ نسخةٍ فيه."""


@dataclass(frozen=True, slots=True)
class MarkovLevelRow:
    """صفُّ مستوًى في جدول ٥ي، كما نُشر بمنزلتين.

    و`identity_exp` تكون `None` حين نُشِر «0 مشاهدة»: غيابُ المشاهدة ليس
    قيمةً صفرًا، وقراءتُه صفرًا تُدخِل في الحساب رقمًا لم يُقَس.
    """

    level: str
    same_block_exp: float
    identity_exp: float | None
    reported_lambda: float
    identity_is_unobserved: bool

    def __post_init__(self) -> None:
        if self.same_block_exp <= 0:
            raise SlgaeDepositError("exp(β) موجبٌ، وإلّا فلا لوغاريتم له.")
        if self.identity_is_unobserved != (self.identity_exp is None):
            raise SlgaeDepositError(
                "«لا مشاهدة» تُسجَّل بغياب القيمة لا بصفرٍ بجانبها؛ "
                "وصفرٌ مكتوبٌ يدخل الحسابَ رقمًا لم يُقَس."
            )


MARKOV_LEVELS: Final[tuple[MarkovLevelRow, ...]] = (
    MarkovLevelRow(
        level="L1 الجذر",
        same_block_exp=0.17,
        identity_exp=None,
        reported_lambda=1.0,
        identity_is_unobserved=True,
    ),
    MarkovLevelRow(
        level="L2 الجذع",
        same_block_exp=0.43,
        identity_exp=0.31,
        reported_lambda=0.43,
        identity_is_unobserved=False,
    ),
    MarkovLevelRow(
        level="L3 الحدّ الصرفي",
        same_block_exp=0.70,
        identity_exp=0.59,
        reported_lambda=0.19,
        identity_is_unobserved=False,
    ),
    MarkovLevelRow(
        level="L4 بين الكلمات",
        same_block_exp=1.00,
        identity_exp=0.94,
        reported_lambda=0.01,
        identity_is_unobserved=False,
    ),
)
"""جدولُ ٥ي كما نُشر: عمودا الأثر، وقوّةُ المستوى المذكورةُ في P2b."""


def _rounding_interval(value: float) -> tuple[float, float]:
    half = 0.5 * 10 ** (-PUBLISHED_DECIMALS)
    return value - half, value + half


@dataclass(frozen=True, slots=True)
class LambdaReconstruction:
    """محاولةُ إعادةِ بناء λ من عمود exp(β)، بمجال تقريبه لا بقيمته وحدها."""

    level: str
    reported: float
    derived: float
    difference: float
    interval_low: float
    interval_high: float
    is_anchor: bool

    @property
    def reported_inside_interval(self) -> bool:
        """أيقع المنشورُ داخل مجال التقريب؟ مُشتَقٌّ لا مكتوبٌ في حقل."""

        return self.interval_low <= self.reported <= self.interval_high


def derive_lambda_reconstructions() -> tuple[LambdaReconstruction, ...]:
    """أعِد بناءَ λ من `exp(β)` بفرض `λ(L1) = 1`، وقارِنه بالمنشور بمجاله.

    فإن كان الشكلُ واحدًا والقوّةُ متدرّجةً — كما تقول P2b — فإنّ
    `ln exp(β_k) = λ_k · β`، فتخرج `λ_k` قسمةَ لوغاريتمَين. وهذه القراءةُ
    شرطٌ للتدقيق لا دعوى عن النموذج: نموذجٌ يُقدَّر فيه λ مع β و γ معًا قد
    لا تُعيد أعمدتُه المنشورةُ بناءَ بعضها، وذلك يُسجَّل ولا يُسمّى خطأ.
    """

    anchor = MARKOV_LEVELS[0]
    beta = math.log(anchor.same_block_exp)
    anchor_low, anchor_high = _rounding_interval(anchor.same_block_exp)
    reconstructions: list[LambdaReconstruction] = []
    for row in MARKOV_LEVELS:
        derived = math.log(row.same_block_exp) / beta
        low, high = _rounding_interval(row.same_block_exp)
        corners = [
            math.log(value) / math.log(base)
            for value in (low, high)
            for base in (anchor_low, anchor_high)
        ]
        reconstructions.append(
            LambdaReconstruction(
                level=row.level,
                reported=row.reported_lambda,
                derived=derived,
                difference=derived - row.reported_lambda,
                interval_low=min(corners),
                interval_high=max(corners),
                is_anchor=row is anchor,
            )
        )
    return tuple(reconstructions)


@dataclass(frozen=True, slots=True)
class RatioCheck:
    """قسمةُ `γ/β` في مستوًى، أو سببُ تعذّرها مُسمًّى لا مطويًّا."""

    level: str
    value: float | None
    unavailable_because: str

    def __post_init__(self) -> None:
        if (self.value is None) != bool(self.unavailable_because):
            raise SlgaeDepositError(
                "قيمةٌ بلا سببِ غيابها، أو سببٌ مع قيمةٍ موجودة؛ "
                "والتعذّرُ يُسمّى ولا يُترَك فراغًا."
            )


def derive_ratio_checks() -> tuple[RatioCheck, ...]:
    """احسب `γ/β` حيث يمكن، وسمِّ سببَ التعذّر حيث لا يمكن.

    وتتعذّر في موضعين بطبيعة المنشور: حيث لا مشاهدةَ للتماثل، وحيث
    `exp(β) = 1.00` فلوغاريتمُه صفرٌ ولا تُقسَم عليه.
    """

    checks: list[RatioCheck] = []
    for row in MARKOV_LEVELS:
        if row.identity_exp is None:
            checks.append(
                RatioCheck(
                    level=row.level,
                    value=None,
                    unavailable_because="لا مشاهدةَ للتماثل في هذا المستوى",
                )
            )
            continue
        denominator = math.log(row.same_block_exp)
        if denominator == 0:
            checks.append(
                RatioCheck(
                    level=row.level,
                    value=None,
                    unavailable_because="exp(β) = 1.00 فلوغاريتمُه صفرٌ ولا يُقسَم عليه",
                )
            )
            continue
        checks.append(
            RatioCheck(
                level=row.level,
                value=math.log(row.identity_exp) / denominator,
                unavailable_because="",
            )
        )
    return tuple(checks)


@dataclass(frozen=True, slots=True)
class MarkovAuditReading:
    """حصادُ التدقيق: ما أُعيد بناؤه، وما تعذّر، وما بقي مفتوحًا."""

    levels: int
    anchor_levels: int
    lambdas_inside_rounding: int
    lambdas_outside_rounding: int
    ratio_levels_computable: int
    ratio_levels_unavailable: int
    reported_ratio: float
    same_block_is_monotone_increasing: bool
    reported_lambda_is_monotone_decreasing: bool

    def __post_init__(self) -> None:
        counted = (
            self.lambdas_inside_rounding
            + self.lambdas_outside_rounding
            + self.anchor_levels
        )
        if counted != self.levels:
            raise SlgaeDepositError(
                "مجموعُ المرساة وما وقع داخلَ المجال وخارجَه يخالف عددَ "
                "المستويات؛ والمرساةُ تُعَدُّ وحدَها إذ وقوعُها داخلَه "
                "بالتعريف لا بالفحص."
            )
        if self.ratio_levels_computable + self.ratio_levels_unavailable != self.levels:
            raise SlgaeDepositError("مجموعُ ما حُسِب وما تعذّر يخالف عددَ المستويات.")


def markov_audit() -> MarkovAuditReading:
    """دقِّق جدولَ ٥ي داخليًّا، ولا رقمَ في الحصاد مكتوبٌ بيد."""

    reconstructions = derive_lambda_reconstructions()
    checks = derive_ratio_checks()
    blocks = [row.same_block_exp for row in MARKOV_LEVELS]
    lambdas = [row.reported_lambda for row in MARKOV_LEVELS]
    checked = tuple(item for item in reconstructions if not item.is_anchor)
    inside = sum(1 for item in checked if item.reported_inside_interval)
    computable = sum(1 for check in checks if check.value is not None)
    return MarkovAuditReading(
        levels=len(MARKOV_LEVELS),
        anchor_levels=len(reconstructions) - len(checked),
        lambdas_inside_rounding=inside,
        lambdas_outside_rounding=len(checked) - inside,
        ratio_levels_computable=computable,
        ratio_levels_unavailable=len(checks) - computable,
        reported_ratio=REPORTED_GAMMA_OVER_BETA,
        same_block_is_monotone_increasing=all(
            earlier < later for earlier, later in pairwise(blocks)
        ),
        reported_lambda_is_monotone_decreasing=all(
            earlier > later for earlier, later in pairwise(lambdas)
        ),
    )


def slgae_v2_path(root: Path | None = None) -> Path:
    """مسارُ النسخة الثانية، مبنيًّا من جذر الشجرة لا مكتوبًا مطلقًا."""

    base = root if root is not None else Path(__file__).resolve().parents[3]
    return base / SLGAE_V2_RELATIVE_PATH


def slgae_v2_digest(root: Path | None = None) -> str:
    """بصمةُ النسخة الثانية، مُشتَقّةً من بايتاتها الآن لا من حقلٍ مكتوب."""

    path = slgae_v2_path(root)
    if not path.is_file():
        raise SlgaeDepositError(
            f"النسخةُ الثانيةُ غيرُ موجودةٍ في موضعها: {SLGAE_V2_RELATIVE_PATH}."
        )
    return canonical_digest(path.read_bytes())


def both_version_digests(root: Path | None = None) -> tuple[tuple[str, str], ...]:
    """بصمتا النسختين معًا بمسارَيهما؛ والأولى باقيةٌ لا تُمحى."""

    digests = (
        (SLGAE_RELATIVE_PATH, slgae_digest(root)),
        (SLGAE_V2_RELATIVE_PATH, slgae_v2_digest(root)),
    )
    if digests[0][1] == digests[1][1]:
        raise SlgaeDepositError(
            "بصمتا النسختين متطابقتان؛ ونسختان ببصمةٍ واحدةٍ نسخةٌ واحدة."
        )
    return digests


A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE: Final[str] = (
    "ASupersededVersionIsRecordedNotErased: النسختان تُودَعان معًا؛ وإيداعُ "
    "الموسَّعة وحدها يُخفي أنّ دعوًى أُطلِقت ثمّ قُيِّدت، ويضيع أنفسُ ما "
    "فيها: مواضعُ التقييد"
)

THE_AUTHORS_OWN_TIERING_IS_THE_STRONGEST_THING_NOTE: Final[str] = (
    "TheAuthorsOwnTieringIsTheStrongestThingInTheSecondVersion: أنفسُ ما "
    "جاءت به الثانيةُ جدولُ المراتب، إذ يُنزِل بيدِ صاحبه ما كان مُطلَقًا؛ "
    "ويُسجَّل كما ورد بلا رفعٍ ولا خفض"
)

THE_TWENTY_SIX_ARE_A_DECLARED_CHOICE_NOTE: Final[str] = (
    "TheTwentySixAreADeclaredChoiceNotABirth: صارت قائمةُ الصوامت في مرتبة "
    "«اختيار مني»؛ فالتعارضُ 26/28 يبقى بعدده وتتغيّر قراءتُه — طرفاه "
    "اختيارٌ مُعلَنٌ وجدولٌ مُبصَّم"
)

AN_INTERNAL_AUDIT_IS_NOT_A_REDERIVATION_NOTE: Final[str] = (
    "AnInternalAuditIsNotARederivation: ما يجري على جدول ماركوف تدقيقُ "
    "اتّساقٍ بين أعمدةٍ منشورة لا إعادةُ اشتقاقٍ من مدوّنة؛ فلا يُقال صوابٌ "
    "ولا خطأ، بل ما يُبنى وما لا يُبنى وما يلزم ليُبنى"
)

ROUNDING_IS_A_CANDIDATE_EXPLANATION_NOTE: Final[str] = (
    "RoundingIsACandidateExplanationNamedBeforeTheVerdict: الأعمدةُ منشورةٌ "
    "بمنزلتين، فمجالُ التقريب يُحسَب أوّلًا ويُقارَن به الفرق؛ ومن أعلن "
    "فرقًا قبل حساب مجاله أعلن أثرَ التقريب خلافًا"
)

SLGAE_V2_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE,
    THE_AUTHORS_OWN_TIERING_IS_THE_STRONGEST_THING_NOTE,
    THE_TWENTY_SIX_ARE_A_DECLARED_CHOICE_NOTE,
    AN_INTERNAL_AUDIT_IS_NOT_A_REDERIVATION_NOTE,
    ROUNDING_IS_A_CANDIDATE_EXPLANATION_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len({tier.tier for tier in CLAIM_TIERS}) != len(
    ClaimTier
):  # pragma: no cover - حارس
    raise RuntimeError(
        "مرتبةٌ من مراتب الادّعاء بلا صفٍّ في السجلّ؛ ومرتبةٌ غائبةٌ تُقرأ "
        "كأنّها لم تُذكَر في الوثيقة."
    )
