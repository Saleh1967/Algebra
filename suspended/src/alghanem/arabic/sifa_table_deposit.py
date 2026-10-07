"""عقدُ إيداعِ جدول الصفة: شرطُ رفع الحاجز مبنيًّا، وقياسُ فصلٍ يسبق الاستيراد.

**ما تفعله هذه الوحدة**: تبني العقدَ الذي يشترطه
`gflk_feature_table_import_barrier` لرفع حاجز جدول الصفة — مصدرٌ مسمًّى بطبعته
وجزئها وصفحتها، وبصمةُ بايتاتٍ تُعاد اشتقاقًا، وتصريحٌ بأنّ الجدولَ ليس دعوى
هذه الشجرة — وتضيف إليه ما لم يكن في عقد المخرج: **قياسَ قوّة الفصل**، أي كم
حرفًا من العشرين المعلَّقة يحسمها جدولٌ مرشَّحٌ لو أُودِع. فيُعرَف ثمنُ الطبعة
قبل استيرادها لا بعده.

**ولا تُودِع جدولًا اليوم**: `DEPOSITED_SIFA_TABLES` **فارغة**. ولم يُكتَب في
هذه الوحدة صفٌّ واحدٌ من صفات العربيّة، لا في مثالٍ ولا في اختبار.

`A_TABLE_WRITTEN_IN_THE_SESSION_IS_THE_THING_THE_BARRIER_FORBIDS`: الحاجزُ قام
لأنّ الجدولَ بلا مصدرٍ مسمًّى ولا بصمة؛ فجدولٌ أكتبه أنا من محفوظي ثمّ أُلصِق
به نسبةً معقولةَ الصورة **هو بعينه العطبُ الذي بُني الحاجزُ ليمنعه**، لا سدٌّ
له. ولذلك تُخرِج هذه الوحدةُ العقدَ فارغًا وتنتظر الصفحة.

`A_CANDIDATE_IS_NOT_A_DEPOSIT`: نوعان مفصولان بنيويًّا لا بالتسمية:
`CandidateSifaTable` صفوفٌ بلا نسبة — تُقاس ولا تُودَع؛ و`DepositedSifaTable`
صفوفٌ مع نسبةٍ كاملةٍ ببصمة. ومن قاس مرشَّحًا فقد قاس، ومن ظنّ القياسَ استيرادًا
أدخل إلى الشجرة ما لم يجتز بابَها (`MEASURING_A_CANDIDATE_IS_NOT_IMPORTING_IT`).

`THE_FEATURE_NAMES_COME_FROM_THE_SOURCE_NOT_FROM_A_VOCABULARY_OF_OURS`: أسماءُ
الصفات تُحمَل كما نطق بها المصدرُ نصًّا، ولا تُقابَل بمفردةٍ مغلقةٍ نكتبها هنا.
فمفردةٌ منّا تُلزِم الطبعةَ بقسمتنا ثمّ تُقرأ النتيجةُ خبرًا عن الطبعة. والفصلُ
يقع على **تساوي مجموعات الصفات** لا على معناها، فلا تحتاج هذه الوحدةُ أن تفهم
صفةً واحدة.

`THIS_MODULE_REPORTS_THE_CONDITION_AND_DOES_NOT_LIFT_THE_BARRIER`: منزلةُ
الحاجز تُقرأ من موضعها ولا تُكتَب هنا. ورفعُه تعديلٌ في وحدته يقع بيد من
أودَع، بعد أن يقول هذا التقريرُ إنّ الشرطَ استُوفي. ووحدةٌ ترفع حاجزَ نفسِها
حاجزٌ بلا حارس.

`THE_GAIN_IS_MEASURED_NOT_PROMISED`: قوّةُ الفصل تخرج من تشغيل القسمة على
الخانات، لا من وعدٍ في نثر الطبعة. وجدولٌ لا يفصل يُسجَّل أنّه لا يفصل وإن
كان مصدرُه أعلى المصادر.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .classical_makharij_table import CLASSICAL_ORDINAL
from .gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)
from .gflk_milestone_blocking_registration import question_named
from .makharij_edition_citation import EditionCitation
from .makhraj_bit_decoder import MAKHRAJ_LETTERS
from .makhraj_bit_decoder import census as makhraj_census

__all__ = [
    "A_CANDIDATE_IS_NOT_A_DEPOSIT_NOTE",
    "A_TABLE_WRITTEN_IN_THE_SESSION_IS_FORBIDDEN_NOTE",
    "DEPOSITED_SIFA_TABLES",
    "MEASURING_A_CANDIDATE_IS_NOT_IMPORTING_IT_NOTE",
    "SIFA_BARRIER_TABLE_NAME",
    "SIFA_OPEN_QUESTION_IDENTIFIER",
    "SIFA_TABLE_NAMED_RESIDUALS",
    "THE_FEATURE_NAMES_COME_FROM_THE_SOURCE_NOTE",
    "THE_GAIN_IS_MEASURED_NOT_PROMISED_NOTE",
    "THIS_MODULE_DOES_NOT_LIFT_THE_BARRIER_NOTE",
    "BarrierLiftCondition",
    "BarrierLiftReport",
    "CandidateSifaTable",
    "ClassSeparation",
    "DepositedSifaTable",
    "SeparationReport",
    "SifaTableError",
    "barrier_lift_report",
    "separation_over",
    "sifa_barrier_standing",
]

SIFA_BARRIER_TABLE_NAME: Final[str] = "جدولُ الصفة"

SIFA_OPEN_QUESTION_IDENTIFIER: Final[str] = "SIFA_TABLE_BYTES"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_FEATURE_SEPARATOR: Final[str] = "\x1d"


class SifaTableError(ValueError):
    """رُفض إيداعٌ أو مرشَّحٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


