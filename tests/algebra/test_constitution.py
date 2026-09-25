"""الدستورُ مقيَّدٌ بنفسه — لا مادّةَ بلا مُنفِّذ، ولا مانعَ بلا مادّة.

**ما يُفحَص ههنا**: أنّ كلَّ مادّةٍ في `دستور-القياس.md` تحمل **موضعًا
موجودًا في الشجرة**؛ وأنّ كلَّ مانعٍ منصوبٍ في
`test_sealed_conditions_audit` **مذكورٌ مادّةً**؛ وأنّ كلَّ عطلٍ تُحيل
إليه مادّةٌ **مُسجَّلٌ في سجلّ الأعطال**.

`A_CONSTITUTION_THAT_CANNOT_BE_CHECKED_IS_PROSE`: ودستورٌ لا يُفحَص نثرٌ
يتبدّل ولا يُعرَف تبدّلُه — **وذاك عينُ ما يمنعه**.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "write_constitution.py"
PAPER = REPOSITORY / "docs" / "دستور-القياس.md"
FLAWS = REPOSITORY / "docs" / "سجل-الأعطال.md"
AUDIT = REPOSITORY / "tests" / "algebra" / "test_sealed_conditions_audit.py"
EASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("write_constitution", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_document_matches_its_generator_byte_for_byte() -> None:
    """الوثيقةُ مولَّدةٌ، ولا تُحرَّر بيد."""

    assert PAPER.read_text(encoding="utf-8") == _tool().render()


def test_every_article_names_a_place_that_exists_in_the_tree() -> None:
    """مادّةٌ بلا موضعٍ موجودٍ **تُردّ** — وهذا ما يجعله دستورًا لا نثرًا."""

    tool = _tool()
    every = tool.articles()
    assert len(every) >= 25
    for number, chapter, (text, _flaw, where, _limit) in every:
        assert chapter.strip(), number
        assert len(text) >= 25, number  # نصٌّ لا شعار
        assert (REPOSITORY / where).exists(), f"المادّة {number}: {where}"


def test_every_flaw_an_article_cites_is_recorded_in_the_register() -> None:
    """كلُّ عطلٍ تُحيل إليه مادّةٌ **مُسجَّلٌ بعنوانه** في سجلّ الأعطال."""

    tool = _tool()
    register = FLAWS.read_text(encoding="utf-8")
    cited = {row[1] for _, _, row in tool.articles() if row[1]}
    assert len(cited) >= 8
    for flaw in cited:
        assert f"## {flaw})" in register, flaw
    highest = max(
        int(one.translate(EASTERN))
        for one in re.findall(r"^## ([٠-٩]+)\)", register, re.MULTILINE)
    )
    assert highest == 24
    assert all(int(one.translate(EASTERN)) <= highest for one in cited)


def test_every_guard_in_the_audit_is_carried_as_an_article() -> None:
    """مانعٌ منصوبٌ ولا مادّةَ له **يُردّ** — فلا يقف حرسٌ خارجَ الدستور."""

    tool = _tool()
    guarded = {where for _, _, (_, _, where, limit) in tool.articles() if not limit}
    assert "tests/algebra/test_sealed_conditions_audit.py" in guarded
    audit = AUDIT.read_text(encoding="utf-8")
    for guard in ("**المانعُ أ)**", "**المانعُ ب)**", "**المانعُ ج)**", "**المانعُ د)**"):
        assert guard.strip("*").replace("**", "") in audit or guard[2:-2] in audit
    written = PAPER.read_text(encoding="utf-8")
    for born in ("٧", "٨", "١٢", "١٧"):
        assert f"**وَلَدها العطل {born}**" in written, born


def test_the_articles_without_an_automatic_guard_are_named_not_buried() -> None:
    """ما ليس له مانعٌ آليٌّ **يُقال**، ويُجمَع في باب مستقلٍّ يُقرَأ."""

    tool = _tool()
    loose = [one for one in tool.articles() if one[2][3]]
    assert len(loose) == 2
    written = PAPER.read_text(encoding="utf-8")
    assert "## ما لا يُنفِّذه الدستورُ آليًّا" in written
    for number, _, row in loose:
        assert row[3] in written, number
        assert "بلا مانعٍ آليّ" in written
    assert "وكاتبُ ختمٍ قد يُغفِل ما في الشجرة" in written


def test_the_constitution_refuses_an_article_born_of_an_opinion() -> None:
    """القاعدةُ الحاكمة: **من أراد مادّةً فليأتِ بعطلها**."""

    written = PAPER.read_text(encoding="utf-8")
    assert "**كلُّ مادّةٍ ههنا وُلِدت من خطأٍ وقع وسُجِّل.**" in written
    assert "وإلّا فهي رأيٌ لا دستور" in written
    tool = _tool()
    numbers = [one for one, _, _ in tool.articles()]
    assert numbers == list(range(1, len(numbers) + 1))  # ترقيمٌ مُشتَقٌّ لا مكتوب
