"""حرّاسُ طبقة الرسم: التطبيعُ، والمدخلُ، والهيكل — **وكلٌّ يَعَضّ أو يُرَدّ**.

**العطبُ الذي تحرسه**: `ccc(الشدّة) = 33` و`ccc(التنوين) = 27..29`،
والترتيبُ المعياريُّ **تصاعديّ**. فالرسمُ يكتب الشدّةَ أوّلًا ويونيكود
يرتّبها آخرًا، **فنقطةُ `normalize` واحدةٌ تقلب المواضعَ كلَّها**، ويعود
كلُّ فحصٍ يقرأ `text[i+1] == SHADDA` **بصفرٍ صامت**.

وهذا ليس فرضًا: بلاغٌ من شجرةٍ جارةٍ كشف مسارين يدّعيان فكَّ التنوين،
**أحدُهما يُبقيه حالةً مركّبة**. فالخطرُ مشهودٌ في جوارنا، **ولم يكن في
هذه الشجرة ما يمنعه**.

`A_GUARD_THAT_CANNOT_BITE_IS_NOT_A_GUARD`: فلكلِّ حارسٍ ههنا **صورةٌ
مكذِّبةٌ تُبنى ويُشترَط أن يردَّها** — تطبيعٌ يقلب، ومصيدةٌ تُحقَن،
وهيكلٌ يُفرِّق ما يجمعه الرسم.

`AND_ZERO_TODAY_IS_MEASURED_NOT_ASSUMED`: و«صفرُ مصائدَ» **مقيسٌ على
البايتات**، لا مفترَضًا من نظافةِ المصدر. فإن دخلت مصيدةٌ غدًا سقط
الفحصُ باسمها.

`AND_WHAT_IS_NOT_GUARDED_IS_NAMED`: **وحدُّها مُعلَن**: تحرس **شكلَ**
المدخل وثباتَ ترتيبه، **ولا تحرس صحّةَ نصٍّ ولا صوابَ قراءة**. ونصٌّ
فارسيٌّ صحيحٌ تُسمّى صورُه **ولا يُقال إنّه غلط**.
"""

from __future__ import annotations

import sys
import unicodedata as ud
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / "src"))

from algebra.rasm import (  # noqa: E402
    ARCHETYPE,
    MARK,
    TRAP,
    families,
    skeleton,
    trapped_points,
    traps,
)

sys.path.insert(0, str(REPOSITORY / "tests" / "arabic"))
from frozen_corpus import CORPUS, requires_corpus  # noqa: E402

SHADDA = 0x0651
TANWIN = (0x064B, 0x064C, 0x064D)
MARKUP = "<sel>"


def _text() -> str:
    return CORPUS.read_text(encoding="utf-8").replace(MARKUP, " ")


# ─────────── ١) حارسُ التطبيع ───────────


def test_the_combining_classes_are_what_the_reordering_claim_rests_on() -> None:
    """`ccc` الشدّةِ أعلى من التنوين — **وذلك سببُ القلب، مقروءًا لا مرويًّا**."""

    assert ud.combining(chr(SHADDA)) == 33
    assert tuple(ud.combining(chr(one)) for one in TANWIN) == (27, 28, 29)
    assert all(ud.combining(chr(one)) < ud.combining(chr(SHADDA)) for one in TANWIN)


def test_normalising_flips_the_pair_and_that_is_the_falsifying_case() -> None:
    """الصورةُ المكذِّبة: `NFC` **يقلب** الشدّةَ والتنوين — فيُرى العضّ."""

    base = chr(0x0628)
    written = base + chr(SHADDA) + chr(TANWIN[0])
    flipped = base + chr(TANWIN[0]) + chr(SHADDA)
    assert written != flipped
    assert ud.normalize("NFC", written) == flipped
    assert ud.normalize("NFC", written) != written
    assert ud.normalize("NFC", flipped) == flipped


@requires_corpus
def test_the_corpus_is_not_normalised_and_that_is_deliberate() -> None:
    """المدوّنةُ **ليست NFC** — ولو طُبِّعت لتبدّلت بصمتُها وسقط كلُّ ختم."""

    text = _text()
    assert not ud.is_normalized("NFC", text)
    assert ud.normalize("NFC", text) != text


@requires_corpus
def test_the_mark_order_in_the_corpus_is_written_order_not_canonical() -> None:
    """وترتيبُها **ترتيبُ الرسم**: الشدّةُ قبل التنوين، وصفرٌ بالعكس."""

    text = _text()
    marks = {chr(one) for one in TANWIN}
    shadda = chr(SHADDA)
    written = sum(
        1 for i in range(len(text) - 1) if text[i] == shadda and text[i + 1] in marks
    )
    canonical = sum(
        1 for i in range(len(text) - 1) if text[i] in marks and text[i + 1] == shadda
    )
    assert written > 200, written
    assert canonical == 0, canonical


