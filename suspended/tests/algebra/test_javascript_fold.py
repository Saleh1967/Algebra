"""قياسُ التطابقِ بين تنفيذَي الطيّ: Python و JavaScript.

**العطلُ الذي تتجنّبه**: نقلٌ يُسمّى «حرفيًّا» بلا قياس. فالنقلُ يُكتَب
مرّةً ثمّ يُصدَّق، **وما كُتِب مرّتين اختلف** (المادّةُ ٤٠) ولو مرَّ كلٌّ
منهما في موضعه. فلا يُحسَم التطابقُ إلّا بتشغيلِ التنفيذَين على
**المُدخَلاتِ نفسِها** ومقابلةِ المخرَجَين نصًّا.

**والأعدادُ تُقابَل نصًّا لا أرقامًا**: `json` في بايثون يقرأ الصحيحَ
الكبيرَ بلا حدّ، و`JSON.parse` في JavaScript يُمرّره على `Number`
فيُقرِّبه. **فلو قُوبِلت أرقامًا لخضرَّ الفحصُ على تنفيذٍ كاذب.**

`A_PORT_THAT_IS_NOT_RUN_IS_NOT_A_PORT`: وغيابُ `node` **يُصنَّف ولا
يُصفَّر**: يُتخطّى الفحصُ بسببٍ مكتوب، ولا يُحذَف من الجمع.
"""

from __future__ import annotations

import json
import random
import shutil
import subprocess
from pathlib import Path
from typing import Any, Final

import pytest

from algebra.folding import (
    Guarded,
    admissible_count,
    bits_exactly,
    fold,
    fold_any,
    offset,
    unfold,
    unfold_any,
)

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[2]
HARNESS: Final[Path] = REPOSITORY / "web" / "harness.mjs"
SOURCE: Final[Path] = REPOSITORY / "web" / "fold.js"
PAGE: Final[Path] = REPOSITORY / "web" / "index.html"

# الأشكالُ المقيسة: الحدُّ الأدنى، والمُتوسِّط، والواسعُ المحجورُ أكثرُه.
SHAPES: Final[tuple[tuple[int, int], ...]] = ((1, 0), (2, 1), (5, 3), (10, 9))

NO_NODE: Final[str] = (
    "لا مفسّرَ JavaScript في هذه البيئة، فالنقلُ غيرُ مُشغَّل — "
    "وفجوةٌ مُصنَّفةٌ ليست فجوةً مطويّة."
)

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason=NO_NODE)


def ask(vectors: list[dict[str, Any]]) -> list[str]:
    """يُشغّل المِرقاةَ على المتّجهاتِ ويُعطي القيمَ نصًّا."""

    done = subprocess.run(
        ["node", str(HARNESS)],
        input=json.dumps(vectors),
        capture_output=True,
        text=True,
        check=True,
        cwd=REPOSITORY,
    )
    got = json.loads(done.stdout)
    assert len(got) == len(vectors)
    for one in got:
        assert "error" not in one, one["error"]
    return [str(one["value"]) for one in got]


def words_of(shape: Guarded, length: int, how_many: int, seed: int) -> list[list[int]]:
    """كلماتٌ جائزةٌ مُولَّدةٌ ببذرةٍ مُودَعة — **فزائفةٌ لا عشوائيّة**."""

    die = random.Random(seed)
    built: list[list[int]] = []
    for _ in range(how_many):
        word: list[int] = []
        after_blocked = False
        for _place in range(length):
            allowed = [s for s in range(shape.size) if shape.admits(s, after_blocked)]
            symbol = die.choice(allowed)
            word.append(symbol)
            after_blocked = not shape.is_free(symbol)
        built.append(word)
    return built


@needs_node
def test_the_two_implementations_agree_on_the_count_and_the_offset() -> None:
    """`T(n)` و`off(n)` متطابقان حرفًا إلى `n = 60`."""

    vectors: list[dict[str, Any]] = []
    expected: list[str] = []
    for free, blocked in SHAPES:
        shape = Guarded(free=free, blocked=blocked)
        for length in range(0, 61):
            for kind, value in (
                ("count", admissible_count(shape, length)),
                ("offset", offset(shape, length)),
                ("bits", bits_exactly(shape, length)),
            ):
                vectors.append(
                    {"kind": kind, "free": free, "blocked": blocked, "length": length}
                )
                expected.append(str(value))
    assert ask(vectors) == expected


