"""جبرُ الحوافّ الثلاث: ابتداءٌ ووصلٌ ووقف، وما تفعله كلُّ حافّةٍ بالعدّ.

**ما تفعله هذه الوحدة**: تُقيِّد الحوافَّ الثلاثَ نوعًا مغلقًا، وتُسمّي لكلّ
حافّةٍ بوّابتَها المُجمَّدة، ثمّ **تشتقّ بالحساب** أثرَ كلّ حافّةٍ في العدّ
الأساسيّ: الابتداءُ يُفرِز صنفًا جديدًا ولا يُنقِص عضوًا، والوصلُ هو الأساسُ
نفسُه، والوقفُ **محجوبٌ بقرارٍ معلَّق** فلا يُخرَج له عددٌ ههنا.

`THE_WASL_COUNT_IS_THE_BASE_NOT_A_CORRECTION`: العدّ الذي بُني (٨٤ ثمّ ٢٣٥٢
ثمّ ٦٥٨٥٦) هو **قراءةُ الوصل** لا قراءةً محايدة. فلا يُقال إنّ الوصلَ يُعدِّله؛
بل هو هو. وكلُّ عددٍ ههنا يحمل حافّتَه في بنيته، ولا يُقرأ عددٌ بلا حافّته —
على منوال `THE_INCLUSION_POLICY_IS_DECLARED_BEFORE_THE_COUNT` في
`slot_rights_algebra`.

`A_REPAIR_IS_NOT_A_MEMBER`: «اُنْصُرْ» و«اِضْرِبْ» و«اِفْتَحْ» جذورُها تبدأ
بعنقودٍ ساكن، وهذا يخالف «لا يُبتدأ بساكن»؛ فهمزةُ الوصل فيها **إصلاحٌ
اضطراريّ** لا عضوٌ أصيلٌ في مجموعة الـ٨٤. ولذلك صنفٌ مستقلٌّ اسمُه «بنيةٌ تحتاج
إصلاحًا ابتدائيًّا»، وحارسٌ يشترط أن يكون تقاطعُه مع الأساس **صفرًا**.

`THE_ONSET_GATE_SUBTRACTS_NOTHING`: بنيةُ `CV` تبدأ دائمًا بصامتٍ يحمل حركةً
حقيقيّة، فلا تخالف قاعدةَ الابتداء بحال؛ والعددُ يبقى كما هو. وهذا **مفحوصٌ
بالطرح** لا معلَنٌ خبرًا: عددُ ما يحتاج إصلاحًا من أعضاء الأساس صفر.

`THE_WAQF_LOSS_IS_INFORMATION_NOT_RECLASSIFICATION`: الوقفُ ليس إعادةَ تصنيف؛
هو **فقدُ معلومة**: حركةُ الحافّة اليمنى تُحيَّد إلى سكون فلا تُستردّ من
المنطوق. ولذلك لا يُحسَب «عددُ الوقف» قبل أن يُحسَم بأيّ محورٍ تُحدَّد الحركةُ
الساقطة، و`waqf_count` ترفع الحجبَ باسم القرار ولا تُرجِع رقمًا تقديريًّا.

`A_STRUCTURAL_VOWEL_CAN_ALSO_DROP`: «نَصَرَ» فعلٌ ماضٍ مبنيّ، وفتحتُه الأخيرةُ
**بنيويّةٌ لا إعرابيّة**، ومع ذلك يتحوّل `CV.CV.CV` إلى `CV.CVC` عند الوقف.
فالعلامةُ الثنائيّةُ (بنيويّة/إعرابيّة) **لا تكفي** وحدَها لحساب عدد الوقف،
إذ المُسقِطُ قد يكون الموقعَ لا الإعراب. وهذا هو بعينه سؤالُ `ق-4`، ويُسجَّل
سؤالًا لا يُحسَم ههنا.

`A_GATE_WITHOUT_ITS_BYTES_IS_A_NAME`: البوّاباتُ الثلاثُ **ليست بايتاتُها في
هذه الشجرة**، فهي إحالاتٌ بأسمائها ومنزلتُها «غيرُ محسوم» بنصّ قاعدة التصديق،
لا تواضعًا. وحارسٌ يردّ أن تُوسَم بوّابةٌ مصدَّقةً وبايتاتُها غائبة.

`AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION`: ما يجري هنا اشتقاقٌ من محورين
مُعلَنَين (حاملٌ وعلامة) ومقابلةٌ بأرقامٍ منشورة، لا إعادةُ اشتقاقٍ من مدوّنة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .decision_register import assert_not_reportable_as_done

__all__ = [
    "A_GATE_WITHOUT_ITS_BYTES_IS_A_NAME_NOTE",
    "AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE",
    "A_REPAIR_IS_NOT_A_MEMBER_NOTE",
    "A_STRUCTURAL_VOWEL_CAN_ALSO_DROP_NOTE",
    "CONSONANT_CARRIERS",
    "EDGE_STATE_NAMED_RESIDUALS",
    "FROZEN_GATES",
    "INITIAL_REPAIR_CLASS",
    "PUBLISHED_CV_CELLS",
    "PUBLISHED_WASL_COUNTS",
    "REAL_VOWELS",
    "THE_ONSET_GATE_SUBTRACTS_NOTHING_NOTE",
    "THE_WAQF_LOSS_IS_INFORMATION_NOTE",
    "THE_WASL_COUNT_IS_THE_BASE_NOTE",
    "WAQF_BLOCKED_ITEM",
    "Certification",
    "Edge",
    "EdgeStateError",
    "FrozenGate",
    "InitialShape",
    "Mark",
    "OnsetPartition",
    "OnsetStanding",
    "WaslCount",
    "derive_cv_cells",
    "derive_onset_partition",
    "derive_wasl_counts",
    "gate_of",
    "waqf_count",
]


class EdgeStateError(ValueError):
    """رُفض مدخلٌ أو حكمٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class Edge(Enum):
    """الحوافُّ الثلاثُ التي تُقرأ عندها البنيةُ الواحدة، ولا رابعةَ لها."""

    IBTIDA = "ابتداء"
    WASL = "وصل"
    WAQF = "وقف"


