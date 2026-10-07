"""عقدُ إيداعِ ترتيبِ مخارجَ منسوبًا إلى طبعةٍ بجزئها وصفحتها، وفرقٌ مُشتَقّ.

**ما تفعله هذه الوحدة**: تبني عقدَ الإيداع الذي يشترطه
`gflk_feature_table_import_barrier` لرفعِ حاجزِ جدول المخرج — طبعةٌ مسمّاةٌ
بمحقّقها وناشرها وسنتها **وجزئها وصفحتها**، وترتيبُها مُودَعًا ببصمةٍ تُعاد
اشتقاقًا، ودالّةُ مقابلةٍ **تُشغَّل** على `CLASSICAL_MAKHARIJ` رتبةً برتبةٍ
وحرفًا بحرف. ولا تُودِع طبعةً اليوم: `DEPOSITED_EDITION_ORDERINGS` **فارغة**.

`A_NAMED_EDITION_IS_NOT_A_DEPOSITED_PAGE`: تسميةُ كتابٍ ليست إيداعَ طبعة.
فالحقولُ السبعةُ — العنوانُ والمحقّقُ والناشرُ وسنةُ الطبع والجزءُ والصفحةُ
والمُقتبَسُ المُودَع — **كلُّها شرطُ إنشاءٍ لا وصفٌ اختياريّ**، وواحدٌ منها
فارغٌ يُبطِل الإنشاء. وهذا هو بعينه ما منع الإيداعَ اليوم: لم تصل إلى هذه
الشجرة صفحةٌ من طبعةٍ بعينها، فبقي الموضعُ مسنونًا وبقيت البايتاتُ خارجَه، على
منوال `corpora/MASAQ.csv` و`MEASURED_SAKIN_CLASH_SOURCES`.

`THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT`: تعارضُ ١٣/١٦ لم يُحسَم بعد،
وقرارُ حسمِه مُسجَّلٌ هنا `NOT_TAKEN` بسؤاله المفتوح المُسمَّى في
`gflk_milestone_blocking_registration`. والقاعدةُ **محروسةٌ بنيويًّا لا موصوفةً
بالنثر**: ما دام القرارُ غيرَ متّخَذٍ فلا إيداعَ يُقبَل، ويُرفَض عند الاستيراد
لا بعده. فلا يقع الإيداعُ ثمّ يُنظَر في التعارض، فيصير الاختيارُ بين رقمين
تابعًا للنتيجة المرغوبة.

`THE_FROZEN_TABLE_CONTRADICTS_ITS_OWN_ATTESTATION`: وقد ظهر بالمقابلة شيءٌ لم
يكن مقصودًا من هذه الوحدة، ولا يحتاج مصدرًا خارجيًّا أصلًا: **الجدولُ
المُبصَّم يخالف نسبتَه المكتوبة في `CLASSICAL_SOURCE_ATTESTATION`.** النسبةُ
تقول «الشفتان اثنان»، والجدولُ يحمل ثلاثةَ مخارجَ شفويّة (ف؛ ب م؛ و)، لأنّ
الواوَ فُصلت عن الباء والميم. ومن هنا جاء الفائضُ كلُّه: السبعةَ عشرَ ناقصةً
الجوفَ والخيشومَ المُعلَنَين خارجَ الترقيم تُعطي خمسةَ عشرَ، والمُودَعُ ستّةَ
عشر. فالفرقُ واحدٌ، وموضعُه الشفتان بعينهما.

**ولا يُعدَّل الجدولُ ليوافق نسبتَه، ولا تُعدَّل النسبةُ لتوافق الجدول**: كلا
الأمرين تصحيحٌ صامتٌ يُنتِج تطابقًا لم يقع. والمُسجَّلُ هنا الفرقُ موضعًا
بموضعٍ مُشتَقًّا من البايتات نفسها، وحاجزُ الاستيراد يبقى `OPEN`.

**وما لا تفعله هذه الوحدة، مُسمًّى لا مطويًّا**:

* **لا ترفع بقيّةَ `CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE`**: البقيّةُ
  تُرفَع بطبعةٍ تصل وتُطابِق، لا بوحدةٍ تصف شرطَ وصولها.
* **لا تمسّ `ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE` ولا
  `JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE`**: فجوةُ النمذجة — جعلُ الترتيب مسافةً
  — ليست فجوةَ نسبةٍ إلى طبعة، ولا يرفعها مصدرٌ مهما عَلا.
* **لا ترفع حاجزَ جدول الصفة**: شرطُ رفعه مكتوبٌ في موضعه (مصدرٌ مسمًّى،
  وبصمةُ بايتات، وتصريحُ نسبة)، ولا يرفعه إيداعُ المخرج ولا يُقرأ رفعُ أحدهما
  رفعًا للآخر.
* **لا تمسّ `PHONETIC_ECONOMY_CANDIDATE`**: تبقى `FAIL` و`DEFER_IN_SCOPE`،
  وأقصى ما يُبلَغ `CLOSURE_MET_PENDING_AUTHORITY`.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .classical_makharij_table import (
    CLASSICAL_MAKHARIJ,
    CLASSICAL_SOURCE_ATTESTATION,
    CLASSICAL_TABLE_DIGEST,
)
from .gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)
from .gflk_milestone_blocking_registration import question_named

__all__ = [
    "ATTESTED_REGION_COUNTS",
    "ATTESTED_TOTAL_MAKHARIJ",
    "ATTESTED_TOTAL_QUOTED_PHRASE",
    "A_NAMED_EDITION_IS_NOT_A_DEPOSITED_PAGE_NOTE",
    "DEPOSITED_EDITION_ORDERINGS",
    "DIVISION_DIFFERENCES",
    "MAKHARIJ_EDITION_NAMED_RESIDUALS",
    "MAKHARIJ_EDITION_REGISTRATION_DIGEST",
    "NO_EDITION_HAS_REACHED_THIS_TREE_NOTE",
    "SCOPE_RESOLUTION",
    "THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOTE",
    "THE_FROZEN_TABLE_CONTRADICTS_ITS_OWN_ATTESTATION_NOTE",
    "THE_SIFA_BARRIER_IS_NOT_LIFTED_BY_THIS_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "UNRANKED_DECLARED_MAKHARIJ",
    "AttestedRegionCount",
    "DepositedEditionOrdering",
    "EditionCitation",
    "MakharijEditionError",
    "MakhrajRegion",
    "RankDifference",
    "RegionCountDifference",
    "ScopeResolution",
    "ScopeResolutionRecord",
    "compare_to_frozen_table",
    "derive_division_differences",
    "derive_frozen_region_counts",
    "edition_matches_the_frozen_table",
    "frozen_ranked_makhraj_count",
    "makharij_edition_registration_digest",
    "region_of_makhraj_name",
]


class MakharijEditionError(ValueError):
    """رُفض إيداعٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class MakhrajRegion(Enum):
    """أقسامُ المخارج المُرقَّمة. والجوفُ والخيشومُ ليسا عضوين هنا قصدًا.

    إذ هما مُعلَنان خارجَ الترقيم في الجدول المُودَع نفسه؛ وإقحامُهما عضوَين
    يُوهم أنّ للجدول رتبةً فيهما، وهو ما لم يقع.
    """

    THROAT = "الحلق"
    TONGUE = "اللسان"
    LIPS = "الشفتان"


