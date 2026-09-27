"""شُغِّل ختمُ `6be35fd8…`: **ثلاثةٌ من ثلاثة — ثابتُ الجرّ يظهر في المستوى الثالث**.

`THE_CONSTANT_HOLDS_AT_A_DISTANCE`: السلسلةُ (جارٌّ، مجرورٌ آخرُه كسرة، ثمّ لفظٌ
يبدأ بـ«ال» أو «وَال») كسرتُها **٤١٨ من ٥٣١** (٠٫٧٨٧٢)، وPMI **١٫٥٨٠٦** بتّ.
ث١ **صمد**: البعدُ عن ١٫٦٣٦٥ هو ٠٫٠٥٥٩. ث٢ **صمد**: كثافةُ الربح ٠٫١٣٧٩ موجبة.
ث٣ **صمد**: الضابطُ بعد ضمّة ٠٫٢١١٨، والفرقُ ٠٫٥٧٥٤.

فالثابتُ في ثلاثة مستويات: ١٫٦٢٤ بين لفظين متجاورين، و١٫٦٤٩ داخلَ اللفظ،
و١٫٥٨١ عن بُعد لفظ.

`WHAT_DID_NOT_FOLLOW_IS_NAMED` — **تشخيصٌ بعد التشغيل**: الضمّاتُ **٢٨**،
أكثرُها **ابتداءُ جملة** («وَاللَّهُ» ١٤). والفتحاتُ **٨٥**: المبنيُّ
(«الَّذِينَ» ١٢)، وجمعُ المذكّر المجرورُ بالياء («الْعَالَمِينَ» ٩)، والمفعولُ
في جملةٍ جديدة («الْكَذِبَ» ١٠). **وعيبٌ في التعريف**: «آلِهَةً» ٤ دخلت لأنّ
طيَّ الهمزة جعل أوّلَها «ال».
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_fractal_third_scale_seal import (
    BASE_KASRA,
    CONSTANT,
    DIGEST,
    ORACLE,
    PREDICTIONS,
)

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_fractal_third_scale.py"

pytestmark = requires_corpus

KASRA, SHOWN = 418, 531
SHARE, PMI = 0.7872, 1.5806
DISTANCE, DENSITY = 0.0559, 0.1379
CONTROL, GAP = 0.2118, 0.5754
SCALES = (1.624, 1.649, 1.581)
DAMMAS, FATHAS = 28, 85
WALLAHU = 14
ALLADHINA, ALAMINA, KADHIBA, ALIHATAN = 12, 9, 10, 4


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_fractal_third_scale", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _text() -> str:
    return CORPUS.read_text(encoding="utf-8").rstrip("\n")


@cache
def _census() -> dict[str, Counter[str]]:
    return _reader().census(_text())  # type: ignore[no-any-return]


def _pmi(kasra: int, shown: int) -> float:
    return math.log2(Fraction(kasra, shown) / BASE_KASRA)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("6be35fd8")


def test_the_constant_holds_at_a_distance() -> None:
    """ث١ صمد: PMI ١٫٥٨٠٦ وبعدُه عن ١٫٦٣٦٥ هو ٠٫٠٥٥٩."""

    reader = _reader()
    assert reader.share(_census()["سلسلة"]) == (KASRA, SHOWN)
    assert abs(KASRA / SHOWN - SHARE) < 5e-5
    value = _pmi(KASRA, SHOWN)
    assert abs(value - PMI) < 5e-5
    distance = abs(Fraction(value) - CONSTANT)
    assert abs(float(distance) - DISTANCE) < 5e-5
    first = next(one for one in PREDICTIONS if one.identifier == "ث١")
    assert first.verdict(distance) is Verdict.MET
    assert max(SCALES) - min(SCALES) < 0.1


def test_the_greedy_gain_stays_positive() -> None:
    """ث٢ صمد: كثافةُ الربح ٠٫١٣٧٩."""

    density = Fraction(_pmi(KASRA, SHOWN) - math.log2(math.e))
    assert abs(float(density) - DENSITY) < 5e-5
    second = next(one for one in PREDICTIONS if one.identifier == "ث٢")
    assert second.verdict(density) is Verdict.MET


def test_and_the_chain_not_the_article_carries_it() -> None:
    """ث٣ صمد: الضابطُ ٠٫٢١١٨ والفرقُ ٠٫٥٧٥٤."""

    reader = _reader()
    other, total = reader.share(_census()["ضابط"])
    assert abs(other / total - CONTROL) < 5e-5
    gap = Fraction(KASRA, SHOWN) - Fraction(other, total)
    assert abs(float(gap) - GAP) < 5e-5
    third = next(one for one in PREDICTIONS if one.identifier == "ث٣")
    assert third.verdict(gap) is Verdict.MET


def test_what_did_not_follow_is_named_after_the_run() -> None:
    """تشخيصًا: ٢٨ ضمّة و٨٥ فتحة، بأبوابها — ومعها عيبُ «آلِهَةً»."""

    counts = _census()["سلسلة"]
    assert (counts["ُ"], counts["َ"]) == (DAMMAS, FATHAS)
    reader = _reader()
    governed = reader._governed()
    peeler = governed._peeler()
    found: Counter[str] = Counter()
    for line in _text().split("\n"):
        tokens = line.replace(governed.MARKUP, " ").split()
        peeled = [peeler.peel(token) for token in tokens]
        finals = [governed.final_vowel(*one, peeler.STRUCTURE) for one in peeled]
        for i in range(1, len(tokens) - 1):
            if (
                finals[i] == governed.KASRA
                and governed.kind(*peeled[i - 1], peeler.STRUCTURE) == "جر"
                and reader.starts_with_al(*peeled[i + 1], peeler.STRUCTURE)
            ):
                skeleton = "".join(
                    letter
                    for (letter, _), extra in zip(*peeled[i + 1], strict=True)
                    if letter != peeler.STRUCTURE and extra.get("تنوين") != "ذيل"
                )
                found[(skeleton, finals[i + 1])] += 1
    assert found[("واللله", "ُ")] == WALLAHU
    assert found[("اللذين", "َ")] == ALLADHINA
    assert found[("العالمين", "َ")] == ALAMINA
    assert found[("الكذب", "َ")] == KADHIBA
    assert found[("الهه", "َ")] == ALIHATAN


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: وما خالف مسمًّى بأبوابه."""