class Certification(Enum):
    """منزلةُ التصديق؛ ولا تبلغ `CERTIFIED` إلّا ببايتاتٍ حاضرةٍ في الشجرة."""

    CERTIFIED = "مصدَّق: بايتاتُ البوّابة في الشجرة"
    UNDETERMINED = "غيرُ محسوم: إحالةٌ بالاسم"


class Mark(Enum):
    """علاماتُ الخانة الأربع، وهي محورُ العلامة في `CV-112` كما أُعلن."""

    FATHA = "فتحة"
    KASRA = "كسرة"
    DAMMA = "ضمة"
    SUKUN = "سكون"


REAL_VOWELS: Final[tuple[Mark, ...]] = tuple(
    mark for mark in Mark if mark is not Mark.SUKUN
)
"""الحركاتُ الحقيقيّة، مُشتَقّةً بإخراج السكون من المحور لا بتعدادٍ مكتوب."""

BARE_CONSONANTS: Final[int] = 26
"""الصوامتُ كما أُعلنت في ٥د: «26 صامتًا» قبل ضمّ الواو والياء."""

SEMIVOWEL_CARRIERS: Final[tuple[str, ...]] = ("و", "ي")
"""«مع الواو والياء في موقع الصامت»، وهما ما يُضمّ إلى الستّة والعشرين."""

CONSONANT_CARRIERS: Final[int] = BARE_CONSONANTS + len(SEMIVOWEL_CARRIERS)
"""الحواملُ في موقع الصامت، مُشتَقّةً بالجمع لا مكتوبةً رقمًا واحدًا."""

PUBLISHED_CV_CELLS: Final[int] = 112
"""ما نُشر في ٥د: «الخلايا الـ 112»؛ ويُقابَل بالمُشتَقّ ولا يُستبدَل به."""

PUBLISHED_WASL_COUNTS: Final[tuple[int, ...]] = (84, 2_352, 65_856)
"""الأعدادُ الثلاثةُ كما وردت في الصياغة، ويُقابَل كلٌّ منها بمُشتَقّه."""


def derive_cv_cells() -> int:
    """فضاءُ `CV-112`: حاملٌ × علامة، مُشتَقًّا بالضرب لا منقولًا رقمًا."""

    return CONSONANT_CARRIERS * len(Mark)


@dataclass(frozen=True, slots=True)
class WaslCount:
    """عددٌ من أعداد الوصل: رتبتُه، ومُشتَقُّه، والمنشورُ الذي يُقابَل به."""

    rank: int
    derived: int
    published: int

    def __post_init__(self) -> None:
        if self.rank < 1:
            raise EdgeStateError("رتبةُ العدّ موجبة؛ ورتبةٌ صفريّةٌ ليست بنية.")

    @property
    def matches_published(self) -> bool:
        """هل يطابق المُشتَقُّ المنشور؟ ولا يُصحَّح أحدُهما بالآخر صمتًا."""

        return self.derived == self.published

    @property
    def edge(self) -> Edge:
        """حافّةُ هذا العدّ، وهي الوصلُ لا غيرُه؛ فلا يُقرأ عددٌ بلا حافّته."""

        return Edge.WASL


