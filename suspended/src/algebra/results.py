"""مكتبةُ نتائجَ مبنيّةٌ ديكارتيًّا: الشجرةُ جداءٌ مقروءٌ مساراتٍ، لا رفٌّ.

**ما تفعله هذه الوحدة**: تأخذ محاورَ مغلقةً — كلُّ محورٍ قيمُه مسرودةٌ —
فتُقيم عليها شجرةً كلُّ مسارٍ فيها من الجذر إلى الورقة نقطةٌ من الجداء،
وتفرض أنّ **لكلّ نقطةٍ خانةً** لا تخلو من واحدٍ من ثلاثة: نتيجةٌ مُودَعةٌ،
أو امتناعٌ مُعلَنٌ يُسمّي ناقضَه، أو موضعٌ مفتوحٌ يُسمّي فحصَه. وهي لا تعرف
موضوعًا: أسماءٌ على محاور.

`A_TREE_IS_A_PRODUCT_READ_AS_PATHS`: الشجرةُ ههنا ليست ترتيبَ حفظٍ اختاره
كاتبٌ، بل الجداءُ نفسُه مقروءًا مساراتٍ. فكلُّ عقدةٍ في مستوًى لها ابنٌ **لكلّ
قيمةٍ** من قيم المحور التالي؛ والفرعُ الناقصُ ثغرةٌ تُرَدّ عند الإنشاء لا
اختصارٌ يُحسَب حُسنَ ترتيب. ومن رتّب نتائجَه بالموضوع رأى ما عنده؛ ومن رتّبها
بالجداء رأى ما ليس عنده.

`AN_ABSENT_RESULT_IS_EITHER_FORBIDDEN_OR_OPEN`: لا خانةَ صامتة. وغيابُ نتيجةٍ
حالان لا يُخلَط أحدُهما بالآخر: **امتناعٌ** يُعلَن ويُسمّى ناقضُه، و**فتحٌ**
يُعلَن ويُسمّى الفحصُ الذي يحسمه. وما لا يُصنَّف في أحدهما نسيانٌ لا نتيجة.

`A_RESULT_CARRIES_ITS_CONDITIONS_NOT_ITS_NUMBER_ALONE`: النتيجةُ ليست رقمًا:
مصدرٌ يُعدّ منه، واسمٌ يطابق المقيس، وصفريٌّ مكافئ، وأوراكلُ منعدمٌ أو مُعلَن،
وثباتٌ تحت اختيارات التمثيل. وما نقص من الخمسة **يُسمّى** فيُخفَض الحكمُ من
«مُوثَّق» إلى «مبدئيّ»، ولا يُطوى في هامش.

`THE_RESIDUE_IS_PART_OF_THE_RESULT`: لكلّ نتيجةٍ بقيّةٌ تُخزَّن معها — ما لا
تقوله. ونتيجةٌ بلا بقيّةٍ نتيجةٌ لم تُقرَأ بعدُ، فتُرَدّ عند الإيداع.

`WHEN_A_WHOLE_SLAB_IS_OPEN_THE_GAP_IS_AN_AXIS_NOT_A_CELL`: إن كان كلُّ ما تحت
قيمةِ محورٍ على حالٍ واحدة، فالخبرُ في **المحور** لا في الخلايا؛ وإصلاحُه
قرارٌ واحدٌ لا رقعٌ بعددها. وهذا ما يخفيه سردُ النتائج ويُظهره التعدادُ التامّ.

`AN_AXIS_THAT_DOES_NOT_DISTINGUISH_IS_NOT_AN_AXIS`: قيمتان من محورٍ تتّفق
حالُهما على الجداء الباقي كلِّه لا يفرّق بينهما البناءُ، مهما اختلف اسماهما.
وذلك حكمٌ على القسمة لا على الشجرة، ويُخرَج صريحًا كيلا يُظَنّ التمييزُ حاصلًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product as _cartesian
from typing import Final

__all__ = [
    "AN_ABSENT_RESULT_IS_EITHER_FORBIDDEN_OR_OPEN_NOTE",
    "A_CLAIM_IS_TRIED_BY_THE_EVIDENCE_OF_ITS_OWN_KIND_NOTE",
    "EVIDENCE_TRIALS",
    "Evidence",
    "A_VACANCY_KIND_IS_DECLARED_NOT_INFERRED_NOTE",
    "VACANCIES_NEEDING_EVIDENCE",
    "Vacancy",
    "AN_AXIS_THAT_DOES_NOT_DISTINGUISH_IS_NOT_AN_AXIS_NOTE",
    "A_RESULT_CARRIES_ITS_CONDITIONS_NOT_ITS_NUMBER_ALONE_NOTE",
    "A_TREE_IS_A_PRODUCT_READ_AS_PATHS_NOTE",
    "Axis",
    "COMPLETENESS_CONDITIONS",
    "FORBIDDEN",
    "Finding",
    "Library",
    "OPEN",
    "Placement",
    "Product",
    "RESULTS_NAMED_RESIDUALS",
    "a_stipulation_has_a_measurable_shadow",
    "trial_for",
    "ResultsError",
    "SHELVED",
    "STATES",
    "THE_RESIDUE_IS_PART_OF_THE_RESULT_NOTE",
    "WHEN_A_WHOLE_SLAB_IS_OPEN_THE_GAP_IS_AN_AXIS_NOT_A_CELL_NOTE",
]


class ResultsError(ValueError):
    """رُفض محورٌ مفتوحٌ أو خانةٌ منسيّةٌ أو نتيجةٌ بلا شرطٍ مُعلَن."""


COMPLETENESS_CONDITIONS: Final[tuple[str, ...]] = (
    "ش١ عدٌّ مباشرٌ أو قياسٌ محجوب",
    "ش٢ اسمٌ يطابق المقيس",
    "ش٣ صفريٌّ مكافئٌ أو حصرٌ تامّ",
    "ش٤ الأوراكلُ منعدمٌ أو مُعلَن",
    "ش٥ ثابتٌ تحت اختيارات التمثيل",
)
"""شروطُ «الحدّ الأدنى المكتمل» الخمسة؛ وما نقص منها يُسمّى لا يُطوى."""


class Evidence(Enum):
    """أجناسُ الدليل الثلاثة؛ ولكلٍّ مِقامُ برهانٍ غيرُ مِقام أخيه.

    **المشهود** نصٌّ مقيس، دليلُه العدّ ولا تُقبَل الروايةُ عنه.
    **الاصطلاح** ما وضعه الواضعون، وحقيقتُه روايةٌ عنهم؛ فتسميتُه تُقبَل
    بنسبتها ولا تُنقَض بعدّ. **والاستنتاج** ما بُني ههنا، ودليلُه الاختبارُ
    بمقامٍ وصفريّ.

    وخلطُ الثلاثة هو الذي يُسقِط الدعاوى: أن يُختبَر استنتاجٌ بمعيار مشهود،
    أو يُروى اصطلاحٌ كأنّه مشهود.
    """

    ATTESTED = "مشهودٌ — نصٌّ يُعَدّ"
    STIPULATED = "اصطلاحٌ — روايةٌ عن واضعٍ تُنسَب"
    INFERRED = "استنتاجٌ — يُختبَر بمقامٍ وصفريّ"


EVIDENCE_TRIALS: Final[dict[Evidence, str]] = {
    Evidence.ATTESTED: "العدُّ على بايتاتٍ مُبصَّمة",
    Evidence.STIPULATED: "النسبةُ إلى واضعه ونصِّه",
    Evidence.INFERRED: "اختبارٌ بمقامٍ مُعلَنٍ وصفريٍّ مُسمّى",
}
"""مِقامُ البرهان لكلّ جنس؛ ولا يُجرَّب جنسٌ بمِقام غيره."""


def trial_for(kind: Evidence) -> str:
    """مِقامُ البرهان الذي يصحّ على هذا الجنس وحدَه."""

    if not isinstance(kind, Evidence):
        raise ResultsError("جنسُ الدليل عضوٌ في مفردته المغلقة لا نصٌّ حرّ.")
    return EVIDENCE_TRIALS[kind]


def a_stipulation_has_a_measurable_shadow(statement: str) -> bool:
    """أللاصطلاح ظلٌّ يُعَدّ؟ نعم متى وصف نمطًا في نصٍّ، لا متى سمّى وحدَه.

    فـ«يُسمّى هذا فاعلًا» تسميةٌ لا تُنقَض بعدّ. و«الفاعلُ مرفوع» يصف نمطًا
    في نصٍّ **فيُعَدّ نصيبُ موافقته**، ولا يُنقَض به الاصطلاحُ بل تُقاس
    كفايتُه. فمن أعفى الاصطلاحَ من العدّ بإطلاق أعفى معه كلَّ وصفٍ لبس ثوبَه.
    """

    return bool(statement.strip())


class Vacancy(Enum):
    """أجناسُ الخلوّ؛ مفردةٌ مغلقةٌ فيها عضوُ «لم يُصنَّف بعد» مُصرَّحٌ به.

    فالجداءُ يعطي **بتّةً واحدةً** لكلّ خانة: مملوءةٌ أم خالية. والخلوُّ أجناسٌ
    لا جنس، والبتّةُ لا تفرّق بينها ألبتّة. فتصنيفُ الخلوّ **فعلٌ ثانٍ يُعلَن
    بشاهده**، ولا يُشتَقّ من كون الخانة خالية.

    وعضوُ `UNCLASSIFIED` هو الحالُ الافتراضيّة، وليس نقصًا بل **صدقًا**:
    الجداءُ يحوّل غيابًا مجهولًا إلى غيابٍ موقوعٍ ثمّ يقف، والوقوفُ يُسمّى.
    """

    IMPOSSIBLE = "استحالةٌ مُعلَنةٌ قابلةٌ للنقض"
    UNATTESTED = "لا شاهدَ عليها فيما فُتِّش"
    UNREACHABLE = "لا تُبلَغ بما في اليد"
    REFUSED = "رُدَّت بقياسٍ جرى"
    UNRUN = "فحصُها مُعيَّنٌ ولم يُجرَ"
    UNCLASSIFIED = "خاليةٌ ولم يُصنَّف خلوُّها"


VACANCIES_NEEDING_EVIDENCE: Final[tuple[Vacancy, ...]] = (
    Vacancy.UNATTESTED,
    Vacancy.UNREACHABLE,
    Vacancy.REFUSED,
)
"""ثلاثةُ أجناسٍ لا تُدَّعى بلا شاهد.

