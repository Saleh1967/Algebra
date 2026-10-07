"""تناسقُ المستودع: **العددُ الواحدُ يُقال مرّةً واحدةً في كلّ موضع**.

**العطلُ الذي يحرسه**: في هذه الشجرة **ثلاثُ وثائقَ مولَّدةٍ تَعُدّ الشيءَ
نفسَه**: الجذرُ (`README.md`) والمدخلُ (`docs/مدخل.md`) وفهرسُ الأختام.
وكلٌّ يُولَّد بمولّدٍ مستقلّ، **فيُمكِن أن يُعاد توليدُ أحدها ويُنسى
الآخر** — فيقول الجذرُ «٤٦ ختمًا» والمدخلُ «٤٥»، **وكلاهما مطابقٌ
لمولّده**، فيمرّان على حراسة التوليد ولا يمرّان على القارئ.

`AGREEMENT_IS_A_SEPARATE_PROPERTY_FROM_DERIVATION`: **فالاشتقاقُ ليس
التناسق**. حراسةُ التوليد تسأل: «أَيطابق الملفُّ مولّدَه؟» — **ولا تسأل**:
«أَيطابق المولّدُ مولّدًا آخرَ في العددِ المشترك؟» وهذا الفحصُ يسأل
الثانية.

`AND_THE_TREE_IS_THE_ARBITER_NOT_EITHER_DOCUMENT`: ولا يُقابَل مستندٌ
بمستندٍ وحدَه: **يُعَدُّ من الشجرة** ثمّ يُطلَب من الجميع أن يوافقوا
العدَّ المُشتَقّ. فإن اتّفقت وثيقتان على خطأٍ **رُدَّتا معًا**.

`AND_WHAT_IT_DOES_NOT_GUARD_IS_NAMED`: **وحدُّه مُعلَن**: يحرس **الأعدادَ
المشتركةَ** بين الوثائق، **ولا يحرس نثرًا** — وثيقةٌ تقول قولًا يخالف
أخرى تمرُّ عليه. ولا يحرس **صوابَ** العدّ في الشجرة، بل **اتّفاقَ
الجميعِ عليه**.
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
DEPOSITS = REPOSITORY / "deposits"
ROOT = REPOSITORY / "README.md"
ENTRY = DOCS / "مدخل.md"
FLAWS = DOCS / "سجل-الأعطال.md"
CONSTITUTION = DOCS / "دستور-القياس.md"


def _tool(name: str) -> Any:
    path = TOOLS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _counts() -> dict[str, int]:
    """الأعدادُ المشتركةُ **مُشتَقّةً من الشجرة**، لا من وثيقة."""

    index = _tool("write_seal_index.py")
    entry = _tool("write_entry.py")
    seals = index.gather()
    return {
        "seals": len(seals),
        "marks": sum(int(one["count"]) for one in seals),
        "records": len(index.records()),
        "flaws": len(
            re.findall(
                r"^## [٠-٩]+\) ", FLAWS.read_text(encoding="utf-8"), re.MULTILINE
            )
        ),
        "logs": len(sorted(DEPOSITS.glob("*.log"))),
        "papers": len(sorted({one.name for one in DOCS.glob("*.md")})),
        "generated": len(entry.generated()),
    }


def test_the_root_and_the_entry_agree_on_every_shared_count() -> None:
    """الجذرُ والمدخلُ يقولان العددَ نفسَه — ولا يُقال مرّتين بوجهين."""

    entry = _tool("write_entry.py")
    root = ROOT.read_text(encoding="utf-8")
    inside = ENTRY.read_text(encoding="utf-8")
    shared = _counts()
    for name in ("seals", "marks", "records", "flaws", "papers", "generated"):
        shown = entry.grouped(shared[name])
        assert shown in root, (name, shown)
        assert shown in inside, (name, shown)


def test_every_count_the_root_shows_is_derived_from_the_tree() -> None:
    """وكلُّ عددٍ في جدول الجذر **مُشتَقٌّ**، ولا واحدَ منه مكتوبٌ بيد."""

    root = _tool("write_root.py")
    assert root.render() == ROOT.read_text(encoding="utf-8")
    shared = _counts()
    written = ROOT.read_text(encoding="utf-8")
    for name in ("seals", "marks", "records", "flaws", "logs"):
        assert root.grouped(shared[name]) in written, name


def test_the_flaw_register_and_the_constitution_agree_on_the_highest_flaw() -> None:
    """أعلى عطلٍ في السجلّ لا يسبقه ما تُحيل إليه مادّةٌ — ولا فجوةَ في الترقيم."""

    eastern = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    register = FLAWS.read_text(encoding="utf-8")
    numbers = sorted(
        int(one.translate(eastern))
        for one in re.findall(r"^## ([٠-٩]+)\)", register, re.MULTILINE)
    )
    assert numbers == list(range(1, len(numbers) + 1)), numbers
    tool = _tool("write_constitution.py")
    cited = {
        int(row[1].translate(eastern))
        for _number, _chapter, row in tool.articles()
        if row[1]
    }
    assert cited
    assert max(cited) <= max(numbers)
    for one in cited:
        assert one in numbers, one


def test_every_generated_paper_is_reachable_from_the_entry() -> None:
    """كلُّ وثيقةٍ مولَّدةٍ مذكورةٌ في جدول المدخل — فلا مولَّدَ خارجَ الفهرس."""

    entry = _tool("write_entry.py")
    inside = ENTRY.read_text(encoding="utf-8")
    made = entry.generated()
    assert len(made) >= 18
    for name, maker in made:
        assert f"[`{name}`]({name})" in inside, name
        assert f"`{maker}`" in inside, maker
        assert (DOCS / name).is_file(), name
        assert (REPOSITORY / maker).is_file(), maker


def test_the_root_certificate_covers_the_folding_claim() -> None:
    """شهادةُ الجذر تذكر **الطيَّ** — فلا يبقى أشدُّ ما في الشجرة خارجَها."""

    tool = _tool("root_certificate.py")
    sealed = tool.FROZEN_ADOPTION
    body = " ".join(" ".join(sealed.certifies).split())
    assert "يُفَكّ" in body or "تقابل" in body, body[:200]
    assert tool.verify_against_root() == []


def test_the_counts_are_plural_and_growing_not_placeholders() -> None:
    """والأعدادُ حقيقيّةٌ لا صفرٌ ولا واحدٌ — فلا يمرّ جدولٌ خاوٍ."""

    shared = _counts()
    assert shared["seals"] > 40
    assert shared["marks"] > 300
    assert shared["flaws"] > 25
    assert shared["logs"] > 40
    assert shared["generated"] >= 18
    assert shared["papers"] >= shared["generated"]


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ: يحرس الأعدادَ المشتركةَ لا النثرَ، ولا صوابَ العدّ."""

    text = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_WHAT_IT_DOES_NOT_GUARD_IS_NAMED`" in text
    assert "**ولا يحرس نثرًا**" in text
    assert "بل **اتّفاقَ\nالجميعِ عليه**" in text
