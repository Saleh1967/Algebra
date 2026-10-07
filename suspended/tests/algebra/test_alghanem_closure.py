"""النقلُ مغلقٌ مفحوصًا: كلُّ استيرادٍ داخلَ `src/alghanem` له ملفٌّ ههنا.

**الغرض**: أن يعمل المستودعان مستقلَّين. فالأمثلةُ العربيّةُ كانت تستورد شجرةَ
الغانم من خارج، فتسقط بـ`ModuleNotFoundError` في كلّ نسخةٍ لا تجاورها تلك
الشجرة — وذلك ما أخرجه التشغيلُ في الفصل السابق. فنُقِل **الإغلاقُ اللازم**
بالشيفرة لا بالإحالة.

`A_PORT_IS_CLOSED_OR_IT_IS_A_PROMISE`: والنقلُ لا يُقاس بعدد ما نُقِل بل
**بإغلاقه**: مديولٌ واحدٌ يشير إلى ما لم يُنقَل يُسقِط الاستقلالَ كلَّه. فيُقرَأ
كلُّ `import` في هذه الشجرة بشجرة التحليل، ويُطلَب له ملفٌّ ههنا. وناقصٌ واحدٌ
يُرَدّ باسمه.

`THE_CLOSURE_IS_WHAT_THIS_TREE_REACHES_AND_NOTHING_MORE`: وسبعةٌ وثلاثون
مديولًا و١٤٬١٠٢ سطرًا — وهي بالضبط ما تصل إليه الأمثلةُ السبعةُ
**و`tests/arabic`** عبر الاستيراد المتعدّي. عشرون كانت ههنا، **وسبعةَ عشرَ
نُقِلت الآن**. وشجرتُها الأصليّةُ تزيد على مئةٍ وثمانيةٍ وستّين ألفَ سطر، فلم
يُنقَل منها إلّا **ثُمنُها تقريبًا**: انتقاءٌ محسوبٌ لا استنساخ.

`THE_PORT_REVIVED_A_SUITE_THAT_WAS_NEVER_COLLECTED`: و`tests/arabic` فيها
عشرون ملفًّا و١٨٧ فحصًا، وكانت **خارجَ `testpaths`** وسبعةٌ منها تسقط عند
الجمع. فلمّا اكتمل النقلُ جُمِعت كلُّها: ١٦٢ تعمل، و٢٤ تنتظر متنًا لم يُنقَل
(الشفرةُ وحدَها نُقِلت)، وواحدٌ يعُدّ ملفّاتِ شجرته فيقيس هذا المستودعَ لا
الذي كُتِب له. والخمسةُ والعشرون **متخطّاةٌ بسببٍ مكتوبٍ لا محذوفةٌ صمتًا**.

`TWO_PACKAGES_SIDE_BY_SIDE_ARE_NOT_TWO_PACKAGES_ENTANGLED`: ولا يعيد هذا
ربطَ الحزمتين: `algebra` لا تستورد `alghanem` حرفًا، وذلك مفحوصٌ في
`test_separation` بقراءة شجرة التحليل. فهما جارتان في مستودعٍ واحدٍ لا
متداخلتان، والجوارُ غيرُ التبعيّة.

`THE_PACKAGE_INIT_IS_DELIBERATELY_EMPTY`: و`alghanem/arabic/__init__.py` في
شجرته الأصليّة **ألفان ومئتان واثنان وتسعون سطرًا** يُعيد تصديرَ ما لا تحتاجه
الأمثلة. ونقلُه كان يجرّ الشجرةَ كلَّها، فكُتِب مختصرًا لا يُصدِّر شيئًا —
والأمثلةُ تستورد مديولاتِها بأسمائها فلا تمرّ به.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PORT = REPOSITORY / "src" / "alghanem"
PACKAGE = "alghanem"


def _modules() -> list[Path]:
    return sorted(PORT.rglob("*.py"))


def _module_name(path: Path) -> str:
    parts = path.relative_to(PORT).with_suffix("").parts
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join((PACKAGE, *parts))


def _resolves(name: str) -> bool:
    """أللاسمِ ملفٌّ في هذا النقل؟ ويُقبَل أن يكون اسمًا داخلَ مديول."""

    parts = name.split(".")
    if parts[0] != PACKAGE:
        return True  # ليس من هذه الشجرة، فليس من شأن الإغلاق
    base = PORT.joinpath(*parts[1:])
    if base.with_suffix(".py").exists() or (base / "__init__.py").exists():
        return True
    parent = PORT.joinpath(*parts[1:-1])  # اسمٌ مُصدَّرٌ من مديولٍ أبيه
    return parent.with_suffix(".py").exists() or (parent / "__init__.py").exists()


def _imported_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    here = _module_name(path)
    package = here if path.name == "__init__.py" else here.rsplit(".", 1)[0]
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                stem = package.split(".")
                stem = stem[: len(stem) - node.level + 1]
                module = ".".join([*stem, *([node.module] if node.module else [])])
            else:
                module = node.module or ""
            if module.split(".")[0] != PACKAGE:
                continue
            found.add(module)
            found.update(f"{module}.{alias.name}" for alias in node.names)
    return found


def test_the_port_is_closed_under_its_own_imports() -> None:
    """كلُّ اسمٍ من هذه الشجرة يُستورَد داخلَها له ملفٌّ ههنا — ولا واحدَ ناقص."""

    unresolved: dict[str, list[str]] = {}
    for path in _modules():
        missing = sorted(name for name in _imported_names(path) if not _resolves(name))
        if missing:
            unresolved[str(path.relative_to(PORT))] = missing
    assert not unresolved, unresolved


def test_the_port_carries_exactly_the_closure_and_no_more() -> None:
    """سبعةٌ وثلاثون مديولًا ومِلفّا تهيئة — وهي ما تصل إليه هذه الشجرة لا أكثر."""

    names = {_module_name(path) for path in _modules()}
    packages = {PACKAGE, f"{PACKAGE}.arabic"}
    carried = names - packages

    assert len(carried) == 37
    assert packages <= names
    assert PORT.joinpath("canonical_content.py").exists()
    assert PORT.joinpath("arabic", "classical_makharij_table.py").exists()

    # ولا مجلَّدَ ثالثَ في النقل: الجذرُ و`arabic` لا غير
    folders = {
        path.relative_to(PORT).parts[0]
        for path in _modules()
        if len(path.relative_to(PORT).parts) > 1
    }
    assert folders == {"arabic"}


def test_the_package_inits_export_nothing() -> None:
    """ملفّا التهيئة مختصران عمدًا؛ ونظيرُ أحدهما هناك ٢٬٢٩٢ سطرًا."""

    for name in ("__init__.py", "arabic/__init__.py"):
        source = (PORT / name).read_text(encoding="utf-8")
        tree = ast.parse(source)
        exported = [
            node
            for node in tree.body
            if isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "__all__"
        ]
        assert len(exported) == 1
        assert len(source.splitlines()) < 30
        # ولا استيرادَ من هذه الشجرة فيهما ألبتّة
        assert not _imported_names(PORT / name)


def test_the_two_packages_are_neighbours_not_dependants() -> None:
    """`algebra` لا تستورد `alghanem`؛ والجوارُ في مستودعٍ غيرُ التبعيّة."""

    package = REPOSITORY / "src" / "algebra"
    for path in sorted(package.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert not any(
                    alias.name.split(".")[0] == PACKAGE for alias in node.names
                ), path
            elif isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] != PACKAGE, path

    # والعكسُ كذلك: النقلُ لا يستورد `algebra`
    for path in _modules():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] != "algebra", path
