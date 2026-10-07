"""شُغِّل: **الوحدةُ تحمل الأثرَ في ٠٫٧٣٤٠ — وسقط شرطان، وأحدُهما يصحّح دعوًى**.

**الحصاد**: عشرٌ من اثنتي عشرةَ صمدت، و**اثنتان سقطتا** — غ٩ وغ١٢.

`THE_UNIT_CARRIES_MORE_THAN_I_CLAIMED`: حاملُ الأثر `{064E, 064B}`
**٤٤٧ من ٦٠٩ = ٠٫٧٣٤٠**، والحدُّ المختومُ ٠٫٤٠. **فالوحدةُ تحمل الأثرَ في
ثلاثة أرباع المواضع** لا في خُمسَيها.

`AND_THE_ESCAPE_I_WAS_TOLD_TO_EXPECT_IS_NEARLY_ABSENT`: **وسقطت غ٩**:
قدَّرتُ `064B` بنصفِ عُشرِ المواضع فأكثر، **فكانت ٣ من ٦٠٩ = ٠٫٠٠٤٩**.
وهذا **يصحّح موضعَ الخسارة**: قيل إنّ جزءًا من الأثر يقع حيث يُكتَب
التنوينُ على الألف فيعرى الحرفُ قبله. **والمقيسُ يقول إنّ ذلك المسلكَ
يكاد لا يوجد بعد هذا الشكل** — التاليُ ههنا معرَّفٌ في أكثره، فلا تنوينَ
فيه أصلًا.

`AND_THE_LOSS_IS_ELSEWHERE_AND_IT_IS_COUNTED`: **والخسارةُ في العُري**:
**١٢٧ = ٠٫٢٠٨٥**. وتفكيكُه بهياكله يقول أين:
`0641 064A` **٥٦** (٤٤٪ من العُري)، و`0647 0630 0627` **٢١**،
و`0631 0628 064A` **١٣** — **وأكثرُ اثنين منه ٠٫٦٠٦٣**.

`AND_ONE_PREMISE_IS_REFUTED_AT_THE_BYTE`: **وأدقُّ ما أخرجه العدُّ**: قيل
إنّ الوحدةَ في «إنّ الذين» **لا تحمل أثرًا أصلًا** لأنّ الآخرَ لا يتغيّر.
**والبايتُ يخالف**: الهيكلُ `0627 0644 0630 064A 0646` وقع **٨٤ مرّةً في
نِصب الحامل** — أي أنّ المجمَّدَ **يكتب `064E` على آخره**. فالوحدةُ
**تحمل علامةً**؛ وما لا تحمله **الفرقُ بين كونها أثرَ عاملٍ وكونها من
بناء اللفظ**. **وذلك فرقٌ في التأويل لا في الوجود** — والبتّاتُ ترى
العلامةَ ولا ترى ذلك الفرق.

`AND_THE_FRONTED_CASE_IS_THE_LARGEST_SINGLE_LOSS`: و`0641 064A` **٥٦
موضعًا** أكبرُ مفردٍ في العُري. **وهو الموضعُ الذي قيل إنّ الترتيبَ يحدّده**
— وقد أُعلِن قبل النظر أنّ تعيينَ الدور **فوق هذا القياس**، فيُعَدّ ههنا
ولا يُفرَز. **فالحدُّ المكتوبُ قبل العدّ هو الذي احتواه، لا تفسيرٌ بعده.**

`AND_THE_SECOND_FALL_NARROWS_MY_OWN_CLAIM`: **وسقطت غ١٢**: قدَّرتُ
هياكلَ التالي بمئتين فأكثر، **فكانت ١٣١**. وأكثرُ اثنين من الحامل
**٠٫٦٤٦٥** — `0627 0644 0644 0647` وحدَه **٢٠٥ من ٦٠٩ = ٠٫٣٣٦٦**.
**فثلثُ المقيس لفظٌ واحد**، والقياسُ **أضيقُ ممّا ادّعيت**. وشرطي هو الذي
كشف ذلك، لا قارئٌ بعدي.

**وما لا يُدَّعى**: العُريُ **خليطٌ `UNCLASSIFIED`** يُعَدّ ولا يُفرَز؛
وشكلٌ واحدٌ **لا يُعمَّم**؛ و**تعيينُ الدور فوق هذا القياس**. ولا يُقال
«هكذا الإعرابُ في العربيّة» — يُقال: **هذا ما تحمله الوحدةُ بعد هذا الشكل
في هذا المجمَّد**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_nasib_particle_seal import (
    DIGEST,
    ONE_PARTICLE_IS_NOT_A_LANGUAGE,
    ORACLE,
    PREDICTIONS,
    THE_BARE_BUCKET_IS_A_MIXTURE,
    THE_ORDER_IS_ABOVE_THIS_MEASUREMENT,
)

from algebra.results import Vacancy
from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "nasib_particle_run.log"
LADDER = REPOSITORY / "deposits" / "context_ladder_run.log"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
HERE = 609
ALONE = 0
MEASURED = 609
DOUBLED = 0
CARRIED = 447
OTHER = 35
BARE = 127
FATHA = 444
TANWEEN = 3
KASRA = 14
SUKUN = 12
DAMMA = 9
CARRIED_SHARE = 0.7340
FATHA_SHARE = 0.7291
TANWEEN_SHARE = 0.0049
BARE_SHARE = 0.2085
DAMMA_SHARE = 0.0148
CORPUS_BARE = 0.3108
GAP = -0.1023
SHAPES = 131
CARRIED_TOP_TWO = 0.6465
BARE_TOP_TWO = 0.6063
ALLAH = 205
ALLADHEEN = 84
FEE = 56

FELL = ("غ٩", "غ١٢")
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد بالقياس — **ولا واحدَ ههنا**.

فكلُّ ما مرَّ **عَدٌّ أو نصيبٌ مطبوعٌ في السجلّ**، وكلُّ تفكيكٍ يُروى في
هذا الشرح **له صفٌّ في السجلّ بهياكله**.
"""

