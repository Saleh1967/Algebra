"""حُكمُ ختم `c4ffe307…`: **عشرٌ صمدت، واثنتان سقطتا — وكلتاهما دعوايَ**.

`THE_STORY_I_TOLD_WAS_BACKWARDS`: زعمتُ أنّ خانةَ «بلا علامة» — وهي أكبرُ
خانةٍ بنصيب `٠٫٣١٠٨` — **مسكونةٌ بالوقف**، فبرفع أواخر الأسطر ينقص
نصيبُها. **فزاد**: من `٠٫٣١٠٨` إلى `٠٫٣٣٣١`. وقِيس المقامُ الثالثُ فبان
السبب: **أواخرُ الأسطر أكثرُها مُعلَّم**، ونصيبُ «بلا علامة» فيها
`٠٫٠٥٣٤` **لا `٠٫٣١٠٨`** — أي **سُدسُ** ما في وسط السطر. فأواخرُ الأسطر
**أقلُّ المواضع خلوًّا من العلامة، لا أكثرُها**.

`AND_THE_ENTROPY_FELL_WHERE_I_SAID_IT_WOULD_RISE`: وزعمتُ أنّ الإنتروبيا
**ترتفع** برفع الوقف لأنّ أكبرَ خانةٍ تنقص. **فنزلت**: `٢٫٦١٠٦` ⟶
`٢٫٥٦٥٨`. **والحدسُ الساذجُ كان أصوبَ من تعليلي.**

`WHAT_SURVIVED_IS_THE_MEASUREMENT_NOT_THE_STORY`: وما صمد هو **العدد**:
البتّاتُ الإحدى عشرة غيرُ الموضعيّة **كلُّها تعيش** بعد رفع أواخر الأسطر،
ومجموعُها `+٠٫١١٣٩٩٣` من `+٠٫١٥٥٠٨٠` — **ثلاثةُ أرباعٍ تقريبًا**. فأكثرُ
ما تحمله بتّاتُ الجوار **ليس أثرَ حدّ السطر**.

`AND_THE_POSITIONAL_BIT_IS_EXACTLY_THE_MIXING`: وكسبُ «آخرُ السطر» على
المقام (ب) **صفرٌ تامّ** — فهو ثابتٌ ثمّة بحكم التقييد. وقاعدةُ السلسلة
تُغلِق: `H(أ) − Σ وزنٌ·H = ٠٫٠٥٧٠٢٥` وهو **الربحُ الملحَقُ للدرجة الأولى
بعينه**، بانحرافٍ `٢٫٦٧٧e−٠٧`. **فتلك البتّةُ هي اختلافُ التوزيعين لا
شيءَ غيره.**

`AND_NO_LINGUISTIC_READING_IS_LICENSED_BY_ANY_OF_THIS`: وكُتِب في الختم
**قبل النظر** أنّ هذا يفصل الوقفَ عن غيره **ولا يُثبِت أنّ غيرَه إعراب**.
**وأنّ أواخرَ الأسطر مواضعُ وقفٍ دعوًى تحتاج فهرسًا مُودَعًا** — وليس في
المستودع فهرس. **فما ههنا مقادير، والقراءةُ فعلُ صاحب المستودع.**
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_pausal_split_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "pausal_split_run.log"
WITNESS = REPOSITORY / "deposits" / "pausal_split_witness.log"
LADDER = REPOSITORY / "deposits" / "context_ladder_run.log"

pytestmark = requires_corpus

LINES = 6_236
WHOLE = 78_245
INNER = 72_009
LIFTED = 6_236
BARE_WHOLE = 0.3108
BARE_INNER = 0.3331
BARE_LAST = 0.0534
FIELD_WHOLE = 2.6106
FIELD_INNER = 2.5658
FIELD_LAST = 2.4124
REST_WHOLE = 0.155080
REST_INNER = 0.113993
DEAD = 0
BEST_INNER = 0.019615
IDENTITY = 2.677e-07
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
    "مبنيّ",
    "وقفٌ لازم",
)
DECLARATION = "— ما لا يدخل هذا السجلّ"


# **سقفُ كلّ نسبةٍ ومقدارٍ مختوم** — العطل ٢٦.
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "و١٠": (
        Fraction(25658, 10000),
        "مجموعُ كسبٍ لا يفوق إنتروبيا الهدف، و`H` على المجال (ب) ٢٫٥٦٥٨",
    ),
}

# **شرطان مرّا بتعليلٍ لم يؤيِّده القياس**: و٩ وو١٠ مقيسان على **حدّ
# السطر** لا على **الوقف**. فأنّ آخرَ السطر موضعُ وقفٍ **دعوًى تحتاج
# فهرسًا مُودَعًا** وليس في المستودع فهرس. فما قِيس رفعُ حدٍّ لا رفعُ وقف،
# **والعددُ صحيحٌ والتعليلُ غيرُ مؤيَّد** — ويُقال ذلك ولا يُطوى.
REASONING_NOT_SUPPORTED = ("و٩", "و١٠")


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, where: Path = LOG) -> str:
    (found,) = re.findall(pattern, where.read_text(encoding="utf-8"))
    return str(found)


def _pairs() -> list[tuple[str, float, float]]:
    """(البتّة، كسبُها في أ، كسبُها في ب) — من جدول المقابلة."""

    found = re.findall(
        r"^  د(\d+) «.+?» \| (\S+) \| (\S+) \| \S+$",
        LOG.read_text(encoding="utf-8"),
        re.M,
    )
    return [(one, float(two), float(three)) for one, two, three in found]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("c4ffe307")


def test_the_three_supports_close_their_arithmetic() -> None:
    """و١ وو٢ وو٣: ٧٨٬٢٤٥ − ٦٬٢٣٦ = ٧٢٬٠٠٩ — والحسابُ يُقفِل نفسَه."""

    assert int(_grab(r"— الأسطر: (\d+)")) == LINES
    assert int(_grab(r"— المجال \(أ\) كلُّ المواضع: (\d+)")) == WHOLE
    assert int(_grab(r"— المجال \(ب\) ما ليس آخرَ سطره: (\d+)")) == INNER
    assert int(_grab(r"— الخارجُ عن \(ب\): (\d+)")) == LIFTED
    assert WHOLE - LIFTED == INNER
    for identifier in ("و١", "و٢", "و٣"):
        assert _one(identifier).verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_positional_bit_is_exactly_constant_on_the_inner_support() -> None:
    """و٤: «آخرُ السطر» ثابتٌ في (ب) — فكسبُه صفرٌ تامٌّ لا صغير."""

    gain = float(_grab(r"— كسبُ «آخرُ السطر» في \(ب\): \+([0-9.]+)"))
    assert gain == 0.0
    inner = LOG.read_text(encoding="utf-8").split("— مقامُ ب:", 1)[1]
    (blocks,) = re.findall(r"— د1 «آخرُ السطر»: .*? \| كتلٌ (\d+)", inner)
    assert int(blocks) == 1
    assert _one("و٤").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_two_proven_bounds_hold_in_both_supports() -> None:
    """و٥ وو٦: التنقيحُ لا يرفع الملحَقة، وحدُّ التباديل دون N·H."""

    gains = re.findall(r"ربحٌ ملحَقٌ \+([0-9.]+)", LOG.read_text(encoding="utf-8"))
    assert len(gains) == 24, len(gains)
    lowest = min(float(one) for one in gains)
    assert lowest == 0.0
    slack = [
        float(one)
        for one in re.findall(
            r"— أقصى \(log₂ التباديل − N·H\) بعد ألف في \([أب]\) = (\S+)",
            LOG.read_text(encoding="utf-8"),
        )
    ]
    assert len(slack) == 2 and max(slack) < 0
    assert _one("و٥").verdict(_exact(lowest)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("و٦").verdict(_exact(max(slack))) is Verdict.MET  # type: ignore[attr-defined]


def test_my_claim_that_the_bare_box_is_inhabited_by_pause_fell() -> None:
    """و٧ **سقط**: نصيبُ «بلا علامة» **زاد** برفع أواخر الأسطر."""

    whole = float(_grab(r"· \| 24319 \| نصيبٌ ([0-9.]+)"))
    inner = float(_grab(r"· \| 23986 \| نصيبٌ ([0-9.]+)"))
    assert abs(whole - BARE_WHOLE) < 5e-5 and abs(inner - BARE_INNER) < 5e-5
    assert inner > whole
    assert _one("و٧").verdict(_exact(whole - inner)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    seventh = _one("و٧")
    assert "وينهار تعليلي للوقف من أصله" in " ".join(seventh.falsifies.split())  # type: ignore[attr-defined]
    last = float(_grab(r"· \| 333 \| نصيبٌ ([0-9.]+)", WITNESS))
    assert abs(last - BARE_LAST) < 5e-5
    assert last < whole / 5


def test_my_claim_that_the_entropy_would_rise_fell_too() -> None:
    """و٨ **سقط**: الإنتروبيا **نزلت** حيث قلتُ ترتفع."""

    whole = float(_grab(r"— خاناتُ الحال في المجال \(أ\): H = ([0-9.]+)"))
    inner = float(_grab(r"— خاناتُ الحال في المجال \(ب\): H = ([0-9.]+)"))
    last = float(_grab(r"— H\(ج\) = ([0-9.]+)", WITNESS))
    assert (whole, inner, last) == (FIELD_WHOLE, FIELD_INNER, FIELD_LAST)
    assert inner < whole
    assert _one("و٨").verdict(_exact(inner - whole)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    eighth = _one("و٨")
    assert "فالحدسُ الساذجُ" in " ".join(eighth.falsifies.split())  # type: ignore[attr-defined]


def test_every_non_positional_bit_survives_the_lift() -> None:
    """و٩: لا بتّةَ ماتت — إحدى عشرةَ بتّةً كسبُها موجبٌ في (ب)."""

    rows = _pairs()
    assert len(rows) == 12
    rest = rows[1:]
    assert all(two > 0 for _, _, two in rest), rest
    assert int(_grab(r"— بتّاتٌ ماتت في \(ب\): (\d+)")) == DEAD
    assert _one("و٩").verdict(Fraction(DEAD)) is Verdict.MET  # type: ignore[attr-defined]


def test_most_of_the_neighbour_information_is_not_the_line_boundary() -> None:
    """و١٠: مجموعُ الإحدى عشرة في (ب) `+٠٫١١٣٩٩٣` — فوق العُشر المختوم."""

    whole = float(_grab(r"— مجموعُ الإحدى عشرة في \(أ\): \+([0-9.]+)"))
    inner = float(_grab(r"— مجموعُ الإحدى عشرة في \(ب\): \+([0-9.]+)"))
    assert (whole, inner) == (REST_WHOLE, REST_INNER)
    assert inner > Fraction(1, 10)
    assert inner / whole > 0.7
    assert _one("و١٠").verdict(_exact(inner)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_leading_bit_after_the_lift_asks_about_the_previous_state() -> None:
    """و١١: أكبرُ بتّةٍ في (ب) «حالُ السابق = ·» — لا حرفُ خاتمته."""

    best = _grab(r"— أكبرُ بتّةٍ في \(ب\): «(.+?)» بـ")
    assert best == "حالُ السابق = ·", best
    gain = float(_grab(r"— أكبرُ بتّةٍ في \(ب\): «.+?» بـ\+([0-9.]+)"))
    assert gain == BEST_INNER
    assert _grab(r"— أهي عن حال السابق\؟ (\S+)") == "نعم"
    assert _one("و١١").verdict(Fraction(1)) is Verdict.MET  # type: ignore[attr-defined]


def test_nothing_of_the_asked_position_entered_a_question() -> None:
    """و١٢: صفرُ بايتٍ من الموضع المسؤولِ عنه دخل سؤالًا."""

    leaked = int(_grab(r"— بايتاتُ الموضع المسؤولِ عنه الداخلةُ في سؤال: (\d+)"))
    assert leaked == 0
    assert _one("و١٢").verdict(Fraction(leaked)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_third_support_is_measured_and_the_subtraction_agrees() -> None:
    """المقامُ (ج) مقيسٌ من المدوّنة، والطرحُ يوافقه في الخانات الثماني."""

    assert int(_grab(r"— ألفاظُه: (\d+) \| وأسطرُ المجمَّد: 6236", WITNESS)) == LIFTED
    assert int(_grab(r"— خاناتٌ خالفت: (\d+)", WITNESS)) == 0
    rows = re.findall(
        r"^    \S+(?: U\+[0-9A-F]{4})? \| مقيسٌ (\d+) \| مطروحٌ (\d+) \| (\S+)$",
        WITNESS.read_text(encoding="utf-8"),
        re.M,
    )
    assert len(rows) == 8
    assert {three for _, _, three in rows} == {"مطابق"}
    assert sum(int(one) for one, _, _ in rows) == LIFTED


def test_the_chain_rule_closes_on_the_first_bit() -> None:
    """الهويّةُ تُغلِق: البتّةُ الأولى **هي** اختلافُ التوزيعين لا شيءَ غيره."""

    mutual = float(_grab(r"— I المُشتَقّ = ([0-9.]+)", WITNESS))
    kept = float(_grab(r"والربحُ الملحَقُ المُودَع = ([0-9.]+)", WITNESS))
    assert mutual == kept
    drift = float(_grab(r"— أقصى انحرافٍ عن الهويّة: (\S+)", WITNESS))
    assert drift == IDENTITY
    assert _grab(r"— أتُغلِق\؟ (\S+)", WITNESS) == "نعم"
    ladder = float(_grab(r"— د1 «آخرُ السطر»: .*? ربحٌ ملحَقٌ \+([0-9.]+)", LADDER))
    assert abs(ladder - mutual) < 5e-5


def test_ten_stood_and_the_two_that_fell_are_both_mine() -> None:
    """عشرٌ صمدت، والساقطتان **دعوايَ لا الآلة** — ولا يُعاد تفسيرُ شرط."""

    fell = {"و٧", "و٨"}
    machine = {"و١", "و٢", "و٣", "و٤", "و٥", "و٦"}
    assert not fell & machine
    assert len(PREDICTIONS) - len(fell) == 10
    for identifier in fell:
        assert "دعواي" in _one(identifier).falsifies  # type: ignore[attr-defined]
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**عشرٌ صمدت، واثنتان سقطتا — وكلتاهما دعوايَ**" in text
    assert "**والحدسُ الساذجُ كان أصوبَ من تعليلي.**" in text


def test_no_name_from_outside_the_frozen_bytes_entered_the_log() -> None:
    """لا اسمَ بابٍ ولا علامةٍ ولا يونيكود — شريحةٌ ونقطةُ ترميز."""

    for where in (LOG, WITNESS):
        text = where.read_text(encoding="utf-8")
        assert DECLARATION in text
        # **المنعُ على المتن المقيس**؛ وأمّا الإقرارُ فموضعُ النفي، ولا
        # يُمنَع فيه اسمٌ يُنفى — وإلّا لم يُمكِن أن يُكتَب النفيُ ألبتّة
        body, _, owned = text.partition(DECLARATION)
        assert owned
        for word in FORBIDDEN:
            assert word not in body, (where.name, word)


def test_no_linguistic_reading_is_licensed_and_the_log_says_so() -> None:
    """السجلُّ يقول بنفسه إنّه لا يُثبِت إعرابًا ولا وقفًا."""

    assert "وهذا يفصل الوقفَ عن غيره ولا يُثبِت أنّ غيرَه إعراب" in LOG.read_text(
        encoding="utf-8"
    )
    assert "ولا يُثبِت أنّها مواضعُ وقف" in WITNESS.read_text(encoding="utf-8")
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**وأنّ أواخرَ الأسطر مواضعُ وقفٍ دعوًى تحتاج فهرسًا مُودَعًا**" in text
