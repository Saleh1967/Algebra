"""شُغِّل ختمُ `8bf5fda5…`: **بلغ الكاملُ ٠٫٩٦٩٠، والفوريُّ تنافسيّ؛ وسقط حارسُ
  التراجع**.

على مجتمع ج١ (١٠١٩٣ موضعًا)، والحَكَمُ QAC:

- `THE_FULL_SOLUTION`: ط١ **ثبت**: ٩٨٧٧ صوابًا (٠٫٩٦٩٠) — والسلسلةُ عبر الأختام:
  ٠٫٤٧١٥ بلا
  معجم، ثم ٠٫٧٩٠١ بمعجم ألفاظ، ثم ٠٫٩٣٢٠ بالموانع والنموذج، ثم هذا.
- `COMPETITIVE_AGAIN`: ط٢ **ثبت**: الفوريُّ ٩٥٤٣ (٠٫٩٣٦٢)، والنسبةُ ٠٫٩٦٦٢.
- `THE_BACKOFF_GUARD`: ط٣ **سقط**: الضمائرُ المتوهَّمة ٢٨٨، وكانت ١٢٨. فسقط معه:
  «أنّ التراجعَ
  لا يزيد الضمائرَ المتوهَّمة على ما كانت». وتشخيصًا بعد التشغيل: ١٦٥ جاءت من
  التراجع (٩٥
  منها ياءٌ أصليّة: «فَبِأَيِّ»، «بَنِي»، «رَوَاسِيَ»؛ و٣٣ «لله» بسابقة:
  «وَلِلَّهِ»، «تَاللَّهِ»،
  لم يمنعها مانعُ «ال»؛ و٣٧ غيرُ ذلك)، و١٢٣ من النموذج؛ ومنها «إِلَهَ» لأنّ اللفظَ
  نفسَه يشهد
  لجذعه («ال»+ه في المعجم هو هو)، وهو عيبٌ في تعريف النموذج منذ الختم السابق.
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
from test_backoff_lexicon_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_backoff_lexicon.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

N = 10_193
OFFLINE = 9_877
ONLINE = 9_543
PHANTOM = 288
SHARES = {"offline": "0.9690", "online": "0.9362", "ratio": "0.9662"}
CHAIN = ("0.4715", "0.7901", "0.9320", "0.9690")
DIAGNOSIS = {"تراجع: ياء أصلية": 95, "تراجع: لله": 33, "تراجع: غيره": 37, "نموذج": 123}
FROM_BACKOFF = 165
QUOTED_FALLEN = {"ط٣": "أنّ التراجعَ لا يزيد الضمائرَ المتوهَّمة"}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_backoff_lexicon", READER)
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
    assert DIGEST.startswith("8bf5fda5")


def test_the_full_solution_holds() -> None:
    """ط١ ثبت: ٩٨٧٧ من ١٠١٩٣."""

    found = _census()
    assert (found["n"], found["offline"], found["online"]) == (N, OFFLINE, ONLINE)
    assert f"{OFFLINE / N:.4f}" == SHARES["offline"] == CHAIN[-1]
    assert [float(one) for one in CHAIN] == sorted(float(one) for one in CHAIN)
    assert _one("ط١").verdict(Fraction(OFFLINE, N)) is Verdict.MET


def test_the_online_is_competitive() -> None:
    """ط٢ ثبت: ٠٫٩٦٦٢."""

    ratio = _census()["ratio"]
    assert isinstance(ratio, Fraction)
    assert ratio == Fraction(ONLINE, OFFLINE)
    assert f"{ONLINE / N:.4f}" == SHARES["online"]
    assert f"{float(ratio):.4f}" == SHARES["ratio"]
    assert _one("ط٢").verdict(ratio) is Verdict.MET


def test_the_backoff_guard_falls() -> None:
    """ط٣ سقط: ٢٨٨ فوق ١٢٨."""

    assert _census()["phantom"] == PHANTOM
    assert sum(DIAGNOSIS.values()) == PHANTOM
    assert FROM_BACKOFF + DIAGNOSIS["نموذج"] == PHANTOM
    assert _one("ط٣").verdict(Fraction(PHANTOM)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ط٣"] in _one("ط٣").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شيء: ط١ وط٢ مرّا بتعليلهما، وثمنُ التراجع مسجَّلٌ في ط٣ الساقط."""
