"""سقوطُ «ستيرلنغ مع الجشع» مُجمَّدًا — والسقوطُ أولى بالتجميد من الصمود.

**ما يُفحَص ههنا**: أنّ بصمةَ السجلّ تُشتَقّ من حقوله، وأنّ كلَّ حقلٍ
مقابَلٌ بالسجلّين المُودَعين، وأنّ **شكلَ السقوط مردودٌ ببنائه** — فمن
بدّل رقمًا ليُظهِر اتّفاقًا حيث كان خلاف، أو خلافًا حيث كان اتّفاق، رُدَّ
سجلُّه.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = REPOSITORY / "tools" / "stirling_greedy_seal.py"


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("stirling_greedy_seal", SEAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_from_its_fields() -> None:
    """البصمةُ تُشتَقّ من الحقول لا تُنقَل."""

    tool = _seal()
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert tool.RECORD_DIGEST.startswith("8264454f")


def test_every_field_is_witnessed_in_the_deposited_logs() -> None:
    """كلُّ حقلٍ له شاهدٌ في السجلّ وفي شاهد عدمِ التبدّل."""

    tool = _seal()
    assert tool.verify_against_logs() == []


def test_the_refutation_itself_is_the_construction_rule() -> None:
    """المعياران يتّفقان، والبتّةُ لم تعد، والإسرافُ في مقامٍ واحد."""

    tool = _seal()
    record = tool.FROZEN_STIRLING
    assert record.bits_entropy == record.bits_permutation == (3, 2)
    assert record.disagreements == 0
    assert record.needed == (2, 2)
    assert record.bits_permutation[0] > record.needed[0]
    assert record.bits_permutation[1] == record.needed[1]
    assert record.smallest_first == (1, 2)
    assert float(record.identity_drift) < 1e-9
    assert float(record.spread) > 0


def test_the_unsearched_space_is_derived_from_the_recurrence() -> None:
    """أرقامُ ستيرلنغ تُشتَقّ بقاعدة النمط — ولا جدولَ في السجلّ."""

    from algebra.stirling import bell, subsets

    tool = _seal()
    record = tool.FROZEN_STIRLING
    assert record.blocks == tuple(
        (one, subsets(record.cells, one)) for one in range(2, record.cells + 1)
    )
    assert record.visited == bell(record.cells) - 1 == 14
    assert record.cells - 1 == 3 < record.visited


def test_the_record_refuses_a_field_that_does_not_hold_the_shape() -> None:
    """من بدّل رقمًا ليُلطّف السقوطَ رُدَّ سجلُّه — ستُّ محاولاتِ تبديل."""

    tool = _seal()
    record = tool.FROZEN_STIRLING
    for name, value in (
        ("bits_permutation", (2, 2)),
        ("disagreements", 1),
        ("identity_drift", "0.01"),
        ("spread", "-1.0"),
        ("trivial_edge", "0.5"),
        ("blocks", ((2, 6), (3, 6), (4, 1))),
    ):
        try:
            dataclasses.replace(record, **{name: value})
        except tool.StirlingGreedyError:
            continue
        raise AssertionError(f"مرَّ حقلٌ مبدَّلٌ بلا ردّ: {name}")


def test_the_trivial_edge_is_kept_beside_the_honest_one() -> None:
    """الطرفُ التافهُ محمولٌ في السجلّ مع الصادق — فلا يُقرأ وحدَه."""

    tool = _seal()
    record = tool.FROZEN_STIRLING
    assert float(record.trivial_edge) == 0.0
    assert float(record.honest_edge) > float(record.trivial_edge)
    assert abs(float(record.honest_edge) - 1.873581) < 5e-7
