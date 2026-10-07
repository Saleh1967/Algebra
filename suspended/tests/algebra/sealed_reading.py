"""قراءةُ التشغيلات وأحكامِها **من الشجرة** — لا من قائمةٍ مكتوبةٍ باليد.

هذه أداةُ **قراءةٍ** لا دعوى. تُحمِّل كلَّ `tests/arabic/test_*_run.py`، وتأخذ
منه **الشروطَ التي يحكم بها فعلًا** (مجموعةُ `Prediction` المربوطةُ في متنه)،
ثمّ تقرأ متنَه شجرةً مجرّدة فتردّ لكلّ شرطٍ: **أحُكِم به؟** و**أسقط؟**

**ولمَ الاشتقاقُ لا القائمة**: قائمةٌ مكتوبةٌ تشيخ بلا أن تُرى شيخوختُها،
وختمٌ جديدٌ لا يدخلها فلا يمسُّه مانع. والاشتقاقُ يُدخِله **بمجرّد وجوده**.

**وحدُّ الأداة مُعلَن**: تشغيلٌ يُحمِّل ختمَه **في جوف الدالّة** لا في متن
الوحدة لا تبلغه القراءة، فيُسمّى في `OUT_OF_REACH` ولا يُبتلَع صمتًا.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[2]
ARABIC = REPOSITORY / "tests" / "arabic"

OUT_OF_REACH: frozenset[str] = frozenset(
    {
        "test_cv_peel_run.py",
        "test_encoding_audit_run.py",
        "test_frequency_matched_run.py",
        "test_frozen_corpus_run.py",
        "test_layer_induction_run.py",
        "test_marked_contrast_run.py",
        "test_pan_difference_run.py",
        "test_rejection_matched_run.py",
        "test_root_projection_run.py",
        "test_schema_transition_run.py",
        "test_tanafur_parallel_run.py",
    }
)
"""تشغيلاتٌ من الجيل الأوّل تُحمِّل شروطَها في جوف دوالِّها، فلا تبلغها القراءة.

وهي **مُسمّاةٌ لتُرى**: كلُّ تشغيلٍ جديدٍ يربط شروطَه في متن وحدته، فيدخل
الموانعَ بنفسه. ونموُّ هذه القائمة **عطلٌ يُرى**، لا سكوتٌ يمرّ.
"""

_LOOKUP = re.compile(r'identifier\s*==\s*"([^"]+)"')
_CALLED = re.compile(r'_one\(\s*"([^"]+)"\s*\)')
_BY_NAME = re.compile(r"_one\(\s*[A-Za-z_]|identifier\s*==\s*[A-Za-z_]")


def _load(path: Path) -> Any:
    for home in (str(ARABIC), str(REPOSITORY / "src")):
        if home not in sys.path:
            sys.path.insert(0, home)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:  # pragma: no cover - لا قارئ
        raise SystemExit(f"لا قارئَ لـ{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class Judgement:
    """حكمٌ واحدٌ مقروءٌ من متن التشغيل."""

    identifier: str
    falsified: bool

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("لا حكمَ بلا شرطٍ يُحكَم به")


@dataclass(frozen=True)
class Sealed:
    """تشغيلٌ وشروطُه وأحكامُه، مقروءةً معًا."""

    run: Path
    predictions: tuple[Any, ...]
    judgements: tuple[Judgement, ...]
    literals: tuple[str, ...]
    docstring: str
    body: str

    def __post_init__(self) -> None:
        if not self.predictions:
            raise ValueError(f"تشغيلٌ بلا شروط: {self.run.name}")
        astray = {one.identifier for one in self.judgements} - {
            one.identifier for one in self.predictions
        }
        if astray:
            raise ValueError(f"{self.run.name}: حكمٌ على غير مختوم {sorted(astray)}")

    def marks(self) -> set[str]:
        return {one.identifier for one in self.predictions}

    def judged(self) -> set[str]:
        return {one.identifier for one in self.judgements}

    def falsified(self) -> set[str]:
        return {one.identifier for one in self.judgements if one.falsified}

    def falsifies(self, identifier: str) -> str:
        found = next(one for one in self.predictions if one.identifier == identifier)
        return str(found.falsifies)

    def quotes(self, text: str, least: int = 10) -> bool:
        return any(len(one) >= least and one in text for one in self.literals)


def _strings(scope: ast.AST) -> set[str]:
    return {
        node.value
        for node in ast.walk(scope)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }


def _bound(scope: ast.AST, source: str) -> dict[str, set[str]]:
    """أسماءٌ محلّيّةٌ مربوطةٌ بشرطٍ مختوم: `أولى = next(… == "ل١")`."""

    where: dict[str, set[str]] = {}
    for node in ast.walk(scope):
        if not isinstance(node, ast.Assign):
            continue
        segment = ast.get_source_segment(source, node) or ""
        found = set(_LOOKUP.findall(segment)) | set(_CALLED.findall(segment))
        if not found:
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                where.setdefault(target.id, set()).update(found)
    return where


def _named(segment: str, bound: dict[str, set[str]], loose: set[str]) -> set[str]:
    found = set(_CALLED.findall(segment)) | set(_LOOKUP.findall(segment))
    for name, mapped in bound.items():
        if re.search(rf"\b{re.escape(name)}\b", segment):
            found |= mapped
    if _BY_NAME.search(segment):
        found |= loose  # حلقةٌ تحكم بأسماءٍ مجموعةٍ في الدالّة نفسِها
    return found


def read_all() -> list[Sealed]:
    """كلُّ تشغيلٍ يربط شروطَه في متنه، مقروءًا من الشجرة."""

    from algebra.signified import Prediction

    out: list[Sealed] = []
    for path in sorted(ARABIC.glob("test_*_run.py")):
        module = _load(path)
        found: tuple[Any, ...] = ()
        for value in vars(module).values():
            if (
                isinstance(value, tuple)
                and value
                and all(isinstance(one, Prediction) for one in value)
            ):
                found = value
                break
        if not found:
            continue
        known = {one.identifier for one in found}
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        outer = _bound(tree, source)
        judgements: list[Judgement] = []
        for scope in ast.walk(tree):
            if not isinstance(scope, ast.FunctionDef):
                continue
            bound = dict(outer)
            bound.update(_bound(scope, source))
            loose = _strings(scope) & known
            for node in ast.walk(scope):
                if not isinstance(node, ast.Assert):
                    continue
                segment = ast.get_source_segment(source, node) or ""
                if ".verdict(" not in segment:
                    continue
                fallen = "Verdict.FALSIFIED" in segment
                for identifier in _named(segment, bound, loose) & known:
                    judgements.append(Judgement(identifier, fallen))
        out.append(
            Sealed(
                run=path,
                predictions=found,
                judgements=tuple(judgements),
                literals=tuple(_strings(tree)),
                docstring=ast.get_docstring(tree) or "",
                body=source,
            )
        )
    return out
