"""سجلُّ أنبوبٍ خارجيٍّ مُقفَلًا — ما أُعيد اشتقاقُه، وما حُدَّ، وما سُمّي دَينًا.

**ما يُفحَص ههنا**: أنّ كلَّ رقمٍ في `deposits/foreign_*.txt` **يُعاد
اشتقاقُه من الأعداد المطبوعة في الملفّات نفسِها**، لا يُنقَل. وأنّ ما لا
يسمح المنشورُ بإعادة اشتقاقه **يُحَدُّ بحدّين** ويُقال أَداخلَهما المنشورُ
أم خارج.

`I_DID_NOT_RUN_IT_AND_I_DO_NOT_SIGN_IT`: ولا أملك مدوّنتَه ولا وسومَه،
**فلا أعيد قياسَه ولا أصدّق تأويلَه**. والتسجيلان المُودَعان **ينفيان عن
نفسيهما** أن يُثبتا أنّ بنودَ الكتاب ثمانيةٌ أو أنّ وسومَ QAC تكشف دلالةً
أصوليّة؛ **ويُنقَل نفيُهما كما هو**.

`THE_STAND_IS_NOT_THE_SAME_STAND`: ومقامُه **٧٧٬٤٢٩** كلمةً و**٦٬٢٠٨**
آيةً، ومقامُ هذه الشجرة **٧٨٬٢٤٥** و**٦٬٢٣٦**. **فلا يُنقَل رقمٌ من أحدهما
إلى الآخر.**
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
SEAL = REPOSITORY / "tools" / "foreign_ledger_seal.py"
NOTE = REPOSITORY / "deposits" / "foreign_ledger_note.md"

THIS_TREE_WORDS = 78_245
THIS_TREE_LINES = 6_236


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("foreign_ledger_seal", SEAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_from_its_fields() -> None:
    """البصمةُ تُشتَقّ من الحقول لا تُنقَل — وتبديلُ حقلٍ يُسقِط الفحص."""

    tool = _seal()
    assert tool.rederive_record_digest() == tool.RECORD_DIGEST
    assert tool.RECORD_DIGEST.startswith("ef803707")


def test_every_field_is_witnessed_in_the_deposited_files() -> None:
    """كلُّ حقلٍ له شاهدٌ في الملفّات المُودَعة، وما خالف يُسمّى."""

    tool = _seal()
    assert tool.verify_against_logs() == []


def test_each_bit_entropy_is_recomputed_from_its_own_count() -> None:
    """ثمانيةُ إنتروبياتٍ تُشتَقّ من ثمانيةِ أعدادٍ — لا واحدةَ منقولة."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    for index, count in enumerate(record.bunud_counts):
        mine = tool.bit_entropy(count / record.stand_words)
        assert abs(mine - float(record.bunud_entropies[index])) < 5e-5


def test_the_vector_entropy_is_bounded_because_six_cells_are_unpublished() -> None:
    """ثمانٍ من أربعَ عشرةَ منشورة — فتُحَدُّ H ولا تُعاد حسابًا تامًّا."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    low, high = record.vector_bounds()
    measured = float(record.vector_entropy)
    assert low < measured < high
    assert abs(low - 1.5745) < 5e-5
    assert abs(high - 1.6000) < 5e-5
    hidden = record.vector_cells - len(record.vector_shown)
    assert hidden == 6
    assert record.stand_words - sum(record.vector_shown) == 1_145


def test_the_two_huffman_codes_obey_kraft_and_the_shannon_bound() -> None:
    """رموزُ هافمان سليمةُ البادئة، وكرافت لا يجاوز الواحد، وH ≤ L < H+1."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    assert tool.prefix_free(record.bunud_codes)
    assert tool.kraft(record.bunud_code_lengths) < 1.0  # منشورٌ ناقصٌ فبقيّةٌ
    assert abs(tool.kraft(record.asalib_code_lengths) - 1.0) < 1e-12
    for value, code in (
        (record.vector_entropy, record.bunud_huffman),
        (record.asalib_entropy, record.asalib_huffman),
    ):
        assert float(value) <= float(code) < float(value) + 1.0


