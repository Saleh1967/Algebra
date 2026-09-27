"""شُغِّل ختمُ `8fc24141…`: **الإعلالُ عاملٌ رابعٌ ضروريّ، لكنّه لا يُقرأ من الرسم
وحده؛ ومع مخزن الجذور يعمّم التقشيرُ الأعمى**.

- `THE_MIRROR`: ع٠ **ثبت**: ٤٤٨٩١ من ٤٤٨٩١ — فحصُ آلةٍ لا دعوى.
- `ILAL_ALONE`: ع١ **سقط**: بالإعلال بلا R أصاب ١٣٥٢ من ٢٨١٢ معتلًّا جديدًا
  (٠٫٤٨٠٨). فسقط معه: «أنّ قواعدَ القلب والحذف وحدها تردّ المعتلَّ إلى جذره من
  الرسم» — فالرسمُ لا يفرّق الياءَ المقلوبةَ عن واوٍ من الياء الأصليّة.
- `BLIND_PEEL`: ع٢ **ثبت**: بالإعلال وR أصاب ٦٢٤٣ من ٦٧٤٢ جديدًا (٠٫٩٢٦٠)، وكان
  في ختم الأوزان ٠٫٧٢٩٦ فسقط.
- `WEAK_ROOTS`: ع٣ **ثبت**: في المعتلّ والمهموز ٢٥٠٠ من ٢٨١٢ (٠٫٨٨٩٠)، وكان ٠٫٤٦.
- `SOUND_ROOTS`: ع٤ **ثبت**: في الصحيح ٣٧٤٣ من ٣٩٣٠ (٠٫٩٥٢٤).
- `ILAL_IS_NEEDED`: ع٥ **ثبت**: بـR وحده أصاب في المعتلّ ١٩٢٧ (٠٫٦٨٥٣)، فالفضلُ
  نحو ٠٫٢٠٣٨.

وتشخيصُ ما بقي من المعتلّ (٣١٢) بعد التشغيل: زوجُ الوزن والإعلال جديدٌ ١٣٣،
وكلُّ العوامل مشهودةٌ والاختيارُ أخطأ ١٢٥، والجذرُ جديدٌ ٥٠، وكلاهما ٤.
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
from test_ilal_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_ilal.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

FOUND = {
    "aligned": 44_891,
    "consistent": 44_891,
    "roundtrip": 44_891,
    "wazns": 1_015,
    "shapes": 873,
    "ilal": 22,
    "novel": 6_742,
    "covered": 5_930,
    "weak": 2_812,
    "sound": 3_930,
    "weak_ilal": 1_352,
    "sound_ilal": 3_622,
    "weak_ilal_root": 2_500,
    "sound_ilal_root": 3_743,
    "weak_root": 1_927,
    "sound_root": 3_745,
}
SHARES = {
    "ع١": "0.4808",
    "ع٢": "0.9260",
    "ع٣": "0.8890",
    "ع٤": "0.9524",
    "ع٥": "0.2038",
    "R وحده": "0.6853",
}
BEFORE = {"و٣": "0.7296", "معتل": "0.46"}
RIGHT_ALL = 6_243
RESIDUE = {"زوج جديد": 133, "اختيار": 125, "جذر جديد": 50, "كلاهما": 4}
RESIDUE_TOTAL = 312
QUOTED_FALLEN = {
    "ع١": "أنّ قواعدَ القلب والحذف وحدها تردّ المعتلَّ إلى جذره من الرسم",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_ilal", READER)
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
    assert DIGEST.startswith("8fc24141")


def test_the_counts_are_as_recorded() -> None:
    """الأعدادُ كما رُويت، والتشخيصُ يجمع إليها."""

    assert _census() == FOUND
    weak, sound = FOUND["weak"], FOUND["sound"]
    assert weak + sound == FOUND["novel"]
    assert FOUND["weak_ilal_root"] + FOUND["sound_ilal_root"] == RIGHT_ALL
    assert f"{FOUND['weak_ilal'] / weak:.4f}" == SHARES["ع١"]
    assert f"{RIGHT_ALL / FOUND['novel']:.4f}" == SHARES["ع٢"]
    assert f"{FOUND['weak_ilal_root'] / weak:.4f}" == SHARES["ع٣"]
    assert f"{FOUND['sound_ilal_root'] / sound:.4f}" == SHARES["ع٤"]
    assert f"{FOUND['weak_root'] / weak:.4f}" == SHARES["R وحده"]
    gain = (FOUND["weak_ilal_root"] - FOUND["weak_root"]) / weak
    assert f"{gain:.4f}" == SHARES["ع٥"]
    assert f"{4_919 / 6_742:.4f}" == BEFORE["و٣"]
    assert f"{1_295 / 2_812:.2f}" == BEFORE["معتل"]
    left = weak - FOUND["weak_ilal_root"]
    assert sum(RESIDUE.values()) == RESIDUE_TOTAL == left


def test_the_verdicts() -> None:
    """ع٠ وع٢ وع٣ وع٤ وع٥ ثبتت، وع١ سقط."""

    weak, sound = FOUND["weak"], FOUND["sound"]
    assert _one("ع٠").verdict(Fraction(44_891, 44_891)) is Verdict.MET
    assert _one("ع١").verdict(Fraction(1_352, weak)) is Verdict.FALSIFIED
    assert _one("ع٢").verdict(Fraction(RIGHT_ALL, 6_742)) is Verdict.MET
    assert _one("ع٣").verdict(Fraction(2_500, weak)) is Verdict.MET
    assert _one("ع٤").verdict(Fraction(3_743, sound)) is Verdict.MET
    assert _one("ع٥").verdict(Fraction(2_500 - 1_927, weak)) is Verdict.MET
    assert QUOTED_FALLEN["ع١"] in _one("ع١").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ع٠",)
"""ع٠ مرّ بالإنشاء: البناءُ عكسُ التفكيك تعريفًا، فلا تعليلَ لغويَّ يؤيّده."""
