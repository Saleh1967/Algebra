"""شُغِّل ختمُ `149af813…`: **القبولُ بالبتّ التالي يتناقص كلّما صعدت الطبقة؛ ثبت
اثنان وسقط ثلاثة**.

المتعلِّمُ يرى البتّاتِ وحدها (سبعٌ للوحدة، والمصحفُ تيّارٌ واحدٌ بلا فراغٍ ولا وقفٍ
ولا آية)،
ويُمتحن على الآيات الفرديّة، والحدودُ المرصودة من الرسم وحده. وF1 بالبتّ التالي وحده
(k = ١، صعودًا):

| الطبقة | الحرفُ أوّلًا | الحالُ أوّلًا |
|---|---|---|
| الوحدة | ٠٫٩٥٠٩ | ٠٫٩٤٨٨ |
| المقطع | ٠٫٨٦٨٩ | ٠٫٩١١٣ |
| الكلمة | ٠٫٨٥٧٧ | ٠٫٨٥٢٣ |
| الوقف | ٠٫٤٤٨٠ | ٠٫٤٨٦٧ |
| الآية | ٠٫٥٥٦٦ | ٠٫٦٠٨٥ |

- `THE_UNIT`: ب١ **سقط**: حدُّ الوحدة ٠٫٩٥٠٩ لا ٠٫٩٩. فسقط معه: «أنّ حدَّ الوحدة
  يُكتشف حرًّا
ويُقبَل بالبتّ التالي وحده» — نحوُ واحدٍ من عشرين موضعًا لا تُعرف فيه مرحلةُ السبعة
  من ٢١ بتًّا.
- `STATE_FIRST`: ب٢ **سقط على الحدّ**: المقطعُ ببتّتين والحالُ أوّلًا ٠٫٩٣٩٧ لا
  ٠٫٩٥. فسقط معه:
«أنّ تقديمَ الحال يجعل المقطعَ مقبولًا ببتّتين». **والاتّجاهُ صدق**: الحالُ أوّلًا
  أبكرُ قبولًا
  (٠٫٩١١٣ مقابل ٠٫٨٦٨٩ ببتٍّ واحد).
- `LETTER_FIRST`: ب٣ **ثبت**: المقطعُ ببتّتين والحرفُ أوّلًا ٠٫٨٨٣٩.
- `THE_WORD`: ب٤ **سقط**: حدُّ الكلمة بالبتّ التالي وحده ٠٫٨٥٢٣، فوق ما توقّعتُ.
  فسقط معه:
«أنّ حدَّ الكلمة لا يُقبَل بالبتّ التالي وحده» — فالكلمةُ تكاد تُغلق نفسَها من
  ماضيها.
- `ONE_UNIT_AHEAD`: ب٥ **ثبت**: استشرافُ وحدةٍ كاملة يزيد الكلمةَ ٠٫٠٥٧١ (إلى ٠٫٩٠٩٣).

**والعكسُ** (رصدٌ لا حكم): المقطعُ يُقبَل من آخره أيسر (٠٫٩٣٥٦ بلا استشراف)،
والكلمةُ والآيةُ
من أوّلها أيسر (الآيةُ صعودًا ٠٫٥٤٥٢ بلا استشراف، وعكسًا ٠٫٣٠٣٨): الفاصلةُ تُغلق
الآيةَ من ماضيها.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_bit_ascent_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_bit_ascent.py"

pytestmark = requires_corpus

MEASURED = {
    "ب١": Fraction(341_752, 359_381),
    "ب٢": Fraction(212_318, 225_949),
    "ب٣": Fraction(198_676, 224_769),
    "ب٤": Fraction(32_199, 37_780),
    "الكلمة ٧": Fraction(69_128, 76_021),
}
SHARES = {
    "ب١": "0.9509",
    "ب٢": "0.9397",
    "ب٣": "0.8839",
    "ب٤": "0.8523",
    "ب٥": "0.0571",
}
TABLE_K1 = {
    ("الحرف أوّلًا", "صعود"): ("0.9509", "0.8689", "0.8577", "0.4480", "0.5566"),
    ("الحال أوّلًا", "صعود"): ("0.9488", "0.9113", "0.8523", "0.4867", "0.6085"),
}
REVERSE = {"مقطع عكس ٠": "0.9356", "آية صعود ٠": "0.5452", "آية عكس ٠": "0.3038"}
WORD_AHEAD = "0.9093"
QUOTED_FALLEN = {
    "ب١": "أنّ حدَّ الوحدة يُكتشف حرًّا ويُقبَل بالبتّ التالي وحده",
    "ب٢": "أنّ تقديمَ الحال يجعل المقطعَ مقبولًا ببتّتين",
    "ب٤": "أنّ حدَّ الكلمة لا يُقبَل بالبتّ التالي وحده",
}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_bit_ascent", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _table() -> dict[tuple[str, str, int], list[Fraction]]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().census(text)  # type: ignore[no-any-return]


def _one(name: str):  # type: ignore[no-untyped-def]
    return next(one for one in PREDICTIONS if one.identifier == name)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("149af813")


def test_the_measurements_are_as_recorded() -> None:
    """الجدولُ كما رُوي."""

    table = _table()
    lf, sf = "الحرف أوّلًا", "الحال أوّلًا"
    assert table[(lf, "صعود", 1)][0] == MEASURED["ب١"]
    assert table[(sf, "صعود", 2)][1] == MEASURED["ب٢"]
    assert table[(lf, "صعود", 2)][1] == MEASURED["ب٣"]
    assert table[(sf, "صعود", 1)][2] == MEASURED["ب٤"]
    assert table[(sf, "صعود", 7)][2] == MEASURED["الكلمة ٧"]
    for (order, direction), row in TABLE_K1.items():
        assert tuple(f"{float(x):.4f}" for x in table[(order, direction, 1)]) == row
    assert f"{float(table[(lf, 'عكس', 0)][1]):.4f}" == REVERSE["مقطع عكس ٠"]
    assert f"{float(table[(lf, 'صعود', 0)][4]):.4f}" == REVERSE["آية صعود ٠"]
    assert f"{float(table[(lf, 'عكس', 0)][4]):.4f}" == REVERSE["آية عكس ٠"]
    assert f"{float(MEASURED['الكلمة ٧']):.4f}" == WORD_AHEAD
    for name in ("ب١", "ب٢", "ب٣", "ب٤"):
        assert f"{float(MEASURED[name]):.4f}" == SHARES[name]
    gain = MEASURED["الكلمة ٧"] - MEASURED["ب٤"]
    assert f"{float(gain):.4f}" == SHARES["ب٥"]


def test_the_verdicts() -> None:
    """ب٣ وب٥ ثبتا، وب١ وب٢ وب٤ سقطت."""

    assert _one("ب١").verdict(Fraction(341_752, 359_381)) is Verdict.FALSIFIED
    assert _one("ب٢").verdict(Fraction(212_318, 225_949)) is Verdict.FALSIFIED
    assert _one("ب٣").verdict(Fraction(198_676, 224_769)) is Verdict.MET
    assert _one("ب٤").verdict(Fraction(32_199, 37_780)) is Verdict.FALSIFIED
    gain = Fraction(69_128, 76_021) - Fraction(32_199, 37_780)
    assert _one("ب٥").verdict(gain) is Verdict.MET
    assert QUOTED_FALLEN["ب١"] in _one("ب١").falsifies
    assert QUOTED_FALLEN["ب٢"] in _one("ب٢").falsifies
    assert QUOTED_FALLEN["ب٤"] in _one("ب٤").falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شيء: ب٣ وب٥ مرّا بتعليلهما (تأخيرُ الحال يؤخّر المقطع، والاستشرافُ يُعين الكلمة)."""
