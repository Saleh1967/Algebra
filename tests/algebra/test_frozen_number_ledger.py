"""فصلُ العدد والمعدود مُجمَّدًا — ما أُعيد حسابُه، وما بقي دَينًا.

**ما يُفحَص ههنا**: أنّ كلَّ رقمٍ عرضه أنبوبٌ خارجيٌّ **يُعاد اشتقاقُه من
أعداده المعروضة**، وأنّ **شكلَ النتيجة مردودٌ ببنائه**.

`I_DID_NOT_RUN_IT_AND_I_DO_NOT_SIGN_IT`: ولا تشجيرَ في هذه الشجرة، **فلا
يُعاد القياسُ ولا يُوقَّع التأويل**. **والمُعادُ حسابُ الأنبوب على أعداده**،
لا **أعدادُه على المصحف**.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = REPOSITORY / "tools" / "number_ledger_seal.py"
NOTE = REPOSITORY / "deposits" / "number_rule_note.md"


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("number_ledger_seal", SEAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_from_its_fields() -> None:
    """البصمةُ تُشتَقّ من الحقول لا تُنقَل."""

    tool = _seal()
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert tool.RECORD_DIGEST.startswith("447bd783")


def test_every_field_is_witnessed_in_the_deposit_and_the_log() -> None:
    """كلُّ حقلٍ له شاهدٌ في الإيداع أو السجلّ، وما خالف يُسمّى."""

    tool = _seal()
    assert tool.verify_against_logs() == []


def test_both_entropies_are_recomputed_from_the_counts() -> None:
    """١٫٤٧١٧ و٠٫٣٤٨٥ تُشتَقّان من العدّ — لا تُنقَلان."""

    tool = _seal()
    record = tool.FROZEN_NUMBERS
    flat = tool.entropy(tuple(two for _, two in record.outcomes))
    assert abs(flat - 1.4717) < 5e-5
    whole = sum(record.places)
    given = math.fsum(
        record.places[index]
        / whole
        * tool.entropy(
            (record.conforming[index], record.places[index] - record.conforming[index])
        )
        for index in range(4)
    )
    assert abs(given - 0.3485) < 5e-5
    assert abs((flat - given) - 1.1232) < 5e-5
    assert abs((flat - given) / flat - 0.7632) < 5e-5
    assert whole == 35 and sum(record.conforming) == 32


def test_two_bits_exhaust_the_four_way_class_with_no_waste() -> None:
    """بتّتان تبلغان الشرطَ التامّ، والسقفُ الخام بتّتان — فلا إسراف."""

    tool = _seal()
    record = tool.FROZEN_NUMBERS
    gains = [float(one) for one in record.step_gains]
    assert record.bits == record.ceiling == 2
    assert abs(math.fsum(gains) - float(record.gain)) < 5e-5
    assert gains[0] == max(gains)
    assert abs(gains[0] / float(record.gain) - 0.8258) < 5e-4
    assert record.steps[1] in record.steps[0]  # والثانيةُ تنقيحٌ لِما قبلها


def test_the_held_out_arms_overlap_so_no_forecast_is_claimed() -> None:
    """مجالا ويلسن متداخلان — والعيّنةُ أصغرُ من أن تحمل دعوى تنبّؤ."""

    tool = _seal()
    record = tool.FROZEN_NUMBERS
    spans = [tool.wilson(hits, tries) for _, hits, tries in record.held_out]
    assert abs(spans[0][0] - 0.548146) < 5e-6
    assert abs(spans[0][1] - 0.929525) < 5e-6
    assert abs(spans[1][0] - 0.301170) < 5e-6
    assert abs(spans[1][1] - 0.751905) < 5e-6
    assert spans[0][0] <= spans[1][1]  # التداخلُ قائم
    assert record.held_out[0][1] / record.held_out[0][2] == 0.8


def test_the_record_refuses_a_field_that_does_not_recompute() -> None:
    """من بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه — سبعُ محاولاتِ تبديل."""

    tool = _seal()
    record = tool.FROZEN_NUMBERS
    for name, value in (
        ("flat", "2.0000"),
        ("given", "0.0000"),
        ("gain", "1.5000"),
        ("share", "0.9000"),
        ("step_gains", ("0.100000", "0.195671")),
        ("bits", 3),
        ("debts", ()),
    ):
        try:
            dataclasses.replace(record, **{name: value})
        except tool.NumberLedgerError:
            continue
        raise AssertionError(f"مرَّ حقلٌ مبدَّلٌ بلا ردّ: {name}")


def test_five_debts_are_carried_and_the_reading_names_its_own_warrant() -> None:
    """خمسةُ دُيونٍ بنصّها — ومنها أنّ قراءةَ المخرجات لي لا نصُّ الأنبوب."""

    tool = _seal()
    record = tool.FROZEN_NUMBERS
    assert len(record.debts) == 5
    joined = " ".join(why for _, why in record.debts)
    assert "توقيعُها ليس فعلي" in joined
    assert "فلا يُوقَّع ولا يُردّ" in joined
    assert "لا حكمٌ على العربيّة" in joined
    assert "سندُها الوحيدُ أنّها تُعيد H" in joined
    assert "وهو إقرارُه لا استنتاجي" in joined
    text = NOTE.read_text(encoding="utf-8")
    assert "ولستُ أنا مَن أجراه ولا مَن يوقّعه" in text
    assert "ولا يُخمَّن" in text
