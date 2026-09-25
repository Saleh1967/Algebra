"""شُغِّل ختمُ `2a849c9a…`: **ثمانيةٌ من ثلاثةَ عشرَ — والدعوى تصمد، وأعدادُها لا**.

`THE_SUBSTANCE_OF_THE_CLAIM_HELD_AND_THEN_SOME`: الهياكلُ الغامضةُ
**١٬٨٨٦** من **١٥٬٤٧٢** (٠٫١٢١٩) تحمل **٣٤٬٩٠٢** كلمةً — **٠٫٤٤٦١** من
الكلم. وبتعريف العرض نفسِه (حروفٌ بلا علامات): **٢٬٢٦٠** من **١٤٬٨٧٢**
(٠٫١٥٢٠) بكتلةٍ **٠٫٥١٨٠**. **فقرابةُ نصفِ الكلم على هياكلَ لا تعيّن
حروفُها ضبطَها** — بأيّ التعريفين.

`AND_THE_FIVE_PRESENTED_NUMBERS_ALL_FELL_FOR_ONE_NAMED_REASON`: ك٥–ك٩
**منقوضةٌ خمسُها**، والسببُ **واحدٌ مُسمًّى**: التقشيرُ المختومُ يجعل
التنوينَ **وحدةً**، فتقع صورُه تحت هيكلٍ آخر. فهيكلُ الوحدات الثلاث
يحمل ٢١ لا ٢٢، وما نقص منه (`كُتُبٍ`) في هيكلِ الأربع.

`AND_THE_PRESENTED_FORMS_ARE_ALL_THERE_AND_MORE`: و**١٣ و٨ و١ و٩ كلُّها
مقيسةٌ كما عُرِضت**؛ وبتعريف العرض: أربعُ صورٍ لا ثلاث، وستُّ صورٍ لا
صورتان. **فالفصلُ أوسعُ ممّا عُرِض لا أضيق.**

`AND_THE_SKELETON_COUNT_ALMOST_MATCHES_UNDER_THE_PRESENTED_DEFINITION`:
وهياكلُ المجرَّد **١٤٬٨٧٢** والمعروضُ **١٤٬٨٧٠** — بفارق **٢**. وعدُّ
الكلم يفترق **٤٤٤** عن عدّ الختم، ولا أدّعي تفسيرَه.

`AND_THE_ESCALATION_REACHES_THE_WORD`: ك١١ صمد بعيدًا عن حدّه:
**٠٫٦٠٧٠** من الكلم صارت **رمزًا واحدًا**. والقيدُ يكلّف **٨٬٦١٦** بتًّا
فقط (١٬٤٠٩٬٠٠٨ مقابلَ ١٬٤٠٠٬٣٩٢) — ك١٠ صمد.

`AND_CONTEXT_IS_A_HIGHER_DEBT_AS_PRESENTED`: ك١٣ صمد: `+٢٫٣٥٠٢` بتًّا
للكلمة. **فهيكلُ ما قبلها يزيد الدَّينَ ولا ينقصه** محجوزًا — كما عُرِض.

`BUT_THE_ABSOLUTE_DEBT_IS_SMOOTHING_BOUND_AND_SAID_TO_BE`: و**الرقمُ
المطلقُ مقيَّدٌ بالتنعيم**: `H(الصورة|الهيكل)` داخلَ العيّنة **٠٫٤٠٦٩**
بتًّا، والمحجوزُ **٨٫٨٤٠٧** — والفرقُ من لابلاس على معجم صورٍ واسع، لا
من الغموض. **فالمقارنةُ هي المتينة، لا المقدار** — ويُقال.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_word_escalation_seal import (
    BY_LICENCE,
    DIGEST,
    ORACLE,
    PREDICTIONS,
    SKELETONS,
    TOKENS,
    VAGUE,
    VAGUE_MASS,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "word_escalation_run.log"
SPLIT = REPOSITORY / "deposits" / "word_escalation_definitions.log"

MY_TOKENS = 78_245
MY_SKELETONS = 15_472
MY_VAGUE = 1_886
MY_VAGUE_MASS = 34_902
MY_EXEMPLAR = 21
BARE_SKELETONS = 14_872
BARE_VAGUE = 2_260
TOTAL = 1_409_008
WHOLE_WORDS = 0.6070
INSIDE = 0.4069
DEBT = 8.8407
WITH_CONTEXT = 11.1909


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, path: Path = LOG) -> str:
    found = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert found is not None, pattern
    return found.group(1)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("2a849c9a")


def test_the_machine_held_and_the_constraint_was_applied() -> None:
    """ك١–ك٤: رجعةٌ صفرٌ، ولا التزامَ بلا نزول، وانحرافٌ صفرٌ، وعبورٌ صفر."""

    assert (
        _one("ك١").verdict(Fraction(int(_grab(r"مواضعُ الخلاف = (\d+)")))) is Verdict.MET
    )  # type: ignore[attr-defined]
    assert _one("ك٢").verdict(Fraction(int(_grab(r"بلا نزولٍ (\d+)")))) is Verdict.MET  # type: ignore[attr-defined]
    drift = float(_grab(r"أقصى انحرافٍ بين الآلتين: ([\d.]+)"))
    assert _one("ك٣").verdict(_exact(drift)) is Verdict.MET and drift == 0.0  # type: ignore[attr-defined]
    crossing = int(_grab(r"العابرُ لحدّ الكلمة: (\d+) من"))
    assert _one("ك٤").verdict(Fraction(crossing)) is Verdict.MET and crossing == 0  # type: ignore[attr-defined]


def test_the_four_presented_counts_all_fell() -> None:
    """ك٥–ك٨ منقوضة — والفروقُ تُنشَر بأرقامها لا تُطوى."""

    apart = {
        "ك٥": abs(MY_TOKENS - TOKENS),
        "ك٦": abs(MY_SKELETONS - SKELETONS),
        "ك٧": abs(MY_VAGUE - VAGUE),
        "ك٨": abs(MY_VAGUE_MASS - VAGUE_MASS),
    }
    for name, gap in apart.items():
        assert _one(name).verdict(Fraction(gap)) is Verdict.FALSIFIED, name  # type: ignore[attr-defined]
    assert apart == {"ك٥": 444, "ك٦": 602, "ك٧": 213, "ك٨": 2_639}
    text = LOG.read_text(encoding="utf-8")
    assert f"الكلمُ: {MY_TOKENS}" in text
    assert f"هياكلُ متمايزة: {MY_SKELETONS}" in text
    assert f"غامضةٌ منها: {MY_VAGUE} " in text
    assert f"كتلتُها من الكلم: {MY_VAGUE_MASS} " in text


def test_the_reason_for_the_gap_is_named_and_measured() -> None:
    """التنوينُ وحدةٌ في التقشير — فتقع صورُه تحت هيكلٍ آخر."""

    text = SPLIT.read_text(encoding="utf-8")
    assert "هيكلٌ بـ3 وحدات (21 كلمة): كُتِبَ×13 | كَتَبَ×8" in text
    assert "كُتُبٍ×1" in text  # في هيكل الأربع
    assert _one("ك٩").verdict(Fraction(abs(MY_EXEMPLAR - 22))) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    tails = int(_grab(r"هياكلُ آخرُ وحدةٍ فيها نون: (\d+)", SPLIT))
    assert tails == 4_976


def test_the_presented_forms_are_all_present_and_more() -> None:
    """١٣ و٨ و١ و٩ مقيسةٌ كما عُرِضت — والفصلُ أوسعُ لا أضيق."""

    text = SPLIT.read_text(encoding="utf-8")
    assert "هيكلُ كتب (23 كلمة، 4 صورة): كُتِبَ×13 | كَتَبَ×8 | كُتُبٍ×1" in text
    assert "عَلِمَ×9" in text
    assert "هيكلُ علم (60 كلمة، 6 صورة)" in text


def test_the_claim_itself_holds_under_both_definitions() -> None:
    """قرابةُ نصفِ الكلم على هياكلَ غامضة — بأيّ التعريفين."""

    assert MY_VAGUE_MASS / MY_TOKENS > 0.44
    text = SPLIT.read_text(encoding="utf-8")
    assert f"هياكلُ مجرَّدةٌ متمايزة: {BARE_SKELETONS}" in text
    assert f"غامضةٌ منها: {BARE_VAGUE} (0.1520)" in text
    assert "كتلتُها: 42752 (0.5180)" in text
    assert abs(BARE_SKELETONS - SKELETONS) == 2  # والمعروضُ ١٤٨٧٠


def test_the_escalation_reaches_the_word_and_the_constraint_is_cheap() -> None:
    """ك١٠ وك١١: ٠٫٦٠٧٠ من الكلم رمزٌ واحد، والقيدُ يكلّف ٨٬٦١٦ بتًّا."""

    assert _one("ك١٠").verdict(Fraction(TOTAL)) is Verdict.MET  # type: ignore[attr-defined]
    assert TOTAL - BY_LICENCE == 8_616
    share = float(_grab(r"كلمٌ صارت رمزًا واحدًا: \d+ من \d+ = ([\d.]+)"))
    assert _one("ك١١").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(share - WHOLE_WORDS) < 5e-5
    assert f"الجملة {TOTAL} | النسبةُ إلى L₀ 0.6891" in LOG.read_text("utf-8")


def test_context_is_a_higher_debt_as_presented() -> None:
    """ك١٣: `+٢٫٣٥٠٢` — فهيكلُ ما قبلها يزيد الدَّينَ محجوزًا."""

    apart = float(_grab(r"الفرقُ على المشهود \(بسياقٍ − بلا سياق\): \+([\d.]+)"))
    assert _one("ك١٣").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(apart - (WITH_CONTEXT - DEBT)) < 5e-4
    assert _one("ك١٢").verdict(_exact(DEBT)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_absolute_debt_is_declared_smoothing_bound() -> None:
    """داخلَ العيّنة ٠٫٤٠٦٩ ومحجوزًا ٨٫٨٤٠٧ — فالمقارنةُ المتينةُ لا المقدار."""

    inside = float(_grab(r"داخلَ العيّنة: ([\d.]+) بتًّا"))
    assert abs(inside - INSIDE) < 5e-5
    assert inside < DEBT / 10  # والفجوةُ من لابلاس لا من الغموض
    assert __doc__ is not None
    assert "فالمقارنةُ هي المتينة، لا المقدار" in __doc__


def test_eight_of_thirteen_and_the_five_that_fell_are_named() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ك١", "ك٢", "ك٣", "ك٤", "ك١٠", "ك١١", "ك١٢", "ك١٣"}
    fell = {"ك٥", "ك٦", "ك٧", "ك٨", "ك٩"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 8 and len(fell) == 5 and not met & fell
