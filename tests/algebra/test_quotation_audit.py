"""حارسُ تحقيقِ النقل.

**العطلُ الذي يحرسه**: تقريرٌ يقول «طابقت حرفيًّا» **لا يُعاد**. فمن
قرأه لا يملك أن يقيسه، وأرقامُ الأسطرِ المرويّةُ لا تُطابق فهرسَ
استخراجٍ آخر — **وفهرسٌ لا يُتَّفَق عليه ليس شاهدًا**.

فهذه الفحوصُ تُثبّت أربعةً:

١. أنّ المطابقةَ تُطلَب **بالنصِّ لا بالرقم**، فيصدُق التحقيقُ ولو
   اختلف ترقيمُ الناقلِ — وهو ما وقع.
٢. أنّ المِسبارَ مُعلَنٌ بنصوصه وأسبابه، **فلا يُنقّى بعد رؤيةِ نتيجته**.
٣. أنّ فيه **ما يُكذِّب** لا ما يُصدِّق وحدَه: ثلاثةُ نصوصٍ تنقض
   المقابلةَ المبنيّةَ على الآية، موضوعةٌ فيه عن قصد.
٤. أنّ حدَّ التحقيقِ مكتوبٌ في الأداةِ وفي السجلّ: **صدقُ النقلِ ليس
   صحّةَ الاستدلال**.

`A_CONTAINER_OUTSIDE_THE_TREE_IS_NAMED_NOT_COPIED`: والحاويةُ متنُ
غيرِنا فلا تُودَع؛ يُودَع سجلُّ التحقيقِ وبصمتُها. **وغيابُها يُصنَّف
بسببٍ مكتوبٍ ولا يُصفَّر.**
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Final

import pytest

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[2]
TOOL: Final[Path] = REPOSITORY / "tools" / "quotation_audit.py"
DEPOSIT: Final[Path] = REPOSITORY / "deposits" / "quotation_audit.log"


def _loaded() -> ModuleType:
    spec = importlib.util.spec_from_file_location("quotation_audit", TOOL)
    assert spec is not None and spec.loader is not None
    found = importlib.util.module_from_spec(spec)
    sys.modules["quotation_audit"] = found
    spec.loader.exec_module(found)
    return found


AUDIT: Final[ModuleType] = _loaded()
ABSENT: Final[str] = (
    "الحاويةُ المختومةُ متنُ غيرِ هذه الشجرةِ فلم تُودَع فيها — "
    "والمرساةُ مُعلَنةٌ في الأداةِ ببصمتها"
)
needs_holder = pytest.mark.skipif(not AUDIT.held(), reason=ABSENT)


def test_the_probe_is_declared_with_a_reason_for_every_text() -> None:
    """لكلّ نصٍّ مطلوبٍ سببُ طلبه — **فلا يُزاد مسبارٌ بلا غرض**.

    ويعمل بلا حاوية: المِسبارُ إعلانٌ في الشفرة، وقراءتُه لا تحتاج متنًا.
    """

    assert len(AUDIT.PROBE) >= 21
    for text, why in AUDIT.PROBE:
        assert text.strip() == text and text
        assert len(why) > 6, text
    # ولا نصَّ مكرَّرًا، فالتكرارُ يُضخِّم العدَّ بلا زيادةِ شهادة
    assert len({one for one, _ in AUDIT.PROBE}) == len(AUDIT.PROBE)


def test_the_probe_carries_what_would_refute_the_mapping() -> None:
    """**وفيه ما يُكذِّب لا ما يُصدِّق وحدَه.**

    فالمقابلةُ المبنيّةُ على «علّم آدم الأسماء» تجعل اللغةَ نواةَ تفكيرِ
    الإنسانِ الأوّل. وثلاثةُ نصوصٍ في المصدرِ تنقض ذلك، **موضوعةٌ في
    المِسبارِ عن قصدٍ لا مصادفةً**: فمن طلب ما يُصدِّقه وحدَه لم يقس.
    """

    texts = {one for one, _ in AUDIT.PROBE}
    against = {
        "مسميات الأشياء لا اللغات",
        "عرف الأشياء ولم يعرف اللغات",
        "الألفاظ ليست دلالة على الحقائق",
    }
    assert against <= texts
    for one, why in AUDIT.PROBE:
        if one in against:
            assert "**" in why, one


def test_the_matching_strips_marks_but_never_touches_the_source() -> None:
    """التجريدُ للمقابلةِ وحدَها — **ونسخةٌ تُجرَّد لا أصلٌ يُحرَّر**."""

    assert AUDIT.bare("عَلَّمَ آدَمَ") == AUDIT.bare("علم آدم")
    assert AUDIT.bare("الأســماء") == AUDIT.bare("الأسماء")
    # ولا يُسوّي بين نصّين مختلفَي الحروف
    assert AUDIT.bare("الحقائق") != AUDIT.bare("الحقيقة")


@needs_holder
def test_the_container_is_the_one_whose_digest_is_declared() -> None:
    """المرساةُ بصمةٌ لا مسار — **فنسخةٌ أخرى لا يُقاس عليها**."""

    assert AUDIT.measured_digest() == AUDIT.DIGEST


@needs_holder
def test_every_declared_text_is_found_in_the_container() -> None:
    """وكلُّ مطلوبٍ موجودٌ — **بالنصِّ لا بالرقم**."""

    rows = AUDIT.lines_of()
    hits = AUDIT.probe(rows)
    assert AUDIT.missing(hits) == ()
    assert len(hits) == len(AUDIT.PROBE)


@needs_holder
def test_the_relations_are_eleven_by_counting_not_by_report() -> None:
    """أحدَ عشرَ نوعًا **عدًّا من المتن**، لا نقلًا عن تقرير."""

    numbered, eleventh = AUDIT.relations(AUDIT.lines_of())
    assert numbered == 10
    assert eleventh
    assert numbered + 1 == 11


@needs_holder
def test_the_deposited_log_matches_what_the_tool_derives_now() -> None:
    """والسجلُّ المُودَعُ هو ما تشتقّه الأداةُ الآن — فلا حقلَ حُرِّر بيد."""

    assert DEPOSIT.read_text(encoding="utf-8") == AUDIT.report()


def test_the_limit_of_the_audit_is_written_where_it_is_read() -> None:
    """**وحدُّه مُعلَنٌ في الأداةِ وفي السجلِّ كليهما.**

    فصدقُ النقلِ ليس صحّةَ الاستدلال؛ ومقابلةٌ بين نصٍّ وقراءةٍ سهمُها
    **يُبرهَن وحدَه**. وحدٌّ مكتوبٌ في الشفرةِ ولا يبلغ السجلَّ حدٌّ لا
    يقرؤه من يقرأ النتيجة (العطل ٣٦).
    """

    body = TOOL.read_text(encoding="utf-8")
    assert "`A_QUOTATION_THAT_MATCHES_PROVES_TRANSFER_NOT_INFERENCE`" in body
    assert "`THE_TEXT_IS_THE_WITNESS_NOT_THE_LINE_NUMBER`" in body
    if DEPOSIT.is_file():
        told = DEPOSIT.read_text(encoding="utf-8")
        assert "ولا يُثبت أنّ ما بُنِي" in told
        assert "استدلالٌ يُبرهَن وحدَه" in told
