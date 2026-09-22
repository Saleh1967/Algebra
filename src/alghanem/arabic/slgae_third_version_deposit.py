"""النسخةُ الثالثة من SLGAE: معرِّفٌ واحدٌ على تجربتين، وفحوصٌ على ما نُشر.

**ما تفعله هذه الوحدة**: تُودِع النسخةَ الثالثةَ مُبصَّمةً إلى جانب الأولى
والثانية، وتُسجّل ما زادته — قسمَي ٥ك — ثمّ **تفحص ما يُفحَص منهما بالحساب**:
اتّساقَ إحصاءاتهما المنشورة، ومطابقةَ ترتيبٍ مرصودٍ لترتيبٍ متوقَّع، وفجوةَ
المقدار بين جسرَين يُقدَّمان جسرًا واحدًا.

`ONE_IDENTIFIER_OVER_TWO_EXPERIMENTS_CAN_BE_CITED_ON_ITSELF`: أخطرُ ما في
النسخة الثالثة ليس نتيجةً، بل **ترقيمٌ**: قسمان يحملان الرقمَ ٥ك نفسَه
والمعرِّفَ `VOWEL-FIRST-BIRTH-AR-1` نفسَه، وهما تجربتان مختلفتان — بيانتان
مختلفتان، وأسماءُ اختباراتٍ مختلفة (P1/P2/P3 مقابل V0–V3)، وحكمان يلتقيان في
الاتّجاه ويفترقان في المقدار. ومعرِّفٌ يسمّي شيئين يُستشهَد به على نفسه: يُذكر
سقوطُ P1 فيُحمَل على نجاح V0، أو بالعكس. والعددان يُقرآن من بايتات الملفّ لا
يُكتَبان هنا.

`THE_COLLISION_IS_CLOSED_IN_THE_DOCUMENT_NOT_IN_THE_DEPOSIT`: التصادمُ أُغلق
بمعرِّفين متمايزين، واحدٍ لكلّ قسم، في
`docs/reference/slgae_5k_identifier_disambiguation.md`. وبايتاتُ `_v3.md` لا
تُمَسّ: هي مُودَعةٌ بنصّها كما وردت ومُبصَّمة، فالعددُ يبقى اثنين مقروءًا منها،
والإغلاقُ **تسميةٌ بعد اليوم لا تصحيحٌ في المُودَع**. وكلُّ إحالةٍ قديمةٍ إلى
المعرِّف المتصادم **ناقصةٌ لا خاطئة**: تتعيّن باسم الاختبار المذكور معها
(P1–P3 مقابل V0–V3)، وما لا يتعيّن يُرَدّ ولا يُخمَّن.

`A_SHARED_DIRECTION_IS_NOT_A_SHARED_MAGNITUDE`: القسمان يتّفقان أنّ الحلقَ
يجرّ الفتح، ويفترقان في المقدار فرقًا كبيرًا: نسبةٌ 1.15 في الأوّل مقابل 4.77
في الثاني، وأرجحيّةٌ 1.39 مقابل 20.8. وهما مجتمعان مختلفان ومقياسان مختلفان،
فلا يُقال إنّ أحدهما يؤكّد الآخر حتّى تُسمّى قاعدةُ ردّ أحدهما إلى الآخر.

`A_FAILED_ORDER_IS_NOT_A_REVERSED_ORDER`: الترتيبُ المتوقَّع في V3 سقط، لكنّ
المرصودَ **ليس معكوسَه** أيضًا؛ وهذا يُشتَقّ بالمقارنة لا يُوصَف. فمن قرأ
سقوطَ ترتيبٍ انقلابًا له بنى على الانقلاب ما لا يحمله.

`AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION`: ما يجري هنا فحصُ أرقامٍ منشورةٍ
بعضِها ببعض، لا إعادةَ اشتقاقٍ من مدوّنة؛ فلا بايتاتِ QAC في مسار هذا الملفّ،
ولا يُقال صوابٌ ولا خطأ.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from alghanem.canonical_content import canonical_digest

from .slgae_deposit import SLGAE_RELATIVE_PATH, SlgaeDepositError, slgae_digest
from .slgae_second_version_deposit import SLGAE_V2_RELATIVE_PATH, slgae_v2_digest

__all__ = [
    "A_FAILED_ORDER_IS_NOT_A_REVERSED_ORDER_NOTE",
    "A_SHARED_DIRECTION_IS_NOT_A_SHARED_MAGNITUDE_NOTE",
    "AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE",
    "COLLIDING_IDENTIFIER",
    "COLLIDING_SECTION_NUMBER",
    "DISAMBIGUATION_RELATIVE_PATH",
    "ONE_IDENTIFIER_OVER_TWO_EXPERIMENTS_NOTE",
    "SLGAE_V3_NAMED_RESIDUALS",
    "SLGAE_V3_RELATIVE_PATH",
    "THE_COLLISION_IS_CLOSED_IN_THE_DOCUMENT_NOTE",
    "THIRD_VERSION_EXPERIMENTS",
    "V3_PREDICTED_ORDER",
    "V3_OBSERVED_VALUES",
    "BridgeGap",
    "IdentifierCollision",
    "OrderingCheck",
    "SectionExperiment",
    "StatisticCheck",
    "derive_bridge_gap",
    "derive_identifier_collision",
    "derive_ordering_check",
    "derive_statistic_checks",
    "disambiguation_digest",
    "disambiguation_path",
    "resolve_colliding_citation",
    "slgae_v3_digest",
    "slgae_v3_path",
    "version_chain_digests",
]

SLGAE_V3_RELATIVE_PATH: Final[str] = "docs/reference/slgae_slot_licensing_algebra_v3.md"

DISAMBIGUATION_RELATIVE_PATH: Final[str] = (
    "docs/reference/slgae_5k_identifier_disambiguation.md"
)

COLLIDING_SECTION_NUMBER: Final[str] = "٥ك"

COLLIDING_IDENTIFIER: Final[str] = "VOWEL-FIRST-BIRTH-AR-1"


def slgae_v3_path(root: Path | None = None) -> Path:
    """مسارُ النسخة الثالثة، مبنيًّا من جذر الشجرة لا مكتوبًا مطلقًا."""

    base = root if root is not None else Path(__file__).resolve().parents[3]
    return base / SLGAE_V3_RELATIVE_PATH


def _read_v3(root: Path | None = None) -> str:
    path = slgae_v3_path(root)
    if not path.is_file():
        raise SlgaeDepositError(
            f"النسخةُ الثالثةُ غيرُ موجودةٍ في موضعها: {SLGAE_V3_RELATIVE_PATH}."
        )
    return path.read_text(encoding="utf-8")


def slgae_v3_digest(root: Path | None = None) -> str:
    """بصمةُ النسخة الثالثة، مُشتَقّةً من بايتاتها الآن لا من حقلٍ مكتوب."""

    return canonical_digest(slgae_v3_path(root).read_bytes())


def disambiguation_path(root: Path | None = None) -> Path:
    """مسارُ وثيقة التمييز، مبنيًّا من جذر الشجرة لا مكتوبًا مطلقًا."""

    base = root if root is not None else Path(__file__).resolve().parents[3]
    return base / DISAMBIGUATION_RELATIVE_PATH


def disambiguation_digest(root: Path | None = None) -> str:
    """بصمةُ وثيقة التمييز؛ فالإغلاقُ نصٌّ له بايتاتٌ لا إحالةٌ في الذاكرة."""

    return canonical_digest(_disambiguation_file(root).read_bytes())


def _disambiguation_file(root: Path | None = None) -> Path:
    path = disambiguation_path(root)
    if not path.is_file():
        raise SlgaeDepositError(
            f"وثيقةُ التمييز غيرُ موجودةٍ في موضعها: {DISAMBIGUATION_RELATIVE_PATH}؛ "
            "وإغلاقٌ بلا نصٍّ في الشجرة إغلاقٌ في المحادثة."
        )
    return path


def _read_disambiguation(root: Path | None = None) -> str:
    return _disambiguation_file(root).read_text(encoding="utf-8")


def version_chain_digests(root: Path | None = None) -> tuple[tuple[str, str], ...]:
    """بصماتُ النسخ الثلاث بمساراتها؛ والسابقتان باقيتان لا تُمحيان."""

    chain = (
        (SLGAE_RELATIVE_PATH, slgae_digest(root)),
        (SLGAE_V2_RELATIVE_PATH, slgae_v2_digest(root)),
        (SLGAE_V3_RELATIVE_PATH, slgae_v3_digest(root)),
    )
    digests = [digest for _path, digest in chain]
    if len(set(digests)) != len(digests):
        raise SlgaeDepositError(
            "بصمتان متطابقتان في سلسلة النسخ؛ ونسختان ببصمةٍ واحدةٍ نسخةٌ واحدة."
        )
    return chain


@dataclass(frozen=True, slots=True)
class SectionExperiment:
    """تجربةٌ واحدةٌ من قسمَي ٥ك: بيانُها، وأسماءُ اختباراتها، وحكمُها، ومعرِّفُها."""

    title: str
    data: str
    test_names: tuple[str, ...]
    verdict: str
    assigned_identifier: str

    def __post_init__(self) -> None:
        if not self.test_names:
            raise SlgaeDepositError("تجربةٌ بلا اسمِ اختبارٍ واحدٍ لا تُقابَل بغيرها.")
        if not self.assigned_identifier.strip():
            raise SlgaeDepositError(
                "تجربةٌ بلا معرِّفٍ مُميَّزٍ تبقى تحت المعرِّف المتصادم، "
                "والإغلاقُ يقتضي اسمًا يُستشهَد به."
            )
        if self.assigned_identifier == COLLIDING_IDENTIFIER:
            raise SlgaeDepositError(
                f"«{COLLIDING_IDENTIFIER}» هو المعرِّفُ المتصادمُ نفسُه؛ "
                "وإعادتُه اسمًا مُميَّزًا تُبقي التصادمَ وتسمّيه إغلاقًا."
            )


THIRD_VERSION_EXPERIMENTS: Final[tuple[SectionExperiment, ...]] = (
    SectionExperiment(
        title="ترتيب بديل: ا و ي أولًا ثم المخرج",
        data="جذوع QAC، أنواع، 4837 جذعًا في التأكيد؛ ملفُّ الميل إلى a/i/u",
        test_names=("P1", "P2", "P3"),
        verdict="المخرجُ لا يرث ا و ي؛ والجسرُ الوحيد الحلق ↔ الفتح",
        assigned_identifier="MAKHRAJ-INHERITS-VOWELS-AR-1",
    ),
    SectionExperiment(
        title="سلسلة الولادة من الصائت أولًا",
        data="جذوع QAC المشكولة، الرسمُ فقط بلا وسومٍ صرفيّة",
        test_names=("V0", "V1", "V2", "V3"),
        verdict=(
            "يولد الطورُ الأوّل، وينعكس الاتّجاه: الصائتُ في الخانة المعجميّة "
            "يرث المخرجَ لا العكس"
        ),
        assigned_identifier="VOWEL-FIRST-BIRTH-CHAIN-AR-1",
    ),
)
"""التجربتان اللتان يحملهما الرقمُ والمعرِّفُ نفساهما، بما يفرّق بينهما."""


@dataclass(frozen=True, slots=True)
class IdentifierCollision:
    """تصادمُ معرِّفٍ: عددُ مواضعه مقروءًا من الملفّ، وما يفرّق بين حامليه."""

    identifier: str
    section_number: str
    heading_occurrences: int
    identifier_occurrences: int
    experiments: tuple[SectionExperiment, ...]
    shared_test_names: tuple[str, ...]
    closing_identifiers_in_document: tuple[str, ...]

    @property
    def is_a_collision(self) -> bool:
        """أيسمّي المعرِّفُ أكثرَ من موضع؟ مُشتَقٌّ من العدّ لا مكتوبٌ بجانبه."""

        return self.heading_occurrences > 1 or self.identifier_occurrences > 1

    @property
    def assigned_identifiers(self) -> tuple[str, ...]:
        """المعرِّفان المُميَّزان بترتيب قسمَيهما، مُشتَقَّين من التجربتين."""

        return tuple(experiment.assigned_identifier for experiment in self.experiments)

    @property
    def is_closed(self) -> bool:
        """أأُغلق التصادم؟ لكلّ قسمٍ معرِّفٌ متمايزٌ، وكلُّها واردةٌ في الوثيقة."""

        assigned = self.assigned_identifiers
        return len(set(assigned)) == len(assigned) == len(self.experiments) and set(
            assigned
        ) <= set(self.closing_identifiers_in_document)


def derive_identifier_collision(root: Path | None = None) -> IdentifierCollision:
    """عُدَّ مواضعَ الرقم والمعرِّف من بايتات الملفّ، ولا تكتب عددًا هنا."""

    text = _read_v3(root)
    headings = sum(
        1
        for line in text.splitlines()
        if line.startswith(f"{COLLIDING_SECTION_NUMBER} ")
    )
    first, second = THIRD_VERSION_EXPERIMENTS
    shared = tuple(sorted(set(first.test_names) & set(second.test_names)))
    disambiguation_text = _read_disambiguation(root)
    closing = tuple(
        experiment.assigned_identifier
        for experiment in THIRD_VERSION_EXPERIMENTS
        if experiment.assigned_identifier in disambiguation_text
    )
    return IdentifierCollision(
        identifier=COLLIDING_IDENTIFIER,
        section_number=COLLIDING_SECTION_NUMBER,
        heading_occurrences=headings,
        identifier_occurrences=text.count(COLLIDING_IDENTIFIER),
        experiments=THIRD_VERSION_EXPERIMENTS,
        shared_test_names=shared,
        closing_identifiers_in_document=closing,
    )


def resolve_colliding_citation(test_name: str) -> SectionExperiment:
    """عيِّن القسمَ المقصودَ باسم الاختبار المذكور مع الإحالة القديمة.

    والإحالةُ التي لا يُذكر معها اسمُ اختبارٍ **ناقصةٌ لا خاطئة**، فتُرَدّ
    ولا تُحمَل على أقرب القسمين.
    """

    wanted = test_name.strip().upper()
    matches = tuple(
        experiment
        for experiment in THIRD_VERSION_EXPERIMENTS
        if wanted in experiment.test_names
    )
    if not matches:
        raise SlgaeDepositError(
            f"«{test_name}» ليس اسمَ اختبارٍ في قسمَي "
            f"{COLLIDING_SECTION_NUMBER}؛ وإحالةٌ لا تتعيّن لا تُخمَّن."
        )
    if len(matches) > 1:  # pragma: no cover - يمنعه افتراقُ الأسماء البنيويّ
        raise SlgaeDepositError(f"«{test_name}» في القسمين معًا؛ فلا يعيّن أحدَهما.")
    return matches[0]


@dataclass(frozen=True, slots=True)
class StatisticCheck:
    """فحصُ اتّساقٍ بين رقمين منشورين، بنصّ ما فُحِص وبنتيجته."""

    what_was_checked: str
    holds: bool
    detail: str


def derive_statistic_checks() -> tuple[StatisticCheck, ...]:
    """افحص إحصاءاتِ القسمين بعضَها ببعض؛ ولا رقمَ في النتيجة مكتوبٌ بيد."""

    pseudo_f, threshold, p_value = 1.48, 1.88, 0.15
    ari = -0.08
    purity, chance, purity_p = 0.654, 0.569, 0.12
    excess = purity - chance
    return (
        StatisticCheck(
            what_was_checked="pseudo-F دون العتبة ⇔ p فوق 0.05",
            holds=(pseudo_f < threshold) == (p_value > 0.05),
            detail=(
                f"F = {pseudo_f} والعتبة {threshold}؛ و p = {p_value}. "
                "الطرفان يقولان الشيءَ نفسه، فالسقوطُ متّسق"
            ),
        ),
        StatisticCheck(
            what_was_checked="ARI دون الصفر ⇒ التجميعُ دون المصادفة",
            holds=ari < 0,
            detail=(
                f"ARI = {ari}؛ وسالبُه يعني أنّ التجميعَ أسوأُ من عشوائيٍّ "
                "لا أنّه ضعيفُ التطابق فحسب"
            ),
        ),
        StatisticCheck(
            what_was_checked="فائضُ النقاء موجبٌ ومع ذلك غيرُ دالّ",
            holds=excess > 0 and purity_p > 0.05,
            detail=(
                f"نقاءٌ {purity} مقابل {chance} عشوائيًّا، فالفائضُ "
                f"{excess:+.3f} أي {100 * excess / chance:+.1f}% نسبيًّا، "
                f"و p = {purity_p}؛ فالفائضُ الموجبُ وحدَه لا يُثبِت"
            ),
        ),
    )


V3_PREDICTED_ORDER: Final[tuple[str, ...]] = ("خيشومي", "أسناني", "لساني")
"""الترتيبُ المتوقَّع في V3، كما كُتب قبل العدّ: خيشومي ≥ أسناني ≥ لساني."""

V3_OBSERVED_VALUES: Final[tuple[tuple[str, float], ...]] = (
    ("خيشومي", 0.19),
    ("أسناني", 0.16),
    ("لساني", 0.21),
)
"""القيمُ المرصودةُ كما نُشرت، كلُّ فئةٍ بقيمتها لا برتبتها."""


@dataclass(frozen=True, slots=True)
class OrderingCheck:
    """مقابلةُ ترتيبٍ متوقَّعٍ بترتيبٍ مرصودٍ مُشتَقٍّ من القيم."""

    predicted: tuple[str, ...]
    observed: tuple[str, ...]
    matches_prediction: bool
    is_exact_reverse: bool

    def __post_init__(self) -> None:
        if set(self.predicted) != set(self.observed):
            raise SlgaeDepositError(
                "الترتيبان على فئتين مختلفتين؛ ومقابلةُ ترتيبين لا يشتركان في "
                "أعضائهما مقابلةٌ لا معنى لها."
            )


def derive_ordering_check() -> OrderingCheck:
    """رتِّب المرصودَ من قيمه، وقابِلْه بالمتوقَّع؛ والرتبةُ تُشتَقّ لا تُكتَب."""

    observed = tuple(
        name for name, _value in sorted(V3_OBSERVED_VALUES, key=lambda row: -row[1])
    )
    return OrderingCheck(
        predicted=V3_PREDICTED_ORDER,
        observed=observed,
        matches_prediction=observed == V3_PREDICTED_ORDER,
        is_exact_reverse=observed == V3_PREDICTED_ORDER[::-1],
    )


@dataclass(frozen=True, slots=True)
class BridgeGap:
    """فجوةُ المقدار بين جسرَي «الحلقُ يجرّ الفتح» في القسمين."""

    first_with: float
    first_without: float
    second_with: float
    second_without: float
    first_ratio: float
    second_ratio: float
    first_odds_ratio: float
    second_odds_ratio: float
    ratio_gap: float
    odds_ratio_gap: float

    def __post_init__(self) -> None:
        if self.ratio_gap <= 1 or self.odds_ratio_gap <= 1:
            raise SlgaeDepositError(
                "فجوةٌ لا تزيد على الواحد ليست فجوة؛ والقسمُ يُجرى بالأكبر "
                "على الأصغر كيلا يُقرأ الفارقُ مقلوبًا."
            )


def derive_bridge_gap() -> BridgeGap:
    """قابِلْ مقدارَي الجسر الواحد في القسمين، بالنسبة وبالأرجحيّة معًا.

    والأرجحيّةُ تُحسَب إلى جانب النسبة لأنّ النسبةَ وحدَها تُصغّر الفارقَ
    حين تقترب إحدى النسبتين من الواحد.
    """

    first_with, first_without = 0.62, 0.54
    second_with, second_without = 0.81, 0.17
    first_ratio = first_with / first_without
    second_ratio = second_with / second_without
    first_odds = (first_with / (1 - first_with)) / (first_without / (1 - first_without))
    second_odds = (second_with / (1 - second_with)) / (
        second_without / (1 - second_without)
    )
    return BridgeGap(
        first_with=first_with,
        first_without=first_without,
        second_with=second_with,
        second_without=second_without,
        first_ratio=first_ratio,
        second_ratio=second_ratio,
        first_odds_ratio=first_odds,
        second_odds_ratio=second_odds,
        ratio_gap=second_ratio / first_ratio,
        odds_ratio_gap=second_odds / first_odds,
    )


ONE_IDENTIFIER_OVER_TWO_EXPERIMENTS_NOTE: Final[str] = (
    "OneIdentifierOverTwoExperimentsCanBeCitedOnItself: قسمان بالرقم "
    "والمعرِّف نفسيهما وهما تجربتان مختلفتان بيانًا واختباراتٍ ومقدارًا؛ "
    "فيُذكر سقوطُ اختبارٍ في أحدهما فيُحمَل على نجاح اختبارٍ في الآخر"
)

A_SHARED_DIRECTION_IS_NOT_A_SHARED_MAGNITUDE_NOTE: Final[str] = (
    "ASharedDirectionIsNotASharedMagnitude: القسمان يتّفقان أنّ الحلقَ يجرّ "
    "الفتحَ ويفترقان في المقدار افتراقًا كبيرًا؛ فلا يؤكّد أحدُهما الآخرَ "
    "حتّى تُسمّى قاعدةُ ردّ أحدهما إليه"
)

A_FAILED_ORDER_IS_NOT_A_REVERSED_ORDER_NOTE: Final[str] = (
    "AFailedOrderIsNotAReversedOrder: ترتيبُ V3 سقط والمرصودُ ليس معكوسَه؛ "
    "ومن قرأ السقوطَ انقلابًا بنى على الانقلاب ما لا يحمله"
)

AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE: Final[str] = (
    "AnInternalCheckIsNotARederivation: فحصُ أرقامٍ منشورةٍ بعضِها ببعض لا "
    "إعادةُ اشتقاقٍ من مدوّنة؛ فلا يُقال صوابٌ ولا خطأ، بل ما يتّسق وما لا يتّسق"
)

THE_COLLISION_IS_CLOSED_IN_THE_DOCUMENT_NOTE: Final[str] = (
    "TheCollisionIsClosedInTheDocumentNotInTheDeposit: لكلّ قسمٍ معرِّفٌ "
    "متمايزٌ في وثيقة التمييز، وبايتاتُ المُودَع لا تُمَسّ فيبقى العددُ اثنين؛ "
    "والإحالةُ القديمةُ ناقصةٌ تتعيّن باسم اختبارها، وما لا يتعيّن يُرَدّ"
)

SLGAE_V3_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    ONE_IDENTIFIER_OVER_TWO_EXPERIMENTS_NOTE,
    A_SHARED_DIRECTION_IS_NOT_A_SHARED_MAGNITUDE_NOTE,
    A_FAILED_ORDER_IS_NOT_A_REVERSED_ORDER_NOTE,
    AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE,
    THE_COLLISION_IS_CLOSED_IN_THE_DOCUMENT_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(THIRD_VERSION_EXPERIMENTS) != 2:  # pragma: no cover - حارس
    raise RuntimeError("قسما ٥ك اثنان؛ وزيادةٌ أو نقصٌ يجعل التصادمَ موصوفًا لا معدودًا.")

if len(  # pragma: no cover - حارس
    {experiment.assigned_identifier for experiment in THIRD_VERSION_EXPERIMENTS}
) != len(THIRD_VERSION_EXPERIMENTS):
    raise RuntimeError("معرِّفان متطابقان بعد التمييز؛ وتصادمٌ يُغلَق باسمٍ واحدٍ لا يُغلَق.")
