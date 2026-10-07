"""فصلُ الحصر والاستثناء مُجمَّدًا — ما أُعيد حسابُه، وما لم يُنشَر فلم يُبنَ.

**ما يُفحَص ههنا**: أنّ المعلوماتِ المنشورةَ **تُعاد من تفصيلها** بتصحيح
الانحياز من الرتبة الأولى، وأنّ **عددًا لا يُغلِق يُسمّى**، وأنّ **إسرافَ
الجشع مقيسٌ لا مرويّ**، وأنّ **ما لم يُنشَر لم يُبنَ**.

`THE_ESTIMATOR_WAS_FOUND_NOT_ASSUMED`: والتقديرُ الخامُ لا يوافق المنشورَ،
**وتصحيحُ ميلر–مادو يُعيد الرقمين معًا إلى أربع منازل**. **فلم يُسمَّ
المنشورُ خطأً**، بل سُمّي التقديرُ باسمه.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = REPOSITORY / "tools" / "hasr_ledger_seal.py"
NOTE = REPOSITORY / "deposits" / "hasr_rule_note.md"


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("hasr_ledger_seal", SEAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_from_its_fields() -> None:
    """البصمةُ تُشتَقّ من الحقول لا تُنقَل."""

    tool = _seal()
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert tool.RECORD_DIGEST.startswith("6d6fd210")


def test_every_field_is_witnessed_in_the_deposit_and_the_logs() -> None:
    """كلُّ حقلٍ له شاهدٌ في الإيداع أو السجلّات الثلاثة."""

    tool = _seal()
    assert tool.verify_against_logs() == []


def test_both_published_informations_return_only_under_the_correction() -> None:
    """الخامُ لا يوافق المنشور، وميلر–مادو يُعيده — فالمقدارُ مُشتَقّ."""

    tool = _seal()
    record = tool.FROZEN_HASR
    flat = tool.binary(record.exception / record.total)
    assert abs(flat - 0.630974) < 5e-6
    for name, cells, expected in (
        ("م١", record.sign_cells, 0.0079),
        ("م٢", record.case_cells, 0.0378),
    ):
        rows = list(cells)
        seen = sum(one for one, _ in rows)
        if seen < record.total:
            rows.append(
                (record.total - seen, record.exception - sum(two for _, two in rows))
            )
        raw = flat - tool.conditional(tuple(rows))
        fixed = raw - tool.miller_madow(len(rows), record.total)
        assert abs(fixed - expected) < 5e-5, name
        assert raw - expected > 1e-4, name  # والخامُ يعلو المنشورَ بيقين
    assert abs(tool.miller_madow(2, 662) - 0.001090) < 5e-7


def test_only_one_of_the_two_published_counts_closes_the_arithmetic() -> None:
    """١٠٥ يُغلِق وحدَه، و١٠٢ لا — والعددان معروضان كلاهما."""

    tool = _seal()
    record = tool.FROZEN_HASR
    assert record.exception == 105 and record.rejected_count == 102
    assert sum(two for _, two in record.sign_cells) == record.exception
    assert sum(one for one, _ in record.sign_cells) == record.total
    assert record.restriction + record.exception == record.total
    assert record.restriction + record.rejected_count != record.total
    text = NOTE.read_text(encoding="utf-8")
    assert "والعددان لا يجتمعان" in text


def test_the_greedy_ladder_spent_a_bit_it_did_not_need() -> None:
    """صرف ثلاثَ بتّاتٍ حيث تكفي اثنتان — شاهدٌ مقيسٌ على أنّ الجشعَ غيرُ مبرهَن."""

    tool = _seal()
    record = tool.FROZEN_HASR
    gains = [float(one) for one in record.ladder_gains]
    assert record.bits_spent == 3 and record.bits_needed == 2
    assert record.bits_spent > record.bits_needed
    assert gains[0] == max(gains)
    assert abs(gains[0] / math.fsum(gains) - 0.868450) < 5e-6
    flat = tool.binary(record.exception / record.total)
    rows = list(record.case_cells)
    rows.append(
        (
            record.total - sum(one for one, _ in rows),
            record.exception - sum(two for _, two in rows),
        )
    )
    assert abs(math.fsum(gains) - (flat - tool.conditional(tuple(rows)))) < 5e-6


def test_the_classifier_learned_to_say_one_word_always() -> None:
    """أصاب من الاستثناء واحدًا من اثنين وسبعين — والزيادةُ موضعٌ من ٣٤١."""

    tool = _seal()
    record = tool.FROZEN_HASR
    right, wrong, missed, caught = record.confusion
    assert (right, wrong, missed, caught) == (269, 0, 71, 1)
    assert right + caught == record.held_out[0][1]
    assert right == record.held_out[1][1]
    assert caught / (missed + caught) < 0.02
    assert (record.held_out[0][1] - record.held_out[1][1]) == 1
    left = tool.binary(record.exception / record.total) - 0.0378
    assert abs(left / tool.binary(record.exception / record.total) - 0.9400) < 5e-4


def test_what_was_not_published_was_not_rebuilt() -> None:
    """ثلاثةُ ملامحَ وجداءٌ — تُسمّى ولا تُعاد ولا تُصدَّق ولا تُكذَّب."""

    tool = _seal()
    record = tool.FROZEN_HASR
    assert len(record.unbuilt) == 4
    joined = " ".join(record.unbuilt)
    assert "بلا تفصيلٍ منشور" in joined
    assert "فلا سلّمَ عبر ملمحين" in joined
    assert len(record.published) == 2  # والمُعادُ ملمحان لا خمسة


def test_the_record_refuses_a_field_that_does_not_recompute() -> None:
    """من بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه — ستُّ محاولاتِ تبديل."""

    tool = _seal()
    record = tool.FROZEN_HASR
    for name, value in (
        ("exception", 102),
        ("published", (("م١", "0.0200"), ("م٢", "0.0378"))),
        ("bits_spent", 2),
        ("confusion", (269, 0, 1, 71)),
        ("unbuilt", ("واحدٌ فقط",)),
        ("debts", ()),
    ):
        try:
            dataclasses.replace(record, **{name: value})
        except tool.HasrLedgerError:
            continue
        raise AssertionError(f"مرَّ حقلٌ مبدَّلٌ بلا ردّ: {name}")


def test_five_debts_are_carried_and_nothing_is_signed() -> None:
    """خمسةُ دُيونٍ بنصّها — ولا يوقَّع تأويلٌ ولا حكمُ مُشجِّر."""

    tool = _seal()
    record = tool.FROZEN_HASR
    assert len(record.debts) == 5
    joined = " ".join(why for _, why in record.debts)
    assert "وهو إقرارُ الأنبوب نفسِه" in joined
    assert "وهو إعلانُ الأنبوب لا استنتاجي" in joined
    assert "لا يُخمَّن" in joined
    assert "لا حكمٌ على العربيّة" in joined
    assert "دَينٌ لا نتيجة" in joined
    text = NOTE.read_text(encoding="utf-8")
    assert "ولستُ أنا مَن أجراه ولا مَن يوقّعه" in text