@needs_node
def test_the_two_implementations_agree_on_every_fold_and_unfold() -> None:
    """الطيُّ والفكُّ — بطولٍ وبلا طول — متطابقان على المتّجهاتِ نفسِها."""

    vectors: list[dict[str, Any]] = []
    expected: list[str] = []
    for free, blocked in SHAPES:
        shape = Guarded(free=free, blocked=blocked)
        for length in (0, 1, 2, 5, 9, 14):
            for word in words_of(shape, length, 6, seed=free * 100 + blocked * 10):
                here = fold(shape, tuple(word))
                anywhere = fold_any(shape, tuple(word))
                vectors += [
                    {"kind": "fold", "free": free, "blocked": blocked, "word": word},
                    {
                        "kind": "unfold",
                        "free": free,
                        "blocked": blocked,
                        "index": str(here),
                        "length": length,
                    },
                    {
                        "kind": "fold_any",
                        "free": free,
                        "blocked": blocked,
                        "word": word,
                    },
                    {
                        "kind": "unfold_any",
                        "free": free,
                        "blocked": blocked,
                        "index": str(anywhere),
                    },
                ]
                back = ",".join(str(s) for s in unfold(shape, here, length))
                whole = ",".join(str(s) for s in unfold_any(shape, anywhere))
                expected += [str(here), back, str(anywhere), whole]
    assert ask(vectors) == expected


@needs_node
def test_the_javascript_numbers_are_bigint_not_number() -> None:
    """حارسُ النوعِ: يقيس `typeof` ولا يقرأ النصَّ بحثًا عن كلمة."""

    got = ask(
        [
            {"kind": "types", "free": 5, "blocked": 3, "length": 9, "word": [0, 5, 1]},
        ]
    )
    assert got == ["bigint,bigint,bigint,bigint"]


@needs_node
def test_number_would_have_lied_and_the_place_is_measured() -> None:
    """**الحالةُ المُكذِّبة لضرورةِ `BigInt`**.

    لو كان `BigInt` زينةً لَطابَق `Number` أبدًا. فيُقاس أوّلُ موضعِ
    فراقٍ لكلِّ شكل، **ويُشترَط وجودُه**: فحصٌ يُثبت الضرورةَ لا يقنع
    بأنّ التنفيذَ الصحيحَ صحيح.

    **وتصحيحٌ قاسه هذا الفحصُ عليَّ**: ظننتُ أوّلَ الفراقِ يقع عند
    تجاوزِ ٢⁵³ بعينه، فكتبتُ ذلك شرطًا فسقط. و`T(19)` للشكل (٥،٣)
    = ١٦٧٩٩٢٥٣١٧١٨٧٥٠٠٠، **وهو فوقَ الحدِّ ووافقه `Number`**. فالحدُّ
    **حدُّ ضمانِ الصدقِ لا حدُّ وقوعِ الكذب**: فوقه يسقط الضمانُ، ولا
    يلزم أن تكذب القيمةُ في أوّلِ خطوة — إذ بعضُ الصحاحِ فوقه
    مُمثَّلٌ تمامًا (المُضاعَفاتُ الموافقة).

    فالمُثبَتُ ههنا ثلاثةٌ: أنّ الفراقَ **واقعٌ** لا محتمَل، وأنّه لا
    يقع **إلّا** فوقَ الحدّ، وأنّ فوقيّةَ الحدِّ **لا تكفي** لوقوعه.
    """

    reach = 2**53
    for free, blocked in ((5, 3), (2, 1), (10, 9)):
        shape = Guarded(free=free, blocked=blocked)
        vectors = [
            {"kind": kind, "free": free, "blocked": blocked, "length": length}
            for length in range(1, 60)
            for kind in ("count", "count_as_number")
        ]
        got = ask(vectors)
        parted: int | None = None
        agreed_above: int | None = None
        for i, length in enumerate(range(1, 60)):
            exact, loose = got[2 * i], got[2 * i + 1]
            value = admissible_count(shape, length)
            assert exact == str(value)
            # ١. **لا فراقَ تحتَ حدِّ الضمان** — مُثبَتًا على كلِّ طولٍ
            #    لا على الطولِ السابقِ للفراقِ وحدَه.
            if value <= reach:
                assert exact == loose, f"({free},{blocked}) n={length} تحتَ الحدّ"
            if exact != loose and parted is None:
                parted = length
            if exact == loose and value > reach and agreed_above is None:
                agreed_above = length
        assert parted is not None, f"({free},{blocked}): لم يفارق `Number` قطّ"
        # ٢. أوّلُ فراقٍ فوقَ الحدّ
        assert admissible_count(shape, parted) > reach
        # ٣. **وفوقيّةُ الحدِّ لا تكفي**: موضعٌ فوقه ووافق فيه `Number`
        assert agreed_above is not None and agreed_above < parted


def test_the_page_and_the_port_are_in_the_tree() -> None:
    """ما لا يُدفَع لا يُشغَّل — والصفحةُ ملفٌّ ساكنٌ بلا بناءٍ ولا تابع."""

    for path in (SOURCE, HARNESS, PAGE):
        assert path.is_file(), path
    page = PAGE.read_text(encoding="utf-8")
    assert "fold.js" in page
    # لا تابعَ خارجيًّا ولا شبكة: الصفحةُ تعمل من القرصِ وحدَه
    assert "http://" not in page and "https://" not in page
    assert "BigInt" in SOURCE.read_text(encoding="utf-8")
