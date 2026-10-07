"""سجلُّ السلّم مُقفَلٌ — بصمتُه تُعاد، وحقولُه تُقابَل بالسجلّ المُودَع.

**ما يحرسه**: أنّ كلَّ درجةٍ في `FROZEN_LADDER` مشهودةٌ **سطرًا كاملًا**
في السجلّ، وأنّ البصمةَ **مُشتَقّةٌ** لا منقولة، وأنّ **شكلَ السلّم شرطُ
بناء**: لا يُقفَل سجلٌّ لا يحمله.

**ولماذا**: الأسماءُ تُنقَل ولا تُراجَع — وقد سمّيتُ اللفظَ كلمةً مرّةً
(العطل ١٩). فتُجمَّد الدرجةُ باسمها ورقمها معًا، **وتُحمَل معها الأربعةُ
التي لا تُرخّصها البايتات** فلا يُقرأ السلّمُ يومًا كأنّه بلغ الجملة.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import fields, replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "ladder_seal.py"
PAPER = REPOSITORY / "docs" / "السلّم-المجمَّد.md"

DIGEST = "426f7fc806766ef1006e9be7d37214787125509f2e68c9e4eed7a4d2d2b472ad"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("ladder_seal", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_and_pinned() -> None:
    """البصمةُ تُشتَقّ من الحقول — وتبديلُ حقلٍ يُغيّرها."""

    tool = _tool()
    assert tool.rederive_record_digest() == DIGEST
    assert tool.RECORD_DIGEST == DIGEST
    moved = replace(tool.FROZEN_LADDER, counts=(364_747, 135_603, 78_245, 6_235))
    assert tool.rederive_record_digest(moved) != DIGEST


def test_every_rung_is_witnessed_as_a_whole_line_in_the_log() -> None:
    """لا درجةَ في السجلّ المُقفَل إلّا ولها سطرٌ تامٌّ في المُودَع."""

    tool = _tool()
    complaints = tool.verify_against_logs()
    assert complaints == [], complaints
    assert len(fields(tool.FROZEN_LADDER)) == 13


def test_the_shape_of_the_ladder_is_a_construction_rule() -> None:
    """لا يُقفَل سجلٌّ يرتفع فيه الملحَقُ أو ينتقل فيه أرخصُ محجوز."""

    tool = _tool()
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, inside_unit=("1.0", "2.0", "3.0", "4.0"))
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, outside_unit=("1.0", "9.0", "8.0", "7.0"))
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, missing=("0.9", "0.5", "0.2", "0.0"))
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, gaps=("0.0230", "0.0287", "0.0272", "1.5"))
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, stirling=("718.3", "-1.0", "32137.3", "8785.2"))


def test_the_vacant_levels_cannot_be_dropped_or_left_bare() -> None:
    """أربعةٌ بأسبابها — ولا تُطوى ولا تُزاد ولا تُترَك بلا سبب."""

    tool = _tool()
    with pytest.raises(tool.LadderSealError):
        replace(tool.FROZEN_LADDER, vacant=tool.FROZEN_LADDER.vacant[:3])
    with pytest.raises(tool.LadderSealError):
        replace(
            tool.FROZEN_LADDER,
            vacant=tuple((name, "قصير") for name, _why in tool.FROZEN_LADDER.vacant),
        )
    assert [name for name, _ in tool.FROZEN_LADDER.vacant] == [
        "الكلمةُ المفردة",
        "التركيبُ الإسناديّ",
        "التركيبُ المزجيّ",
        "الجملة",
    ]


def test_the_frozen_numbers_are_the_ones_already_published() -> None:
    """ما جُمِّد هو ما نُشِر — لا نسخةٌ أخرى منه."""

    r = _tool().FROZEN_LADDER
    assert r.outside_unit == ("5.6059", "3.6549", "4.2118", "6.9369")
    assert r.inside_unit == ("5.6048", "3.6155", "2.4926", "0.2154")
    assert r.counts == (364_747, 135_603, 78_245, 6_236)
    assert r.names[2] == "م٢ اللفظُ المفرد"  # لفظٌ لا كلمة


def test_the_paper_is_generated_from_the_record_and_never_typed() -> None:
    """الوثيقةُ تُولَّد من السجلّ المُقفَل — فمقارنتُها به مطابقةٌ تامّة."""

    tool = REPOSITORY / "tools" / "write_ladder_paper.py"
    spec = importlib.util.spec_from_file_location("write_ladder_paper", tool)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    written = PAPER.read_text(encoding="utf-8")
    assert module.render() == written
    assert DIGEST in written
    assert "ولم يُسمَّ السطرُ جملةً ولا اللفظُ كلمة" in written
    assert "شرطُ بناءٍ في السجلّ لا وصفٌ فيه" in written
