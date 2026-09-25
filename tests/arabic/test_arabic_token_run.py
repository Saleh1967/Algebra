"""شُغِّل ختمُ `494465d1…`: **اثنا عشرَ من اثني عشر — ولا نتيجةَ تنقلب**.

`THE_CORRECTION_DID_EXACTLY_WHAT_SUBTRACTION_SAID_IT_WOULD`: ط٢ وط٣ وط١٠
وط١١ — **وهي حسابٌ لا تنبّؤ، وقد كُتِب ذلك قبل النظر**. الألفاظُ
**٧٨٬٢٤٥** = ٨٢٬٥٣٢ − ٤٬٢٨٧ بلا بقيّة، وألفاظُ الترقيم **صفر**،
والهياكلُ **١٤٬٨٧١** بنقصان واحد.

`AND_THE_BLIND_LETTER_IS_ONE_AND_IT_IS_A_LETTER`: وحروفُ الخاتمة التي لا
تحمل حالًا ألبتّة صارت **واحدًا**: `ى` بـ**٢٬٥٩٢** وقوعًا. **فما بقي حرفٌ
حقًّا**، وما سقط كان ذنَبَ وسم. وهذه صورةُ الخانة الخالية بتّةً: **موضعٌ
لا يحمل حالًا في المجمَّد كلِّه**، وخلوُّه **مُصنَّفٌ لا مُصفَّر**.

`AND_THE_FIVE_THAT_COULD_NOT_BE_SUBTRACTED_ALL_HELD`: ط٦ وط٧ وط٨ وط٩
وط١٢ — **وهي ما لا يُعلَم إلّا بالتشغيل**، لأنّ إسقاطَ الوسم **يَصِل
جارَين كانا مفصولين**. فالأزواجُ نزلت **٧٦٬٢٩٦ ⟶ ٧٢٬٠٠٩**، والمعلوماتُ
**٠٫٠٦٨٣ ⟶ ٠٫٠٦٥٣** — فرقٌ **٠٫٠٠٣٠** دون الحدّ **٠٫٠١**. **فالوسمُ كان
يقطع السلسلةَ قطعًا طفيفًا**، كما قدّرت.

`AND_THE_ENDING_LETTER_STILL_TELLS_FIFTEEN_TIMES_MORE`: معلوماتُ حرفِ
الخاتمة **١٫٠٦٠٨ ⟶ ١٫٠٣١٠** — نقصانٌ **٠٫٠٢٩٨** دون الحدّ **٠٫١٥**.
والنسبةُ إلى معلوماتِ الجار **١٥٫٧٩** ضعفًا. **فحالُ الخاتمة يُقرأ من
خاتمتها لا من جارتها**، والتصحيحُ لم يُزحزح ذلك.

`AND_THE_MASS_MOVED_MORE_THAN_THE_COUNT`: نصيبُ ثابتِ الحال من الهياكل
**٠٫٥٧٧١ ⟶ ٠٫٥٧٦٩** — لم يكد يتحرّك. **وكتلتُه تحرّكت**: **٠٫٣٩٦٤ ⟶
٠٫٣٦٣٣**، لأنّ الوسمَ كان **هيكلًا واحدًا ثابتَ الحال يحمل ٤٬٢٨٧ لفظًا**.
فكان يُثقِل كفّةَ الثابت **بكتلةٍ لا بعدد**. **وهذا وجهُ الخلل الأشدّ**:
عدٌّ واحدٌ معطوبٌ لا يُرى في نصيب العدد ويُرى في نصيب الكتلة.

`AND_CONSTANCY_STILL_CARRIES_ACROSS_THE_SPLIT`: ط١٢ صمد **على حدٍّ
مرفوع**: كنتُ قِستُ ٠٫٩٠٦١ على الحدّ المعطوب فرفعتُ الشرطَ من ثمانين إلى
**خمسٍ وثمانين**، والمقيسُ بعد التصحيح **٠٫٩٠٥٩** — ٥٤٩ من ٦٠٦.

`AND_THE_THREE_STILL_DO_NOT_HOLD_THE_FIELD`: نصيبُ الثلاث **٠٫٤٣٩٦ ⟶
٠٫٤٦٣٧** — صعد ولم يبلغ النصف. و«بلا علامة» **٠٫٣٤٦٦ ⟶ ٠٫٣١٠٨**، وبقيت
أكبرَ خانةٍ في الحقل. وH(الحال) **٢٫٥٥٨٣ ⟶ ٢٫٦١٠٦**.

`AND_THE_PROVEN_BOUNDS_WERE_TAKEN_WHERE_THEY_TESTIFY`: ط٤ وط٥ أُخِذا
**بعد ألفِ لفظ** لا عند أوّل الحلقة: **+٠٫٠٥٥٢٠٧** و**−٢٩٫٧٨٥٢٦١**،
وعند الختام **+٠٫٠٦٥٣٤٩** و**−٥٢٫٤٣١٤٣٤**. **فالشهادةُ غيرُ خاوية** —
وهو إصلاحُ ما سُمّي في `7773c03f…` تعليلًا لم يُؤيَّد.

**ولا نتيجةَ انقلبت**: الخللُ مسَّ **٥٫٢٪ من الألفاظ** ولم يقلب حكمًا
واحدًا سوى الشرط الذي كشفه. **وهذا لا يُبرّئه** — يُقال إنّه لم يقلب، لا
إنّه لم يكن.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_arabic_token_seal import DIGEST, ORACLE, PREDICTIONS
from test_ingestion_swallows import MIRROR_INVARIANT, WHOLE_LINE_TOKENS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "arabic_token_run.log"
FIRST = REPOSITORY / "deposits" / "state_cycle_run.log"

pytestmark = requires_corpus

LINES = 6_236
BEFORE_TOKENS = WHOLE_LINE_TOKENS
TOKENS = MIRROR_INVARIANT
MARKUP = BEFORE_TOKENS - TOKENS
"""لا يُكتَب ههنا عددٌ بيد: الثلاثةُ تُؤخَذ من `test_ingestion_swallows`.

