"""شُغِّل ختمُ `f23fc0cd…`: **ثلاثةٌ من أربعة — صُنِّف كلُّ شيء، وسقط ك٤**.

`EVERYTHING_IS_CLASSIFIED`: بالجدول الذي وقّعه صاحبُ المستودع صارت خاناتُ
السجلّ **١٬٦٨٠ كلُّها مصنَّفة**: **الصامتةُ صفر** (ك١) **وغيرُ المصنَّف صفر**
(ك٢). ملأ الجدولُ الموقَّع **٨٢٤** خانةً كانت معلَّقة؛ منها في النحويّ **١٣**
وحدةً يذكرها باب الحرف في الكتاب فحملت نصَّه حرفيًّا، و**٩٩** بصياغة الجدول.
واقتباساتُ الكتاب **خمسةَ عشرَ** كلُّها موجودةٌ بحروفها في الملفّ `978eb9cc…`.

`THE_PLURAL_MIM_CLOSES_ITS_WORD`: ك٣ **صمد**: «مْ» آخرًا **٦٬٧٩٠** من
**١١٬١٢٠** (٠٫٦١٠٦).

`THE_FEMININE_TA_DOES_NOT`: ك٤ **سقط**: «تْ» آخرًا **٤٢٢** من **١٬٥٦١**
(٠٫٢٧٠٣) — دون النصف بكثير. فسقط معه ما قال نصُّه: «دورَ تاء التأنيث الساكنة
في الجدول الموقَّع غالبًا: إن كان أكثرُ «تْ» وسطًا فهي تاءُ بنيةٍ أكثرَ منها
لاحقة».

`WHY_IT_FELL — AFTER_THE_RUN`: **تشخيصٌ بعد التشغيل، لا حكم**: **٨١٧** من
«تْ» (أكثرُ من نصفها) **شطرُ شدّة** — «حَتَّى» ١٤٢، و«اتَّقُوا» و«اتَّخَذَ»
و«الْمُتَّقِينَ»: تاءُ الافتعال المدغمة. والختمُ عدّها في المقام ولم يستثنها،
**مع أنّ ختمَ `a581ddb9…` قبله استثنى شطرَ الشدّة في ج٤**. فهذا عطلٌ في تعريف
الشرط لا في الجدول وحده. وبلا الأشطار: **٤٢٢ من ٧٤٤** (٠٫٥٦٧٢)؛ ومن الوسط
الباقي تاءُ تأنيثٍ يليها ضمير («جَاءَتْهُمْ»). **ولا يُقلَب الحكمُ بهذا**: يحتاج
ختمًا جديدًا يستثني الشطر قبل أن يُعَدّ.

وفي «مْ» الأشطارُ **٣٬٢٤٤**، وبلاها **٠٫٨٦٢١** — وصفًا.
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
from test_signed_roles_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_unit_roles.py"
BOOK = Path(os.environ.get("NABHANI_PART_THREE", "/mnt/user-data/uploads/missing"))
"""ملفُّ «الشخصية الإسلامية» ج٣ — ليس في الشجرة؛ ويُطابَق حيث وُجد."""

pytestmark = requires_corpus

CELLS = 1_680
FILLED_BY_SIGNATURE = 824
NAHWI_FROM_BOOK = 13
NAHWI_FROM_TABLE = 99
BOOK_QUOTES = 15
MIM_LAST, MIM_ALL = 6_790, 11_120
MIM_SHARE = 0.6106
TA_LAST, TA_ALL = 422, 1_561
TA_SHARE = 0.2703
TA_SHADDA_HALVES = 817
TA_WITHOUT_HALVES = 744
TA_SHARE_WITHOUT_HALVES = 0.5672
MIM_SHADDA_HALVES = 3_244
MIM_SHARE_WITHOUT_HALVES = 0.8621
HATTA = 142

EARLIER_SEAL = "a581ddb9"
"""الختمُ السابق الذي استثنى شطرَ الشدّة في ج٤."""
BOOK_PRINT = "978eb9cc"
"""بصمةُ ملفّ الكتاب."""

QUOTED_FALLEN = {"ك٤": "فهي تاءُ بنيةٍ أكثرَ منها لاحقة"}


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_unit_roles", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _text() -> str:
    return CORPUS.read_text(encoding="utf-8").rstrip("\n")


@cache
def _registry() -> tuple[object, object]:
    return _reader().registry(_text(), signed=True)  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("f23fc0cd")
    assert _reader().BOOK_PART_THREE.startswith(BOOK_PRINT)
    earlier = REPOSITORY / "tests" / "arabic" / "test_unit_roles_seal.py"
    assert EARLIER_SEAL in earlier.read_text(encoding="utf-8")


def test_the_table_is_signed_by_the_owner() -> None:
    """سطرُ التوقيع يقول «موقَّع»، والجدولُ ١١٢ صفًّا."""

    reader = _reader()
    table = reader.signed_table()
    assert len(table) == CELLS // len(reader.LEVELS)


def test_no_cell_is_silent_and_none_is_unclassified() -> None:
    """ك١ وك٢: ١٬٦٨٠ خانةً مصنَّفةً كلُّها."""

    reader = _reader()
    rows, _ = _registry()
    first = next(one for one in PREDICTIONS if one.identifier == "ك١")
    assert first.verdict(Fraction(reader.silent_cells(rows))) is Verdict.MET
    table = reader.coverage(rows)
    left = sum(sources[reader.UNCLASSIFIED] for sources in table.values())
    second = next(one for one in PREDICTIONS if one.identifier == "ك٢")
    assert second.verdict(Fraction(left)) is Verdict.MET
    assert (
        sum(sources[reader.SIGNED] for sources in table.values()) + (NAHWI_FROM_BOOK)
        == FILLED_BY_SIGNATURE
    )
    assert table["نحوي"][reader.BOOK] == NAHWI_FROM_BOOK
    assert table["نحوي"][reader.SIGNED] == NAHWI_FROM_TABLE


def test_the_book_quotes_are_the_books_own_words() -> None:
    """خمسةَ عشرَ اقتباسًا من باب الحرف — بحروفها في الملفّ حيث وُجد."""

    reader = _reader()
    assert sum(len(one) for one in reader.BOOK_NAHWI.values()) == BOOK_QUOTES
    if not BOOK.is_file():
        pytest.skip("ملفُّ الكتاب ليس في الشجرة")
    assert reader.missing_book_quotes(BOOK) == []


def test_the_plural_mim_closes_its_word() -> None:
    """ك٣ صمد: ٦٬٧٩٠ من ١١٬١٢٠."""

    last, total = _reader().final_share(_text(), ("م", "ْ"))
    assert (last, total) == (MIM_LAST, MIM_ALL)
    share = Fraction(last, total)
    assert abs(float(share) - MIM_SHARE) < 5e-5
    third = next(one for one in PREDICTIONS if one.identifier == "ك٣")
    assert third.verdict(share) is Verdict.MET


def test_the_feminine_ta_does_not_close_most_of_its_occurrences() -> None:
    """ك٤ سقط: ٤٢٢ من ١٬٥٦١ — وأكثرُ الباقي شطرُ شدّة."""

    last, total = _reader().final_share(_text(), ("ت", "ْ"))
    assert (last, total) == (TA_LAST, TA_ALL)
    share = Fraction(last, total)
    assert abs(float(share) - TA_SHARE) < 5e-5
    fourth = next(one for one in PREDICTIONS if one.identifier == "ك٤")
    assert fourth.verdict(share) is Verdict.FALSIFIED
    assert QUOTED_FALLEN["ك٤"] in fourth.falsifies


def test_the_diagnosis_after_the_run() -> None:
    """وصفًا: ٨١٧ شطرَ شدّة في «تْ»، و٣٬٢٤٤ في «مْ»، و«حَتَّى» ١٤٢."""

    peeler = _reader()._load("run_cv_peel")
    halves = {"ت": 0, "م": 0}
    final = {"ت": 0, "م": 0}
    hatta = 0
    for line in _text().split("\n"):
        for token in line.replace("<sel>", " ").split():
            units, extras = peeler.peel(token)
            for index, (letter, state) in enumerate(units):
                if letter not in halves or state != "ْ":
                    continue
                if extras[index].get("شدّة") == "نعم":
                    halves[letter] += 1
                    hatta += "".join(c for c in token if c.isalpha()) == "حتى"
                elif index == len(units) - 1:
                    final[letter] += 1
    assert (halves["ت"], halves["م"], hatta) == (
        TA_SHADDA_HALVES,
        MIM_SHADDA_HALVES,
        HATTA,
    )
    assert TA_ALL - TA_SHADDA_HALVES == TA_WITHOUT_HALVES
    ta = final["ت"] / TA_WITHOUT_HALVES
    mim = final["م"] / (MIM_ALL - MIM_SHADDA_HALVES)
    assert abs(ta - TA_SHARE_WITHOUT_HALVES) < 5e-5
    assert abs(mim - MIM_SHARE_WITHOUT_HALVES) < 5e-5


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد — لا شيء.

ك٣ مرّ وتعليلُه «ميمُ الجمع لاحقة» مؤيَّدٌ بالتشخيص: بلا أشطار الشدّة يصير
الآخرُ أكثرَ من ستّة أعشار ما بقي. وك١ وك٢ عن السجلّ لا عن تعليل.
"""
