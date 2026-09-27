"""شُغِّل ختمُ `aaf77e3d…`: **واحدٌ من ثلاثة — والذي صمد لم يُؤيَّد تعليلُه**.

`THE_CEILING_HOLDS`: س١ **صمد تمامًا**: الألفاظُ ذات سبعة أحرفٍ فأكثر **٦٬٩٩١**،
ولا يتجاوز غيرُ الزائد فيها خمسةً في واحدٍ منها.

`BUT_THE_LETTERS_ALREADY_GIVE_IT`: س٢ **سقط**: السحبُ المستقلّ بنسبة م وأ في
حروف المصحف (٠٫٢٨٠٢) يعطي وحده ٠٫٩٩٤٥، فالزيادةُ ٠٫٠٠٥٥ لا عُشر. فسقط معه ما
قال نصُّه: «فالخمسةُ سقفٌ يعطيه تواترُ الحروف لا حدُّ الجذر». **وهذا عيبٌ في
تصميمي**: كان المتوقَّعُ قابلًا للحساب من أعداد الوحدات قبل الختم، ولم أحسبه،
فختمتُ سقفًا يكاد يلزم من النسبة وحدها.

`THE_INITIAL_STATE_BARELY_MOVES`: س٣ **سقط**: أ في الحروف ٠٫١٨٧٥، وحرفًا أوّل
٠٫١٦٨٤، والفرقُ ٠٫٠١٩١ لا نصفُ عُشر. فسقط معه: «فالسوابقُ لا تحكم الحالَ
الابتدائيّة» — بقدر ما قاسه هذا الشرطُ على مجموعة أ.

`WHERE_THE_PREFIXES_ACTUALLY_SHOW` — **تشخيصٌ بعد التشغيل، لا حكم**: الحالُ
الابتدائيّة تتحرّك في **م** لا في أ: م في الحروف ٠٫٠٩٢٧ وحرفًا أوّل ٠٫١٤٥٢. وز
تقلّ أوّلًا (٠٫٧١٩٨ ← ٠٫٦٨٦٣) خلافَ ما قدّرتُ. ومصفوفةُ ماركوف داخلَ اللفظ:

- **من م إلى م** ٠٫٠٥٩٦ ونسبةُ م ٠٫٠٩٢٧: الملتصقاتُ **يتدافع** بعضُها عن بعض.
- **من أ إلى أ** ٠٫٢٣٠٤ ونسبةُ أ ٠٫١٨٧٥: الأصليُّ وحده **يتجاور**.
- **من م إلى أ** ٠٫٢١٩٣: بعد الملتصق يكثر الأصليّ — السابقةُ ثمّ الجذر.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_zawaid_letters_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_zawaid_letters.py"

pytestmark = requires_corpus

WORDS = 78_245
LETTERS = 332_837
NON_ZAWAID = 0.2802
LONG_WORDS = 6_991
BINOMIAL = 0.9945
GAP = 0.0055
RADICAL_SHARE = 0.1875
RADICAL_FIRST = 0.1684
FIRST_GAP = 0.0191
INITIAL = {"ز": 0.6863, "م": 0.1452, "أ": 0.1684}
OVERALL = {"ز": 0.7198, "م": 0.0927, "أ": 0.1875}
ROWS = {
    "ز": {"ز": 0.7488, "م": 0.0734, "أ": 0.1778},
    "م": {"ز": 0.721, "م": 0.0596, "أ": 0.2193},
    "أ": {"ز": 0.6749, "م": 0.0947, "أ": 0.2304},
}
QUOTED_FALLEN = {
    "س٢": "سقفٌ يعطيه تواترُ الحروف لا حدُّ الجذر",
    "س٣": "فالسوابقُ لا تحكم الحالَ الابتدائيّة",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_zawaid_letters", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _words() -> list[str]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().letters(text)  # type: ignore[no-any-return]


@cache
def _measures() -> dict[str, float]:
    return _reader().measures(_words())  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("aaf77e3d")


def test_the_ceiling_holds_in_every_long_word() -> None:
    """س١ صمد: ٦٬٩٩١ من ٦٬٩٩١."""

    m = _measures()
    assert (m["words"], m["letters"]) == (WORDS, LETTERS)
    assert (m["under"], m["long"]) == (LONG_WORDS, LONG_WORDS)
    first = next(one for one in PREDICTIONS if one.identifier == "س١")
    assert first.verdict(Fraction(int(m["under"]), int(m["long"]))) is Verdict.MET


def test_but_the_letter_shares_already_give_the_ceiling() -> None:
    """س٢ سقط: ذو الحدّين ٠٫٩٩٤٥ والزيادة ٠٫٠٠٥٥."""

    m = _measures()
    assert abs(m["p"] - NON_ZAWAID) < 5e-5
    assert abs(m["expected"] - BINOMIAL) < 5e-5
    gap = Fraction(m["share"]).limit_denominator(10**9) - Fraction(
        m["expected"]
    ).limit_denominator(10**9)
    assert abs(float(gap) - GAP) < 5e-5
    second = next(one for one in PREDICTIONS if one.identifier == "س٢")
    assert second.verdict(gap) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["س٢"] in second.falsifies


def test_the_initial_state_barely_moves_for_the_radical_only_group() -> None:
    """س٣ سقط: ٠٫١٨٧٥ في الحروف و٠٫١٦٨٤ أوّلًا."""

    m = _measures()
    assert abs(m["radical_share"] - RADICAL_SHARE) < 5e-5
    assert abs(m["first_share"] - RADICAL_FIRST) < 5e-5
    gap = Fraction(int(m["radical_first"]), int(m["starts"]))
    gap = Fraction(m["radical_share"]).limit_denominator(10**9) - gap
    assert abs(float(gap) - FIRST_GAP) < 5e-5
    third = next(one for one in PREDICTIONS if one.identifier == "س٣")
    assert third.verdict(gap) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["س٣"] in third.falsifies


def test_the_markov_matrix_after_the_run() -> None:
    """تشخيصًا: الحالُ الابتدائيّة والانتقالاتُ بين المجموعات."""

    reader = _reader()
    first, moves = reader.markov(_words())
    words = len(_words())
    for group, value in INITIAL.items():
        assert abs(first[group] / words - value) < 5e-5
    for group, row in ROWS.items():
        out = sum(moves[(group, other)] for other in reader.GROUPS)
        for other, value in row.items():
            assert abs(moves[(group, other)] / out - value) < 5e-5
    letters = "".join(_words())
    for group, value in OVERALL.items():
        assert abs(letters.count(group) / len(letters) - value) < 5e-5


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("س١",)
"""س١ مرّ، وتعليلُه «السقفُ حدُّ الجذر» لم يُؤيَّد: سقط س٢ الذي يقيسه، فالسقفُ
يكاد يلزم من نسبة الحروف وحدها."""
