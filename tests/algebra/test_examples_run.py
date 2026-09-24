"""الأمثلةُ تُشغَّل لا تُقرَأ: أحدَ عشرَ مثالًا، وكلُّها تعمل.

**ما كشفه التشغيل أوّلًا**: فحصُ الفصل يغطّي `src/algebra` و`tests/algebra`
**ولا يغطّي `examples/`**. وسبعةٌ من أحدَ عشرَ مثالًا كانت تسقط بـ
`ModuleNotFoundError` لأنّها تستورد `alghanem` من خارج. فالمستودعُ كان يشحن
أكثرَ من نصف أمثلته لا يعمل، **ولا فحصَ واحدٌ يمسك ذلك** — لأنّ الأمثلةَ
تُقرَأ ولا تُشغَّل.

**وما جرى بعدَه**: نُقِلت شفرةُ الإغلاق اللازم إلى `src/alghanem`، فصار
المستودعان يعملان مستقلَّين. **فالسبعةُ تعمل الآن**، ودخلت جدولَ التشغيل.

`AN_EXAMPLE_THAT_IS_NEVER_RUN_IS_NOT_AN_EXAMPLE`: والأمثلةُ **مُعدَّدةٌ**
ههنا: كلُّ ملفٍّ تحت `examples/` في جدول التشغيل بوسائطه المُعلَنة، يُشغَّل
ويُفحَص خروجُه ومخرَجُه. ومثالٌ جديدٌ لا يدخله يُرَدّ باسمه — فلا يُشحَن
مثالٌ لا يُدرى أيعمل أم لا.

`THE_MEASURE_IS_RUNNING_HERE_NOT_WHICH_PACKAGE_IT_IMPORTS`: وكان الجدولُ
الثاني «ما يستورد `alghanem`»، وذلك وصفٌ لا معيار. **والمعيارُ أن يعمل في
هذا المستودع**؛ والحزمتان جارتان فيه، و`algebra` لا تستورد الأخرى — وذلك
مفحوصٌ في `test_separation` بعمليّةٍ مستقلّة.
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

# مثالٌ يعمل في هذا المستودع، ومعه وسائطُه المُعلَنة
RUNNABLE: dict[str, tuple[str, ...]] = {
    "arabic/audit_slgae_markov.py": (),
    "arabic/audit_slgae_third_version.py": (),
    "arabic/decode_makhraj_bits.py": (),
    "arabic/decode_makhraj_haraka_bits.py": (),
    "arabic/encode_arabic_units.py": (),
    "arabic/measure_sifa_candidate.py": (),
    "arabic/read_slgae_separation.py": (),
    "hawk_dove/run_hawk_dove.py": (),
    "irab/run_harf_measurement.py": ("--smoke", "--defer", "error"),
    "isnad/run_ittifaq.py": ("--smoke",),
    "maana/run_imtihan.py": ("--smoke",),
}


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


def test_every_example_is_declared_and_none_is_left_out() -> None:
    """أحدَ عشرَ مثالًا، كلُّها في الجدول — ولا يمرّ جديدٌ صامتًا."""

    found = set(_examples())
    assert not (found - set(RUNNABLE)), sorted(found - set(RUNNABLE))
    assert not (set(RUNNABLE) - found), sorted(set(RUNNABLE) - found)
    assert len(found) == 11
    assert len(RUNNABLE) == 11


@pytest.mark.parametrize("name", sorted(RUNNABLE))
def test_a_runnable_example_runs_and_exits_clean(name: str) -> None:
    """يُشغَّل فعلًا ويخرج بصفرٍ ويطبع شيئًا؛ والقراءةُ لا تُغني عن التشغيل."""

    path = EXAMPLES / name
    finished = subprocess.run(  # noqa: S603
        [sys.executable, str(path), *RUNNABLE[name]],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPOSITORY,
    )
    assert finished.returncode == 0, finished.stderr[-600:]
    assert finished.stdout.strip()


def test_seven_examples_still_import_the_ported_package_and_now_run() -> None:
    """سبعةٌ تستورد `alghanem` — وكانت تسقط، وصارت تعمل بعد نقل الشفرة.

    فالاستيرادُ لم يتغيّر، والذي تغيّر أنّ ما يُستورَد صار **ههنا**. وذلك
    معنى الاستقلال: لا إحالةَ إلى شجرةٍ مجاورة.
    """

    foreign = [name for name in _examples() if _imports_foreign(EXAMPLES / name)]
    assert len(foreign) == 7
    assert all(name.startswith("arabic/") for name in foreign)
    assert set(foreign) <= set(RUNNABLE)

    # والأربعةُ الباقيةُ لا تستوردها ألبتّة
    assert len(_examples()) - len(foreign) == 4
