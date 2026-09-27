"""شُغِّل ختمُ `c35956ef…`: **ثلاثةٌ من ثلاثة — الحركةُ الأخيرة تتبع العامل**.

`AFTER_A_PREPOSITION_THE_KASRA`: ت١ **صمد**: الكسرة بعد حرف الجرّ المنفصل
**٢٬٦٢٨ من ٣٬٢٤١** (٠٫٨١٠٩). والتوزيعُ بلا عاملٍ كانت الكسرةُ فيه ربعَ الآخِر.

`AFTER_INNA_THE_FATHA`: ت٢ **صمد**: الفتحة بعد «إِنَّ» **٤٤٧ من ٤٧٠**
(٠٫٩٥١١).

`AND_THE_DISTRIBUTION_TURNS`: ت٣ **صمد**: الفرقُ في نصيب الكسرة ٠٫٧٨١١.

`THE_EXCEPTIONS_ARE_NAMED_BY_THE_SAME_EXPLANATION` — **تشخيصٌ بعد التشغيل**:
ما خالف الغالبَ يسمّيه النحوُ نفسُه، لا يبقى منه صنفٌ بلا اسم:

- **المبنيّ**: بعد الجرّ ضمّةُ «قَبْلُ» ٥٨ و«حَيْثُ» ١١ و«بَعْدُ» ٤؛ وفتحةُ
  «الَّذِينَ» ٦١. وبعد «إِنَّ» كسرةُ «هَؤُلَاءِ» ٧.
- **الضميرُ المتّصل**: آخرُ اللفظ حركةُ الضمير لا حركةُ الإعراب («رَّبِّكَ» ٢٣،
  و«ذَلِكَ» ٦٠، و«قُلُوبِهِمُ»).
- **الإعرابُ النائب**: جمعُ المذكّر مجرورٌ بالياء فآخرُه نونٌ مفتوحة
  («الْمُؤْمِنِينَ» ٢٣)؛ والممنوعُ من الصرف مجرورٌ بالفتحة («فِرْعَوْنَ» ١٥)؛
  وجمعُ المؤنّث منصوبٌ بالكسرة («الْحَسَنَاتِ»).
- **تقديمُ الخبر**: «إِنَّ لِلَّهِ» — الكسرةُ للجارّ لا لاسم «إِنَّ».

**والعيبُ المُعلَن قبل العدّ قائم**: من فتحات ت٢ **٨٤** فتحةُ «الَّذِينَ»
المبنيّ، لا نصبٌ ظاهر. فالسطحُ وحده لا يفرّق النصبَ من البناء على الفتح.
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
from test_governed_vowel_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_governed_vowel.py"

pytestmark = requires_corpus

KASRA_AFTER_PREPOSITION, SHOWN_AFTER_PREPOSITION = 2_628, 3_241
FATHA_AFTER_INNA, SHOWN_AFTER_INNA = 447, 470
KASRA_AFTER_INNA = 14
SHARES = (0.8109, 0.9511, 0.7811)
NAMED_AFTER_PREPOSITION = {"قَبْلُ": 58, "حَيْثُ": 11, "بَعْدُ": 4}
ALLADHINA_AFTER_PREPOSITION = 61
DHALIKA_AFTER_PREPOSITION = 60
RABBIKA_AFTER_PREPOSITION = 23
MUMININA_AFTER_PREPOSITION = 23
PHARAOH_AFTER_PREPOSITION = 15
HA_ULA_I_AFTER_INNA = 7
ALLADHINA_AFTER_INNA = 84


def _canonical(token: str) -> str:
    """الشدّةُ قبل الحركة في كلّ حرف — فيُطابَق المكتوبُ هنا بما في المصحف."""

    out: list[str] = []
    marks: list[str] = []
    for one in token:
        if "\u064b" <= one <= "\u0652":
            marks.append(one)
            continue
        out.extend(sorted(marks, key=lambda mark: mark != "\u0651"))
        marks = []
        out.append(one)
    out.extend(sorted(marks, key=lambda mark: mark != "\u0651"))
    return "".join(out)


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_governed_vowel", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _census() -> dict[str, Counter[str]]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().census(text)  # type: ignore[no-any-return]


@cache
def _following() -> dict[tuple[str, str], Counter[str]]:
    reader = _reader()
    peeler = reader._peeler()
    found: dict[tuple[str, str], Counter[str]] = {}
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    for line in text.split("\n"):
        tokens = line.replace(reader.MARKUP, " ").split()
        peeled = [peeler.peel(token) for token in tokens]
        for index in range(len(tokens) - 1):
            governor = reader.kind(*peeled[index], peeler.STRUCTURE)
            if governor is None:
                continue
            vowel = reader.final_vowel(*peeled[index + 1], peeler.STRUCTURE)
            if vowel is None:
                continue
            found.setdefault((governor, vowel), Counter())[
                _canonical(tokens[index + 1])
            ] += 1
    return found


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("c35956ef")


def test_after_a_preposition_the_kasra_holds() -> None:
    """ت١ صمد: ٢٬٦٢٨ من ٣٬٢٤١."""

    reader = _reader()
    kasra, shown = reader.share(_census()["جر"], reader.KASRA)
    assert (kasra, shown) == (KASRA_AFTER_PREPOSITION, SHOWN_AFTER_PREPOSITION)
    first = next(one for one in PREDICTIONS if one.identifier == "ت١")
    assert abs(kasra / shown - SHARES[0]) < 5e-5
    assert first.verdict(Fraction(kasra, shown)) is Verdict.MET


def test_after_inna_the_fatha_holds() -> None:
    """ت٢ صمد: ٤٤٧ من ٤٧٠."""

    reader = _reader()
    fatha, shown = reader.share(_census()["إنّ"], reader.FATHA)
    assert (fatha, shown) == (FATHA_AFTER_INNA, SHOWN_AFTER_INNA)
    second = next(one for one in PREDICTIONS if one.identifier == "ت٢")
    assert abs(fatha / shown - SHARES[1]) < 5e-5
    assert second.verdict(Fraction(fatha, shown)) is Verdict.MET


def test_the_distribution_turns_with_the_governor() -> None:
    """ت٣ صمد: الفرقُ ٠٫٧٨١١."""

    reader = _reader()
    kasra, shown = reader.share(_census()["جر"], reader.KASRA)
    other, after = reader.share(_census()["إنّ"], reader.KASRA)
    assert other == KASRA_AFTER_INNA
    gap = Fraction(kasra, shown) - Fraction(other, after)
    third = next(one for one in PREDICTIONS if one.identifier == "ت٣")
    assert abs(float(gap) - SHARES[2]) < 5e-5
    assert third.verdict(gap) is Verdict.MET


def test_the_exceptions_are_named_after_the_run() -> None:
    """تشخيصًا: المبنيّ والضمير المتّصل والإعراب النائب — بأسمائها وأعدادها."""

    found = _following()
    damma = found[("جر", "ُ")]
    assert {
        key: damma[key] for key in NAMED_AFTER_PREPOSITION
    } == NAMED_AFTER_PREPOSITION
    fatha = found[("جر", "َ")]
    assert fatha[_canonical("الَّذِينَ")] == ALLADHINA_AFTER_PREPOSITION
    assert fatha[_canonical("ذَلِكَ")] == DHALIKA_AFTER_PREPOSITION
    assert fatha[_canonical("رَّبِّكَ")] == RABBIKA_AFTER_PREPOSITION
    assert fatha[_canonical("الْمُؤْمِنِينَ")] == MUMININA_AFTER_PREPOSITION
    assert fatha[_canonical("فِرْعَوْنَ")] == PHARAOH_AFTER_PREPOSITION
    assert found[("إنّ", "ِ")][_canonical("هَؤُلَاءِ")] == HA_ULA_I_AFTER_INNA
    assert found[("إنّ", "َ")][_canonical("الَّذِينَ")] == ALLADHINA_AFTER_INNA


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء، مع قيدٍ على ت٢.

ت١ وت٣ مرّا وتعليلُهما «العاملُ يقرّر الحركة الأخيرة» مؤيَّدٌ بأنّ ما خالف
الغالبَ مسمًّى كلُّه. وت٢ مرّ، وتعليلُه مؤيَّدٌ **دون** فتحات «الَّذِينَ»، وهي
بناءٌ لا نصب — والعيبُ مُعلَنٌ في الختم قبل العدّ.
"""
