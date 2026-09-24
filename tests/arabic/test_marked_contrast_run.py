"""تشغيلُ `6a584a5a…`: شرطان سقطا، وأحدُهما سقط **بعيبٍ في صياغتي لا في المادّة**.

**الحكمُ كما خرج**: ك٣ وك٤ وك٥ تحقّقت، وك١ وك٢ سقطتا.

`THE_CORRECTION_WORKED_AND_THE_GATE_ASKED_THE_WRONG_QUANTITY`: وكتبتُ في
ك١: «**أعلى** مؤشّرِ رَند يبلغه تبديلُ الوسمين ... لا يجاوز ٠٫١٠». فخرج
الأعلى **٠٫٢٩٧٩** فسقط. ثمّ نظرتُ في الصفريّ كلِّه فإذا هو **متمركزٌ عند
الصفر**: متوسّطُه ‎−٠٫٠١٤٢‎ ووسيطُه ‎−٠٫٠٢٢٨‎، ومئينُه الخامسُ والتسعون
**٠٫٠٩٢٨** — أي **دون الحدّ**. فالمقياسُ المُصحَّحُ أدّى ما وُضِع له،
والشرطُ سألَ **أقصى ألفي سحبةٍ** أن يسلك مسلكَ مئين. وأقصى ألفين مرتفعٌ
بالبناء، فالحدُّ كان على كمّيّةٍ غير التي تُقاس.

`AND_THE_FALL_STANDS_AS_WRITTEN`: ومع ذلك **ك١ ساقطٌ ويبقى ساقطًا**: لا
أُعيد تفسيرَ شرطٍ بعد أن رأيتُ رقمَه. والتشخيصُ يُنشَر **وصفًا خارجَ
الختم**، ويُصلَح في ختمٍ رابعٍ يسأل المئينَ لا الأقصى.

`THE_SECOND_FELL_HONESTLY`: وأمّا ك٢ فسقط سقوطًا نظيفًا: كتبتُ ٠٫٣٥ على
مقياسٍ **لم يُحسَب بعد**، فخرج التكرارُ على النصف المحجوب **٠٫٢٨٥٣**. فهو
دون الحدّ بلا تأويل — وذلك ثمنُ أن يُكتَب الحدُّ قبل النظر.

`ONE_JUNCTION_LIES_ON_THE_CUT_AND_BELONGS_TO_NEITHER_HALF`: ومقامُ النصفين
١٦٬٩٥٦ و١٠٬٤٢٥ = ٢٧٬٣٨١، والكلُّ ٢٧٬٣٨٢. فموضعٌ واحدٌ يقع **على القطع**:
نونٌ آخرَ النصف الأوّل يليها حرفُ النصف الثاني. لا يملكه نصفٌ منهما فيضيع
بالقسمة. وواحدٌ من سبعةٍ وعشرين ألفًا لا يبدّل حكمًا، **ويُعلَن مع ذلك**:
فالمقامُ الذي لا يُجمَع يُسأل عنه قبل أن يُسأل عن الرقم.

`THE_TWO_PANS_ARE_NOT_COMPARABLE_TO_خ١_AND_THAT_IS_DECLARED`: وكفّةُ الرسم
ههنا **٠٫٠٥١٨**، وكانت في خ١ **٠٫٠٢٦٠**. وليس أحدهما تحسينًا للآخر: هذا
يعُدّ الجوارَ **عابرًا حدَّ الكلمة** (كما يقتضي ملتقى النون)، وذاك يعُدُّه
**داخلَ الكلمة**. فمقياسان لا مقياس، ولم يُسمِّ الختمُ أيَّهما — فيُعلَن
ههنا ولا يُطوى.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus

from algebra.signified import Verdict

REPOSITORY = Path(__file__).resolve().parents[2]

pytestmark = requires_corpus

MARKED_SEAL = "6a584a5a1254329445f8a8c5dcc5b52303155fe9c13cafb9dd844a3abf36c1d3"

NUN_SITES, MARKED, UNMARKED = 27_382, 1_716, 25_666
HALVES = (16_956, 10_425)

NULL_HIGHEST = Fraction(2_979, 10_000)
NULL_MEAN = Fraction(-142, 10_000)
NULL_MEDIAN = Fraction(-228, 10_000)
NULL_P95 = Fraction(928, 10_000)
OBSERVED_WHOLE = Fraction(2_474, 10_000)
OBSERVED_P = Fraction(3, 2_000)

HELD_OUT = Fraction(2_853, 10_000)
BARE_PAN, MARKED_PAN = Fraction(518, 10_000), Fraction(1_133, 10_000)
BARE_PAN_IN_خ١ = Fraction(260, 10_000)


def _prediction(identifier: str):
    import importlib.util
    import sys

    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    name = "test_marked_contrast_preregistration"
    spec = importlib.util.spec_from_file_location(name, path / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    for one in module.PREDICTIONS:
        if one.identifier.startswith(identifier):
            return one
    raise AssertionError(identifier)


def test_the_first_condition_fell_as_written() -> None:
    """٠٫٢٩٧٩ فوق ٠٫١٠ «لا يجاوز» — فساقطٌ، ولا يُعاد تفسيرُه بعد رؤيته."""

    first = _prediction("ك١")
    assert first.verdict(NULL_HIGHEST) is Verdict.FALSIFIED
    assert first.threshold == Fraction(10, 100)


def test_the_null_is_centred_at_zero_so_the_correction_did_its_work() -> None:
    """متوسّطُ الصفريّ ‎−٠٫٠١٤٢‎ ووسيطُه ‎−٠٫٠٢٢٨‎: التردُّدُ سقط من الطرفين."""

    assert NULL_MEAN < 0 and NULL_MEDIAN < 0
    assert abs(NULL_MEAN) < Fraction(2, 100)
    # وهذا ما كان يُرجى من التصحيح، وقد وقع
    assert NULL_MEAN < NULL_P95 < NULL_HIGHEST


def test_the_gate_asked_a_maximum_to_behave_like_a_quantile() -> None:
    """المئينُ الخامسُ والتسعون ٠٫٠٩٢٨ **دون الحدّ**، والأقصى فوقَه بثلاثة أضعاف."""

    gate = _prediction("ك١")
    assert gate.verdict(NULL_P95) is Verdict.MET  # لو سُئِل المئين
    assert gate.verdict(NULL_HIGHEST) is Verdict.FALSIFIED  # وقد سُئِل الأقصى
    assert NULL_HIGHEST / NULL_P95 > 3

    # والعيبُ في الصياغة لا في المادّة، ويُنشَر وصفًا لا إعادةَ تفسير
    assert "أعلى" in gate.statistic


def test_the_observed_is_far_beyond_the_null_and_that_is_a_description() -> None:
    """المرصودُ ٠٫٢٤٧٤ وبلغه اثنان من ألفين: `p = 0.0015` — وصفٌ خارجَ الختم."""

    assert OBSERVED_WHOLE > NULL_P95
    assert OBSERVED_P < Fraction(5, 1_000)
    assert OBSERVED_P == Fraction(3, 2_000)
    # ولا يُقرَأ هذا تحقّقًا لك١: الشرطُ سألَ غيرَه
    assert _prediction("ك١").verdict(NULL_HIGHEST) is not Verdict.MET


def test_the_second_condition_fell_cleanly_on_an_unseen_measure() -> None:
    """٠٫٢٨٥٣ دون ٠٫٣٥ المكتوبة قبل النظر — سقوطٌ بلا تأويل."""

    second = _prediction("ك٢")
    assert second.verdict(HELD_OUT) is Verdict.FALSIFIED
    assert HELD_OUT < second.threshold == Fraction(35, 100)
    assert min(HALVES) > 200  # فالمقامُ ليس علّةَ السقوط


def test_the_three_met_conditions_are_met_on_their_own_numbers() -> None:
    """ك٣ ثلاثُ مجموعات، وك٤ كفّتان منشورتان، وك٥ أقلُّ كفّةٍ فوق المئتين."""

    assert _prediction("ك٣").verdict(Fraction(3)) is Verdict.MET
    assert _prediction("ك٤").verdict(Fraction(2)) is Verdict.MET
    assert _prediction("ك٥").verdict(Fraction(332_836)) is Verdict.MET
    assert NUN_SITES == MARKED + UNMARKED
    # وموضعٌ واحدٌ يقع **على القطع**: نونٌ آخرَ النصف الأوّل يليها حرفُ
    # النصف الثاني. فلا يملكه نصفٌ منهما، ويضيع بالقسمة — ويُعلَن ولا يُطوى.
    assert sum(HALVES) == NUN_SITES - 1


def test_the_bare_pan_here_is_not_the_bare_pan_of_the_first_seal() -> None:
    """٠٫٠٥١٨ ههنا و٠٫٠٢٦٠ هناك: جوارٌ عابرُ الكلمة مقابلَ جوارٍ داخلَها."""

    assert BARE_PAN != BARE_PAN_IN_خ١
    assert BARE_PAN > BARE_PAN_IN_خ١
    # وليس تحسينًا: مقياسان لا مقياس، والختمُ لم يُسمِّ أيَّهما
    definitions = ("الجوارُ عابرًا حدَّ الكلمة", "الجوارُ داخلَ الكلمة")
    assert len(set(definitions)) == 2

    # وكفّةُ الضبط أعلى من كفّة الرسم، وكلتاهما منشورتان معًا بنصّ ك٤
    assert MARKED_PAN > BARE_PAN
    assert len(MARKED_SEAL) == 64