@dataclass(frozen=True, slots=True)
class CandidateSifaTable:
    """صفوفُ صفاتٍ بلا نسبة: تُقاس قوّتُها ولا تدخل الشجرةَ جدولًا.

    وشرطُ بنائها تغطيةُ الحروف المرقَّمة تغطيةً تامّةً بلا نقصٍ ولا تكرارٍ ولا
    حرفٍ خارجَ الترقيم؛ فجدولٌ يترك حرفًا بلا صفٍّ يُخرِج «فصلًا» سببُه غيابُ
    الصفّ لا الصفة.
    """

    rows: tuple[tuple[str, tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        if not self.rows:
            raise SifaTableError("جدولٌ بلا صفٍّ واحدٍ ليس جدولًا يُقاس.")
        seen: set[str] = set()
        for letter, features in self.rows:
            if letter not in CLASSICAL_ORDINAL:
                raise SifaTableError(
                    f"صفٌّ لحرفٍ لا رتبةَ له في الجدول المُودَع: {letter!r}؛ "
                    "وحروفُ المدّ والخيشومُ خارجَ الترقيم قصدًا."
                )
            if letter in seen:
                raise SifaTableError(
                    f"حرفٌ في صفَّين: {letter}؛ وصفّان لحرفٍ واحدٍ يجعلان "
                    "مجموعةَ صفاته تابعةً لأيّهما قُرئ آخرًا."
                )
            seen.add(letter)
            if not features:
                raise SifaTableError(
                    f"صفٌّ بلا صفةٍ واحدة: {letter}؛ وصفٌّ فارغٌ يساوي كلَّ "
                    "صفٍّ فارغٍ فيُخرِج تعادلًا سببُه الفراغ."
                )
            if len(set(features)) != len(features):
                raise SifaTableError(
                    f"صفةٌ مكرّرةٌ في صفٍّ واحد: {letter}؛ والتكرارُ يُغيّر "
                    "عدَّ الصفات ولا يُغيّر مجموعتَها."
                )
            for feature in features:
                if not feature.strip():
                    raise SifaTableError(
                        f"صفةٌ بلا اسمٍ في صفّ: {letter}؛ واسمٌ فارغٌ يُطابِق "
                        "كلَّ اسمٍ فارغٍ في كلّ صفّ."
                    )
        missing = sorted(set(CLASSICAL_ORDINAL) - seen)
        if missing:
            raise SifaTableError(
                "حروفٌ مرقَّمةٌ بلا صفّ: "
                + "، ".join(missing)
                + "؛ وتغطيةٌ ناقصةٌ تُخرِج فصلًا سببُه غيابُ الصفّ لا الصفة."
            )

    def features_of(self, letter: str) -> frozenset[str]:
        """مجموعةُ صفات حرفٍ، مأخوذةً من صفّه لا محمولةً على أقرب صفّ."""

        for row_letter, features in self.rows:
            if row_letter == letter:
                return frozenset(features)
        raise SifaTableError(f"حرفٌ بلا صفٍّ في هذا المرشَّح: {letter!r}.")

    def table_bytes(self) -> bytes:
        """رمِّز الصفوفَ بدقّة البايت؛ ولا تطبيعَ هنا قصدًا.

        والسببُ هو المكتوبُ في `classical_table_bytes`: تطبيعُنا إيّاه يجعل
        البصمةَ بصمةَ نصٍّ آخرَ ثمّ يُسمّى الاختلافُ تطابقًا.
        """

        lines = [
            f"{letter}{_FIELD_SEPARATOR}{_FEATURE_SEPARATOR.join(features)}"
            for letter, features in self.rows
        ]
        return _RECORD_SEPARATOR.join(lines).encode("utf-8")

    def rederive_table_digest(self) -> str:
        """أعِد اشتقاقَ بصمةِ الصفوف من بايتاتها الآن، لا من رقمٍ في حقل."""

        return canonical_digest(self.table_bytes())


@dataclass(frozen=True, slots=True)
class DepositedSifaTable:
    """جدولُ صفةٍ مُودَعٌ عن طبعةٍ بعينها: نسبةٌ كاملةٌ وصفوفٌ وبصمةٌ تُعاد.

    والنسبةُ من نوع `EditionCitation` عينِه الذي يشترطه عقدُ المخرج: سبعةُ
    حقولٍ كلُّها شرطُ إنشاء. ونسخُ قاعدةٍ ثانيةٍ للنسبة يجعل في الشجرة قاعدتين
    تنفكّان بصمت.
    """

    citation: EditionCitation
    table: CandidateSifaTable
    attribution_declaration: str

    def __post_init__(self) -> None:
        if not isinstance(self.citation, EditionCitation):
            raise SifaTableError("الإيداعُ يحمل نسبةً كاملةً من نوعها المعروف.")
        if not isinstance(self.table, CandidateSifaTable):
            raise SifaTableError("الإيداعُ يحمل صفوفًا مبنيّةً بشرطها.")
        if not self.attribution_declaration.strip():
            raise SifaTableError(
                "تصريحُ النسبة شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ وجدولٌ بلا تصريحٍ "
                "بأنّه ليس دعوى هذه الشجرة يصير بعد جلساتٍ كأنّه اشتُقّ فيها."
            )

    def rederive_table_digest(self) -> str:
        """بصمةُ بايتات الجدول المُودَع، مُعادةَ الاشتقاق لا منسوخة."""

        return self.table.rederive_table_digest()

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإيداع للبصمة، ونسبتُه معه لا مفصولةً عنه."""

        return {
            "citation": self.citation.as_canonical_content(),
            "rows": [[letter, list(features)] for letter, features in self.table.rows],
            "attribution_declaration": self.attribution_declaration,
            "table_digest": self.rederive_table_digest(),
        }


DEPOSITED_SIFA_TABLES: Final[tuple[DepositedSifaTable, ...]] = ()
"""جداولُ الصفة المُودَعة. **فارغة**: لم تصل صفحةُ طبعةٍ بعينها إلى هذه الشجرة."""


@dataclass(frozen=True, slots=True)
class ClassSeparation:
    """ما فعلته الصفاتُ بخانةِ مخرجٍ واحدة: ما انفرد وما بقي متعادلًا."""

    makhraj_rank: int
    letters: tuple[str, ...]
    separated_letters: tuple[str, ...]
    tied_groups: tuple[tuple[str, ...], ...]

    def __post_init__(self) -> None:
        counted = len(self.separated_letters) + sum(
            len(group) for group in self.tied_groups
        )
        if counted != len(self.letters):
            raise SifaTableError(
                f"حروفُ الخانة {len(self.letters)} والمعدودُ {counted}؛ "
                "وحرفٌ يُعَدُّ مرّتين أو لا يُعَدُّ يُفسِد كسبَ الفصل."
            )

    @property
    def is_closed(self) -> bool:
        """أانفرد كلُّ حرفٍ في خانته؟ مُشتَقٌّ من التعادل لا مكتوبٌ في حقل."""

        return not self.tied_groups


@dataclass(frozen=True, slots=True)
class SeparationReport:
    """قوّةُ فصلِ مرشَّحٍ، مقيسةً على الخانات كلِّها لا موصوفةً."""

    letters_unresolved_before: int
    letters_unresolved_after: int
    separation_gain: int
    classes_closed: int
    classes_open: int
    per_class: tuple[ClassSeparation, ...]
    candidate_digest: str

    def __post_init__(self) -> None:
        expected = self.letters_unresolved_before - self.letters_unresolved_after
        if self.separation_gain != expected:
            raise SifaTableError(
                "كسبُ الفصل لا يطابق الفرقَ بين العددين؛ وكسبٌ يُكتَب ولا "
                "يُطرَح دعوى لا قياس."
            )

    @property
    def closes_every_class(self) -> bool:
        """أأُغلِقت الخاناتُ كلُّها؟ مُشتَقٌّ من عدد المفتوحة لا مكتوبٌ بجانبها."""

        return self.classes_open == 0


def separation_over(candidate: CandidateSifaTable) -> SeparationReport:
    """شغِّل قسمةَ الخانات على صفات المرشَّح، وأخرِج كسبَ الفصل مطروحًا.

    والقسمةُ على تساوي مجموعات الصفات لا على معناها: حرفان اتّفقت مجموعتاهما
    يبقيان متعادلَين وإن اختلفت العبارةُ عنهما، وحرفان اختلفتا ينفصلان وإن لم
    تُفهَم الصفةُ الفارقة.
    """

    if not isinstance(candidate, CandidateSifaTable):
        raise SifaTableError("القياسُ يُشغَّل على مرشَّحٍ مبنيٍّ بشرطه لا على غيره.")
    per_class: list[ClassSeparation] = []
    for rank in sorted(MAKHRAJ_LETTERS):
        letters = MAKHRAJ_LETTERS[rank]
        if len(letters) == 1:
            continue
        cells: dict[frozenset[str], list[str]] = {}
        for letter in letters:
            cells.setdefault(candidate.features_of(letter), []).append(letter)
        separated = tuple(cell[0] for cell in cells.values() if len(cell) == 1)
        tied = tuple(tuple(cell) for cell in cells.values() if len(cell) > 1)
        per_class.append(
            ClassSeparation(
                makhraj_rank=rank,
                letters=letters,
                separated_letters=separated,
                tied_groups=tied,
            )
        )
    before = makhraj_census().letters_in_underdetermined_patterns
    after = sum(len(group) for row in per_class for group in row.tied_groups)
    return SeparationReport(
        letters_unresolved_before=before,
        letters_unresolved_after=after,
        separation_gain=before - after,
        classes_closed=sum(1 for row in per_class if row.is_closed),
        classes_open=sum(1 for row in per_class if not row.is_closed),
        per_class=tuple(per_class),
        candidate_digest=candidate.rederive_table_digest(),
    )


def sifa_barrier_standing() -> ImportBarrierStanding:
    """اقرأ منزلةَ الحاجز من موضعه الآن، لا من كلمةٍ منسوخةٍ هنا."""

    for barrier in FEATURE_TABLE_IMPORT_BARRIERS:
        if barrier.table == SIFA_BARRIER_TABLE_NAME:
            return barrier.standing
    raise SifaTableError(
        f"لم يُوجَد حاجزٌ باسم {SIFA_BARRIER_TABLE_NAME!r}؛ وغيابُ الحاجز ليس رفعًا له."
    )


@dataclass(frozen=True, slots=True)
class BarrierLiftCondition:
    """شرطٌ واحدٌ من شروط رفع الحاجز، ووفاؤه مُشتَقٌّ لا مكتوب."""

    requirement: str
    what_satisfies_it: str
    is_met: bool


@dataclass(frozen=True, slots=True)
class BarrierLiftReport:
    """تقريرُ استيفاء الشرط: ما استُوفي وما بقي، والمنزلةُ مقروءةٌ حيّة."""

    standing: ImportBarrierStanding
    deposits: int
    conditions: tuple[BarrierLiftCondition, ...]
    open_question_identifier: str

    @property
    def condition_is_met(self) -> bool:
        """أاستُوفيت الشروطُ كلُّها؟ مُشتَقٌّ من أعضائها لا مكتوبٌ بجانبها."""

        return all(condition.is_met for condition in self.conditions)


def barrier_lift_report() -> BarrierLiftReport:
    """اقرأ اليومَ: أيُّ شروط رفع الحاجز استُوفي، وأيُّها بقي."""

    deposited = len(DEPOSITED_SIFA_TABLES)
    has_deposit = deposited > 0
    return BarrierLiftReport(
        standing=sifa_barrier_standing(),
        deposits=deposited,
        conditions=(
            BarrierLiftCondition(
                requirement="مصدرٌ مسمًّى بطبعته وجزئها وصفحتها",
                what_satisfies_it=(
                    "إيداعٌ يحمل `EditionCitation` بحقولها السبعة، وكلُّها "
                    "شرطُ إنشاءٍ يُرفَض عند فراغِ واحدٍ منها"
                ),
                is_met=has_deposit,
            ),
            BarrierLiftCondition(
                requirement="بصمةُ بايتاتٍ تُعاد اشتقاقًا",
                what_satisfies_it=(
                    "`rederive_table_digest` تُشتَقّ من بايتات الصفوف عند كلّ "
                    "نداء، فلا يُنسَخ رقمٌ يَتقادم صدقُه"
                ),
                is_met=has_deposit,
            ),
            BarrierLiftCondition(
                requirement="تصريحٌ بأنّ الجدول ليس دعوى هذه الشجرة",
                what_satisfies_it=(
                    "`attribution_declaration` نصٌّ غيرُ فارغٍ شرطُ إنشاء، على "
                    "منوال `imported_feature_vocabulary`"
                ),
                is_met=has_deposit,
            ),
        ),
        open_question_identifier=question_named(
            SIFA_OPEN_QUESTION_IDENTIFIER
        ).identifier,
    )


A_TABLE_WRITTEN_IN_THE_SESSION_IS_FORBIDDEN_NOTE: Final[str] = (
    "ATableWrittenInTheSessionIsTheThingTheBarrierForbids: الحاجزُ قام على "
    "جدولٍ بلا مصدرٍ ولا بصمة؛ فجدولٌ يُكتَب في الجلسة ثمّ تُلصَق به نسبةٌ "
    "معقولةُ الصورة هو العطبُ بعينه لا سدُّه"
)

A_CANDIDATE_IS_NOT_A_DEPOSIT_NOTE: Final[str] = (
    "ACandidateIsNotADeposit: المرشَّحُ صفوفٌ بلا نسبةٍ تُقاس ولا تُودَع، "
    "والمُودَعُ صفوفٌ بنسبةٍ كاملةٍ وبصمة؛ والفصلُ بينهما بالنوع لا بالتسمية"
)

MEASURING_A_CANDIDATE_IS_NOT_IMPORTING_IT_NOTE: Final[str] = (
    "MeasuringACandidateIsNotImportingIt: قياسُ قوّةِ فصلِ جدولٍ لا يُدخِله "
    "الشجرةَ ولا يُنشئ له نسبة؛ ومن قرأ القياسَ استيرادًا أدخل ما لم يجتز الباب"
)

THE_FEATURE_NAMES_COME_FROM_THE_SOURCE_NOTE: Final[str] = (
    "TheFeatureNamesComeFromTheSourceNotFromAVocabularyOfOurs: أسماءُ الصفات "
    "تُحمَل كما نطق بها المصدر، والفصلُ يقع على تساوي المجموعات لا على معناها؛ "
    "ومفردةٌ مغلقةٌ منّا تُلزِم الطبعةَ بقسمتنا ثمّ تُقرأ النتيجةُ خبرًا عنها"
)

THE_GAIN_IS_MEASURED_NOT_PROMISED_NOTE: Final[str] = (
    "TheGainIsMeasuredNotPromised: قوّةُ الفصل تخرج من تشغيل القسمة على "
    "الخانات لا من وعدٍ في نثر الطبعة؛ وجدولٌ لا يفصل يُسجَّل أنّه لا يفصل "
    "وإن علا مصدرُه"
)

THIS_MODULE_DOES_NOT_LIFT_THE_BARRIER_NOTE: Final[str] = (
    "ThisModuleReportsTheConditionAndDoesNotLiftTheBarrier: المنزلةُ تُقرأ من "
    "موضعها، ورفعُها تعديلٌ في وحدة الحاجز بيد من أودَع؛ ووحدةٌ ترفع حاجزَ "
    "نفسِها حاجزٌ بلا حارس"
)

SIFA_TABLE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_TABLE_WRITTEN_IN_THE_SESSION_IS_FORBIDDEN_NOTE,
    A_CANDIDATE_IS_NOT_A_DEPOSIT_NOTE,
    MEASURING_A_CANDIDATE_IS_NOT_IMPORTING_IT_NOTE,
    THE_FEATURE_NAMES_COME_FROM_THE_SOURCE_NOTE,
    THE_GAIN_IS_MEASURED_NOT_PROMISED_NOTE,
    THIS_MODULE_DOES_NOT_LIFT_THE_BARRIER_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def sifa_deposit_registration_digest() -> str:
    """بصمةُ هذا التسجيل، محسوبةً عند النداء لا مكتوبةً رقمًا ثابتًا."""

    return canonical_digest(
        canonical_bytes(
            {
                "deposits": [
                    deposit.as_canonical_content() for deposit in DEPOSITED_SIFA_TABLES
                ],
                "named_residuals": list(SIFA_TABLE_NAMED_RESIDUALS),
            }
        )
    )


if not DEPOSITED_SIFA_TABLES and sifa_barrier_standing() is (
    ImportBarrierStanding.LIFTED
):  # pragma: no cover - حارس
    raise RuntimeError(
        "الحاجزُ مرفوعٌ ولا إيداعَ في الشجرة؛ ورفعٌ بلا إيداعٍ يُبيح الاستيرادَ "
        "بما كان يمنعه."
    )