UNRANKED_DECLARED_MAKHARIJ: Final[tuple[str, ...]] = ("الجوف", "الخيشوم")
"""المخرجان المُعلَنان خارجَ الترقيم في الجدول المُودَع، مُسمّيَين لا محذوفَين."""


_REGION_MARKERS: Final[MappingProxyType[MakhrajRegion, tuple[str, ...]]] = (
    MappingProxyType(
        {
            MakhrajRegion.THROAT: ("الحلق",),
            MakhrajRegion.TONGUE: ("اللسان",),
            MakhrajRegion.LIPS: ("الشفة", "الشفتان"),
        }
    )
)


def region_of_makhraj_name(name: str) -> MakhrajRegion:
    """اقسِمْ مخرجًا إلى قسمه من نصّ اسمه، ولا تُحمَل تسميةٌ على أقرب قسم.

    والاسمُ الذي يقع تحت قسمين أو تحت لا قسمٍ يُرَدّ صريحًا: قسمةٌ صامتةٌ
    بالافتراض تجعل العددَ المُشتَقَّ أثرَ الافتراض لا أثرَ الجدول.
    """

    if not isinstance(name, str) or not name.strip():
        raise MakharijEditionError("اسمُ المخرج نصٌّ غير فارغ")
    matched = tuple(
        region
        for region, markers in _REGION_MARKERS.items()
        if any(marker in name for marker in markers)
    )
    if len(matched) != 1:
        raise MakharijEditionError(
            f"اسمُ مخرجٍ لا يقع تحت قسمٍ واحدٍ بعينه: {name!r}؛ "
            "وحملُه على أقربِ قسمٍ يجعل العددَ أثرَ الحمل لا أثرَ الجدول."
        )
    return matched[0]


