"""شُغِّل السقفُ المادّيّ: **الحلقةُ تقف عند الدرجة ٢٦، لا عند ١٢**.

**الحصاد**: **الاثنتا عشرةَ كلُّها صمدت** — ومنها ذ٥ التي كانت **دعوًى
عليّ**: أنّ سقفي المكتوبَ عند ١٢ كان **سابقًا للمادّة**. وقد كان.

`THE_MATERIAL_CEILING_IS_TWENTY_SIX_AND_THE_WRITTEN_ONE_WAS_TWELVE`: رُفِع
`MOST` **في الذاكرة** إلى مئة، فبلغت الحلقةُ **٢٦ درجةً** ثمّ طبعت سطرَ
الوقوف عند الدرجة ٢٧: **لا سؤالَ يربح محجوزًا**. **فالوقوفُ بالمادّة لا
بنفاد الأسئلة** (سبعةٌ وخمسون سؤالًا متاحًا، اختير منها ٢٦).

`AND_THE_FIRST_TWELVE_REPRODUCED_EXACTLY_SO_THE_WRAPPER_IS_NOT_ACCUSED`:
و**صفرُ خلافٍ** في الاثنتي عشرةَ الأولى مقابلةً بـ
`context_ladder_run.log` — سطرًا سطرًا بكلّ حقوله. **فاختيارُ الجشع لا
يتعلّق بالسقف**، وذلك مفحوصٌ لا مقولٌ (ذ٤).

`AND_WHAT_MY_CAP_WAS_HIDING_IS_ELEVEN_AND_A_HALF_PERCENT`: والدرجاتُ
الأربعَ عشرةَ الزائدةُ تضيف **+٠٫٠٢٧٨ بتًّا محجوزًا** — **٠٫١١٦ من الكسب
كلِّه**. **فحدِّي كان يكتم نحوَ ثُمنِ ما يفيده السياق**، لا نصفَه ولا
عُشرَ عُشره. **ويُقال بمقداره لا بوصفه.**

`AND_THE_FIRST_BIT_STAYS_THE_LARGEST`: ونصيبُ «آخرُ السطر» من الكسب
المحجوز **٠٫٢٣٧٤** بعد التعميق، وكان **٠٫٢٦٨٦** عند السقف القصير. **فهي
تبقى أكبرَ بتّةٍ في السلّم**، وإنّما نزل نصيبُها بمقدارٍ صغير — **والدعوى
التي كانت تُخشى (أنّها بدت غالبةً بسقفٍ قصير) سقطت**.

`AND_THE_SUM_IS_READ_FROM_THE_LADDERS_OWN_LINE_NOT_RESUMMED`: ومجموعُ
الكسب يُقرَأ من **سطر السلّم نفسِه** (`+0.239608`) لا من جمع المطبوع بأربع
منازل (`+0.239800`). **والفرقُ ٠٫٠٠٠١٩٢ تدويرٌ لا خلاف**، ويُطبَع عددًا
كي لا يُظَنّ اختلافًا في المقيس.

**وما لا يُدَّعى**: بلوغُ السقف **لا يستنفد السياق**. العائلاتُ **خمسٌ**
على **هذه القسمة**؛ وعائلةٌ سادسةٌ (طولُ اللفظ، موقعُه من السطر، جارُه
التالي) **قد تربح ولم تُقَس** — **دَينٌ يُسمّى ولا يُسدّ بهذا التشغيل**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_context_depth_seal import (
    DIGEST,
    ORACLE,
    PREDICTIONS,
    THE_FAMILIES_ARE_FIVE_AND_A_SIXTH_IS_NOT_MEASURED,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "context_depth_run.log"
SEALED = REPOSITORY / "deposits" / "context_ladder_run.log"
LADDER = REPOSITORY / "examples" / "rasm" / "run_context_ladder.py"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
QUESTIONS = 57
WRITTEN_CAP = 12
LIFTED_TO = 100
REACHED = 26
STOPPED_AT = 27
APART = 0
LOWEST = 2.3712
TOTAL_OUT = 0.239608
TOTAL_IN = 0.307338
FIRST_SHARE = 0.2374
SHARE_BEFORE = 0.2686
LAST_GAIN = 0.000100
EXTRA_DEPTHS = 14
EXTRA_OUT = 0.027800
EXTRA_SHARE = 0.1160
ROUNDING = 0.000192
BLOCKS = 567

REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد بالقياس — **ولا واحدَ ههنا**.

فكلُّ شرطٍ **عَدٌّ أو مقدارٌ مطبوع**: عددُ درجاتٍ، وإنتروبيا، وربحٌ، ونصيبٌ.
**ولا تفسيرَ يُحمَل على واحدٍ منها** إلّا ما أُعلِن دَينًا غيرَ مقيس.
"""

CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ذ٩": (
        Fraction(1),
        "نصيبٌ تامٌّ من مجموع الكسب: الكسبُ كلُّه قد يجتمع في الدرجة "
        "الأولى وحدَها — فلا ممتنعَ في المقام، والسقفُ الواحد",
    ),
}
"""**سقفُ كلّ شرطٍ محدود** — العطل ٢٦."""

FORBIDDEN = ("مبنيّ", "معرب", "فتحة", "ضمّة", "كسرة", "حرف جرّ")
DECLARATION = "— ما لا يُدَّعى"


def _text() -> str:
    return LOG.read_text(encoding="utf-8")


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _grab(pattern: str) -> str:
    found = re.search(pattern, _text(), re.M)
    assert found is not None, pattern
    return found.group(1)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def test_the_seal_is_unchanged() -> None:
    """الختمُ كما دُفِع — ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_machine_conditions_hold() -> None:
    """ذ١ وذ٢ وذ٣: المدوّنةُ والألفاظُ والأسئلةُ كما في المسند."""

    text = _text()
    assert f"— الأسطر: {LINES}" in text
    assert f"وعبرَ العدّادات {TOKENS}" in text
    assert f"— الأسئلةُ المتاحة: {QUESTIONS}" in text
    for identifier in ("ذ١", "ذ٢", "ذ٣"):
        assert _one(identifier).verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_first_twelve_reproduce_the_sealed_log_exactly() -> None:
    """ذ٤: صفرُ خلافٍ — فاختيارُ الجشع لا يتعلّق بالسقف، والغلافُ بريء."""

    apart = int(_grab(r"^  درجاتٌ خالفت: (\d+)$"))
    assert apart == APART
    assert _one("ذ٤").verdict(Fraction(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert int(_grab(r"درجاتٌ في السجلّ: (\d+)")) == WRITTEN_CAP
    assert SEALED.is_file()


def test_the_material_ceiling_is_twenty_six_not_twelve() -> None:
    """ذ٥ وذ٦: بُلِغت ٢٦ درجةً، والوقوفُ **بالمادّة** عند ٢٧ لا بنفاد الأسئلة."""

    reached = int(_grab(r"^— الدرجاتُ المبلوغة: (\d+)$"))
    assert reached == REACHED
    assert _one("ذ٥").verdict(Fraction(reached)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ذ٦").verdict(Fraction(reached)) is Verdict.MET  # type: ignore[attr-defined]
    assert int(_grab(r"وسطرُ الوقوف عند الدرجة (\d+)")) == STOPPED_AT
    assert "**فالوقوفُ بالمادّة**" in _text()
    assert reached < QUESTIONS


def test_my_written_cap_was_premature_and_that_was_my_own_claim() -> None:
    """ذ٥ **دعوًى عليّ** — وقد صدقت: السقفُ المكتوبُ كان سابقًا للمادّة."""

    assert "دعوايَ أنّ سقفي عند ١٢ كان **سابقًا للمادّة**" in _one("ذ٥").falsifies  # type: ignore[attr-defined]
    assert f"— السقفُ المكتوبُ في الملفّ: {WRITTEN_CAP}" in _text()
    assert f"ورُفِع في الذاكرة إلى {LIFTED_TO}" in _text()
    assert REACHED > WRITTEN_CAP


def test_the_held_out_floor_and_total_hold_their_bounds() -> None:
    """ذ٧ وذ٨: أدنى محجوزةٍ ٢٫٣٧١٢، ومجموعُ الكسب ٠٫٢٣٩٦٠٨."""

    lowest = float(_grab(r"أدنى إنتروبيا محجوزة: ([\d.]+)"))
    assert lowest == LOWEST
    assert _one("ذ٧").verdict(_exact(lowest)) is Verdict.MET  # type: ignore[attr-defined]
    total = float(_grab(r"مجموعُ الكسب المحجوز \(من سطر السلّم\): \+([\d.]+)"))
    assert total == TOTAL_OUT
    assert _one("ذ٨").verdict(_exact(total)) is Verdict.MET  # type: ignore[attr-defined]
    assert float(_grab(r"مجموعُ الكسب الملحَق \(من سطر السلّم\): \+([\d.]+)")) == TOTAL_IN


def test_the_first_bit_stays_the_largest_after_deepening() -> None:
    """ذ٩: نصيبُها ٠٫٢٣٧٤ بعد التعميق، وكان ٠٫٢٦٨٦ — **فلم تكن وهمَ سقف**."""

    share = float(_grab(r"نصيبُ الدرجة الأولى من المحجوز \(من سطر السلّم\): ([\d.]+)"))
    assert share == FIRST_SHARE
    assert _one("ذ٩").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert share < SHARE_BEFORE
    assert SHARE_BEFORE - share < 0.05


def test_no_reached_depth_lost_and_the_in_sample_never_stalled() -> None:
    """ذ١٠ وذ١١ وذ١٢: لا درجةَ ربحُها ≤ صفر، وآخرُ ربحٍ ٠٫٠٠٠١."""

    zero_out = int(_grab(r"درجاتٌ ربحُها المحجوزُ ≤ صفر: (\d+)"))
    zero_in = int(_grab(r"درجاتٌ ربحُها الملحَقُ ≤ صفر: (\d+)"))
    assert zero_out == 0 and zero_in == 0
    assert _one("ذ١٠").verdict(Fraction(zero_out)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ذ١٢").verdict(Fraction(zero_in)) is Verdict.MET  # type: ignore[attr-defined]
    last = float(_grab(r"ربحُ الدرجة الأخيرة محجوزًا: \+([\d.]+)"))
    assert last == LAST_GAIN
    assert _one("ذ١١").verdict(_exact(last)) is Verdict.MET  # type: ignore[attr-defined]


def test_what_the_written_cap_was_hiding_is_given_as_a_number() -> None:
    """الزائدُ **+٠٫٠٢٧٨ بتًّا** — **٠٫١١٦ من الكسب**، بمقداره لا بوصفه."""

    assert int(_grab(r"درجاتٌ زائدة: (\d+)")) == EXTRA_DEPTHS
    assert float(_grab(r"كسبٌ محجوزٌ زائد: \+([\d.]+)")) == EXTRA_OUT
    assert float(_grab(r"ونصيبُ الزائد من المحجوز: ([\d.]+)")) == EXTRA_SHARE
    assert int(_grab(r"كتلُ آخر درجة: (\d+)")) == BLOCKS
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**فحدِّي كان يكتم نحوَ ثُمنِ ما يفيده السياق**" in text
    assert "**ويُقال بمقداره لا بوصفه.**" in text


def test_the_sum_is_read_from_the_ladder_and_the_rounding_is_named() -> None:
    """المجموعُ من سطر السلّم لا من جمع المطبوع — **والفرقُ تدويرٌ يُعلَن**."""

    rounding = float(_grab(r"فالفرقُ تدويرٌ: ([\d.]+)"))
    assert rounding == ROUNDING
    assert rounding < 0.001
    assert "وبجمع المطبوعِ بأربع منازل" in _text()
    assert __doc__ is not None
    assert "**والفرقُ ٠٫٠٠٠١٩٢ تدويرٌ لا خلاف**" in " ".join(__doc__.split())


def test_the_sealed_script_was_not_edited() -> None:
    """`MOST = 12` كما هو في الملفّ — رُفِع في الذاكرة (العطل ٢٩)."""

    assert f"MOST = {WRITTEN_CAP}" in LADDER.read_text(encoding="utf-8")
    assert "— والملفُّ لم يُحرَّر بحرف (العطل ٢٩)" in _text()
    assert f"— الدرجاتُ المبلوغة: {REACHED}" in _text()


def test_reaching_the_ceiling_is_not_exhausting_the_context() -> None:
    """حدُّ التشغيل في متنه: خمسُ عائلاتٍ، والسادسةُ دَينٌ يُسمّى."""

    text = _text()
    assert DECLARATION in text
    _, _, owned = text.partition(DECLARATION)
    assert "لا يستنفد السياق" in owned
    assert "العائلاتُ خمسٌ" in owned
    assert "لم تُقَس ههنا" in owned
    assert "دَينٌ يُسمّى" in THE_FAMILIES_ARE_FIVE_AND_A_SIXTH_IS_NOT_MEASURED
    for word in FORBIDDEN:
        assert word not in text, word


def test_all_twelve_held_and_the_ceiling_is_declared() -> None:
    """الاثنتا عشرةَ صمدت، وذ٩ محدودةٌ فسقفُها مُصرَّحٌ به (العطل ٢٦)."""

    assert len(PREDICTIONS) == 12
    assert REASONING_NOT_SUPPORTED == ()
    assert set(CEILINGS) == {"ذ٩"}
    ceiling, reason = CEILINGS["ذ٩"]
    assert _one("ذ٩").threshold <= ceiling  # type: ignore[attr-defined]
    assert len(reason) > 40
