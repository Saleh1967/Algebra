"""شُغِّل ختمُ `66687b35…`: **الأوزانُ مخزنٌ صغيرٌ هو وزنُ الصرف، والجِدّةُ تركيبٌ
بالعوامل الثلاثة؛ والتقشيرُ الأعمى يسقط بالإعلال**.

- `THE_MIRROR`: و٠ **ثبت**: ٤٤٨٩١ من ٤٤٨٩١ — فحصُ آلةٍ لا دعوى.
- `FEW_AWZAN`: و١ **ثبت**: ١٠٠٨ أوزانٍ مقابلَ ٥٤٠١ قالبًا كاملًا في الزوجيّ (٠٫١٨٦٦).
- `NOVELTY_IS_RECOMBINATION`: و٢ **ثبت**: من ٦٧٤٢ لفظًا جديدًا، ٥٩٣٣ عواملُها
  وجذرُها مشهودة (٠٫٨٨٠٠) — وكانت بعاملين ٠٫٥٠٨٦ فسقطت.
- `BLIND_PEEL`: و٣ **سقط**: التقشيرُ الأعمى استردّ ٤٩١٩ من ٦٧٤٢ (٠٫٧٢٩٦). فسقط معه:
  «أنّ التقشيرَ بالعوامل الثلاثة يعمّم بلا حدودٍ من خارج الرسم».
  وتشخيصًا بعد التشغيل: في الجذور الصحيحة أصاب ٣٦٢٤ وأخطأ ٣٠٦ (٠٫٩٢)، وفي
  المعتلّة والمهموزة أصاب ١٢٩٥ وأخطأ ١٥١٧ (٠٫٤٦): **فالساقطُ الإعلال** — حرفُ
  العلّة يُحذف أو يُقلب فلا تحمله خانة.
- `WAZN_IS_BAB`: و٤ **ثبت**: الوزنُ وحدَه يعيّن بابَ الفعل في ٨١٨٠ من ٨٣٤٧ (٠٫٩٨٠٠).

وتشخيصُ غير المركَّب (٨٠٩): جذرٌ جديد ٣٨٩، وزنٌ جديد ٣٢٤، لاحقةٌ جديدة ٥٨، وزنٌ
وجذر ٣٠، سابقة ٦، وزنٌ ولاحقة ٢.
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
from test_wazn_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_wazn.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

FOUND = {
    "observations": 45_275,
    "aligned": 44_891,
    "consistent": 44_891,
    "prefixes": 54,
    "suffixes": 242,
    "roundtrip": 44_891,
    "wazns": 1_008,
    "whole_templates": 5_401,
    "novel": 6_742,
    "covered": 5_933,
    "peeled_right": 4_919,
    "verbs_odd_seen": 8_347,
    "verbs_odd": 8_472,
    "vf_right": 8_180,
}
SHARES = {"و١": "0.1866", "و٢": "0.8800", "و٣": "0.7296", "و٤": "0.9800"}
BEFORE = "0.5086"
PEEL_BY_ROOT = {
    "صحيح أصاب": 3_624,
    "صحيح أخطأ": 306,
    "معتل أصاب": 1_295,
    "معتل أخطأ": 1_517,
}
PEEL_SHARES = {"صحيح": "0.92", "معتل": "0.46"}
UNCOVERED = {
    "جذر": 389,
    "وزن": 324,
    "لاحقة": 58,
    "وزن وجذر": 30,
    "سابقة": 6,
    "وزن ولاحقة": 2,
}
UNCOVERED_TOTAL = 809
QUOTED_FALLEN = {"و٣": "أنّ التقشيرَ بالعوامل الثلاثة يعمّم بلا حدودٍ من خارج الرسم"}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_wazn", READER)
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
    assert DIGEST.startswith("66687b35")


def test_the_counts_are_as_recorded() -> None:
    """الأعدادُ كما رُويت، والتشخيصُ يجمع إليها."""

    assert _census() == FOUND
    assert f"{FOUND['wazns'] / FOUND['whole_templates']:.4f}" == SHARES["و١"]
    assert f"{FOUND['covered'] / FOUND['novel']:.4f}" == SHARES["و٢"]
    assert f"{FOUND['peeled_right'] / FOUND['novel']:.4f}" == SHARES["و٣"]
    assert f"{FOUND['vf_right'] / FOUND['verbs_odd_seen']:.4f}" == SHARES["و٤"]
    assert f"{3_480 / 6_842:.4f}" == BEFORE
    assert sum(PEEL_BY_ROOT.values()) == FOUND["novel"]
    right = PEEL_BY_ROOT["صحيح أصاب"] + PEEL_BY_ROOT["معتل أصاب"]
    assert right == FOUND["peeled_right"]
    sound = PEEL_BY_ROOT["صحيح أصاب"] / (
        PEEL_BY_ROOT["صحيح أصاب"] + PEEL_BY_ROOT["صحيح أخطأ"]
    )
    weak = PEEL_BY_ROOT["معتل أصاب"] / (
        PEEL_BY_ROOT["معتل أصاب"] + PEEL_BY_ROOT["معتل أخطأ"]
    )
    assert f"{sound:.2f}" == PEEL_SHARES["صحيح"]
    assert f"{weak:.2f}" == PEEL_SHARES["معتل"]
    left = FOUND["novel"] - FOUND["covered"]
    assert sum(UNCOVERED.values()) == UNCOVERED_TOTAL == left


def test_the_verdicts() -> None:
    """و٠ وو١ وو٢ وو٤ ثبتت، وو٣ سقط."""

    assert _one("و٠").verdict(Fraction(44_891, 44_891)) is Verdict.MET
    assert _one("و١").verdict(Fraction(1_008, 5_401)) is Verdict.MET
    assert _one("و٢").verdict(Fraction(5_933, 6_742)) is Verdict.MET
    assert _one("و٣").verdict(Fraction(4_919, 6_742)) is Verdict.FALSIFIED
    assert _one("و٤").verdict(Fraction(8_180, 8_347)) is Verdict.MET
    assert QUOTED_FALLEN["و٣"] in _one("و٣").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("و٠",)
"""و٠ مرّ بالإنشاء: البناءُ عكسُ التفكيك تعريفًا، فلا تعليلَ لغويَّ يؤيّده."""
