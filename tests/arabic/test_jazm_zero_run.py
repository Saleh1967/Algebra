"""شُغِّل ختمُ `0dd2643d…`: **سقطت الشروطُ الثلاثة** — والطردُ بعشرين موضعًا بأعيانها.

`THE_FORWARD_FALLS`: ج١ **سقط**: من ٦١١ مضارعًا بعد الجوازم الأربعة، ٢٠ لا تفسّرها
علاماتُ الجزم الموقَّعة. فسقط معه: «فالجزمُ لا يستمرّ ١٠٠٪ بهذا الجدول وهذه الأداة».
وعملت العلامات: السكون ٤٦٣، وحذفُ حرف العلّة ٧٣، والتقاءُ الساكنين ٤٠، و«يَكُ» ١٠،
والمضعَّف ٥.

`THE_TWENTY_SORTED` — **تشخيصٌ بعد التشغيل، لا حكم** (المواضعُ في `FORWARD`):
- **٨ — عيبُ الأداة في حذف حرف العلّة**: الهيكلُ بحرف العلّة لم يرد مجرّدًا بل بضمير
  («تَنتَهِ» ٣، «يَنتَهِ»، «يَكْفِ»، «يَأْنِ»، «نَنْهَكَ»، «تَرَنِ»).
- **٥ — عيبُ الأداة في لام الأمر**: لامٌ مكسورةٌ أوّلَ المقطع هي لامُ التعليل الناصبة؛
  علامةُ الوقف تقع داخل الكلام («لِيَقْطَعَ»، «لِتُنذِرَ»).
- **٤ — عيبُ قسم الكلمة**: ماضٍ على «أَفْعَلَ» أو بـ«سَـ» عُدّ مضارعًا بعد «إِنْ»
  («أَصْبَحَ»، «أَمْسَكَ»، «أَتْمَمْتَ»، «سَأَلْتُكَ»).
- **٢ — بابٌ في الجدول سقط من نصّ الختم**: نونُ النسوة («يَحِضْنَ»، «وَلْيَضْرِبْنَ»).
- **١ — عيبُ الأداة**: «لِّمَا» بشدّة الإدغام عُدّت «لَمَّا».
فلا موضعَ واحدٌ منها مضارعٌ مجزومٌ بجازمٍ ظاهرٍ بلا علامة جزم.

`THE_REVERSE_FALLS`: ج٢ **سقط**: ١١٦٠ «مضارعًا» ساكنَ الآخر بلا سببٍ في مقطعه. فسقط
معه: «أو قسمُ الكلمة في الأداة خاطئ». وتشخيصًا: ٨٠٨ آخرُها حرفُ مدٍّ عارٍ عُدّ سكونًا
(«أَرْسَلْنَا»، «تُتْلَى»، «يَكُونُوا» المنصوبة) — أخذتُ «السكون» بلفظ الختم حالَ الوحدة؛
و٢٨٥ أوّلُها همزة (ماضٍ على أَفْعَلَ، أو همزةُ استفهام: «أَلَمْ»، «أَفَلَا»)؛ و٦٧ غيرُ ذلك،
منها جزمٌ حقيقيٌّ سببُه «إِلَّا» الشرطيّة (إنْ + لا) وليست في قائمة الأسباب، أو أمرٌ من
«تَفَعَّلَ» («تَوَكَّلْ»).

`THE_CONTROL_FALLS`: ج٣ **سقط**: من ٦١١ مضارعًا مسحوبًا لا جازمَ قبله لم يُفسَّر إلّا
٢٢٣ (٠٫٣٦٥٠)، دون النصف. فسقط معه: «فهي واسعةٌ تفسّر كلَّ شيء». وتشخيصًا: السكونُ بلفظ
الختم (حروفُ المدّ العارية) فسّر ٢٦٥، والتقاءُ الساكنين ٥٥، وحذفُ حرف العلّة ٤٦، والمضعَّف ٢٢.

**فالدرس**: الجزمُ بعواملِه الظاهرة لم يُخطئ في موضعٍ واحدٍ لغةً؛ والذي سقط الأداةُ:
«السكونُ» يجب أن يُفرَّق فيه المكتوبُ من العاري، وقسمُ الكلمة يحتاج الماضي، وحذفُ حرف
العلّة يحتاج الجذعَ قبل الضمير. وذلك كلُّه لختمٍ جديد، لا لهذا.
"""

from __future__ import annotations

import importlib.util
import sys
import unicodedata
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_jazm_zero_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_jazm_zero.py"

pytestmark = requires_corpus

