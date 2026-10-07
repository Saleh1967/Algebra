"""سجلُّ الانقلاب مُقفَلٌ — بصمتُه تُعاد، وحقولُه تُقابَل بالسجلّات.

**ما يحرسه**: أنّ **كلَّ حقلٍ** في `FROZEN_INVERSION` مشهودٌ في سجلٍّ
مُودَعٍ نصًّا، وأنّ بصمةَ السجلّ **مُشتَقّةٌ** من حقوله لا منقولة، وأنّ
**الانقلابَ نفسَه شرطُ بناء**: لا يُقفَل سجلٌّ لا يحمله.

**ولماذا**: صار الانقلابُ يُذكَر نثرًا — «الأكثرُ وقوعًا ليس الأكبرَ ربحًا».
والنثرُ يتبدّل ولا يُعرَف تبدّلُه؛ وقد نقلتُ من قبلُ بصمةً بذيلٍ مُختلَق
(العطل ١٦). **فما يُستشهَد به يُجمَّد، أو فهو نثر.**
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import fields, replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "inversion_seal.py"

DIGEST = "ca75f300ba9125e3cd45cbf1f43eb6482d2ae6cdf40d1876eeb5fbc76ee7278a"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("inversion_seal", TOOL)
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
    moved = replace(tool.FROZEN_INVERSION, pairs_looked=201)
    assert tool.rederive_record_digest(moved) != DIGEST


def test_every_field_is_witnessed_in_a_deposited_log() -> None:
    """لا حقلَ في السجلّ المُقفَل إلّا وله شاهدٌ نصّيٌّ في سجلٍّ مُودَع."""

    tool = _tool()
    complaints = tool.verify_against_logs()
    assert complaints == [], complaints
    assert len(fields(tool.FROZEN_INVERSION)) == 28


def test_the_inversion_is_a_construction_rule_not_a_description() -> None:
    """لا يُقفَل سجلٌّ يكون فيه العددُ الخامُ أقربَ إلى الربح من المشتَقّ."""

    tool = _tool()
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, rho_derived="0.1000")
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, median_chosen_rank=3)
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, median_count_chosen=999)
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, rank_agreed=900)


def test_the_identity_and_the_ceiling_cannot_be_softened() -> None:
    """`Σ p·PMI = I` هويّةٌ، وتجاوزُ الرتبة الأولى شرطُ هذا السجلّ."""

    tool = _tool()
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, sum_p_pmi="1.300000")
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, ceiling_ratio="0.9000")
    with pytest.raises(tool.InversionSealError):
        replace(tool.FROZEN_INVERSION, threshold_agreed=100)


def test_the_frozen_numbers_are_the_ones_already_published() -> None:
    """ما جُمِّد هو ما نُشِر — لا نسخةٌ أخرى منه."""

    record = _tool().FROZEN_INVERSION
    assert record.rho_count == "0.1805" and record.rho_derived == "0.9759"
    assert record.rank_agreed == 27 and record.states == 1_530
    assert record.block_saving == 824_618
    assert record.first_order_ceiling == 467_355
    assert record.mutual_information == record.sum_p_pmi == "1.303600"


def test_the_paper_is_generated_from_the_record_and_never_typed() -> None:
    """الوثيقةُ تُولَّد من السجلّ المُقفَل — فمقارنتُها به مطابقةٌ تامّة."""

    paper = REPOSITORY / "docs" / "الانقلاب-المجمَّد.md"
    tool = REPOSITORY / "tools" / "write_inversion_paper.py"
    spec = importlib.util.spec_from_file_location("write_inversion_paper", tool)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    written = paper.read_text(encoding="utf-8")
    assert module.render() == written
    assert DIGEST in written  # فالوثيقةُ تحمل ختمَ سجلّها
    assert "مقياسان لا مقياس" in written
    assert "شرطُ بناءٍ في السجلّ لا وصفٌ فيه" in written