CEILINGS: dict[str, tuple[Fraction, str]] = {
    "غ٧": (
        Fraction(1),
        "نصيبٌ تامٌّ من الوقوعات التي لها تالٍ: كلُّها قد تكون في نِصب "
        "الحامل — فلا ممتنعَ في المقام، والسقفُ الواحد",
    ),
    "غ٨": (
        Fraction(1),
        "وكذلك `064E` وحدَها: كلُّ التالي قد يحمل `064E` — فلا ممتنعَ، " "والسقفُ الواحد",
    ),
    "غ٩": (
        Fraction(1),
        "وكذلك `064B` وحدَها: لا يمنع بناءٌ أن يحملها كلُّ التالي — "
        "**والسقفُ الواحد، والشرطُ سقط دونه بمقيسه لا بامتناعه**",
    ),
}
"""**سقفُ كلّ شرطٍ محدود** — العطل ٢٦."""

FORBIDDEN = ("مبنيّ", "معرب", "فتحة", "ضمّة", "كسرة", "فاعل", "مبتدأ", "خبر")
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
    """غ١ وغ٢ وغ٣: المدوّنةُ والألفاظُ، والشكلُ واحدٌ بالشدّة لا شكلان."""

    assert int(_grab(r"^— الأسطر: (\d+) \|")) == LINES
    assert int(_grab(r"الألفاظ: (\d+)$")) == TOKENS
    doubled = int(_grab(r"أشكالٌ فيها 0651 وليست المقصودَ: (\d+)"))
    assert doubled == DOUBLED
    for identifier in ("غ١", "غ٢"):
        assert _one(identifier).verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("غ٣").verdict(Fraction(doubled)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_support_holds_its_two_bounds_and_closes_its_count() -> None:
    """غ٤ وغ٥ وغ٦: ٦٠٩ وقوعًا، كلُّها لها تالٍ — والعدُّ يُغلِق."""

    here = int(_grab(r"^— وقوعاتُ الشكل: (\d+)$"))
    alone = int(_grab(r"منها بلا تالٍ في سطرها: (\d+)"))
    measured = int(_grab(r"ولها تالٍ: (\d+)"))
    assert (here, alone, measured) == (HERE, ALONE, MEASURED)
    assert here == alone + measured
    assert _one("غ٤").verdict(Fraction(here)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("غ٥").verdict(Fraction(here)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("غ٦").verdict(Fraction(alone)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_three_buckets_close_on_one() -> None:
    """النِّصَبُ الثلاثةُ تجمع الواحدَ بالضبط — قيدُ بناءٍ لا دعوى."""

    carried = int(_grab(r"حاملٌ للأثر \{064E, 064B\}: (\d+)"))
    other = int(_grab(r"حالٌ Mn غيرُهما: (\d+)"))
    bare = int(_grab(r"عارٍ ·: (\d+)"))
    assert (carried, other, bare) == (CARRIED, OTHER, BARE)
    assert carried + other + bare == MEASURED
    assert _text().count("ومجموعُ النصيب: 1.000000") == 1


def test_the_unit_carries_the_effect_above_my_threshold_by_a_named_factor() -> None:
    """غ٧ وغ٨: الحاملُ ٠٫٧٣٤٠ والحدُّ ٠٫٤٠ — **بمعامل ١٫٨٣٥×، لا ضعفين**.

    وكتبتُ أوّلًا `carried > 2 * threshold` فسقط الفحصُ عليّ: ٠٫٧٣٤ ليست
    فوق ٠٫٨. **فالمعاملُ يُسمّى بمقداره** ولا يُقال «أضعافًا».
    """

    carried = float(_grab(r"حاملٌ للأثر \{064E, 064B\}: \d+ \| نصيبٌ ([\d.]+)"))
    assert carried == CARRIED_SHARE
    assert _one("غ٧").verdict(_exact(carried)) is Verdict.MET  # type: ignore[attr-defined]
    fatha = float(_grab(r"^  064E: (?:\d+) \| نصيبٌ ([\d.]+)$"))
    assert fatha == FATHA_SHARE
    assert _one("غ٨").verdict(_exact(fatha)) is Verdict.MET  # type: ignore[attr-defined]
    factor = carried / float(_one("غ٧").threshold)  # type: ignore[attr-defined]
    assert abs(factor - 1.835) < 0.001, factor


def test_the_tanween_condition_fell_and_its_falsification_is_quoted() -> None:
    """غ٩ سقطت: ٠٫٠٠٤٩ والحدُّ ٠٫٠٥ — ويُقتبَس نصُّ ما عُلِّق على سقوطها."""

    tanween = float(_grab(r"^  064B: (?:\d+) \| نصيبٌ ([\d.]+)$"))
    assert tanween == TANWEEN_SHARE
    assert _one("غ٩").verdict(_exact(tanween)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert "تنوينُ الفتح قليلٌ ههنا" in _one("غ٩").falsifies  # type: ignore[attr-defined]
    assert int(_grab(r"^  064B: (\d+) \|")) == TANWEEN
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**وسقطت غ٩**" in text
    assert "**والمقيسُ يقول إنّ ذلك المسلكَ يكاد لا يوجد بعد هذا الشكل**" in text


def test_the_breadth_condition_fell_and_narrows_my_own_claim() -> None:
    """غ١٢ سقطت: ١٣١ هيكلًا والحدُّ ٢٠٠ — **وثلثُ المقيس لفظٌ واحد**."""

    shapes = int(_grab(r"^— هياكلُ التالي المتمايزة: (\d+)$"))
    assert shapes == SHAPES
    assert _one("غ١٢").verdict(Fraction(shapes)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert "لا عامٌّ في المسند" in _one("غ١٢").falsifies  # type: ignore[attr-defined]
    assert f"0627 0644 0644 0647: {ALLAH}" in _text()
    assert abs(ALLAH / MEASURED - 0.3366) < 0.0001
    assert float(_grab(r"ونصيبُ أكثرِ اثنين من هذا النِّصب: ([\d.]+)")) == CARRIED_TOP_TWO


def test_the_bare_share_is_below_the_corpus_and_the_gap_is_printed() -> None:
    """غ١٠ وغ١١: العُريُ ٠٫٢٠٨٥ دون ٠٫٣١٠٨، و`064F` ٠٫٠١٤٨."""

    bare = float(_grab(r"وعُريُ التالي ههنا: ([\d.]+)"))
    assert bare == BARE_SHARE
    assert _one("غ١٠").verdict(_exact(bare)) is Verdict.MET  # type: ignore[attr-defined]
    damma = float(_grab(r"^  064F: (?:\d+) \| نصيبٌ ([\d.]+)$"))
    assert damma == DAMMA_SHARE
    assert _one("غ١١").verdict(_exact(damma)) is Verdict.MET  # type: ignore[attr-defined]
    assert float(_grab(r"فالفرقُ: ([+-][\d.]+)")) == GAP
    assert f"{CORPUS_BARE:.4f}" in LADDER.read_text(encoding="utf-8")


def test_the_indeclinable_carries_a_mark_in_the_bytes() -> None:
    """`0627 0644 0630 064A 0646` في نِصب الحامل ٨٤ مرّةً — **والوحدةُ تحمل**.

    وهذا يصحّح دعوًى: قيل إنّ الوحدةَ **لا تحمل أثرًا أصلًا** ثمّة.
    **والبايتُ يكتب `064E` على آخره.** فما لا تحمله الوحدةُ **الفرقُ** بين
    أن تكون العلامةُ أثرَ عاملٍ وأن تكون من بناء اللفظ — **لا العلامةُ**.
    """

    body = _text().split("تفكيكُ كلّ نِصبٍ بهياكله")[1].split("— هياكلُ")[0]
    carried = body.split("حامل (")[1].split("عارٍ (")[0]
    assert f"0627 0644 0630 064A 0646: {ALLADHEEN}" in carried
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**والبايتُ يخالف**" in text
    assert "**وذلك فرقٌ في التأويل لا في الوجود**" in text


def test_the_largest_single_loss_is_the_one_the_order_explains() -> None:
    """`0641 064A` ٥٦ موضعًا أكبرُ مفردٍ في العُري — والحدُّ احتواه قبل النظر."""

    body = _text().split("تفكيكُ كلّ نِصبٍ بهياكله")[1]
    bare = body.split("عارٍ (")[1]
    assert f"0641 064A: {FEE}" in bare
    assert float(bare.split("ونصيبُ أكثرِ اثنين من هذا النِّصب: ")[1][:6]) == BARE_TOP_TWO
    assert "في مستوى التركيب" in THE_ORDER_IS_ABOVE_THIS_MEASUREMENT
    assert "ولا يُفرَز" in THE_ORDER_IS_ABOVE_THIS_MEASUREMENT


def test_the_bare_bucket_is_classified_not_explained() -> None:
    """العُريُ `UNCLASSIFIED` — ١٢٧ موضعًا يُعَدّ ولا يُفرَز."""

    assert THE_BARE_BUCKET_IS_A_MIXTURE is Vacancy.UNCLASSIFIED
    text = _text()
    assert DECLARATION in text
    _, _, owned = text.partition(DECLARATION)
    assert f"العُريُ خليطٌ UNCLASSIFIED: {BARE} موضعًا" in owned
    assert "يُعَدّ ولا يُفرَز" in owned
    assert "جردًا مُودَعًا" in owned


def test_the_log_names_no_ruling_and_declares_its_limits() -> None:
    """لا اسمَ بابٍ في المتن المقيس، والحدّان مكتوبان بعد الإعلان."""

    text = _text()
    body, _, owned = text.partition(DECLARATION)
    for word in FORBIDDEN:
        assert word not in body, word
    assert "لا يُعمَّم" in owned
    assert "ولا يُقال «هكذا الإعراب»" in owned
    assert "لا يُعمَّم" in ONE_PARTICLE_IS_NOT_A_LANGUAGE


def test_ten_held_and_two_fell_and_the_ceilings_are_declared() -> None:
    """عشرٌ صمدت واثنتان سقطتا، ولكلّ شرطٍ محدودٍ سقفٌ مُصرَّحٌ به."""

    assert len(PREDICTIONS) == 12
    assert FELL == ("غ٩", "غ١٢")
    assert REASONING_NOT_SUPPORTED == ()
    assert set(CEILINGS) == {"غ٧", "غ٨", "غ٩"}
    for identifier, (ceiling, why) in CEILINGS.items():
        assert _one(identifier).threshold <= ceiling  # type: ignore[attr-defined]
        assert len(why) >= 25
    assert __doc__ is not None
    assert "**اثنتان سقطتا**" in " ".join(__doc__.split())
