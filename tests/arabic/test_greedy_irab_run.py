"""شُغِّل ختمُ `9390b473…`: **قرارُ العامل جشعٌ أمثل، وقراراتُ السطح ليست كذلك**.

على ٥٧٧١ آيةً متطابقة، والحَكَمُ QAC:

- `THE_GOVERNOR_IS_GREEDY`: ج٤ **ثبت**: تالي الجارّ المنفصل مجرورٌ في QAC في ٣٤١٢ من ٣٤١٣
  (٠٫٩٩٩٧) — والواحدُ «أَيِّ».
- `NEAREST_COORDINATION`: ج٥ **ثبت على الحدّ**: «وال…» بعد جارٍّ ومجرور مجرورٌ في ٨٣ من ٩٢
  (٠٫٩٠٢٢)، والتسعةُ هي بأعيانها مواضعُ القرائن الأربع في مسوّدة الجرّ.
- `LONGEST_PRONOUN`: ج١ **سقط**: ٤٨٠٦ من ١٠١٩٣ (٠٫٤٧١٥). فسقط معه: «أنّ اختيارَ أطول ضميرٍ
  محلّيًّا يحقّق خاصّيةَ الاختيار الجشع». وتشخيصًا بعد التشغيل: من ٥٣٨٧ خطأً، ٥٣٦٨ ليس فيها
  ضميرٌ أصلًا («اللَّهِ»، «الْقِيَامَةِ»: الهاءُ أصلٌ أو تاءٌ مربوطةٌ مطويّة)، و١٤ فقط كان
  الصوابُ فيها ضميرًا أقصر. فالذي فشل قرارُ «هنا ضمير»، لا اختيارُ الأطول بين الضمائر.
- `CUT_THE_PREFIX`: ج٢ **سقط**: ١١٣٤٩ من ١٢١٠٠ (٠٫٩٣٧٩). فسقط معه: «أنّ قطعَ الواو والفاء
  أوّلَ اللفظ يحقّق خاصّيةَ الاختيار الجشع» — جذورٌ أوّلُها واوٌ أو فاء («فَضْلِهِ»، «وَاحِدَةً»،
  «وَعْدَ»، «وَجَدْنَا»).
- `RANK_THE_TEMPLATES`: ج٣ **سقط** (وتوقّعتُ ثباته): ١١٦٤ من ١٥٢٢ (٠٫٧٦٤٨). فسقط معه:
  «أنّ ترتيبَ القوالب يحقّق خاصّيةَ الاختيار الجشع ببرهان التبادل»: وزنُ QAC كان بين المرشَّحات
  وأخذ الترتيبُ غيرَه («يَتَّقُونَ»، «يَفْتَرُونَ» افتعال؛ «أَخَافُ» للمتكلّم).
- `THE_SUBSTRUCTURE`: ب١ **سقط** (وتوقّعتُ ثباته): ٥٢١ من ٦٠٩ (٠٫٨٥٥٥). فسقط معه: «أنّ قرارَ
  الجارّ ذو بنيةٍ جزئيّةٍ مثلى تتكرّر على المسألة الأصغر». وتشخيصًا بعد التشغيل: الشرطُ عدّ
  العلَمَ («اللَّهِ» بلا DET في QAC) قابلًا للإضافة؛ وبعزله ٤٨٧ من ٥٠٦ — تشخيصٌ لا يصحّح الحكم.
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
from test_greedy_irab_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_greedy_irab.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

ALIGNED = 5_771
HITS = {
    "ج١": (4_806, 10_193),
    "ج٢": (11_349, 12_100),
    "ج٣": (1_164, 1_522),
    "ج٤": (3_412, 3_413),
    "ج٥": (83, 92),
    "ب١": (521, 609),
}
SHARES = {
    "ج١": "0.4715",
    "ج٢": "0.9379",
    "ج٣": "0.7648",
    "ج٤": "0.9997",
    "ج٥": "0.9022",
    "ب١": "0.8555",
}
DIAGNOSIS = {"بلا ضمير": 5_368, "أقصر": 14, "أخطاء ج١": 5_387, "ب١ بلا علم": (487, 506)}
QUOTED_FALLEN = {
    "ج١": "أنّ اختيارَ أطول ضميرٍ محلّيًّا يحقّق خاصّيةَ الاختيار الجشع",
    "ج٢": "أنّ قطعَ الواو والفاء أوّلَ اللفظ يحقّق خاصّيةَ الاختيار الجشع",
    "ج٣": "أنّ ترتيبَ القوالب يحقّق خاصّيةَ الاختيار الجشع ببرهان التبادل",
    "ب١": "أنّ قرارَ الجارّ ذو بنيةٍ جزئيّةٍ مثلى تتكرّر على المسألة الأصغر",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_greedy_irab", READER)
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
    assert DIGEST.startswith("9390b473")


def test_the_counts_are_as_recorded() -> None:
    """العدُّ كما سُجِّل، والحصصُ كما رُويت."""

    found = _census()
    assert found["aligned"] == ALIGNED
    hits = found["hits"]
    assert isinstance(hits, dict)
    assert {k: tuple(v) for k, v in hits.items()} == HITS
    for name, (good, total) in HITS.items():
        assert f"{good / total:.4f}" == SHARES[name]
    assert DIAGNOSIS["بلا ضمير"] + DIAGNOSIS["أقصر"] < DIAGNOSIS["أخطاء ج١"]
    assert HITS["ج١"][1] - HITS["ج١"][0] == DIAGNOSIS["أخطاء ج١"]


def test_the_governor_decisions_are_greedy() -> None:
    """ج٤ وج٥ ثبتا."""

    assert _one("ج٤").verdict(Fraction(3_412, 3_413)) is Verdict.MET
    assert _one("ج٥").verdict(Fraction(83, 92)) is Verdict.MET


def test_the_surface_decisions_are_not() -> None:
    """ج١ وج٢ وج٣ سقطت."""

    assert _one("ج١").verdict(Fraction(4_806, 10_193)) is Verdict.FALSIFIED
    assert _one("ج٢").verdict(Fraction(11_349, 12_100)) is Verdict.FALSIFIED
    assert _one("ج٣").verdict(Fraction(1_164, 1_522)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج١"] in _one("ج١").falsifies
    assert QUOTED_FALLEN["ج٢"] in _one("ج٢").falsifies
    assert QUOTED_FALLEN["ج٣"] in _one("ج٣").falsifies


def test_the_substructure_falls_as_written() -> None:
    """ب١ سقط: ٥٢١ من ٦٠٩."""

    assert _one("ب١").verdict(Fraction(521, 609)) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ب١"] in _one("ب١").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شيء: ج٤ وج٥ مرّا بتعليلهما — والتسعةُ في ج٥ مواضعُ القرائن نفسُها."""
