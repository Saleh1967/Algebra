"""شُغِّل ختمُ `b904a9f9…`: **الموانعُ صدقت، والنموذجُ رفع الكاملَ إلى ٠٫٩٣٢٠ ولم يبلغ الحدّ**.

على مجتمع ج١ (١٠١٩٣ موضعًا)، والحَكَمُ QAC:

- `THE_MARBUTA_BAR`: ح٣ **ثبت**: صفرُ خطأٍ في الألفاظ المنتهية بتاءٍ مربوطة — ذهبت الأخطاءُ
  الـ٨٠٣ كلُّها بمانعٍ واحدٍ من الرسم.
- `THE_FULL_SOLUTION`: ح١ **سقط**: ٩٥٠٠ صوابًا (٠٫٩٣٢٠) — من ٠٫٧٩٠١ قبله ومن ٠٫٤٧١٥
  بلا معجم، ودون ٠٫٩٥. فسقط معه: «أنّ الموانعَ ومعجمَ الجذوع يحلّان معضلةَ
  المعجم». وتشخيصًا بعد
  التشغيل: من ٦٩٣ خطأً، ٥٠٥ جذعُها لم يرد بلاحقتين (نادرٌ: «مَوَازِينُهُ»، «وَحْدَهُ»)، و١٢٨
  جذعُها ورد بلاحقتين ولا ضمير («إِلَهَ» ⟵ «إِلْ»)، و٤٩ قبل ضميرها ياءٌ ساكنةٌ مكتوبة (المثنّى:
  «يَدَيْهِ»، «عَقِبَيْهِ»)، و٦ منع فيها مانعٌ ضميرًا صحيحًا، و٥ ضميرٌ آخر.
- `STILL_ONLINE`: ح٢ **سقط**: الفوريُّ ٨٧٦٦ (٠٫٨٦٠٠)، والنسبةُ ٠٫٩٢٢٧ دون ٠٫٩٥. فسقط معه:
  «أنّ الحلَّ يبقى تنافسيًّا حين يُبنى فوريًّا» — بهذا الحدّ؛ فالنموذجُ يحتاج لاحقتين قد مرّتا،
  فيتعلّم أبطأ من المعجم الكامل.
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
from test_paradigm_lexicon_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_paradigm_lexicon.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

N = 10_193
OFFLINE = 9_500
ONLINE = 8_766
SHARES = {"offline": "0.9320", "online": "0.8600", "ratio": "0.9227"}
BEFORE = {"بلا معجم": "0.4715", "المعجم الكامل": "0.7901", "أخطاء المربوطة": 803}
DIAGNOSIS = {"نموذج": 505, "بلا ضمير": 128, "ياء ساكنة": 49, "مانع": 6, "آخر": 5}
QUOTED_FALLEN = {
    "ح١": "أنّ الموانعَ ومعجمَ الجذوع يحلّان معضلةَ المعجم",
    "ح٢": "أنّ الحلَّ يبقى تنافسيًّا حين يُبنى فوريًّا",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_paradigm_lexicon", READER)
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
    assert DIGEST.startswith("b904a9f9")


def test_the_marbuta_bar_holds() -> None:
    """ح٣ ثبت: صفر."""

    found = _census()
    errors = found["marbuta_errors"]
    assert errors == 0
    assert _one("ح٣").verdict(Fraction(0)) is Verdict.MET


def test_the_full_solution_falls_short() -> None:
    """ح١ سقط: ٩٥٠٠ من ١٠١٩٣."""

    found = _census()
    assert (found["n"], found["offline"], found["online"]) == (N, OFFLINE, ONLINE)
    assert f"{OFFLINE / N:.4f}" == SHARES["offline"]
    assert float(BEFORE["المعجم الكامل"]) < OFFLINE / N
    assert sum(DIAGNOSIS.values()) == N - OFFLINE
    assert _one("ح١").verdict(Fraction(OFFLINE, N)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ح١"] in _one("ح١").falsifies


def test_the_online_ratio_falls_short() -> None:
    """ح٢ سقط: ٠٫٩٢٢٧."""

    found = _census()
    ratio = found["ratio"]
    assert isinstance(ratio, Fraction)
    assert ratio == Fraction(ONLINE, OFFLINE)
    assert f"{ONLINE / N:.4f}" == SHARES["online"]
    assert f"{float(ratio):.4f}" == SHARES["ratio"]
    assert _one("ح٢").verdict(ratio) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ح٢"] in _one("ح٢").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شيء: ح٣ مرّ بتعليله (التاءُ المربوطة في الرسم ليست هاءً)."""