def test_the_three_tree_depths_are_recomputed_from_the_counts() -> None:
    """أعماقُ الشجرات الثلاثِ تُشتَقّ من الأعداد — والفرقُ ٤٫٣٦١٨."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    shares = record.asalib_shares()
    walked = math.fsum(
        one * two for one, two in zip(shares, record.asalib_code_lengths)
    )
    linear = math.fsum(one * (index + 1) for index, one in enumerate(shares))
    booked = math.fsum(one * two for one, two in zip(shares, record.asalib_book_ranks))
    assert abs(walked - 1.8554) < 5e-5
    assert abs(linear - 1.8641) < 5e-5
    assert abs(booked - 6.2172) < 5e-5
    assert abs((booked - walked) - 4.3618) < 5e-5
    assert record.asalib_book_ranks[0] == 7  # وأشيعُها سابعٌ من ثمانية


def test_the_last_place_differences_are_rounding_not_disagreement() -> None:
    """فرقُ المنزلة الأخيرة ترتيبُ تقريبٍ لا خلافُ حساب — ويُبَيَّن لا يُطوى.

    مجموعُ الإنتروبيات **قبل** التقريب **١٫٦٧٥٢٨٠** فيُطبَع ١٫٦٧٥٣، ومجموعُ
    المنشور بأربع منازلَ ١٫٦٧٥٢. **وكلاهما صحيح**، والفرقُ **وحدةٌ في
    المنزلة الرابعة** لا خلافَ فيه على شيء. وكذلك مجموعُ الكسب: المنشورُ
    ٠٫٢٦٧٥ ومجموعُ أرقامه ٠٫٢٦٧٦.
    """

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    exact = math.fsum(
        tool.bit_entropy(one / record.stand_words) for one in record.bunud_counts
    )
    printed = math.fsum(float(one) for one in record.bunud_entropies)
    assert abs(exact - 1.675280) < 5e-7
    assert abs(printed - 1.6752) < 5e-5
    assert round(exact, 4) == 1.6753  # والمنشورُ هو المجموعُ قبل التقريب
    assert abs((exact - printed) - 0.0001) < 5e-5
    gains = math.fsum(float(one) for one in record.bunud_gains)
    assert abs(gains - 0.2676) < 5e-5
    assert abs((gains - float(record.vector_gain)) - 0.1613) < 5e-5


def test_the_redundancy_is_read_as_printed_and_not_softened() -> None:
    """مجموعُ كسبِ البتّات يفوق كسبَ المتّجه — فتكرارٌ لا تآزر."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    gains = math.fsum(float(one) for one in record.bunud_gains)
    assert gains > float(record.vector_gain)
    assert float(record.vector_gain) / 8 < min(float(one) for one in record.bunud_gains)
    widest = max(range(8), key=lambda one: float(record.bunud_gains[one]))
    rarest = min(range(8), key=lambda one: record.bunud_counts[one])
    assert widest == rarest  # وأكبرُ كسبٍ عند أندرِ البنود
    commonest = max(range(8), key=lambda one: record.bunud_counts[one])
    assert float(record.bunud_gains[commonest]) == min(
        float(one) for one in record.bunud_gains
    )


def test_the_allocation_efficiency_is_derived_not_asserted() -> None:
    """ثمانيةُ بتّاتٍ لأربعَ عشرةَ حالةً — وأربعةٌ تكفي، والمحمولُ خُمسٌ."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    assert (record.vector_cells - 1).bit_length() == 4
    carried = float(record.vector_entropy) / len(record.bunud_names)
    assert abs(carried - 0.1984) < 5e-5


def test_the_stand_is_named_as_different_from_this_tree() -> None:
    """المقامان لا يُقابَلان — والفرقُ يُسمّى ولا يُخمَّن."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    assert record.stand_words != THIS_TREE_WORDS
    assert record.stand_verses != THIS_TREE_LINES
    text = NOTE.read_text(encoding="utf-8")
    assert str(THIS_TREE_WORDS)[:2] in text or "٧٨٬٢٤٥" in text
    assert "٧٧٬٤٢٩" in text and "٦٬٢٠٨" in text
    assert "يُسمّى ولا يُخمَّن" in text
    assert "لا يوقّع" in text


def test_every_debt_is_named_with_its_figures() -> None:
    """خمسةُ دُيونٍ مُسمّاةٌ بأرقامها — ولا سجلَّ بلا دَين."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    assert len(record.debts) == 5
    for name, why in record.debts:
        assert name.strip() and len(why) > 25
    joined = " ".join(why for _, why in record.debts)
    for figure in ("٩٠٢", "٨٩٤", "٨٤٥", "٨٤٨", "١٬١٤٥", "٧٧٬٤٢٩"):
        assert figure in joined, figure


def test_the_record_refuses_a_field_that_does_not_recompute() -> None:
    """من بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه — والقيدُ في المُنشئ."""

    tool = _seal()
    record = tool.FROZEN_FOREIGN
    import dataclasses

    for name, value in (
        ("bunud_entropies", ("0.9999",) + record.bunud_entropies[1:]),
        ("vector_entropy", "2.5000"),
        ("asalib_huffman", "1.2000"),
        ("asalib_by_book", "3.0000"),
        ("debts", ()),
    ):
        try:
            dataclasses.replace(record, **{name: value})
        except tool.ForeignLedgerError:
            continue
        raise AssertionError(f"مرَّ حقلٌ مبدَّلٌ بلا ردّ: {name}")
