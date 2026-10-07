"""الختمُ البايتيُّ مفحوصًا: بصمةٌ تُشتَقّ، وحقلٌ مقيسٌ يُقابَل بالبايتات.

**ما أُقفِل**: سجلٌّ واحدٌ يحمل المدوّنةَ (بصمةً وطولًا وأسطرًا)، ومصدرَها
الموقَّع، وروايتَها بمنزلتها وعدد فوارقها، وعلاماتِ السكون، وملتقى النون.
وبصمتُه `30c7e393…` — وبها يُستشهَد في أوراكل ما بعده بدل النثر.

`THE_DIGEST_MOVES_WHEN_ANY_FIELD_MOVES`: ومفحوصٌ بضِدّه: تبديلُ حقلٍ واحدٍ
يُغيّر البصمة. فليست رقمًا منقولًا في متنٍ يُنسى، بل مُشتَقّةً عند كلّ تشغيل.

`A_MAJORITY_CANNOT_BE_SEALED`: ولا يُقفَل سجلٌّ باسمِ روايةٍ لم توافقها
الفوارقُ **كلُّها**: المُنشئُ نفسُه يردُّه. فما امتنع في `identify_reading`
امتنع في القفل أيضًا — والقيدُ في موضعين لا في موضع.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest
from frozen_corpus import CORPUS, HELD, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "corpus_seal.py"

RECORD_DIGEST = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"


def _tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("corpus_seal", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


seal_tool = _tool()


def test_the_record_digest_is_rederived_and_frozen() -> None:
    """بصمةٌ مُشتَقّةٌ من الحقول، ومكتوبةٌ في المتن ليُمسَك تبدّلُها."""

    assert seal_tool.RECORD_DIGEST == RECORD_DIGEST
    assert seal_tool.rederive_record_digest() == RECORD_DIGEST
    assert len(RECORD_DIGEST) == 64
    assert hashlib.sha256(seal_tool.record_bytes()).hexdigest() == RECORD_DIGEST


def test_moving_any_single_field_moves_the_digest() -> None:
    """تبديلُ حقلٍ واحدٍ يُغيّر البصمة — في الموقَّع وفي المقيس سواءً."""

    from dataclasses import replace

    for name, value in (
        ("source_tag", "مصدرٌ آخر"),
        ("reading_name", "روايةٌ أخرى"),
        ("sukun_marks", 37_371),
        ("ayah_lines", 6_235),
    ):
        moved = replace(seal_tool.FROZEN_RECORD, **{name: value})
        assert seal_tool.rederive_record_digest(moved) != RECORD_DIGEST, name


def test_a_record_naming_a_reading_on_a_majority_is_refused() -> None:
    """اسمُ روايةٍ بـ٢ من ٣ لا يُقفَل: القيدُ في المُنشئ لا في النيّة."""

    from dataclasses import replace

    with pytest.raises(seal_tool.CorpusSealError) as raised:
        replace(seal_tool.FROZEN_RECORD, reading_agreed=2)
    assert "النسبةُ بأغلبيّةٍ ليست نسبة" in str(raised.value)


def test_an_empty_signed_field_or_a_bad_digest_is_refused() -> None:
    """حقلٌ موقَّعٌ فارغٌ أو بصمةٌ ناقصةٌ تُرَدّ في الإنشاء."""

    from dataclasses import replace

    for name in ("source_tag", "reading_name", "name"):
        with pytest.raises(seal_tool.CorpusSealError):
            replace(seal_tool.FROZEN_RECORD, **{name: "   "})
    with pytest.raises(seal_tool.CorpusSealError):
        replace(seal_tool.FROZEN_RECORD, sha256_hex="0" * 63)


@requires_corpus
def test_every_measured_field_is_reproduced_from_the_bytes() -> None:
    """الطولُ والبصمةُ والأسطرُ والسكونُ تُعاد من البايتات، فلا حقلَ مقيسٌ مُدَّعى."""

    assert seal_tool.verify_against_corpus() == []


def test_a_missing_corpus_is_refused_by_its_path() -> None:
    """غيابُ البايتات يُسمّي المسارَ ولا يُقرأ تطابقًا."""

    with pytest.raises(seal_tool.CorpusSealError) as raised:
        seal_tool.verify_against_corpus(REPOSITORY / "corpora" / "لا-وجودَ-له.txt")
    assert "لا بايتاتِ مدوّنة" in str(raised.value)


def test_the_holder_is_found_by_its_bytes_and_not_by_its_name(
    tmp_path: Path,
) -> None:
    """حاملٌ باسم المدوّنة ببايتاتٍ أخرى لا يُقبَل، والصحيحُ يُقبَل أينما كان."""

    for relative in seal_tool.DECLARED_HOLDERS:
        (tmp_path / relative).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / relative).write_bytes(b"\xd8\xa7 laysat hiya")
    assert seal_tool.holder_in(tmp_path) is None

    assert len(seal_tool.DECLARED_HOLDERS) == 2
    assert seal_tool.DECLARED_HOLDERS[0] == seal_tool.FROZEN_RECORD.name
    assert "corpora/" in seal_tool.DECLARED_HOLDERS[1]


@requires_corpus
def test_the_present_holder_carries_the_sealed_bytes_exactly() -> None:
    """الحاملُ الحاضرُ يُعاد اشتقاقُ بصمته ههنا، فلا يُقبَل بعنوانه."""

    assert HELD and CORPUS.is_file()
    digest = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    assert digest == seal_tool.FROZEN_RECORD.sha256_hex
    assert seal_tool.verify_against_corpus(CORPUS) == []
    assert CORPUS.name == seal_tool.FROZEN_RECORD.name