def derive_wasl_counts() -> tuple[WaslCount, ...]:
    """اشتقّ أعدادَ الوصل الثلاثة: `CV` ثمّ ما يزيده كلُّ حاملٍ بعده.

    الأساسُ `حاملٌ × حركةٌ حقيقيّة`، ثمّ يُضرَب في عدد الحوامل مرّةً لكلّ
    خانةٍ صامتةٍ تُضاف. والمنشورُ يُقابَل ولا يُكتَب في موضع المُشتَقّ.
    """

    counts: list[WaslCount] = []
    value = CONSONANT_CARRIERS * len(REAL_VOWELS)
    for rank, published in enumerate(PUBLISHED_WASL_COUNTS, start=1):
        counts.append(WaslCount(rank=rank, derived=value, published=published))
        value *= CONSONANT_CARRIERS
    return tuple(counts)


@dataclass(frozen=True, slots=True)
class FrozenGate:
    """بوّابةُ حافّةٍ مُجمَّدة: معرِّفُها، وحضورُ بايتاتها، ومنزلةُ تصديقها."""

    edge: Edge
    identifier: str
    statement: str
    bytes_present: bool

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise EdgeStateError("بوّابةٌ بلا معرِّفٍ لا يُحال إليها باسمها.")
        if not self.statement.strip():
            raise EdgeStateError(
                f"{self.identifier}: نصُّ البوّابة شرطُ إنشاء؛ ومعرِّفٌ بلا نصٍّ "
                "يُستشهَد به ولا يُراجَع."
            )

    @property
    def certification(self) -> Certification:
        """منزلةُ التصديق، مُشتَقّةً من حضور البايتات لا مكتوبةً حقلًا."""

        return (
            Certification.CERTIFIED
            if self.bytes_present
            else Certification.UNDETERMINED
        )


FROZEN_GATES: Final[tuple[FrozenGate, ...]] = (
    FrozenGate(
        edge=Edge.IBTIDA,
        identifier="IBTIDA-SUKUN-EXCLUSION-AR-1",
        statement="لا يبدأ الكلامُ بساكن",
        bytes_present=False,
    ),
    FrozenGate(
        edge=Edge.WASL,
        identifier="WASL-HAMZA-ELISION-AR-1",
        statement="همزةُ الوصل تسقط في الدرج، والكلمةُ السابقةُ تمنح النواة",
        bytes_present=False,
    ),
    FrozenGate(
        edge=Edge.WAQF,
        identifier="WAQF-TANWEEN-CARRIER-AR-1",
        statement="حركةُ الحافّة اليمنى تُخلى، وتنوينُ الفتح يصير مدًّا",
        bytes_present=False,
    ),
)
"""البوّاباتُ الثلاثُ بأسمائها؛ وبايتاتُها ليست ههنا، فمنزلتُها غيرُ محسوم."""


def gate_of(edge: Edge) -> FrozenGate:
    """بوّابةُ حافّةٍ بعينها؛ وحافّةٌ بلا بوّابةٍ تُرَدُّ ولا تُحمَل على أقربها."""

    for gate in FROZEN_GATES:
        if gate.edge is edge:
            return gate
    raise EdgeStateError(  # pragma: no cover - حارس
        f"لا بوّابةَ مُسجَّلةٌ للحافّة «{edge.value}»."
    )


class OnsetStanding(Enum):
    """منزلةُ البنية عند حافّة الابتداء؛ ولا منزلةَ ثالثةٌ اسمُها «مقبول تجاوزًا»."""

    WELL_FORMED_ONSET = "مستقيمُ الابتداء: صامتٌ بحركةٍ حقيقيّة"
    NEEDS_INITIAL_REPAIR = "يحتاج إصلاحًا ابتدائيًّا: عنقودٌ ساكنٌ في الأوّل"