GOVERNED = 611
FIRED = {"سكون": 463, "حذف حرف العلّة": 73, "التقاء الساكنين": 40, "يك": 10, "مضعَّف": 5}
BY_TOOL = {"لم": 8, "لام الأمر": 6, "إن": 5, "لمّا": 1}
SORTED = {"حرف العلة": 8, "لام التعليل": 5, "ماض": 4, "نون النسوة": 2, "لما": 1}
REVERSE = 1_160
REVERSE_SORTED = {"مد عار": 808, "همزة أولا": 285, "غير ذلك": 67}
CONTROL = Fraction(223, 611)
CONTROL_SHARE = "0.3650"
POOL = 11_644
CONTROL_BY_CLASS = {
    "سكون": 265,
    None: 223,
    "التقاء الساكنين": 55,
    "حذف حرف العلّة": 46,
    "مضعَّف": 22,
}
QUOTED_FALLEN = {
    "ج١": "فالجزمُ لا يستمرّ ١٠٠٪ بهذا الجدول وهذه الأداة",
    "ج٢": "أو قسمُ الكلمة في الأداة خاطئ",
    "ج٣": "فهي واسعةٌ تفسّر كلَّ شيء",
}
FORWARD = (
    (420, 0, "لام الأمر", "لِيَقْطَعَ"),
    (1696, 42, "لمّا", "يَشَاءُ"),
    (1872, 2, "لم", "نَنْهَكَ"),
    (1940, 0, "لام الأمر", "لِيُبَيِّنَ"),
    (2179, 13, "إن", "تَرَنِ"),
    (2216, 2, "إن", "سَأَلْتُكَ"),
    (2296, 9, "لم", "تَنتَهِ"),
    (2371, 0, "لام الأمر", "لِنُرِيَكَ"),
    (2822, 14, "لام الأمر", "وَلْيَضْرِبْنَ"),
    (3048, 3, "لم", "تَنتَهِ"),
    (3099, 3, "لم", "تَنتَهِ"),
    (3279, 14, "إن", "أَتْمَمْتَ"),
    (3711, 0, "لام الأمر", "لِتُنذِرَ"),
    (4271, 12, "لم", "يَكْفِ"),
    (4708, 0, "لام الأمر", "لِنُرْسِلَ"),
    (5091, 1, "لم", "يَأْنِ"),
    (5221, 13, "لم", "يَحِضْنَ"),
    (5262, 5, "إن", "أَمْسَكَ"),
    (5271, 3, "إن", "أَصْبَحَ"),
    (6121, 3, "لم", "يَنتَهِ"),
)
"""المواضعُ العشرون بأعيانها: (السطر، رقمُ اللفظ، الجازم، اللفظ)."""


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_jazm_zero", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _census() -> dict[str, object]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().census(text)  # type: ignore[no-any-return]


def _canonical(row: tuple) -> tuple:  # type: ignore[type-arg]
    """ترتيبُ الشدّة والحركة في البايتات يختلف بين المصحف وهذا الملفّ."""

    return tuple(
        unicodedata.normalize("NFD", one) if isinstance(one, str) else one
        for one in row
    )


def _one(name: str):  # type: ignore[no-untyped-def]
    return next(one for one in PREDICTIONS if one.identifier == name)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("0dd2643d")


def test_the_forward_falls_at_twenty_named_positions() -> None:
    """ج١ سقط: ٢٠ موضعًا من ٦١١، كلٌّ بعينه."""

    found = _census()
    forward = found["forward"]
    assert isinstance(forward, list)
    assert tuple(_canonical(one) for one in forward) == tuple(
        _canonical(one) for one in FORWARD
    )
    assert found["governed"] == GOVERNED
    assert dict(found["fired"]) == FIRED  # type: ignore[call-overload]
    assert Counter(one[2] for one in forward) == BY_TOOL
    first = _one("ج١")
    assert first.verdict(Fraction(len(forward))) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج١"] in first.falsifies


def test_the_twenty_sort_into_five_named_classes() -> None:
    """تشخيصًا: ٨ + ٥ + ٤ + ٢ + ١ = ٢٠ — ولا مجزومَ بلا علامة."""

    def kind(tool: str, token: str) -> str:
        if token in ("يَحِضْنَ", "وَلْيَضْرِبْنَ"):
            return "نون النسوة"
        if tool == "لام الأمر":
            return "لام التعليل"
        if tool == "لمّا":
            return "لما"
        if token in ("سَأَلْتُكَ", "أَتْمَمْتَ", "أَمْسَكَ", "أَصْبَحَ"):
            return "ماض"
        return "حرف العلة"

    assert Counter(kind(one[2], one[3]) for one in FORWARD) == SORTED
    assert sum(SORTED.values()) == len(FORWARD)


def test_the_reverse_falls() -> None:
    """ج٢ سقط: ١١٦٠، أكثرُها حرفُ مدٍّ عارٍ عُدّ سكونًا."""

    reader = _reader()
    reverse = _census()["reverse"]
    assert isinstance(reverse, list)
    assert len(reverse) == REVERSE

    def kind(token: str) -> str:
        last = reader.units(token)[-1]
        if last[0][0] in "اوي" and last[1].get("سكون") == "عارٍ":
            return "مد عار"
        if reader.raw(token).lstrip("وف")[:1] == "أ":
            return "همزة أولا"
        return "غير ذلك"

    assert Counter(kind(one[2]) for one in reverse) == REVERSE_SORTED
    second = _one("ج٢")
    assert second.verdict(Fraction(len(reverse))) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج٢"] in second.falsifies


def test_the_control_falls() -> None:
    """ج٣ سقط: ٢٢٣ من ٦١١ دون النصف — العلاماتُ واسعة."""

    found = _census()
    assert found["control"] == CONTROL
    assert f"{float(CONTROL):.4f}" == CONTROL_SHARE
    assert found["pool"] == POOL
    assert sum(CONTROL_BY_CLASS.values()) == GOVERNED
    assert CONTROL_BY_CLASS[None] == CONTROL.numerator
    third = _one("ج٣")
    assert third.verdict(CONTROL) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ج٣"] in third.falsifies


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: لم يمرّ شرط."""