def derive_frozen_region_counts() -> MappingProxyType[MakhrajRegion, int]:
    """عدُّ مخارجِ كلِّ قسمٍ، مُشتَقًّا من الجدول المُبصَّم لا مكتوبًا هنا."""

    counts = dict.fromkeys(MakhrajRegion, 0)
    for _rank, name, _letters in CLASSICAL_MAKHARIJ:
        counts[region_of_makhraj_name(name)] += 1
    return MappingProxyType(counts)


def frozen_ranked_makhraj_count() -> int:
    """عددُ المخارج المُرقَّمة، مقروءًا من الجدول المُبصَّم لا مكتوبًا هنا."""

    return len(CLASSICAL_MAKHARIJ)


@dataclass(frozen=True, slots=True)
class AttestedRegionCount:
    """عددُ قسمٍ كما نطقت به النسبةُ المكتوبة، مربوطًا باقتباسها الحرفيّ.

    ولا يُكتَب العددُ هنا طليقًا: `quoted_phrase` يجب أن يَرِد **حرفيًّا** في
    `CLASSICAL_SOURCE_ATTESTATION`، وإلّا صار الرقمُ دعوى هذه الوحدة لا نقلًا
    عن النسبة التي تدّعي نقلَه.
    """

    region: MakhrajRegion
    quoted_phrase: str
    attested_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.region, MakhrajRegion):
            raise MakharijEditionError("القسمُ عضوٌ في مفردته المغلقة")
        if not isinstance(self.quoted_phrase, str) or not self.quoted_phrase.strip():
            raise MakharijEditionError("الاقتباسُ الحرفيُّ نصٌّ غير فارغ")
        if self.quoted_phrase not in CLASSICAL_SOURCE_ATTESTATION:
            raise MakharijEditionError(
                f"اقتباسٌ لا يَرِد حرفيًّا في النسبة المكتوبة: "
                f"{self.quoted_phrase!r}؛ ورقمٌ بلا اقتباسِه دعوى هذه الوحدة "
                "لا نقلٌ عن النسبة."
            )
        if not isinstance(self.attested_count, int) or self.attested_count <= 0:
            raise MakharijEditionError("عددُ القسم صحيحٌ موجب")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العدّ المنسوب للبصمة."""

        return {
            "region": self.region.name,
            "quoted_phrase": self.quoted_phrase,
            "attested_count": self.attested_count,
        }


ATTESTED_TOTAL_QUOTED_PHRASE: Final[str] = "المخارج السبعةَ عشرَ"
"""اقتباسُ العدد الكلّيّ من النسبة المكتوبة، حرفيًّا لا مُعادَ صياغته."""

ATTESTED_TOTAL_MAKHARIJ: Final[int] = 17
"""العددُ الكلّيُّ كما نطقت به النسبة؛ ومربوطٌ باقتباسه أعلاه لا طليقًا."""

ATTESTED_REGION_COUNTS: Final[tuple[AttestedRegionCount, ...]] = (
    AttestedRegionCount(
        region=MakhrajRegion.THROAT,
        quoted_phrase="الحلقُ ثلاثة",
        attested_count=3,
    ),
    AttestedRegionCount(
        region=MakhrajRegion.TONGUE,
        quoted_phrase="اللسانُ عشرة",
        attested_count=10,
    ),
    AttestedRegionCount(
        region=MakhrajRegion.LIPS,
        quoted_phrase="الشفتان اثنان",
        attested_count=2,
    ),
)
"""ما نطقت به النسبةُ المكتوبة لكلّ قسم، كلُّ عددٍ باقتباسه الحرفيّ."""


@dataclass(frozen=True, slots=True)
class RegionCountDifference:
    """فرقٌ بين عددٍ منسوبٍ وعددٍ مُشتَقٍّ من البايتات، بمواضعه مُسمّاة.

    ولا حقلَ حكمٍ هنا ولا حقلَ تصحيح: الفرقُ يُسجَّل بمواضعه، ولا يُقال أيُّ
    الطرفين الخطأ، لأنّ تسميةَ أحدهما خطأً حسمٌ لم تَجْرِ أدواتُه.
    """

    region: MakhrajRegion
    attested_count: int
    frozen_count: int
    quoted_phrase: str
    frozen_rows: tuple[tuple[int, str, str], ...]

    def __post_init__(self) -> None:
        if self.attested_count == self.frozen_count:
            raise MakharijEditionError(
                "لا يُسجَّل فرقٌ حيث لا فرق؛ وصفٌّ بلا فرقٍ يُضخّم جدولَ "
                "الفروق فيُقرأ خلافًا لم يقع."
            )
        if not self.frozen_rows:
            raise MakharijEditionError("فرقٌ بلا مواضعِه في الجدول المُبصَّم فرقٌ لا يُفحَص")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرق للبصمة."""

        return {
            "region": self.region.name,
            "attested_count": self.attested_count,
            "frozen_count": self.frozen_count,
            "quoted_phrase": self.quoted_phrase,
            "frozen_rows": [list(row) for row in self.frozen_rows],
        }