**ولمَ الاشتقاقُ لا الكتابة**: هذه الأعدادُ كانت **مُودَعةً في الشجرة قبل
أن أكتب ختمَ `7773c03f…`** — ٨٢٬٥٣٢ على السطر كلِّه، و٧٨٬٢٤٥ بعد الوسم،
والفجوةُ ٤٬٢٨٧ **محسوبةً ومُغلَقةً**. فكتبتُ حدَّ اللفظ بما يبتلعها، **وما
راجعتُ ما في يدي**. فهي تُشتَقُّ ههنا من مصدرها الواحد كي لا تُكتَب مرّتين
ولا تفترق نسختاها.
"""
SKELETONS = 14_871
BLIND_COUNT = 2_592
PAIRS_BEFORE = 76_296
PAIRS = 72_009
NEIGHBOUR_BEFORE = 0.0683
NEIGHBOUR = 0.0653
LETTER_BEFORE = 1.0608
LETTER = 1.0310
STEADY_SHARE_BEFORE = 0.5771
STEADY_SHARE = 0.5769
MASS_BEFORE = 0.3964
MASS = 0.3633
CARRIED = 0.9059
THREE = 0.4637
BARE_SHARE = 0.3108
FIELD_ENTROPY = 2.6106


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("494465d1")
    assert "عربيٌّ فيه حرفٌ عربيّ" in LOG.read_text(encoding="utf-8")


def test_the_subtraction_conditions_hold_exactly_as_subtraction() -> None:
    """ط٢ وط٣ وط١٠ وط١١ حسابٌ لا تنبّؤ — والحسابُ يُطابِق بلا بقيّة."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    assert _one("ط١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    tokens = int(_grab(r"عبرَ العدّادات (\d+) \| عبرَ الأسطر \d+"))
    assert tokens == TOKENS == BEFORE_TOKENS - MARKUP
    assert _one("ط٢").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert int(_grab(r"ألفاظُ الترقيم \(لا حرفَ عربيًّا فيها\): (\d+)")) == 0
    assert int(_grab(r"هياكلُ متمايزة: (\d+)")) == SKELETONS
    assert SKELETONS == int(_grab(r"هياكلُ متمايزة: (\d+)", FIRST)) - 1
    blind = int(_grab(r"لا تحمل حالًا ألبتّة: (\d+)"))
    assert blind == 1
    assert _one("ط٣").verdict(Fraction(blind)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_one_blind_position_is_a_letter_and_its_vacancy_is_classified() -> None:
    """خانةُ الحال تخلو عند موضعٍ واحدٍ — وخلوُّها يُصنَّف ولا يُصفَّر."""

    below = LOG.read_text(encoding="utf-8").split("لا تحمل حالًا ألبتّة:")[1]
    found = re.findall(r"^    (\S+) \| وقوعاتٌ (\d+)$", below, re.M)
    assert len(found) == 1
    ((shape, number),) = found
    assert int(number) == BLIND_COUNT
    assert len(shape) == 1  # محرفٌ واحدٌ، مقروءٌ من السجلّ لا مكتوبٌ بيد
    assert "فحصُها مُعيَّنٌ ولم يُجرَ" in LOG.read_text(encoding="utf-8")


def test_the_two_proven_bounds_testify_past_the_trivial_extreme() -> None:
    """ط٤ وط٥ بعد ألفِ لفظ — والشهادةُ غيرُ خاوية هذه المرّة."""

    settled = float(_grab(r"أدنى فرقٍ بعد ألف = (\S+)"))
    slack = float(_grab(r"أقصى فسحةٍ بعد ألف = (\S+)"))
    assert _one("ط٤").verdict(_exact(settled)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ط٥").verdict(_exact(slack)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(settled - 0.055207) < 5e-7 and settled > 0
    assert abs(slack + 29.785261) < 5e-7 and slack < 0
    closing, closing_slack = re.findall(
        r"وعند الختام: فرقٌ (\S+) \| فسحةٌ (\S+)", LOG.read_text(encoding="utf-8")
    )[0]
    assert abs(float(closing) - 0.065349) < 5e-7
    assert abs(float(closing_slack) + 52.431434) < 5e-7


def test_dropping_the_markup_joined_neighbours_and_barely_moved_the_chain() -> None:
    """ط٦ وط٧: الأزواجُ نزلت والمعلوماتُ لم تكد تتحرّك."""

    pairs = int(_grab(r"أزواجٌ (\d+)"))
    assert pairs == PAIRS
    assert int(_grab(r"أزواجٌ (\d+)", FIRST)) == PAIRS_BEFORE
    assert PAIRS_BEFORE - pairs == MARKUP  # زوجان يصيران زوجًا: نقصٌ بواحدٍ لكلّ وسم
    now = float(_grab(r"\n  I = ([\d.]+)"))
    before = float(_grab(r"\n  I = ([\d.]+)", FIRST))
    assert abs(now - NEIGHBOUR) < 5e-5 and abs(before - NEIGHBOUR_BEFORE) < 5e-5
    assert _one("ط٦").verdict(_exact(abs(now - before))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ط٧").verdict(_exact(now)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(abs(now - before) - 0.0030) < 5e-5


def test_the_ending_letter_still_tells_fifteen_times_more() -> None:
    """ط٩: النقصانُ ٠٫٠٢٩٨ دون الحدّ، والنسبةُ إلى الجار ١٥٫٧٩ ضعفًا."""

    now = float(_grab(r"I\(الحال؛ حرفُ الخاتمة\) = ([\d.]+)"))
    before = float(_grab(r"I\(الحال؛ حرفُ الخاتمة\) = ([\d.]+)", FIRST))
    assert abs(now - LETTER) < 5e-5 and abs(before - LETTER_BEFORE) < 5e-5
    assert _one("ط٩").verdict(_exact(abs(now - before))) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(abs(now - before) - 0.0298) < 5e-5
    neighbour = float(_grab(r"\n  I = ([\d.]+)"))
    assert abs(now / neighbour - 15.79) < 5e-3
    assert int(_grab(r"حروفُ خاتمةٍ متمايزة: (\d+)")) == 36


def test_the_hold_out_direction_held_under_the_corrected_bound() -> None:
    """ط٨: الملحَقةُ ٠٫٠٦٦٠ والمحجوزةُ ٠٫٠٦٣٩ — والاتّجاهُ كما يقتضي."""

    inside, outside, apart = re.findall(
        r"ملحَقة ([\d.]+) \| محجوزة ([\d.]+) \| فرقٌ (\S+)",
        LOG.read_text(encoding="utf-8"),
    )[0]
    assert abs(float(inside) - 0.0660) < 5e-5
    assert abs(float(outside) - 0.0639) < 5e-5
    assert _one("ط٨").verdict(_exact(float(apart))) is Verdict.MET  # type: ignore[attr-defined]
    assert float(apart) < 0


def test_the_mass_moved_far_more_than_the_count_did() -> None:
    """ط١٠ وط١١: العددُ لم يتحرّك والكتلةُ تحرّكت — وذاك وجهُ الخلل الأشدّ."""

    share = float(_grab(r"نصيبُ الثابت من الهياكل: ([\d.]+)"))
    mass = float(_grab(r"نصيبُ كتلة الثابت من الألفاظ: ([\d.]+)"))
    assert abs(share - STEADY_SHARE) < 5e-5 and abs(mass - MASS) < 5e-5
    assert _one("ط١٠").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ط١١").verdict(_exact(mass)) is Verdict.MET  # type: ignore[attr-defined]
    moved_count = abs(share - STEADY_SHARE_BEFORE)
    moved_mass = abs(mass - MASS_BEFORE)
    assert moved_count < 0.0005 and moved_mass > 0.03
    assert moved_mass / moved_count > 100  # عدٌّ واحدٌ معطوبٌ يُرى في الكتلة
    steady_mass = int(_grab(r"كتلةُ الثابت (\d+) \| كتلةُ المتبدّل \d+"))
    assert (
        steady_mass
        == int(_grab(r"كتلةُ الثابت (\d+) \| كتلةُ المتبدّل \d+", FIRST)) - MARKUP
    )


def test_constancy_still_carries_across_the_split_on_a_raised_bar() -> None:
    """ط١٢: ٥٤٩ من ٦٠٦ = ٠٫٩٠٥٩ — على حدٍّ رُفِع من ثمانين إلى خمسٍ وثمانين."""

    even, both, carried = re.findall(
        r"ثابتُ الزوجيّ (\d+) \| باقٍ ثابتًا في الفرديّ (\d+) \| نصيبٌ ([\d.]+)",
        LOG.read_text(encoding="utf-8"),
    )[0]
    assert (int(even), int(both)) == (606, 549)
    assert abs(float(carried) - CARRIED) < 5e-5
    assert _one("ط١٢").verdict(_exact(float(carried))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ط١٢").threshold == Fraction(85, 100)  # type: ignore[attr-defined]


def test_the_field_shifted_and_the_three_still_do_not_hold_it() -> None:
    """نصيبُ الثلاث صعد ولم يبلغ النصف، وبلا علامةٍ بقيت أكبرَ خانة."""

    three = float(_grab(r"نصيبُ الثلاث: \d+ من \d+ = ([\d.]+)"))
    bare = float(_grab(r"بلا علامة\) \d+ \| نصيبٌ ([\d.]+)"))
    assert abs(three - THREE) < 5e-5 and three < 0.5
    assert abs(bare - BARE_SHARE) < 5e-5
    assert three > float(_grab(r"نصيبُ الثلاث: \d+ من \d+ = ([\d.]+)", FIRST))
    assert bare < float(_grab(r"بلا علامة\) \d+ \| نصيبٌ ([\d.]+)", FIRST))
    assert abs(float(_grab(r"H\(الحال\) = ([\d.]+)")) - FIELD_ENTROPY) < 5e-5
    assert bare > max(
        float(one)
        for one in re.findall(
            r"ARABIC \w+\) \d+ \| نصيبٌ ([\d.]+)", LOG.read_text(encoding="utf-8")
        )
    )


def test_twelve_of_twelve_stood_and_no_conclusion_turned_over() -> None:
    """الحصادُ يُعَدّ: اثنا عشرَ صمدت، ولا حكمَ انقلب — ولا تبرئةَ في ذلك."""

    assert len(PREDICTIONS) == 12
    assert __doc__ is not None
    assert "اثنا عشرَ من اثني عشر" in __doc__
    assert "يُقال إنّه لم يقلب، لا" in " ".join(__doc__.split())
    assert abs(MARKUP / BEFORE_TOKENS - 0.0519) < 5e-5


FELL_WITH_THEM: dict[str, str] = {}
"""لم يسقط شرطٌ ههنا — فلا نصَّ سقوطٍ يُقتبَس، والجدولُ فارغٌ بشاهده."""


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا تعليلَ مرَّ بلا تأييد ههنا: كلُّ شرطٍ حُكِم به بطرفٍ غيرِ تافه.

وط٤ وط٥ — وهما اللذان مرّا في `7773c03f…` بطرفين تافهين — **أُخِذا ههنا
بعد ألفِ لفظ** بنصّ الختم نفسِه، فالشهادةُ غيرُ خاوية.
"""
