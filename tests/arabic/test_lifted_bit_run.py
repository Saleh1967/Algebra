"""شُغِّل ختمُ `0c070831…`: **ستّةٌ من سبعة — والبتّةُ كانت ضارّةً فالتُزِمت**.

`THE_EFFECT_OF_ONE_BIT_IS_NOW_ISOLATED`: وهو ما بقي موسومًا «استنتاجًا لا
قياسًا» منذ `69a1c10c…`. ورُفِعت **بتّةٌ واحدةٌ** اختارتها الآلةُ — أوّلُ
ما صعد بسبب الانقلاب — فتبدّلت الجملةُ **١١٬١٩٤** بتًّا.

`AND_LIFTING_IT_HELPED_WHICH_IS_THE_STRONGEST_READING`: ون٦ **منقوض**:
الفرقُ **−١١٬١٩٤** لا موجبًا. **فالبتّةُ كانت ضارّةً وقد التُزِمت**،
ورفعُها يزيد الالتزاماتِ **٦٠** والرموزَ **٥٥** ويُنزِل النسبةَ من
**٠٫٧٢٠٠** إلى **٠٫٧١٤٦**. وهو ما كتبتُه في الختم قبل النظر بوصفه
«أقوى ممّا ادّعيت على الجشع» — فوقع.

`AND_THE_BIT_WAS_TAKEN_BECAUSE_IT_LOOKED_BEST`: والبتّةُ التُزِمت لأنّها
**أربحُ ما في النافذة**: ربحُها المقيس **+١٥٬٣٣١٫٩٣** مقابلَ **+٨٬٥٨٧٫٨٣**
لِما كان «أوّلُ رابح» يأخذه — **قرابةَ الضِّعف**. فأكبرُ ربحٍ آنيٍّ كلّف
١١٬١٩٤ بتًّا في الجملة.

`AND_THE_DERIVATION_PRICED_IT_TOO`: والمشتَقُّ بالتباديل **+١٤٬٠٤٦٫٨٥**
مقابلَ المقيس **+١٥٬٣٣١٫٩٣** — خطأٌ نسبيٌّ **٠٫٠٨٣٨**، و`PMI` لها
**+٣٫٥٧٠٠** أي **+٢٫١٢٧٣** فوق `log₂ e` (ن٤ صمد).

`AND_A_ZERO_SPAN_UNIT_WAS_PRINTED_BLANK_AND_THEN_FIXED`: وطرفُها الأوّلُ
**مداه في البايتات صفر** — فطُبِع أوّلَ مرّةٍ فراغًا، وهو عطلُ عرضٍ ثامنَ
عشرَ. وأُصلِح وأُعيد التشغيلُ، **والسجلّان متطابقان رقمًا رقمًا** عدا
سطرَ العرض — وكلاهما مُودَع.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_lifted_bit_seal import BY_RANKING, DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "lifted_bit_run.log"
BLANK = REPOSITORY / "deposits" / "lifted_bit_blank_display.log"
FLAWS = REPOSITORY / "docs" / "سجل-الأعطال.md"

WHOLE = 1_472_223
WITHOUT = 1_461_028
APART = -11_194
SHARE = 0.007604
COMMITS = 1_530
COMMITS_WITHOUT = 1_590
SYMBOLS = 1_501
SYMBOLS_WITHOUT = 1_556
EXCESS = 2.1273
DERIVED = 14_046.85
MEASURED = 15_331.93
FIRST_PAYER = 8_587.83


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _text() -> str:
    return LOG.read_text(encoding="utf-8")


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("0c070831")


def test_the_control_arm_reproduces_the_sealed_run() -> None:
    """ن١: ١٬٤٧٢٬٢٢٣ و١٬٥٣٠ التزامًا — وإلّا رُدَّت المقابلةُ كلُّها."""

    assert _one("ن١").verdict(Fraction(abs(WHOLE - BY_RANKING))) is Verdict.MET  # type: ignore[attr-defined]
    assert WHOLE == BY_RANKING
    assert f"الجملة {WHOLE} | النسبةُ إلى L₀ 0.7200 | رموزٌ {SYMBOLS}" in _text()
    assert f"التزاماتٌ {COMMITS} | اقتراحاتٌ 36744" in _text()


def test_both_arms_passed_the_machine_checks() -> None:
    """ن٢ ون٣: رجعةٌ صفرٌ، ولا التزامَ بلا نزول، في الذراعين معًا."""

    text = _text()
    (first, second) = re.findall(r"رجعةُ الذراعين (\d+) و(\d+)", text)[0]
    (one, two) = re.findall(r"بلا نزولٍ في الذراعين (\d+) و(\d+)", text)[0]
    assert _one("ن٢").verdict(Fraction(max(int(first), int(second)))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ن٣").verdict(Fraction(int(one) + int(two))) is Verdict.MET  # type: ignore[attr-defined]
    assert "أقصى انحرافٍ في الذراعين 0.000000000" in text


def test_the_lifted_bit_clears_the_derived_threshold() -> None:
    """ن٤: `PMI − log₂e = +٢٫١٢٧٣` — فالعتبةُ تصف هذا الفردَ لا أكثريّةً."""

    assert _one("ن٤").verdict(_exact(EXCESS)) is Verdict.MET  # type: ignore[attr-defined]
    assert f"PMI +3.5700 | PMI − log₂e +{EXCESS:.4f}" in _text()


def test_one_bit_moves_the_total_and_by_how_much() -> None:
    """ن٥ ون٧: الفرقُ ١١٬١٩٤ بتًّا، ونسبتُه ٠٫٠٠٧٦٠٤ — موجودٌ وصغير."""

    assert _one("ن٥").verdict(Fraction(abs(APART))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ن٧").verdict(_exact(SHARE)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(abs(APART) / WHOLE - SHARE) < 1e-6  # والمطبوعُ ستُّ منازل
    assert f"الفرقُ (مرفوعةً − كما هي) {APART} بتًّا" in _text()


def test_lifting_the_bit_helped_and_that_falsifies_the_sixth() -> None:
    """ن٦ منقوض: −١١٬١٩٤ — فالجشعُ التزم ما يضرّه."""

    assert _one("ن٦").verdict(Fraction(APART)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert WITHOUT < WHOLE
    assert COMMITS_WITHOUT - COMMITS == 60
    assert SYMBOLS_WITHOUT - SYMBOLS == 55
    assert "كانت ضارّةً وقد التُزِمت" in _one("ن٦").falsifies  # type: ignore[attr-defined]
    assert "أقوى ممّا ادّعيت" in _one("ن٦").falsifies  # type: ignore[attr-defined]


def test_the_bit_was_taken_because_it_looked_best_at_that_state() -> None:
    """أربحُ ما في النافذة: +١٥٬٣٣١٫٩٣ مقابلَ +٨٬٥٨٧٫٨٣ — قرابةَ الضِّعف."""

    text = _text()
    assert f"الربحُ المقيس +{MEASURED}" in text
    assert f"رتبةٌ 1 بربحٍ +{FIRST_PAYER}" in text
    assert MEASURED / FIRST_PAYER > 1.7
    assert f"الربحُ المشتَقُّ بالتباديل +{DERIVED}" in text
    assert abs(abs(DERIVED - MEASURED) / MEASURED - 0.0838) < 5e-5


def test_no_shape_is_ever_printed_blank_again() -> None:
    """العطلُ الثامنَ عشرَ: مدًى صفرٌ يُصرَّح به ولا يُطبَع فراغًا."""

    assert "طرفاها ببايتاتهما: «مدًى صفرٌ في البايتات» + " in _text()
    assert "طرفاها ببايتاتهما:  + " in BLANK.read_text(encoding="utf-8")
    assert "طرفاها ببايتاتهما:  + " not in _text()
    written = FLAWS.read_text(encoding="utf-8")
    assert "وحدةٌ مداها صفرٌ طُبِعت فراغًا" in written
    assert "صدقٌ يُقرَأ كذبًا" in written


def test_the_two_runs_agree_digit_for_digit_apart_from_the_display() -> None:
    """إصلاحُ العرض عرضٌ لا حساب — وذلك مقيسٌ لا مُدَّعًى."""

    mark = "طرفاها ببايتاتهما"
    here = [one for one in _text().splitlines() if mark not in one]
    there = [
        one for one in BLANK.read_text(encoding="utf-8").splitlines() if mark not in one
    ]
    assert here == there
    assert len(here) > 20


def test_six_of_seven_and_the_one_that_fell_is_named() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ن١", "ن٢", "ن٣", "ن٤", "ن٥", "ن٧"}
    fell = {"ن٦"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 6 and not met & fell