@dataclass(frozen=True, slots=True)
class InitialShape:
    """بنيةٌ بأوّلِ علامتها ومثالها؛ ومنزلةُ ابتدائها مُشتَقّةٌ من العلامة."""

    label: str
    example: str
    first_mark: Mark
    repair: str = ""

    def __post_init__(self) -> None:
        if not self.label.strip() or not self.example.strip():
            raise EdgeStateError("بنيةٌ بلا اسمٍ أو بلا مثالٍ لا تُقيَّد.")
        if self.standing is OnsetStanding.NEEDS_INITIAL_REPAIR:
            if not self.repair.strip():
                raise EdgeStateError(
                    f"{self.label}: بنيةٌ تخالف الابتداءَ بلا إصلاحٍ مُسمًّى؛ "
                    "والإصلاحُ يُسمّى وإلّا قُرئت المخالفةُ عضوًا أصيلًا."
                )
        elif self.repair.strip():
            raise EdgeStateError(
                f"{self.label}: بنيةٌ مستقيمةُ الابتداء بإصلاحٍ مذكور؛ "
                "وإصلاحٌ بلا مخالفةٍ يُدخِل الاضطراريَّ في الأصيل."
            )

    @property
    def standing(self) -> OnsetStanding:
        """المنزلةُ مُشتَقّةٌ من أوّل العلامة: السكونُ مخالفة، وما سواه استقامة."""

        return (
            OnsetStanding.NEEDS_INITIAL_REPAIR
            if self.first_mark is Mark.SUKUN
            else OnsetStanding.WELL_FORMED_ONSET
        )


INITIAL_REPAIR_CLASS: Final[tuple[InitialShape, ...]] = (
    InitialShape(
        label="صفّ ١١ — أمرُ «نصر»",
        example="اُنْصُرْ",
        first_mark=Mark.SUKUN,
        repair="همزةُ وصلٍ بضمّة",
    ),
    InitialShape(
        label="صفّ ١٢ — أمرُ «ضرب»",
        example="اِضْرِبْ",
        first_mark=Mark.SUKUN,
        repair="همزةُ وصلٍ بكسرة",
    ),
    InitialShape(
        label="صفّ ١٣ — أمرُ «فتح»",
        example="اِفْتَحْ",
        first_mark=Mark.SUKUN,
        repair="همزةُ وصلٍ بكسرة",
    ),
)
"""صنفُ «بنيةٌ تحتاج إصلاحًا ابتدائيًّا»، وهو **خارجُ** الأساس لا عضوٌ فيه."""


@dataclass(frozen=True, slots=True)
class OnsetPartition:
    """قسمةُ الابتداء: أساسٌ لا ينقص، وصنفُ إصلاحٍ منفصلٌ عنه انفصالًا مفحوصًا."""

    base_before: int
    base_after: int
    repair_members: int
    overlap_with_base: int

    def __post_init__(self) -> None:
        if self.overlap_with_base:
            raise EdgeStateError(
                "صنفُ الإصلاح يتقاطع مع الأساس؛ والإصلاحُ الاضطراريُّ لا يُعَدّ "
                "عضوًا أصيلًا، فالقسمةُ تُرَدُّ ولا تُقرَّب."
            )
        if self.repair_members < 1:
            raise EdgeStateError("صنفُ إصلاحٍ فارغٌ لا يُقيَّد صنفًا؛ وتصنيفٌ بلا عضوٍ دعوى.")

    @property
    def base_is_unchanged(self) -> bool:
        """هل بقي الأساسُ بلا نقصان؟ مُشتَقًّا بالطرح لا معلَنًا خبرًا."""

        return self.base_after - self.base_before == 0


def derive_onset_partition() -> OnsetPartition:
    """اقسِمْ عند حافّة الابتداء، واشتقّ الانفصالَ والنقصانَ بالحساب.

    وأعضاءُ الأساس كلُّهم `CV`: صامتٌ بحركةٍ حقيقيّة، فلا واحدَ منهم يخالف
    «لا يُبتدأ بساكن». ولذلك التقاطعُ صفرٌ **بالاشتقاق** لا بالدعوى: يُعَدّ
    من أعضاء صنف الإصلاح ما كانت أولى علامته حركةً حقيقيّة، فيكون عددُه
    مقدارَ التقاطع.
    """

    base = CONSONANT_CARRIERS * len(REAL_VOWELS)
    overlap = sum(
        1 for shape in INITIAL_REPAIR_CLASS if shape.first_mark in REAL_VOWELS
    )
    return OnsetPartition(
        base_before=base,
        base_after=base - overlap,
        repair_members=len(INITIAL_REPAIR_CLASS),
        overlap_with_base=overlap,
    )


WAQF_BLOCKED_ITEM: Final[str] = "إعلانُ عددِ الوقف"
"""ما يحجُبه `ق-4`؛ ويُكتَب هنا بنصّه ليُطابِق ما في سجلّ القرارات."""


