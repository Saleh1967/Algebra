"""شُغِّل ختمُ `1b3a639a…`: **الطبقةُ الأولى ثبت صوابُها وتعلُّمها، وسقط تنافسُها
وتعميمُها**.

على ٦٩٨٤٣ كلمةً في الآيات المتطابقة، والحَكَمُ QAC:

- `ONLINE_RIGHT`: س١ **ثبت على الحدّ**: الفوريُّ صائبٌ في ٥٩٤٩٨ (٠٫٨٥١٩).
- `IT_LEARNS`: س٣ **ثبت**: الربعُ الأوّل ٠٫٨٠١٤، والأخير ٠٫٨٨٣٨ (+٠٫٠٨٢٣).
- `COMPETITIVE`: س٢ **سقط على الحدّ**: غيرُ الفوريّ ٦٦٤٦٢ (٠٫٩٥١٦)، والنسبةُ ٠٫٨٩٥٢.
  فسقط معه:
  «أنّ التقطيعَ الفوريَّ تنافسيٌّ بنسبةٍ ثابتة» — بحدّ ٠٫٩.
- `GENERALISES`: س٤ **سقط**: في الهياكل التي لم تُرَ صائبٌ في ٦٩٦٢ من ١٣٦٨٢ (٠٫٥٠٨٨).
  فسقط معه:
  «أنّ الهندسةَ العكسيّة استخرجت قاعدةً تتعدّى الحفظ».

**وتشخيصًا بعد التشغيل**: أخطاءُ الفوريّ ١٠٣٤٥؛ منها ٣٦٢٥ في هياكلَ محفوظةٍ جاء
جوابُها بتوقيعٍ
آخر — ووسومُ QAC للواو والفاء (CONJ، REM، CIRC، SUP، RSLT، CAUS) تفرّق بالمعنى لا
بالرسم، فهذا
الجزءُ من التوقيع من الطبقة السادسة لا الأولى؛ و٦٧٢٠ في هياكلَ لم تُرَ: قسمُ الجذع
وحده ٢٢٥٥،
واللواحقُ وحدها ١٣١٩، ومعًا ١٢١١، والسوابقُ وحدها ٧٢٠، والباقي مركّب. **فالخطوةُ
التالية**:
توقيعٌ بالرسم وحده (الواو واوٌ بلا وسمها المعنويّ)، وقسمُ الجذع من الطبقة الثانية
بعلامات الاسم.
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
from test_ladder_segmentation_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_ladder_segmentation.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

N = 69_843
ONLINE = 59_498
OFFLINE = 66_462
UNSEEN = (6_962, 13_682)
SHARES = {
    "online": "0.8519",
    "offline": "0.9516",
    "ratio": "0.8952",
    "unseen": "0.5088",
}
QUARTERS = {"first": "0.8014", "last": "0.8838", "gain": "0.0823"}
DIAGNOSIS = {"محفوظ بلبس": 3_625, "لم يُرَ": 6_720, "كلّها": 10_345}
UNSEEN_PARTS = {"قسم الجذع": 2_255, "اللواحق": 1_319, "معًا": 1_211, "السوابق": 720}
QUOTED_FALLEN = {
    "س٢": "أنّ التقطيعَ الفوريَّ تنافسيٌّ بنسبةٍ ثابتة",
    "س٤": "أنّ الهندسةَ العكسيّة استخرجت قاعدةً تتعدّى الحفظ",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_ladder_segmentation", READER)
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
    assert DIGEST.startswith("1b3a639a")


def test_online_right_and_learning() -> None:
    """س١ وس٣ ثبتا."""

    f = _census()
    assert (f["n"], f["online"], f["offline"]) == (N, ONLINE, OFFLINE)
    assert f"{ONLINE / N:.4f}" == SHARES["online"]
    assert f"{OFFLINE / N:.4f}" == SHARES["offline"]
    first, last = f["first"], f["last"]
    assert isinstance(first, Fraction) and isinstance(last, Fraction)
    assert f"{float(first):.4f}" == QUARTERS["first"]
    assert f"{float(last):.4f}" == QUARTERS["last"]
    assert f"{float(last - first):.4f}" == QUARTERS["gain"]
    assert _one("س١").verdict(Fraction(ONLINE, N)) is Verdict.MET
    assert _one("س٣").verdict(last - first) is Verdict.MET


def test_competitive_and_generalising_fall() -> None:
    """س٢ وس٤ سقطا."""

    f = _census()
    assert (f["unseen_right"], f["unseen"]) == UNSEEN
    assert f"{ONLINE / OFFLINE:.4f}" == SHARES["ratio"]
    assert f"{UNSEEN[0] / UNSEEN[1]:.4f}" == SHARES["unseen"]
    assert (
        DIAGNOSIS["محفوظ بلبس"] + DIAGNOSIS["لم يُرَ"] == DIAGNOSIS["كلّها"] == N - ONLINE
    )
    assert UNSEEN[1] - UNSEEN[0] == DIAGNOSIS["لم يُرَ"]
    assert sum(UNSEEN_PARTS.values()) < DIAGNOSIS["لم يُرَ"]
    assert _one("س٢").verdict(Fraction(ONLINE, OFFLINE)) is Verdict.FALSIFIED
    assert _one("س٤").verdict(Fraction(*UNSEEN)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["س٢"] in _one("س٢").falsifies
    assert QUOTED_FALLEN["س٤"] in _one("س٤").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("س١",)
"""س١ مرّ على الحدّ، وتعليلُه (الاستخراجُ الفوريّ) لم يُؤيَّد: صوابُه من الحفظ،
والتعميمُ سقط (س٤)."""