def derive_division_differences() -> tuple[RegionCountDifference, ...]:
    """قابِلْ أعدادَ النسبة بأعداد البايتات الآن، ولا تقرأ فرقًا مكتوبًا."""

    frozen = derive_frozen_region_counts()
    differences: list[RegionCountDifference] = []
    for attested in ATTESTED_REGION_COUNTS:
        frozen_count = frozen[attested.region]
        if frozen_count == attested.attested_count:
            continue
        differences.append(
            RegionCountDifference(
                region=attested.region,
                attested_count=attested.attested_count,
                frozen_count=frozen_count,
                quoted_phrase=attested.quoted_phrase,
                frozen_rows=tuple(
                    (rank, name, letters)
                    for rank, name, letters in CLASSICAL_MAKHARIJ
                    if region_of_makhraj_name(name) is attested.region
                ),
            )
        )
    return tuple(differences)


DIVISION_DIFFERENCES: Final[tuple[RegionCountDifference, ...]] = (
    derive_division_differences()
)
"""الفرقُ بين النسبة المكتوبة والبايتات المُبصَّمة، محسوبًا عند الاستيراد."""


class ScopeResolution(Enum):
    """وجها حسمِ تعارض ١٣/١٦، وعضوٌ ثالثٌ لمن لم يُحسَم بعد.

    والعضوُ الثالثُ ليس ثغرةً: تسجيلُ «لم يُتَّخَذ» أصدقُ من حملِ القرار على
    أحد الوجهين ثمّ الاستشهادِ به كأنّه اتُّخِذ.
    """

    RESTATE_THE_SPECIFICATION_ON_THE_FROZEN_SIXTEEN = (
        "إعادةُ بيانِ المواصفة على الستّةَ عشر"
    )
    IMPORT_THE_THIRTEEN_AS_A_SECOND_ATTRIBUTED_TABLE = (
        "استيرادُ الثلاثةَ عشرَ جدولًا ثانيًا منسوبًا"
    )
    NOT_TAKEN = "لم يُتَّخَذ بعد"


