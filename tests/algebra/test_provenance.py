"""ختمُ النسبة مُشغَّلًا: رقمان لا يُطرَح أحدُهما من الآخر، والآلةُ هي الرادّة.

**ما يُفحَص ههنا**: أنّ الامتناعَ عن نقل رقمٍ إلى مدوّنةٍ أخرى صار **قيدَ
إنشاءٍ في الشيفرة** لا انضباطًا في النثر. فقد كُتِب في `test_mizan_pans` أنّ
«١٫٣٤× و٤٫٦× مقياسان لا مقياس» — وكان ذلك حكمًا يُقرَأ ويُنسى. وههنا تردُّه
`Reading.against` بعطلٍ مُسمًّى، فيسقط الاختبارُ إن نُقِل.

`THE_REFUSAL_IS_OVER_THE_STATISTIC_NOT_THE_CORPUS`: وموضعُ الردِّ يُسمَّى
بدقّة. فالرقمان مختلفا **المقياس** قبل أن يكونا مختلفَي المدوّنة: أحدُهما
تركيزُ حملٍ وظيفيٍّ في تمييز الأنواع، والآخرُ وسيطُ نصيبٍ صرفيٍّ في الوقوعات.
ولو قِيسا على مدوّنةٍ واحدةٍ لرُدَّا كما هما — وذلك مفحوصٌ أدناه بخانةٍ
ثالثة. فوصفُهما «مقارنةً بين مدوّنتين» **يُقدِّم العارضَ على العلّة**.

`A_DIFFERENT_CORPUS_IS_A_DECLARATION_NOT_A_REFUSAL`: وأمّا اتّحادُ المقياس
والوحدة مع اختلاف المدوّنة فمفتوحٌ بنصّه: يُحسَب الفرقُ ويُكتَب معه أنّه
**عبر مدوّنتين**، فيُقرَأ خبرًا عنهما لا عن العربيّة. والنقلُ المحرَّمُ إنّما
هو الصامت.

`NO_CORPUS_BYTES_LIVE_HERE_SO_EVERY_DIGEST_BELOW_IS_A_STAND_IN`: ولا مدوّنةَ
في هذه الشجرة: بصماتُ ما دون مشتقّةٌ من **أسماءٍ مكتوبةٍ ههنا**، لا من
بايتاتٍ مودَعة. وذلك مُعلَنٌ ومفحوصٌ — إذ لو مرّ اسمٌ في موضع البصمة لصار
الختمُ زينةً. فالمفحوصُ آلةُ الختم، والبصمةُ الحقيقيّةُ تُملأ يوم تُودَع
المدوّنة.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from pathlib import Path

import pytest

from algebra.provenance import (
    PROVENANCE_NAMED_RESIDUALS,
    Corpus,
    ProvenanceError,
    Reading,
)

REPOSITORY = Path(__file__).resolve().parents[2]


def _stand_in_digest(label: str) -> str:
    """بصمةُ **اسمٍ** لا بصمةُ مدوّنة؛ وتسميتُها ههنا شرطُ صدقِ الختم."""

    return hashlib.sha256(label.encode("utf-8")).hexdigest()


MUSHAF = Corpus(
    name="المصحف — الرسمُ المشكول",
    digest=_stand_in_digest("نائبٌ عن المصحف؛ لا بايتاتِ مدوّنةٍ ههنا"),
    size=18_992,
    size_unit="نوعٌ مشكول",
)

PROSE = Corpus(
    name="نثرٌ حديثٌ لمؤلّفٍ واحد",
    digest=_stand_in_digest("نائبٌ عن مدوّنة النثر؛ لا بايتاتِ مدوّنةٍ ههنا"),
    size=236_994,
    size_unit="كلمة",
)

# الرقمان المتنازَعان، كلٌّ بمقياسه ووحدته ومدوّنته
FUNCTIONAL = Reading(
    value=Fraction("4.6"),
    statistic="تركيزُ الحمل الوظيفيّ في حروف الزوائد",
    unit="النوعُ المشكول",
    corpus=MUSHAF,
)

MORPHOLOGICAL_PROXY = Reading(
    value=Fraction("1.34"),
    statistic="وسيطُ نصيب الأدوات الصرفيّة",
    unit="الوقوع",
    corpus=PROSE,
)


def test_the_worked_case_is_refused_and_the_refusal_names_the_statistic() -> None:
    """٤٫٦× و١٫٣٤× يُرَدّان، ويُسمّي الردُّ المقياسين لا المدوّنتين."""

    assert not FUNCTIONAL.comparable_with(MORPHOLOGICAL_PROXY)
    with pytest.raises(ProvenanceError) as raised:
        FUNCTIONAL.against(MORPHOLOGICAL_PROXY)

    said = str(raised.value)
    assert FUNCTIONAL.statistic in said
    assert MORPHOLOGICAL_PROXY.statistic in said
    assert MUSHAF.name not in said and PROSE.name not in said


def test_one_corpus_does_not_rescue_two_statistics() -> None:
    """ولو قِيسا على المصحف وحدَه لرُدّا: العلّةُ المقياسُ لا المدوّنة.

    وهذه الخانةُ الثالثةُ هي ما يفصل الدعوى: إن بقي الردُّ بعد توحيد
    المدوّنة فليس اختلافُها هو السبب.
    """

    proxy_here = Reading(
        value=MORPHOLOGICAL_PROXY.value,
        statistic=MORPHOLOGICAL_PROXY.statistic,
        unit=MORPHOLOGICAL_PROXY.unit,
        corpus=MUSHAF,
    )
    assert proxy_here.corpus == FUNCTIONAL.corpus
    with pytest.raises(ProvenanceError):
        FUNCTIONAL.against(proxy_here)

    # والنسبةُ ٣٫٤٣× التي يعطيها الطرحُ الساذجُ لا تُبلَغ أصلًا من هذا الباب
    assert round(float(FUNCTIONAL.value / MORPHOLOGICAL_PROXY.value), 2) == 3.43


def test_one_statistic_across_two_corpora_is_permitted_and_declared() -> None:
    """اتّحادُ المقياس والوحدة يفتح المقارنةَ، والاختلافُ يُكتَب لا يُكتَم."""

    here = Reading(
        value=Fraction("4.6"),
        statistic="تركيزُ الحمل الوظيفيّ في حروف الزوائد",
        unit="النوعُ المشكول",
        corpus=MUSHAF,
    )
    there = Reading(
        value=Fraction("2.1"),
        statistic="تركيزُ الحمل الوظيفيّ في حروف الزوائد",
        unit="النوعُ المشكول",
        corpus=PROSE,
    )

    gap, note = here.against(there)
    assert gap == Fraction("2.5")
    assert "عبر مدوّنتين" in note
    assert MUSHAF.name in note and PROSE.name in note

    back, _ = there.against(here)
    assert back == -gap


def test_within_one_corpus_the_note_says_so_and_names_it() -> None:
    """وفي المدوّنة الواحدة يُكتَب اسمُها كذلك — فلا رقمَ بلا نسبة."""

    first = Reading(
        value=Fraction(1, 2),
        statistic="نصيبُ الخانات الخالية",
        unit="خانة",
        corpus=MUSHAF,
    )
    second = Reading(
        value=Fraction(1, 4),
        statistic="نصيبُ الخانات الخالية",
        unit="خانة",
        corpus=MUSHAF,
    )

    gap, note = first.against(second)
    assert gap == Fraction(1, 4)
    assert "مدوّنةٌ واحدة" in note
    assert MUSHAF.name in note


def test_the_unit_is_a_construction_field_not_a_footnote() -> None:
    """مقياسٌ واحدٌ بوحدتين يُرَدّ: النوعُ ليس الوقوعَ وإن اتّحد الاسم."""

    by_type = Reading(
        value=Fraction("54.4"),
        statistic="نصيبُ حروف الزوائد",
        unit="النوعُ المشكول",
        corpus=MUSHAF,
    )
    by_token = Reading(
        value=Fraction("54.4"),
        statistic="نصيبُ حروف الزوائد",
        unit="الوقوع",
        corpus=MUSHAF,
    )

    assert not by_type.comparable_with(by_token)
    with pytest.raises(ProvenanceError) as raised:
        by_type.against(by_token)
    assert "وحدتان لا وحدة" in str(raised.value)


def test_a_reading_without_a_statistic_or_a_unit_is_not_constructible() -> None:
    """قيمةٌ بلا مقياسٍ أو بلا وحدةٍ لا تُبنى أصلًا — والفراغُ ليس وحدة."""

    for statistic, unit in (("", "النوع"), ("نصيب", ""), ("  ", "النوع")):
        with pytest.raises(ProvenanceError):
            Reading(value=Fraction(1, 2), statistic=statistic, unit=unit, corpus=MUSHAF)


def test_a_corpus_without_a_full_digest_is_not_constructible() -> None:
    """المدوّنةُ اسمٌ وبصمةٌ وحجمٌ بوحدة؛ وناقصُ واحدٍ منها ليس ختمًا."""

    good = _stand_in_digest("مدوّنةٌ للفحص")
    for digest in (good[:63], good + "0", good[:-1] + "z", ""):
        with pytest.raises(ProvenanceError):
            Corpus(name="مدوّنة", digest=digest, size=1, size_unit="كلمة")

    with pytest.raises(ProvenanceError):
        Corpus(name=" ", digest=good, size=1, size_unit="كلمة")
    with pytest.raises(ProvenanceError):
        Corpus(name="مدوّنة", digest=good, size=1, size_unit="")
    for size in (0, -1):
        with pytest.raises(ProvenanceError):
            Corpus(name="مدوّنة", digest=good, size=size, size_unit="كلمة")


def test_the_stamp_prints_the_three_fields_with_the_number() -> None:
    """الختمُ سطرٌ يحمل المقياسَ والوحدةَ والمدوّنةَ ببصمتها — لا حاشية."""

    stamp = FUNCTIONAL.stamp
    assert FUNCTIONAL.statistic in stamp
    assert FUNCTIONAL.unit in stamp
    assert MUSHAF.name in stamp
    assert MUSHAF.digest[:8] in stamp
    assert stamp != MORPHOLOGICAL_PROXY.stamp


def test_no_corpus_bytes_are_deposited_so_the_digests_are_stand_ins() -> None:
    """بصماتُ هذا الملفّ مشتقّةٌ من أسماء، ولا تطابق بايتاتِ ملفٍّ مودَع.

    وليس هذا تجميلًا: لو طابقت بصمةُ نائبٍ ملفًّا في الشجرة لصار الختمُ
    يدّعي نسبةً لم تُقَس. فيُفحَص النفيُ على كلّ ملفٍّ مودَعٍ في `corpora`.
    """

    stand_ins = {MUSHAF.digest, PROSE.digest}
    holders = [
        *(one for one in (REPOSITORY / "corpora").rglob("*") if one.is_file()),
        # وأُودِعت بايتاتُ المصحف في جذر الشجرة أيضًا، فيُفحَص النفيُ عليها
        *(one for one in REPOSITORY.glob("*.txt") if one.is_file()),
    ]
    deposited = {hashlib.sha256(one.read_bytes()).hexdigest() for one in holders}
    assert not (stand_ins & deposited)
    assert MUSHAF.digest != PROSE.digest


def test_the_named_residuals_are_three_and_distinct() -> None:
    """ثلاثةُ بواقٍ مُسمّاة، ولا اسمَ يتكرّر."""

    assert len(PROVENANCE_NAMED_RESIDUALS) == 3
    assert len(set(PROVENANCE_NAMED_RESIDUALS)) == 3
    joined = " ".join(PROVENANCE_NAMED_RESIDUALS)
    assert "ANumberWithoutItsCorpusIsARumour" in joined
    assert "ADifferentCorpusIsADeclarationNotARefusal" in joined
    assert "TheUnitIsPartOfTheStatisticNotAFootnote" in joined
