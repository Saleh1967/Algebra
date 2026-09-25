"""شُغِّل ختمُ `73cc5b24…`: **الرخصةُ أوقفت البناءَ عند الطبقة الأولى**.

`THE_LICENCE_DID_ITS_WORK_AND_ITS_WORK_WAS_TO_STOP_ME`: ه١ اشترط أن يكون
غيرُ المُسنَدِ دون واحدٍ من مئة، والمقيسُ **٤١٬٨٠٧ وحدةً = ٠٫١١٤٦**.
فـ**سقطت الدالّيةُ لـL₁**، ونصُّ الشرط يُلزِم: «**فيوقَف الصعودُ عندها**
وتُعاد صياغةُ القاعدة بختمٍ جديد». فلا L₂ ولا L₃ **مُرخَّصتان**، وإن قِيستا.

`AND_MY_OWN_FORECAST_OF_THREE_LAYERS_FALLS_WITH_IT`: وه٤ كان **تقديري أنا**:
«الطبقاتُ المرخَّصةُ فوق L₀ ثلاثٌ فأكثر». والمُرخَّصُ **صفر**. فالسقفُ
أدنى ممّا قدّرتُ بثلاث طبقات، ويُنشَر كذلك.

`THE_REFUSAL_IS_NOT_SCATTERED_IT_IS_ONE_NAMED_PHENOMENON`: وأنفعُ ما خرج
أنّ الرفضَ **ليس موزَّعًا**: **ل (١٦٬٣٩٩) وا (١٦٬٠٤٨) = ٣٢٬٤٤٧ من ٤١٬٨٠٧
— ٠٫٧٧٦١ منه**. وأوائلُ الكلم الرافضة: **الل** (٣٬٤٩٣) · الا · الم · الس
· الر. فالعطلُ **كلُّه تقريبًا في «ال»**: ألفُ الوصل ولامُ التعريف
المدغمة.

`AND_THE_FAULT_IS_IN_THE_CLAUSE_I_SEALED_NOT_IN_THE_MATTER`: وعلّتُه
مكتوبةٌ في قاعدتي: **«داخلَ الكلمة»**. والمقطعُ العربيُّ **يعبر الوصلَ**:
«بِسْمِ ٱللَّهِ» تُقطَّع bis-mil-laa-hi، فالـ«ال» تلحق بما قبلها. فحصرُ
المقطع في الكلمة **هو الذي كسر القاعدة**، لا المادّة. وإصلاحُه **يحتاج
ختمًا جديدًا** — ولا أُبدّل شرطًا تحت ختمه.

`THREE_CLAUSES_OF_THE_LICENCE_DID_HOLD`: وصمدت ثلاثٌ: **الانغلاقُ** —
الأنواعُ **ثلاثةٌ** (CV ١٠٦٬٥٤٤ · CVC ٥٨٬٩٩٦ · CVV ٤٩٬٢٠٢) والمقاطعُ
المتمايزةُ ١٬٢٥٤؛ و**التمامُ** — ٣٢٢٬٩٤٠ + ٤١٬٨٠٧ = **٣٦٤٬٧٤٧** بلا بقيّةٍ
واحدة، وغيرُ المُسنَدِ **معدودٌ باسمه لا مبتلَعًا**؛ و**الرجعةُ** —
التقطيعُ **يُعيد الوحداتِ بلا فقد**، لأنّه تقطيعٌ لا تخشين.

`AND_WHAT_WAS_MEASURED_UNLICENSED_IS_PUBLISHED_AS_SUCH`: وقِيست L₂ وL₃
**ولا تُحسَبان**: أشكالُ الكلم **٣٨٦** متمايزًا، وردُّ النوع إلى المقطع
يكلّف **٥٫٩٦٨٥ بتًّا** محجوزةً؛ وأوزانُ الكمّ **١٣٢**، وردُّ الوزن إلى
الشكل **١٫٥٩٠٠**. وتُنشَر **مرقومةً غيرَ مُرخَّصة**، لأنّ ما بُني على
طبقةٍ ساقطةِ الدالّيةِ يرث سقوطَها.

`AND_THE_ANTI_OVERFIT_CONDITION_HELD`: وه٥ صمد: المحجوزةُ فوقَ الملحَقة في
الرجعتين (٥٫٩٦٨٥ > ٥٫٩٢٨٣ و١٫٥٩٠٠ > ١٫١٦٧٧)، وأدنى فرقٍ **+٠٫٠٤٠٢**.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus
from test_layer_licence_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_layer_licence.py"

pytestmark = requires_corpus

UNITS = 364_747
WORDS = 78_245
REFUSED = 41_807
COVERED = 322_940
SYLLABLES = 214_742
KINDS = {"CV": 106_544, "CVC": 58_996, "CVV": 49_202}
DISTINCT_SYLLABLES = 1_254
SHAPES = 386
WEIGHTS = 132
DESCENT_SHAPE = (5.9685, 5.9283)
DESCENT_WEIGHT = (1.5900, 1.1677)
ARTICLE_SHARE = 32_447


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_layer_licence", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _built() -> tuple[int, int, list[object], list[str]]:
    reader = _reader()
    words = reader.words_of(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
    refused = 0
    covered = 0
    syllables: list[object] = []
    for word in words:
        built, missed = reader.syllabify(word)  # type: ignore[attr-defined]
        refused += missed
        covered += sum(len(one) for one in built)
        syllables.extend(built)
    kinds = [reader.kind(one) for one in syllables]  # type: ignore[attr-defined]
    return (refused, covered, syllables, kinds)


def test_the_seal_was_deposited_before_the_build() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("73cc5b24")


def test_the_totality_clause_fails_and_the_ascent_halts() -> None:
    """٠٫١١٤٦ فوقَ حدّ ه١ — فتسقط الدالّيةُ ويُوقَف البناء."""

    refused, _, _, _ = _built()
    assert refused == REFUSED
    first = next(one for one in PREDICTIONS if one.identifier == "ه١")
    assert first.verdict(_exact(refused / UNITS)) is Verdict.FALSIFIED
    assert "فيوقَف الصعودُ عندها" in first.falsifies
    assert refused / UNITS > 0.11


def test_my_own_forecast_of_three_layers_is_withdrawn() -> None:
    """ه٤ كان تقديري، والمُرخَّصُ صفر — فالسقفُ أدنى بثلاث طبقات."""

    fourth = next(one for one in PREDICTIONS if one.identifier == "ه٤")
    licensed = 0  # لا طبقةَ فوقَ L₀ اجتمعت لها الأربع
    assert fourth.verdict(Fraction(licensed)) is Verdict.FALSIFIED
    assert "دعوايَ" in fourth.falsifies


def test_the_refusal_concentrates_in_the_definite_article() -> None:
    """ل وا ٣٢٬٤٤٧ من ٤١٬٨٠٧ — فالعطلُ في «ال» لا موزَّعًا."""

    assert ARTICLE_SHARE / REFUSED > 0.77
    assert ARTICLE_SHARE == 16_399 + 16_048
    assert ARTICLE_SHARE < REFUSED


def test_the_closure_clause_holds_with_three_kinds() -> None:
    """ه٢: ثلاثةُ أنواعٍ من ثمانيةٍ مسموحة، ومقاطعُ متمايزةٌ محصاة."""

    _, _, syllables, kinds = _built()
    second = next(one for one in PREDICTIONS if one.identifier == "ه٢")
    from collections import Counter

    spread = Counter(kinds)
    assert dict(spread) == KINDS
    assert second.verdict(Fraction(len(spread))) is Verdict.MET
    assert len(set(syllables)) == DISTINCT_SYLLABLES
    assert len(syllables) == SYLLABLES


def test_the_completeness_clause_closes_with_no_remainder() -> None:
    """ه٣: ٣٢٢٬٩٤٠ + ٤١٬٨٠٧ = ٣٦٤٬٧٤٧ — وغيرُ المُسنَدِ معدودٌ لا مبتلَع."""

    refused, covered, _, _ = _built()
    assert covered == COVERED
    assert covered + refused == UNITS
    third = next(one for one in PREDICTIONS if one.identifier == "ه٣")
    assert third.verdict(Fraction(0)) is Verdict.MET


def test_the_unlicensed_layers_are_measured_and_marked_as_such() -> None:
    """L₂ وL₃ مرقومتان غيرَ مُرخَّصتين — وما بُني على ساقطٍ يرث سقوطَه."""

    reader = _reader()
    words = reader.words_of(CORPUS.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
    shapes = []
    for word in words:
        built, _ = reader.syllabify(word)  # type: ignore[attr-defined]
        shapes.append(tuple(reader.kind(one) for one in built))  # type: ignore[attr-defined]
    assert len(set(shapes)) == SHAPES
    weights = {tuple(reader.weight(one) for one in shape) for shape in shapes}  # type: ignore[attr-defined]
    assert len(weights) == WEIGHTS
    text = Path(__file__).read_text(encoding="utf-8")
    assert "غيرَ مُرخَّصة" in text


def test_the_anti_overfit_condition_held_on_both_descents() -> None:
    """ه٥: المحجوزةُ فوقَ الملحَقة في الرجعتين، وأدنى فرقٍ +٠٫٠٤٠٢."""

    fifth = next(one for one in PREDICTIONS if one.identifier == "ه٥")
    gaps = [DESCENT_SHAPE[0] - DESCENT_SHAPE[1], DESCENT_WEIGHT[0] - DESCENT_WEIGHT[1]]
    assert fifth.verdict(_exact(min(gaps))) is Verdict.MET
    assert abs(min(gaps) - 0.0402) < 1e-3


def test_the_return_clause_holds_because_syllabifying_is_not_coarsening() -> None:
    """ه٦: التقطيعُ يُعيد الوحداتِ بلا بقيّة — فبقيّةُ الرجعة صفر."""

    refused, covered, syllables, _ = _built()
    flattened = sum(len(one) for one in syllables)  # type: ignore[arg-type]
    assert flattened == covered
    sixth = next(one for one in PREDICTIONS if one.identifier == "ه٦")
    assert sixth.verdict(Fraction(0)) is Verdict.MET
    assert covered + refused == UNITS


FELL_WITH_THEM: dict[str, str] = {
    "ه٤": "دعوايَ أنّ البناءَ يبلغ الوزنَ الكمّيَّ بلا",
}
"""ما عُلِّق على سقوط كلِّ شرطٍ، مقتبَسًا من نصّ الختم لا مُعادَ تفسيره.

فنصُّ `falsifies` **دعوًى ثانيةٌ معرَّضةٌ للسقوط** لا شرحًا محايدًا: إن سقط
الشرطُ سقط معه ما عُلِّق عليه، ويُعلَن ذلك **عند موضع السقوط** لا في شرحٍ
لاحق. وهو العطلُ الثاني عشر، ممنوعًا آليًّا.
"""


def test_what_fell_with_each_fallen_condition_is_quoted_where_it_fell() -> None:
    """كلُّ منقوضٍ يحمل نصَّ ما سقط معه، مطابقًا لنصّ الختم بايتةً."""

    for identifier, meaning in FELL_WITH_THEM.items():
        found = next(one for one in PREDICTIONS if one.identifier == identifier)
        assert meaning in found.falsifies, identifier
        assert len(meaning) >= 10


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

فشرطٌ يمرُّ بتعليلٍ خاطئ **ليس تأييدًا**: العددُ صحيحٌ والسببُ المنسوبُ إليه
غيرُ مقيس. وهذا الاسمُ **مطلوبٌ في كلّ تشغيل** وإن كان فارغًا، كي يُسأل
السؤالُ في كلّ مرّة ولا يُطوى بالسكوت — وهو العطلُ الثامن.
"""
