"""شُغِّل ختمُ `72b39b4c…`: **سقط ر١، فبطلت الأربعةُ بعده بنصّ الختم**.

`THE_TABLE_WAS_INCOMPLETE_AND_I_SAID_WHAT_FOLLOWS_IS_NOT_READ`: وقع **٣٬١٧٣**
موضعًا من **٢٦٥٬٨٤٢** (٠٫٠١١٩) في خاناتٍ جعلتُها فارغة، وحدّي واحدٌ من ألف.
وقد كتبتُ عند ر١: «فالجدولُ ناقصٌ عمّا في المدوّنة، ولا يُقرأ ما بعده».
**فالأربعةُ `VOID`**: لا تُعَدّ صامدةً ولا ساقطة، وإن طُبعت أعدادُها.

`AND_THE_EMPTY_CELLS_ARE_ALMOST_ONE_THING_FOUND_AFTER_LOOKING`: **بعد النظر**،
**٣٬١٧٠** من الثلاثة آلاف والمئة والثلاثة والسبعين **حرفٌ مشدّدٌ أوّلَ اللفظ**
— «مِّن» و«مَّا» و«لَّا» — **فالمجمَّدُ يكتب الإدغامَ عابرًا للّفظ**: «مِن
مَّاءٍ»، «يَكُن لَّهُ». والتقشيرُ يجعل الشدّةَ وحدتين أُولاهما ساكنة، **فيقع
السكونُ أوّلَ اللفظ**. وجعلتُ هذه الخانةَ فارغةً لأنّ العربيّةَ لا تبتدئ
بساكن: **صدقٌ في النطق، وخطأٌ في الوحدات**. والباقي ثلاثة: لامُ الأمر ساكنةً
مكتوبةً أوّلَ اللفظ في «لْيَقْطَعْ» و«لْيَقْضُوا»، وفاتحةُ «يس». **وقولي في
المسوّدة الأولى لهذا السجلّ «كلُّها شدّة» كان خطأً ردّه الفحص.** وهي
الظاهرةُ التي صمد بها ج٤ في `34176d22…`: النونُ العاريةُ في «مِن» يقابلها
حرفٌ مشدّدٌ في اللفظ التالي.

`AND_THE_SAME_CAUSE_HID_IN_A_FILLED_CELL`: وفي الاتّجاه الآخر: خانةُ (ن، أوّل،
سكون) ملأتُها بدورٍ واحدٍ لفاتحة «ن» وحدَها، **فدخلها ٢١٢ نونًا مشدّدةً أوّلَ
اللفظ** وعُدّت ذاتَ دورٍ واحد. **خطأٌ لا يكشفه ر١** لأنّ الخانةَ ليست فارغة.

`THE_VOID_READINGS_ARE_BOUNDED_WHATEVER_FILLS_THE_EMPTY_CELLS`: والأعدادُ
المطبوعةُ **غيرُ محكومٍ بها**: لا حرفَ محسومٌ من التسعة، وفي خانةٍ ذات دورٍ
واحد **٠٫٠٥٥٩**، ومتوسّطُ الأدوار **٢٫٧٤٠٧**، وما أسقطه الموقعُ والحال
**٠٫٧١٠١**. **وبعد النظر حُسبت حدودُها** على أيّ ملءٍ للخانات الفارغة بدورٍ
إلى أربعة: الأوّلُ يبقى تحت **٠٫٠٦٧٨**، والثاني فوق **٢٫٧٥٢٦**، والثالثُ فوق
**٠٫٦٧٧٧**. **فلا ملءَ يقلب واحدًا منها عن حدّه المختوم** — لكنّ الحكمَ بها
يحتاج ختمًا جديدًا يملأ الخانات قبل النظر.

`THE_TEN_ARE_NINE`: والحروفُ **تسعةٌ** في فضاء الـ١١٢ لا عشرة — الهمزةُ
والألفُ من «سألتمونيها» وحدةٌ واحدةٌ بالطيّ. والألفُ وحدَها **٦٥٬٦٤١** موضعًا،
ومتوسّطُ أدوارها **٣٫٥٢٩٣** من أربعة: **أثقلُ الحروف التباسًا**.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_letter_roles_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_letter_roles.py"

pytestmark = requires_corpus

ALPHABET = 112
"""فضاءُ الوحدات: ثمانيةٌ وعشرون حرفًا في أربع حالات."""
NEIGHBOUR_SEAL = "34176d22"
"""الختمُ الذي صمد فيه ج٤ بالظاهرة نفسِها."""

OCCURRENCES = 265_842
IN_EMPTY = 3_173
IN_EMPTY_SHARE = 0.0119
EMPTY_CELLS = {
    ("م", "أوّل", "سكون"): 2_185,
    ("ل", "أوّل", "سكون"): 949,
    ("و", "أوّل", "سكون"): 23,
    ("ت", "أوّل", "سكون"): 15,
    ("ي", "أوّل", "سكون"): 1,
}
SINGLE = 14_859
SINGLE_SHARE = 0.0559
CANDIDATES = 2.7407
NARROWING = 0.7101
BOUNDS = {"ر٣": 0.0678, "ر٤": 2.7526, "ر٥": 0.6777}
"""حدودُ الأعداد الباطلة على أيّ ملءٍ للخانات الفارغة بدورٍ إلى أربعة — بعد النظر."""

ALIF = (65_641, 3.5293)

EMPTY_CAUSES = {"شدّة": 3_170, "سكونٌ مكتوب": 2, "عارٍ": 1}
WRITTEN_SUKUN = ["لْيَقْطَعْ", "لْيَقْضُوا"]
NUN_IN_THE_OPENING_CELL = 212
"""نونٌ مشدّدةٌ أوّلَ اللفظ وقعت في خانةٍ ملأتُها لفاتحة «ن» — عُدّت ذاتَ دورٍ واحد."""

QUOTED_FALLEN = {"ر١": "فالجدولُ ناقصٌ عمّا في المدوّنة"}
"""ما عُلِّق على سقوط ر١ بنصّ الختم — ومنه بطلانُ ما بعده."""


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_letter_roles", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _reading() -> object:
    return _reader().read(CORPUS.read_text(encoding="utf-8"))


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ ولا خانةٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("72b39b4c")
    assert ALPHABET == 28 * 4


def test_the_table_fell_on_initial_shadda() -> None:
    """ر١ سقط: ٣٬١٧٣ من ٢٦٥٬٨٤٢ في خاناتٍ فارغة، كلُّها سكونٌ أوّلَ اللفظ."""

    reading = _reading()
    first = next(one for one in PREDICTIONS if one.identifier == "ر١")
    assert reading.occurrences == OCCURRENCES  # type: ignore[attr-defined]
    assert reading.in_empty == IN_EMPTY  # type: ignore[attr-defined]
    assert reading.empty_cells == EMPTY_CELLS  # type: ignore[attr-defined]
    share = Fraction(IN_EMPTY, OCCURRENCES)
    assert abs(float(share) - IN_EMPTY_SHARE) < 5e-5
    assert first.verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ر١"] in first.falsifies
    assert "ولا يُقرأ ما بعده" in first.falsifies


def test_after_looking_the_empty_cells_are_almost_all_a_doubled_first_letter() -> None:
    """٣٬١٧٠ شدّة، واثنتان سكونٌ مكتوب، وواحدةٌ «يس» — و٢١٢ نونًا في خانةٍ ملأى."""

    reader = _reader()
    peeler = reader._peeler()
    roles = reader.table()
    text = CORPUS.read_text(encoding="utf-8").replace(reader.MARKUP, " ")
    empty: dict[str, int] = {}
    written: list[str] = []
    nun_filled = 0
    for token in text.split():
        units, extras = peeler.peel(token)
        letter, state = units[0]
        if letter not in reader.NINE or letter == "ا" or state != "ْ":
            continue
        doubled = extras[0].get("شدّة") == "نعم"
        if roles[(letter, "أوّل", "سكون")]:
            nun_filled += doubled
            continue
        if doubled:
            kind = "شدّة"
        elif extras[0].get("سكون") == "مكتوب":
            kind = "سكونٌ مكتوب"
            written.append(token)
        else:
            kind = "عارٍ"
        empty[kind] = empty.get(kind, 0) + 1
    assert empty == EMPTY_CAUSES
    assert sum(empty.values()) == IN_EMPTY
    assert sorted(written) == sorted(WRITTEN_SUKUN)
    assert nun_filled == NUN_IN_THE_OPENING_CELL


def test_the_four_after_it_are_void_by_the_sealed_text() -> None:
    """ر٢…ر٥ باطلةٌ بسقوط ر١ — تُطبَع أعدادُها ولا يُحكَم بها."""

    reading = _reading()
    second = next(one for one in PREDICTIONS if one.identifier == "ر٢")
    third = next(one for one in PREDICTIONS if one.identifier == "ر٣")
    fourth = next(one for one in PREDICTIONS if one.identifier == "ر٤")
    fifth = next(one for one in PREDICTIONS if one.identifier == "ر٥")
    decided = Fraction(len(reading.decided_letters))  # type: ignore[attr-defined]
    single = Fraction(reading.single, OCCURRENCES)  # type: ignore[attr-defined]
    candidates = reading.candidates  # type: ignore[attr-defined]
    narrowing = reading.narrowing  # type: ignore[attr-defined]
    assert second.verdict(decided, void=True) is Verdict.VOID
    assert third.verdict(single, void=True) is Verdict.VOID
    assert fourth.verdict(candidates, void=True) is Verdict.VOID
    assert fifth.verdict(narrowing, void=True) is Verdict.VOID
    assert decided == 0
    assert reading.single == SINGLE  # type: ignore[attr-defined]
    assert abs(float(single) - SINGLE_SHARE) < 5e-5
    assert abs(float(candidates) - CANDIDATES) < 5e-5
    assert abs(float(narrowing) - NARROWING) < 5e-5


def test_after_looking_no_filling_of_the_empty_cells_moves_a_void_reading() -> None:
    """بدورٍ واحدٍ أو بأربعةٍ في كلّ فارغة: تبقى الثلاثةُ في جهة حدودها."""

    reading = _reading()
    stock = _reader().inventory(_reader().table())
    single_high = Fraction(SINGLE + IN_EMPTY, OCCURRENCES)
    candidates_low = reading.candidates + Fraction(IN_EMPTY, OCCURRENCES)  # type: ignore[attr-defined]
    empty_stock = sum(
        count * len(stock[letter]) for (letter, _, _), count in EMPTY_CELLS.items()
    )
    narrowing_low = reading.narrowing - Fraction(empty_stock, OCCURRENCES)  # type: ignore[attr-defined]
    assert abs(float(single_high) - BOUNDS["ر٣"]) < 5e-5
    assert abs(float(candidates_low) - BOUNDS["ر٤"]) < 5e-5
    assert abs(float(narrowing_low) - BOUNDS["ر٥"]) < 5e-5
    assert single_high <= Fraction(1, 2)
    assert candidates_low >= Fraction(3, 2)
    assert narrowing_low >= Fraction(1, 2)


def test_the_alif_is_the_heaviest_ambiguity() -> None:
    """الألفُ ٦٥٬٦٤١ موضعًا، ومتوسّطُ أدوارها ٣٫٥٢٩٣ — وتسعةُ حروفٍ لا عشرة."""

    reading = _reading()
    table = reading.per_letter  # type: ignore[attr-defined]
    assert len(table) == 9
    mass, mean, _, stock = table["ا"]
    assert (mass, stock) == (ALIF[0], 4)
    assert abs(float(mean) - ALIF[1]) < 5e-5
    assert max(float(one[1]) for one in table.values()) < float(mean) + 0.1


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""لا شرطَ مرّ في هذا التشغيل، فلا تعليلَ لشرطٍ مارٍّ يُسأل عنه."""
