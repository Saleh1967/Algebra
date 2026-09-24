"""الاستقبالُ مفحوصٌ على بايتاتٍ مصنوعة: بصمةٌ تُطابَق، ومقصدٌ لا يُكتَب فوقه.

**ولا مدوّنةَ تُقرَأ ههنا**: البايتاتُ تُكتَب في هذا الملفّ وتُحسَب بصمتُها
منها. فالمفحوصُ **آلةُ الاستقبال** لا متنٌ بعينه.

`THE_TABLE_IS_CLOSED_AND_ITS_DESTINATIONS_ARE_IGNORED_BY_GIT`: ويُفحَص أمرٌ
ثانٍ لا يقلّ: أنّ كلَّ مقصدٍ في الجدول **مستثنًى في `.gitignore`**. فلو
دخل مقصدٌ جديدٌ بلا استثناء لأودعت أوّلُ دفعةٍ بايتاتِ مدوّنةٍ في شجرة
الشفرة من حيث لا يُرى — وذلك ما يمنعه هذا الفحص، لا النيّة.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY / "tools" / "intake_corpus.py"


def _tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("intake_corpus", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # والتسجيلُ في `sys.modules` قبل التنفيذ شرطُ `dataclass(slots=True)`:
    # فالصنفُ يُعاد بناؤه فيطلب وحدتَه بالاسم، ولا يجدها إن لم تُسجَّل.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


intake_corpus = _tool()

CONTENT = "ألفٌ باءٌ تاء\n".encode()
OTHER = "ألفٌ باءٌ ثاء\n".encode()


def _an_intake(name: str = "متنٌ للفحص") -> object:
    return intake_corpus.Intake(
        name=name,
        source_relative="corpora/one.txt",
        destination_relative="corpora/one.txt",
        byte_length=len(CONTENT),
        sha256_hex=hashlib.sha256(CONTENT).hexdigest(),
    )


def _a_source(folder: Path, payload: bytes = CONTENT) -> Path:
    path = folder / "corpora" / "one.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def test_an_intake_refuses_a_bad_digest_or_length_or_name() -> None:
    """ثلاثةُ حقولٍ شرطَ إنشاء: اسمٌ، وطولٌ موجب، وبصمةٌ ستّونيّة."""

    good = hashlib.sha256(CONTENT).hexdigest()
    for digest in (good[:63], good + "0", good[:-1] + "z", ""):
        with pytest.raises(intake_corpus.IntakeError):
            intake_corpus.Intake(
                name="متن",
                source_relative="a",
                destination_relative="a",
                byte_length=1,
                sha256_hex=digest,
            )
    for length in (0, -1):
        with pytest.raises(intake_corpus.IntakeError):
            intake_corpus.Intake(
                name="متن",
                source_relative="a",
                destination_relative="a",
                byte_length=length,
                sha256_hex=good,
            )
    with pytest.raises(intake_corpus.IntakeError):
        intake_corpus.Intake(
            name="  ",
            source_relative="a",
            destination_relative="a",
            byte_length=1,
            sha256_hex=good,
        )


def test_the_length_matching_does_not_excuse_the_digest(tmp_path: Path) -> None:
    """طولٌ موافقٌ وبصمةٌ مخالفةٌ يُرَدّ — فالطولُ وحدَه ليس شهادة."""

    source = _a_source(tmp_path, OTHER)
    assert len(OTHER) == len(CONTENT)  # الطولان سواءٌ، والبايتاتُ مختلفة
    with pytest.raises(intake_corpus.IntakeError) as raised:
        intake_corpus.verify(source, _an_intake())
    assert "البصمةُ" in str(raised.value)


def test_a_missing_source_is_refused_by_its_path(tmp_path: Path) -> None:
    """غيابُ المصدر يُسمّي المسارَ، فيُقرَأ الفرقُ بين غيابٍ ومخالفة."""

    with pytest.raises(intake_corpus.IntakeError) as raised:
        intake_corpus.receive(_an_intake(), tmp_path, into=tmp_path / "إلى")
    assert "لا ملفَّ في" in str(raised.value)


def test_a_matching_intake_is_received_then_reported_as_present(
    tmp_path: Path,
) -> None:
    """أوّلُ تشغيلٍ يستقبل، وثانيه يقول «حاضرٌ سلفًا» ولا ينسخ مرّتين."""

    root, into = tmp_path / "من", tmp_path / "إلى"
    _a_source(root)
    first = intake_corpus.receive(_an_intake(), root, into=into)
    assert first.startswith("استُقبِل:")
    assert (into / "corpora" / "one.txt").read_bytes() == CONTENT

    second = intake_corpus.receive(_an_intake(), root, into=into)
    assert second.startswith("حاضرٌ سلفًا:")


def test_differing_bytes_at_the_destination_are_not_overwritten_silently(
    tmp_path: Path,
) -> None:
    """مقصدٌ فيه بايتاتٌ مخالفةٌ يُوقِف الاستقبالَ، و`--replace` تُعلَن."""

    root, into = tmp_path / "من", tmp_path / "إلى"
    _a_source(root)
    destination = into / "corpora" / "one.txt"
    destination.parent.mkdir(parents=True)
    destination.write_bytes(OTHER)

    with pytest.raises(intake_corpus.IntakeError) as raised:
        intake_corpus.receive(_an_intake(), root, into=into)
    assert "--replace" in str(raised.value)
    assert destination.read_bytes() == OTHER  # ولم تُمَسّ

    replaced = intake_corpus.receive(_an_intake(), root, into=into, replace=True)
    assert replaced.startswith("استُقبِل:")
    assert destination.read_bytes() == CONTENT


def test_the_source_root_is_declared_and_never_guessed(tmp_path: Path) -> None:
    """المُصرَّحُ أوّلًا، ثمّ متغيّرُ البيئة، وغيابُهما رفضٌ صريحٌ لا افتراض."""

    assert intake_corpus.source_root(tmp_path) == tmp_path
    with pytest.raises(intake_corpus.IntakeError) as raised:
        intake_corpus.source_root(None)
    assert intake_corpus.SOURCE_ROOT_VARIABLE in str(raised.value)


def test_the_declared_table_is_closed_and_distinct() -> None:
    """مستقبَلان مُعلَنان، ولا اسمَ ولا مقصدَ يتكرّر، ولا بصمةَ تُشارك أختَها."""

    table = intake_corpus.INTAKES
    assert len(table) == 2
    assert len({one.name for one in table}) == 2
    assert len({one.destination_relative for one in table}) == 2
    assert len({one.sha256_hex for one in table}) == 2
    for one in table:
        assert len(one.sha256_hex) == 64
        assert one.byte_length > 0


def test_every_destination_is_excluded_from_the_code_tree() -> None:
    """كلُّ مقصدٍ مستثنًى في `.gitignore` — فلا تُودَع مدوّنةٌ من حيث لا يُرى."""

    ignored = (REPOSITORY / ".gitignore").read_text(encoding="utf-8").splitlines()
    entries = {line.strip() for line in ignored if line.strip()}
    for one in intake_corpus.INTAKES:
        assert one.destination_relative in entries, one.destination_relative
