"""المدخلُ مُشتَقٌّ، وكلُّ وثيقةٍ مولَّدةٍ تُقابَل بمولّدها — دفعةً واحدة.

**ما يحرسه**: أنّ `docs/مدخل.md` يُعاد توليدُه مطابقًا، وأنّ أعدادَه
**تتبع الشجرة** لا الذاكرة، وأنّ كلَّ إشارةٍ فيه تقع على ملفٍّ موجود.
**وأنّ كلَّ وثيقةٍ مولَّدةٍ في الشجرة مطابقةٌ لما يولّده مولّدُها** —
فحصٌ واحدٌ يكتشف المولّداتِ ويقابلها، فلا يُنسى واحدٌ منها.

**ولماذا**: `تقرير-الإنجاز.md` مؤرَّخٌ بيومه ويصدق عليه، **وأعدادُه لا
تتبع الشجرة** — فصار يُقرَأ حالًا راهنةً وليس كذلك. **وما يُقرَأ حالًا
يجب أن يُشتَقّ**، أو فهو تاريخٌ يُقال إنّه تاريخ.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
TOOLS = REPOSITORY / "tools"
DOCS = REPOSITORY / "docs"
ENTRY = DOCS / "مدخل.md"


def _tool(name: str) -> Any:
    path = TOOLS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_entry_is_regenerated_and_never_typed() -> None:
    """المكتوبُ مطابقٌ لما تولّده الأداة — حرفًا بحرف."""

    assert _tool("write_entry.py").render() == ENTRY.read_text(encoding="utf-8")


def test_every_generated_document_matches_its_generator() -> None:
    """تُكتشَف المولّداتُ وتُقابَل — فلا تُنسى وثيقةٌ ولا تُحرَّر بيد."""

    made = _tool("write_entry.py").generated()
    assert len(made) >= 6, made
    for name, maker in made:
        module = _tool(Path(maker).name)
        written = (DOCS / name).read_text(encoding="utf-8")
        assert module.render() == written, name


def test_the_counts_follow_the_tree_not_the_memory() -> None:
    """أعدادُ المدخل تُعاد من الشجرة، لا تُقارَن بثابتٍ مكتوب."""

    entry = _tool("write_entry.py")
    index = _tool("write_seal_index.py")
    written = ENTRY.read_text(encoding="utf-8")
    seals = index.gather()
    records = index.records()
    marks = sum(int(one["count"]) for one in seals)
    flaws = re.findall(
        r"^## [٠-٩]+\) ",
        (DOCS / "سجل-الأعطال.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    for number in (len(seals), marks, len(records), len(flaws)):
        assert entry.grouped(number) in written, number
    assert len(seals) > 30 and marks > 200 and len(flaws) > 20


def test_every_pointer_in_the_entry_resolves() -> None:
    """كلُّ إشارةٍ تقع على ملفٍّ موجود — ولا رابطَ معلَّق."""

    written = ENTRY.read_text(encoding="utf-8")
    links = re.findall(r"\]\((?!https?:)([^)]+)\)", written)
    assert links
    for one in links:
        assert (DOCS / one).resolve().is_file(), one


def test_the_dated_report_is_named_as_dated() -> None:
    """`تقرير-الإنجاز.md` تاريخٌ، ويُقال إنّه تاريخ."""

    written = ENTRY.read_text(encoding="utf-8")
    assert "`تقرير-الإنجاز.md` **مؤرَّخٌ بيومه**" in written
    assert "ولا تُؤخَذ أعدادُه حالًا راهنة" in written
    report = (DOCS / "تقرير-الإنجاز.md").read_text(encoding="utf-8")
    assert "**التاريخ**:" in report.splitlines()[2]


def test_the_standing_caveats_are_carried_not_buried() -> None:
    """التحفّظاتُ القائمةُ في صدر المدخل، ولكلٍّ موضعٌ يُقرأ فيه."""

    entry = _tool("write_entry.py")
    written = ENTRY.read_text(encoding="utf-8")
    assert len(entry.STANDING) == 8
    for title, _body, where in entry.STANDING:
        assert title in written, title
        assert (DOCS / where).resolve().is_file(), where
    assert "أبالبسملات أم بدونها" in written
    assert "ولا يُسمّى السطرُ جملةً ولا اللفظُ كلمة" in written
    assert "والنقلُ ليس السببيّة" in written  # ولا يُقرأ سببًا يومًا
    assert "ولا يُوقَّع تأويلٌ ولا يُنقَل رقمٌ بين مقامين" in written
