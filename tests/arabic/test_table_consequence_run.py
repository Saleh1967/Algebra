"""حُكمُ ختم `9470c8f0…`: **عشرٌ صمدت، وصفّان من الجدول سقطا**.

`THE_TABLE_WAS_HALF_RIGHT_AND_THE_HALF_THAT_FELL_IS_ITS_CORE`: **صمد
اللازمُ الأكبرُ في اتّجاهه وسقط في مقداره.** فحيث تتبدّل العلامةُ صار
الجارُ أخبرَ بها: `+٠٫١٢٨٢٠٩` محجوزًا — **١٫٨٤ ضِعفَ** `٠٫٠٦٩٥٢٢` المقيسة
على المدوّنة كلِّها (ج٨ صمد). **فللموقع أثرٌ ثمّةَ، وذلك يوافق الجدول.**

`BUT_THE_FORM_STILL_WINS_BY_ELEVEN_TIMES`: **وسقط ج٩**: يلزم عن الجدول
أنّ تبدّلَ العلامة تبدّلُ **موقع** لا تبدّلُ **صورة**، فتكون الصورةُ أقلَّ
خبرًا من الجار ثمّةَ. **فجاءت أخبرَ بـ`١٠٫٦٨` ضِعفًا**: `+١٫٣٦٨٧٤٧` مقابلَ
`+٠٫١٢٨٢٠٩`. **فالتبدّلُ تبدّلُ صورةٍ في أكثره لا تبدّلُ موقع** — ويسقط
الجدولُ في أصل دعواه، **ولا يُتأوَّل**.

`AND_THE_SUKUN_ROW_FELL_OUTRIGHT_AND_BACKWARDS`: **وسقط ج٧ معكوسًا**:
يقول الجدولُ في السكون «جزمٌ أو بناءٌ عليه» — وذلك أقربُ إلى الثابت. **فجاء
نصيبُه في المتبدّلة `٠٫١٩٤٠٢١` وفي الثابتة `٠٫٠٢٤٦٥٩`** — **٧٫٨٧ أضعافًا
في الجهة المخالفة**. فصفُّ السكون **ساقطٌ بعينه**، ويُسمّى.

`AND_TWO_THAT_STOOD_STOOD_BY_A_THIN_MARGIN_AND_IT_IS_SAID`: وصمد ج١٠ بفضلِ
`+٠٫٠١٥١٩١` وج١١ بفضلِ `+٠٫٠٢٠٠١٥` فوق النصف. **فلو كان الحدُّ `٠٫٥٣`
لسقطا** — **وصمودٌ بهذا الهامش يُذكَر هامشُه**، ولا يُقرأ كصمود ج٨.

`AND_A_FALL_HERE_IS_THE_FALL_OF_A_DEPOSIT_NOT_OF_A_GRAMMAR`: والجدولُ
**فرضٌ إسناديٌّ أوّليٌّ** أُودِع وكالةً، لا نقلٌ عن عالمٍ ولا راوٍ.
**فسقوطُ صفَّيه سقوطُ فرضٍ مُودَعٍ**، ولا يمسُّ نحوًا ولا ناقلًا — ولا
يُقال «سقط الإعراب».
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_table_consequence_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "table_consequence_run.log"
MORPH = REPOSITORY / "deposits" / "morph_residue_run.log"
TABLES = REPOSITORY / "deposits" / "bridge_tables.md"

pytestmark = requires_corpus

LINES = 6_236
TOKENS = 78_245
SKELETONS = 14_871
LEAST = 5
STEADY_KINDS = 1_223
SHIFTING_KINDS = 897
STEADY = 28_428
SHIFTING = 30_775
OUTSIDE = 19_042
FIELD_STEADY = 2.0225
FIELD_SHIFTING = 2.6943
NEAR_SHIFTING = 0.128209
SHAPE_SHIFTING = 1.368747
NEAR_STEADY = 0.032602
SHAPE_STEADY = 1.452106
NEAR_WHOLE = 0.069522
TANWEEN_GAP = 0.026164
SUKUN_GAP = -0.169362
MOVES_SHIFTING = 0.515191
QUIET_STEADY = 0.520015
THIN = 0.03
FORBIDDEN = (
    "ARABIC",
    "مبنيّ",
    "معرب",
    "فتحة",
    "ضمّة",
    "كسرة",
    "سكونٌ جزم",
    "إعراب",
    "مرفوع",
    "منصوب",
    "مجرور",
)
DECLARATION = "— ما لا يدخل هذا السجلّ"


# **سقفُ كلّ نسبةٍ ومقدارٍ مختوم** — العطل ٢٦: حدٌّ فوق سقفٍ شرطٌ لا يُختبَر.
# والسقفُ يُصرَّح به ويُعلَّل، ويفحص `test_ceiling_audit` أنّ الحدَّ دونه.
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ج٨": (
        Fraction(26943, 10000),
        "المعلوماتُ لا تفوق إنتروبيا الهدف، و`H` على المتبدّلة ٢٫٦٩٤٣",
    ),
    "ج١٠": (
        Fraction(1),
        "كلُّ لفظٍ في المسند يقبل أن تكون حالُه إحدى الحركات الثلاث",
    ),
    "ج١١": (
        Fraction(1),
        "كلُّ لفظٍ في المسند يقبل أن يكون بلا علامةٍ أو ساكنًا",
    ),
}

# **لا شرطَ مرَّ بتعليلٍ غيرِ مؤيَّد**: كلُّ ما صمد قِيس على مسنده بعينه
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"), re.M)
    return str(found)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("9470c8f0")


def test_the_partition_closes_on_the_whole_support() -> None:
    """ج١ وج٢ وج٣: ثابتة + متبدّلة + خارجُ القسمة = ٧٨٬٢٤٥."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    assert int(_grab(r"— الألفاظ: (\d+)$")) == TOKENS
    assert int(_grab(r"— هياكلُ متمايزة: (\d+) \|")) == SKELETONS
    assert int(_grab(r"وشرطُ القسمة: (\d+) وقوعاتٍ")) == LEAST
    steady = int(_grab(r"— المسندُ \(ثابتة\): (\d+)"))
    shifting = int(_grab(r"— المسندُ \(متبدّلة\): (\d+)"))
    outside = int(_grab(r"— خارجُ القسمة \(دون الشرط\): (\d+)"))
    assert (steady, shifting, outside) == (STEADY, SHIFTING, OUTSIDE)
    assert steady + shifting + outside == TOKENS
    assert int(_grab(r"— مجموعُها: (\d+)")) == TOKENS
    for identifier in ("ج١", "ج٢", "ج٣"):
        assert _one(identifier).verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_steady_support_is_determined_by_its_skeleton_by_construction() -> None:
    """ج٤: `H(الحال|الهيكل)` على الثابتة **صفرٌ تامّ** — بحكم البناء."""

    found = float(_grab(r"— H\(الحال\|الهيكل\) على الثابتة ملحَقةً: ([0-9.]+)"))
    assert found == 0.0
    assert int(_grab(r"— هياكلُ ثابتة: (\d+) \|")) == STEADY_KINDS
    assert int(_grab(r"هياكلُ متبدّلة: (\d+)$")) == SHIFTING_KINDS
    assert _one("ج٤").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_permutation_bound_holds_in_both_supports_and_no_leak() -> None:
    """ج٥ وج١٢: حدُّ التباديل دون N·H في المسندين، وصفرُ محرفِ حالٍ دخل."""

    slack = [
        float(one)
        for one in re.findall(
            r"— أقصى \(log₂ التباديل − N·H\) بعد ألفٍ في \((?:ثابتة|متبدّلة)\) = (\S+)",
            LOG.read_text(encoding="utf-8"),
        )
    ]
    assert len(slack) == 2 and max(slack) < 0
    leaked = int(_grab(r"— محارفُ الحال الداخلةُ في متغيّر: (\d+)"))
    assert leaked == 0
    assert _one("ج٥").verdict(_exact(max(slack))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ج١٢").verdict(Fraction(leaked)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_neighbour_does_carry_more_where_the_mark_varies() -> None:
    """ج٨ **صمد**: `+٠٫١٢٨٢٠٩` — **١٫٨٤ ضِعفَ** ما في المدوّنة كلِّها."""

    near = float(_grab(r"— I\(الحال؛ر\) محجوزةً على \(متبدّلة\): \+([0-9.]+)"))
    steady = float(_grab(r"— I\(الحال؛ر\) محجوزةً على \(ثابتة\): \+([0-9.]+)"))
    whole = float(_grab(r"— I\(الحال؛ر\) محجوزةً: \+([0-9.]+)", MORPH))
    assert (near, steady, whole) == (NEAR_SHIFTING, NEAR_STEADY, NEAR_WHOLE)
    assert near > Fraction(1, 10)
    assert 1.8 < near / whole < 1.9
    assert near > steady * 3  # والجارُ أخبرُ حيث يتبدّل ممّا هو حيث يثبت
    assert _one("ج٨").verdict(_exact(near)) is Verdict.MET  # type: ignore[attr-defined]


def test_but_the_form_still_outcarries_the_neighbour_and_the_table_falls() -> None:
    """ج٩ **سقط**: الصورةُ أخبرُ بـ`١٠٫٦٨` ضِعفًا حيث يتبدّل الحكم."""

    near = float(_grab(r"— I\(الحال؛ر\) محجوزةً على \(متبدّلة\): \+([0-9.]+)"))
    shape = float(_grab(r"— I\(الحال؛ه\) محجوزةً على \(متبدّلة\): \+([0-9.]+)"))
    apart = float(_grab(r"— الفرقُ \(ر − ه\) على \(متبدّلة\): (\S+)"))
    assert shape == SHAPE_SHIFTING
    assert abs(apart - SUKUN_GAP) > 1  # فرقٌ كبيرٌ لا هامشٌ
    assert abs((near - shape) - apart) < 5e-6
    assert shape / near > 10
    assert _one("ج٩").verdict(_exact(apart)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    ninth = _one("ج٩")
    assert "فالتبدّلُ صرفيٌّ لا تركيبيّ" in " ".join(ninth.falsifies.split())  # type: ignore[attr-defined]
    assert float(_grab(r"— I\(الحال؛ه\) محجوزةً على \(ثابتة\): \+([0-9.]+)")) == (
        SHAPE_STEADY
    )


def test_the_sukun_row_of_the_table_fell_and_backwards() -> None:
    """ج٧ **سقط معكوسًا**: السكونُ في المتبدّلة **٧٫٨٧ أضعافًا**."""

    steady = float(_grab(r"— نصيبُ السكون: ثابتة ([0-9.]+) \|"))
    shifting = float(_grab(r"— نصيبُ السكون: ثابتة [0-9.]+ \| متبدّلة ([0-9.]+)"))
    gap = float(_grab(r"— وفرقُه \(ثابتة − متبدّلة\): (\S+)"))
    assert abs(gap - SUKUN_GAP) < 5e-6
    assert gap < 0
    assert 7.8 < shifting / steady < 8.0
    assert _one("ج٧").verdict(_exact(gap)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    seventh = _one("ج٧")
    assert "سقط هذا الصفُّ من الجدول" in " ".join(seventh.falsifies.split())  # type: ignore[attr-defined]


def test_the_tanween_row_of_the_table_stood() -> None:
    """ج٦ **صمد**: التنوينُ يزيد حيث تتبدّل العلامة."""

    gap = float(_grab(r"— وفرقُه \(متبدّلة − ثابتة\): \+([0-9.]+)"))
    assert abs(gap - TANWEEN_GAP) < 5e-6
    assert _one("ج٦").verdict(_exact(gap)) is Verdict.MET  # type: ignore[attr-defined]


def test_two_conditions_stood_on_a_thin_margin_and_the_margin_is_named() -> None:
    """ج١٠ وج١١ صمدا بهامشٍ رقيق — **ويُذكَر هامشُهما ولا يُقرآن كج٨**."""

    moves = float(_grab(r"— نصيبُ الحركات الثلاث في المتبدّلة: ([0-9.]+)"))
    quiet = float(_grab(r"— نصيبُ \(«بلا علامة» \+ السكون\) في الثابتة: ([0-9.]+)"))
    assert (moves, quiet) == (MOVES_SHIFTING, QUIET_STEADY)
    for value in (moves, quiet):
        assert value > Fraction(1, 2)
        assert value - 0.5 < THIN  # هامشٌ رقيقٌ يُسمّى
    assert _one("ج١٠").verdict(_exact(moves)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ج١١").verdict(_exact(quiet)) is Verdict.MET  # type: ignore[attr-defined]
    assert __doc__ is not None
    assert "**فلو كان الحدُّ `٠٫٥٣`\nلسقطا**" in __doc__


def test_ten_stood_and_two_rows_of_the_table_fell() -> None:
    """عشرٌ صمدت، والساقطان **لازمان من الجدول** لا دعويان لي."""

    fell = {"ج٧", "ج٩"}
    machine = {"ج١", "ج٢", "ج٣", "ج٤", "ج٥", "ج١٢"}
    assert not fell & machine
    assert len(PREDICTIONS) - len(fell) == 10
    for identifier in fell:
        assert "لازم" in _one(identifier).falsifies  # type: ignore[attr-defined]
        assert "الجدول" in _one(identifier).falsifies  # type: ignore[attr-defined]
    assert REASONING_NOT_SUPPORTED == ()


def test_the_log_names_no_ruling_and_declares_its_limit() -> None:
    """لا اسمَ بابٍ في المتن المقيس، والقسمةُ بالبايتات لا بالأحكام."""

    text = LOG.read_text(encoding="utf-8")
    assert DECLARATION in text
    body, _, owned = text.partition(DECLARATION)
    assert owned
    for word in FORBIDDEN:
        assert word not in body, word
    assert "والقسمةُ بالبايتات: ثابتٌ ومتبدّلٌ، لا حكمَ بابٍ يُسمّى" in owned
    assert "وسقوطُ لازمٍ سقوطُ فرضٍ مُودَعٍ لا سقوطُ لغة" in owned


def test_the_fall_is_recorded_against_the_deposited_table() -> None:
    """الجدولُ المُودَعُ يحمل ما سقط منه — ولا يُصلَح صفٌّ بعد النظر."""

    rows = TABLES.read_text(encoding="utf-8")
    assert "## ما سقط من هذا الجدول" in rows
    assert "ج٧" in rows and "ج٩" in rows
    assert "٧٫٨٧" in rows
    assert "١٠٫٦٨" in rows
    assert "ولا يُصلَح صفٌّ بعد النظر" in rows
