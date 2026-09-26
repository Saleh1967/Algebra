"""شُغِّل ختمُ `62495099…`: **سبعٌ من عشرٍ — ودعوايَ الكبرى سقطت**.

`THE_PROPOSAL_WAS_MEASURED_AND_IT_FAILED`: غ٤ **سقط**. الحسابُ بعدد
التباديل **وقت الاختيار** صرف **ثلاثَ بتّاتٍ** كما صرفت الإنتروبيا
سواءً بسواء. **فالبتّةُ المفقودةُ لم تعد.**

`AND_THE_REASON_I_GAVE_FELL_WITH_IT`: وغ٥ **سقط**: أصغرُ كتلةٍ في السؤال
الأوّل **واحدةٌ** لا اثنتان. **فقسمةُ التباديل لم تتوازن**، وتعليلي بأنّ
فجوةَ ستيرلنغ تدفع إلى التوازن **ساقطٌ برقمه**.

`AND_THE_STRONGEST_RESULT_IS_THE_THIRD_FALL`: وغ٧ **سقط**، **وهو أنفعُ
الثلاثة**: عددُ الدرجات التي يفترق فيها سؤالُ المعيارين **صفر**.
**فالمعياران يتّفقان على كلّ سؤالٍ في المقامين**. يُبدِّل ستيرلنغ
**المقدارَ** — **٧٫٤٩٧٤١٣** بتًّا في مقام الحصر وحدَه — **ولا يُبدِّل
الاختيارَ ولا مرّةً**.

`AND_THE_IDENTITY_CLOSED_TO_THE_LAST_DIGIT`: وغ٣ صمد: فرقُ الكسبين ناقصَ
(Σ فجواتِ الكتل − فجوةُ الجذر) **٤٫٩٧٤e−١٤** — وهي خطوةُ العائم لا خلاف.
**فالفرقُ مُعيَّنٌ بالفجوات تمامًا**، كما كُتِب قبل النظر.

`AND_MY_DERIVED_CLAIM_HELD_WHERE_MY_GUESSED_ONE_FELL`: وغ٨ صمد:
مجموعُ الكسب بالتباديل **يفوق** مجموعَه بالإنتروبيا بـ**+٧٫٤٩٧٤١٣**.
**وهذه كانت مُشتَقّةً لا مظنونة** — من أنّ فجوةَ الجذر أصغرُ من مجموع
فجوات الكتل. **فما اشتُقّ صمد، وما ظُنّ سقط.**

`AND_THE_GREEDY_IS_STILL_THE_CULPRIT_NOT_THE_YARDSTICK`: **فالإسرافُ ليس
أثرَ المعيار**. السؤالُ الأوّلُ في مقام الحصر يقسم **١–٣** بالمعيارين،
فيلزم ثلاثةُ أسئلةٍ لبلوغ أربع كتل؛ ولو قُسِم **٢–٢** لكفى اثنان.
**والمعياران كلاهما يرى ١–٣ أربح الآن** — **وهذه هي قِصَرُ نظر الجشع، لا
حدُّ ستيرلنغ.**

`AND_THE_UNSEARCHED_SPACE_IS_NOW_A_NUMBER`: وقسماتُ أربع خاناتٍ إلى كتلتين
فأكثر **أربعَ عشرةَ قسمة** (`S(4,2)=٧` و`S(4,3)=٦` و`S(4,4)=١`)،
**والجشعُ يزور ثلاثًا**. **فدعوى «الجشعُ غيرُ مبرهَن» صارت عددًا لا قولًا.**

`AND_TWO_CONDITIONS_PASSED_ON_A_TRIVIAL_EDGE`: وغ٢ وغ٩ مرّا بطرفٍ
**تافه**: كلاهما يقع عند **كتلةٍ نقيّةٍ صنفُها واحد**، وثمناها صفران.
**فالمرورُ صحيحٌ والشهادةُ خاوية**، وما يشهد حقًّا **+١٫٨٧٣٥٨١** على أدنى
كتلةٍ غيرِ نقيّة.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_stirling_greedy_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal
from algebra.stirling import bell, subsets

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "stirling_greedy_run.log"
WITNESS = REPOSITORY / "deposits" / "stirling_greedy_witness.log"

STANDS = 662 + 35
BITS_HASR = 3
BITS_NUMBERS = 2
SMALLEST_FIRST_HASR = 1
DISAGREE = 0
SPREAD = 7.497413
IDENTITY = 4.974e-14
REAL_GAP = 1.873581


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**12)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def _spent() -> dict[tuple[str, str], tuple[int, int]]:
    """(المقام، المعيار) ⟶ (بتّاتٌ، أصغرُ كتلةٍ في السؤال الأوّل)."""

    found = re.findall(
        r"^  (\S+) بمعيار (\S+): بتّاتٌ (\d+) \| أوّلُ سؤالٍ أصغرُ كتلةٍ فيه (\d+)$",
        LOG.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    return {(one, two): (int(three), int(four)) for one, two, three, four in found}


def test_the_seal_was_deposited_before_anything_was_computed() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("62495099")
    assert int(_grab(r"— مجموعُ المقامين: (\d+)")) == STANDS
    assert _one("غ١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_proposal_did_not_bring_the_missing_bit_back() -> None:
    """غ٤ سقط: ثلاثُ بتّاتٍ بالتباديل كما بالإنتروبيا سواءً بسواء."""

    spent = _spent()
    assert spent[("الحصر", "تباديل")][0] == BITS_HASR
    assert spent[("الحصر", "إنتروبيا")][0] == BITS_HASR
    assert _one("غ٤").verdict(Fraction(BITS_HASR)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("غ٤").threshold == Fraction(2)  # type: ignore[attr-defined]


def test_the_reason_i_gave_fell_with_the_number() -> None:
    """غ٥ سقط: القسمةُ الأولى ١–٣ بالمعيارين — ولا توازنَ يدفع إليه ستيرلنغ."""

    spent = _spent()
    assert spent[("الحصر", "تباديل")][1] == SMALLEST_FIRST_HASR
    assert spent[("الحصر", "إنتروبيا")][1] == SMALLEST_FIRST_HASR
    assert _one("غ٥").verdict(Fraction(SMALLEST_FIRST_HASR)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert spent[("العدد", "تباديل")][1] == 2  # وفي العدد توازنٌ بالمعيارين


def test_the_two_yardsticks_never_disagreed_on_a_single_question() -> None:
    """غ٧ سقط — وهو أنفعُ الثلاثة: صفرُ درجةٍ يفترقان فيها."""

    (apart_text,) = re.findall(
        r"^  درجاتٌ يفترق فيها السؤالُ الأوّل: (\d+)$",
        LOG.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    apart = int(apart_text)
    assert apart == DISAGREE
    assert _one("غ٧").verdict(Fraction(apart)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    agreed = re.findall(
        r"أيتّفق المعياران على السؤال الأوّل؟ (\w+)", LOG.read_text("utf-8")
    )
    assert agreed == ["True", "True"]  # مقامان، والاتّفاقُ في كليهما
    assert _one("غ١٠").verdict(Fraction(1)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_identity_between_the_criteria_closed_exactly() -> None:
    """غ٣ صمد: فرقُ الكسبين مُعيَّنٌ بالفجوات إلى خطوة العائم."""

    astray = float(_grab(r"أقصى انحرافٍ عن الهويّة: (\S+)"))
    assert abs(astray - IDENTITY) < 1e-15
    assert _one("غ٣").verdict(_exact(astray)) is Verdict.MET  # type: ignore[attr-defined]
    assert astray < 1e-9


def test_the_derived_claim_held_where_the_guessed_one_fell() -> None:
    """غ٨ صمد: الكسبُ بالتباديل أوفر بـ+٧٫٤٩٧٤١٣ — وكانت مُشتَقّةً."""

    (spread_text,) = re.findall(
        r"مجموعُ الكسب في الحصر: تباديلُ \S+ \| إنتروبيا \S+ \| فرقٌ (\S+)",
        LOG.read_text(encoding="utf-8"),
    )
    spread = float(spread_text)
    assert abs(spread - SPREAD) < 5e-7
    assert _one("غ٨").verdict(_exact(spread)) is Verdict.MET  # type: ignore[attr-defined]
    assert spread > 0
    eighth = _one("غ٨")
    assert "دعوًى مُشتَقّةٌ لا مقيسة" in eighth.falsifies  # type: ignore[attr-defined]


def test_the_other_stand_was_not_broken_by_the_new_criterion() -> None:
    """غ٦ صمد: مقامُ العدد يبقى عند بتّتين بالمعيارين."""

    spent = _spent()
    assert spent[("العدد", "تباديل")][0] == BITS_NUMBERS
    assert spent[("العدد", "إنتروبيا")][0] == BITS_NUMBERS
    assert _one("غ٦").verdict(Fraction(BITS_NUMBERS)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_two_proven_bounds_passed_on_a_trivial_edge_and_it_is_said() -> None:
    """غ٢ وغ٩ مرّا عند كتلةٍ نقيّةٍ ثمناها صفران — والشهادةُ خاوية."""

    over = float(_grab(r"أقصى \(log₂ التباديل − n·H\): (\S+)"))
    gap = float(_grab(r"أدنى فجوةِ ستيرلنغ على الكتل: (\S+)"))
    assert _one("غ٢").verdict(_exact(over)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("غ٩").verdict(_exact(gap)) is Verdict.MET  # type: ignore[attr-defined]
    assert over == 0.0 and gap == 0.0  # طرفان تافهان
    real = float(_grab(r"وأدناها على كتلةٍ غيرِ نقيّة: (\S+)"))
    assert abs(real - REAL_GAP) < 5e-7 and real > 0
    assert "كتلةٍ نقيّةٍ صنفُها واحد" in LOG.read_text(encoding="utf-8")


def test_the_unsearched_space_is_counted_by_the_second_kind() -> None:
    """قسماتُ أربعٍ أربعَ عشرةَ، والجشعُ يزور ثلاثًا — عددٌ لا قول."""

    rows_space = re.findall(
        r"قسماتُ (\d+) خاناتٍ \(بِلّ ناقصَ الواحدة\): (\d+) \| وزارها الجشعُ (\d+)",
        LOG.read_text("utf-8"),
    )
    assert len(rows_space) == 2 and len(set(rows_space)) == 1  # المقامان سواء
    space, visited, walked = rows_space[0]
    assert (int(space), int(visited)) == (4, 14)
    assert int(visited) == bell(4) - 1
    rows = {
        int(one): int(two)
        for one, two in re.findall(
            r"إلى (\d+) كتلًا: S\(4,\d\) = (\d+)", LOG.read_text("utf-8")
        )
    }
    assert rows == {2: subsets(4, 2), 3: subsets(4, 3), 4: subsets(4, 4)}
    assert rows == {2: 7, 3: 6, 4: 1}
    assert int(walked) == 3


def test_the_added_witnesses_changed_no_sealed_number() -> None:
    """الشاهدان المُضافان لم يُبدّلا رقمًا — والسجلّان مُقابَلان سطرًا بسطر."""

    text = WITNESS.read_text(encoding="utf-8")
    assert "لا فرقَ ألبتّة — صفرُ أسطرٍ مختلفة." in text
    assert "قسماتُ ستيرلنغ" in text and "الطرفُ غيرُ التافه" in text


def test_seven_of_ten_stood_and_the_three_that_fell_are_named() -> None:
    """الحصادُ يُعَدّ ولا يُدَّعى: سبعٌ صمدت وثلاثٌ سقطت."""

    fell = {"غ٤", "غ٥", "غ٧"}
    stood = {one.identifier for one in PREDICTIONS} - fell
    assert len(stood) == 7 and len(fell) == 3
    assert __doc__ is not None
    assert "سبعٌ من عشرٍ — ودعوايَ الكبرى سقطت" in __doc__
    assert "قِصَرُ نظر الجشع، لا حدُّ ستيرلنغ" in " ".join(__doc__.split())


FELL_WITH_THEM: dict[str, str] = {
    "غ٤": "دعوايَ أنّ المعيارَ هو العطل: أنّ الحسابَ بالتباديل",
    "غ٥": "دعوايَ أنّ التباديلَ تدفع إلى قسمةٍ **متوازنة**",
    "غ٧": "دعوايَ أنّ المعيارين **يرتّبان الأسئلةَ ترتيبين**",
}
"""ما عُلِّق على سقوط كلِّ شرطٍ، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره."""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10
    assert "وهو أنفعُ من تصديق دعوايَ" in _one("غ٤").falsifies  # type: ignore[attr-defined]


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("غ٢", "غ٩")
"""غ٢ وغ٩ **مرّا بطرفين تافهين**، وشهادتُهما خاوية.

كلاهما يقع عند **كتلةٍ نقيّةٍ صنفُها واحد**: ثمنُها بالإنتروبيا صفرٌ
وبالتباديل صفر، **فالفرقُ صفرٌ بالضرورة لا بالقياس**. وما يشهد للمبرهنة
حقًّا **+١٫٨٧٣٥٨١** على أدنى كتلةٍ غيرِ نقيّة — **وهو مقيسٌ ومطبوعٌ
ولكنّه ليس ما نصَّ عليه الشرطان**.
"""
