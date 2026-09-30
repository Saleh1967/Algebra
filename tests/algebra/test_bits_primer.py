"""درسُ البتّات **مُشتَقٌّ من الشجرة** — فلا يُعلَّم رقمٌ بعد أن كَذَب.

**العطلُ الذي يحرسه**: الدرسُ إذا كُتِب بيدٍ انفصل عمّا يُعلِّمه. فرقمٌ
في شرحٍ لا يُعاد من الشجرة **يَبلى صامتًا ويبقى يُعلَّم**. وهذا أخطرُ من
عطبٍ في شفرة: الشفرةُ تسقط، **والدرسُ يُصدَّق**.

`A_LESSON_THAT_IS_NOT_RE_DERIVED_ROTS`: فيُعاد توليدُ الوثيقة ويُقابَل
المكتوبُ بالمولَّد حرفًا بحرف؛ **ودرسٌ يخالف شجرتَه يُرَدّ**.

`AND_IT_DOES_NOT_GUARD_THAT_THE_TEACHING_IS_RIGHT`: **وحدُّه مُعلَن**:
يحرس **مطابقةَ الدرس لما في الشجرة**، **لا صوابَ التعليم**. وشرحٌ
مضلِّلٌ بأرقامٍ صحيحةٍ يمرُّ عليه.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
PAPER = REPOSITORY / "docs" / "بايثون-بالبتّات.md"


def _tool() -> Any:
    path = REPOSITORY / "tools" / "write_bits_primer.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_primer_is_regenerated_and_never_typed() -> None:
    """المكتوبُ مطابقٌ لما يولّده مولّدُه — حرفًا بحرف."""

    assert _tool().render() == PAPER.read_text(encoding="utf-8")


def test_every_number_in_it_comes_from_the_tree_not_from_memory() -> None:
    """وأعدادُه تُعاد من الشجرة والودائع — ولا ثابتَ يُقابَل ههنا بيد."""

    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import folding, rasm

    written = PAPER.read_text(encoding="utf-8")
    tool = _tool()
    assert tool.grouped(len(rasm.ARCHETYPE)) in written
    assert tool.eastern(len(rasm.families())) in written
    unit = folding.Guarded(free=9, blocked=6)
    assert tool.grouped(folding.fold_any(unit, (0, 4, 11, 2))) in written
    corpus = (REPOSITORY / "quran-simple-enhanced.txt").stat().st_size
    assert tool.grouped(corpus) in written


def test_the_two_gates_table_matches_the_files_it_describes() -> None:
    """وجدولُ البوّابتين يُقرَأ من `ci.yml` و`verify.sh` لا يُكتَب ههنا."""

    guard = importlib.util.spec_from_file_location(
        "ciguard", REPOSITORY / "tests" / "algebra" / "test_ci_workflow.py"
    )
    assert guard is not None and guard.loader is not None
    module = importlib.util.module_from_spec(guard)
    sys.modules["ciguard"] = module
    guard.loader.exec_module(module)
    written = PAPER.read_text(encoding="utf-8")
    for one in module.local_gates():
        assert f"`{one}`" in written, one
    for one in module.runs(module._workflow()):
        if module.kind_of(one):
            assert f"`{one}`" in written, one


def test_it_carries_no_western_digit_in_its_measured_numbers() -> None:
    """ولا رقمَ غربيٌّ في أعداده المقيسة — الصياغةُ واحدةٌ لا مختلطة."""

    body = "\n".join(
        one
        for one in PAPER.read_text(encoding="utf-8").splitlines()
        if one.startswith("- ") and "`" not in one
    )
    assert body
    assert not any(one.isdigit() and one.isascii() for one in body), body[:200]


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوب: يحرس المطابقةَ لا صوابَ التعليم."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`A_LESSON_THAT_IS_NOT_RE_DERIVED_ROTS`" in here
    assert "`AND_IT_DOES_NOT_GUARD_THAT_THE_TEACHING_IS_RIGHT`" in here
    assert "**لا صوابَ التعليم**" in here
