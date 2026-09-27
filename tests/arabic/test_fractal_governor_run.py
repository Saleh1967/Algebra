"""شُغِّل ختمُ `58e14ba9…`: **ثلاثةٌ من ثلاثة — العاملُ يعمل داخلَ اللفظ كما يعمل بينهما**.

`THE_ATTACHED_GOVERNOR_WORKS`: ف١ **صمد**: الكسرة في آخر اللفظ الذي أوّلُه
«بِال» أو «لِل» **٧٤٣ من ٩٠٠** (٠٫٨٢٥٦). **ولا ضمّةَ واحدة**.

`AT_THE_SAME_RATE_AS_ACROSS_WORDS`: ف٢ **صمد**: الفرقُ عن ٠٫٨١٠٩ (بين لفظين)
٠٫٠١٤٧ — أقلُّ من عُشرٍ بكثير.

`AND_NOT_BECAUSE_OF_ATTACHMENT`: ف٣ **صمد**: الضابطُ «وَال/فَال» كسرتُه
٠٫٣٢٤٢، والفرقُ ٠٫٥٠١٣.

`EVERY_FATHA_IS_NAMED` — **تشخيصٌ بعد التشغيل**: الفتحاتُ **١٥٧** كلُّها آخرُها
«ـينَ»: **٥٦** «الَّذِينَ» المبنيّ (لِلَّذِينَ ٥٠، بِالَّذِينَ ٦)، و**١٠١** جمعُ مذكّرٍ
مجرورٌ بالياء («لِلْكَافِرِينَ» ١٦، «لِلْمُتَّقِينَ» ١١). فما ظهرت حركتُه بعد
الجارّ الملتصق إمّا كسرةٌ وإمّا بابٌ مسمًّى — لا ثالثَ لهما.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_fractal_governor_seal import BETWEEN_WORDS, DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_fractal_governor.py"

pytestmark = requires_corpus

KASRA, SHOWN = 743, 900
SHARE = 0.8256
ACROSS = 0.8109
DISTANCE = 0.0147
CONTROL_SHARE = 0.3242
GAP = 0.5013
FATHAS = 157
ALLADHINA = 56
PLURALS = 101
LI_ALLADHINA, BI_ALLADHINA = 50, 6
LIL_KAFIRINA, LIL_MUTTAQINA = 16, 11


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_fractal_governor", READER)
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


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("58e14ba9")


def test_the_attached_governor_works() -> None:
    """ف١ صمد: ٧٤٣ من ٩٠٠، ولا ضمّة."""

    reader = _reader()
    counts = _census()["عامل"]
    assert reader.share(counts) == (KASRA, SHOWN)
    assert counts[reader.DAMMA] == 0
    first = next(one for one in PREDICTIONS if one.identifier == "ف١")
    assert abs(KASRA / SHOWN - SHARE) < 5e-5
    assert first.verdict(Fraction(KASRA, SHOWN)) is Verdict.MET


def test_at_the_same_rate_as_across_words() -> None:
    """ف٢ صمد: البعدُ عن ٠٫٨١٠٩ هو ٠٫٠١٤٧."""

    assert float(BETWEEN_WORDS) == ACROSS
    distance = abs(Fraction(KASRA, SHOWN) - BETWEEN_WORDS)
    assert abs(float(distance) - DISTANCE) < 5e-5
    second = next(one for one in PREDICTIONS if one.identifier == "ف٢")
    assert second.verdict(distance) is Verdict.MET


def test_and_not_because_of_attachment() -> None:
    """ف٣ صمد: الضابطُ ٠٫٣٢٤٢ والفرقُ ٠٫٥٠١٣."""

    reader = _reader()
    other, total = reader.share(_census()["ضابط"])
    assert abs(other / total - CONTROL_SHARE) < 5e-5
    gap = Fraction(KASRA, SHOWN) - Fraction(other, total)
    assert abs(float(gap) - GAP) < 5e-5
    third = next(one for one in PREDICTIONS if one.identifier == "ف٣")
    assert third.verdict(gap) is Verdict.MET


def test_every_fatha_after_the_attached_governor_is_named() -> None:
    """تشخيصًا: ١٥٧ فتحةً كلُّها «ـينَ» — ٥٦ «الَّذِينَ» و١٠١ جمعُ مذكّر."""

    reader = _reader()
    peeler = reader._peeler()
    found: Counter[str] = Counter()
    for line in _text().split("\n"):
        for token in line.replace(reader.MARKUP, " ").split():
            units, extras = peeler.peel(token)
            kept = [
                unit
                for unit, extra in zip(units, extras, strict=True)
                if unit[0] != peeler.STRUCTURE and extra.get("تنوين") != "ذيل"
            ]
            if reader.prefix(kept) == "عامل" and kept[-1][1] == reader.FATHA:
                found["".join(letter for letter, _ in kept)] += 1
    assert sum(found.values()) == FATHAS
    assert all(key.endswith("ين") for key in found)
    built = found["لللذين"] + found["باللذين"]
    assert (found["لللذين"], found["باللذين"]) == (LI_ALLADHINA, BI_ALLADHINA)
    assert (built, FATHAS - built) == (ALLADHINA, PLURALS)
    assert (found["للكافرين"], found["للمتتقين"]) == (LIL_KAFIRINA, LIL_MUTTAQINA)


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: والفتحاتُ كلُّها مسمّاة."""
