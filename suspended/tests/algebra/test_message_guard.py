"""المتنُ المُودَعُ في التاريخ يُقرَأ قبل إرساله — والمسجَّلُ منه لا يُكرَّر.

**العطلُ الذي يحرسه (٣٣)**: كتبتُ متنَ دفعةِ دمجِ الطلب ٥٢ **في حقلِ
الأداة مباشرةً**، فدخل فيه `</commit_message>` و`</invoke>` — وسمَي
بروتوكولٍ صارا نصًّا في `a13e735` على `main`. وأختُها `ca09705` كُتِبت في
ملفٍّ ثمّ أُودِعت بـ`git commit -F -` **فسلِمت**. فالفرقُ ليس عنايةً بل
**موضعَ الكتابة**: ما يُكتَب في ملفٍّ يُقرَأ، وما يُكتَب في حقلٍ يُرسَل بلا
قراءة.

**ولا يُحرَّر المتنُ بعد نشره**: إعادةُ كتابةِ تاريخٍ منشورٍ أسوأُ من الوسم،
فيبقى `a13e735` ويُقرَأ بحدِّه — **مُسمًّى في `REGISTERED` لا مدفونًا**.

`THE_REGISTER_IS_A_CEILING_NOT_AN_EXCUSE`: والمسجَّلُ **واحدٌ بعينه ببصمته
ووسومه**؛ فلو حمل غيرُه وسمًا، أو حمل هو وسمًا آخر، **رُدَّ**. فالتسجيلُ
يمنع التكرارَ ولا يأذن به.

`AND_WHAT_IT_CANNOT_REACH_IS_CLASSIFIED_NOT_ZEROED`: ونسخةُ CI ضحلةٌ لا
تحمل إلّا دفعةً واحدة، **فلا يُقرَأ سكوتُها براءةً**: يُتخطّى المسحُ بسببٍ
مُسمًّى (`SHALLOW`)، **وذلك تصنيفٌ لا تصفير**.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOLS = REPOSITORY / "tools"
FLAWS = REPOSITORY / "docs" / "سجل-الأعطال.md"


def _tool() -> Any:
    path = TOOLS / "message_guard.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GUARD = _tool()
SHALLOW = "نسخةٌ ضحلة: التاريخُ لا يبلغه المسحُ — والحالُ مُصنَّفةٌ لا مُصفَّرة"
needs_history = pytest.mark.skipif(GUARD.shallow_here(), reason=SHALLOW)


def test_the_tag_that_slipped_is_refused_by_name() -> None:
    """الوسمُ الذي سرَب بعينه يُرَدّ — **والفحصُ يذكره لا يصفه**."""

    said = GUARD.objections("والكبسُ يطويه.</commit_message>\n</invoke>")
    assert len(said) == 2
    assert any("</commit_message>" in one for one in said)
    assert any("</invoke>" in one for one in said)


def test_a_tag_inside_backticks_is_not_a_stray_tag() -> None:
    """ووسمٌ في شفرةٍ مقصودٌ لا سارب — فلا يُرَدّ متنٌ يشرح وسمًا."""

    assert GUARD.objections("يُذكَر `</invoke>` نصًّا في الشرح") == ()
    assert GUARD.objections("و`<sel>` علامةُ الاختيار") == ()
    assert GUARD.objections("<sel> بلا شفرةٍ — وهي مأذونةٌ باسمها") == ()


def test_an_empty_message_is_refused() -> None:
    """ومتنٌ خالٍ لا يُودَع — فدفعةٌ بلا قولٍ لا تُقرَأ."""

    assert GUARD.objections("   \n\t ") != ()
    assert GUARD.objections("ادمجْ") == ()


def test_reading_from_a_file_is_the_place_the_message_is_read(
    tmp_path: Path,
) -> None:
    """والقراءةُ من ملفٍّ هي موضعُ الردّ — فما مرَّ عليها يُودَع كما هو."""

    clean = tmp_path / "clean.txt"
    clean.write_text("متنٌ سليمٌ يُودَع\n", encoding="utf-8")
    assert GUARD.read_message(clean) == "متنٌ سليمٌ يُودَع\n"

    broken = tmp_path / "broken.txt"
    broken.write_text("متنٌ ثمّ</invoke>\n", encoding="utf-8")
    with pytest.raises(GUARD.MessageError) as why:
        GUARD.read_message(broken)
    assert "</invoke>" in str(why.value)


@needs_history
def test_no_commit_carries_a_stray_tag_beyond_the_registered_one() -> None:
    """ولا دفعةَ فيها وسمٌ ساربٌ إلّا المسجَّلةَ — **وما زاد يُرَدّ باسمه**."""

    extra = GUARD.unregistered()
    assert extra == {}, {one[:10]: two for one, two in extra.items()}


@needs_history
def test_the_registered_flaw_is_actually_present_and_not_a_dead_entry() -> None:
    """والمسجَّلُ **موجودٌ فعلًا** — فلا يُترَك في القائمة استثناءٌ ميّت."""

    found = GUARD.history_stray()
    for digest, tags in GUARD.REGISTERED.items():
        assert found.get(digest) == tags, digest
    assert len(found) == len(GUARD.REGISTERED)


def test_the_flaw_is_registered_in_the_register_with_its_digest() -> None:
    """والعطلُ ٣٣ مكتوبٌ في السجلّ ببصمةِ دفعته — فلا يُحرَس ما لا يُقال."""

    register = FLAWS.read_text(encoding="utf-8")
    assert "## ٣٣)" in register
    for digest in GUARD.REGISTERED:
        assert digest[:7] in register, digest


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ: يحرس الشكلَ لا المعنى، وما لا يبلغه يُصنَّف لا يُصفَّر."""

    said = (TOOLS / "message_guard.py").read_text(encoding="utf-8")
    assert "`AND_THE_GUARD_DOES_NOT_READ_MEANING`" in said
    assert "**ولا يحرس صوابَ المتن**" in said
    here = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_WHAT_IT_CANNOT_REACH_IS_CLASSIFIED_NOT_ZEROED`" in here
    assert "`THE_REGISTER_IS_A_CEILING_NOT_AN_EXCUSE`" in here