@dataclass(frozen=True, slots=True)
class ScopeResolutionRecord:
    """قرارُ الحسمِ مُسجَّلًا قبل الاستيراد، بسؤاله المفتوح لا بجوابٍ مُخمَّن."""

    resolution: ScopeResolution
    admissible_resolutions: tuple[ScopeResolution, ...]
    open_question_identifier: str
    why_it_stands_here: str

    def __post_init__(self) -> None:
        if not isinstance(self.resolution, ScopeResolution):
            raise MakharijEditionError("القرارُ عضوٌ في مفردته المغلقة")
        if ScopeResolution.NOT_TAKEN in self.admissible_resolutions:
            raise MakharijEditionError(
                "«لم يُتَّخَذ» حالُ القرار لا وجهًا من وجوه حسمه؛ وعدُّه وجهًا "
                "يجعل تركَ الحسم حسمًا"
            )
        if len(self.admissible_resolutions) < 2:
            raise MakharijEditionError(
                "وجها الحسم يُسمَّيان معًا؛ وتسميةُ وجهٍ واحدٍ تجعل القرارَ "
                "مكتوبًا قبل أن يُتَّخَذ"
            )
        if not self.why_it_stands_here.strip():
            raise MakharijEditionError("حالُ القرار يُسجَّل بسببه نصًّا غير فارغ")
        question_named(self.open_question_identifier)

    @property
    def is_taken(self) -> bool:
        """أاتُّخِذ القرار؟ مُشتَقٌّ من عضوه لا مكتوبٌ في حقلٍ بجانبه."""

        return self.resolution is not ScopeResolution.NOT_TAKEN

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القرار للبصمة."""

        return {
            "resolution": self.resolution.name,
            "admissible_resolutions": [
                member.name for member in self.admissible_resolutions
            ],
            "open_question_identifier": self.open_question_identifier,
            "why_it_stands_here": self.why_it_stands_here,
        }


SCOPE_RESOLUTION: Final[ScopeResolutionRecord] = ScopeResolutionRecord(
    resolution=ScopeResolution.NOT_TAKEN,
    admissible_resolutions=(
        ScopeResolution.RESTATE_THE_SPECIFICATION_ON_THE_FROZEN_SIXTEEN,
        ScopeResolution.IMPORT_THE_THIRTEEN_AS_A_SECOND_ATTRIBUTED_TABLE,
    ),
    open_question_identifier="THIRTEEN_VERSUS_SIXTEEN_MAKHARIJ",
    why_it_stands_here=(
        "لم يُقدَّم إلى هذه الشجرة مصدرٌ مسمًّى لتقسيم الثلاثةَ عشر، ولا صدر "
        "قرارٌ بإعادة بيان المواصفة على الستّةَ عشرَ المُبصَّمة؛ وحملُ القرار "
        "على أحد الوجهين هنا يجعل وحدةَ تسجيلٍ تُصدِر ما لا سلطةَ لها به"
    ),
)
"""قرارُ الحسم كما هو اليوم: غيرُ متّخَذ، وسؤالُه مُسمًّى لا مُخمَّنٌ جوابُه."""


@dataclass(frozen=True, slots=True)
class EditionCitation:
    """طبعةٌ مُسمّاةٌ بجزئها وصفحتها؛ وسبعةُ حقولٍ كلُّها شرطُ إنشاء.

    والجزءُ والصفحةُ ليسا زينةً ببليوغرافيّة: بهما وحدهما يُعاد النظرُ في
    المُودَع، وبلاهما تصير النسبةُ إحالةً إلى كتابٍ لا إلى موضعٍ يُراجَع.
    """

    work_title: str
    editor: str
    publisher: str
    edition_year: str
    volume: str
    page: str
    deposited_quotation: str

    def __post_init__(self) -> None:
        for field_name, label in (
            ("work_title", "عنوانُ الكتاب"),
            ("editor", "المحقّق"),
            ("publisher", "الناشر"),
            ("edition_year", "سنةُ الطبع"),
            ("volume", "الجزء"),
            ("page", "الصفحة"),
            ("deposited_quotation", "المُقتبَسُ المُودَع"),
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise MakharijEditionError(
                    f"{label} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ وطبعةٌ بحقلٍ فارغٍ "
                    "إحالةٌ إلى كتابٍ لا إلى موضعٍ يُراجَع"
                )

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى النسبة للبصمة."""

        return {
            "work_title": self.work_title,
            "editor": self.editor,
            "publisher": self.publisher,
            "edition_year": self.edition_year,
            "volume": self.volume,
            "page": self.page,
            "deposited_quotation": self.deposited_quotation,
        }