# ─────────── ٢) حارسُ المدخل ───────────


@requires_corpus
def test_the_corpus_carries_none_of_the_six_traps_measured_not_assumed() -> None:
    """صفرُ مصائدَ — **مقيسًا على البايتات** لا مفترَضًا من نظافة المصدر."""

    assert traps(_text()) == ()
    assert trapped_points(_text()) == {}


def test_each_trap_is_caught_by_name_when_injected() -> None:
    """وكلُّ مصيدةٍ تُحقَن **فتُسمّى** — فلا اسمَ في الجدول بلا عضّ."""

    base = chr(0x0628) + chr(0x062A)
    shown = {
        "صور عرض": chr(0xFEDF),
        "تطويل": chr(0x0640),
        "محارف خفية": chr(0x200C),
        "صور فارسية": chr(0x06CC),
        "أرقام شرقية": chr(0x0661),
        "خارج المجال": chr(0x0041),
    }
    for name, point in shown.items():
        assert name in traps(base + point), name
    assert len(shown) == len(TRAP)


def test_a_trap_names_a_place_to_look_not_a_verdict() -> None:
    """و«مصيدةٌ» موضعٌ يُنظَر فيه — فنصٌّ فارسيٌّ صحيحٌ تُسمّى صورُه فقط."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_A_TRAP_IS_A_PLACE_TO_LOOK_NOT_A_VERDICT`" in (
        here + (REPOSITORY / "src" / "algebra" / "rasm.py").read_text(encoding="utf-8")
    )
    assert traps(chr(0x0628)) == ()


# ─────────── ٣) الهيكلُ المُعلَن ───────────


def test_the_skeleton_drops_marks_and_folds_families() -> None:
    """الهيكلُ يحذف الضبطَ ويجمع العائلة — **بالنقاط لا بحرفٍ مكتوب**."""

    word = "".join(chr(one) for one in (0x0628, 0x064E, 0x062A, 0x0651, 0x064A))
    assert skeleton(word) == chr(0x0628) * 3
    assert all(one not in {ord(c) for c in skeleton(word)} for one in MARK)


def test_the_skeleton_is_total_and_loses_no_point_silently() -> None:
    """**تامّةٌ**: كلُّ نقطةٍ إمّا علامةٌ تُحذَف أو تمرّ — ولا ثالثَ يسقط."""

    sample = "".join(chr(one) for one in range(0x0600, 0x0700))
    kept = [one for one in sample if ord(one) not in MARK]
    assert len(skeleton(sample)) == len(kept)
    outside = chr(0x0041) + chr(0x0660)
    assert len(skeleton(outside)) == 2


def test_the_families_are_disjoint_and_each_has_a_head() -> None:
    """والعائلاتُ **متباينةٌ** ولكلٍّ رأسٌ — فلا نقطةَ في عائلتين."""

    seen: set[int] = set()
    for family in families():
        assert len(family) >= 2, family
        assert not seen & set(family), family
        seen |= set(family)
        assert ARCHETYPE[family[0]] == family[0]
    assert len(seen) == len(ARCHETYPE)


def test_the_skeleton_would_be_refused_if_it_split_what_the_script_joins() -> None:
    """الصورةُ المكذِّبةُ للهيكل: لو فرَّق الأسنانَ لَما اجتمع اللفظان."""

    one = chr(0x0628) + chr(0x0646)
    two = chr(0x062A) + chr(0x064A)
    assert skeleton(one) == skeleton(two), "الأسنانُ لا تجتمع — فالجدولُ ناقص"
    assert skeleton(chr(0x062F)) != skeleton(chr(0x0631)), "عائلتان جُمِعتا خطأً"


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ: يحرس الشكلَ لا صحّةَ النصّ، والصفرُ مقيسٌ لا مفترَض."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`A_GUARD_THAT_CANNOT_BITE_IS_NOT_A_GUARD`" in here
    assert "`AND_ZERO_TODAY_IS_MEASURED_NOT_ASSUMED`" in here
    assert "**ولا تحرس صحّةَ نصٍّ ولا صوابَ قراءة**" in here
    module = (REPOSITORY / "src" / "algebra" / "rasm.py").read_text(encoding="utf-8")
    assert "`THE_SKELETON_IS_NOT_A_LETTER_NAME`" in module
