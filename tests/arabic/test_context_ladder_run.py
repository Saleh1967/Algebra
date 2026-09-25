"""شُغِّل ختمُ `d568a91d…`: **إحدى عشرةَ من اثنتي عشرة — والساقطةُ هي الخبر**.

`THE_FIRST_BIT_THE_CORPUS_PAYS_FOR_IS_NOT_THE_NEIGHBOUR`: ق٥ **سقط**.
قدّرتُ أنّ أوّلَ سؤالٍ يربح يسأل عن **حال السابق**، والجشعُ اختار
**«أآخرُ السطر؟»** — بتّةَ الموضع لا بتّةَ الجار. وربحُها المحجوز
**+٠٫٠٥٦٩**، وهو **الأكبرُ في السلّم كلِّه**.

`AND_IT_AGREES_WITH_A_SEAL_THAT_DID_NOT_KNOW_OF_IT`: وقد قِيس في
`26ae5b5b…` أنّ `I(الحال ؛ الموضع)` = **٠٫٠٥٦٥٢٩**. **وهذا الختمُ لم
يقرأ ذاك**، وإنّما بحث في سبعةٍ وخمسين سؤالًا فاختار هذا بربحٍ
**٠٫٠٥٦٩**. **فالرقمان يتلاقيان من طريقين**، والتلاقي **شاهدٌ لا صدفة**.

`AND_MY_FALSIFICATION_CLAUSE_HAD_NAMED_THIS_VERY_OUTCOME`: ونصُّ سقوط ق٥
مكتوبٌ فيه **قبل النظر**: «فقد تسبق بتّةُ الموضع بتّةَ الحال». **فالسقوطُ
وقع في الموضع الذي عُيِّن له**، ويُنشَر كذلك.

`THE_LADDER_FAR_EXCEEDS_FIRST_ORDER_MARKOV_ON_THE_STATE`: ومجموعُ الكسب
المحجوز **+٠٫٢١١٩٦٣** بتًّا، والجارُ **كلُّه** يحمل **٠٫٠٦٥٣**.
فالتصعيدُ بتّةً بتّة على سياقٍ أوسعَ **يبلغ ثلاثةَ أضعافٍ ورُبعًا** ما
تبلغه سلسلةُ ماركوف على الحال وحدَه.

`AND_THE_GAIN_IS_SPREAD_NOT_PILED`: ق٨ صمد **على حدّه بالكاد**: نصيبُ
الدرجة الأولى **٠٫٢٦٨٤** والحدُّ ٠٫٢٥. **فالبتّةُ الأولى تأخذ رُبعًا
وأكثرَ قليلًا**، والثلاثةُ أرباعٍ الباقيةُ موزّعةٌ على إحدى عشرةَ درجة.

`AND_THE_PAST_LETTER_DOES_CARRY_ACROSS`: ق١٠ صمد: خمسةُ أسئلةٍ من اثني
عشرَ عن **حرف خاتمة السابق**. فخبرُ الحرف **لا يقف عند موضعه** بل يمتدّ
إلى جاره — وهو غيرُ ما قِيس في `494465d1…` من خبر الحرف **عن حاله هو**.

`AND_NOTHING_WAS_LEAKED`: ق١٢ صمد. لا اسمَ بابٍ ولا اسمَ علامةٍ ولا اسمَ
يونيكود فوق سطر الإعلان — **والمحرفُ شريحةٌ ونقطةُ ترميز**. ولا قائمةَ
مُودَعةٌ ولا صورةٌ منقولةٌ عن نصٍّ خارجيّ: **الأسئلةُ السبعةُ والخمسون
قيمُها مجموعةٌ من المجمَّد**.

`AND_THE_LADDER_DID_NOT_STOP_BY_ITSELF`: وق٦ صمد (اثنتا عشرةَ درجةٍ
والحدُّ ثمانٍ) **لكنّ الوقوفَ لم يقع**: بلغ السلّمُ **السقفَ الذي أعلنتُه
أنا** لا سقفَ المادّة، **وكلُّ درجةٍ من الاثنتي عشرةَ ربحت محجوزًا**.
**فحدُّ ما تحمله المادّةُ لم يُبلَغ**، ويُسجَّل دَينًا لا نتيجة.

`AND_THE_GREEDY_IS_STILL_UNPROVEN`: **وما بُلِغ حدٌّ أدنى**: أفضلُ سؤالٍ
عند درجةٍ ليس أفضلَ سلّمٍ في النهاية. **ولا يُقال «لا يُبلَغ أكثر»** بل
**«لم يُبلَغ بهذا الجشع»**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_context_ladder_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "context_ladder_run.log"
VERSE_END = REPOSITORY / "deposits" / "verse_ending_run.log"
NEIGHBOUR_LOG = REPOSITORY / "deposits" / "arabic_token_run.log"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
BOXES = 8
FIELD = 2.6106
QUESTIONS = 57
DEPTHS = 12
FIRST_GAIN = 0.0569
WHOLE_OUT = 0.211963
WHOLE_IN = 0.227508
FIRST_SHARE = 0.2684
LOWEST_IN = 0.008087
APART = 0.000258
BLOCKS = 105
SLACK = -29.785261
FORBIDDEN = (
    "ARABIC",
    "فتحة",
    "ضمّة",
    "كسرة",
    "سكون",
    "تنوين",
    "شدّة",
    "فاعل",
    "مبتدأ",
    "إعراب",
    "مرفوع",
    "منصوب",
    "مجرور",
    "أمر",
    "نهي",
)
DECLARATION = "— ما لا يدخل هذا السجلّ"


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def _rungs() -> list[tuple[str, float, float, float, float, int]]:
    """(السؤال، ملحَقة، محجوزة، ربحٌ ملحَق، ربحٌ محجوز، كتل) لكلّ درجة."""

    found = re.findall(
        r"— د\d+ «(.+?)»: ملحَقة ([\d.]+) \| محجوزة ([\d.]+) "
        r"\| ربحٌ ملحَقٌ (\S+) \| ربحٌ محجوزٌ (\S+) \| كتلٌ (\d+)",
        LOG.read_text(encoding="utf-8"),
    )
    return [
        (one, float(two), float(three), float(four), float(five), int(six))
        for one, two, three, four, five, six in found
    ]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("d568a91d")


def test_the_machine_conditions_hold_under_the_corrected_token_bound() -> None:
    """ق١ وق٢: الأسطرُ ٦٬٢٣٦ والألفاظُ ٧٨٬٢٤٥ — ولا يُعاد العطل ٢٣."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    both = re.findall(
        r"— الألفاظ: (\d+) \| وعبرَ العدّادات (\d+)", LOG.read_text("utf-8")
    )
    assert both == [(str(TOKENS), str(TOKENS))]
    assert _one("ق١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ق٢").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert "المُصحَّح من 494465d1…" in LOG.read_text(encoding="utf-8")
    boxes, field = re.findall(
        r"— خاناتُ الحال: (\d+) \| H = ([\d.]+)", LOG.read_text("utf-8")
    )[0]
    assert int(boxes) == BOXES and abs(float(field) - FIELD) < 5e-5


