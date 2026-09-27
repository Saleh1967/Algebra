"""شُغِّل ختمُ `d957be5b…`: **خمسةٌ من خمسة — والشاهدُ في الحركة لا في الإطار**.

`THE_FRAME_DOES_NOT_RECOVER_WHAT_WAS_DELETED`: ق١ — `H(المدّ | الإطار)`
**٠٫٤٧٢٧** بتًّا، و**٧ أُطُرٍ من ١٨** وحدَها يسترجع إطارُها مدَّه. فدعوى
«الحذفُ مسترجَعٌ بالإطار، لا بقيّةَ له» **ساقطةٌ بعددٍ لا بتأويل**.
وسببُها مرئيٌّ: إطارُ (ق·ل) يحمل `قَالَ` و`قِيلَ` و`يَقُولُ` — صورَ مادّةٍ
واحدة. فالمدُّ تابعٌ للصورة، والصورةُ ليست في الإطار.

`BUT_THE_SHORTENED_STEM_CARRIES_ITS_OWN_WITNESS`: ق٢ وق٣ — حركةُ الجذع
المقصور تحمل **٠٫٩٦٢٧** بتًّا (ضمّةٌ ٦٥ · كسرةٌ ٤١ من ١٠٦)، و`H(حركة |
إطار)` **صفرٌ تامّ**: **ثمانيةَ عشرَ إطارًا من ثمانيةَ عشرَ** حركتُها
واحدةٌ في سطوحها كلِّها. فالإفادةُ **٠٫٩٦٢٧** بتًّا كاملةً غيرَ منقوصة.

`AND_THE_FINDING_IS_PRICED_AGAINST_A_NULL_NOT_ASSERTED`: ق٤ — والتوحّدُ
مقصورٌ على ما له سطحان فأكثرُ (**١١ إطارًا · ٩٩ سطحًا**) لأنّ ذا السطح
الواحد مُوحَّدٌ بالضرورة. وفي **٢٠٬٠٠٠** خلطةٍ لم تبلغ الصدفةُ ما بلغه
المرصودُ **ولا مرّةً واحدة**: `p = 0.00005` وهو أدنى ما يُعطيه العدد.

`AND_IT_SURVIVES_THE_REMOVAL_OF_ITS_OWN_WEAKEST_FRAMES`: ق٥ — وبطرحِ
الأُطُر الأربعةِ الملتبسةِ بالسابقة (`سَمِعْنَا` · `وَسِعْتَ` · `وَحُسْنَ`
· `وَخُضْتُمْ`) وهي ليست جوفاءَ أصلًا، يبقى **٩ من ٩** و٧٨ سطحًا،
و`p = 0.00005` كما هي. فالخبرُ **في الأجوف لا في الالتباس**.

**وما لا يُدَّعى**: أنّ الحركةَ هي حرفُ الأصل. فـ`مِتْنَا` و`خِفْتُمْ`
كسرتان في مادّتين واويّتين عند الصناعة، وتسميةُ الأصل تحتاج جدولًا لا
تحمله الشجرة. **والمقيسُ إفادةُ الحركة عن الإطار، وهي مقيسةٌ تامّة.**
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from frozen_corpus import CORPUS, requires_corpus
from test_deletion_witness_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Prediction, Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_deletion_witness.py"

pytestmark = requires_corpus

FRAMES = 18
BORROWED = 4
RECOVERED = 7
LEFT_OVER = 0.4727
DAMMA = 65
KASRA = 41
SHORTENED = 106
LOAD = 0.9627
ABLE = 11
ABLE_BARE = 9
HELD = 99
HELD_BARE = 78
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ق١": (
        Fraction(317, 200),
        "إنتروبيا شرطيّةٌ لا تفوق إنتروبيا موضوعها، وشاهدُ المدّ ثلاثةٌ "
        "مُعلَنةٌ في `WEAK` بعد ردّ المقصورة — فالسقفُ `log₂٣` مجبورًا "
        "إلى ١٫٥٨٥، وهو فوق الحقيقيّ ١٫٥٨٤٩٦ فلا يردُّ مقيسًا مشروعًا",
    ),
    "ق٢": (
        Fraction(1),
        "حمولةُ موضعٍ ثنائيٍّ بالبناء: نمطُ `vowelled` لا يلتقط سوى "
        "الضمّة والكسرة، فالفضاءُ رمزان والسقفُ `log₂٢` أي بتّةٌ واحدة",
    ),
}
"""**سقفُ كلّ شرطٍ محدود** — العطل ٢٦. والفضاءان مُعلَنان في الآلة نفسِها."""

REPLICATES = 20_000
TOLD = 1 / 20_001


def _one(identifier: str) -> Prediction:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _module() -> Any:
    spec = importlib.util.spec_from_file_location("run_deletion_witness", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _measured() -> tuple[Any, Any, list[str], set[tuple[str, str]]]:
    run = _module()
    reader = run.witness_module()
    tokens = reader.read_tokens(CORPUS)
    _, frames = reader.alternating(tokens)
    return run, reader, tokens, frames


def test_the_seal_is_rederived_before_any_verdict_is_read() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد الحكم."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("d957be5b")
    assert "37633090" in ORACLE.source


def test_the_frame_does_not_recover_the_madd_it_is_said_to_recover() -> None:
    """ق١: ٠٫٤٧٢٧ بتًّا باقيةً — ودعوى الاسترجاع بالإطار تسقط بعددها."""

    run, reader, tokens, frames = _measured()
    assert len(frames) == FRAMES
    madd = run.madd_by_frame(reader, tokens, frames)
    assert sum(1 for frame in frames if len(madd[frame]) == 1) == RECOVERED
    left = run.conditional(madd)
    assert abs(left - LEFT_OVER) < 5e-5
    assert _one("ق١").verdict(_exact(left)) is Verdict.MET
    assert set(madd[("ق", "ل")]) == {"ا", "و", "ي"}  # قَالَ · يَقُولُ · قِيلَ


def test_the_vowel_carries_a_load_worth_calling_a_witness() -> None:
    """ق٢: ٠٫٩٦٢٧ بتًّا — فموضعٌ لا يحمل شيئًا لا يُسمّى شاهدًا."""

    run, reader, tokens, frames = _measured()
    rows = run.vowel_rows(reader, tokens, frames)
    assert len(rows) == SHORTENED
    spread: Counter[str] = Counter(vowel for _, vowel in rows)
    assert spread[reader.DAMMA] == DAMMA
    assert spread[reader.KASRA] == KASRA
    load = run.entropy(spread)
    assert abs(load - LOAD) < 5e-5
    assert _one("ق٢").verdict(_exact(load)) is Verdict.MET


def test_the_vowel_is_a_function_of_the_frame_with_nothing_left_over() -> None:
    """ق٣: صفرٌ تامّ — ثمانيةَ عشرَ إطارًا حركتُها واحدةٌ في سطوحها كلِّها."""

    run, reader, tokens, frames = _measured()
    by_frame = run.grouped(run.vowel_rows(reader, tokens, frames))
    assert len(by_frame) == FRAMES
    assert all(len(one) == 1 for one in by_frame.values())
    left = run.conditional(by_frame)
    assert _one("ق٣").verdict(_exact(left)) is Verdict.MET
    assert left == 0.0
    assert by_frame[("ق", "ل")][reader.DAMMA] == 44  # `قُلْنَا` وأخواتُها


def test_the_uniformity_is_priced_and_the_single_surface_frames_are_barred() -> None:
    """ق٤: ١١ من ١١ في ٩٩ سطحًا، وp = 0.00005 — وذو السطح الواحد مطروح."""

    run, reader, tokens, frames = _measured()
    rows = run.vowel_rows(reader, tokens, frames)
    met, able, held = run.uniform(run.grouped(rows))
    assert (met, able, held) == (ABLE, ABLE, HELD)
    assert run.REPLICATES == REPLICATES  # ٢٠٬٠٠٠ مُعادةً — والرقمُ مشهودٌ ههنا
    assert able < FRAMES  # فالمطروحُ ذو السطح الواحد، وطرحُه يضرّ لا ينفع
    told = run.null_reading(rows, met)
    assert abs(told - TOLD) < 1e-9
    assert _one("ق٤").verdict(_exact(told)) is Verdict.MET


def test_the_finding_survives_the_removal_of_the_ambiguous_frames() -> None:
    """ق٥: ٩ من ٩ في ٧٨ سطحًا بعد طرحِ ملتبسِ السابقة — والخبرُ في الأجوف."""

    run, reader, tokens, frames = _measured()
    borrowed = reader.proclitic_only(tokens, frames)
    assert len(borrowed) == BORROWED
    bare = [
        one for one in run.vowel_rows(reader, tokens, frames) if one[0] not in borrowed
    ]
    met, able, held = run.uniform(run.grouped(bare))
    assert (met, able, held) == (ABLE_BARE, ABLE_BARE, HELD_BARE)
    told = run.null_reading(bare, met)
    assert _one("ق٥").verdict(_exact(told)) is Verdict.MET
    assert ("م", "ع") in borrowed and ("ق", "ل") not in borrowed


def test_five_of_five_stood_and_none_fell() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ق١", "ق٢", "ق٣", "ق٤", "ق٥"}
    assert met == {one.identifier for one in PREDICTIONS}


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ق٣",)
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس**.

ق٣ مرّ بصفرٍ تامّ، والتعليلُ المتبادر — أنّ الحركةَ **تشهد لحرف الأصل
المحذوف** — **لم يُقَس ههنا ولا يُقاس بهذه الشجرة**: `مِتْنَا` و`خِفْتُمْ`
كسرتان في مادّتين واويّتين عند الصناعة، فالحركةُ تصف **الصورةَ** لا
الأصلَ فيما يظهر. والمقيسُ هو **دالّيّةُ الحركة على الإطار** وحدَها،
وتسميةُ ما تشهد له تحتاج جدولَ جذورٍ لا تحمله الشجرة. فيُسمّى ذلك ولا
يُطوى بالسكوت — وهو العطلُ الثامن.
"""
