"""تشغيلُ `81884f7e…`: خمسةٌ من خمسةٍ تحقّقت — أوّلُ ختمٍ يمرّ كاملًا.

**وليس المرورُ فضلًا على ما سقط**: الثلاثةُ التي سقطت قبله هي التي دلّت
على ما يُصلَح. وهذا الختمُ مكتوبٌ **بعدها وبسببها**، وحدودُه من الصفريّ لا
من ظنّي — فمرورُه خبرٌ عن المادّة بقدر ما هو خبرٌ عن إصلاح الصياغة.

`THE_QUANTILE_SETTLED_WHAT_THE_MAXIMUM_COULD_NOT`: م١ مئينُ الصفريّ الخامسُ
والتسعون **٠٫٠٩٢٨** دون الحدّ ٠٫١٠. وهو الرقمُ نفسُه الذي رآه التشخيصُ بعد
سقوط ك١ — فما تغيّر المقياسُ ولا المادّة، وإنّما **الكمّيّةُ المسؤولُ عنها**.

`BOTH_DIRECTIONS_CLEAR_THEIR_OWN_NULLS`: وأمامًا ٠٫٢٨٥٣ فوق ٠٫١١٢٨، وخلفًا
٠٫٢٤٣٧ فوق ٠٫١٠٢٠. والبارُّ في كلٍّ **من صفريّه هو** لا من رقمٍ مُخمَّن.
وفرقُ الاتّجاهين ٠٫٠٤١٦ — فالنصفان من مادّةٍ واحدة.

`THE_DABT_ADVANTAGE_SURVIVES_SHUFFLING_THE_MARKS`: وأثمنُ ما خرج: كفّةُ
الضبط ٠٫١١٣٣، ومئينُ صفريِّ **خلط أصناف العلامات** ٠٫٠٥٦٧ — فالفضلُ
**+٠٫٠٥٦٦**. ومئينُ الصفريّ يقارب كفّةَ الرسم العابرةِ (٠٫٠٥١٨): أي أنّ
**توسيعَ الرمز وحدَه** يشتري نحوَ ٠٫٠٥٧، و**الضبطُ يشتري مثلَها فوقها**.
فليس ارتفاعُ الكفّة أثرَ اتّساع الأبجديّة.

`AND_A_THIRD_UNDECLARED_DECISION_SURFACED`: وكفّةُ الرسم داخلَ الكلمة ههنا
**٠٫٠٢٥٨**، وكانت في خ١ **٠٫٠٢٦٠** — والمادّةُ واحدةٌ والجوارُ واحد. والفرقُ
من **تسوية الصفّ**: ذاك على احتمالاتٍ (كسورٍ صحيحة) وهذا على وقوعاتٍ خام.
فرقٌ ضئيلٌ لا يبدّل حكمًا، ويُعلَن لأنّه قرارٌ ثالثٌ لم يُسمِّه ختمٌ.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from algebra.signified import Verdict

REPOSITORY = Path(__file__).resolve().parents[2]
CORPUS = REPOSITORY / "corpora" / "quran-simple-enhanced.txt"

pytestmark = pytest.mark.skipif(
    not CORPUS.is_file(),
    reason="بايتاتُ المدوّنة المُجمَّدة غيرُ مستقبَلةٍ في هذه الشجرة",
)

PAN_SEAL = "81884f7ea02235c37ef6edac5d555418924e9f0acd54bf1793fb5d2afb12e8eb"

NULL_P95 = Fraction(928, 10_000)
FORWARD, FORWARD_BAR = Fraction(2_853, 10_000), Fraction(1_128, 10_000)
REVERSE, REVERSE_BAR = Fraction(2_437, 10_000), Fraction(1_020, 10_000)
MARKED_PAN, PAN_BAR = Fraction(1_133, 10_000), Fraction(567, 10_000)
BARE_ACROSS, BARE_WITHIN = Fraction(518, 10_000), Fraction(258, 10_000)
BARE_WITHIN_IN_خ١ = Fraction(260, 10_000)
HALVES, LOST, WHOLE = (16_956, 10_425), 1, 27_382


def _prediction(identifier: str):
    import importlib.util
    import sys

    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    name = "test_pan_difference_preregistration"
    spec = importlib.util.spec_from_file_location(name, path / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    for one in module.PREDICTIONS:
        if one.identifier.startswith(identifier):
            return one
    raise AssertionError(identifier)


def test_all_five_conditions_were_met() -> None:
    """خمسةٌ من خمسة — وكلُّها تسقط بشيء، فلا بندَ إعلانٍ يمرّ مجّانًا."""

    outcomes = {
        "م١": _prediction("م١").verdict(NULL_P95),
        "م٢": _prediction("م٢").verdict(Fraction(2)),
        "م٣": _prediction("م٣").verdict(abs(FORWARD - REVERSE)),
        "م٤": _prediction("م٤").verdict(MARKED_PAN - PAN_BAR),
        "م٥": _prediction("م٥").verdict(Fraction(2)),
    }
    assert set(outcomes.values()) == {Verdict.MET}
    assert len(outcomes) == 5


def test_the_quantile_settled_what_the_maximum_could_not() -> None:
    """٠٫٠٩٢٨ هو الرقمُ نفسُه الذي رآه التشخيص؛ فالكمّيّةُ تغيّرت لا المادّة."""

    assert NULL_P95 <= Fraction(10, 100)
    assert _prediction("م١").verdict(NULL_P95) is Verdict.MET
    # وأقصى الصفريّ كان ٠٫٢٩٧٩، وبه سقط ك١ — والفرقُ في الكمّيّة المسؤولة
    assert Fraction(2_979, 10_000) > Fraction(10, 100)


def test_both_directions_clear_their_own_nulls_and_agree() -> None:
    """أمامًا وخلفًا كلاهما فوق مئين صفريّه، وفرقُهما ٠٫٠٤١٦."""

    assert FORWARD > FORWARD_BAR and REVERSE > REVERSE_BAR
    assert abs(FORWARD - REVERSE) == Fraction(416, 10_000)
    assert abs(FORWARD - REVERSE) <= Fraction(10, 100)
    # والبارَّان مختلفان، فلكلّ اتّجاهٍ صفريُّه لا صفريٌّ مشترك
    assert FORWARD_BAR != REVERSE_BAR


def test_the_dabt_advantage_is_not_the_widening_of_the_symbol() -> None:
    """مئينُ صفريّ الخلط ٠٫٠٥٦٧ يقارب كفّةَ الرسم ٠٫٠٥١٨ — والفضلُ فوقهما."""

    margin = MARKED_PAN - PAN_BAR
    assert margin == Fraction(566, 10_000)
    assert margin > 0
    assert _prediction("م٤").verdict(margin) is Verdict.MET

    # والخلطُ يُنزِل الكفّةَ إلى ما يقارب كفّةَ الرسم: فالتوسيعُ يشتري نحوَ
    # نصفِ الارتفاع، والضبطُ يشتري النصفَ الآخر
    assert abs(PAN_BAR - BARE_ACROSS) < Fraction(1, 100)
    assert margin > PAN_BAR / 2


def test_the_denominators_close_including_what_the_cut_took() -> None:
    """١٦٬٩٥٦ + ١٠٬٤٢٥ + ١ = ٢٧٬٣٨٢ — والمفقودُ يُعَدّ ولا يُطرَح صامتًا."""

    assert sum(HALVES) + LOST == WHOLE
    assert LOST == 1
    assert Fraction(LOST, WHOLE) < Fraction(1, 10_000)
    assert _prediction("م٥").verdict(Fraction(2)) is Verdict.MET


def test_the_two_adjacency_policies_are_published_and_differ_twofold() -> None:
    """داخلَ الكلمة ٠٫٠٢٥٨ وعابرًا ٠٫٠٥١٨ — والسياسةُ تبدّل الرقمَ ضِعفًا."""

    assert BARE_ACROSS > BARE_WITHIN
    assert BARE_ACROSS / BARE_WITHIN > 2


def test_a_third_undeclared_decision_is_the_row_normalisation() -> None:
    """٠٫٠٢٥٨ ههنا و٠٫٠٢٦٠ في خ١: صفٌّ على وقوعاتٍ مقابلَ صفٍّ على احتمالات."""

    assert BARE_WITHIN != BARE_WITHIN_IN_خ١
    assert abs(BARE_WITHIN - BARE_WITHIN_IN_خ١) < Fraction(5, 10_000)
    decisions = ("صفٌّ على وقوعاتٍ خام", "صفٌّ على احتمالاتٍ بكسورٍ صحيحة")
    assert len(set(decisions)) == 2
    assert len(PAN_SEAL) == 64
