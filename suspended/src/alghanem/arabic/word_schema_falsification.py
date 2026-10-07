"""«كلمةٌ = جذرٌ + وزنٌ + زوائد»: شروطُ إبطالٍ مكتوبةٌ قبل القياس، ثمّ قياس.

**الدعوى الواردة** (من محادثةٍ أخرى، بنصّها): أنّ مستوًى وسطيًّا `T(2.5)` قد
«بُرهِن ✅»، وأنّ الاسمَ والفعلَ والحرفَ تحت قانونٍ واحد: «كلمة = جذر + وزن +
زوائد»؛ ومثالُه للحرف: «مِنْ = م-ن + حرف_بسيط + ْ» بجذرٍ **اصطلاحيّ**.

`A_SCHEMA_THAT_ABSORBS_ITS_COUNTEREXAMPLES_SAYS_NOTHING`: الدعوى بصيغتها لا
تُبطَل بشيء: كلُّ كلمةٍ تُخالف يُقال لها «جذرٌ اصطلاحيّ» فتدخل. وهذا ما فعله
النصُّ بـ«مِنْ» صراحةً. فالمقيسُ ههنا ليس «أصحيحةٌ هي» — بل **كم تُخبر**: هل
يُعيِّن السطحُ تحليلًا واحدًا، وهل يغطّي، وهل يمنع ما تمنعه العربيّة.

`THE_TREE_ALREADY_WITHHELD_THIS_LAYER`: طبقةُ «المقطع والوزن» **محجوزةٌ**
مُسجَّلةً في `word_structure_dictionary_preregistration` بمنزلة «فرضٌ مُعلَنُ
العطب»، وشرطُ دخولها مكتوبٌ: وحدةُ سيلبنةٍ في الشجرة، وتصريحٌ بأنّ الوزنَ
**إسقاطٌ مشتقٌّ لا كائنٌ صرفيٌّ مولود**، وأرضيّةُ قبولٍ مكتوبةٌ قبل قياسها على
مدوَّنةٍ مُبصَّمة. فالدعوى لا تأتي بجديدٍ على الشجرة: هي **الفرضُ نفسُه**
مختومًا بعلامة ✅ قبل أن يستوفيَ شرطَ دخوله.

`AN_AFFIX_SET_IS_WHAT_MAKES_THE_SCHEMA_SAY_ANYTHING`: «زوائد» بلا حصرٍ تقبل كلَّ
بقيّة. والعربيّةُ تحصرها بـ«سألتمونيها»، وهو حصرٌ **لم تذكره الدعوى**؛ فإن كان
أكثرُ التحليلات التي تقبلها الدعوى ممتنعًا بهذا الحصر، فالمحتوى كلُّه في الشرط
المحذوف لا في الصيغة المذكورة.

`THE_AUGMENT_SET_IS_A_RECEIVED_CONVENTION_NOT_A_MEASURED_TABLE`: «سألتمونيها»
مأخوذةٌ اصطلاحًا مشهورًا، لا جدولًا مُبصَّمًا في هذه الشجرة؛ فقياسُ ت٣ مشروطٌ
بها ويُقرأ بشرطه.

`THIS_IS_A_TEST_NOT_A_VERDICT_ON_ARABIC`: المقيسُ سلوكُ **صيغةٍ مقترَحة** على
مدوَّنةٍ مُبصَّمة، لا حكمٌ على الصرف العربيّ. وسقوطُ شرطٍ يُسقِط الصيغةَ
بصياغتها هذه، ولا يقول إنّ الجذرَ والوزنَ باطلان.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from itertools import combinations
from typing import Final

from .letter_fingerprint import fold_root
from .maqayis_root_table_deposit import read_root_table_bytes, root_table_digest

__all__ = [
    "AUGMENT_LETTERS",
    "A_FILE_THAT_NAMES_MARKS_ENTERS_THE_CORPUS_NOTE",
    "A_SCHEMA_THAT_ABSORBS_ITS_COUNTEREXAMPLES_SAYS_NOTHING_NOTE",
    "AN_AFFIX_SET_IS_WHAT_MAKES_THE_SCHEMA_SAY_ANYTHING_NOTE",
    "CorpusRule",
    "FalsificationCondition",
    "RECEIVED_CLAIM",
    "SCHEMA_NAMED_RESIDUALS",
    "THE_AUGMENT_SET_IS_A_RECEIVED_CONVENTION_NOT_A_MEASURED_TABLE_NOTE",
    "THE_TREE_ALREADY_WITHHELD_THIS_LAYER_NOTE",
    "THIS_IS_A_TEST_NOT_A_VERDICT_ON_ARABIC_NOTE",
    "WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA",
    "SchemaVerdict",
    "WordSchemaError",
    "candidate_roots",
    "corpus_words",
    "deposited_trilateral_roots",
    "derive_coverage",
    "derive_determination",
    "derive_residue_legality",
    "read_verdicts",
]

RECEIVED_CLAIM: Final[str] = (
    "كلمة = جذر + وزن + زوائد — سواء كان اسمًا أو فعلًا أو حرفًا؛ ومثالُه "
    "للحرف: «مِنْ = م-ن + حرف_بسيط + ْ» بجذرٍ اصطلاحيٍّ لا دلاليّ"
)
"""الدعوى كما وردت، بنصّها، لا بإعادة صياغتي لها."""


class WordSchemaError(ValueError):
    """رُفض مدخلٌ أو قراءةٌ ناقصة؛ ولا يُحمَل على أقرب مقبول."""


class SchemaVerdict(Enum):
    """منازلُ الحكم، مغلقةً: لا منزلةَ اسمُها «مؤيَّدٌ جزئيًّا»."""

    SURVIVED = "صمد"
    FALSIFIED = "سقط"
    UNMEASURED = "غير مقيس"


@dataclass(frozen=True, slots=True)
class FalsificationCondition:
    """شرطُ إبطالٍ بعتبةٍ عدديّةٍ مكتوبةٍ **قبل** النظر."""

    identifier: str
    statement: str
    threshold: str
    what_it_refutes: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.statement, "النصّ"),
            (self.threshold, "العتبة"),
            (self.what_it_refutes, "ما يُبطِله"),
        ):
            if not value.strip():
                raise WordSchemaError(
                    f"{self.identifier}: {name} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ "
                    "وشرطٌ بلا عتبةٍ يُفصَّل على مقاس الرقم بعد رؤيته."
                )


WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA: Final[tuple[FalsificationCondition, ...]] = (
    FalsificationCondition(
        identifier="ت١ التعيين",
        statement=(
            "إن كان السطحُ يُعيِّن التحليلَ، فأكثرُ الكلمات تقبل جذرًا مُودَعًا "
            "واحدًا بوصفه متتاليةً جزئيّةً مرتَّبةً من حروفها"
        ),
        threshold="يسقط الشرطُ إن كان وسيطُ عدد الجذور المرشَّحة للكلمة أكبرَ من 1",
        what_it_refutes=(
            "يُبطِل أنّ «كلمة = جذر + وزن + زوائد» **تحليلٌ**؛ فتصير مخطَّطًا "
            "يقبل تحليلاتٍ كثيرةً ولا يختار بينها"
        ),
    ),
    FalsificationCondition(
        identifier="ت٢ التغطية",
        statement=(
            "إن كانت الصيغةُ تغطّي، فقليلٌ من الكلمات لا يقبل جذرًا مُودَعًا "
            "واحدًا على القراءة التوصيليّة (الجذرُ متتاليةٌ جزئيّةٌ مرتَّبة)"
        ),
        threshold="يسقط الشرطُ إن تجاوزت نسبةُ الكلمات بلا مرشَّحٍ واحدٍ 5%",
        what_it_refutes=(
            "يُبطِل كفايةَ القراءة التوصيليّة، ويُظهِر أنّ الصيغةَ تحتاج آليّةً "
            "غيرَ تجاوريّةٍ لم تذكرها (الإعلالُ والإبدالُ وجمعُ التكسير)"
        ),
    ),
    FalsificationCondition(
        identifier="ت٣ الحصر",
        statement=(
            "إن كانت «الزوائد» في الصيغة هي زوائدَ العربيّة، فأكثرُ التحليلات "
            "التي تقبلها الصيغةُ يكون باقيها من «سألتمونيها»"
        ),
        threshold=(
            "يسقط الشرطُ إن كانت نسبةُ التحليلات المقبولة التي باقيها داخلَ "
            "«سألتمونيها» أقلَّ من 50%"
        ),
        what_it_refutes=(
            "يُبطِل أنّ الصيغةَ المذكورةَ تحمل محتواها؛ فيكون المحتوى في حصرٍ "
            "**لم تذكره** لا في الصيغة"
        ),
    ),
)
"""شروطُ الإبطال الثلاثة، مكتوبةً قبل تشغيل القياس ومدفوعةً قبل قراءة رقمٍ."""

AUGMENT_LETTERS: Final[frozenset[str]] = frozenset("سألتمونيها")
"""حروفُ الزيادة اصطلاحًا مشهورًا («سألتمونيها»)، لا جدولًا مُبصَّمًا هنا."""

_ARABIC_LETTERS: Final[str] = "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"
_MARK_CODEPOINTS: Final[tuple[int, ...]] = (*range(0x064B, 0x0653), 0x0670, 0x0640)
"""نقاطُ الحركات والألفِ الخنجريّةِ والتطويل **بأرقامها**، لا بحروفها.

