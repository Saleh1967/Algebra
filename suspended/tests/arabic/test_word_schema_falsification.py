"""«كلمة = جذر + وزن + زوائد»: ثلاثةُ شروطٍ مكتوبةٍ قبل النظر، وثلاثةُ سقوط.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ شروطَ الإبطال ثلاثةٌ ولكلٍّ عتبةٌ
عدديّةٌ مكتوبة، وأنّ شرطًا بلا عتبةٍ يُرفَض عند الإنشاء، وأنّ منازلَ الحكم ثلاثٌ
مغلقةٌ ولا «مؤيَّدٌ جزئيًّا» فيها، وأنّ المدوَّنةَ والجذورَ تُقرآن من بايتاتٍ
مُبصَّمة، وأنّ استخراجَ المرشَّحين يعمل على مثالٍ مبنيٍّ باليد، وأنّ **ت١
التعيين سقط** (الوسيطُ اثنان لا واحد)، وأنّ **ت٢ التغطية سقط** (8.19% بلا
مرشَّح)، وأنّ **ت٣ الحصر سقط** (34.9% فقط باقيها من «سألتمونيها»).

والأرقامُ مربوطةٌ ببصمة المدوَّنة: إن تغيّرت البايتاتُ سقط الاختبارُ ولم يُقرأ
رقمٌ قديمٌ خبرًا عن مدوَّنةٍ جديدة.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.word_schema_falsification import (
    AUGMENT_LETTERS,
    RECEIVED_CLAIM,
    SCHEMA_NAMED_RESIDUALS,
    WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA,
    FalsificationCondition,
    SchemaVerdict,
    WordSchemaError,
    candidate_roots,
    corpus_digest,
    corpus_words,
    deposited_trilateral_roots,
    derive_coverage,
    derive_determination,
    derive_residue_legality,
    read_verdicts,
)


def test_every_condition_carries_a_written_threshold() -> None:
    """شروطُ الإبطال ثلاثةٌ، ولكلٍّ عتبةٌ وما تُبطِله؛ ولا شرطَ بلا عتبة."""

    assert len(WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA) == 3
    for condition in WHAT_WOULD_FALSIFY_THE_WORD_SCHEMA:
        assert condition.threshold.strip()
        assert condition.what_it_refutes.strip()
    with pytest.raises(WordSchemaError):
        FalsificationCondition(
            identifier="ت-س",
            statement="دعوًى",
            threshold="   ",
            what_it_refutes="شيء",
        )


def test_the_verdict_type_is_closed() -> None:
    """ثلاثُ منازلَ: صمد، سقط، غيرُ مقيس — ولا «مؤيَّدٌ جزئيًّا»."""

    assert [verdict.name for verdict in SchemaVerdict] == [
        "SURVIVED",
        "FALSIFIED",
        "UNMEASURED",
    ]
    assert len(AUGMENT_LETTERS) == 10


def test_the_corpus_is_read_from_digested_bytes() -> None:
    """الجذورُ والكلماتُ من بايتات الجدول المُودَع، والبصمةُ تُنقَل مع الرقم."""

    assert len(corpus_digest()) == 64
    assert len(deposited_trilateral_roots()) == 4562
    assert len(corpus_words()) == 60407
    assert all(3 <= len(word) <= 8 for word in corpus_words())


def test_candidate_extraction_works_on_a_built_example() -> None:
    """المرشَّحون متتالياتٌ جزئيّةٌ مرتَّبة، والباقي هو «الزوائد» بنصّ الدعوى."""

    found = dict(candidate_roots("مكتوب"))
    assert "كتب" in found
    assert found["كتب"] == "مو"
    assert candidate_roots("اا") == ()


def test_determination_falls() -> None:
    """ت١: السطحُ لا يُعيِّن تحليلًا؛ الوسيطُ اثنان، والمتوسّطُ فوق ثلاثة."""

    reading = derive_determination()
    assert reading.words == 60407
    assert reading.median_candidates == 2
    assert reading.mean_candidates > 3
    assert reading.verdict is SchemaVerdict.FALSIFIED


def test_coverage_falls() -> None:
    """ت٢: 4,947 كلمةً لا تقبل جذرًا مُودَعًا أصلًا — فوق عتبة 5%."""

    reading = derive_coverage()
    assert reading.uncovered == 4947
    assert reading.uncovered_share > 0.05
    assert reading.verdict is SchemaVerdict.FALSIFIED


def test_residue_legality_falls() -> None:
    """ت٣: أقلُّ من نصف التحليلات باقيها من «سألتمونيها»."""

    reading = derive_residue_legality()
    assert reading.analyses == 206855
    assert reading.legal_share < 0.5
    assert reading.verdict is SchemaVerdict.FALSIFIED


def test_all_three_verdicts_are_falsified_and_the_claim_is_kept_verbatim() -> None:
    """الأحكامُ الثلاثةُ سقوطٌ، والدعوى محفوظةٌ بنصّها لا بإعادة صياغتها."""

    assert set(read_verdicts().values()) == {SchemaVerdict.FALSIFIED}
    assert "جذر + وزن + زوائد" in RECEIVED_CLAIM
    assert "اصطلاحي" in RECEIVED_CLAIM
    assert len(SCHEMA_NAMED_RESIDUALS) == 6
    assert len(set(SCHEMA_NAMED_RESIDUALS)) == 6
