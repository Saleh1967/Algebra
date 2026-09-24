"""الحزمةُ تُفحَص بدعواها عن نفسها: «القيدُ في المُنشئ» مقروءًا بالشجرة.

**ما يُقاس ههنا**: أنّ كلَّ صنفِ بياناتٍ في `algebra` إمّا يحمل `__post_init__`
يرُدّ ما لا يصحّ، وإمّا يكون **مركَّبًا من أصنافٍ مقيَّدة** فيرث قيدَها. وما
ليس واحدًا منهما يُسمّى في قائمةٍ مُعلَنةٍ صغيرة، فيُرى إن كبرت.

`AN_AUTOMATED_AUDIT_MAY_OVERSTATE_ITS_OWN_FINDING`: أوّلُ مسحٍ آليٍّ عدَّ خمسةَ
أصنافٍ «بلا قيد» من واحدٍ وأربعين. وقراءةُ المتن أسقطت ثلاثةً منها: `Difference`
و`QuotientClaim` و`Fork` مركَّبةٌ كلُّها من أصنافٍ مقيَّدة (`PrintedFigure`،
`Quotient`، `Case`، `Branch`)، فقيدُها محمولٌ لا غائب. فالمسحُ يُسمّي
المرشَّحين، والقراءةُ تحكم — وعددُ المسح وحدَه كان **يبالغ في العيب**.

`A_CONTAINER_OF_DERIVED_READINGS_IS_NOT_A_GAP`: صنفٌ حقولُه مخرَجُ حسابٍ تَمَّ
قبله لا يُطلَب منه أن يُعيد التحقّق. وإنّما يُطلَب ذلك حين تكون الحقولُ
**قابلةً للاشتقاق من بعضها** — فحينئذٍ مخالفةُ أحدها الآخرَ دعوًى ثانيةٌ
تُرَدّ. وذلك ما وقع في `AttainabilityReading` وقد أُصلِح.
"""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[2] / "src" / "algebra"

COMPOSED_OF_CONSTRAINED_PARTS: frozenset[str] = frozenset(
    {
        "reconciliation.Difference",  # طرفاه `PrintedFigure` مقيَّدان
        "reconciliation.QuotientClaim",  # `Quotient` و`PrintedFigure`
        "stipulation.Weighing",  # لا يُبنى إلّا من `weigh` على `Schema` مقيَّد
        "witness.Fork",  # `Case` وفرعان `Branch` مقيَّدة
    }
)
"""ما قيدُه محمولٌ في مكوّناته؛ وكلُّ اسمٍ هنا قُرِئ متنُه لا اسمُه."""

RAW_READINGS: frozenset[str] = frozenset(
    {
        "contingency.ModelCost",  # أربعةُ أعدادٍ عائمةٍ مخرَجُ حسابٍ تَمَّ قبله
    }
)
"""حاوياتُ قراءاتٍ مُشتَقّة؛ وتُسمّى ههنا كيلا تكثر بلا أن تُرى."""


def _data_classes() -> list[tuple[str, ast.ClassDef]]:
    found: list[tuple[str, ast.ClassDef]] = []
    for path in sorted(PACKAGE.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            decorators = {ast.unparse(one).split("(")[0] for one in node.decorator_list}
            if "dataclass" in decorators:
                found.append((f"{path.stem}.{node.name}", node))
    return found


def _has_post_init(node: ast.ClassDef) -> bool:
    return any(
        isinstance(one, ast.FunctionDef) and one.name == "__post_init__"
        for one in node.body
    )


def test_every_data_class_either_constrains_or_is_named() -> None:
    """لا صنفَ بياناتٍ بلا قيدٍ إلّا وهو مذكورٌ في إحدى القائمتين."""

    classes = _data_classes()
    assert len(classes) >= 40

    unguarded = {name for name, node in classes if not _has_post_init(node)}
    declared = COMPOSED_OF_CONSTRAINED_PARTS | RAW_READINGS
    assert unguarded <= declared, sorted(unguarded - declared)
    assert declared <= unguarded, sorted(declared - unguarded)


def test_the_share_that_constrains_in_its_constructor_is_reported() -> None:
    """ثلاثةٌ وأربعون من ثمانيةٍ وأربعين تقيّد في مُنشئها — والرقمُ يُطبَع لا يُدَّعى.

    وكانت ستًّا وثلاثين من إحدى وأربعين، ثمّ زاد `Taught` و`Segment`، ثمّ
    `ClusteredSample`، ثمّ `Corpus` و`Reading`، ثمّ `ClusterProfile`
    و`EffectReading`. وكلُّها تقيّد في مُنشئها،
    والعدُّ يُعاد عند كلّ زيادة.
    """

    classes = _data_classes()
    guarded = [name for name, node in classes if _has_post_init(node)]
    assert len(classes) == 48
    assert len(guarded) == 43
    assert len(classes) - len(guarded) == len(
        COMPOSED_OF_CONSTRAINED_PARTS | RAW_READINGS
    )


def test_no_module_carries_a_floating_point_literal_outside_a_logarithm() -> None:
    """الكسورُ صحيحةٌ والعائمُ عند اللوغاريتم وحدَه — دعوى الحزمة، مفحوصةً.

    ويُستثنى `1e-12` في `contingency`: هو **تسامحُ مقارنةٍ** بين عائمين لا
    مقدارٌ يدخل حسابًا، ويُسمّى ههنا كيلا يمرّ صامتًا.
    """

    allowed = {1e-12}
    for path in sorted(PACKAGE.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        floats = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, float)
        }
        assert floats <= allowed, f"{path.name}: {sorted(floats - allowed)}"


def test_no_module_imports_beyond_the_standard_library() -> None:
    """لا تابعَ خارجيًّا: ما يُبرهَن بالحساب لا يُستورَد من طرفٍ ثالث.

    والاستيرادُ النسبيُّ (`from .stipulation import`) أخٌ في الحزمة لا تابع،
    فيُستثنى **بمستواه** لا باسمه — والاسمُ وحدَه لا يفرّق بين الأخ والغريب.
    """

    standard = {
        "__future__",
        "abc",
        "argparse",
        "ast",
        "collections",
        "dataclasses",
        "decimal",
        "datetime",
        "enum",
        "fractions",
        "functools",
        "hashlib",
        "itertools",
        "math",
        "pathlib",
        "random",
        "re",
        "sys",
        "typing",
    }
    for path in sorted(PACKAGE.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            relative = isinstance(node, ast.ImportFrom) and node.level > 0
            for name in names:
                if relative:
                    continue  # أخٌ في الحزمة نفسِها، لا تابعٌ خارجيّ
                root = name.split(".")[0]
                assert root in standard or root == "algebra", f"{path.name} ← {name}"