_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"


@dataclass(frozen=True, slots=True)
class DepositedEditionOrdering:
    """ترتيبٌ مُودَعٌ عن طبعةٍ بعينها، ببصمةٍ تُعاد اشتقاقًا من بايتاته."""

    citation: EditionCitation
    rows: tuple[tuple[int, str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.citation, EditionCitation):
            raise MakharijEditionError("الترتيبُ المُودَع يحمل نسبةً كاملة")
        if not self.rows:
            raise MakharijEditionError("ترتيبٌ بلا صفٍّ واحدٍ ليس ترتيبًا مُودَعًا")
        expected = tuple(range(1, len(self.rows) + 1))
        if tuple(rank for rank, _name, _letters in self.rows) != expected:
            raise MakharijEditionError(
                "رتبُ الترتيب المُودَع متتاليةٌ من الواحد؛ وثغرةٌ في الترقيم "
                "تجعل فرقَ الرتبتين غيرَ ما تقوله الطبعة"
            )
        seen: set[str] = set()
        for _rank, name, letters in self.rows:
            if not name.strip() or not letters:
                raise MakharijEditionError("صفٌّ بلا اسمٍ أو بلا حرفٍ لا يُودَع")
            for letter in letters:
                if letter in seen:
                    raise MakharijEditionError(
                        f"حرفٌ في مخرجَين في الترتيب المُودَع: {letter}"
                    )
                seen.add(letter)

    def edition_bytes(self) -> bytes:
        """رمِّز الترتيبَ المُودَع بدقّة البايت، بترميز الجدول المُبصَّم نفسه.

        ولا تطبيعَ هنا قصدًا، للسبب المكتوب في `classical_table_bytes`: تطبيعُنا
        إيّاه يجعل البصمةَ بصمةَ نصٍّ آخرَ ثمّ يُسمّى الاختلافُ تطابقًا.
        """

        lines = [
            f"{rank}{_FIELD_SEPARATOR}{letters}" for rank, _name, letters in self.rows
        ]
        return _RECORD_SEPARATOR.join(lines).encode("utf-8")

    def rederive_edition_digest(self) -> str:
        """أعِد اشتقاقَ بصمةِ المُودَع من بايتاته الآن، لا من رقمٍ في حقل."""

        return canonical_digest(self.edition_bytes())

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإيداع للبصمة، ونسبتُه معه لا مفصولةً عنه."""

        return {
            "citation": self.citation.as_canonical_content(),
            "rows": [list(row) for row in self.rows],
            "edition_digest": self.rederive_edition_digest(),
        }


DEPOSITED_EDITION_ORDERINGS: Final[tuple[DepositedEditionOrdering, ...]] = ()
"""الطبعاتُ المُودَعة. **فارغة**: لم تصل صفحةُ طبعةٍ بعينها إلى هذه الشجرة."""


@dataclass(frozen=True, slots=True)
class RankDifference:
    """اختلافُ رتبةٍ واحدةٍ بين طبعةٍ مُودَعةٍ والجدول المُبصَّم.

    و`None` في أحد الطرفين تعني أنّ الرتبةَ غائبةٌ عنه؛ وهو خلافٌ يُسجَّل
    كسائره، لأنّ حذفَ الصفوف الزائدة يجعل الطبعةَ تُطابِق ما لم تُطابِقه.
    """

    rank: int
    edition_letters: str | None
    frozen_letters: str | None

    def __post_init__(self) -> None:
        if self.edition_letters == self.frozen_letters:
            raise MakharijEditionError("لا يُسجَّل اختلافٌ حيث لا اختلاف")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الاختلاف للبصمة."""

        return {
            "rank": self.rank,
            "edition_letters": self.edition_letters,
            "frozen_letters": self.frozen_letters,
        }


def compare_to_frozen_table(
    ordering: DepositedEditionOrdering,
) -> tuple[RankDifference, ...]:
    """قابِلِ الطبعةَ بالجدول المُبصَّم رتبةً برتبةٍ وحرفًا بحرف، بتشغيلٍ لا بدعوى.

    والمقابلةُ على الحروف لا على أسماء المخارج: العبارةُ تختلف بين الطبعات بلا
    خلافٍ في القسمة، وجعلُ اللفظِ محكَّ التطابق يُنتج خلافًا لم يقع.
    """

    if not isinstance(ordering, DepositedEditionOrdering):
        raise MakharijEditionError("المقابلةُ تُشغَّل على ترتيبٍ مُودَعٍ لا على غيره")
    edition = {rank: letters for rank, _name, letters in ordering.rows}
    frozen = {rank: letters for rank, _name, letters in CLASSICAL_MAKHARIJ}
    differences = [
        RankDifference(
            rank=rank,
            edition_letters=edition.get(rank),
            frozen_letters=frozen.get(rank),
        )
        for rank in sorted(set(edition) | set(frozen))
        if edition.get(rank) != frozen.get(rank)
    ]
    return tuple(differences)


def edition_matches_the_frozen_table(ordering: DepositedEditionOrdering) -> bool:
    """أتُطابِق الطبعةُ الجدولَ المُبصَّم؟ مُشتَقٌّ بالمقابلة لا مكتوبٌ في حقل."""

    return not compare_to_frozen_table(ordering)


A_NAMED_EDITION_IS_NOT_A_DEPOSITED_PAGE_NOTE: Final[str] = (
    "ANamedEditionIsNotADepositedPage: تسميةُ كتابٍ ليست إيداعَ طبعة؛ "
    "والعنوانُ والمحقّقُ والناشرُ والسنةُ والجزءُ والصفحةُ والمُقتبَسُ سبعةُ "
    "شروطِ إنشاءٍ لا أوصافٍ اختياريّة، وبغير الجزء والصفحة لا يُراجَع موضع"
)

NO_EDITION_HAS_REACHED_THIS_TREE_NOTE: Final[str] = (
    "NoEditionHasReachedThisTree: `DEPOSITED_EDITION_ORDERINGS` فارغةٌ لأنّ "
    "صفحةَ طبعةٍ بعينها لم تصل؛ والموضعُ مسنونٌ والبايتاتُ خارجَه، على منوال "
    "`MEASURED_SAKIN_CLASH_SOURCES` و`corpora/MASAQ.csv`، لا على منوال إيداعٍ تمّ"
)

THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOTE: Final[str] = (
    "TheConflictIsResolvedBeforeTheImport: ما دام قرارُ تعارض ١٣/١٦ غيرَ "
    "متّخَذٍ فالإيداعُ مرفوضٌ عند الاستيراد لا بعده؛ فالحسمُ بعد الإيداع "
    "يجعل الاختيارَ بين رقمين تابعًا للنتيجة المرغوبة"
)

THE_FROZEN_TABLE_CONTRADICTS_ITS_OWN_ATTESTATION_NOTE: Final[str] = (
    "TheFrozenTableContradictsItsOwnAttestation: النسبةُ المكتوبة تقول "
    "«الشفتان اثنان» والبايتاتُ تحمل ثلاثةَ مخارجَ شفويّة، ففائضُ الترقيم "
    "واحدٌ وموضعُه الشفتان؛ ولا يُعدَّل الجدولُ ليوافق نسبتَه ولا النسبةُ "
    "لتوافق الجدول، فكلاهما تصحيحٌ صامتٌ يُنتِج تطابقًا لم يقع"
)

THE_SIFA_BARRIER_IS_NOT_LIFTED_BY_THIS_NOTE: Final[str] = (
    "TheSifaBarrierIsNotLiftedByThis: حاجزُ جدول الصفة يبقى `OPEN` بشرطِ "
    "رفعه المكتوب في موضعه؛ ولا يرفعه إيداعُ المخرج، ولا يُقرأ رفعُ أحدهما "
    "رفعًا للآخر"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`، "
    "ولا استيرادَ من `kernel/`"
)

MAKHARIJ_EDITION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_NAMED_EDITION_IS_NOT_A_DEPOSITED_PAGE_NOTE,
    NO_EDITION_HAS_REACHED_THIS_TREE_NOTE,
    THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOTE,
    THE_FROZEN_TABLE_CONTRADICTS_ITS_OWN_ATTESTATION_NOTE,
    THE_SIFA_BARRIER_IS_NOT_LIFTED_BY_THIS_NOTE,
    THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def makharij_edition_registration_digest() -> str:
    """بصمةُ هذا التسجيل، محسوبةً عند الاستيراد لا مكتوبةً رقمًا ثابتًا."""

    return canonical_digest(
        canonical_bytes(
            {
                "attested_total": {
                    "quoted_phrase": ATTESTED_TOTAL_QUOTED_PHRASE,
                    "count": ATTESTED_TOTAL_MAKHARIJ,
                },
                "attested_region_counts": [
                    attested.as_canonical_content()
                    for attested in ATTESTED_REGION_COUNTS
                ],
                "unranked_declared_makharij": list(UNRANKED_DECLARED_MAKHARIJ),
                "frozen_table_digest": CLASSICAL_TABLE_DIGEST,
                "frozen_ranked_count": frozen_ranked_makhraj_count(),
                "division_differences": [
                    difference.as_canonical_content()
                    for difference in DIVISION_DIFFERENCES
                ],
                "scope_resolution": SCOPE_RESOLUTION.as_canonical_content(),
                "deposited_edition_orderings": [
                    ordering.as_canonical_content()
                    for ordering in DEPOSITED_EDITION_ORDERINGS
                ],
                "named_residuals": list(MAKHARIJ_EDITION_NAMED_RESIDUALS),
            }
        )
    )


MAKHARIJ_EDITION_REGISTRATION_DIGEST: Final[str] = (
    makharij_edition_registration_digest()
)
"""البصمةُ المُجمَّدة؛ وأيُّ تغييرٍ في نصٍّ أعلاه يُغيّرها فيُكشَف."""


def _refuse_an_incoherent_registration() -> None:
    """احرس الوحدةَ عند الاستيراد: لا إيداعَ قبل الحسم، ولا حاجزَ يُرفَع ضمنًا."""

    if DEPOSITED_EDITION_ORDERINGS and not SCOPE_RESOLUTION.is_taken:
        raise MakharijEditionError(THE_CONFLICT_IS_RESOLVED_BEFORE_THE_IMPORT_NOTE)
    if ATTESTED_TOTAL_QUOTED_PHRASE not in CLASSICAL_SOURCE_ATTESTATION:
        raise MakharijEditionError("اقتباسُ العدد الكلّيّ لا يَرِد حرفيًّا في النسبة المكتوبة")
    if any(
        barrier.standing is not ImportBarrierStanding.OPEN
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS
    ):
        raise MakharijEditionError(
            "حاجزٌ مرفوعٌ بلا إيداعٍ يُقابله؛ ورفعُ الحاجز يكون بطبعةٍ تصل "
            "وتُطابِق، لا بوحدةٍ تصف شرطَ وصولها"
        )
    if list(MAKHARIJ_EDITION_NAMED_RESIDUALS) != sorted(
        MAKHARIJ_EDITION_NAMED_RESIDUALS
    ):
        raise MakharijEditionError("البواقي المُسمّاةُ تُرتَّب ترتيبًا ثابتًا")


_refuse_an_incoherent_registration()
