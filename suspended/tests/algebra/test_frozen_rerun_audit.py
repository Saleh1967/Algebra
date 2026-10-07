"""المقابلةُ مُجمَّدةٌ، وبصمةُ كلّ سجلٍّ مودَعٍ تُعاد **في كلّ بوّابة**.

**ما يحرسه**: أنّ كلَّ سجلٍّ مودَعٍ لم يُمَسّ منذ أن أُعيد من المدوّنة
فطابق — فبصمتُه تُحسَب الآن وتُقابَل بالمُجمَّد. **وأنّ لا سجلَّ تشغيلٍ
يدخل الشجرةَ بلا صفٍّ مُجمَّد**: فزيادةُ سجلٍّ بلا تجميدِ بصمته تردُّ
البوّابة.

**وحدُّه مُصرَّحٌ به**: عمودُ «المُعاد» في `rerun_audit.log` **لا يُعاد
ههنا** — يحتاج المدوّنةَ، وهي ليست في الشجرة. فذلك **خلوٌّ مُصنَّفٌ**
(`UNREACHABLE`) لا فحصٌ مُدَّعًى، والمحروسُ عمودُ «المودَع» وحدَه.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
DEPOSITS = REPOSITORY / "deposits"
CORPUS_SEAL = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"


def _tool(name: str) -> Any:
    path = REPOSITORY / "tools" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_record_digest_is_rederived_not_written() -> None:
    """البصمةُ مُشتَقّةٌ من الحقول، وتبديلُ حقلٍ يُغيّرها."""

    tool = _tool("rerun_audit_seal.py")
    record = tool.FROZEN_RERUN
    assert tool.rederive_record_digest(record) == tool.RECORD_DIGEST
    assert len(tool.RECORD_DIGEST) == 64
    other = replace(record, corpus_lines=record.corpus_lines + 1)
    assert tool.rederive_record_digest(other) != tool.RECORD_DIGEST


def test_every_deposited_log_still_hashes_to_the_frozen_digest() -> None:
    """تُحسَب البصماتُ الآن من الملفّات نفسِها — وما خالف يُسمّى."""

    tool = _tool("rerun_audit_seal.py")
    assert tool.verify_against_logs() == []


def test_no_run_log_escapes_the_record() -> None:
    """كلُّ `*_run.log` في الشجرة له صفٌّ أو هو مختصَرٌ مُسمًّى."""

    tool = _tool("rerun_audit_seal.py")
    record = tool.FROZEN_RERUN
    covered = {one for one, _, _ in record.rows} | {
        one for one, _, _ in record.abridged
    }
    present = {one.name for one in DEPOSITS.glob("*_run.log")}
    assert present - covered == set(), sorted(present - covered)
    assert len(record.rows) == record.compared == record.matched


def test_the_abridged_log_loses_no_line() -> None:
    """المختصَرُ شريحةُ أسطرٍ من الكامل — صفرُ سطرٍ مفقود."""

    tool = _tool("rerun_audit_seal.py")
    record = tool.FROZEN_RERUN
    assert record.abridged, "لا مختصَرَ مُسمًّى — والسجلُّ يحمل واحدًا"
    for name, lines, missing in record.abridged:
        assert missing == 0, (name, missing)
        brief = (DEPOSITS / name).read_text(encoding="utf-8").splitlines()
        assert len(brief) == lines, (name, len(brief), lines)


def test_a_record_that_hides_a_mismatch_is_refused() -> None:
    """لا يُقفَل سجلٌّ فيه مخالفٌ — والمخالفُ يُسمّى ولا يُجمَّد."""

    tool = _tool("rerun_audit_seal.py")
    record = tool.FROZEN_RERUN
    with pytest.raises(tool.RerunAuditError):
        replace(record, matched=record.matched - 1)
    with pytest.raises(tool.RerunAuditError):
        replace(record, compared=record.compared + 1)
    with pytest.raises(tool.RerunAuditError):
        replace(record, abridged=((record.abridged[0][0], 1, 1),))
    with pytest.raises(tool.RerunAuditError):
        replace(record, corpus="لا بصمة")


def test_the_comparison_was_against_the_sealed_corpus() -> None:
    """المقابلةُ على البايتات المختومة، لا على مدوّنةٍ أخرى."""

    tool = _tool("rerun_audit_seal.py")
    maker = _tool("rerun_audit.py")
    assert tool.FROZEN_RERUN.corpus == CORPUS_SEAL
    assert maker.CORPUS_SEAL == CORPUS_SEAL
    assert tool.FROZEN_RERUN.corpus_lines == maker.CORPUS_LINES


def test_the_invocation_of_every_run_is_deposited() -> None:
    """وسائطُ كلّ تشغيلٍ مكتوبةٌ — فلا يُقرَأ عطلُ استدعاءٍ عطلَ رقم."""

    maker = _tool("rerun_audit.py")
    written = (DEPOSITS / "rerun_audit.log").read_text(encoding="utf-8")
    assert len(maker.RUNS) == _tool("rerun_audit_seal.py").FROZEN_RERUN.compared
    for name, (script, extra, needs_text) in maker.RUNS.items():
        assert (REPOSITORY / "examples" / "rasm" / script).is_file(), script
        args = ("--text <المدوّنة> " if needs_text else "") + " ".join(extra)
        assert f"    {name}: {script} {args}".rstrip() in written, name
    odd = {one for one, (_, extra, _) in maker.RUNS.items() if extra}
    assert len(odd) == 5, sorted(odd)
