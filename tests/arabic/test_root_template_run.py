"""شُغِّل ختمُ `7a042f97…`: **القالبُ ⊗ الجذر يعمّم ويولّد، والجِدّةُ ليست تركيبًا
لقوالبَ كاملة**.

- `THE_MIRROR`: ن٠ **ثبت**: ٤٥٢٧٥ من ٤٥٢٧٥ — فحصُ آلةٍ لا دعوى.
- `NOVELTY_IS_RECOMBINATION`: ن١ **سقط**: من ٦٨٤٢ لفظًا جديدًا في الفرديّ، ٣٤٨٠
  قالبُها وجذرُها
مشهودان (٠٫٥٠٨٦). فسقط معه: «أنّ جِدّةَ اللفظ تركيبٌ لقالبٍ وجذرٍ مشهودَين».
  وتشخيصًا بعد
التشغيل: من ٣٣٦٢ غيرِ مركَّب، ٢٩٤٠ قالبُها جديدٌ وجذرُها مشهود، و٢٦٨ جذرُها جديد،
  و١٥٤ كلاهما.
فالقالبُ الكامل يحمل السوابقَ واللواحق فيتكاثر (٥٤٩١ قالبًا): **والعاملُ الناقص في
  النموذج أنّ
  القالبَ نفسَه حاصلُ ضرب** — سابقةٌ ⊗ وزنٌ ⊗ لاحقة.
- `PEEL_GENERALISES`: ن٢ **ثبت**: التقشيرُ يستردّ جذرَ ٣٠٧٤ من ٣٤٨٠ (٠٫٨٨٣٣).
- `STRUCTURE_GENERATES`: ن٣ **ثبت بفارقٍ كبير**: من ١٨٧٥٤٤ زوجًا مولَّدًا بالجوار
  وقع في الفرديّ
  ١٤١٧، ومن مثلها عشوائيًّا ٦٦ — نحو ٢١٫٥ ضعفًا.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

import pytest
from frozen_corpus import CORPUS, requires_corpus
from test_root_template_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_root_template.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

FOUND = {
    "observations": 45_275,
    "templates": 5_491,
    "roots": 1_329,
    "novel": 6_842,
    "covered": 3_480,
    "right": 3_074,
    "generated": 187_544,
    "hits": 1_417,
    "base_hits": 66,
    "roundtrip": 45_275,
}
SHARES = {"ن١": "0.5086", "ن٢": "0.8833", "ن٣": "21.5"}
DIAGNOSIS = {"قالب جديد": 2_940, "جذر جديد": 268, "كلاهما": 154, "غير مركب": 3_362}
QUOTED_FALLEN = {"ن١": "أنّ جِدّةَ اللفظ تركيبٌ لقالبٍ وجذرٍ مشهودَين"}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_root_template", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _census() -> dict[str, object]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().census(text, QAC)  # type: ignore[no-any-return]


def _one(name: str):  # type: ignore[no-untyped-def]
    return next(one for one in PREDICTIONS if one.identifier == name)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("7a042f97")


def test_the_counts_are_as_recorded() -> None:
    """الأعدادُ كما رُويت."""

    assert _census() == FOUND
    assert f"{FOUND['covered'] / FOUND['novel']:.4f}" == SHARES["ن١"]
    assert f"{FOUND['right'] / FOUND['covered']:.4f}" == SHARES["ن٢"]
    assert f"{FOUND['hits'] / FOUND['base_hits']:.1f}" == SHARES["ن٣"]
    parts = DIAGNOSIS["قالب جديد"] + DIAGNOSIS["جذر جديد"] + DIAGNOSIS["كلاهما"]
    assert parts == DIAGNOSIS["غير مركب"] == FOUND["novel"] - FOUND["covered"]


def test_the_verdicts() -> None:
    """ن٠ ون٢ ون٣ ثبتت، ون١ سقط."""

    assert _one("ن٠").verdict(Fraction(45_275, 45_275)) is Verdict.MET
    assert _one("ن١").verdict(Fraction(3_480, 6_842)) is Verdict.FALSIFIED
    assert _one("ن٢").verdict(Fraction(3_074, 3_480)) is Verdict.MET
    lift = Fraction(1_417, 187_544) / Fraction(66, 187_544)
    assert _one("ن٣").verdict(lift) is Verdict.MET
    assert QUOTED_FALLEN["ن١"] in _one("ن١").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ن٠",)
"""ن٠ مرّ بالإنشاء: المرآةُ صحيحةٌ لأنّ البناءَ عكسُ القالب تعريفًا، فلا تعليلَ لغويَّ يؤيّده."""
