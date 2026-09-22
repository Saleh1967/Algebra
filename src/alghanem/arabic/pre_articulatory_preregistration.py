"""تسجيلٌ مسبقٌ لقاعدةٍ تحت المخرج: السلسلةُ، والمساران، والمَسبارانِ، والمانع.

**ما تفعله هذه الوحدة**: تُسجّل — قبل أيّ قياس — سلسلةَ ما قبل التمفصل
المقترحةَ من خارج الشجرة، ومسارَيها، ومَسبارَي الهمزة والعين، **وشرطَ إبطال
كلٍّ منهما**. ولا تقيس شيئًا: الباقي المانعُ مكتوبٌ في `BLOCKING_RESIDUAL`،
وهو أنّه **لم تصل إشارةٌ صوتيّةٌ مُودَعةٌ إلى هذه الشجرة** ألبتّة.

`THE_BASE_IS_BELOW_THE_DEPOSITED_INVENTORY`: أليافُ هذه الشجرة كلُّها قاعدتُها
حاملٌ أو موضعٌ **يفترض مفردةَ الحروف سلفًا**. والمقترَحُ هنا يدفع القاعدةَ إلى
ما تحت المخرج: فرقُ ضغطٍ، فجريانٌ، فحاملُ تصويت. وهذه نقلةٌ حقيقيّةٌ في موضع
القاعدة، **وهي بعينها ما يجعلها غيرَ قابلةٍ للقياس بما أُودِع**: المُودَعُ
كلُّه رسمٌ — Tanzil وQAC والمقاييس — ولا بايتَ صوتٍ واحد.

`NO_SIGNAL_HAS_REACHED_THIS_TREE`: `DEPOSITED_SIGNAL_SOURCES` **فارغة**.
والرسمُ لا يرى الإغلاقَ ولا الجريان، فمَسبارٌ ميكانيكيٌّ لا يُشغَّل على حرفٍ
مكتوب. وهذا مانعٌ مُسمًّى لا فجوةٌ مسكوتٌ عنها، وشرطُ رفعه مكتوبٌ معه.

`A_PREREGISTRATION_IS_NOT_A_RESULT`: كلُّ ما هنا **توقّعٌ مكتوبٌ قبل العدّ**.
ولا يُقرأ سطرٌ منه خبرًا عن العربيّة، ولا عن آليّة النطق. ومن استشهد بتسجيلٍ
مسبقٍ على أنّه نتيجةٌ استشهد بنيّةٍ على فعل.

`THE_ORDER_IS_GEOMETRIC_NOT_CAUSAL`: ترتيبُ المخارج من الحنجرة إلى الشفتين
**ترتيبٌ هندسيّ**، ولا يُقرأ ادّعاءَ أنّ كلَّ حرفٍ يتولّد سببيًّا ممّا قبله.
وهذا هو القيدُ نفسُه المُسجَّل في `ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP`
على الجدول المُودَع: الترتيبُ عن المصدر، وجعلُه اشتقاقًا خطوتُنا نحن.

`HAMZA_IS_A_BOUNDARY_CANDIDATE_NOT_A_MOTHER_OF_LETTERS`: الهمزةُ هنا **أوّلُ
مرشّحٍ واضحٍ لحدّ الإغلاق**، لا أصلٌ تاريخيٌّ ولا فيزيائيٌّ لبقيّة الصوامت.
ومن قرأها أمًّا للحروف حمّل المَسبارَ دعوى نسبٍ لم تُختبَر.

`AIN_IS_A_PROBE_NOT_AN_ORIGIN`: والعينُ نقطةٌ في هندسة التضييق تُختبَر عند
الرجوع من الصائت المفتوح، لا أصلٌ مفترَضٌ لكلّ حركة. والفرقُ بين المَسبارَين
ميكانيكيٌّ: الهمزةُ تسأل أوُلِد الإغلاق، والعينُ تسأل أوُلِد التضييقُ مع بقاء
الجريان.

`A_PROBE_WITHOUT_A_FALSIFIER_IS_NOT_A_PROBE`: كلُّ مَسبارٍ هنا يحمل **شرطَ
إبطاله** نصًّا غيرَ فارغٍ شرطَ إنشاء. فمَسبارٌ لا يُقال فيه ما يُبطله يُثبَّت
مهما جاءت البيانات، وذلك سؤالٌ لا اختبار.

`IT_IS_NOT_A_BUNDLE_AND_LOCAL_TRIVIALITY_IS_NOT_THE_GATE`: لا تُسمّى هذه
البنيةُ حزمةَ ألياف. والسببُ **ليس** أنّ التفاهةَ الموضعيّة لم تُبرهَن: فوق
قاعدةٍ منفصلةٍ منتهيةٍ هي قائمةٌ دائمًا وتُحصَّل مجّانًا
(`LOCAL_TRIVIALITY_IS_VACUOUS_OVER_A_DISCRETE_BASE` في
`position_bundle_sections`). والشرطُ الساقطُ **ثباتُ الليف النموذجيّ**، وهو
مقيسٌ فاشلٌ فوق الحروف (`THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS`
في `haraka_fiber_structure`). فالتسميةُ المستعمَلة هنا **بنيةٌ ليفيّةٌ
مرخَّصة** لا حزمة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "AIN_IS_A_PROBE_NOT_AN_ORIGIN_NOTE",
    "A_PREREGISTRATION_IS_NOT_A_RESULT_NOTE",
    "A_PROBE_WITHOUT_A_FALSIFIER_IS_NOT_A_PROBE_NOTE",
    "BLOCKING_RESIDUAL",
    "CONSTRICTION_GEOMETRY",
    "DEPOSITED_SIGNAL_SOURCES",
    "HAMZA_IS_A_BOUNDARY_CANDIDATE_NOTE",
    "IT_IS_NOT_A_BUNDLE_NOTE",
    "NO_SIGNAL_HAS_REACHED_THIS_TREE_NOTE",
    "PRE_ARTICULATORY_CHAIN",
    "PRE_ARTICULATORY_NAMED_RESIDUALS",
    "PROBES",
    "STRUCTURE_NAME",
    "THE_BASE_IS_BELOW_THE_DEPOSITED_INVENTORY_NOTE",
    "THE_ORDER_IS_GEOMETRIC_NOT_CAUSAL_NOTE",
    "Branch",
    "BlockingResidual",
    "ChainStage",
    "MechanicalProbe",
    "PreArticulatoryError",
    "THE_TWO_PATHS_ARE_NOT_EQUALLY_DEEP_NOTE",
    "branch_depth_asymmetry",
    "branch_stages",
    "derive_branch_depths",
    "is_testable_today",
    "probe_named",
]

STRUCTURE_NAME: Final[str] = "بنيةٌ ليفيّةٌ مرخَّصة (Licensed Phonetic Fiber Structure)"
"""الاسمُ المستعمَل، وليس «حزمةَ ألياف»؛ والسببُ مكتوبٌ في بواقي الوحدة."""


class PreArticulatoryError(ValueError):
    """رُفض تسجيلٌ خارج شرطه؛ ولا يُحمَل على أقرب صيغةٍ مقبولة."""


class Branch(Enum):
    """المسارانِ بعد حامل التصويت، وعضوٌ للمشترك قبل التشعّب."""

    SHARED = "مشتركٌ قبل التشعّب"
    VOCALIC = "مسارُ الصائت: جريانٌ مفتوحٌ ثمّ هندسةٌ صائتيّة"
    CONSONANTAL = "مسارُ الصامت: تضييقٌ ثمّ هندسةٌ صامتيّة"


@dataclass(frozen=True, slots=True)
class ChainStage:
    """طورٌ في السلسلة: ما هو، وما **ليس** هو، ومساره.

    وحقلُ `what_it_is_not` شرطُ إنشاءٍ لا وصفٌ اختياريّ: طورٌ بلا حدٍّ يُقرأ
    بعد جلساتٍ أوسعَ ممّا سُجِّل، فيُحمَّل ما لم يُسجَّل له.
    """

    order: int
    name: str
    what_it_is: str
    what_it_is_not: str
    branch: Branch

    def __post_init__(self) -> None:
        if self.order < 0:
            raise PreArticulatoryError("رتبةُ الطور لا تكون سالبة.")
        for value, label in (
            (self.name, "اسمُ الطور"),
            (self.what_it_is, "ما هو الطور"),
            (self.what_it_is_not, "ما ليس هو الطور"),
        ):
            if not value.strip():
                raise PreArticulatoryError(
                    f"{label} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ وطورٌ بلا حدٍّ "
                    "يُقرأ أوسعَ ممّا سُجِّل"
                )


PRE_ARTICULATORY_CHAIN: Final[tuple[ChainStage, ...]] = (
    ChainStage(
        order=0,
        name="ε — مرجعُ انعدام الفرق",
        what_it_is="حالةُ لا فرقٍ تشغيليّة، تُتّخذ مرجعًا يُقاس عنه",
        what_it_is_not="ليست صوتًا، ولا صمتًا مقيسًا، ولا عدمًا فلسفيًّا",
        branch=Branch.SHARED,
    ),
    ChainStage(
        order=1,
        name="فرقُ الضغط",
        what_it_is="فرقٌ يُنشئ إمكانَ الحركة، وهو أوّلُ ما يُفارِق المرجع",
        what_it_is_not="ليس جريانًا بعدُ، ولا يُشترَط أن يُنتِج أثرًا مسموعًا",
        branch=Branch.SHARED,
    ),
    ChainStage(
        order=2,
        name="الجريان",
        what_it_is="انتقالُ الهواء الناشئ عن فرق الضغط",
        what_it_is_not="ليس تصويتًا، ولا يحمل جهرًا ولا همسًا بذاته",
        branch=Branch.SHARED,
    ),
    ChainStage(
        order=3,
        name="حاملُ التصويت",
        what_it_is="الجريانُ وقد حمل حالةَ تصويتٍ: مجهورًا أو مهموسًا",
        what_it_is_not="ليس حرفًا، ولا مخرجًا، ولا يُعيّن موضعَ تضييق",
        branch=Branch.SHARED,
    ),
    ChainStage(
        order=4,
        name="الحقلُ الصائتيُّ المفتوح V₀",
        what_it_is="جريانٌ مجهورٌ بلا إغلاق، قبل أيّ تعيينٍ مخرجيّ",
        what_it_is_not=(
            "ليس فتحةً ولا ضمّةً ولا كسرة؛ فالثلاثُ إسقاطاتٌ هندسيّةٌ عنه " "لا ذرّاتٌ أولى"
        ),
        branch=Branch.VOCALIC,
    ),
    ChainStage(
        order=5,
        name="الهندسةُ الصائتيّة",
        what_it_is="اتّجاهاتُ اللسان والفكّ والشفة تُسقِط V₀ على حالاتٍ متمايزة",
        what_it_is_not="ليست تسميةَ الحركات؛ والتسميةُ تأتي بعد التعيين لا قبله",
        branch=Branch.VOCALIC,
    ),
    ChainStage(
        order=4,
        name="حقلُ التضييق",
        what_it_is="اعتراضُ مجرى الهواء بدرجاتٍ، من الجريان المقيَّد إلى الإغلاق",
        what_it_is_not="ليس مكانًا بعدُ؛ فالمكانُ تعيينٌ لاحقٌ داخل الحقل",
        branch=Branch.CONSONANTAL,
    ),
    ChainStage(
        order=5,
        name="مرشّحُ حدّ الإغلاق (الهمزة)",
        what_it_is="أقصى حدٍّ أدنى من الإغلاق: مفتوحٌ ← مغلقٌ ← انطلاق",
        what_it_is_not=(
            "ليست أمًّا للحروف، ولا أصلًا تاريخيًّا ولا فيزيائيًّا لبقيّة " "الصوامت"
        ),
        branch=Branch.CONSONANTAL,
    ),
    ChainStage(
        order=6,
        name="الأليافُ الصامتيّة",
        what_it_is=(
            "تعييناتٌ فوق الحقل: درجةُ الإغلاق، والمكان، والكيفيّة، والتصويت، "
            "والاستمرار، والانطلاق"
        ),
        what_it_is_not="ليست مفردةَ الحروف الثمانيةِ والعشرين، ولا تُنتِجها بذاتها",
        branch=Branch.CONSONANTAL,
    ),
    ChainStage(
        order=7,
        name="الخانةُ الدنيا المكتملة (C+H)",
        what_it_is=(
            "صامتٌ وحركةٌ في وحدةٍ واحدةٍ تُغلق المستوى الأدنى، وهويّةُ الصامت "
            "محفوظةٌ داخلها لا مُلغاةٌ فيها"
        ),
        what_it_is_not="ليست مقطعًا ولا جذرًا؛ وبناؤهما يبدأ بعدها لا معها",
        branch=Branch.SHARED,
    ),
)
"""السلسلةُ المُسجَّلة، كلُّ طورٍ بحدّه وبمساره."""


CONSTRICTION_GEOMETRY: Final[tuple[str, ...]] = (
    "حنجريّ",
    "حلقيّ",
    "لهويّ",
    "طبقيّ",
    "غاريّ",
    "أسنانيّ/لثويّ",
    "شفويّ",
)
"""ترتيبُ مواضع التضييق هندسيًّا من الحنجرة إلى الشفتين — لا اشتقاقًا سببيًّا."""


@dataclass(frozen=True, slots=True)
class MechanicalProbe:
    """مَسبارٌ ميكانيكيّ: سؤالُه، وما يؤكّده، **وما يُبطله**، وأداتُه."""

    symbol: str
    name: str
    question: str
    what_would_confirm: str
    what_would_falsify: str
    instrument_required: str

    def __post_init__(self) -> None:
        if not self.what_would_falsify.strip():
            raise PreArticulatoryError(
                "مَسبارٌ بلا شرطِ إبطالٍ يُثبَّت مهما جاءت البيانات؛ " "وذلك سؤالٌ لا اختبار"
            )
        if not self.instrument_required.strip():
            raise PreArticulatoryError(
                "مَسبارٌ بلا أداةٍ مُسمّاةٍ لا يُعرَف أيُمكن تشغيلُه اليوم أم لا"
            )
        if self.what_would_confirm.strip() == self.what_would_falsify.strip():
            raise PreArticulatoryError(
                "شرطُ التأكيد وشرطُ الإبطال واحدٌ؛ وشرطان متطابقان لا يفصلان"
            )


PROBES: Final[tuple[MechanicalProbe, ...]] = (
    MechanicalProbe(
        symbol="ء",
        name="مَسبارُ حدّ الإغلاق",
        question="أوُلِد الإغلاق؟ أي: هل انقطع الجريانُ انقطاعًا تامًّا ثمّ انطلق",
        what_would_confirm=(
            "انقطاعٌ تامٌّ مقيسٌ في الجريان يتلوه انطلاقٌ، في موضعٍ حنجريّ، "
            "على تسجيلاتٍ مُبصَّمةٍ بمتحدّثين متعدّدين"
        ),
        what_would_falsify=(
            "بقاءُ جريانٍ مقيسٍ خلال ما يُوسَم همزةً في أغلب المواضع، أو عدمُ "
            "تمايزِ الانقطاع عن تضييقٍ شديدٍ بحدٍّ مُعلَنٍ قبل القياس"
        ),
        instrument_required="تسجيلٌ صوتيٌّ مُبصَّم، أو قياسُ تدفّقٍ/ضغطٍ فمويّ",
    ),
    MechanicalProbe(
        symbol="ع",
        name="مَسبارُ التضييق الحلقيّ",
        question="أوُلِد التضييقُ الحلقيُّ مع بقاء الحامل الصوتيّ جاريًا",
        what_would_confirm=(
            "تضييقٌ حلقيٌّ مقيسٌ مع استمرارِ جريانٍ مجهورٍ بلا انقطاع، "
            "متمايزٌ عن الإغلاق بحدٍّ مُعلَنٍ قبل القياس"
        ),
        what_would_falsify=(
            "انقطاعُ الجريان فيما يُوسَم عينًا، أو انعدامُ تمايزٍ حلقيٍّ عن "
            "بقيّة الحلقيّات بالأداة نفسها"
        ),
        instrument_required="تسجيلٌ صوتيٌّ مُبصَّم مع قياسٍ حلقيٍّ أو تصويرٍ للمجرى",
    ),
)
"""المَسباران، كلٌّ بسؤاله وشرطَي تأكيده وإبطاله وأداته."""


DEPOSITED_SIGNAL_SOURCES: Final[tuple[str, ...]] = ()
"""مصادرُ الإشارة المُودَعة. **فارغة**: لم تصل إلى هذه الشجرة إشارةٌ ألبتّة."""


@dataclass(frozen=True, slots=True)
class BlockingResidual:
    """الباقي المانعُ من التشغيل، وشرطُ رفعه مكتوبًا معه."""

    code: str
    what_blocks: str
    what_lifts_it: str

    def __post_init__(self) -> None:
        if not self.what_lifts_it.strip():
            raise PreArticulatoryError("باقٍ بلا شرطِ رفعٍ مكتوبٍ باقٍ يُرفَع متى شاء رافعُه")


BLOCKING_RESIDUAL: Final[BlockingResidual] = BlockingResidual(
    code="NO_SIGNAL_HAS_REACHED_THIS_TREE",
    what_blocks=(
        "المُودَعُ في هذه الشجرة رسمٌ كلُّه — Tanzil وQAC والمقاييس — ولا "
        "بايتَ صوتٍ واحد. والرسمُ لا يرى الإغلاقَ ولا الجريان، فلا يُشغَّل "
        "مَسبارٌ ميكانيكيٌّ على حرفٍ مكتوب"
    ),
    what_lifts_it=(
        "إيداعُ تسجيلاتٍ مُبصَّمةٍ بمصدرٍ مسمًّى ومتحدّثين معدودين، مع "
        "`MeasurementRunManifest` يُبيّن الأداةَ وحدَّ التمايز؛ وعندها "
        "يُشغَّل المَسباران على ما سُجِّل قبلَهما لا بعدَهما"
    ),
)
"""المانعُ اليوم، وشرطُ رفعه؛ ولا يُرفَع بنثرٍ ولا بتقديرٍ."""


def is_testable_today() -> bool:
    """أيُشغَّل شيءٌ من هذا اليوم؟ مُشتَقٌّ من وجود إيداعٍ لا مكتوبٌ في حقل."""

    return bool(DEPOSITED_SIGNAL_SOURCES)


def branch_stages(branch: Branch) -> tuple[ChainStage, ...]:
    """أطوارُ مسارٍ بعينه، مرتّبةً برتبتها كما سُجِّلت."""

    return tuple(
        sorted(
            (stage for stage in PRE_ARTICULATORY_CHAIN if stage.branch is branch),
            key=lambda stage: stage.order,
        )
    )


def derive_branch_depths() -> tuple[tuple[Branch, int], ...]:
    """عددُ أطوار كلّ مسارٍ الخاصّةِ به، مُشتَقًّا بالعدّ لا مكتوبًا."""

    return tuple(
        (branch, len(branch_stages(branch)))
        for branch in (Branch.SHARED, Branch.VOCALIC, Branch.CONSONANTAL)
    )


def branch_depth_asymmetry() -> int:
    """كم يزيد مسارُ الصامت على مسار الصائت طورًا قبل الخانة الدنيا؟

    والفرقُ يُخرَج ولا يُملَّس. ويتقابل حقلُ التضييق مع الحقل الصائتيّ، وتتقابل
    الأليافُ الصامتيّة مع الهندسة الصائتيّة، فيبقى **مرشّحُ حدّ الإغلاق** وحدَه
    بلا نظير. وهذه خاصّيّةُ المقترَح نفسِه، فتُسجَّل خبرًا عنه لا عيبًا يُسوّى
    بترقيمٍ.
    """

    depths = dict(derive_branch_depths())
    return depths[Branch.CONSONANTAL] - depths[Branch.VOCALIC]


def probe_named(symbol: str) -> MechanicalProbe:
    """اقرأ مَسبارًا برمزه؛ ورمزٌ غيرُ مُسجَّلٍ يُرَدُّ ولا يُحمَل على أقربه."""

    for probe in PROBES:
        if probe.symbol == symbol:
            return probe
    raise PreArticulatoryError(
        f"لا مَسبارَ مُسجَّلٌ بالرمز {symbol!r}؛ وغيابُ المَسبار ليس نفيًا لسؤاله."
    )


THE_BASE_IS_BELOW_THE_DEPOSITED_INVENTORY_NOTE: Final[str] = (
    "TheBaseIsBelowTheDepositedInventory: أليافُ الشجرة كلُّها قاعدتُها تفترض "
    "مفردةَ الحروف، والمقترَحُ يدفع القاعدةَ تحت المخرج؛ وهذه النقلةُ بعينها "
    "ما يجعلها غيرَ قابلةٍ للقياس بما أُودِع"
)

NO_SIGNAL_HAS_REACHED_THIS_TREE_NOTE: Final[str] = (
    "NoSignalHasReachedThisTree: المُودَعُ رسمٌ كلُّه ولا بايتَ صوتٍ واحد؛ "
    "والرسمُ لا يرى الإغلاقَ ولا الجريان، فالمانعُ مُسمًّى وشرطُ رفعه معه"
)

A_PREREGISTRATION_IS_NOT_A_RESULT_NOTE: Final[str] = (
    "APreregistrationIsNotAResult: كلُّ ما هنا توقّعٌ مكتوبٌ قبل العدّ؛ ومن "
    "استشهد بتسجيلٍ مسبقٍ نتيجةً استشهد بنيّةٍ على فعل"
)

THE_ORDER_IS_GEOMETRIC_NOT_CAUSAL_NOTE: Final[str] = (
    "TheOrderIsGeometricNotCausal: ترتيبُ المواضع من الحنجرة إلى الشفتين "
    "هندسيّ، ولا يُقرأ ادّعاءَ أنّ كلَّ حرفٍ يتولّد سببيًّا ممّا قبله"
)

HAMZA_IS_A_BOUNDARY_CANDIDATE_NOTE: Final[str] = (
    "HamzaIsABoundaryCandidateNotAMotherOfLetters: الهمزةُ أوّلُ مرشّحٍ واضحٍ "
    "لحدّ الإغلاق لا أصلٌ لبقيّة الصوامت؛ ومن قرأها أمًّا حمّل المَسبارَ دعوى "
    "نسبٍ لم تُختبَر"
)

AIN_IS_A_PROBE_NOT_AN_ORIGIN_NOTE: Final[str] = (
    "AinIsAProbeNotAnOrigin: العينُ نقطةٌ في هندسة التضييق تُختبَر عند الرجوع "
    "من الصائت المفتوح، لا أصلٌ مفترَضٌ لكلّ حركة"
)

A_PROBE_WITHOUT_A_FALSIFIER_IS_NOT_A_PROBE_NOTE: Final[str] = (
    "AProbeWithoutAFalsifierIsNotAProbe: شرطُ الإبطال شرطُ إنشاء؛ ومَسبارٌ لا "
    "يُقال فيه ما يُبطله يُثبَّت مهما جاءت البيانات"
)

THE_TWO_PATHS_ARE_NOT_EQUALLY_DEEP_NOTE: Final[str] = (
    "TheTwoPathsAreNotEquallyDeep: مسارُ الصامت يزيد على مسار الصائت طورًا "
    "واحدًا قبل الخانة الدنيا. ويتقابل حقلُ التضييق مع V₀، وتتقابل الأليافُ "
    "الصامتيّة مع الهندسة الصائتيّة، فيبقى **مرشّحُ حدّ الإغلاق** بلا نظيرٍ "
    "في مسار الصائت؛ وهذا خبرٌ عن المقترَح لا عيبٌ يُسوّى بترقيم"
)

IT_IS_NOT_A_BUNDLE_NOTE: Final[str] = (
    "ItIsNotABundleAndLocalTrivialityIsNotTheGate: التفاهةُ الموضعيّة فوق "
    "قاعدةٍ منفصلةٍ منتهيةٍ تُحصَّل مجّانًا، والشرطُ الساقطُ ثباتُ الليف "
    "النموذجيّ وهو مقيسٌ فاشلٌ فوق الحروف؛ فالتسميةُ بنيةٌ ليفيّةٌ مرخَّصة"
)

PRE_ARTICULATORY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_BASE_IS_BELOW_THE_DEPOSITED_INVENTORY_NOTE,
    NO_SIGNAL_HAS_REACHED_THIS_TREE_NOTE,
    A_PREREGISTRATION_IS_NOT_A_RESULT_NOTE,
    THE_ORDER_IS_GEOMETRIC_NOT_CAUSAL_NOTE,
    HAMZA_IS_A_BOUNDARY_CANDIDATE_NOTE,
    AIN_IS_A_PROBE_NOT_AN_ORIGIN_NOTE,
    A_PROBE_WITHOUT_A_FALSIFIER_IS_NOT_A_PROBE_NOTE,
    THE_TWO_PATHS_ARE_NOT_EQUALLY_DEEP_NOTE,
    IT_IS_NOT_A_BUNDLE_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if is_testable_today():  # pragma: no cover - حارس
    raise RuntimeError(
        "أُودِعت إشارةٌ ولم يُحدَّث الباقي المانع؛ وباقٍ قائمٌ بعد رفع سببه "
        "يُخفي أنّ التشغيلَ صار ممكنًا."
    )
if len({probe.symbol for probe in PROBES}) != len(PROBES):  # pragma: no cover - حارس
    raise RuntimeError("مَسباران برمزٍ واحد؛ ورمزٌ يسمّي مَسبارين يُستشهَد به على نفسه.")