وكتابتُها حروفًا تُدخِل هذا الملفَّ في المدوَّنة التي يقيسها غيرُه: نثرُ
الشجرة هو مجتمعُ قياس `pair_sample_widening`، فعلامةٌ مكتوبةٌ ههنا تصير
مشاهَدةً هناك. وقد وقع ذلك فعلًا (`A_FILE_THAT_NAMES_MARKS_ENTERS_THE_CORPUS`).
"""

_MARKS: Final[re.Pattern[str]] = re.compile(
    "[" + "".join(chr(point) for point in _MARK_CODEPOINTS) + "]"
)


@dataclass(frozen=True, slots=True)
class CorpusRule:
    """قاعدةُ استخراج الكلمات، مكتوبةً كي يُعاد العدُّ بها لا بغيرها."""

    column: str = "body_text"
    minimum_letters: int = 3
    maximum_letters: int = 8
    folding: str = "fold_root المُودَع: أإؤئآ←ء، ٱ←ا، ى←ي"

    def describe(self) -> str:
        """وصفُ القاعدة في سطرٍ يُنقَل مع كلّ رقم."""

        return (
            f"عمود {self.column}؛ الكلماتُ المتمايزةُ بعد حذف العلامات "
            f"وطيِّ الهمزات ({self.folding})؛ الطولُ "
            f"{self.minimum_letters}–{self.maximum_letters} حرفًا"
        )


CORPUS_RULE: Final[CorpusRule] = CorpusRule()


@lru_cache(maxsize=1)
def deposited_trilateral_roots() -> frozenset[str]:
    """الجذورُ الثلاثيّةُ المُودَعةُ مطويّةً، من بايتات الجدول لا من ذاكرة."""

    text = read_root_table_bytes().decode("utf-8")
    roots: set[str] = set()
    for row in csv.DictReader(text.splitlines()):
        folded = fold_root(row["root_full"])
        if len(folded) == 3 and all(letter in _ARABIC_LETTERS for letter in folded):
            roots.add(folded)
    if not roots:
        raise WordSchemaError("لا جذورَ ثلاثيّةً في الجدول المُودَع.")
    return frozenset(roots)


@lru_cache(maxsize=1)
def corpus_words() -> tuple[str, ...]:
    """كلماتُ المدوَّنة المُودَعة بالقاعدة المكتوبة، متمايزةً ومرتَّبة."""

    text = read_root_table_bytes().decode("utf-8")
    words: set[str] = set()
    for row in csv.DictReader(text.splitlines()):
        body = _MARKS.sub("", row[CORPUS_RULE.column])
        for raw in re.split(r"[^؀-ۿ]+", body):
            folded = fold_root(raw)
            if not folded or any(ch not in _ARABIC_LETTERS for ch in folded):
                continue
            if (
                CORPUS_RULE.minimum_letters
                <= len(folded)
                <= CORPUS_RULE.maximum_letters
            ):
                words.add(folded)
    if not words:
        raise WordSchemaError("لا كلماتٍ في المدوَّنة بالقاعدة المكتوبة.")
    return tuple(sorted(words))


def candidate_roots(word: str) -> tuple[tuple[str, str], ...]:
    """الجذورُ المُودَعةُ التي تقبلها الكلمةُ متتالياتٍ جزئيّةً، مع باقي كلٍّ.

    والباقي هو «الزوائد» بنصّ الدعوى: ما بقي من الحروف بعد انتزاع الجذر.
    وتُرجَع أزواجٌ متمايزةٌ (جذر، باقٍ) فلا يُعَدُّ الجذرُ الواحدُ مرّتين.
    """

    roots = deposited_trilateral_roots()
    found: dict[tuple[str, str], None] = {}
    for positions in combinations(range(len(word)), 3):
        candidate = "".join(word[index] for index in positions)
        if candidate in roots:
            residue = "".join(
                letter for index, letter in enumerate(word) if index not in positions
            )
            found[(candidate, residue)] = None
    return tuple(found)


@dataclass(frozen=True, slots=True)
class DeterminationReading:
    """قراءةُ ت١: كم تحليلًا يقبل السطحُ."""

    words: int
    median_candidates: int
    mean_candidates: float
    words_with_one_or_none: int
    verdict: SchemaVerdict


@dataclass(frozen=True, slots=True)
class CoverageReading:
    """قراءةُ ت٢: كم كلمةً لا تقبل جذرًا مُودَعًا أصلًا."""

    words: int
    uncovered: int
    uncovered_share: float
    verdict: SchemaVerdict


@dataclass(frozen=True, slots=True)
class ResidueReading:
    """قراءةُ ت٣: كم من التحليلات المقبولة باقيها من «سألتمونيها»."""

    analyses: int
    legal_residue: int
    legal_share: float
    verdict: SchemaVerdict


@lru_cache(maxsize=1)
def _counts() -> tuple[tuple[int, ...], int]:
    counts: list[int] = []
    analyses = 0
    for word in corpus_words():
        found = candidate_roots(word)
        counts.append(len(found))
        analyses += len(found)
    return tuple(counts), analyses


def derive_determination() -> DeterminationReading:
    """هل يُعيِّن السطحُ تحليلًا واحدًا؟ (ت١)"""

    counts, _ = _counts()
    ordered = sorted(counts)
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) // 2
    )
    return DeterminationReading(
        words=len(counts),
        median_candidates=median,
        mean_candidates=sum(counts) / len(counts),
        words_with_one_or_none=sum(1 for value in counts if value <= 1),
        verdict=SchemaVerdict.SURVIVED if median <= 1 else SchemaVerdict.FALSIFIED,
    )


def derive_coverage() -> CoverageReading:
    """كم كلمةً لا يقبلها الجذرُ المُودَعُ متتاليةً جزئيّة؟ (ت٢)"""

    counts, _ = _counts()
    uncovered = sum(1 for value in counts if value == 0)
    share = uncovered / len(counts)
    return CoverageReading(
        words=len(counts),
        uncovered=uncovered,
        uncovered_share=share,
        verdict=SchemaVerdict.SURVIVED if share <= 0.05 else SchemaVerdict.FALSIFIED,
    )


def derive_residue_legality() -> ResidueReading:
    """كم من التحليلات المقبولة باقيها داخلَ «سألتمونيها»؟ (ت٣)"""

    legal = 0
    total = 0
    for word in corpus_words():
        for _root, residue in candidate_roots(word):
            total += 1
            if all(letter in AUGMENT_LETTERS for letter in residue):
                legal += 1
    if total == 0:
        return ResidueReading(0, 0, 0.0, SchemaVerdict.UNMEASURED)
    share = legal / total
    return ResidueReading(
        analyses=total,
        legal_residue=legal,
        legal_share=share,
        verdict=SchemaVerdict.SURVIVED if share >= 0.5 else SchemaVerdict.FALSIFIED,
    )


def read_verdicts() -> dict[str, SchemaVerdict]:
    """الأحكامُ الثلاثةُ مجموعةً، كلٌّ بشرطه المكتوب قبل النظر."""

    return {
        "ت١ التعيين": derive_determination().verdict,
        "ت٢ التغطية": derive_coverage().verdict,
        "ت٣ الحصر": derive_residue_legality().verdict,
    }


def corpus_digest() -> str:
    """بصمةُ المدوَّنة التي قِيس عليها، فلا يُنقَل رقمٌ بلا مصدره."""

    return root_table_digest()


A_FILE_THAT_NAMES_MARKS_ENTERS_THE_CORPUS_NOTE: Final[str] = (
    "AFileThatNamesMarksEntersTheCorpus: كتبتُ صنفَ العلامات بحروفه، فدخل هذا "
    "الملفُّ مجتمعَ قياس نثرِ الشجرة وأزاح زوجًا مُجمَّدًا كان يقوم على مشاهدةٍ "
    "واحدةٍ فصار على اثنتين؛ فأُعيدت كتابتُه بنقاط ترميزٍ لا بحروف — وذلك تصحيحُ "
    "تمثيلٍ لا تفاديًا للقياس، إذ صنفُ علاماتٍ في نصِّ برنامجٍ ليس نثرًا"
)

A_SCHEMA_THAT_ABSORBS_ITS_COUNTEREXAMPLES_SAYS_NOTHING_NOTE: Final[str] = (
    "ASchemaThatAbsorbsItsCounterexamplesSaysNothing: «جذرٌ اصطلاحيّ» يُدخِل كلَّ "
    "مخالفٍ في القانون، فيصير القانونُ غيرَ قابلٍ للإبطال؛ والمقيسُ ههنا كم "
    "يُخبر لا أصحيحٌ هو"
)

THE_TREE_ALREADY_WITHHELD_THIS_LAYER_NOTE: Final[str] = (
    "TheTreeAlreadyWithheldThisLayer: طبقةُ «المقطع والوزن» محجوزةٌ في التسجيل "
    "القبْليّ بمنزلة «فرضٌ مُعلَنُ العطب»، وشرطُ دخولها مكتوبٌ ولم يُستوفَ؛ "
    "فالدعوى هي الفرضُ نفسُه مختومًا ✅ قبل شرطه"
)

AN_AFFIX_SET_IS_WHAT_MAKES_THE_SCHEMA_SAY_ANYTHING_NOTE: Final[str] = (
    "AnAffixSetIsWhatMakesTheSchemaSayAnything: «زوائد» بلا حصرٍ تقبل كلَّ بقيّة، "
    "والعربيّةُ تحصرها بسألتمونيها؛ فإن كان أكثرُ المقبول ممتنعًا بالحصر فالمحتوى "
    "في الشرط المحذوف"
)

THE_AUGMENT_SET_IS_A_RECEIVED_CONVENTION_NOT_A_MEASURED_TABLE_NOTE: Final[str] = (
    "TheAugmentSetIsAReceivedConventionNotAMeasuredTable: «سألتمونيها» اصطلاحٌ "
    "مشهورٌ لا جدولٌ مُبصَّمٌ في هذه الشجرة، فقياسُ ت٣ يُقرأ بشرطه"
)

THIS_IS_A_TEST_NOT_A_VERDICT_ON_ARABIC_NOTE: Final[str] = (
    "ThisIsATestNotAVerdictOnArabic: المقيسُ سلوكُ صيغةٍ مقترَحةٍ على مدوَّنةٍ "
    "مُبصَّمة؛ وسقوطُها يُسقِط الصياغةَ لا الجذرَ ولا الوزن"
)

SCHEMA_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_FILE_THAT_NAMES_MARKS_ENTERS_THE_CORPUS_NOTE,
    A_SCHEMA_THAT_ABSORBS_ITS_COUNTEREXAMPLES_SAYS_NOTHING_NOTE,
    THE_TREE_ALREADY_WITHHELD_THIS_LAYER_NOTE,
    AN_AFFIX_SET_IS_WHAT_MAKES_THE_SCHEMA_SAY_ANYTHING_NOTE,
    THE_AUGMENT_SET_IS_A_RECEIVED_CONVENTION_NOT_A_MEASURED_TABLE_NOTE,
    THIS_IS_A_TEST_NOT_A_VERDICT_ON_ARABIC_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


# يُفحَص عند كلّ استيراد: شروطُ الإبطال ثلاثةٌ، ولكلٍّ عتبةٌ مكتوبة.
if len(WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA) != 3:  # pragma: no cover - حارس
    raise RuntimeError("شروطُ الإبطال ثلاثةٌ: التعيينُ والتغطيةُ والحصر.")
if len(SchemaVerdict) != 3:  # pragma: no cover - حارس
    raise RuntimeError("منازلُ الحكم ثلاثٌ مغلقةٌ؛ ولا «مؤيَّدٌ جزئيًّا» فيها.")
if len(AUGMENT_LETTERS) != 10:  # pragma: no cover - حارس
    raise RuntimeError("حروفُ «سألتمونيها» عشرةٌ متمايزة.")
