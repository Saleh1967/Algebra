"""حارسُ جدولِ وحداتِ المعياريّة.

**العطلُ الذي يتجنّبه**: جدولٌ يُكتَب مرّةً ثمّ يُستورَد بعده استيرادٌ
جديدٌ فيبقى الجدولُ ناقصًا وهو يُقرَأ. **فالنقصُ ههنا صامت**: لا يسقط
شيءٌ، ويبقى القارئُ يحسب أنّه قرأ الشجرةَ كلَّها.

فهذه الفحوصُ تُثبّت ثلاثةً:
١. كلُّ وحدةٍ مستورَدةٍ لها مُدخَلٌ في «ما لا تُعطيه» — **وإلّا سقط**.
٢. المكتوبُ في `docs/` يطابق المولَّدَ حسابًا.
٣. قائمةُ المسموحِ مقروءةٌ من الحارسِ نفسِه لا منسوخةً — فلا موضعان
   لعقدٍ واحد.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[2]
GENERATOR: Final[Path] = REPOSITORY / "tools" / "write_module_map.py"
PAPER: Final[Path] = REPOSITORY / "docs" / "وحدات-المعياريّة.md"
AUDIT: Final[Path] = REPOSITORY / "tests" / "algebra" / "test_package_self_audit.py"


def _loaded() -> ModuleType:
    spec = importlib.util.spec_from_file_location("write_module_map", GENERATOR)
    assert spec is not None and spec.loader is not None
    found = importlib.util.module_from_spec(spec)
    sys.modules["write_module_map"] = found
    spec.loader.exec_module(found)
    return found


MAP: Final[ModuleType] = _loaded()


def test_every_imported_module_has_a_withheld_entry() -> None:
    """استيرادٌ بلا مُدخَلٍ يُسقِط الفحصَ ولا يمرُّ صامتًا."""

    use, _ = MAP.scan()
    assert MAP.undocumented(use) == ()


def test_a_new_import_without_an_entry_is_refused() -> None:
    """الحالةُ المُكذِّبة: وحدةٌ مستورَدةٌ زائدةٌ يجب أن تُسمّى نقصًا.

    وتُصطنَع بالإضافةِ إلى المسحِ لا بالكتابةِ في الشجرة — فالحارسُ
    يُختبَر بنسخةٍ في الذاكرة، ولا يُلمَس ملفٌّ مُودَع.
    """

    use, _ = MAP.scan()
    intruder = next(
        name
        for name in sorted(sys.stdlib_module_names)
        if name not in use and name not in MAP.WITHHELD
    )
    assert MAP.undocumented({**use, intruder: {"الجبر": 1}}) == (intruder,)


def test_the_allowlist_is_read_from_the_guard_not_copied() -> None:
    """القائمةُ المقروءةُ هي عينُ القائمةِ في `test_package_self_audit`.

    فلو نُسخت، اختلفت النسختان ولو مرّتا. والقراءةُ تُبطل الموضعَ الثاني.
    """

    read = MAP.allowlist()
    tree = ast.parse(AUDIT.read_text(encoding="utf-8"), filename=AUDIT.name)
    literal = {
        one.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(t.id == "standard" for t in node.targets if isinstance(t, ast.Name))
        and isinstance(node.value, ast.Set)
        for one in node.value.elts
        if isinstance(one, ast.Constant) and isinstance(one.value, str)
    }
    assert read == frozenset(literal)
    assert len(read) == 19


def test_algebra_never_imports_unicodedata() -> None:
    """القياسُ لا يُبنى على جدولٍ يتغيّر بإصدارِ المفسّر.

    و`unicodedata` تُستعمَل خارجَ الجبرِ، فالمنعُ موضعيٌّ لا كُلّيّ.
    """

    use, _ = MAP.scan()
    assert "الجبر" not in use["unicodedata"]
    assert sum(use["unicodedata"].values()) > 0


def test_the_written_table_equals_the_generated_one() -> None:
    """وثيقةٌ تخالف شجرتَها تُرَدّ."""

    assert PAPER.read_text(encoding="utf-8") == MAP.render()


def test_the_permission_is_wider_than_the_use_and_the_gap_is_named() -> None:
    """الرخصةُ غيرُ المُستعمَلةِ مقيسةٌ ومطبوعةٌ، لا مسكوتٌ عنها."""

    use, _ = MAP.scan()
    exercised = {name for name, rows in use.items() if "الجبر" in rows}
    unexercised = MAP.allowlist() - exercised
    assert unexercised, "لو خلا الفرقُ لوجب حذفُ هذا القسمِ من الوثيقة"
    for name in unexercised:
        assert f"`{name}`" in PAPER.read_text(encoding="utf-8")
