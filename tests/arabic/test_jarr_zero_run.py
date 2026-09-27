"""شُغِّل ختمُ `a57f54c1…`: **سقط ص١ — ٦٨ موضعًا بلا تفسير، كلٌّ منها بعينه**.

`THE_ZERO_FALLS`: ص١ **سقط**: المواضعُ غيرُ المفسَّرة **٦٨** على المستويات الثلاثة
(الأوّل ٣، الثاني ٢٥، الثالث ٤٠). فسقط معه: «فالفراكتالُ لا يستمرّ ١٠٠٪ بهذا
الجدول». والمواضعُ كلُّها في `UNEXPLAINED` أدناه: السطر، ورقمُ اللفظ، والمستوى،
واللفظ، وحركتُه.

`EVERY_CLASS_WORKS`: ص٢ **صمد**: عملت الأبوابُ كلُّها: الكسرة ٣٬٧٨٨، والمبنيّ
٣٨٦، والضمير المتّصل ٧١٢، والإعرابُ بالحرف ٣٥٤، والمقدَّر ١٩١، والممنوعُ وزنًا
١٢ وعلَمًا ٥٠، والاستئنافُ بعلامة وقف ٢٨.

`THE_SIXTY_EIGHT_SORTED` — **تشخيصٌ بعد التشغيل، لا حكم**:

- **٣١ — لغويٌّ متوقَّع**: في المستوى الثالث لفظٌ ليس تابعًا للمجرور، بل ابتداءُ
  جملةٍ أو عطفٌ على غيره، **بلا علامة وقف** («عَلَى اللَّهِ الْكَذِبَ»). وهذا ما
  تركه الجدولُ عن قصد.
- **١٩ — لغويٌّ ناقصٌ من الجدول**: «أَنْ» المصدريّة بعد الجارّ («عَلَى أَن
  يَخْلُقَ»): المجرورُ المصدرُ المؤوَّل، و«أَنْ» لا تُعرَب.
- **١٥ — عيبُ الأداة**: طيُّ الهمزة جعل أوّلَ اللفظ «ال» («بِأَلْسِنَتِهِمْ»،
  «آلِهَةً»، «إِلَهِكَ»).
- **٢ — نقصٌ في قائمة الأعلام**: «سَقَرَ»، و«دَاوُودَ» برسمٍ غير «داود».
- **١ — عيبُ الأداة**: فعلٌ أوّلُه «وال» («وَالْعَنْهُمْ»).
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
from test_jarr_zero_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_jarr_zero.py"

pytestmark = requires_corpus

FIRED = {
    "كسرة": 3_788,
    "مبنيّ": 386,
    "ضمير متّصل": 712,
    "إعرابٌ بالحرف": 354,
    "إعرابٌ مقدَّر": 191,
    "ممنوعٌ من الصرف: وزن": 12,
    "ممنوعٌ من الصرف: علَم": 50,
    "استئنافٌ بعلامة وقف": 28,
}
BY_LEVEL = {"١": 3, "٢": 25, "٣": 40}
SORTED = {"المستوى الثالث": 31, "أن المصدرية": 19, "طي الهمزة": 15, "علم": 2, "فعل": 1}
QUOTED_FALLEN = {"ص١": "فالفراكتالُ لا يستمرّ ١٠٠٪ بهذا الجدول"}
UNEXPLAINED = (
    (292, 7, "٣", "وَالْمُؤْمِنُونَ", "فتحة"),
    (368, 33, "٣", "الْكَذِبَ", "فتحة"),
    (371, 26, "٣", "الْكَذِبَ", "فتحة"),
    (387, 4, "٣", "الْكَذِبَ", "فتحة"),
    (437, 8, "٣", "الرُّسُلُ", "ضمة"),
    (446, 6, "٣", "وَالرَّسُولُ", "ضمة"),
    (539, 15, "١", "بِأَلْسِنَتِهِمْ", "لا حركة"),
    (543, 5, "٣", "الْكَذِبَ", "فتحة"),
    (674, 16, "٣", "وَالْمُحْصَنَاتُ", "ضمة"),
    (744, 10, "٣", "الرُّسُلُ", "ضمة"),
    (772, 17, "٣", "الْكَذِبَ", "فتحة"),
    (801, 11, "٣", "الرَّحْمَةَ", "فتحة"),
    (826, 12, "٢", "أَن", "لا حركة"),
    (843, 12, "٣", "الرَّحْمَةَ", "فتحة"),
    (854, 4, "٢", "أَن", "لا حركة"),
    (1059, 2, "٢", "أَن", "لا حركة"),
    (1245, 4, "٣", "إِلّاً", "فتحة"),
    (1347, 11, "٣", "وَالْحَافِظُونَ", "فتحة"),
    (1424, 6, "٣", "الْكَذِبَ", "فتحة"),
    (1433, 6, "٣", "الْكَذِبَ", "فتحة"),
    (1593, 13, "٣", "الْحَقُّ", "ضمة"),
    (1856, 3, "٢", "أَن", "لا حركة"),
    (1950, 10, "٣", "وَالْمَلَائِكَةُ", "ضمة"),
    (2017, 13, "٣", "الْكَذِبَ", "فتحة"),
    (2017, 19, "٣", "الْكَذِبَ", "فتحة"),
    (2117, 6, "٢", "أَن", "لا حركة"),
    (2128, 10, "٢", "أَن", "لا حركة"),
    (2141, 10, "٣", "الْكِتَابَ", "فتحة"),
    (2154, 14, "٣", "إِلَهاً", "فتحة"),
    (2155, 5, "٣", "آلِهَةً", "فتحة"),
    (2206, 6, "٢", "أَن", "لا حركة"),
    (2234, 15, "٢", "أَن", "لا حركة"),
    (2445, 17, "٢", "إِلَهِكَ", "فتحة"),
    (2507, 4, "٣", "آلِهَةً", "فتحة"),
    (2613, 12, "٣", "وَالشَّمْسُ", "ضمة"),
    (2660, 9, "٣", "وَالْفُلْكَ", "فتحة"),
    (2768, 2, "٢", "أَن", "لا حركة"),
    (2806, 2, "١", "بِأَلْسِنَتِكُمْ", "لا حركة"),
    (2858, 3, "٣", "آلِهَةً", "فتحة"),
    (3279, 9, "٢", "أَن", "لا حركة"),
    (3367, 7, "٣", "النُّبُوَّةَ", "فتحة"),
    (3484, 3, "٢", "أَن", "لا حركة"),
    (3499, 10, "٣", "الْبَاطِلُ", "ضمة"),
    (3601, 5, "٣", "وَالْعَنْهُمْ", "لا حركة"),
    (3637, 22, "٣", "الْقَوْلَ", "فتحة"),
    (3688, 12, "٣", "الْعُلَمَاءُ", "ضمة"),
    (3728, 3, "٣", "آلِهَةً", "فتحة"),
    (3786, 7, "٢", "أَن", "لا حركة"),
    (3879, 2, "٢", "آلِهَتِهِمْ", "لا حركة"),
    (3918, 2, "٢", "إِلْ", "لا حركة"),
    (3976, 7, "٢", "آلِهَتِكُمْ", "لا حركة"),
    (3992, 3, "٢", "دَاوُودَ", "فتحة"),
    (4159, 17, "٣", "الْفَسَادَ", "فتحة"),
    (4409, 4, "٣", "إِلَهٌ", "ضمة"),
    (4411, 6, "٣", "الشَّفَاعَةَ", "فتحة"),
    (4543, 13, "٢", "أَن", "لا حركة"),
    (4544, 6, "٣", "أَلَيْسَ", "فتحة"),
    (4594, 11, "١", "بِأَلْسِنَتِهِم", "لا حركة"),
    (5040, 1, "٢", "أَن", "لا حركة"),
    (5088, 26, "٣", "الْعَذَابُ", "ضمة"),
    (5105, 15, "٣", "وَاللَّهُ", "ضمة"),
    (5162, 8, "٢", "أَن", "لا حركة"),
    (5170, 6, "٣", "الْكَذِبَ", "فتحة"),
    (5416, 1, "٢", "أَن", "لا حركة"),
    (5537, 3, "٢", "سَقَرَ", "فتحة"),
    (5555, 3, "٢", "أَن", "لا حركة"),
    (5591, 4, "٢", "أَن", "لا حركة"),
    (5730, 4, "٢", "أَن", "لا حركة"),
)
"""المواضعُ الثمانية والستّون بأعيانها: (السطر، رقمُ اللفظ، المستوى، اللفظ، الحركة)."""


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_jarr_zero", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _census() -> tuple[Counter[str], list[tuple[int, int, str, str, str]], int]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().census(text)  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("a57f54c1")


def test_the_zero_falls_at_sixty_eight_named_positions() -> None:
    """ص١ سقط: ٦٨ موضعًا، كلٌّ بعينه."""

    _, unexplained, _ = _census()
    assert tuple(unexplained) == UNEXPLAINED
    assert Counter(one[2] for one in unexplained) == BY_LEVEL
    first = next(one for one in PREDICTIONS if one.identifier == "ص١")
    assert first.verdict(Fraction(len(unexplained))) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ص١"] in first.falsifies


def test_every_class_of_the_table_works() -> None:
    """ص٢ صمد: لا بابَ ميّت."""

    reader = _reader()
    fired, _, _ = _census()
    assert {one: fired[one] for one in reader.CLASSES} == FIRED
    dead = sum(1 for one in reader.CLASSES if fired[one] == 0)
    second = next(one for one in PREDICTIONS if one.identifier == "ص٢")
    assert second.verdict(Fraction(dead)) is Verdict.MET


def test_the_sixty_eight_sort_into_five_named_classes() -> None:
    """تشخيصًا: ٣١ + ١٩ + ١٥ + ٢ + ١ = ٦٨."""

    def kind(level: str, token: str) -> str:
        if token == "أَن":
            return "أن المصدرية"
        if token[0] in "آإأ" or token.startswith("بِأَ"):
            return "طي الهمزة"
        if token in ("سَقَرَ", "دَاوُودَ"):
            return "علم"
        if token == "وَالْعَنْهُمْ":
            return "فعل"
        assert level == "٣", token
        return "المستوى الثالث"

    found = Counter(kind(one[2], one[3]) for one in UNEXPLAINED)
    assert found == SORTED
    assert sum(SORTED.values()) == len(UNEXPLAINED)


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء: ص٢ آليٌّ لا تعليلَ له."""
