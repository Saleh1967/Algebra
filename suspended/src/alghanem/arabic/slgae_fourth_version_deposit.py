"""النسخةُ الرابعة من SLGAE: جسرٌ بثلاثة مقادير، ونافذةٌ تتّزن، وفراكتاليّةٌ مقسومة.

**ما تفعله هذه الوحدة**: تُودِع النسخةَ الرابعةَ مُبصَّمةً إلى جانب سابقاتها،
وتفحص ما زادته — قسمَي ٥ل و٥م — بالحساب: تجمع مقاديرَ جسر الحلق الثلاثةَ في
موضعٍ واحد، وتتحقّق من اتّزان جدول النوافذ بمجال تقريبه، وتسجّل كيف قُسمت
الفراكتاليّةُ بين نفيٍ وإثبات.

`A_THIRD_MAGNITUDE_MAKES_THE_BRIDGE_A_FAMILY_NOT_A_FIGURE`: «الحلقيّ يفرض
الفتح» ورد الآن **بثلاثة مقادير** في ثلاثة أقسام: 0.62/0.54، ثمّ 0.81/0.17،
ثمّ 0.81/0.22. فلم يعد رقمًا واحدًا يُستشهَد به، بل أسرةَ أرقامٍ تحتاج قاعدةَ
اختيارٍ مكتوبةً قبل الاستشهاد.

`A_SMALLER_P_WITH_A_WEAKER_EFFECT_MEANS_A_LARGER_SAMPLE`: بين القسمين
الأخيرين **ضعُف الأثرُ** (أرجحيّةٌ من 20.81 إلى 15.11، أي −27.4%) و**اشتدّت
الدلالة** (p من 1.5e-14 إلى 9e-17). ولا يجتمعان إلّا بكِبَر العيّنة؛ وحجمُ
العيّنة **غيرُ مذكورٍ في القسمين**. فالفارقُ يُسجَّل سؤالًا لا خطأً، وسؤالُه
واحد: كم كانت N في كلٍّ منهما.

`THE_WINDOW_TABLE_BALANCES_WITHIN_ITS_ROUNDING`: جدولُ ٥م يتّزن في مستوياته
الثلاثة إن قُرئت التجاوزاتُ **مضافةً** إلى `s=0` و`s=1`، وذلك بعد حساب مجال
التقريب لا قبله. وأضيقُ الصفوف هامشًا هو المفصلُ الصرفيّ. وهذا خبرٌ موجب:
عمودُ «غير مفسَّر» صفرٌ في الثلاثة، والحسابُ لا يكذّبه.

`ONE_WORD_TWO_VERDICTS_IS_A_DIVISION_NOT_A_CONTRADICTION`: ٥ل يقول
«لا تصمد فراكتاليًّا» و٥م يقول «فراكتالي»، وليسا متناقضَين: الأوّلُ عن علاقات
**النوع** (أيُّ صائتٍ مع أيّ صامت) والثاني عن قيد **العدد** (`s ≤ 1`).
والوثيقةُ تحسمه بنفسها: «العدد فراكتالي، والنوع معجمي». فيُسجَّل الحسمُ حيث
وقع، ولا يُترَك اللفظُ يوهم خلافًا.

`AN_EXACT_ZERO_IS_NOT_A_MEASURED_RATIO`: في جدول ٥ل خليّتان قيمتُهما 0.00
بالضبط، وهما نسبتا O/E؛ ونسبةُ الصفر تعني صفرَ مشاهدةٍ لا ضعفَ أثر. وما لم
يُذكر المتوقَّعُ E لم يُعرَف أهي فجوةٌ بنيويّةٌ أم قلّةُ فرصة.

`AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION`: ما يجري هنا حسابٌ على أرقامٍ
منشورة، لا إعادةَ اشتقاقٍ من مدوّنة؛ فلا يُقال صوابٌ ولا خطأ.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from alghanem.canonical_content import canonical_digest

from .slgae_deposit import SlgaeDepositError
from .slgae_third_version_deposit import (
    slgae_v3_digest,
    version_chain_digests,
)

__all__ = [
    "AN_EXACT_ZERO_IS_NOT_A_MEASURED_RATIO_NOTE",
    "AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE",
    "A_SMALLER_P_WITH_A_WEAKER_EFFECT_NOTE",
    "A_THIRD_MAGNITUDE_MAKES_THE_BRIDGE_A_FAMILY_NOTE",
    "FRACTALITY_DIVISION",
    "GUTTURAL_BRIDGE_READINGS",
    "ONE_WORD_TWO_VERDICTS_IS_A_DIVISION_NOTE",
    "ONSET_TOTAL",
    "ONSET_WITH_WRITTEN_WASLA",
    "ONSET_REMAINDER",
    "PUBLISHED_PERCENT_DECIMALS",
    "SLGAE_V4_NAMED_RESIDUALS",
    "SLGAE_V4_RELATIVE_PATH",
    "THE_WINDOW_TABLE_BALANCES_NOTE",
    "VCV_LEVELS",
    "VOWEL_RATIO_CELLS",
    "BridgeComparison",
    "BridgeReading",
    "FractalityDivision",
    "OnsetCheck",
    "VcvLevelRow",
    "WindowBalance",
    "compare_bridges",
    "derive_exact_zero_cells",
    "derive_onset_check",
    "derive_window_balances",
    "slgae_v4_digest",
    "slgae_v4_path",
    "version_chain_with_fourth",
]

SLGAE_V4_RELATIVE_PATH: Final[str] = "docs/reference/slgae_slot_licensing_algebra_v4.md"

PUBLISHED_PERCENT_DECIMALS: Final[int] = 1
"""عددُ المنازل التي نُشرت بها نِسَبُ جدول ٥م؛ ومنه يُحسَب مجالُ التقريب."""


def slgae_v4_path(root: Path | None = None) -> Path:
    """مسارُ النسخة الرابعة، مبنيًّا من جذر الشجرة لا مكتوبًا مطلقًا."""

    base = root if root is not None else Path(__file__).resolve().parents[3]
    return base / SLGAE_V4_RELATIVE_PATH


def slgae_v4_digest(root: Path | None = None) -> str:
    """بصمةُ النسخة الرابعة، مُشتَقّةً من بايتاتها الآن لا من حقلٍ مكتوب."""

    path = slgae_v4_path(root)
    if not path.is_file():
        raise SlgaeDepositError(
            f"النسخةُ الرابعةُ غيرُ موجودةٍ في موضعها: {SLGAE_V4_RELATIVE_PATH}."
        )
    return canonical_digest(path.read_bytes())


def version_chain_with_fourth(
    root: Path | None = None,
) -> tuple[tuple[str, str], ...]:
    """بصماتُ النسخ الأربع بمساراتها؛ والسابقاتُ باقياتٌ لا تُمحى."""

    chain = (
        *version_chain_digests(root),
        (SLGAE_V4_RELATIVE_PATH, slgae_v4_digest(root)),
    )
    digests = [digest for _path, digest in chain]
    if len(set(digests)) != len(digests):
        raise SlgaeDepositError(
            "بصمتان متطابقتان في سلسلة النسخ؛ ونسختان ببصمةٍ واحدةٍ نسخةٌ واحدة."
        )
    if chain[-2][1] != slgae_v3_digest(root):  # pragma: no cover - حارس
        raise SlgaeDepositError("بصمةُ الثالثة في السلسلة تخالف قراءتَها المباشرة.")
    return chain


@dataclass(frozen=True, slots=True)
class BridgeReading:
    """قراءةٌ واحدةٌ لجسر «الحلقيّ يفرض الفتح»، بموضعها ونسبتَيها."""

    section: str
    scope: str
    with_guttural: float
    without_guttural: float
    p_value: float | None

    def __post_init__(self) -> None:
        for value in (self.with_guttural, self.without_guttural):
            if not 0 < value < 1:
                raise SlgaeDepositError("نسبةُ الفتح بين الصفر والواحد حصرًا.")

    @property
    def ratio(self) -> float:
        """نسبةُ الفتح مع الحلقيّ إلى نسبته بدونه."""

        return self.with_guttural / self.without_guttural

    @property
    def odds_ratio(self) -> float:
        """الأرجحيّة، وتُحسَب لأنّ النسبةَ وحدَها تُصغّر الفارقَ قرب الواحد."""

        return (self.with_guttural / (1 - self.with_guttural)) / (
            self.without_guttural / (1 - self.without_guttural)
        )


GUTTURAL_BRIDGE_READINGS: Final[tuple[BridgeReading, ...]] = (
    BridgeReading(
        section="٥ك — ترتيب بديل",
        scope="ميلُ الحلقيّات إلى الفتح بعدها",
        with_guttural=0.62,
        without_guttural=0.54,
        p_value=None,
    ),
    BridgeReading(
        section="٥ك — سلسلة الولادة",
        scope="حركةُ عين المضارع في الثلاثيّ السالم",
        with_guttural=0.81,
        without_guttural=0.17,
        p_value=1.5e-14,
    ),
    BridgeReading(
        section="٥ل — الفراكتاليّة",
        scope="مضارعُ الثلاثيّ",
        with_guttural=0.81,
        without_guttural=0.22,
        p_value=9e-17,
    ),
)
"""مقاديرُ الجسر الثلاثةُ كما نُشرت، كلٌّ بموضعه ومجاله."""


@dataclass(frozen=True, slots=True)
class BridgeComparison:
    """مقابلةُ قراءتين للجسر نفسه: أثرٌ ودلالةٌ واتّجاهُ كلٍّ منهما."""

    earlier: BridgeReading
    later: BridgeReading
    odds_ratio_change: float
    effect_weakened: bool
    significance_strengthened: bool

    @property
    def implies_a_larger_sample(self) -> bool:
        """أثرٌ أضعفُ ودلالةٌ أشدّ لا يجتمعان إلّا بعيّنةٍ أكبر."""

        return self.effect_weakened and self.significance_strengthened


def compare_bridges() -> BridgeComparison:
    """قابِلْ آخِرَ قراءتين للجسر، وأخرِج ما يلزم منهما بالحساب."""

    earlier, later = GUTTURAL_BRIDGE_READINGS[1], GUTTURAL_BRIDGE_READINGS[2]
    if earlier.p_value is None or later.p_value is None:
        raise SlgaeDepositError("المقابلةُ تحتاج دلالتين منشورتين لا واحدة.")
    return BridgeComparison(
        earlier=earlier,
        later=later,
        odds_ratio_change=(later.odds_ratio - earlier.odds_ratio) / earlier.odds_ratio,
        effect_weakened=later.odds_ratio < earlier.odds_ratio,
        significance_strengthened=later.p_value < earlier.p_value,
    )


@dataclass(frozen=True, slots=True)
class VcvLevelRow:
    """صفُّ مستوًى في جدول ٥م، كما نُشر: نوافذُه ونِسَبُه وتجاوزاتُه."""

    level: str
    windows: int
    zero_percent: float
    one_percent: float
    licensed_excess: int
    repaired_excess: int
    unexplained: int

    def __post_init__(self) -> None:
        if self.windows <= 0:
            raise SlgaeDepositError("عددُ النوافذ موجب.")
        if self.unexplained < 0:
            raise SlgaeDepositError("عددُ غير المفسَّر لا يكون سالبًا.")

    @property
    def excess(self) -> int:
        """مجموعُ التجاوزات: المرخَّصُ منها والمُصلَحُ بالنطق."""

        return self.licensed_excess + self.repaired_excess


VCV_LEVELS: Final[tuple[VcvLevelRow, ...]] = (
    VcvLevelRow(
        level="الجذع",
        windows=100_440,
        zero_percent=46.0,
        one_percent=53.9,
        licensed_excess=96,
        repaired_excess=0,
        unexplained=0,
    ),
    VcvLevelRow(
        level="المفصل الصرفي",
        windows=37_172,
        zero_percent=63.8,
        one_percent=36.2,
        licensed_excess=3,
        repaired_excess=1,
        unexplained=0,
    ),
    VcvLevelRow(
        level="بين الكلمات",
        windows=71_129,
        zero_percent=32.4,
        one_percent=63.8,
        licensed_excess=0,
        repaired_excess=2_694,
        unexplained=0,
    ),
)
"""جدولُ ٥م كما نُشر، بنوافذه ونسبه وتجاوزاته."""


@dataclass(frozen=True, slots=True)
class WindowBalance:
    """اتّزانُ صفٍّ من جدول النوافذ داخل مجال تقريب نِسَبه."""

    level: str
    windows: int
    estimate_low: float
    estimate_high: float
    balances: bool
    nearest_edge_slack: float


def derive_window_balances() -> tuple[WindowBalance, ...]:
    """افحص اتّزانَ كلّ صفّ بعد حساب مجال التقريب، لا قبله.

    والقراءةُ المفحوصة: التجاوزاتُ **مضافةٌ** إلى `s=0` و`s=1`، إذ التجاوزُ
    `s > 1` فلا يقع داخل أيٍّ منهما.
    """

    half = 0.5 * 10 ** (-PUBLISHED_PERCENT_DECIMALS)
    balances: list[WindowBalance] = []
    for row in VCV_LEVELS:
        low = (
            (row.zero_percent - half) + (row.one_percent - half)
        ) / 100 * row.windows + row.excess
        high = (
            (row.zero_percent + half) + (row.one_percent + half)
        ) / 100 * row.windows + row.excess
        balances.append(
            WindowBalance(
                level=row.level,
                windows=row.windows,
                estimate_low=low,
                estimate_high=high,
                balances=low <= row.windows <= high,
                nearest_edge_slack=min(row.windows - low, high - row.windows),
            )
        )
    return tuple(balances)


ONSET_TOTAL: Final[int] = 9_421
"""الكلماتُ التي تبدأ بساكن، كما نُشرت في ٥م."""

ONSET_WITH_WRITTEN_WASLA: Final[int] = 9_417
"""منها ما بدأ بهمزة وصلٍ مكتوبة."""

ONSET_REMAINDER: Final[tuple[tuple[str, int], ...]] = (
    ("لام الأمر بعد ثمّ", 2),
    ("«لْـَٔيْكَة» بلا ألف وصل في الرسم", 2),
)
"""البقيّةُ مُسمّاةً حالةً حالة، لا مجموعةً في رقمٍ واحد."""


@dataclass(frozen=True, slots=True)
class OnsetCheck:
    """مطابقةُ بقيّة الابتداء: الفرقُ بالطرح مقابل مجموع الحالات المُسمّاة."""

    subtraction: int
    named_sum: int
    matches: bool


def derive_onset_check() -> OnsetCheck:
    """اطرح، واجمع الحالاتِ المُسمّاة، وقابِلْ؛ ولا تكتب الفرقَ رقمًا."""

    subtraction = ONSET_TOTAL - ONSET_WITH_WRITTEN_WASLA
    named = sum(count for _name, count in ONSET_REMAINDER)
    return OnsetCheck(
        subtraction=subtraction, named_sum=named, matches=subtraction == named
    )


VOWEL_RATIO_CELLS: Final[tuple[tuple[str, tuple[float, ...]], ...]] = (
    ("ضمة ثم واو صامتة", (1.26, 0.00, 0.90)),
    ("كسرة ثم ياء صامتة", (0.54, 1.14, 0.67)),
    ("كسرة ثم واو", (0.01, 0.24, 1.53)),
    ("ضمة ثم ياء", (0.11, 0.00, 0.54)),
)
"""نِسَبُ O/E في جدول ٥ل، بمستوياتها الثلاثة لكلّ علاقة."""


def derive_exact_zero_cells() -> tuple[tuple[str, int], ...]:
    """أخرِج الخلايا التي قيمتُها صفرٌ تامّ؛ وصفرُ النسبة صفرُ مشاهدة."""

    return tuple(
        (name, index)
        for name, values in VOWEL_RATIO_CELLS
        for index, value in enumerate(values)
        if value == 0.0
    )


@dataclass(frozen=True, slots=True)
class FractalityDivision:
    """كيف قُسمت الفراكتاليّةُ بين نفيٍ وإثبات، ومن حسم القسمة."""

    denied_for: str
    denied_in: str
    affirmed_for: str
    affirmed_in: str
    resolution_quoted: str
    is_a_contradiction: bool

    def __post_init__(self) -> None:
        if self.denied_for == self.affirmed_for:
            raise SlgaeDepositError(
                "نفيٌ وإثباتٌ على الشيء نفسِه تناقضٌ لا قسمة؛ "
                "فلا يُسجَّل قسمةً حتّى يختلف المحمولان."
            )


FRACTALITY_DIVISION: Final[FractalityDivision] = FractalityDivision(
    denied_for="علاقاتُ النوع: أيُّ صائتٍ يجاور أيَّ صامت",
    denied_in="٥ل — FRACTAL-VOWEL-AR-1",
    affirmed_for="قيدُ العدد: s ≤ 1 في النافذة VCV",
    affirmed_in="٥م — VCV-WINDOW-AR-1",
    resolution_quoted="العدد فراكتالي، والنوع معجمي",
    is_a_contradiction=False,
)
"""القسمةُ كما حسمتها الوثيقةُ بنفسها، لا كما نحملها عليها."""


A_THIRD_MAGNITUDE_MAKES_THE_BRIDGE_A_FAMILY_NOTE: Final[str] = (
    "AThirdMagnitudeMakesTheBridgeAFamilyNotAFigure: «الحلقيّ يفرض الفتح» ورد "
    "بثلاثة مقادير في ثلاثة أقسام؛ فلم يعد رقمًا يُستشهَد به بل أسرةَ أرقامٍ "
    "تحتاج قاعدةَ اختيارٍ مكتوبةً قبل الاستشهاد"
)

A_SMALLER_P_WITH_A_WEAKER_EFFECT_NOTE: Final[str] = (
    "ASmallerPWithAWeakerEffectMeansALargerSample: ضعُف الأثرُ واشتدّت "
    "الدلالةُ معًا، ولا يجتمعان إلّا بعيّنةٍ أكبر؛ وحجمُ العيّنة غيرُ مذكورٍ "
    "في القسمين، فالفارقُ سؤالٌ لا خطأ"
)

THE_WINDOW_TABLE_BALANCES_NOTE: Final[str] = (
    "TheWindowTableBalancesWithinItsRounding: جدولُ ٥م يتّزن في مستوياته "
    "الثلاثة إن قُرئت التجاوزاتُ مضافةً، بعد حساب مجال التقريب لا قبله؛ "
    "وعمودُ «غير مفسَّر» صفرٌ في الثلاثة والحسابُ لا يكذّبه"
)

ONE_WORD_TWO_VERDICTS_IS_A_DIVISION_NOTE: Final[str] = (
    "OneWordTwoVerdictsIsADivisionNotAContradiction: ٥ل ينفي الفراكتاليّةَ "
    "عن النوع و٥م يثبتها للعدد؛ والوثيقةُ تحسمها بنفسها: العدد فراكتالي "
    "والنوع معجمي"
)

AN_EXACT_ZERO_IS_NOT_A_MEASURED_RATIO_NOTE: Final[str] = (
    "AnExactZeroIsNotAMeasuredRatio: خليّتان في ٥ل قيمتُهما 0.00 وهما نسبتا "
    "O/E؛ وصفرُ النسبة صفرُ مشاهدة، وما لم يُذكر المتوقَّعُ لم يُعرَف أفجوةٌ "
    "بنيويّةٌ هي أم قلّةُ فرصة"
)

AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE: Final[str] = (
    "AnInternalCheckIsNotARederivation: حسابٌ على أرقامٍ منشورةٍ لا إعادةُ "
    "اشتقاقٍ من مدوّنة؛ فلا يُقال صوابٌ ولا خطأ"
)

SLGAE_V4_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_THIRD_MAGNITUDE_MAKES_THE_BRIDGE_A_FAMILY_NOTE,
    A_SMALLER_P_WITH_A_WEAKER_EFFECT_NOTE,
    THE_WINDOW_TABLE_BALANCES_NOTE,
    ONE_WORD_TWO_VERDICTS_IS_A_DIVISION_NOTE,
    AN_EXACT_ZERO_IS_NOT_A_MEASURED_RATIO_NOTE,
    AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(GUTTURAL_BRIDGE_READINGS) < 3:  # pragma: no cover - حارس
    raise RuntimeError("قراءاتُ الجسر أقلُّ من ثلاث؛ ونقصُ قراءةٍ يجعل الأسرةَ رقمًا.")