والاستحالةُ ناقضُها هو شاهدُها، و`UNRUN` شاهدُه فحصُه المُعيَّن — فكلاهما
مشهودٌ ببنائه. وأمّا `UNCLASSIFIED` فلا شاهدَ له لأنّه **عدمُ تصنيفٍ** لا
تصنيف.
"""


def vacancy_of_a_bare_cell() -> Vacancy:
    """ما يعطيه الجداءُ وحدَه عن خانةٍ خالية: **جنسًا واحدًا لا غير**.

    فالنقطةُ من `Product.points()` تقول «ههنا خانة» ولا تقول شيئًا عن خلوّها.
    وهذه الدالّةُ تُودِع ذلك الحدَّ صريحًا: الجداءُ يحوّل غيابًا مجهولًا إلى
    غيابٍ موقوع، ثمّ **يقف**. وما بعدَه فعلٌ ثانٍ يُعلَن.
    """

    return Vacancy.UNCLASSIFIED


SHELVED: Final[str] = "مُودَع"
FORBIDDEN: Final[str] = "ممتنعٌ مُعلَن"
OPEN: Final[str] = "مفتوحٌ بفحصٍ يحسمه"
STATES: Final[tuple[str, ...]] = (SHELVED, FORBIDDEN, OPEN)
"""حالاتُ الخانة الثلاث؛ ولا رابعةَ لها إلّا النسيانُ وهو مردود."""

_VACUOUS_RESIDUES: Final[frozenset[str]] = frozenset(
    {"لا شيء", "لا بقيّة", "لا بقية", "—", "-", "لا يوجد", "لا شيءَ"}
)


def _reject_disjunction(text: str, what: str) -> None:
    """«أ أو ب» في خانةٍ واحدةٍ امتناعٌ عن القسمة لا قسمة."""

    if " أو " in text or "/" in text:
        raise ResultsError(
            f"{what} «{text}» شيئان في خانةٍ واحدةٍ، والقسمةُ لا «أو» فيها."
        )


@dataclass(frozen=True, slots=True)
class Axis:
    """محورٌ مغلق: اسمُه وقيمُه مسرودةً مرتَّبةً متمايزة."""

    name: str
    values: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ResultsError("محورٌ بلا اسمٍ لا يُبنى عليه.")
        if not self.values:
            raise ResultsError(f"محورُ «{self.name}» بلا قيم؛ والمحورُ المفتوحُ لا يُجدَأ.")
        if len(set(self.values)) != len(self.values):
            raise ResultsError(f"قيمُ «{self.name}» تُسمّى أسماءً متمايزة.")
        for value in self.values:
            if not value.strip():
                raise ResultsError(f"قيمةٌ خاليةٌ في محور «{self.name}».")
            _reject_disjunction(value, "قيمةُ محور")

    def __len__(self) -> int:
        return len(self.values)


@dataclass(frozen=True, slots=True)
class Product:
    """جداءُ محاورَ مغلقةٍ؛ ونقاطُه هي أوراقُ الشجرة بعينها."""

    axes: tuple[Axis, ...]

    def __post_init__(self) -> None:
        if not self.axes:
            raise ResultsError("جداءٌ بلا محاورَ ليس جداءً.")
        names = [axis.name for axis in self.axes]
        if len(set(names)) != len(names):
            raise ResultsError("المحاورُ تُسمّى أسماءً متمايزة.")

    @property
    def depth(self) -> int:
        """عددُ المحاور، وهو ارتفاعُ الشجرة من الجذر إلى الورقة."""

        return len(self.axes)

    @property
    def size(self) -> int:
        """عددُ النقاط: حاصلُ ضربِ أحجام المحاور، لا عددُ ما عندنا."""

        total = 1
        for axis in self.axes:
            total *= len(axis)
        return total

    def points(self) -> tuple[tuple[str, ...], ...]:
        """النقاطُ كلُّها بترتيبٍ ثابت — التعدادُ الشاملُ لا عيّنةٌ منه."""

        return tuple(_cartesian(*(axis.values for axis in self.axes)))

    def index_of(self, axis_name: str) -> int:
        """رتبةُ محورٍ باسمه؛ ويُرَدّ الاسمُ المجهولُ بالتسمية لا بمفتاحٍ ضائع."""

        for position, axis in enumerate(self.axes):
            if axis.name == axis_name:
                return position
        raise ResultsError(f"«{axis_name}» ليس محورًا في هذا الجداء.")

    def check(self, coordinate: tuple[str, ...]) -> None:
        """فحصُ نقطةٍ: طولُها عددُ المحاور، وكلُّ حدٍّ من قيم محوره."""

        if len(coordinate) != self.depth:
            raise ResultsError(
                f"إحداثيٌّ بطول {len(coordinate)} على جداءٍ عمقُه {self.depth}."
            )
        for axis, value in zip(self.axes, coordinate, strict=True):
            if value not in axis.values:
                raise ResultsError(f"«{value}» ليس من قيم محور «{axis.name}».")


@dataclass(frozen=True, slots=True)
class Finding:
    """نتيجةٌ مُودَعة: قولُها ومصدرُها ووحدتُها وصفريُّها وأوراكلُها وبقيّتُها."""

    statement: str
    source: str
    unit: str
    null: str
    oracle: str
    invariance: str
    residue: str
    unmet: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        fields = (
            ("القول", self.statement),
            ("المصدر", self.source),
            ("الوحدة", self.unit),
            ("الصفريّ", self.null),
            ("الأوراكل", self.oracle),
            ("الثبات", self.invariance),
            ("البقيّة", self.residue),
        )
        for label, text in fields:
            if not text.strip():
                raise ResultsError(
                    f"نتيجةٌ بلا {label}؛ والنتيجةُ ليست رقمًا وحدَه "
                    "(A_RESULT_CARRIES_ITS_CONDITIONS_NOT_ITS_NUMBER_ALONE)."
                )
        if self.residue.strip() in _VACUOUS_RESIDUES:
            raise ResultsError(
                f"«{self.residue}» ليست بقيّةً بل نفيُها؛ ونتيجةٌ بلا بقيّةٍ "
                "نتيجةٌ لم تُقرَأ (THE_RESIDUE_IS_PART_OF_THE_RESULT)."
            )
        if len(set(self.unmet)) != len(self.unmet):
            raise ResultsError("الشرطُ المخرومُ لا يُذكَر مرّتين.")
        for condition in self.unmet:
            if condition not in COMPLETENESS_CONDITIONS:
                raise ResultsError(f"«{condition}» ليس من الشروط الخمسة المُعلَنة.")

    @property
    def is_minimally_complete(self) -> bool:
        """الحدُّ الأدنى المكتمل: الشروطُ الخمسةُ كلُّها قائمة."""

        return not self.unmet

    @property
    def standing(self) -> str:
        """«مُوثَّق» عند تمام الشروط، و«مبدئيّ» عند خرمِ واحدٍ منها."""

        return "مُوثَّق" if self.is_minimally_complete else "مبدئيّ"

    def conditions(self) -> tuple[tuple[str, bool], ...]:
        """الشروطُ الخمسةُ كلُّها بحالها — تعدادٌ تامٌّ لا ذكرُ الناقص وحدَه."""

        broken = set(self.unmet)
        return tuple(
            (condition, condition not in broken)
            for condition in COMPLETENESS_CONDITIONS
        )


@dataclass(frozen=True, slots=True)
class Placement:
    """خانةٌ على نقطةٍ من الجداء: مُودَعةٌ أو ممتنعةٌ مُعلَنةٌ أو مفتوحةٌ بفحص."""

    coordinate: tuple[str, ...]
    finding: Finding | None = None
    forbidden_because: str = ""
    refuted_by: str = ""
    open_test: str = ""
    absence: Vacancy | None = None
    absence_evidence: str = ""

    def __post_init__(self) -> None:
        if not self.coordinate:
            raise ResultsError("خانةٌ بلا إحداثيٍّ لا تُوضَع في شجرة.")
        kinds = (
            self.finding is not None,
            bool(self.forbidden_because.strip()),
            bool(self.open_test.strip()),
        )
        if sum(kinds) != 1:
            raise ResultsError(
                f"خانةُ {self.path} تحمل {sum(kinds)} من ثلاثٍ، والواجبُ واحدةٌ: "
                "نتيجةٌ أو امتناعٌ أو فتحٌ "
                "(AN_ABSENT_RESULT_IS_EITHER_FORBIDDEN_OR_OPEN)."
            )
        if self.forbidden_because.strip():
            if not self.refuted_by.strip():
                raise ResultsError(
                    f"امتناعُ {self.path} بلا ناقضٍ مُسمًّى؛ والامتناعُ دعوًى "
                    "قابلةٌ للنقض لا إعفاءٌ من الملء."
                )
        elif self.refuted_by.strip():
            raise ResultsError(f"ناقضٌ في {self.path} بلا امتناعٍ يَنقُضه.")
        if self.open_test.strip():
            _reject_disjunction(self.open_test, "فحصُ موضعٍ مفتوح")
        self._check_vacancy()

    def _check_vacancy(self) -> None:
        """جنسُ الخلوِّ يُعلَن بشاهده، ولا يُقرَأ من كون الخانة خالية."""

        if self.absence is not None and not isinstance(self.absence, Vacancy):
            raise ResultsError("جنسُ الخلوِّ عضوٌ في مفردته المغلقة لا نصٌّ حرّ.")
        if self.finding is not None:
            if self.absence is not None or self.absence_evidence.strip():
                raise ResultsError(
                    f"خانةُ {self.path} مملوءةٌ ويُصنَّف خلوُّها؛ "
                    "والمملوءةُ لا خلوَّ لها يُصنَّف."
                )
            return
        if self.forbidden_because.strip():
            if self.absence not in (None, Vacancy.IMPOSSIBLE):
                raise ResultsError(
                    f"امتناعُ {self.path} جنسُه الاستحالةُ لا غير؛ "
                    "ودعوى الامتناع نفسُها هي التصنيف."
                )
            return
        if self.absence is Vacancy.UNCLASSIFIED:
            raise ResultsError(
                f"خانةُ {self.path} تحمل فحصًا مُعيَّنًا فخلوُّها **مصنَّف**؛ "
                "و«غيرُ مصنَّف» جنسٌ للخانة العارية من الجداء لا للمُودَعة."
            )
        if self.absence in VACANCIES_NEEDING_EVIDENCE:
            if not self.absence_evidence.strip():
                raise ResultsError(
                    f"خلوُّ {self.path} صُنِّف «{self.absence.value}» بلا شاهد؛ "
                    "و«لا شاهدَ عليها» غيرُ «لم يُفتَّش عنها»، والفرقُ يُكتَب "
                    "(A_VACANCY_KIND_IS_DECLARED_NOT_INFERRED)."
                )
        elif self.absence_evidence.strip():
            raise ResultsError(f"شاهدٌ في {self.path} بلا جنسِ خلوٍّ يشهد له.")

    @property
    def path(self) -> str:
        """المسارُ من الجذر إلى هذه الخانة، مقروءًا سطرًا واحدًا."""

        return " ← ".join(self.coordinate)

    @property
    def state(self) -> str:
        """حالُ الخانة: واحدةٌ من الثلاث لا غير."""

        if self.finding is not None:
            return SHELVED
        if self.forbidden_because.strip():
            return FORBIDDEN
        return OPEN

    @property
    def vacancy(self) -> Vacancy | None:
        """جنسُ الخلوّ، أو `None` للمملوءة؛ والمفتوحةُ بلا إعلانٍ **غيرُ مصنَّفة**."""

        if self.finding is not None:
            return None
        if self.forbidden_because.strip():
            return Vacancy.IMPOSSIBLE
        return self.absence or Vacancy.UNRUN

    @property
    def text(self) -> str:
        """نصُّ الخانة أيًّا كانت حالُها؛ فالمفتوحُ يقول فحصَه لا يسكت."""

        if self.finding is not None:
            return self.finding.statement
        if self.forbidden_because.strip():
            return f"{self.forbidden_because} — ينقضه: {self.refuted_by}"
        return f"الفحصُ الفاصل: {self.open_test}"

    def summary(self, width: int = 72) -> str:
        """سطرٌ واحدٌ: الحالُ ثمّ النصُّ مقصوصًا عند حدٍّ مُعلَن."""

        if width < 8:
            raise ResultsError("عرضٌ دون ثمانيةٍ لا يُبقي من النصّ شيئًا.")
        body = " ".join(self.text.split())
        if len(body) > width:
            body = body[: width - 1].rstrip() + "…"
        return f"[{self.state}] {body}"


@dataclass(frozen=True, slots=True)
class Library:
    """شجرةُ نتائجَ على جداءٍ مُعلَن؛ وتمامُها شرطُ إنشاءٍ لا دعوى."""

    name: str
    product: Product
    placements: tuple[Placement, ...]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ResultsError("مكتبةٌ بلا اسمٍ لا يُحال إليها.")
        seen: set[tuple[str, ...]] = set()
        for placement in self.placements:
            self.product.check(placement.coordinate)
            if placement.coordinate in seen:
                raise ResultsError(f"خانةُ {placement.path} موضوعةٌ مرّتين.")
            seen.add(placement.coordinate)
        holes = [point for point in self.product.points() if point not in seen]
        if holes:
            shown = "، ".join(" ← ".join(point) for point in holes[:4])
            raise ResultsError(
                f"ثغراتٌ غيرُ مُعلَنةٍ ({len(holes)} من {self.product.size}): "
                f"{shown}… — وفرعٌ ناقصٌ ثغرةٌ لا اختصار "
                "(A_TREE_IS_A_PRODUCT_READ_AS_PATHS)."
            )

    @property
    def table(self) -> dict[tuple[str, ...], Placement]:
        """الخاناتُ مفهرسةً بإحداثيّها."""

        return {placement.coordinate: placement for placement in self.placements}

    def at(self, coordinate: tuple[str, ...]) -> Placement:
        """خانةٌ بإحداثيّها؛ ويُرَدّ المجهولُ بالتسمية لا بمفتاحٍ ضائع."""

        self.product.check(coordinate)
        return self.table[coordinate]

    def state_at(self, coordinate: tuple[str, ...]) -> str:
        """حالُ خانةٍ بإحداثيّها."""

        return self.at(coordinate).state

    def paths(self) -> tuple[tuple[tuple[str, ...], Placement], ...]:
        """الجداءُ مقروءًا مساراتٍ، بترتيب النقاط الثابت."""

        table = self.table
        return tuple((point, table[point]) for point in self.product.points())

    def vacancy_census(self) -> dict[Vacancy, int]:
        """عدُّ أجناس الخلوّ الخمسة كلِّها — والصفرُ يُطبَع، والمُهمَلُ يُعَدّ.

        فالمقصودُ من هذا العدِّ رقمٌ واحد: **كم غيابًا لم يُصنَّف بعد**. وهو
        الرقمُ الذي لا يظهر في عدِّ الحالات الثلاث ألبتّة.
        """

        counts = {kind: 0 for kind in Vacancy}
        for placement in self.placements:
            kind = placement.vacancy
            if kind is not None:
                counts[kind] += 1
        return counts

    def absences_of(self, kind: Vacancy) -> tuple[Placement, ...]:
        """الخاناتُ التي خلوُّها من هذا الجنس؛ والجنسُ يُطلَب باسمه لا برقمه."""

        return tuple(
            placement for placement in self.placements if placement.vacancy is kind
        )

    def census(self) -> dict[str, int]:
        """عدُّ الحالات الثلاث كلِّها — والصفرُ يُطبَع ولا يُحذَف."""

        counts = {state: 0 for state in STATES}
        for placement in self.placements:
            counts[placement.state] += 1
        return counts

    def covers_the_product(self) -> bool:
        """مجموعُ الحالات الثلاث يساوي الجداءَ كلَّه — وهو شرطُ الإنشاء."""

        return sum(self.census().values()) == self.product.size

    def slice_of(self, axis_name: str, value: str) -> tuple[Placement, ...]:
        """الخاناتُ التي يأخذ فيها محورٌ قيمةً بعينها."""

        position = self.product.index_of(axis_name)
        if value not in self.product.axes[position].values:
            raise ResultsError(f"«{value}» ليس من قيم محور «{axis_name}».")
        return tuple(
            placement
            for _, placement in self.paths()
            if placement.coordinate[position] == value
        )

    def slabs_entirely(self, state: str) -> tuple[tuple[str, str], ...]:
        """قيمُ المحاور التي كلُّ ما تحتها على حالٍ واحدة — فالخبرُ في المحور."""

        if state not in STATES:
            raise ResultsError(f"«{state}» ليس من الحالات الثلاث.")
        found: list[tuple[str, str]] = []
        for axis in self.product.axes:
            for value in axis.values:
                under = self.slice_of(axis.name, value)
                if all(placement.state == state for placement in under):
                    found.append((axis.name, value))
        return tuple(found)

    def indistinguishable_values(self, axis_name: str) -> tuple[tuple[str, ...], ...]:
        """قيمُ محورٍ لا يفرّق بينها البناءُ — حكمٌ على القسمة لا على الشجرة."""

        position = self.product.index_of(axis_name)
        groups: dict[tuple[str, ...], list[str]] = {}
        rest = tuple(
            axis.values
            for index, axis in enumerate(self.product.axes)
            if index != position
        )
        others = tuple(_cartesian(*rest)) if rest else ((),)
        for value in self.product.axes[position].values:
            signature = []
            for other in others:
                point = list(other)
                point.insert(position, value)
                signature.append(self.state_at(tuple(point)))
            groups.setdefault(tuple(signature), []).append(value)
        return tuple(tuple(members) for members in groups.values() if len(members) > 1)

    def findings(self) -> tuple[Finding, ...]:
        """النتائجُ المُودَعةُ بترتيب المسارات."""

        return tuple(
            placement.finding
            for _, placement in self.paths()
            if placement.finding is not None
        )

    def certified(self) -> tuple[Finding, ...]:
        """ما تمّت شروطُه الخمسة."""

        return tuple(one for one in self.findings() if one.is_minimally_complete)

    def provisional(self) -> tuple[Finding, ...]:
        """ما خُرِم فيه شرطٌ فصار مبدئيًّا — مُعلَنًا لا مطويًّا."""

        return tuple(one for one in self.findings() if not one.is_minimally_complete)

    def broken_conditions(self) -> dict[str, int]:
        """كم نتيجةً خُرِم فيها كلُّ شرط — تعدادٌ تامٌّ على الخمسة."""

        counts = {condition: 0 for condition in COMPLETENESS_CONDITIONS}
        for finding in self.findings():
            for condition in finding.unmet:
                counts[condition] += 1
        return counts

    def residues(self) -> tuple[str, ...]:
        """ما لا تقوله النتائج، مُخرَجًا بطلبٍ كما تُخرَج النتائج."""

        return tuple(finding.residue for finding in self.findings())

    def open_loci(self) -> tuple[tuple[str, str], ...]:
        """المواضعُ المفتوحةُ ومعها الفحصُ الفاصلُ لكلٍّ منها."""

        return tuple(
            (placement.path, placement.open_test)
            for _, placement in self.paths()
            if placement.state == OPEN
        )

    def forbidden_claims(self) -> tuple[tuple[str, str, str], ...]:
        """الامتناعاتُ المُعلَنةُ ومعها ناقضُ كلٍّ منها."""

        return tuple(
            (placement.path, placement.forbidden_because, placement.refuted_by)
            for _, placement in self.paths()
            if placement.state == FORBIDDEN
        )

    def assert_not_reportable_as_settled(self) -> None:
        """يُرَدّ إعلانُ التمام ما بقي موضعٌ مفتوح، ويُسمّى أوّلُه وفحصُه."""

        loci = self.open_loci()
        if loci:
            path, test = loci[0]
            raise ResultsError(f"{len(loci)} موضعًا مفتوحًا؛ أوّلُها {path} وفحصُه: {test}.")

    def tree(self, width: int = 72) -> str:
        """الشجرةُ مطبوعةً بالإزاحة: مسارٌ لكلّ نقطةٍ من الجداء، لا أقلّ."""

        rows: list[str] = [self.name]
        self._walk((), rows, width)
        return "\n".join(rows)

    def _walk(self, prefix: tuple[str, ...], rows: list[str], width: int) -> None:
        depth = len(prefix)
        indent = "  " * (depth + 1)
        for value in self.product.axes[depth].values:
            here = (*prefix, value)
            if depth + 1 == self.product.depth:
                rows.append(f"{indent}{value} · {self.at(here).summary(width)}")
            else:
                rows.append(f"{indent}{value}")
                self._walk(here, rows, width)


A_TREE_IS_A_PRODUCT_READ_AS_PATHS_NOTE: Final[str] = (
    "ATreeIsAProductReadAsPaths: الشجرةُ الجداءُ مقروءًا مساراتٍ لا ترتيبَ "
    "حفظٍ اختاره كاتب؛ والفرعُ الناقصُ ثغرةٌ تُرَدّ لا اختصارٌ يُحسَب حُسنَ ترتيب"
)

AN_ABSENT_RESULT_IS_EITHER_FORBIDDEN_OR_OPEN_NOTE: Final[str] = (
    "AnAbsentResultIsEitherForbiddenOrOpen: غيابُ نتيجةٍ إمّا امتناعٌ يُسمّى "
    "ناقضُه وإمّا فتحٌ يُسمّى فحصُه، وما ليس أحدَهما نسيانٌ لا نتيجة"
)

A_RESULT_CARRIES_ITS_CONDITIONS_NOT_ITS_NUMBER_ALONE_NOTE: Final[str] = (
    "AResultCarriesItsConditionsNotItsNumberAlone: النتيجةُ مصدرٌ ووحدةٌ "
    "وصفريٌّ وأوراكلُ وثبات؛ وما نقص منها يُسمّى فيُخفَض الحكمُ إلى «مبدئيّ»"
)

THE_RESIDUE_IS_PART_OF_THE_RESULT_NOTE: Final[str] = (
    "TheResidueIsPartOfTheResult: لكلّ نتيجةٍ بقيّةٌ تُخزَّن معها، ونتيجةٌ "
    "بلا بقيّةٍ نتيجةٌ لم تُقرَأ بعدُ فتُرَدّ عند الإيداع"
)

WHEN_A_WHOLE_SLAB_IS_OPEN_THE_GAP_IS_AN_AXIS_NOT_A_CELL_NOTE: Final[str] = (
    "WhenAWholeSlabIsOpenTheGapIsAnAxisNotACell: قيمةُ محورٍ كلُّ ما تحتها "
    "على حالٍ واحدةٍ خبرٌ عن المحور، وإصلاحُه قرارٌ واحدٌ لا رقعٌ بعددها"
)

AN_AXIS_THAT_DOES_NOT_DISTINGUISH_IS_NOT_AN_AXIS_NOTE: Final[str] = (
    "AnAxisThatDoesNotDistinguishIsNotAnAxis: قيمتان تتّفق حالُهما على "
    "الجداء الباقي كلِّه لا يفرّق بينهما البناءُ مهما اختلف اسماهما"
)

A_CLAIM_IS_TRIED_BY_THE_EVIDENCE_OF_ITS_OWN_KIND_NOTE: Final[str] = (
    "AClaimIsTriedByTheEvidenceOfItsOwnKind: المشهودُ يُعَدّ، والاصطلاحُ "
    "يُنسَب، والاستنتاجُ يُختبَر بمقامٍ وصفريّ؛ وخلطُ المِقامات يُسقِط "
    "الدعاوى — واصطلاحٌ يصف نمطًا في نصٍّ له ظلٌّ يُعَدّ، فلا يُعفى بإطلاق"
)

A_VACANCY_KIND_IS_DECLARED_NOT_INFERRED_NOTE: Final[str] = (
    "AVacancyKindIsDeclaredNotInferred: الجداءُ يعطي بتّةً واحدةً لكلّ خانة — "
    "مملوءةٌ أم خالية — والخلوُّ أجناسٌ: استحالةٌ، ولا شاهدَ، ولا بلوغَ، وردٌّ "
    "مقيس؛ فتصنيفُه فعلٌ ثانٍ يُعلَن بشاهده ولا يُشتَقّ من الخلوّ"
)

RESULTS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_CLAIM_IS_TRIED_BY_THE_EVIDENCE_OF_ITS_OWN_KIND_NOTE,
    A_VACANCY_KIND_IS_DECLARED_NOT_INFERRED_NOTE,
    A_TREE_IS_A_PRODUCT_READ_AS_PATHS_NOTE,
    AN_ABSENT_RESULT_IS_EITHER_FORBIDDEN_OR_OPEN_NOTE,
    A_RESULT_CARRIES_ITS_CONDITIONS_NOT_ITS_NUMBER_ALONE_NOTE,
    THE_RESIDUE_IS_PART_OF_THE_RESULT_NOTE,
    WHEN_A_WHOLE_SLAB_IS_OPEN_THE_GAP_IS_AN_AXIS_NOT_A_CELL_NOTE,
    AN_AXIS_THAT_DOES_NOT_DISTINGUISH_IS_NOT_AN_AXIS_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة."""
