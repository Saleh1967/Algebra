"""الفصلُ مفحوصٌ لا مُعلَن: لا وحدةَ في `algebra` تستورد من `alghanem`.

يُثبِت هذا الاختبارُ خمسةَ أشياء: أنّ **كلَّ** ملفٍّ في `src/algebra` خالٍ من
استيرادِ `alghanem` بقراءة شجرةِ التحليل لا بالبحث النصّيّ، وأنّ اختباراتِها
كذلك، وأنّ الحزمةَ تُستورَد وحدَها بلا أيّ اسمٍ من تلك الشجرة في مسار الاستيراد،
وأنّ اسمَ التوزيعة صار `algebra` لا `alghanem` — وهو أعمقُ التشابك إذ كان
تثبيتُ هذا المستودع يضع حزمةً بذلك الاسم في المسار — وأنّ `pyproject` يُشغّل
اختباراتِ هذه الحزمة فعلًا فلا يكون الفصلُ دعوًى بلا فحص.

وذِكرُ الاسم في نصِّ توثيقٍ ليس استيرادًا: الباقي المُسمّى في `__init__` يقول
إنّ الحزمةَ لا تستورد منها، وهذا الاختبارُ هو ما يجعل ذلك القولَ مفحوصًا.
"""

from __future__ import annotations

import ast
from pathlib import Path

import tomllib

REPOSITORY = Path(__file__).resolve().parents[2]
PACKAGE = REPOSITORY / "src" / "algebra"
TESTS = REPOSITORY / "tests" / "algebra"
FOREIGN = "alghanem"


def _imported_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_the_package_imports_nothing_from_the_other_tree() -> None:
    """لا استيرادَ من `alghanem` في أيّ ملفٍّ، بشجرة التحليل لا بالنصّ."""

    modules = sorted(PACKAGE.glob("*.py"))
    assert len(modules) >= 4
    for module in modules:
        for name in _imported_names(module):
            assert not name.split(".")[0] == FOREIGN, f"{module.name} ← {name}"


def test_the_tests_import_nothing_from_the_other_tree() -> None:
    """واختباراتُها كذلك، وإلّا كان الفصلُ في المتن دون الفحص."""

    for module in sorted(TESTS.glob("*.py")):
        for name in _imported_names(module):
            assert not name.split(".")[0] == FOREIGN, f"{module.name} ← {name}"


def test_the_package_imports_on_its_own() -> None:
    """تُستورَد الحزمةُ ووحداتُها بلا اسمٍ من تلك الشجرة في المسار."""

    import sys

    import algebra
    import algebra.attainability
    import algebra.decisions
    import algebra.simplicial

    assert algebra.__file__ is not None
    assert Path(algebra.__file__).resolve().parent == PACKAGE
    assert not [name for name in sys.modules if name.split(".")[0] == FOREIGN]


def test_the_distribution_is_no_longer_named_after_the_other_project() -> None:
    """اسمُ التوزيعة `algebra`: وهو أعمقُ التشابك، إذ كان التثبيتُ يضع تلك الحزمة."""

    data = tomllib.loads((REPOSITORY / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["name"] == "algebra"
    assert "algebra*" in data["tool"]["setuptools"]["packages"]["find"]["include"]
    assert "algebra" in data["tool"]["mypy"]["packages"]


def test_the_package_tests_are_actually_run() -> None:
    """`pyproject` يُشغّل اختباراتِ الحزمة، فلا يكون الفصلُ دعوًى بلا فحص."""

    data = tomllib.loads((REPOSITORY / "pyproject.toml").read_text(encoding="utf-8"))
    assert "tests/algebra" in data["tool"]["pytest"]["ini_options"]["testpaths"]