def waqf_count() -> int:
    """عددُ الوقف — **محجوبٌ** بقرارٍ معلَّق، فيُرفَع الحجبُ ولا يُلفَّق رقم.

    والحجبُ ليس عجزًا: الوقفُ فقدُ معلومةٍ لا إعادةَ تصنيف، وحسابُ المفقود
    يقتضي أن يُحسَم أوّلًا بأيّ محورٍ تُحدَّد الحركةُ الساقطة — وهو `ق-4`.
    """

    assert_not_reportable_as_done(WAQF_BLOCKED_ITEM)
    raise EdgeStateError(  # pragma: no cover - لا يُبلَغ ما دام ق-4 معلَّقًا
        "عددُ الوقف لا يُخرَج إلّا بفرعٍ مُسمًّى من ق-4."
    )


THE_WASL_COUNT_IS_THE_BASE_NOTE: Final[str] = (
    "TheWaslCountIsTheBaseNotACorrection: ٨٤ و٢٣٥٢ و٦٥٨٥٦ قراءةُ الوصل لا "
    "قراءةٌ محايدة؛ فلا يُقال إنّ الوصلَ يُعدّلها، ولا يُقرأ عددٌ بلا حافّته"
)

THE_ONSET_GATE_SUBTRACTS_NOTHING_NOTE: Final[str] = (
    "TheOnsetGateSubtractsNothing: بنيةُ CV تبدأ بصامتٍ بحركةٍ حقيقيّة فلا "
    "تخالف قاعدةَ الابتداء بحال؛ والنقصانُ صفرٌ مفحوصٌ بالطرح لا معلَنٌ خبرًا"
)

A_REPAIR_IS_NOT_A_MEMBER_NOTE: Final[str] = (
    "ARepairIsNotAMember: همزةُ الوصل في اُنْصُرْ واِضْرِبْ واِفْتَحْ إصلاحٌ "
    "اضطراريٌّ لا عضوٌ أصيل؛ فصنفُها مستقلٌّ وتقاطعُه مع الأساس صفرٌ بالحارس"
)

THE_WAQF_LOSS_IS_INFORMATION_NOTE: Final[str] = (
    "TheWaqfLossIsInformationNotReclassification: الوقفُ يُحيّد حركةَ الحافّة "
    "إلى سكونٍ فتُفقَد المعلومة؛ وعددُه محجوبٌ بق-4 لا يُخرَج تقديرًا"
)

A_STRUCTURAL_VOWEL_CAN_ALSO_DROP_NOTE: Final[str] = (
    "AStructuralVowelCanAlsoDrop: فتحةُ «نَصَرَ» الأخيرةُ بنيويّةٌ لا إعرابيّة "
    "وتسقط عند الوقف؛ فالعلامةُ الثنائيّةُ لا تكفي وحدَها، وقد يكون المُسقِطُ "
    "الموقعَ لا الإعراب"
)

A_GATE_WITHOUT_ITS_BYTES_IS_A_NAME_NOTE: Final[str] = (
    "AGateWithoutItsBytesIsAName: البوّاباتُ الثلاثُ ليست بايتاتُها في هذه "
    "الشجرة، فهي إحالاتٌ بأسمائها ومنزلتُها غيرُ محسومٍ بنصّ القاعدة"
)

AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE: Final[str] = (
    "AnInternalCheckIsNotARederivation: اشتقاقٌ من محورين مُعلَنَين ومقابلةٌ "
    "بأرقامٍ منشورة، لا إعادةُ اشتقاقٍ من مدوّنة"
)

EDGE_STATE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_WASL_COUNT_IS_THE_BASE_NOTE,
    THE_ONSET_GATE_SUBTRACTS_NOTHING_NOTE,
    A_REPAIR_IS_NOT_A_MEMBER_NOTE,
    THE_WAQF_LOSS_IS_INFORMATION_NOTE,
    A_STRUCTURAL_VOWEL_CAN_ALSO_DROP_NOTE,
    A_GATE_WITHOUT_ITS_BYTES_IS_A_NAME_NOTE,
    AN_INTERNAL_CHECK_IS_NOT_A_REDERIVATION_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


if len(FROZEN_GATES) != len(Edge):  # pragma: no cover - حارس
    raise RuntimeError("حافّةٌ بلا بوّابة؛ وحافّةٌ لا بوّابةَ لها تُقرأ بلا قيد.")

if any(gate.certification is Certification.CERTIFIED for gate in FROZEN_GATES):
    raise RuntimeError(  # pragma: no cover - حارس
        "بوّابةٌ مصدَّقةٌ وبايتاتُها غائبةٌ عن الشجرة؛ والتصديقُ يشترط البايتات."
    )
