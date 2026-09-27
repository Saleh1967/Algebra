"""شُغِّل ختمُ `7f050383…`: **ثبت خمسةٌ وسقط ثلاثة** — والأوضحُ ت٢: المتعدّي يليه المنصوب.

على ٥٧٧١ آيةً تساوى فيها عددُ الألفاظ والكلمات:

- `THE_VERB`: ق٥ **ثبت**: ٠٫٩٤٦١ من ألفاظ الأداة أفعالٌ في QAC (١٣١٩٤ من ١٣٩٤٦).
- `THE_FORM`: ق٣ **ثبت**: الوزنُ واحدٌ في ٠٫٩٣٦٣ (١٢١١٧ من ١٢٩٤١).
- `THE_OBJECT`: ق٤ **ثبت على الحدّ**: الضميرُ المفعول ٠٫٩٠٣١ (٢٠٥٠ من ٢٢٧٠).
- `THE_PASSIVE`: ق١ **سقط** (٠٫٧٩٩٥، ٧١٠ من ٨٨٨) وق٢ **سقط** (٠٫٦٦٦٧، ٧١٠ من ١٠٦٥). فسقط
  معهما: «أنّ قالبَ المجهول في الرسم يرى المجهولَ كما يراه المحلّل»، و«أنّ الأداةَ لا يفوتها
  من المجهول إلّا قليل». **وتشخيصًا**: ما عدّته مجهولًا وهو معلوم أكثرُه مضارعُ أَفْعَلَ المعتلّ
  أو المجزوم («يُوقِنُونَ»، «يُطِعِ»، «يُرِدْ»، «تُصِبْهُمْ») وألفاظٌ ليست أفعالًا («فِيمَا»،
  «عِيسَى»)؛ وما فاتها مجهولُ المعتلّ والمضعَّف («أُوتُوا»، «تُتْلَى»، «يُوحَى»، «تُوعَدُونَ»،
  «أُحِلَّ»، «يُرَدُّ»، «اضْطُرَّ») — قوالبُ ناقصة، لا ظاهرةٌ غائبة.
- `THE_WEIGHT`: ت١ **سقط**: ٦ من ١١ جذرًا (٠٫٥٤٥٥). فسقط معه: «أنّ همزةَ أَفْعَلَ تعدّي اللازم،
  بتحليلٍ مستقلٍّ عن الأداة» — **بهذا الدليل**. وتشخيصًا بعد التشغيل: الخمسةُ الباقية
  ثلاثةٌ منها   مفعولُها اسمٌ ظاهرٌ لا ضمير («يُولِجُ اللَّيْلَ»، «يُرْبِي الصَّدَقَاتِ»، «أَحْبَطَ أَعْمَالَهُمْ»)،
  وواحدٌ مفعولُه محذوف («لَا تُبْقِي وَلَا تَذَرُ»)، وواحدٌ همزتُه للصيرورة («أَثْقَلَتْ»). فالشرطُ
  قاس التعدّي بالضمير والمجهول وحدهما، وهذا أضيقُ من التعدّي.
- `THE_ACCUSATIVE`: ت٢ **ثبت بفارقٍ كبير**: أوّلُ معرَّفٍ بعد الفعل منصوبٌ في QAC بعد المتعدّي
  ٦٠٠ من ٩٧٤، وبعد اللازم ٤٢ من ٢٤٥؛ والفرقُ ٠٫٤٤٤٦ (الحدّ ٠٫١٥).
- `NO_NOMINAL_PASSIVE`: ت٣ **ثبت**: الجذورُ الثلاثة عشر اللازمةُ في الغني ليس لها في QAC
  مجهولٌ   في VF:1 أصلًا.
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
from test_valency_qac_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_valency_qac.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(
        not QAC.exists(), reason="ملفّ QAC (GPL) لا يُودَع؛ يُعطى بـQAC_MORPHOLOGY"
    ),
]

ALIGNED = 5_771
COUNTS = {
    "ق١": (710, 888),
    "ق٢": (710, 1_065),
    "ق٣": (12_117, 12_941),
    "ق٤": (2_050, 2_270),
    "ق٥": (13_194, 13_946),
}
SHARES = {
    "ق١": "0.7995",
    "ق٢": "0.6667",
    "ق٣": "0.9363",
    "ق٤": "0.9031",
    "ق٥": "0.9461",
}
ELIGIBLE = 11
NOT_SHIFTED = ["بقي", "ثقل", "حبط", "ربو", "ولج"]
WEIGHT_SHARE = "0.5455"
AFTER = {
    "متعدٍّ": {"ACC": 600, "NOM": 188, "GEN": 186},
    "لازم": {"ACC": 42, "NOM": 128, "GEN": 75},
}
GAP = "0.4446"
QUOTED_FALLEN = {
    "ق١": "أنّ قالبَ المجهول في الرسم يرى المجهولَ كما يراه المحلّل",
    "ق٢": "أنّ الأداةَ لا يفوتها من المجهول إلّا قليل",
    "ت١": "أنّ همزةَ أَفْعَلَ تعدّي اللازم",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_valency_qac", READER)
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
    assert DIGEST.startswith("7f050383")


def test_the_instrument_against_qac() -> None:
    """ق٣ وق٤ وق٥ ثبتت، وق١ وق٢ سقطا."""

    found = _census()
    assert found["aligned"] == ALIGNED
    counts = found["counts"]
    assert isinstance(counts, dict)
    assert {k: tuple(v) for k, v in counts.items()} == COUNTS
    for name, (hit, total) in COUNTS.items():
        assert f"{hit / total:.4f}" == SHARES[name]
    assert _one("ق١").verdict(Fraction(710, 888)) is Verdict.FALSIFIED
    assert _one("ق٢").verdict(Fraction(710, 1_065)) is Verdict.FALSIFIED
    assert _one("ق٣").verdict(Fraction(12_117, 12_941)) is Verdict.MET
    assert _one("ق٤").verdict(Fraction(2_050, 2_270)) is Verdict.MET
    assert _one("ق٥").verdict(Fraction(13_194, 13_946)) is Verdict.MET
    assert QUOTED_FALLEN["ق١"] in _one("ق١").falsifies
    assert QUOTED_FALLEN["ق٢"] in _one("ق٢").falsifies


def test_the_weight_falls_on_its_narrow_evidence() -> None:
    """ت١ سقط: ٦ من ١١، والخمسةُ مسمّاة."""

    found = _census()
    eligible, shifted = found["eligible"], found["shifted"]
    assert isinstance(eligible, list) and isinstance(shifted, list)
    assert len(eligible) == ELIGIBLE
    assert sorted(set(eligible) - set(shifted)) == NOT_SHIFTED
    share = Fraction(len(shifted), len(eligible))
    assert f"{float(share):.4f}" == WEIGHT_SHARE
    assert _one("ت١").verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ت١"] in _one("ت١").falsifies


def test_the_accusative_follows_the_transitive() -> None:
    """ت٢ ثبت: ٦٠٠ من ٩٧٤ مقابل ٤٢ من ٢٤٥."""

    found = _census()
    after = found["after"]
    assert isinstance(after, dict)
    assert {g: dict(c) for g, c in after.items()} == AFTER
    gap = found["gap"]
    assert isinstance(gap, Fraction)
    assert f"{float(gap):.4f}" == GAP
    assert _one("ت٢").verdict(gap) is Verdict.MET


def test_no_nominal_passive_of_the_lexicon_intransitives() -> None:
    """ت٣ ثبت: صفر."""

    named = _census()["passive_named"]
    assert isinstance(named, dict)
    assert _one("ت٣").verdict(Fraction(sum(named.values()))) is Verdict.MET


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: ق٣ وق٥ مرّا فوق ما توقّعتُ لا دونه."""
