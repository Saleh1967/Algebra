"""توسيعُ العيّنة: الصدارةُ تثبت، والقاعُ يتبيّن أنّه ليس عربيّةً أصلًا.

طُلب أمران: أن تُوسَّع عيّنةُ `mark_pair_census`، وأن يُبحَث فيها عن **الأقلّ
تكرارًا**. وقد وُسِّعت، فأجاب التوسيعُ عن الأوّل إجابةً مؤكِّدة، وأجاب عن
الثاني إجابةً لم تكن متوقَّعة: **مزدوجا القاع ليسا من العربيّة في شيء**.

**أوّلًا: بأيّ شيءٍ وُسِّعت؟** لا ثالثَ للمُودَعَين في هذه الشجرة؛ فُتِّشت
فلم يُوجَد نصٌّ قرآنيٌّ مشكولٌ ثالث، وبايتاتُ المدوّنة غائبةٌ كما قُرِّر في
`THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED`. والباقي في
الشجرة عربيّةٌ كثيرة: **نثرُها هي**، أي ما في `src/alghanem/**/*.py` من شروحٍ
وبقايا مسمّاة. وهذه بايتاتٌ مُودَعةٌ حاضرةٌ يُعاد اشتقاقُ كلِّ رقمٍ منها عند
القراءة، فصلحت نطاقًا ثالثًا. ويُخرَج منها المُودَعان نفساهما ووحدةُ القياس
هذه، كيلا تُعَدَّ الدرجةُ الأولى مرّتين وكيلا تقيسَ الآلةُ نفسَها. **ولا يُدَّعى
أنّها شاهدٌ قرآنيٌّ ثانٍ، ولا أنّها خطٌّ ناسخٍ ثانٍ**: كاتبُها كاتبُ الشجرة،
وهي سجلٌّ هندسيٌّ لا مُصحَف
(`THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS`).

**وثانيًا: سُلَّمُ التوسيع، ثلاثُ درجات:**

| الدرجة | المزدوجات | المتحقّق | المتصدّر | القاع |
|---|---|---|---|---|
| الفاتحة | 16 | 3/36 | فتحة+شدّة (10) | فتحة+خنجريّة (2) |
| + الفتح ٢٩ | 32 | 4/36 | فتحة+شدّة (24) | ضمّة+شدّة (2) |
| + نثر الشجرة | 17,154 | 9/36 | فتحة+شدّة (7,522) | سكون+خنجريّة (1) |

فالتوسيعُ **536 ضعفًا** في عدد المزدوجات. وفيه جوابُ السؤالين معًا:

**المتصدّرُ لم يتزحزح في درجةٍ من الثلاث**، ولا نوزع في واحدةٍ منها، مع تغيُّر
السِّجلّ وتغيُّر الحجم مرتبتين ونصفًا. وهذا تثبيتٌ معتبَرٌ للصدارة.

**والقاعُ تزحزح في كلّ درجة**: ثلاثُ درجاتٍ ادّعت ثلاثةَ مزدوجاتٍ مختلفةٍ قاعًا.
فالقاعُ أقلُّ إحصاءات العيّنة ثباتًا، لأنّه يتحرّك بوقوعٍ واحد
(`THE_MINIMUM_MOVES_AT_EVERY_RUNG_WHILE_THE_MAXIMUM_NEVER_DOES`).

**وثالثًا: التوزيعُ ليس ذا ذيلٍ بل ذو جُرف.** المتحقّقُ تسعةٌ على النثر، ستّةٌ
منها `X + شدّة` وتحوز 17,142 من 17,154 — أي **99.930%** — وثلاثةٌ تحوز **12**
وقوعًا لا غير. وبين 951 و9 عاملُ 105. فليس بين الجسم والقاع تدرّجٌ يُقرأ منه
ترتيبٌ في الندرة.

**ورابعًا: وفُحصت الوقوعاتُ الاثنتا عشرةُ كلُّها واحدةً واحدة**، إذ لا يُنشَر
قاعٌ لم يُنظَر في مادّته:

- **فتحة + خنجريّة (9)**: عربيّةٌ صحيحة، كلُّها اقتباساتٌ قرآنيّةٌ فيها ألفٌ
  خنجريّة، في `fatiha_source_text` و`irab_case_readout`.
- **فتحة + ضمّة (2)**: **ليست عربيّة**؛ موضعٌ عليه حركتان، وهو في الموضعين
  شاهدٌ مضروبٌ عمدًا على الفساد: «سطح ``بَُ``» مقتبسًا في
  `carrier_state_candidate` و`state_evidence` ليُبيَّن أنّه لا يُخرِج حالة.
- **سكون + خنجريّة (1)**: **ليست عربيّة**؛ إنّها مخرَجُ مِرماز معيبٍ مقتبسًا
  في `gflk_codec_revision_audit` عند تدوين عيبه.

فالمزدوجُ الأقلُّ تكرارًا في العيّنة الموسَّعة، والذي يليه، **كلاهما أثرُ
الوسيط لا أثرُ اللغة**. والأقلُّ من العربيّ الصحيح هو فتحة+خنجريّة عند التسع،
وهو أعلى من القاع المُعلَن بتسعة أضعاف. فالقاعُ لا يقيس ندرةً في الخطّ، بل
**يقيس ما يقتبسه الوسيطُ من الفساد**
(`THE_FLOOR_MEASURES_WHAT_THE_MEDIUM_QUOTES_NOT_WHAT_THE_SCRIPT_ALLOWS`).

**وخامسًا: التوسيعُ غيّر المجتمعَ لا الحجمَ وحدَه.** المزدوجاتُ المبدوءةُ
بتنوينٍ: **صفرٌ** من 32 في المُودَعَين القرآنيَّين، و**4,498** من 17,122 في
النثر — أي 26.373%. فالنثرُ يُظهِر تركيباتِ تنوينٍ لم يُظهِرها النصّان ألبتّة.
فلا يُقال إنّ العيّنةَ الكبرى عيّنةٌ أكبرُ من الشيء نفسه
(`WIDENING_INTO_A_NEW_REGISTER_CHANGES_THE_POPULATION_NOT_ONLY_ITS_SIZE`).

**وسادسًا: نطاقُ النثر ينمو بنموّ الشجرة.** فأرقامُه مؤرَّخةٌ لا دائمة، وقد
جُمِّد عدَدُ ملفّاته وبايتاتِه وقتَ القياس، وتُكشَف الزحزحةُ بـ
`prose_scope_has_drifted` ولا تُخفى. والوحدةُ تُخرِج نفسَها من نطاقها كيلا
تقيسَ الآلةُ نفسَها
(`THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED`).

**وسابعًا: وكانت البصمةُ تحرس النطاقَ ولا تحرس الأرقام.** فلمّا أُعيد القياسُ
على البصمة المُجمَّدة نفسِها — 408 ملفًّا و7,588,660 بايتًا — خرج 16,796
مزدوجًا حيث كان المنقولُ 16,781. فالمنقولُ كان قد انفصل عن المقيس بلا أن يسقط
شاهد. فجُمِّدت أرقامُ الدرجة الثالثة في `THE_THIRD_RUNG_AT_MEASUREMENT`،
وتُقابَل بما يقيسه القرصُ في `third_rung_figures`. ويُقرَّر ههنا صريحًا أنّ
مجتمعَ هذا القياس مربوطٌ **ببنية المستودع** لا بمجالٍ لغويٍّ مستقلّ: كلُّ
ملفٍّ يُضاف يوسّعه. وهذا مذكورٌ لا مُصحَّحٌ، لأنّ الوحدةَ تقيس سِجلَّ النثر
بما هو، ولا تدّعي أنّه عيّنةٌ من العربيّة
(`THE_FINGERPRINT_GUARDED_THE_SCOPE_AND_NOT_THE_FIGURES_TRANSCRIBED`).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from functools import lru_cache
from pathlib import Path
from typing import Final

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.mark_pair_census import PairCensus, pair_census_over

FATHA: Final[str] = "\u064e"
DAMMA: Final[str] = "\u064f"
SHADDA: Final[str] = "\u0651"
SUKUN: Final[str] = "\u0652"
DAGGER: Final[str] = "\u0670"
THE_TANWIN: Final[tuple[str, ...]] = ("\u064b", "\u064c", "\u064d")


class PairWideningError(ValueError):
    """خطأُ توسيعِ عيّنةِ المزدوجات."""


@dataclass(frozen=True)
class TailOccurrence:
    """مزدوجٌ من القاع، وطبيعةُ مادّته منصوصةً لا مُجمَلة."""

    pair: tuple[str, str]
    occurrences: int
    is_arabic: bool
    provenance: str

    def __post_init__(self) -> None:
        if len(self.pair) != 2 or self.pair[0] == self.pair[1]:
            raise PairWideningError("المزدوجُ نقطتان متغايرتان لا غير.")
        if self.occurrences < 1:
            raise PairWideningError("لا يُسجَّل في القاع ما لم يقع.")
        if not self.provenance.strip():
            raise PairWideningError("لا يُنشَر قاعٌ بلا بيانِ مادّته.")

    @property
    def codepoints(self) -> tuple[str, str]:
        """نقطتا الترميز بصورتهما المعهودة."""

        return (f"U+{ord(self.pair[0]):04X}", f"U+{ord(self.pair[1]):04X}")


THE_TAIL_AUDITED: Final[tuple[TailOccurrence, ...]] = (
    TailOccurrence(
        pair=(FATHA, DAGGER),
        occurrences=9,
        is_arabic=True,
        provenance=(
            "اقتباساتٌ قرآنيّةٌ فيها ألفٌ خنجريّة، في fatiha_source_text "
            "و irab_case_readout؛ عربيّةٌ صحيحة."
        ),
    ),
    TailOccurrence(
        pair=(FATHA, DAMMA),
        occurrences=2,
        is_arabic=False,
        provenance=(
            "شاهدٌ مضروبٌ عمدًا على الفساد: «بَُ» موضعٌ عليه حركتان، مقتبسًا "
            "في carrier_state_candidate و state_evidence لبيان أنّه لا يُخرِج حالة."
        ),
    ),
    TailOccurrence(
        pair=(SUKUN, DAGGER),
        occurrences=1,
        is_arabic=False,
        provenance=(
            "مخرَجُ مِرمازٍ معيبٍ مقتبسًا في gflk_codec_revision_audit عند "
            "تدوين عيبه؛ ليست عربيّةً بحال."
        ),
    ),
)


@dataclass(frozen=True)
class ScopeFingerprint:
    """بصمةُ نطاقٍ مؤرَّخة: عددُ ملفّاته وبايتاتِه وقتَ القياس."""

    files: int
    text_bytes: int

    def __post_init__(self) -> None:
        if self.files < 1 or self.text_bytes < 1:
            raise PairWideningError("نطاقٌ خالٍ لا يُبصَم.")


PROSE_SCOPE_AT_MEASUREMENT: Final[ScopeFingerprint] = ScopeFingerprint(
    files=414,
    text_bytes=7731852,
)


@dataclass(frozen=True)
class RungFigures:
    """أرقامُ درجةٍ مؤرَّخةٌ كما نُقلت إلى النثر، ليُقابَل المنقولُ بالمقيس."""

    total_pairs: int
    realized: int
    shadda_bearing: int
    tanwin_initial_in_prose: int
    prose_pairs: int

    def __post_init__(self) -> None:
        if min(vars(self).values()) < 1:
            raise PairWideningError("رقمُ درجةٍ دون الواحد لا يُجمَّد.")


THE_THIRD_RUNG_AT_MEASUREMENT: Final[RungFigures] = RungFigures(
    total_pairs=17154,
    realized=9,
    shadda_bearing=17142,
    tanwin_initial_in_prose=4498,
    prose_pairs=17122,
)

THE_SCOPE_EXCLUSIONS: Final[frozenset[str]] = frozenset(
    {
        "pair_sample_widening.py",
        "fatiha_source_text.py",
        "fath_ayah_source_text.py",
    }
)


def _source_root() -> Path:
    return Path(__file__).resolve().parent.parent


def prose_scope_files() -> tuple[Path, ...]:
    """ملفّاتُ نثر الشجرة مرتَّبةً، والوحدةُ مُخرَجةٌ من نطاقها."""

    root = _source_root()
    return tuple(
        path
        for path in sorted(root.rglob("*.py"))
        if path.name not in THE_SCOPE_EXCLUSIONS and path.is_file()
    )


@lru_cache(maxsize=1)
def prose_scope_text() -> str:
    """نصُّ نثر الشجرة مقروءًا من بايتاته، ويُخزَن للجلسة لا للأبد.

    والخزنُ ههنا خزنُ أداءٍ لا خزنُ حكم: `prose_scope_fingerprint` تبقى
    مقروءةً من القرص في كلّ نداء، فتُكشَف الزحزحةُ وإن خُزِن النصّ.
    """

    return "\n".join(path.read_text(encoding="utf-8") for path in prose_scope_files())


def prose_scope_fingerprint() -> ScopeFingerprint:
    """بصمةُ النطاق الآن، تُقاس ولا تُفترَض."""

    paths = prose_scope_files()
    return ScopeFingerprint(
        files=len(paths),
        text_bytes=sum(len(path.read_bytes()) for path in paths),
    )


def prose_scope_has_drifted() -> bool:
    """أنَما النطاقُ عمّا قِيس عليه؟ وتُكشَف الزحزحةُ ولا تُخفى."""

    return prose_scope_fingerprint() != PROSE_SCOPE_AT_MEASUREMENT


@lru_cache(maxsize=1)
def the_widening_ladder() -> tuple[PairCensus, ...]:
    """درجاتُ التوسيع الثلاث، كلٌّ تراكميّةٌ على ما قبلها بلا تكرار."""

    fatiha = "\n".join(FATIHA_LINES)
    quranic = f"{fatiha}\n{FATH_AYAH_SOURCE_TEXT}"
    return (
        pair_census_over(fatiha, "الفاتحة"),
        pair_census_over(quranic, "الفاتحة + الفتح ٢٩"),
        pair_census_over(f"{quranic}\n{prose_scope_text()}", "وزيادةُ نثر الشجرة"),
    )


def the_leader_is_stable_across_the_ladder() -> bool:
    """أبقي المتصدّرُ نفسَه في الدرجات الثلاث، متفرِّدًا في كلٍّ منها؟"""

    leaders = []
    for census in the_widening_ladder():
        if not census.the_lead_is_uncontested:
            return False
        leaders.append(census.leaders[0].pair)
    return len(set(leaders)) == 1


def the_floor_moves_across_the_ladder() -> bool:
    """أتزحزح القاعُ بين الدرجات؟ فإن تزحزح فليس إحصاءً يُعوَّل عليه."""

    floors = [
        census.ranked[-1].pair for census in the_widening_ladder() if census.ranked
    ]
    return len(set(floors)) > 1


def tanwin_initial_pairs(census: PairCensus) -> int:
    """كم مزدوجًا مبدوءًا بتنوينٍ في تعدادٍ؟ وبه يُقاس فرقُ السِّجلّ."""

    tanwin = set(THE_TANWIN)
    return sum(count.occurrences for count in census.counts if count.pair[0] in tanwin)


def shadda_bearing_pairs(census: PairCensus) -> int:
    """كم مزدوجًا فيه شدّة؟ وبه يُقاس الجُرفُ بين الجسم والقاع."""

    return sum(count.occurrences for count in census.counts if SHADDA in count.pair)


def third_rung_figures() -> RungFigures:
    """أرقامُ الدرجة الثالثة الآن، تُقاس من القرص ولا تُنقَل عن النثر."""

    rung = the_widening_ladder()[2]
    prose = pair_census_over(prose_scope_text(), "نثر الشجرة وحدَه")
    return RungFigures(
        total_pairs=rung.total_pairs,
        realized=rung.realized,
        shadda_bearing=shadda_bearing_pairs(rung),
        tanwin_initial_in_prose=tanwin_initial_pairs(prose),
        prose_pairs=prose.total_pairs,
    )


def the_transcribed_figures_have_drifted() -> bool:
    """أزحزحت الأرقامُ المنقولةُ عمّا يقيسه القرصُ الآن؟ وتُكشَف ولا تُخفى."""

    return third_rung_figures() != THE_THIRD_RUNG_AT_MEASUREMENT


def the_least_frequent_arabic_pair() -> TailOccurrence:
    """أقلُّ المزدوجات وقوعًا **ممّا هو عربيٌّ صحيح**، لا أقلُّ الجميع."""

    arabic = [entry for entry in THE_TAIL_AUDITED if entry.is_arabic]
    if not arabic:
        raise PairWideningError("لا عربيَّ في القاع؛ وهذا خبرٌ لا يُبتلَع صمتًا.")
    return min(arabic, key=lambda entry: entry.occurrences)


def the_floor_is_not_arabic() -> bool:
    """أمزدوجُ القاعِ المُعلَنُ خارجٌ عن العربيّة؟"""

    floor = min(THE_TAIL_AUDITED, key=lambda entry: entry.occurrences)
    return not floor.is_arabic


THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS: Final[str] = (
    "THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS: نثرُ "
    "الشجرة بايتاتٌ مُودَعةٌ يُعاد اشتقاقُ أرقامها، لكنّه ليس شاهدًا قرآنيًّا "
    "ثانيًا ولا خطَّ ناسخٍ ثانيًا: كاتبُه كاتبُ الشجرة، ويدٌ واحدة. فدورُه "
    "اختبارُ ثباتِ الترتيب عند تغيُّر السِّجلّ، لا توسيعُ القياس القرآنيّ."
)

THE_MINIMUM_MOVES_AT_EVERY_RUNG_WHILE_THE_MAXIMUM_NEVER_DOES: Final[str] = (
    "THE_MINIMUM_MOVES_AT_EVERY_RUNG_WHILE_THE_MAXIMUM_NEVER_DOES: ادّعت "
    "الدرجاتُ الثلاثُ ثلاثةَ مزدوجاتٍ مختلفةٍ قاعًا، وأبقت متصدّرًا واحدًا. "
    "والقاعُ يتحرّك بوقوعٍ واحد، ووقوعٌ واحدٌ لا يُميَّز من العدم بالعيّنة؛ "
    "فلا يُثبَت ههنا مزدوجٌ أقلُّ تكرارًا، وإنّما يُحَدّ."
)

THE_FLOOR_MEASURES_WHAT_THE_MEDIUM_QUOTES_NOT_WHAT_THE_SCRIPT_ALLOWS: Final[str] = (
    "THE_FLOOR_MEASURES_WHAT_THE_MEDIUM_QUOTES_NOT_WHAT_THE_SCRIPT_ALLOWS: "
    "فُحصت وقوعاتُ القاع الاثنتا عشرةَ فكان أقلُّها مخرَجَ مِرمازٍ معيب، "
    "والذي يليه شاهدًا مضروبًا عمدًا على الفساد؛ وكلاهما ليس عربيّةً. فالقاعُ "
    "في هذه العيّنة أثرُ الوسيط لا أثرُ اللغة، ولا يُقرأ ندرةً في الخطّ."
)

WIDENING_INTO_A_NEW_REGISTER_CHANGES_THE_POPULATION_NOT_ONLY_ITS_SIZE: Final[str] = (
    "WIDENING_INTO_A_NEW_REGISTER_CHANGES_THE_POPULATION_NOT_ONLY_ITS_SIZE: "
    "المزدوجاتُ المبدوءةُ بتنوينٍ صفرٌ من 32 في المُودَعَين القرآنيَّين، "
    "و4,498 من 17,122 في النثر. فليست الكبرى عيّنةً أكبرَ من الشيء نفسه، "
    "وثباتُ الصدارةِ عبرَها ثباتٌ عبرَ سِجلَّين لا داخلَ سِجلٍّ واحد."
)

THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED: Final[str] = (
    "THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED: أرقامُ "
    "النثر مؤرَّخةٌ ببصمةٍ مُجمَّدةٍ لعدد الملفّات والبايتات، وكلُّ إضافةٍ "
    "إلى الشجرة تزحزحها. وشواهدُ الأرقام تسقط عند الزحزحة قصدًا ولا تُتخطّى، "
    "فإعادةُ التجميد قياسٌ يُعاد لا صيانةٌ تُجرى؛ وتبقى الأحكامُ البنيويّةُ "
    "— ثباتُ الصدارة وتزحزحُ القاع — قائمةً على أيّ نطاقٍ كان."
)

THE_FINGERPRINT_GUARDED_THE_SCOPE_AND_NOT_THE_FIGURES_TRANSCRIBED: Final[str] = (
    "THE_FINGERPRINT_GUARDED_THE_SCOPE_AND_NOT_THE_FIGURES_TRANSCRIBED: كانت "
    "البصمةُ تحرس عدد الملفّات والبايتات ولا تحرس الأرقامَ المنقولةَ إلى "
    "النثر، فانفصل المنقولُ عن المقيس على النطاق المُجمَّد نفسِه: قِيس 16,796 "
    "مزدوجًا حيث نُقِل 16,781. فجُمِّدت أرقامُ الدرجة الثالثة كذلك، وصارت "
    "زحزحتُها تُكشَف بـ`the_transcribed_figures_have_drifted`. وأصلُ الأمر "
    "أنّ مجتمعَ القياس ههنا مربوطٌ ببنية المستودع لا بمجالٍ لغويٍّ مستقلّ، "
    "فكلُّ ملفٍّ يُضاف يوسّعه؛ وهذا مذكورٌ لا مُصحَّحٌ، إذ الوحدةُ تقيس سِجلَّ "
    "النثر بما هو، ولا تدّعي أنّه عيّنةٌ من العربيّة."
)

PAIR_SAMPLE_WIDENING_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS": (
        THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS
    ),
    "THE_MINIMUM_MOVES_AT_EVERY_RUNG_WHILE_THE_MAXIMUM_NEVER_DOES": (
        THE_MINIMUM_MOVES_AT_EVERY_RUNG_WHILE_THE_MAXIMUM_NEVER_DOES
    ),
    "THE_FLOOR_MEASURES_WHAT_THE_MEDIUM_QUOTES_NOT_WHAT_THE_SCRIPT_ALLOWS": (
        THE_FLOOR_MEASURES_WHAT_THE_MEDIUM_QUOTES_NOT_WHAT_THE_SCRIPT_ALLOWS
    ),
    "WIDENING_INTO_A_NEW_REGISTER_CHANGES_THE_POPULATION_NOT_ONLY_ITS_SIZE": (
        WIDENING_INTO_A_NEW_REGISTER_CHANGES_THE_POPULATION_NOT_ONLY_ITS_SIZE
    ),
    "THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED": (
        THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED
    ),
    "THE_FINGERPRINT_GUARDED_THE_SCOPE_AND_NOT_THE_FIGURES_TRANSCRIBED": (
        THE_FINGERPRINT_GUARDED_THE_SCOPE_AND_NOT_THE_FIGURES_TRANSCRIBED
    ),
}

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في عدٍّ لا سلطةَ فيه."""

    for holder in (TailOccurrence, ScopeFingerprint, RungFigures):
        for declared in fields(holder):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise PairWideningError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى {holder.__name__}: "
                        f"{declared.name}؛ وهذا عدٌّ لا سلطةَ فيه."
                    )


def _assert_the_tail_is_ordered_and_audited() -> None:
    """حارسُ استيراد: القاعُ مرتَّبٌ نزولًا، وكلُّ وقوعٍ فيه مبيَّنُ المادّة."""

    counts = [entry.occurrences for entry in THE_TAIL_AUDITED]
    if counts != sorted(counts, reverse=True):
        raise PairWideningError("القاعُ المفحوصُ غيرُ مرتَّبٍ نزولًا.")
    for entry in THE_TAIL_AUDITED:
        for mark in entry.pair:
            if unicodedata.combining(mark) == 0:
                raise PairWideningError(
                    f"نقطةٌ غيرُ لاصقةٍ في مزدوج القاع: {entry.codepoints!r}."
                )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in PAIR_SAMPLE_WIDENING_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise PairWideningError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_tail_is_ordered_and_audited()
_assert_every_residual_is_named_by_its_key()
