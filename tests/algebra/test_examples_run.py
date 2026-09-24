"""الأمثلةُ تُشغَّل لا تُقرَأ: أربعةٌ تعمل، وسبعةٌ تنتمي إلى الشجرة الأخرى.

**ما كشفه التشغيل**: فحصُ الفصل (`test_separation`) يغطّي `src/algebra` و
`tests/algebra` **ولا يغطّي `examples/`**. وسبعةٌ من أحدَ عشرَ مثالًا تستورد
`alghanem` فتسقط عند التشغيل بـ`ModuleNotFoundError`. فالمستودعُ كان يدّعي
فصلًا ويشحن سبعةَ أمثلةٍ لا تعمل فيه — **ولا فحصَ واحدٌ يمسك ذلك**، لأنّ
الأمثلةَ تُقرَأ ولا تُشغَّل.

`AN_EXAMPLE_THAT_IS_NEVER_RUN_IS_NOT_AN_EXAMPLE`: فصارت الأمثلةُ **مُعدَّدةً**
ههنا: كلُّ ملفٍّ تحت `examples/` إمّا في جدول التشغيل — فيُشغَّل ويُفحَص
خروجُه — وإمّا في جدول الشجرة الأخرى — فيُفحَص أنّه يستورد `alghanem` فعلًا.
ولا ثالثَ: مثالٌ جديدٌ لا يدخل أحدَ الجدولين يُرَدّ باسمه.

`THE_SEVEN_ARE_NOT_DEAD_WEIGHT_TO_BE_SWEPT`: وستّةٌ منها **مطابقةٌ بايتًا
ببايت** لنظائرها في شجرة الغانم وتعمل هناك. والسابعُ —
`audit_slgae_third_version` — **أحدثُ من نظيره هناك**: فيه
`disambiguation_digest` و`resolve_colliding_citation` وسبعةُ أسطرِ طباعةٍ
ليست في تلك النسخة. فحذفُها هنا يُسقِط عملًا لم يُدفَع بعد، **والعدُّ أولى
من الكنس**.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
EXAMPLES = REPOSITORY / "examples"
FOREIGN = "alghanem"

# مثالٌ يعمل على هذه الحزمة وحدَها، ومعه وسائطُه المُعلَنة
RUNNABLE: dict[str, tuple[str, ...]] = {
    "hawk_dove/run_hawk_dove.py": (),
    "irab/run_harf_measurement.py": ("--smoke", "--defer", "error"),
    "isnad/run_ittifaq.py": ("--smoke",),
    "maana/run_imtihan.py": ("--smoke",),
}

# مثالٌ متنُه على الشجرة الأخرى؛ يُعَدّ ههنا ولا يُشغَّل
BELONGS_TO_THE_OTHER_TREE: frozenset[str] = frozenset(
    {
        "arabic/audit_slgae_markov.py",
        "arabic/audit_slgae_third_version.py",
        "arabic/decode_makhraj_bits.py",
        "arabic/decode_makhraj_haraka_bits.py",
        "arabic/encode_arabic_units.py",
        "arabic/measure_sifa_candidate.py",
        "arabic/read_slgae_separation.py",
    }
)


def _examples() -> list[str]:
    return sorted(str(path.relative_to(EXAMPLES)) for path in EXAMPLES.rglob("*.py"))


def _imports_foreign(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[0] == FOREIGN for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == FOREIGN:
                return True
    return False


def test_every_example_is_in_exactly_one_table() -> None:
    """أحدَ عشرَ مثالًا، كلٌّ في جدولٍ واحدٍ لا غير — ولا يمرّ جديدٌ صامتًا."""

    found = set(_examples())
    declared = set(RUNNABLE) | BELONGS_TO_THE_OTHER_TREE

    assert not (found - declared), sorted(found - declared)
    assert not (declared - found), sorted(declared - found)
    assert not (set(RUNNABLE) & BELONGS_TO_THE_OTHER_TREE)
    assert len(found) == 11
    assert len(RUNNABLE) == 4
    assert len(BELONGS_TO_THE_OTHER_TREE) == 7


@pytest.mark.parametrize("name", sorted(RUNNABLE))
def test_a_runnable_example_runs_and_exits_clean(name: str) -> None:
    """يُشغَّل فعلًا ويخرج بصفرٍ ويطبع شيئًا؛ والقراءةُ لا تُغني عن التشغيل."""

    path = EXAMPLES / name
    assert not _imports_foreign(path)

    finished = subprocess.run(  # noqa: S603
        [sys.executable, str(path), *RUNNABLE[name]],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPOSITORY,
    )
    assert finished.returncode == 0, finished.stderr[-600:]
    assert finished.stdout.strip()


@pytest.mark.parametrize("name", sorted(BELONGS_TO_THE_OTHER_TREE))
def test_a_foreign_example_really_imports_the_other_tree(name: str) -> None:
    """الجدولُ الثاني يُفحَص بالبناء لا بالدعوى: يستورد `alghanem` فعلًا.

    فلو أُصلِح أحدُها يومًا وصار يعمل على هذه الحزمة وحدَها، سقط هذا الفحصُ
    ونُقِل إلى جدول التشغيل — ولا يبقى في جدول المُستثنى بالسهو.
    """

    assert _imports_foreign(EXAMPLES / name)


def test_the_separation_guard_did_not_cover_this_directory() -> None:
    """فحصُ الفصل يقرأ `src/algebra` و`tests/algebra` — ولا يقرأ `examples/`.

    وهذا هو سببُ بقاء السبعة ساقطةً بلا إنذار: الحزمةُ مفصولةٌ مفحوصةً،
    والأمثلةُ خارجَ نطاق الفحص. فالفحصُ ههنا يُكمِل النطاق ولا يُبدِّله.
    """

    guard = (REPOSITORY / "tests" / "algebra" / "test_separation.py").read_text(
        encoding="utf-8"
    )
    assert 'PACKAGE = REPOSITORY / "src" / "algebra"' in guard
    assert 'TESTS = REPOSITORY / "tests" / "algebra"' in guard
    assert "examples" not in guard

    # وسبعةٌ من أحدَ عشرَ تستورد الشجرةَ الأخرى: أكثرُ من نصف الأمثلة
    foreign = [name for name in _examples() if _imports_foreign(EXAMPLES / name)]
    assert len(foreign) == 7
    assert set(foreign) == BELONGS_TO_THE_OTHER_TREE
    assert len(foreign) * 2 > len(_examples())
