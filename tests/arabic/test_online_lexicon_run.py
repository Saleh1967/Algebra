"""شُغِّل ختمُ `363ee517…`: **الفوريُّ تنافسيٌّ ويتعلّم، والمعجمُ الكاملُ نفسُه دون الحدّ**.

على مجتمع ج١ (١٠١٩٣ موضعًا)، والحَكَمُ QAC:

- `THE_OFFLINE_LEXICON`: ف١ **سقط**: المعجمُ الكامل صائبٌ في ٨٠٥٣ (٠٫٧٩٠١) — ارتفع من
  ٠٫٤٧١٥ بلا معجم، ولم يبلغ ٠٫٨٥. فسقط معه: «أنّ المعجمَ (الوضع) وحده يحسم قرارَ الضمير
  الذي أخطأه الاختيارُ المحلّيّ». وتشخيصًا بعد التشغيل: من ٢١٤٠ خطأً، ١١٣٣ جذعُها لم يرد
  لفظًا تامًّا («أَيْدِيهِمْ»)، و٨٠٣ تاؤها مربوطةٌ طُويت هاءً فصار جذعُها معروفًا
  («الْآخِرَةِ» ⟵ الآخر + ه)، و٢٠٢ لا ضميرَ فيها وجذعُها معروف، و٢ غيرُ ذلك. فالمعجمُ الذي
  يحسم معجمُ جذوعٍ لا ألفاظ، وبالتاء المربوطة لا مطويّة.
- `COMPETITIVE`: ف٢ **ثبت**: الفوريُّ صائبٌ في ٧٧٤٧ (٠٫٧٦٠٠)، والنسبةُ ٠٫٩٦٢٠ — ثابتٌ فوق
  ٠٫٩، فالخوارزميةُ الفوريّةُ تنافسيّة.
- `IT_LEARNS`: ف٣ **ثبت**: النسبةُ في الربع الأوّل ٠٫٩١٥٤ وفي الأخير ١٫٠٠١٥ (+٠٫٠٨٦١):
  في آخر المصحف صار الفوريُّ مثلَ الكامل، بل فوقه قليلًا، لأنّ الكاملَ يرى جذوعًا تأتي
  لاحقًا فتغرّه.
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
from test_online_lexicon_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_online_lexicon.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

N = 10_193
ONLINE = 7_747
OFFLINE = 8_053
SHARES = {"offline": "0.7901", "online": "0.7600", "ratio": "0.9620"}
QUARTERS = {"first": "0.9154", "last": "1.0015", "gain": "0.0861"}
GREEDY_BASELINE = "0.4715"
DIAGNOSIS = {"جذع لم يرد": 1_133, "مربوطة": 803, "بلا ضمير": 202, "غيره": 2}
QUOTED_FALLEN = {"ف١": "أنّ المعجمَ (الوضع) وحده يحسم قرارَ الضمير"}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_online_lexicon", READER)
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
    assert DIGEST.startswith("363ee517")


def test_the_offline_lexicon_falls_short() -> None:
    """ف١ سقط: ٨٠٥٣ من ١٠١٩٣."""

    found = _census()
    assert (found["n"], found["online"], found["offline"]) == (N, ONLINE, OFFLINE)
    assert f"{OFFLINE / N:.4f}" == SHARES["offline"]
    assert f"{ONLINE / N:.4f}" == SHARES["online"]
    assert float(GREEDY_BASELINE) < OFFLINE / N
    assert sum(DIAGNOSIS.values()) == N - OFFLINE
    assert _one("ف١").verdict(Fraction(OFFLINE, N)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ف١"] in _one("ف١").falsifies


def test_the_online_lexicon_is_competitive_and_learns() -> None:
    """ف٢ وف٣ ثبتا."""

    found = _census()
    ratio, first, last = found["ratio"], found["first"], found["last"]
    assert isinstance(ratio, Fraction) and isinstance(first, Fraction)
    assert isinstance(last, Fraction)
    assert ratio == Fraction(ONLINE, OFFLINE)
    assert f"{float(ratio):.4f}" == SHARES["ratio"]
    assert f"{float(first):.4f}" == QUARTERS["first"]
    assert f"{float(last):.4f}" == QUARTERS["last"]
    assert f"{float(last - first):.4f}" == QUARTERS["gain"]
    assert _one("ف٢").verdict(ratio) is Verdict.MET
    assert _one("ف٣").verdict(last - first) is Verdict.MET


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شيء: ف٢ وف٣ مرّا بتعليلهما (الفوريُّ يبني المعجمَ ممّا مرّ به)."""
