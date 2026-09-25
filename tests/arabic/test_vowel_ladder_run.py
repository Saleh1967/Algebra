"""شُغِّل ختمُ `9034199d…`: **أربعةٌ من خمسة، وس٣ سقط — والضبطُ دون بتٍّ**.

`THE_ONE_CONDITION_THAT_WAS_REALLY_AT_RISK_IS_THE_ONE_THAT_FELL`: وس٣ —
«أدنى h على رتبةٍ مقروءة **≥ بتٍّ واحد**» — **سقط**. والمقيسُ عند الرتبة
الثانية من سلّم الفكّ **٠٫٧٦٥٢ بتًّا**. وما يسقط بسقوطه مكتوبٌ في الختم
نفسِه: «أكثرُ الضبط **مُستخرَجٌ من الرسم وسياقِه**، والدَّينُ الأوّلُ كان
أصغرَ ممّا ظُنّ».

`AND_NO_READING_OF_READABILITY_SAVES_IT`: والحكمُ **لا يتبدّل بتأويل**: إن
عُدَّت الرتبُ الأربعُ كلُّها مقروءةً فالأدنى ٠٫٥٧٤٨؛ وإن قُصِرت القراءةُ على
ما نصيبُه ≥ ½ (وهو معيارُ س٤) فالأدنى ٠٫٧٦٥٢. وكلاهما دون البتّ — فلا
مدخلَ لإعادة تفسيرِ شرطٍ بعد النظر.

`THE_LADDER`: والسلّمان:

| الرتبة | h^A (الرسم) | نصيبُ المقروء | h^B (الفكّ) | نصيبُ المقروء |
|---|---|---|---|---|
| ٠ | ١٫٩٥٢٥ | ١٫٠٠٠٠ | ١٫٩٥٢٥ | ١٫٠٠٠٠ |
| ١ | ١٫٤٩٦٤ | ٠٫٩٩٠٧ | **١٫١٠٦٦** | ٠٫٩٣٢٧ |
| ٢ | ١٫٠٩٩٠ | ٠٫٧٨٩٨ | **٠٫٧٦٥٢** | ٠٫٥٩١٩ |
| ٣ | ٠٫٧٥٣٧ | ٠٫٤١٨٤ | ٠٫٥٧٤٨ | ٠٫٣٠٤٠ |

فحرفٌ واحدٌ قبلَه يستردّ **٢٣٪** ممّا ظُنّ ضبطًا خالصًا، وحرفان **٤٤٪**؛
وقارئٌ متتابعٌ حلّ ما قبلَه يستردّ **٦١٪** بحرفين. والمعنى بلسانٍ غيرِ
رياضيّ: **أكثرُ الشكل مُستنتَجٌ لا مُخبِر** — وهو ما يفعله القارئُ المتمكّن
بالنصّ غير المشكول، مقيسًا لأوّل مرّة.

`AND_THE_MACHINE_CONDITIONS_HELD`: وس١ (التناقصُ بالرتبة) وس٢ (سلّمُ الفكّ
لا يعلو سلّمَ الرسم) صمدتا في الرتب كلِّها — **وهما شرطا آلةٍ لا مادّة**؛
ويُقيَّد إقرارُهما: الرتبُ تُقرأ على **مجموعاتٍ مختلفة** من المواضع (نصيبُ
المقروء ينزل بالرتبة)، فتناقصُ السلّم ههنا **مرصودٌ لا موجَبٌ بالمبرهنة**.

`AND_THE_BIAS_IS_NOT_THE_STORY_THIS_TIME`: وس٥ صمد بهامشٍ واسع: التصحيحُ
**٠٫٠١٧٤** عند أعلى رتبةٍ مقروءة، والحدُّ ٠٫٢. فالهبوطُ **بنيةٌ لا ندرة** —
بخلاف هضبةِ المدى البعيد التي كانت انحيازًا كلَّها. والشاهدُ الداخليّ:
h^A_0 مصحَّحةً ١٫٩٥٢٥ وتصحيحُها ٠٫٠٠٠٧، و١٫٩٥٢٥ − ٠٫٠٠٠٧ = **١٫٩٥١٨** —
وهو المقيسُ في `dd8d366` بالضبط، فالآلتان تتّفقان على رقمٍ واحد.

`AND_THE_LADDER_HAS_NOT_CONVERGED`: **ولا يُدَّعى حدّ**: السلّمُ ما زال
ينزل عند الرتبة الثالثة، ونصيبُ المقروء ينزل معه. فالمنشورُ **حدٌّ أعلى
يزداد إحكامًا**، لا قيمةٌ نهائيّة؛ والرتبةُ الرابعةُ فما فوقُ `UNREACHABLE`
بأرضيّة الختم — تُصنَّف ولا تُقدَّر.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus
from test_vowel_ladder_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_vowel_ladder.py"

pytestmark = requires_corpus

RASM = ((0, 1.9525), (1, 1.4964), (2, 1.0990), (3, 0.7537))
DECODE = ((0, 1.9525), (1, 1.1066), (2, 0.7652), (3, 0.5748))
RASM_SHARE = {0: 1.0000, 1: 0.9907, 2: 0.7898, 3: 0.4184}
DECODE_SHARE = {0: 1.0000, 1: 0.9327, 2: 0.5919, 3: 0.3040}
HIGHEST_READABLE = 2
BIAS_AT_TWO = 0.0174
UNCONDITIONED = 1.9518


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_vowel_ladder", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _ladders() -> (
    tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]
):
    reader = _reader()
    lines = reader.lines_of_units(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
    rasm = [
        reader.ladder_step(reader.contexts(lines, order, with_states=False))  # type: ignore[attr-defined]
        for order, _ in RASM
    ]
    decode = [
        reader.ladder_step(reader.contexts(lines, order, with_states=True))  # type: ignore[attr-defined]
        for order, _ in DECODE
    ]
    return (rasm, decode)


def test_the_seal_is_the_one_that_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("9034199d")


def test_the_run_reproduces_the_recorded_ladders() -> None:
    """السلّمان يُعادُ اشتقاقُهما من الشيفرة لا يُنقلان."""

    rasm, decode = _ladders()
    for (order, expected), (measured, _, share) in zip(RASM, rasm):
        assert abs(measured - expected) < 5e-4, order
        assert abs(share - RASM_SHARE[order]) < 5e-4
    for (order, expected), (measured, _, share) in zip(DECODE, decode):
        assert abs(measured - expected) < 5e-4, order
        assert abs(share - DECODE_SHARE[order]) < 5e-4


def test_the_zeroth_rung_agrees_with_the_earlier_unconditioned_measure() -> None:
    """١٫٩٥٢٥ − ٠٫٠٠٠٧ = ١٫٩٥١٨ — والآلتان تتّفقان على رقمٍ واحد."""

    rasm, _ = _ladders()
    corrected, bias, share = rasm[0]
    assert share == 1.0
    assert abs((corrected - bias) - UNCONDITIONED) < 5e-4


def test_condition_one_and_two_held_as_machine_checks() -> None:
    """س١ التناقصُ وس٢ الفكُّ لا يعلو الرسمَ — صمدتا في الرتب كلِّها."""

    rasm, decode = _ladders()
    first = next(one for one in PREDICTIONS if one.identifier == "س١")
    steps = [a[0] - b[0] for a, b in zip(rasm, rasm[1:])]
    steps += [a[0] - b[0] for a, b in zip(decode, decode[1:])]
    worst = min(steps)
    assert first.verdict(Fraction(int(worst * 10_000), 10_000)) is Verdict.MET
    second = next(one for one in PREDICTIONS if one.identifier == "س٢")
    gaps = [d[0] - r[0] for r, d in zip(rasm, decode)]
    assert second.verdict(Fraction(int(max(gaps) * 10_000), 10_000)) is Verdict.MET


def test_condition_three_is_falsified_under_either_reading() -> None:
    """أدنى h دون البتّ — سواءٌ عُدَّت الرتبُ الأربعُ مقروءةً أم الثلاثُ."""

    rasm, decode = _ladders()
    third = next(one for one in PREDICTIONS if one.identifier == "س٣")
    everything = min(one[0] for one in rasm + decode)
    by_share = min(one[0] for one in rasm + decode if one[2] >= 0.5)
    for lowest in (everything, by_share):
        measured = Fraction(int(lowest * 10_000), 10_000)
        assert third.verdict(measured) is Verdict.FALSIFIED
    assert abs(by_share - 0.7652) < 5e-4
    assert abs(everything - 0.5748) < 5e-4


def test_condition_four_and_five_held() -> None:
    """نصيبُ المقروء عند الثانية ٠٫٧٨٩٨، والانحيازُ ٠٫٠١٧٤ من حدٍّ ٠٫٢."""

    rasm, _ = _ladders()
    fourth = next(one for one in PREDICTIONS if one.identifier == "س٤")
    share = rasm[HIGHEST_READABLE][2]
    assert fourth.verdict(Fraction(int(share * 10_000), 10_000)) is Verdict.MET
    fifth = next(one for one in PREDICTIONS if one.identifier == "س٥")
    bias = rasm[HIGHEST_READABLE][1]
    assert abs(bias - BIAS_AT_TWO) < 5e-4
    assert fifth.verdict(Fraction(int(bias * 10_000), 10_000)) is Verdict.MET


def test_the_share_recovered_by_context_is_reported_not_extrapolated() -> None:
    """٢٣٪ بحرفٍ و٤٤٪ بحرفين، و٦١٪ للقارئ المتتابع — ولا حدَّ يُدَّعى."""

    rasm, decode = _ladders()
    base = rasm[0][0]
    assert abs((base - rasm[1][0]) / base - 0.2336) < 2e-3
    assert abs((base - rasm[2][0]) / base - 0.4371) < 2e-3
    assert abs((base - decode[2][0]) / base - 0.6081) < 2e-3
    # والسلّمُ لم يستوِ: الرتبةُ الثالثةُ أدنى من الثانية في السلّمين
    assert rasm[3][0] < rasm[2][0] and decode[3][0] < decode[2][0]
    assert rasm[3][2] < 0.5 and decode[3][2] < 0.5  # ونصيبُهما دون الأرضيّة


FELL_WITH_THEM: dict[str, str] = {
    "س٣": "دعوى أنّ الضبطَ خبرٌ جوهريٌّ لا زائدةٌ",
}
"""ما عُلِّق على سقوط كلِّ شرطٍ، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره.

فنصُّ `falsifies` **دعوًى ثانيةٌ معرَّضةٌ للسقوط** لا شرحًا محايدًا: إن سقط
الشرطُ سقط معه ما عُلِّق عليه، ويُعلَن ذلك **عند موضع السقوط** لا في شرحٍ
لاحق. وهو العطلُ الثاني عشر، ممنوعًا آليًّا.
"""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
