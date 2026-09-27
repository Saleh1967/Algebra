"""شُغِّل ختمُ `f43b9095…`: **خمسةٌ من خمسة — والأرضيّةُ ٠٫١٥٦٦ بتًّا**.

**البرهانُ في** `docs/برهان-أرضية-الرسم.md`؛ وهذا سجلُّ تشغيله.

`THE_FIRST_LOWER_BOUND_IN_THE_SERIES`: كلُّ ما قيس قبلَه حدودٌ عليا. وهذا
**حدٌّ أدنى**: لأيّ مُرمِّزٍ لا يرى إلّا رسمَ الكلمة، لا ينزل متوسّطُ شفرته
عن **٠٫١٥٦٦ بت/موضع** (٥٢٬١٣٥ بتًّا) — بحدّ شانون، **لازمًا لا مقدَّرًا**،
لأنّ التوزيعَ تجريبيٌّ على مجمَّدٍ متناهٍ.

`THE_DECOMPOSITION_IS_EXACT_TO_THE_LAST_DIGIT`: والتفكيكُ هويّةٌ لا تقريب،
والفرقُ المقيسُ **٠٫٠٠٠e+٠٠**. فالدفترُ يُقرأ بلا تحفّظ: **اللامُ (٢٫٦٣١٣)
والنونُ (٢٫٣٦٤٨) كلتاهما فوقَ «سائر الحروف» (٢٫١٧٦٥)** — وهما حرفا
التعريف والتنوين، أي **حاملا الطبقتين الوظيفيّتين**؛ **وحروفُ المدّ أدناها
(١٫١٠٢٤)**، دون نصفِ السائر، وهو ما يوجبه كونُها محمولة.

`MORE_THAN_HALF_THE_TOKENS_HAVE_AN_AMBIGUOUS_RASM`: و**٤٣٬٨١٩ من ٧٨٬٢٤٥**
(٠٫٥٦٠٠) رسمُها يحتمل أكثرَ من ضبط — خمسةُ أضعافِ ما اشترطتُه في ج٤.
ومع ذلك الأرضيّةُ ٠٫١٥٦٦، **لأنّ الالتباسَ مائلٌ شديدُ الميل**: للرسم
الواحد ضبطٌ غالبٌ وبقيّةٌ نادرة. **فكثرةُ الالتباس وضآلةُ كلفتِه يجتمعان**،
وهما يبدوان متناقضين حتّى يُفصَل العدُّ عن الوزن.

`AND_THE_AMBIGUITY_LIVES_IN_THE_CLOSED_CLASS`: وشواهدُه بأسمائها: **«من»
بأربعةَ عشرَ ضبطًا** (٢٬٧٦٣ وقوعًا)، و**«ءن» بثمانية**، و«وءن» بتسعة،
و«ءلا» بأربعة. وهي **الكلمُ الوظيفيُّ المغلق** — الطبقةُ التي سمّتها
الأطروحةُ مغلقةً بالعدّ. فالخطُّ **يقتصد حيث الفضاءُ منتهٍ ويُفصِح حيث هو
مفتوح**؛ وصفٌ مقيسٌ لا تفسيرٌ مقترَح.

`AND_MY_HELD_OUT_ESTIMATOR_FAILED_AND_IS_CLASSIFIED_NOT_PUBLISHED`: والنسخةُ
المحجوزةُ خرجت **١٫٩٢٠٧** — وهي **عطلُ مقدِّرٍ لا خبرُ لغة**: تنعيمُ
لابلاس المختومُ يوزّع كتلتَه على **٣٬٩٠٦ ضبطاتٍ** أكثرُها **مستحيلٌ طولًا**
للكلمة المعيَّنة. **ولا أبدّل المقدِّرَ تحت الختم نفسِه**: يُنشَر بعلّته
ويُوسَم غيرَ مقروء، والأصحُّ يحتاج ختمًا جديدًا.

`AND_THE_GAP_IS_WHAT_KNOWING_THE_WHOLE_WORD_BUYS`: وبين **٠٫١٥٦٦** (أرضيّةُ
مَن يرى الكلمةَ كاملةً ويعرف توزيعَ هذه المدوّنة) و**١٫٣١٧٧ ± ٠٫٠٠٥١**
(محقَّقُ مَن لم يحفظ، بحرفٍ من السياق) يقع **١٫١٦ بتًّا للموضع** — وهو
**ثمنُ معرفةِ الكلمة كاملةً**، مقيسًا لا مقدَّرًا.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus
from test_script_floor_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_script_floor.py"
PROOF = REPOSITORY / "docs" / "برهان-أرضية-الرسم.md"

pytestmark = requires_corpus

FLOOR = 0.1566
TOTAL_BITS = 52_135
POSITIONS = 332_837
WORDS = 78_245
AMBIGUOUS = 43_819
DELTA = 1.951840099090
PARTS = {
    "مدّ (ا و ي)": (0.2727, 1.1024),
    "لام": (0.1161, 2.6313),
    "نون": (0.0823, 2.3648),
    "سائرُ الحروف": (0.5289, 2.1765),
}
HELD_OUT = 1.9207
ACHIEVED = 1.3177


# **سقفُ كلّ شرطٍ محدود** — العطل ٢٦.
CEILINGS: dict[str, tuple[Fraction, str]] = {
    "ج٤": (
        Fraction(1),
        "نسبةٌ تامّة: كلُّ ما في المقام يقبل الدخولَ في البسط، فلا ممتنعَ فيه",
    ),
}


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_script_floor", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _words() -> list[tuple[tuple[str, ...], tuple[str, ...]]]:
    reader = _reader()
    return reader.words(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined,no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("f43b9095")


def test_the_floor_is_reproduced_from_the_code() -> None:
    """٠٫١٥٦٦ بتًّا للموضع، و٥٢٬١٣٥ بتًّا جملةً — يُعاد اشتقاقُها."""

    reader = _reader()
    level, bits, positions, ambiguous = reader.floor_of(_words())  # type: ignore[attr-defined]
    assert abs(level - FLOOR) < 5e-5
    assert bits == TOTAL_BITS
    assert positions == POSITIONS
    assert ambiguous == AMBIGUOUS


def test_the_lower_bound_conditions_held() -> None:
    """ج٢ الأرضيّةُ > ٠، وج٣ ≤ ٠٫٥ — فرسمُ الكلمة يعيّن أكثرَ ضبطِها."""

    second = next(one for one in PREDICTIONS if one.identifier == "ج٢")
    third = next(one for one in PREDICTIONS if one.identifier == "ج٣")
    assert second.verdict(_exact(FLOOR)) is Verdict.MET
    assert third.verdict(_exact(FLOOR)) is Verdict.MET
    assert 0 < FLOOR < 0.5


def test_the_decomposition_is_an_identity_not_an_approximation() -> None:
    """الفرقُ صفرٌ بالضبط — فالدفترُ يُقرأ بلا تحفّظ."""

    reader = _reader()
    direct, parts = reader.decompose(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
    rebuilt = sum(share * inside for share, inside in parts.values())
    first = next(one for one in PREDICTIONS if one.identifier == "ج١")
    assert first.verdict(_exact(abs(direct - rebuilt))) is Verdict.MET
    assert abs(direct - DELTA) < 1e-9
    assert abs(sum(share for share, _ in parts.values()) - 1.0) < 1e-12
    for name, (share, inside) in PARTS.items():
        measured = parts[name]
        assert abs(measured[0] - share) < 5e-5 and abs(measured[1] - inside) < 5e-5


def test_lam_and_nun_both_exceed_the_remainder_and_the_madd_is_least() -> None:
    """لامٌ ٢٫٦٣١٣ ونونٌ ٢٫٣٦٤٨ فوقَ السائر ٢٫١٧٦٥، والمدُّ ١٫١٠٢٤ أدناها."""

    inside = {name: value for name, (_, value) in PARTS.items()}
    assert inside["لام"] > inside["نون"] > inside["سائرُ الحروف"]
    assert min(inside.values()) == inside["مدّ (ا و ي)"]
    assert inside["مدّ (ا و ي)"] < inside["سائرُ الحروف"] / 1.9  # أدنى بكثير


def test_most_tokens_are_ambiguous_yet_the_floor_is_small() -> None:
    """٠٫٥٦٠٠ ملتبسة و٠٫١٥٦٦ أرضيّة — والعدُّ غيرُ الوزن."""

    fourth = next(one for one in PREDICTIONS if one.identifier == "ج٤")
    share = AMBIGUOUS / WORDS
    assert fourth.verdict(_exact(share)) is Verdict.MET
    assert share > 0.5 > FLOOR  # كثرةُ الالتباس مع ضآلة كلفته


def test_the_ambiguity_witnesses_are_closed_class_words() -> None:
    """«من» بأربعةَ عشرَ ضبطًا — والالتباسُ في الكلم الوظيفيّ المغلق."""

    reader = _reader()
    found = {rasm: (shapes, mass) for rasm, shapes, mass in reader.witnesses(_words())}  # type: ignore[attr-defined]
    assert found["من"] == (14, 2_763)
    assert found["ءن"][0] == 8
    assert "الله" in found
    for rasm in ("من", "ءن", "وءن", "ءلا"):
        assert rasm in found  # كلُّها وظيفيّةٌ مغلقة


def test_my_held_out_estimator_is_classified_not_published() -> None:
    """١٫٩٢٠٧ عطلُ تنعيمٍ — ولا يُبدَّل المقدِّرُ تحت الختم نفسِه."""

    fifth = next(one for one in PREDICTIONS if one.identifier == "ج٥")
    assert fifth.verdict(_exact(HELD_OUT - FLOOR)) is Verdict.MET
    text = PROOF.read_text(encoding="utf-8")
    assert "غيرَ مقروء" in text
    assert "٣٬٩٠٦" in text  # العلّةُ مسمّاةٌ بعددها
    assert "يحتاج ختمًا جديدًا" in text


def test_the_gap_between_floor_and_achieved_is_stated() -> None:
    """١٫١٦ بتًّا هو ثمنُ معرفةِ الكلمة كاملةً."""

    assert abs((ACHIEVED - FLOOR) - 1.1611) < 1e-3
    assert FLOOR < ACHIEVED
    text = PROOF.read_text(encoding="utf-8")
    assert "أرضيّةُ **حافظٍ" in text  # والقيدُ منشورٌ مع الرقم


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