def test_the_two_proven_bounds_hold_at_every_rung() -> None:
    """ق٣ وق٤: التنقيحُ لا يرفع الملحَقة، والتباديلُ دون N·H بعد ألف."""

    lowest = float(_grab(r"أدنى ربحٍ ملحَق: (\S+)"))
    slack = float(_grab(r"أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)"))
    assert _one("ق٣").verdict(_exact(lowest)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ق٤").verdict(_exact(slack)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(lowest - LOWEST_IN) < 5e-7 and lowest > 0
    assert abs(slack - SLACK) < 5e-7
    rungs = _rungs()
    assert len(rungs) == DEPTHS
    assert all(one[3] > 0 for one in rungs)  # وكلُّ درجةٍ تنقيحٌ يُنزِل الملحَقة
    inside = [one[1] for one in rungs]
    assert inside == sorted(inside, reverse=True)


def test_the_first_bit_is_positional_and_my_forecast_fell() -> None:
    """ق٥ سقط: الجشعُ اختار «أآخرُ السطر؟» لا سؤالًا عن حال السابق."""

    rungs = _rungs()
    first = rungs[0]
    assert first[0] == "آخرُ السطر"
    assert _one("ق٥").verdict(Fraction(0)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert abs(first[4] - FIRST_GAIN) < 5e-5
    assert first[4] == max(one[4] for one in rungs)  # وهي الأكبرُ في السلّم
    assert first[5] == 2  # سؤالٌ واحدٌ يقسم إلى كتلتين


def test_the_positional_gain_agrees_with_a_seal_that_did_not_know_of_it() -> None:
    """٠٫٠٥٦٩ ههنا و٠٫٠٥٦٥٢٩ في `26ae5b5b…` — من طريقين لا من نقل."""

    mine = _rungs()[0][4]
    theirs = float(_grab(r"I\(الحال ; الموضع\) = ([\d.]+)", VERSE_END))
    assert abs(theirs - 0.056529) < 5e-7
    assert abs(mine - theirs) < 5e-4
    assert LOG.read_text(encoding="utf-8").count("26ae5b5b") == 0  # لم يُقرَأ ذاك


def test_the_ladder_beats_first_order_markov_on_the_state_alone() -> None:
    """ق٧: ٠٫٢١١٩٦٣ مقابلَ ٠٫٠٦٥٣ للجار كلِّه — ثلاثةُ أضعافٍ ورُبع."""

    whole = float(_grab(r"مجموعُ الكسب المحجوز: (\S+)"))
    inside = float(_grab(r"مجموعُ الكسب الملحَق: (\S+)"))
    assert abs(whole - WHOLE_OUT) < 5e-7 and abs(inside - WHOLE_IN) < 5e-7
    assert _one("ق٧").verdict(_exact(whole)) is Verdict.MET  # type: ignore[attr-defined]
    neighbour = float(_grab(r"\n  I = ([\d.]+)", NEIGHBOUR_LOG))
    assert abs(neighbour - 0.0653) < 5e-5
    assert abs(whole / neighbour - 3.246) < 5e-3
    assert inside > whole  # والملحَقُ يربح أكثرَ دائمًا، وذاك الانتحال


def test_the_gain_is_spread_and_the_eighth_passed_on_its_edge() -> None:
    """ق٨: نصيبُ الأولى ٠٫٢٦٨٤ والحدُّ ٠٫٢٥ — مرورٌ قريبٌ من الحدّ."""

    share = float(_grab(r"نصيبُ الدرجة الأولى من الكسب المحجوز: ([\d.]+)"))
    assert abs(share - FIRST_SHARE) < 5e-5
    assert _one("ق٨").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert share - 0.25 < 0.02  # ومرورُه على الحدّ بفارقٍ دون جزأين من مئة
    rungs = _rungs()
    assert sum(one[4] for one in rungs[1:]) > 2 * rungs[0][4]


def test_the_past_letter_carries_across_to_its_neighbour() -> None:
    """ق١٠: خمسةُ أسئلةٍ من اثني عشرَ عن حرف خاتمة السابق."""

    tally = {
        one: int(two)
        for one, two in re.findall(
            r"  أسئلةُ «(.+?)»: (\d+)", LOG.read_text(encoding="utf-8")
        )
    }
    assert sum(tally.values()) == DEPTHS
    letters = tally["حرفُ خاتمةِ السابق"]
    assert letters == 5
    assert _one("ق١٠").verdict(Fraction(letters)) is Verdict.MET  # type: ignore[attr-defined]
    assert tally["حالُ السابق"] == 5
    assert tally["آخرُ السطر"] == 1 and tally["حالُ ما قبله"] == 1
    assert "أوّلُ السطر" not in tally  # ولم يُختَر سؤالُ صدر السطر ألبتّة


def test_the_hold_out_never_sits_below_the_in_sample_estimate() -> None:
    """ق٩: أدنى (محجوزة − ملحَقة) موجب — والاتّجاهُ كما يقتضي الانتحال."""

    apart = float(_grab(r"أدنى \(محجوزة − ملحَقة\): (\S+)"))
    assert abs(apart - APART) < 5e-7
    assert _one("ق٩").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    rungs = _rungs()
    assert all(one[2] >= one[1] for one in rungs)


def test_each_rung_splits_and_the_last_carries_many_blocks() -> None:
    """ق١١: مئةٌ وخمسُ كتلٍ عند الثانيةَ عشرة، وكلُّ درجةٍ تقسم."""

    rungs = _rungs()
    blocks = [one[5] for one in rungs]
    assert blocks[-1] == BLOCKS
    assert _one("ق١١").verdict(Fraction(BLOCKS)) is Verdict.MET  # type: ignore[attr-defined]
    assert blocks == sorted(blocks)
    assert all(
        two <= 2 * one for one, two in zip(blocks, blocks[1:])
    )  # سؤالٌ واحدٌ يُضاعِف على الأكثر
    assert int(_grab(r"كتلُ آخر درجة: (\d+)")) == BLOCKS


def test_no_name_from_outside_the_corpus_entered_the_log() -> None:
    """ق١٢: لا اسمَ بابٍ ولا علامةٍ ولا يونيكود فوق سطر الإعلان."""

    text = LOG.read_text(encoding="utf-8")
    assert DECLARATION in text
    measured = text.split(DECLARATION)[0]
    leaked = [one for one in FORBIDDEN if one in measured]
    assert not leaked, leaked
    assert _one("ق١٢").verdict(Fraction(len(leaked))) is Verdict.MET  # type: ignore[attr-defined]
    latin = set(re.findall(r"[A-Za-z]", measured))
    assert latin <= set("UNHABCDEFabcdeflog")  # ترميزٌ وبصمةٌ ورمزٌ حسابيّ
    assert int(_grab(r"— الأسئلةُ المتاحة: (\d+)")) == QUESTIONS
    assert "قيمُها مجموعةٌ من المجمَّد" in text


def test_eleven_of_twelve_stood_and_the_one_that_fell_is_named() -> None:
    """الحصادُ يُعَدّ ولا يُدَّعى: إحدى عشرةَ صمدت وواحدةٌ سقطت."""

    fell = {"ق٥"}
    stood = {one.identifier for one in PREDICTIONS} - fell
    assert len(stood) == 11 and len(fell) == 1
    assert __doc__ is not None
    assert "إحدى عشرةَ من اثنتي عشرة" in __doc__


FELL_WITH_THEM: dict[str, str] = {
    "ق٥": "دعوايَ أنّ أوّلَ ما يربح سؤالٌ عن **حال السابق**",
}
"""ما عُلِّق على سقوط الشرط، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره."""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10
    fifth = _one("ق٥")
    assert "فقد تسبق بتّةُ الموضع بتّةَ الحال" in fifth.falsifies  # type: ignore[attr-defined]


def test_the_sixth_passed_while_its_own_wording_went_untested() -> None:
    """ق٦: اثنتا عشرةَ درجةٍ والحدُّ ثمانٍ — **والوقوفُ لم يقع**."""

    depths = int(_grab(r"— الدرجاتُ المبلوغة: (\d+)"))
    assert depths == DEPTHS
    assert _one("ق٦").verdict(Fraction(depths)) is Verdict.MET  # type: ignore[attr-defined]
    assert "قبل أن يقف" in _one("ق٦").statistic  # type: ignore[attr-defined]
    assert "الوقوف:" not in LOG.read_text(encoding="utf-8")  # ولم يُطبَع وقوف
    rungs = _rungs()
    assert all(one[4] > 0 for one in rungs)  # وكلُّ درجةٍ ربحت محجوزًا
    assert "السقفَ الذي أعلنتُه" in " ".join((__doc__ or "").split())


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ق٦",)
"""ق٦ **مرَّ ونصُّه لم يُمتحَن**: إحصاؤه «الدرجاتُ المبلوغة **قبل أن يقف**».

**والسلّمُ لم يقف**: بلغ **السقفَ الذي أعلنتُه أنا** (اثنتا عشرة) وكلُّ
درجةٍ منها **ربحت محجوزًا**. فالعددُ ١٢ ≥ ٨ صحيحٌ، **والوقوفُ لم يقع**،
**فحدُّ ما تحمله المادّةُ لم يُبلَغ**. ويُسجَّل **دَينًا** لا نتيجة: بحثٌ
يمدّ السقفَ حتّى يقف السلّمُ بنفسه **مُعيَّنٌ ولم يُجرَ**.
"""
