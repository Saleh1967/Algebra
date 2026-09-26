"""حُكمُ ختم `0410f435…`: **إحدى عشرةَ صمدت، وواحدةٌ سقطت — وهي دعوايَ**.

`THE_MARK_IS_MOSTLY_IN_THE_WORD_ITSELF`: صورةُ اللفظ منقوصةَ علامتِه
الأخيرة تحمل عن تلك العلامة **`+١٫٢١٥٢٥٢` بتًّا محجوزًا** — **٥٫٧٣ ضِعفَ**
كسبِ سلّم السياق كلِّه (`+٠٫٢١١٩٦٣`)، و**٠٫٤٦٥٥** من الحقل. **فالعلامةُ
الأخيرةُ في أكثرها من بنية اللفظ لا من جواره.**

`AND_MY_CLAIM_THAT_THE_NEIGHBOUR_ADDS_SOMETHING_FELL`: زعمتُ (ص١٠) أنّ
الجارَ **يزيد شيئًا بعد معرفة الصورة** محجوزًا. **فجاء سالبًا**:
`−٠٫٢٩٠٠٤٩`.

`BUT_THE_FALL_DOES_NOT_LICENSE_THE_OPPOSITE_READING`: **ولا يُقرَأ ذلك
«الجارُ لا يحمل شيئًا»**. السالبُ يعني أنّ التقديرَ المحجوزَ **ساء** حين
اتّسع الفضاء من `١٦٬٢٤٤` خانةً إلى `٢٤٬٠٦٧` — **وهو عقابُ السَّعة لا
عدمُ الخبر**. والملحَقُ — وهو **حدٌّ أعلى** مُسمًّى منتفخًا قبل النظر —
يعطي `+٠٫١٠٣٦٦٢`. **فالحقُّ محصورٌ بين سالبٍ مُضلَّلٍ بالسَّعة وموجبٍ
منتفخٍ**، والسؤالُ **لم يُحسَم بهذا المقدِّر**: خلوٌّ يُصنَّف
`UNCLASSIFIED` لا نتيجةُ صفر.

`WHAT_THE_BRACKET_DOES_GIVE_IS_A_CEILING`: وأمّا **السقفُ** فيُقرَأ:
حتّى بالتقدير المنتفخ، ما يزيده الجارُ بعد الصورة **`+٠٫١٠٣٦٦٢`** — أي
**دون نصف** كسبِ السلّم وحدَه، و**٠٫٠٣٩٧** من الحقل. **فأكثرُ نصفِ ما
قِيس للجار في `041cdcf4…` هو بنيةُ اللفظ نفسِها**، وما يبقى لأيّ قراءةٍ
تركيبيّة **أربعةٌ من مئةٍ من الحقل فأقلّ**.

`AND_THE_OPAQUE_BOX_IS_NAMED_BY_ITS_PARTS`: وخانةُ «بلا علامة» — أكبرُ
الخانات — **شُقِّقت بحرف خاتمتها**: عشرون قسمًا، وحروفُ المدّ الثلاثةُ
المختومةُ `٠٫٦٩٦١٢٢` منها. **فصارت الفجوةُ مُسمّاةً بأقسامها.**

`AND_NOTHING_HERE_NAMES_A_CHAPTER`: ولا يُسمّى بابٌ ولا حكم. **المقيسُ
مقدارٌ، والتسميةُ فعلُ صاحب المستودع.**
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_morph_residue_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.results import Vacancy
from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "morph_residue_run.log"
LADDER = REPOSITORY / "deposits" / "context_ladder_run.log"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
FIELD = 2.6106
SHAPES = 16_244
BONES = 14_871
NEARS = 9
TOGETHER = 24_067
SHAPE_OUT = 1.215252
BONE_OUT = 1.213593
NEAR_OUT = 0.069522
ADDED_OUT = -0.290049
ADDED_IN = 0.103662
LADDER_GAIN = 0.211963
STRETCH = 0.696122
PARTS = 20
SLACK = -29.710188

# **شرطٌ مرَّ بتعليلٍ لم يؤيِّده القياس**: ص١١ يوجب أن يكون ما بقي للجار
# دون نصفِ ما كان له وحدَه — **ومرَّ لأنّ البسطَ صار سالبًا**، لا لأنّ
# النسبةَ قِيست موجبةً صغيرة. **فمرورُه صحيحٌ وتعليلي غيرُ مؤيَّد.**
REASONING_NOT_SUPPORTED = ("ص١١",)

# **والسؤالُ الذي سقط لا يُصفَّر**: خلوٌّ مُصنَّفٌ لأنّ المقدِّر لم يحسمه
THE_NEIGHBOUR_BEYOND_THE_FORM = Vacancy.UNCLASSIFIED

FORBIDDEN = (
    "ARABIC",
    "فتحة",
    "ضمّة",
    "كسرة",
    "سكون",
    "تنوين",
    "إعراب",
    "مرفوع",
    "منصوب",
    "مجرور",
    "صرفيّ",
    "مبتدأ",
)
DECLARATION = "— ما لا يدخل هذا السجلّ"


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def _row(name: str) -> tuple[int, float, float]:
    """(قيمُ المتغيّر، ملحَقةٌ، محجوزة) من جدول الإنتروبيا الشرطيّة."""

    ((cells, inside, outside),) = re.findall(
        rf"^  {re.escape(name)} \| (\d+) \| ([0-9.]+) \| ([0-9.]+)$",
        LOG.read_text(encoding="utf-8"),
        re.M,
    )
    return int(cells), float(inside), float(outside)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("0410f435")


def test_the_corpus_and_the_single_support_are_what_was_sealed() -> None:
    """ص١ وص٢: الأسطرُ ٦٬٢٣٦ والألفاظُ ٧٨٬٢٤٥ على مسندٍ واحد."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    assert int(_grab(r"— الألفاظ: (\d+) \| والمسندُ واحدٌ في كلّ مقدار")) == TOKENS
    assert float(_grab(r"— خاناتُ الحال: 8 \| H = ([0-9.]+)")) == FIELD
    for identifier in ("ص١", "ص٢"):
        assert _one(identifier).verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_skeleton_is_a_lumping_of_the_stripped_form() -> None:
    """ص٣: صورُ (ج) دون صور (ه) — تكتيلٌ بحكم البناء."""

    shapes = int(_grab(r"— صورُ \(ه\) منقوصةَ العلامة: (\d+)"))
    bones = int(_grab(r"— صورُ \(ج\) مجرَّدةً: (\d+)"))
    assert (shapes, bones) == (SHAPES, BONES)
    assert bones < shapes
    assert int(_grab(r"— قيمُ \(ر\) حالِ السابق: (\d+)")) == NEARS
    assert _one("ص٣").verdict(Fraction(bones - shapes)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_two_proven_monotonicities_hold_in_sample() -> None:
    """ص٤ وص٥: التنقيحُ لا يرفع الملحَقة، والتكتيلُ لا يزيد معلومات."""

    _, shape_in, _ = _row("(ه) الصورةُ منقوصةً")
    _, bone_in, _ = _row("(ج) الهيكلُ مجرَّدًا")
    cells, both_in, _ = _row("(ه، ر) معًا")
    assert cells == TOGETHER
    assert both_in < shape_in
    assert bone_in > shape_in  # شرطيّةٌ أعلى ⟹ معلوماتٌ أدنى
    assert _one("ص٤").verdict(_exact(both_in - shape_in)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ص٥").verdict(_exact(shape_in - bone_in)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_permutation_bound_and_the_absence_of_leak() -> None:
    """ص٦ وص٧: حدُّ التباديل دون N·H، وصفرُ محرفِ علامةٍ دخل متغيّرًا."""

    slack = float(_grab(r"— أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)"))
    assert slack == SLACK and slack < 0
    leaked = int(_grab(r"— محارفُ العلامة الأخيرة الداخلةُ في متغيّر: (\d+)"))
    assert leaked == 0
    assert _one("ص٦").verdict(_exact(slack)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ص٧").verdict(Fraction(leaked)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_word_own_form_outcarries_the_whole_context_ladder() -> None:
    """ص٨: `+١٫٢١٥٢٥٢` محجوزًا — **٥٫٧٣ ضِعفَ** كسبِ السلّم كلِّه."""

    shape = float(_grab(r"— I\(الحال؛ه\) محجوزةً: \+([0-9.]+)"))
    ladder = float(_grab(r"مجموعُ الكسب المحجوز: \+([0-9.]+)", LADDER))
    assert shape == SHAPE_OUT and ladder == LADDER_GAIN
    assert _grab(r"— أتفوق الصورةُ السلّمَ\؟ (\S+)") == "نعم"
    assert shape / ladder > 5.7
    assert _one("ص٨").verdict(_exact(shape)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_form_outcarries_the_neighbour_alone() -> None:
    """ص٩: الصورةُ أخبرُ من الجار بـ`+١٫١٤٥٧٣٠` محجوزًا."""

    shape = float(_grab(r"— I\(الحال؛ه\) محجوزةً: \+([0-9.]+)"))
    near = float(_grab(r"— I\(الحال؛ر\) محجوزةً: \+([0-9.]+)"))
    apart = float(_grab(r"— I\(الحال؛ه\) − I\(الحال؛ر\) محجوزتين: \+([0-9.]+)"))
    assert near == NEAR_OUT
    assert abs((shape - near) - apart) < 5e-6
    assert _one("ص٩").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    bone = float(_grab(r"— I\(الحال؛ج\) محجوزةً: \+([0-9.]+)"))
    assert bone == BONE_OUT


def test_my_claim_that_the_neighbour_adds_beyond_the_form_fell() -> None:
    """ص١٠ **سقط**: ما زاده الجارُ محجوزًا `−٠٫٢٩٠٠٤٩` لا موجبًا."""

    added = float(_grab(r"— I\(الحال؛ر \| ه\) محجوزةً: (\S+)"))
    assert added == ADDED_OUT and added < 0
    assert _one("ص١٠").verdict(_exact(added)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    tenth = _one("ص١٠")
    assert "وكيلًا عن بنية اللفظ لا خبرًا عن تركيب" in " ".join(
        tenth.falsifies.split()  # type: ignore[attr-defined]
    )


def test_the_fall_is_bracketed_and_the_question_is_a_classified_vacancy() -> None:
    """السالبُ عقابُ سَعةٍ لا عدمُ خبر — والسؤالُ خلوٌّ يُصنَّف لا صفر."""

    _, shape_in, _ = _row("(ه) الصورةُ منقوصةً")
    _, both_in, _ = _row("(ه، ر) معًا")
    inflated = shape_in - both_in
    assert abs(inflated - ADDED_IN) < 5e-6
    assert inflated > 0 > ADDED_OUT  # الحقُّ بين حدّين
    assert THE_NEIGHBOUR_BEYOND_THE_FORM is Vacancy.UNCLASSIFIED
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**ولا يُقرَأ ذلك «الجارُ لا يحمل شيئًا»**" in text
    assert "**وهو عقابُ السَّعة لا عدمُ الخبر**" in text
    assert "خلوٌّ يُصنَّف `UNCLASSIFIED` لا نتيجةُ صفر" in text


def test_the_ceiling_on_any_syntactic_reading_is_named() -> None:
    """السقفُ: `+٠٫١٠٣٦٦٢` بالتقدير المنتفخ — دون أربعةٍ من مئةٍ من الحقل."""

    _, shape_in, _ = _row("(ه) الصورةُ منقوصةً")
    _, both_in, _ = _row("(ه، ر) معًا")
    ceiling = shape_in - both_in
    assert abs(ceiling - ADDED_IN) < 5e-6
    assert ceiling < LADDER_GAIN / 2
    assert ceiling / FIELD < 0.04
    assert __doc__ is not None
    assert "**أربعةٌ من مئةٍ من الحقل فأقلّ**" in " ".join(__doc__.split())


def test_the_ratio_passed_but_its_reasoning_is_not_supported() -> None:
    """ص١١ مرَّ — **لأنّ البسطَ سالب**، لا لأنّ النسبةَ قِيست صغيرةً موجبة."""

    share = float(_grab(r"— وما بقي للجار بعد الصورة نسبةً إلى وحده: (\S+)"))
    assert share < 0
    assert _one("ص١١").verdict(_exact(share)) is Verdict.MET  # type: ignore[attr-defined]
    assert REASONING_NOT_SUPPORTED == ("ص١١",)


def test_the_opaque_box_is_split_into_named_byte_parts() -> None:
    """ص١٢: عشرون قسمًا، وحروفُ المدّ الثلاثةُ `٠٫٦٩٦١٢٢` منها."""

    whole = int(_grab(r"— ألفاظُ الخانة: (\d+) \| نصيبُها من الكلّ [0-9.]+"))
    assert whole == 24_319
    parts = re.findall(
        r"^    (\S+ U\+[0-9A-F]{4}) \| (\d+) \| نصيبٌ ([0-9.]+)$",
        LOG.read_text(encoding="utf-8"),
        re.M,
    )
    assert len(parts) == 8, len(parts)
    assert int(_grab(r"— أقسامُها: (\d+)")) == PARTS
    stretch = float(_grab(r"— نصيبُ حروف المدّ الثلاثة منها: ([0-9.]+)"))
    assert stretch == STRETCH
    assert _one("ص١٢").verdict(_exact(stretch)) is Verdict.MET  # type: ignore[attr-defined]


def test_eleven_stood_and_the_one_that_fell_is_mine() -> None:
    """إحدى عشرةَ صمدت، والساقطُ **دعوايَ** — ولا يُعاد تفسيرُ شرط."""

    machine = {"ص١", "ص٢", "ص٣", "ص٤", "ص٥", "ص٦", "ص٧"}
    assert "ص١٠" not in machine
    assert len(PREDICTIONS) - 1 == 11
    assert "دعواي" in _one("ص١٠").falsifies  # type: ignore[attr-defined]
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**إحدى عشرةَ صمدت، وواحدةٌ سقطت — وهي دعوايَ**" in text


def test_no_name_from_outside_the_frozen_bytes_entered_the_log() -> None:
    """لا اسمَ بابٍ ولا علامةٍ ولا يونيكود في المتن المقيس."""

    text = LOG.read_text(encoding="utf-8")
    assert DECLARATION in text
    body, _, owned = text.partition(DECLARATION)
    assert owned
    for word in FORBIDDEN:
        assert word not in body, word


def test_the_log_declares_that_it_names_no_chapter() -> None:
    """السجلُّ يقول بنفسه إنّه يقيس سقفًا ولا يُسمّي بابًا."""

    text = LOG.read_text(encoding="utf-8")
    assert "وهذا يقيس سقفَ القراءة التركيبيّة ولا يُسمّي بابًا ولا حكمًا" in text
    assert "والملحَقةُ منتفخةٌ بسَعة الفضاء، والحكمُ على المحجوز وحدَه" in text
